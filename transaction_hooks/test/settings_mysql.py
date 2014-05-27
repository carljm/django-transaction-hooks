import os

from .settings import *  # noqa

DATABASES = {
    'default': {
        'ENGINE': 'transaction_hooks.backends.mysql',
        'NAME': 'dtc',
        },
    }

if 'DTC_MYSQL_USERNAME' in os.environ:
    DATABASES['default'].update(
        {
            'USER': os.environ['DTC_MYSQL_USERNAME'],
            'PASSWORD': '',
            'HOST': 'localhost',
            }
        )
