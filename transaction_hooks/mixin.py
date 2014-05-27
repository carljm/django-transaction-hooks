class TransactionHooksDatabaseWrapperMixin(object):
    """
    A ``DatabaseWrapper`` mixin to implement transaction-committed hooks.

    To use, create a package for your custom database backend and place a
    ``base.py`` module within it. Import whatever ``DatabaseWrapper`` you want
    to subclass (under some other name), and then create a ``DatabaseWrapper``
    class which inherits from both this mixin and the parent
    ``DatabaseWrapper`` (in that order).

    For an example, see ``backends/postgresql_psycopg2/base.py``.

    """
    def __init__(self, *a, **kw):
        # a list of no-argument functions to run when the transaction commits;
        # each entry is an (sids, func) tuple, where sids is a list of the
        # active savepoint IDs when this function was registered
        self.run_on_commit = []
        # Should we run the on-commit hooks the next time set_autocommit(True)
        # is called?
        self.run_commit_hooks_on_set_autocommit_on = False

        super(TransactionHooksDatabaseWrapperMixin, self).__init__(*a, **kw)

    def on_commit(self, func):
        if self.in_atomic_block:
            # transaction in progress; save for execution on commit
            self.run_on_commit.append((self.savepoint_ids[:], func))
        else:
            # no transaction in progress; execute immediately
            func()

    def run_and_clear_commit_hooks(self):
        self.validate_no_atomic_block()
        try:
            while self.run_on_commit:
                sids, func = self.run_on_commit.pop(0)
                func()
        finally:
            self.run_on_commit = []

    def commit(self, *a, **kw):
        super(TransactionHooksDatabaseWrapperMixin, self).commit(*a, **kw)

        # Atomic has not had a chance yet to restore autocommit on this
        # connection, so on databases that handle autocommit correctly, we need
        # to wait to run the hooks until it calls set_autocommit(True)
        if self.features.autocommits_when_autocommit_is_off:
            self.run_and_clear_commit_hooks()
        else:
            self.run_commit_hooks_on_set_autocommit_on = True

    def set_autocommit(self, autocommit):
        super(TransactionHooksDatabaseWrapperMixin, self).set_autocommit(
            autocommit)

        if autocommit and self.run_commit_hooks_on_set_autocommit_on:
            self.run_and_clear_commit_hooks()
            self.run_commit_hooks_on_set_autocommit_on = False

    def savepoint_rollback(self, sid, *a, **kw):
        super(TransactionHooksDatabaseWrapperMixin, self).savepoint_rollback(
            sid, *a, **kw)

        # remove any callbacks registered while this savepoint was active
        self.run_on_commit = list(filter(
            lambda x: sid not in x[0], self.run_on_commit))

    def rollback(self, *a, **kw):
        super(TransactionHooksDatabaseWrapperMixin, self).rollback(*a, **kw)

        self.run_on_commit = []

    def connect(self, *a, **kw):
        super(TransactionHooksDatabaseWrapperMixin, self).connect(*a, **kw)

        self.run_on_commit = []

    def close(self, *a, **kw):
        super(TransactionHooksDatabaseWrapperMixin, self).close(*a, **kw)

        self.run_on_commit = []
