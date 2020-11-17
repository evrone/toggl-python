Toggl Python API
================

![https://pypi.python.org/pypi/toggl_python](https://img.shields.io/pypi/v/toggl_python.svg) ![https://travis-ci.com/evrone/toggl_python](https://img.shields.io/travis/evrone/toggl_python.svg) ![https://toggl-python.readthedocs.io/en/latest/?badge=latest](https://readthedocs.org/projects/toggl-python/badge/?version=latest) ![https://pyup.io/repos/github/evrone/toggl_python/](https://pyup.io/repos/github/evrone/toggl_python/shield.svg)


Toggl Python API
----------------
[<img src="https://evrone.com/logo/evrone-sponsored-logo.png" width=231>](https://evrone.com/?utm_source=github.com)  
* Based on open Toggl API documentation: https://github.com/toggl/toggl_api_docs/blob/master/toggl_api.md
* Free software: MIT license
* Documentation: https://toggl-python.readthedocs.io.  


Installation
------------
`pip install toggl-python` or use [poetry](https://python-poetry.org) `poetry add toggl-python`

Features
--------

- Get TimeEntries.

```python
from toggl_python import TokenAuth, TimeEntries

if __name__ == "__main__":
    auth = TokenAuth('AUTH_TOKEN')
    print(TimeEntries(auth=auth).list())
```

* *TODO*

Credits
-------

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) project template.
