from django.db.backends.postgresql_psycopg2 import base

from transaction_hooks.mixin import TransactionHooksDatabaseWrapperMixin


class DatabaseWrapper(TransactionHooksDatabaseWrapperMixin,
                      base.DatabaseWrapper):
    pass
