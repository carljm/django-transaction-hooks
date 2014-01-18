"""A PostgreSQL Django backend with hooks for transaction-deferred execution."""

from django.db.backends.postgresql_psycopg2 import base


class DatabaseWrapper(base.DatabaseWrapper):
    def __init__(self, *a, **kw):
        super(DatabaseWrapper, self).__init__(*a, **kw)

        # a list of callables to run when the transaction commits
        self.run_on_commit = []


    def on_commit(self, func):
        if self.in_atomic_block:
            self.run_on_commit.append(func)
        else:
            func()



    def commit(self, *a, **kw):
        super(DatabaseWrapper, self).commit(*a, **kw)

        while self.run_on_commit:
            func = self.run_on_commit.pop()
            func()


    def rollback(self, *a, **kw):
        super(DatabaseWrapper, self).connect(*a, **kw)

        self.run_on_commit = []


    def connect(self, *a, **kw):
        super(DatabaseWrapper, self).connect(*a, **kw)

        self.run_on_commit = []


    def close(self, *a, **kw):
        super(DatabaseWrapper, self).close(*a, **kw)

        self.run_on_commit = []
