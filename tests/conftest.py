from typing import Generator

import pytest
from respx import MockRouter
from respx import mock as respx_mock
from toggl_python.api import ROOT_URL
from toggl_python.auth import TokenAuth
from toggl_python.entities.report_time_entry import REPORT_ROOT_URL, ReportTimeEntry
from toggl_python.entities.user import CurrentUser
from toggl_python.entities.workspace import Workspace

from tests.responses.me_get import FAKE_TOKEN


@pytest.fixture()
def response_mock() -> Generator[MockRouter, None, None]:
    with respx_mock(base_url=ROOT_URL) as mock_with_base_url:
        yield mock_with_base_url


@pytest.fixture()
def response_report_mock() -> Generator[MockRouter, None, None]:
    with respx_mock(base_url=REPORT_ROOT_URL) as mock_with_base_url:
        yield mock_with_base_url


@pytest.fixture()
def authed_current_user() -> CurrentUser:
    auth = TokenAuth(token=FAKE_TOKEN)

    return CurrentUser(auth=auth)


@pytest.fixture()
def authed_workspace() -> Workspace:
    auth = TokenAuth(token=FAKE_TOKEN)

    return Workspace(auth=auth)


@pytest.fixture()
def authed_report_time_entry() -> ReportTimeEntry:
    auth = TokenAuth(token=FAKE_TOKEN)

    return ReportTimeEntry(auth=auth)
