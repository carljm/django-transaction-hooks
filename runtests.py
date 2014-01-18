#!/usr/bin/env python
# This script exists so this dir is on sys.path when running pytest in tox.
import pytest
import os

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'transaction_hooks.test.settings_pg')

pytest.main()
