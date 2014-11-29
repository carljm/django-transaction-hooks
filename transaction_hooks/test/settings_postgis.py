import os

try:
    from psycopg2cffi import compat
    compat.register()
except ImportError:
    pass

from .settings import *  # noqa

DATABASES = {
    'default': {
        'ENGINE': 'transaction_hooks.backends.postgis',
        'NAME': 'dtc',
        },
    }


if 'DTC_PG_USERNAME' in os.environ:
    DATABASES['default'].update(
        {
            'USER': os.environ['DTC_PG_USERNAME'],
            'PASSWORD': '',
            'HOST': 'localhost',
            }
        )
