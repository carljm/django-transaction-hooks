from .settings import *

import os

DATABASES = {
    'default': {
        'ENGINE': 'transaction_hooks.backends.sqlite3',
        'TEST_NAME': os.path.join(
            os.path.dirname(os.path.abspath('__file__')),
            'testdb.sqlite',
            )
        },
    }
