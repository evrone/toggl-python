from __future__ import annotations

import os
import time
from typing import TYPE_CHECKING, Generator

import pytest
from toggl_python.auth import TokenAuth
from toggl_python.entities.report_time_entry import ReportTimeEntry
from toggl_python.entities.user import CurrentUser
from toggl_python.entities.workspace import Workspace


if TYPE_CHECKING:
    from toggl_python.schemas.current_user import MePreferencesResponse, MeResponse


@pytest.fixture(scope="session")
def i_authed_user() -> CurrentUser:
    token = os.environ["TOGGL_TOKEN"]
    auth = TokenAuth(token=token)

    return CurrentUser(auth=auth)


@pytest.fixture(scope="session")
def i_authed_workspace() -> Workspace:
    token = os.environ["TOGGL_TOKEN"]
    auth = TokenAuth(token=token)

    return Workspace(auth=auth)


@pytest.fixture(scope="session")
def i_authed_report_time_entry() -> ReportTimeEntry:
    token = os.environ["TOGGL_TOKEN"]
    auth = TokenAuth(token=token)

    return ReportTimeEntry(auth=auth)


@pytest.fixture()
def me_response(i_authed_user: CurrentUser) -> MeResponse:
    return i_authed_user.me()


@pytest.fixture()
def me_preferences_response(i_authed_user: CurrentUser) -> MePreferencesResponse:
    return i_authed_user.preferences()


@pytest.fixture(autouse=True)
def slow_down_tests() -> Generator[None, None, None]:
    """Wait for some time between separate tests to avoid API rate limiting.

    Toggl API uses Leaky Bucket, recommended rate is 1 request per second per API token.
    """
    yield
    time.sleep(1)
