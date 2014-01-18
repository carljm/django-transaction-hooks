from django.db.backends.sqlite3 import base

from transaction_hooks.mixin import TransactionHooksDatabaseWrapperMixin


class DatabaseWrapper(TransactionHooksDatabaseWrapperMixin,
                      base.DatabaseWrapper):
    pass
