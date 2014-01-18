Welcome to django-transaction-hooks!
========================================

Sometimes you need to fire off some non-database action related to a database
transaction, where the action should only occur if the transaction succeeds,
but you'd like to record the need for the action while the transaction is still
active. Examples might include a Celery task, an email notification, or a cache
invalidation.

Doing this correctly, especially in the face of possible savepoints within a
transaction that might be individually rolled back, is quite
difficult. ``django-transaction-hooks`` exists to handle the hard parts for
you.

Contents:

.. toctree::
   :maxdepth: 2



Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
