"""A PostgreSQL Django backend with hooks for transaction-deferred execution."""

from django.db.backends.postgresql_psycopg2 import base


class DatabaseWrapper(base.DatabaseWrapper):
    def __init__(self, *a, **kw):
        super(DatabaseWrapper, self).__init__(*a, **kw)

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



    def commit(self, *a, **kw):
        super(DatabaseWrapper, self).commit(*a, **kw)

        for sids, func in self.run_on_commit:
            func()

        self.run_on_commit = []


    def savepoint_rollback(self, sid, *a, **kw):
        super(DatabaseWrapper, self).savepoint_rollback(sid, *a, **kw)

        # remove any callbacks registered while this savepoint was active
        self.run_on_commit = list(filter(
            lambda x: sid not in x[0], self.run_on_commit))


    def rollback(self, *a, **kw):
        super(DatabaseWrapper, self).connect(*a, **kw)

        self.run_on_commit = []


    def connect(self, *a, **kw):
        super(DatabaseWrapper, self).connect(*a, **kw)

        self.run_on_commit = []


    def close(self, *a, **kw):
        super(DatabaseWrapper, self).close(*a, **kw)

        self.run_on_commit = []
