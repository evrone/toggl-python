from typing import Generator

import pytest
from respx import MockRouter
from respx import mock as respx_mock
from toggl_python.api import ROOT_URL


@pytest.fixture()
def response_mock() -> Generator[MockRouter, None, None]:
    with respx_mock(base_url=ROOT_URL) as mock_with_base_url:
        yield mock_with_base_url
