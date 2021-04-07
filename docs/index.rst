Toggl Python API
================

.. image:: https://evrone.com/logo/evrone-sponsored-logo.png
  :width: 231
  :alt: Sponsored by evrone.com
  :target: https://evrone.com/?utm_source=github.com

Based on open `Toggl API documentation <https://github.com/toggl/toggl_api_docs/blob/master/toggl_api.md>`_

Installation
============
`pip install toggl-python` or use `poetry <https://python-poetry.org>`_ `poetry add toggl-python`

Usage example
=============

Get authenticated user time entries:

.. code-block:: python

  from toggl_python import TokenAuth, TimeEntries

  if __name__ == "__main__":
      auth = TokenAuth('AUTH_TOKEN')
      print(TimeEntries(auth=auth).list())

Get information about authenticated user:

.. code-block:: python

  from toggl_python import TokenAuth, Users

  if __name__ == "__main__":
      auth = TokenAuth('AUTH_TOKEN')
      print(Users(auth=auth).me())

Get information about authenticated user workspaces:

.. code-block:: python

  from toggl_python import TokenAuth, Workspaces

  if __name__ == "__main__":
      auth = TokenAuth('AUTH_TOKEN')
      print(Workspaces(auth=auth).list())
