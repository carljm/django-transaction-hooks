from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'transaction_hooks.backends.sqlite3',
        },
    }
