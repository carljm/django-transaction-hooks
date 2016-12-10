Contributing
============

Thanks for your interest in contributing!

Django-transaction-hooks has been merged into Django 1.9. Thus, this package
will receive no changes other than possibly backports of changes to the same
feature in core Django (as long as Django 1.8 is supported). So if you've found
a bug, first check if it exists in core Django, and if so file it on `the
Django issue tracker`_. If you'd like to suggest a feature, please suggest it
on the Django issue tracker or `development mailing list`_.

If you find a bug in this third-party package that does not exist in core
Django, this is the only case where you should file bugs and send pull requests
to the django-transaction-hooks `GitHub repository`_ and `issue tracker`_.

.. _Django issue tracker: https://code.djangoproject.com/
.. _development mailing list: https://groups.google.com/forum/#!forum/django-developers
.. _GitHub repository: https://github.com/carljm/django-transaction-hooks/
.. _issue tracker: https://github.com/carljm/django-transaction-hooks/issues


Submitting Issues
-----------------

Issues are easier to reproduce/resolve when they have:

- A pull request with a failing test demonstrating the issue
- A code example that produces the issue consistently
- A traceback (when applicable)


Pull Requests
-------------

When creating a pull request:

- Write tests (see below)
- Note user-facing changes in the `CHANGES`_ file
- Update the documentation as needed
- Add yourself to the `AUTHORS`_ file

.. _AUTHORS: AUTHORS.rst
.. _CHANGES: CHANGES.rst


Testing
-------

Please add tests for any changes you submit. The tests should fail before your
code changes, and pass with your changes. Existing tests should not
break. Coverage (see below) should remain at 100% following a full tox run.

To install all the requirements for running the tests::

    pip install -r requirements.txt

To run the tests once::

    ./runtests.py

(This runs the tests on SQLite.)

To run tox (which runs the tests across all supported Python and Django
versions and databases) and generate a coverage report in the ``htmlcov/``
directory::

    make test

This requires that you have ``python2.6``, ``python2.7``, ``python3.2``,
``python3.3``, ``python3.4``, ``pypy``, and ``pypy3`` binaries on your system's
shell path.

It also requires that you have local PostgreSQL and MySQL servers running with
a ``dtc`` database on each.

To install PostgreSQL and create the required database on Debian-based
systems::

    $ sudo apt-get install postgresql
    $ createdb dtc

To install MySQL and create the required database on Debian-based systems::

    $ sudo apt-get install mysql-server

    # Connect to MySQL as a user with permission to create databases:
    mysql> CREATE DATABASE dtc;

You'll also need to run the tests as a user with permission to create
databases. By default, the tests attempt to connect as a user with your shell
username. You can override this by setting the environment variables
``DTC_PG_USERNAME`` and ``DTC_MYSQL_USERNAME``.
