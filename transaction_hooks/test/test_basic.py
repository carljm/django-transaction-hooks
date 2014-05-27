from django.db import connection
from django.db.transaction import atomic
import pytest

from .models import Thing


class Tracker(object):
    """Simulate the pattern of creating a DB object and notifying about it."""
    def __init__(self):
        self.notified = []

    def notify(self, id_):
        if id_ == 'error':
            raise ForcedError()
        self.notified.append(id_)

    def do(self, num):
        """Create a Thing instance and notify about it."""
        Thing.objects.create(num=num)
        connection.on_commit(lambda: self.notify(num))

    def assert_done(self, nums):
        self.assert_notified(nums)
        assert sorted(t.num for t in Thing.objects.all()) == sorted(nums)

    def assert_notified(self, nums):
        assert self.notified == nums


@pytest.fixture
def track():
    """Return a new ``Tracker`` instance."""
    return Tracker()


class ForcedError(Exception):
    pass


@pytest.mark.usefixtures('transactional_db')
class TestConnectionOnCommit(object):
    """
    Tests for connection.on_commit().

    Creation/checking of database objects in parallel with callback tracking is
    to verify that the behavior of the two match in all tested cases.

    """
    def test_executes_immediately_if_no_transaction(self, track):
        track.do(1)
        track.assert_done([1])

    def test_delays_execution_until_after_transaction_commit(self, track):
        with atomic():
            track.do(1)
            track.assert_notified([])
        track.assert_done([1])

    def test_does_not_execute_if_transaction_rolled_back(self, track):
        try:
            with atomic():
                track.do(1)
                raise ForcedError()
        except ForcedError:
            pass

        track.assert_done([])

    def test_executes_only_after_final_transaction_committed(self, track):
        with atomic():
            with atomic():
                track.do(1)
                track.assert_notified([])
            track.assert_notified([])
        track.assert_done([1])

    def test_discards_hooks_from_rolled_back_savepoint(self, track):
        with atomic():
            # one successful savepoint
            with atomic():
                track.do(1)
            # one failed savepoint
            try:
                with atomic():
                    track.do(2)
                    raise ForcedError()
            except ForcedError:
                pass
            # another successful savepoint
            with atomic():
                track.do(3)

        # only hooks registered during successful savepoints execute
        track.assert_done([1, 3])

    def test_no_hooks_run_from_failed_transaction(self, track):
        """If outer transaction fails, no hooks from within it run."""
        try:
            with atomic():
                with atomic():
                    track.do(1)
                raise ForcedError()
        except ForcedError:
            pass

        track.assert_done([])

    def test_inner_savepoint_rolled_back_with_outer(self, track):
        with atomic():
            try:
                with atomic():
                    with atomic():
                        track.do(1)
                    raise ForcedError()
            except ForcedError:
                pass
            track.do(2)

        track.assert_done([2])

    def test_no_savepoints_atomic_merged_with_outer(self, track):
        with atomic():
            with atomic():
                track.do(1)
                try:
                    with atomic(savepoint=False):
                        raise ForcedError()
                except ForcedError:
                    pass

        track.assert_done([])

    def test_inner_savepoint_does_not_affect_outer(self, track):
        with atomic():
            with atomic():
                track.do(1)
                try:
                    with atomic():
                        raise ForcedError()
                except ForcedError:
                    pass

        track.assert_done([1])

    def test_runs_hooks_in_order_registered(self, track):
        with atomic():
            track.do(1)
            with atomic():
                track.do(2)
            track.do(3)

        track.assert_done([1, 2, 3])

    def test_hooks_cleared_after_successful_commit(self, track):
        with atomic():
            track.do(1)
        with atomic():
            track.do(2)

        track.assert_done([1, 2])  # not [1, 1, 2]

    def test_hooks_cleared_after_rollback(self, track):
        try:
            with atomic():
                track.do(1)
                raise ForcedError()
        except ForcedError:
            pass

        with atomic():
            track.do(2)

        track.assert_done([2])

    def test_hooks_cleared_on_reconnect(self, track):
        with atomic():
            track.do(1)
            connection.close()

        connection.connect()

        with atomic():
            track.do(2)

        track.assert_done([2])

    def test_error_in_hook_doesnt_prevent_clearing_hooks(self, track):
        try:
            with atomic():
                connection.on_commit(lambda: track.notify('error'))
        except ForcedError:
            pass

        with atomic():
            track.do(1)

        track.assert_done([1])

    def test_db_query_in_hook(self, track):
        with atomic():
            Thing.objects.create(num=1)
            connection.on_commit(
                lambda: [track.notify(t.num) for t in Thing.objects.all()])

        track.assert_done([1])

    # On databases that don't work with autocommit off (SQLite), Atomic doesn't
    # ever call set_autocommit(True) after committing a transaction (it sets
    # ``connection.autocommit = True`` directly instead), so we have to run
    # hooks immediately on commit instead of waiting for autocommit to be
    # restored. If a hook tries to create an internal transaction of its own,
    # this fails with an error. Need a better solution here; could be fixed if
    # transaction-hooks is merged into Django.
    @pytest.mark.xfail(
        connection.features.autocommits_when_autocommit_is_off,
        reason="Can't open transaction in a hook on SQLite",
    )
    def test_transaction_in_hook(self, track):
        def on_commit():
            with atomic():
                t = Thing.objects.create(num=1)
                track.notify(t.num)

        with atomic():
            connection.on_commit(on_commit)

        track.assert_done([1])
