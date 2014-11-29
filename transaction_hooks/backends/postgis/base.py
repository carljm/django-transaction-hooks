from django.contrib.gis.db.backends.postgis import base

from transaction_hooks.mixin import TransactionHooksDatabaseWrapperMixin


class DatabaseWrapper(TransactionHooksDatabaseWrapperMixin,
                      base.DatabaseWrapper):
    pass
