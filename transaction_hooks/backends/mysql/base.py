from django.db.backends.mysql import base

from transaction_hooks.mixin import TransactionHooksDatabaseWrapperMixin


class DatabaseWrapper(TransactionHooksDatabaseWrapperMixin,
                      base.DatabaseWrapper):
    pass
