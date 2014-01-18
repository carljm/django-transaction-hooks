import django
from django.db import connection
from django.db.transaction import atomic
import pytest


# Make sure Django app registry is ready (in 1.7+); workaround for
# pytest-django not being updated to 1.7+ yet.
@pytest.mark.tryfirst
@pytest.fixture(scope='session', autouse=True)
def setup_django():
    setup = getattr(django, 'setup', lambda: None)
    setup()



class CallTrack(object):
    """An object that can be called, and tracks its calls."""
    def __init__(self):
        self.calls = []


    def __call__(self, id_):
        self.calls.append(id_)



@pytest.fixture
def track():
    """Return a new ``CallTrack`` instance."""
    return CallTrack()



class ForcedError(Exception):
    pass



@pytest.mark.usefixtures('transactional_db')
class TestConnectionOnCommit(object):
    """Tests for connection.on_commit()."""
    def test_executes_immediately_if_no_transaction(self, track):
        connection.on_commit(lambda: track(1))
        assert track.calls == [1]


    def test_delays_execution_until_after_transaction_commit(self, track):
        with atomic():
            connection.on_commit(lambda: track(1))
            assert not track.calls
        assert track.calls == [1]


    def test_does_not_execute_if_transaction_rolled_back(self, track):
        try:
            with atomic():
                connection.on_commit(lambda: track(1))
                raise ForcedError()
        except ForcedError:
            pass

        assert not track.calls


    def test_executes_only_after_final_transaction_committed(self, track):
        with atomic():
            with atomic():
                connection.on_commit(lambda: track(1))
                assert not track.calls
            assert not track.calls
        assert track.calls == [1]


    def test_discards_hooks_from_rolled_back_savepoint(self, track):
        with atomic():
            # one successful savepoint
            with atomic():
                connection.on_commit(lambda: track(1))
            # one failed savepoint
            try:
                with atomic():
                    connection.on_commit(lambda: track(2))
                    raise ForcedError()
            except ForcedError:
                pass
            # another successful savepoint
            with atomic():
                connection.on_commit(lambda: track(3))

        # only hooks registered during successful savepoints execute
        assert track.calls == [1, 3]


    def test_no_hooks_run_from_failed_transaction(self, track):
        """If outer transaction fails, no hooks from within it run."""
        try:
            with atomic():
                with atomic():
                    connection.on_commit(lambda: track(1))
                raise ForcedError()
        except ForcedError:
            pass

        assert not track.calls


    def test_inner_savepoint_rolled_back_with_outer(self, track):
        with atomic():
            try:
                with atomic():
                    with atomic():
                        connection.on_commit(lambda: track(1))
                    raise ForcedError()
            except ForcedError:
                pass
            connection.on_commit(lambda: track(2))

        assert track.calls == [2]


    def test_no_savepoints_atomic_merged_with_outer(self, track):
        with atomic():
            with atomic():
                connection.on_commit(lambda: track(1))
                try:
                    with atomic(savepoint=False):
                        raise ForcedError()
                except ForcedError:
                    pass

        assert not track.calls


    def test_inner_savepoint_does_not_affect_outer(self, track):
        with atomic():
            with atomic():
                connection.on_commit(lambda: track(1))
                try:
                    with atomic():
                        raise ForcedError()
                except ForcedError:
                    pass

        assert track.calls == [1]


    def test_hooks_cleared_after_successful_commit(self, track):
        with atomic():
            connection.on_commit(lambda: track(1))
        with atomic():
            connection.on_commit(lambda: track(2))

        assert track.calls == [1, 2] # not [1, 1, 2]


    def test_hooks_cleared_after_rollback(self, track):
        try:
            with atomic():
                connection.on_commit(lambda: track(1))
                raise ForcedError()
        except ForcedError:
            pass

        with atomic():
            connection.on_commit(lambda: track(2))

        assert track.calls == [2]


    def test_hooks_cleared_on_reconnect(self, track):
        with atomic():
            connection.on_commit(lambda: track(1))
            connection.close()

        connection.connect()

        with atomic():
            connection.on_commit(lambda: track(2))

        assert track.calls == [2]


    def test_runs_hooks_in_order_registered(self, track):
        with atomic():
            connection.on_commit(lambda: track(1))
            with atomic():
                connection.on_commit(lambda: track(2))
            connection.on_commit(lambda: track(3))

        assert track.calls == [1, 2, 3]
