============================
django-transaction-hooks
============================

.. image:: https://secure.travis-ci.org/carljm/django-transaction-hooks.png?branch=master
   :target: http://travis-ci.org/carljm/django-transaction-hooks
   :alt: Test status
.. image:: https://coveralls.io/repos/carljm/django-transaction-hooks/badge.png?branch=master
   :target: https://coveralls.io/r/carljm/django-transaction-hooks
   :alt: Test coverage
.. image:: https://readthedocs.org/projects/django-transaction-hooks/badge/?version=latest
   :target: https://readthedocs.org/projects/django-transaction-hooks/?badge=latest
   :alt: Documentation Status
.. image:: https://badge.fury.io/py/django-transaction-hooks.svg
   :target: https://pypi.python.org/pypi/django-transaction-hooks
   :alt: Latest version

Django database backends with post-transaction-commit callback hooks.

This project has been merged into Django and is now core functionality in
Django 1.9+. It should not be used with any Django version later than 1.8, and
will not receive any updates except for backports of changes to the same
functionality in core Django.

``django-transaction-hooks`` supports `Django`_ 1.6.1 through 1.8 on Python
2.6, 2.7, 3.2, 3.3, 3.4, and 3.5.

.. _Django: http://www.djangoproject.com/


Getting Help
============

Documentation for django-transaction-hooks is available at
https://django-transaction-hooks.readthedocs.io/

This app is available on `PyPI`_ and can be installed with ``pip install
django-transaction-hooks``.

.. _PyPI: https://pypi.python.org/pypi/django-transaction-hooks/


Contributing
============

See the `contributing docs`_.

.. _contributing docs: https://github.com/carljm/django-transaction-hooks/blob/master/CONTRIBUTING.rst

