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
        super(TransactionHooksDatabaseWrapperMixin, self).__init__(*a, **kw)

        # a list of no-argument functions to run when the transaction commits;
        # each entry is an (sids, func) tuple, where sids is a list of the
        # active savepoint IDs when this function was registered
        self.run_on_commit = []


    def on_commit(self, func):
        if self.in_atomic_block:
            # transaction in progress; save for execution on commit
            self.run_on_commit.append((self.savepoint_ids[:], func))
        else:
            # no transaction in progress; execute immediately
            func()


    def run_and_clear_commit_hooks(self):
        try:
            for sids, func in self.run_on_commit:
                func()
        finally:
            self.run_on_commit = []


    def commit(self, *a, **kw):
        super(TransactionHooksDatabaseWrapperMixin, self).commit(*a, **kw)

        self.run_and_clear_commit_hooks()


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
