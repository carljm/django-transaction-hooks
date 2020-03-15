CHANGES
=======

0.3 (2020.03.15)
----------------

* Formally deprecate and archive the project; it is included as part of all
  Django versions since 1.9. Use the version included in Django and report any
  bugs or issues to Django; this standalone app is not maintained.

* Drop support for Python 2.6, Python 3.2, and Django 1.6.


0.2 (2014.11.29)
----------------

* Add built-in PostGIS backend. Merge of GH-16, fixes GH-14. Thanks Bertrand
  Bordage.


0.1.4 (2014.05.27)
------------------

* Make it possible to execute a transaction within an on-commit hook (except on
  SQLite). Merge of GH-9, fixes GH-8. Thanks Marek Malek.


0.1.3 (2014.01.24)
-------------------

* Fix failure when mixing-in with database backends that perform queries in
  ``__init__`` (e.g. PostGIS backend when ``POSTGIS_VERSION`` setting is not
  set). Merge of GH-6, fixes GH-5. Thanks Niels Sandholt Busch.


0.1.2 (2014.01.21)
------------------

* Fix bug where running queries in an ``on_commit`` hook under Postgres caused
  an "autocommit cannot be used inside a transaction" error. (GH-4).


0.1.1 (2014.01.18)
------------------

* Clear run-on-commit hooks even if one raises an exception. Thanks akaariai.


0.1 (2014.01.18)
----------------

* Initial working version; support for SQLite3, PostgreSQL, MySQL.
