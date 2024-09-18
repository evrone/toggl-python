from __future__ import annotations

import os
from datetime import timedelta
from typing import TYPE_CHECKING

from toggl_python.schemas.time_entry import MeTimeEntryResponse

from tests.conftest import fake
from tests.factories.time_entry import (
    time_entry_extended_request_factory,
    time_entry_request_factory,
)

# Necessary to mark all tests in module as integration
from tests.integration import pytestmark  # noqa: F401 - imported but unused


try:
    import zoneinfo
except ImportError:
    from backports import zoneinfo


if TYPE_CHECKING:
    from toggl_python.entities.user import CurrentUser
    from toggl_python.entities.workspace import Workspace


def test_create_time_entry__only_necessary_fields(i_authed_workspace: Workspace) -> None:
    workspace_id = int(os.environ["WORKSPACE_ID"])
    request_body = time_entry_request_factory(workspace_id)
    expected_result = set(MeTimeEntryResponse.model_fields.keys())

    result = i_authed_workspace.create_time_entry(
        workspace_id,
        start_datetime=request_body["start"],
        created_with=request_body["created_with"],
    )

    assert result.model_fields_set == expected_result

    _ = i_authed_workspace.delete_time_entry(workspace_id=workspace_id, time_entry_id=result.id)


def test_create_time_entry__all_fields(i_authed_workspace: Workspace) -> None:
    """Create TimeEntry without fields `tag_ids` and `task_id`.

    `tag_ids` requires existing Tags and it is complicated to test
    and `task_id` is available on paid plan.
    """
    workspace_id = int(os.environ["WORKSPACE_ID"])
    request_body = time_entry_extended_request_factory(workspace_id)
    expected_result = set(MeTimeEntryResponse.model_fields.keys())

    result = i_authed_workspace.create_time_entry(
        workspace_id,
        start_datetime=request_body["start"],
        created_with=request_body["created_with"],
        billable=request_body["billable"],
        description=request_body["description"],
        duration=request_body["duration"],
        project_id=os.environ["PROJECT_ID"],
        stop=request_body["stop"],
        tags=request_body["tags"],
        user_id=os.environ["USER_ID"],
    )

    assert result.model_fields_set == expected_result

    _ = i_authed_workspace.delete_time_entry(workspace_id=workspace_id, time_entry_id=result.id)


def test_list_time_entries__with_start_and_end_date__datetime(
    i_authed_user: CurrentUser, i_authed_workspace: Workspace
) -> None:
    workspace_id = int(os.environ["WORKSPACE_ID"])
    timezone_name = fake.timezone()
    tz = zoneinfo.ZoneInfo(timezone_name)
    start_date = fake.date_time_this_month(tzinfo=tz, before_now=True)
    delta = fake.random_int(min=1, max=999999)
    end_date = start_date + timedelta(seconds=delta)
    time_entry = i_authed_workspace.create_time_entry(
        workspace_id,
        start_datetime=fake.date_time_between_dates(start_date, end_date, tzinfo=tz),
        created_with=fake.word(),
    )

    expected_result = set(MeTimeEntryResponse.model_fields.keys())

    result = i_authed_user.get_time_entries(start_date=start_date, end_date=end_date)

    assert result[0].model_fields_set == expected_result

    _ = i_authed_workspace.delete_time_entry(workspace_id, time_entry.id)


def test_list_time_entries__with_start_and_end_date__str(
    i_authed_user: CurrentUser, i_authed_workspace: Workspace
) -> None:
    workspace_id = int(os.environ["WORKSPACE_ID"])
    start_date = fake.date_this_month(before_today=True)
    delta = fake.random_int(min=1, max=999)
    end_date = start_date + timedelta(days=delta)
    timezone_name = fake.timezone()
    tz = zoneinfo.ZoneInfo(timezone_name)
    time_entry = i_authed_workspace.create_time_entry(
        workspace_id,
        start_datetime=fake.date_time_between_dates(start_date, end_date, tzinfo=tz),
        created_with=fake.word(),
    )

    expected_result = set(MeTimeEntryResponse.model_fields.keys())

    result = i_authed_user.get_time_entries(
        start_date=start_date.isoformat(), end_date=end_date.isoformat()
    )

    assert result[0].model_fields_set == expected_result

    _ = i_authed_workspace.delete_time_entry(workspace_id, time_entry.id)


def test_list_time_entries__no_results(i_authed_user: CurrentUser) -> None:
    start_date = fake.date_time_between(start_date="-6m", end_date="-3m")
    delta = fake.random_int(min=0, max=999)
    end_date = start_date + timedelta(days=delta)

    result = i_authed_user.get_time_entries(start_date=start_date, end_date=end_date)

    assert result == []
