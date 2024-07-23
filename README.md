# Toggl Python API

![https://pypi.python.org/pypi/toggl_python](https://img.shields.io/pypi/v/toggl_python.svg) [![Supported python versions](https://img.shields.io/pypi/pyversions/toggl_python.svg?style=flat-square)](https://pypi.python.org/pypi/toggl_python) [![MIT License](https://img.shields.io/pypi/l/aiogram.svg?style=flat-square)](https://opensource.org/licenses/MIT)


* Based on open [Toggl API documentation](https://engineering.toggl.com/docs/)
* [Documentation](https://toggl-python.readthedocs.io)

## Warning

The package is currently broken because it uses **deprecated** Toggl API V8. Migration to V9 is currently in progress.

## Development

In order to run tests using different Python versions, please follow these steps:
* Install `pyenv`
* Install all supported Python versions - `pyenv install 3.8.* 3.9.* ...`
* Run `pyenv local 3.8.* 3.9.* ...`
* Run `poetry run nox`

## Credits
-------

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) project template.

[<img src="https://evrone.com/logo/evrone-sponsored-logo.png" width=231>](https://evrone.com/?utm_source=github.com)
