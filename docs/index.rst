toggl-python
============

|https://pypi.python.org/pypi/toggl_python| |Supported python versions|
|MIT License|

Typed python wrapper for ``Toggl API`` with pre-validation to avoid
extra network usage.

-  Based on `Toggl API <https://engineering.toggl.com/docs/>`__
-  `Documentation <https://toggl-python.readthedocs.io>`__

Important Note
--------------

Migration to API V9 is currently in progress. Many methods are not
implemented yet. Feel free to open an issue to escalate their
implementation.

Install
-------

``pip install toggl-python``

Usage
-----

Fetch information about current user via ``TokenAuth`` (``TOGGL_TOKEN``
is required):

.. code:: python

   from toggl_python.auth import TokenAuth
   from toggl_python.entities.user import CurrentUser


   if __name__ == "__main__":
       auth = TokenAuth(token="TOGGL_TOKEN")
       CurrentUser(auth=auth).me()

``Basic Auth`` is also supported.

.. code:: python

   from toggl_python.auth import BasicAuth
   from toggl_python.entities.user import CurrentUser


   if __name__ == "__main__":
       auth = BasicAuth(username="username", password="password")
       CurrentUser(auth=auth).me()

Package supports different input formats for ``datetime`` arguments:

-  ``str``:

.. code:: python

   from toggl_python.auth import TokenAuth
   from toggl_python.entities.user import CurrentUser


   if __name__ == "__main__":
       auth = TokenAuth(token="TOGGL_TOKEN")
       CurrentUser(auth=auth).get_time_entries(
           start_date="2024-01-01",
           end_date="2024-02-01T15:00:00-02:00",
       )

-  ``datetime``:

.. code:: python

   from datetime import datetime, timezone

   from toggl_python.auth import TokenAuth
   from toggl_python.entities.user import CurrentUser


   if __name__ == "__main__":
       auth = TokenAuth(token="TOGGL_TOKEN")
       CurrentUser(auth=auth).get_time_entries(
           start_date=datetime(2024, 1, 1, tzinfo=timezone.utc),
           end_date=datetime(2024, 2, 1, 15, tzinfo=timezone.utc),
       )

Query params are available as well:

.. code:: python

   from toggl_python.auth import TokenAuth
   from toggl_python.entities.workspace import Workspace


   if __name__ == "__main__":
       auth = TokenAuth(token="TOGGL_TOKEN")
       workspace_id = "WORKSPACE_ID"
       Workspace(auth=auth).get_projects(active=True)

Pre-validation to avoid extra network usage:

.. code:: python

   from datetime import datetime, timezone

   from toggl_python.auth import TokenAuth
   from toggl_python.entities.workspace import Workspace


   if __name__ == "__main__":
       auth = TokenAuth(token="TOGGL_TOKEN")
       workspace_id = "WORKSPACE_ID"
       since = datetime(2024, 1, 20, tzinfo=timezone.utc)
       # Assume that datetime.now is 2024-05-01
       Workspace(auth=auth).list(since=since)

       # ValidationError: Since cannot be older than 3 months

Development
-----------

``poetry`` is required during local setup.

Run ``poetry install --no-root`` to setup local environment.
``pre-commit install`` is also advisable.

Unit Testing
~~~~~~~~~~~~

In order to run tests using different Python versions, please follow
these steps: \* Install ``pyenv`` \* Install all supported Python
versions - ``pyenv install 3.8.* 3.9.* ...`` \* Run
``pyenv local 3.8.* 3.9.* ...`` \* Run ``poetry run nox``

To run classic unit tests, execute ``pytest -m "not integration"``

Integration Testing
~~~~~~~~~~~~~~~~~~~

Pre-defined ``Workspace`` and ``Project`` are required to have in
``Toggl`` system.

Command
``TOGGL_TOKEN=... WORKSPACE_ID=... PROJECT_ID=... USER_ID=... TOGGL_PASSWORD=... pytest -m integration``

Credits
-------

This package follows
`evrone-python-guidelines <https://github.com/evrone/evrone-python-guidelines>`__
and uses configs from
`evrone-django-template <https://github.com/evrone/evrone-django-template>`__.

` <https://evrone.com/?utm_source=github.com>`__

.. |https://pypi.python.org/pypi/toggl_python| image:: https://img.shields.io/pypi/v/toggl_python.svg
.. |Supported python versions| image:: https://img.shields.io/pypi/pyversions/toggl_python.svg?style=flat-square
   :target: https://pypi.python.org/pypi/toggl_python
.. |MIT License| image:: https://img.shields.io/pypi/l/aiogram.svg?style=flat-square
   :target: https://opensource.org/licenses/MIT
