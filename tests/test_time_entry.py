from __future__ import annotations

from datetime import datetime, timezone
from random import randint
from typing import TYPE_CHECKING, Dict, List, Union
from unittest.mock import Mock, patch

import pytest
from httpx import Response
from pydantic import ValidationError
from toggl_python.exceptions import BadRequest
from toggl_python.schemas.time_entry import (
    BulkEditTimeEntriesFieldNames,
    BulkEditTimeEntriesOperation,
    BulkEditTimeEntriesOperations,
    BulkEditTimeEntriesResponse,
    MeTimeEntryResponse,
    MeTimeEntryWithMetaResponse,
    MeWebTimerResponse,
)

from tests.conftest import fake
from tests.factories.time_entry import time_entry_request_factory, time_entry_response_factory
from tests.responses.me_get import ME_WEB_TIMER_RESPONSE
from tests.responses.time_entry_get import ME_TIME_ENTRY_RESPONSE, ME_TIME_ENTRY_WITH_META_RESPONSE
from tests.responses.time_entry_put_and_patch import BULK_EDIT_TIME_ENTRIES_RESPONSE


if TYPE_CHECKING:
    from respx import MockRouter
    from toggl_python.entities.user import CurrentUser
    from toggl_python.entities.workspace import Workspace


def test_create_time_entry__only_required_fields(
    response_mock: MockRouter, authed_workspace: Workspace
) -> None:
    workspace_id = fake.random_int()
    request_body = time_entry_request_factory(workspace_id)
    fake_response = time_entry_response_factory(workspace_id, request_body["start"])
    mocked_route = response_mock.post(
        f"/workspaces/{workspace_id}/time_entries", json=request_body
    ).mock(
        return_value=Response(status_code=200, json=fake_response),
    )
    expected_result = MeTimeEntryResponse.model_validate(fake_response)

    result = authed_workspace.create_time_entry(
        workspace_id,
        start_datetime=request_body["start"],
        created_with=request_body["created_with"],
    )

    assert mocked_route.called is True
    assert result == expected_result


def test_create_time_entry__all_fields(
    response_mock: MockRouter, authed_current_user: CurrentUser
) -> None:
    pass


def test_create_time_entry__invalid_start_stop_and_duration(
    response_mock: MockRouter, authed_current_user: CurrentUser
) -> None:
    pass


# ? not sure if it is relevant
def test_create_time_entry__update_existing(
    response_mock: MockRouter, authed_current_user: CurrentUser
) -> None:
    pass


def test_get_time_entry__without_query_params(
    response_mock: MockRouter, authed_current_user: CurrentUser
) -> None:
    fake_time_entry_id = 123
    mocked_route = response_mock.get(f"/me/time_entries/{fake_time_entry_id}").mock(
        return_value=Response(status_code=200, json=ME_TIME_ENTRY_RESPONSE),
    )
    expected_result = MeTimeEntryResponse.model_validate(ME_TIME_ENTRY_RESPONSE)

    result = authed_current_user.get_time_entry(fake_time_entry_id)

    assert mocked_route.called is True
    assert result == expected_result


def test_get_time_entry__with_meta_query_param(
    response_mock: MockRouter, authed_current_user: CurrentUser
) -> None:
    fake_time_entry_id = 123
    mocked_route = response_mock.get(f"/me/time_entries/{fake_time_entry_id}?meta=true").mock(
        return_value=Response(status_code=200, json=ME_TIME_ENTRY_WITH_META_RESPONSE),
    )
    expected_result = MeTimeEntryWithMetaResponse.model_validate(ME_TIME_ENTRY_WITH_META_RESPONSE)

    result = authed_current_user.get_time_entry(fake_time_entry_id, meta=True)

    assert mocked_route.called is True
    assert result == expected_result


def test_get_current_time_entry__ok(
    response_mock: MockRouter, authed_current_user: CurrentUser
) -> None:
    mocked_route = response_mock.get("/me/time_entries/current").mock(
        return_value=Response(status_code=200, json=ME_TIME_ENTRY_RESPONSE),
    )
    expected_result = MeTimeEntryResponse.model_validate(ME_TIME_ENTRY_RESPONSE)

    result = authed_current_user.get_current_time_entry()

    assert mocked_route.called is True
    assert result == expected_result


def test_get_current_time_entry__no_current_entry(
    response_mock: MockRouter, authed_current_user: CurrentUser
) -> None:
    mocked_route = response_mock.get("/me/time_entries/current").mock(
        return_value=Response(status_code=200, json={}),
    )

    result = authed_current_user.get_current_time_entry()

    assert mocked_route.called is True
    assert result is None


def test_get_time_entries__without_query_params(
    response_mock: MockRouter, authed_current_user: CurrentUser
) -> None:
    fake_response = [ME_TIME_ENTRY_RESPONSE]
    mocked_route = response_mock.get("/me/time_entries").mock(
        return_value=Response(status_code=200, json=fake_response),
    )
    expected_result = [MeTimeEntryResponse.model_validate(ME_TIME_ENTRY_RESPONSE)]

    result = authed_current_user.get_time_entries()

    assert mocked_route.called is True
    assert result == expected_result


def test_get_time_entries__with_meta_query_param(
    response_mock: MockRouter, authed_current_user: CurrentUser
) -> None:
    mocked_route = response_mock.get("/me/time_entries", params={"meta": True}).mock(
        return_value=Response(status_code=200, json=[ME_TIME_ENTRY_WITH_META_RESPONSE]),
    )
    expected_result = [
        MeTimeEntryWithMetaResponse.model_validate(ME_TIME_ENTRY_WITH_META_RESPONSE)
    ]

    result = authed_current_user.get_time_entries(meta=True)

    assert mocked_route.called is True
    assert result == expected_result


@patch("toggl_python.schemas.base.datetime")
@pytest.mark.parametrize(
    argnames="query_params, method_kwargs",
    argvalues=(
        (
            {"since": 1715299200},
            {"since": int(datetime(2024, 5, 10, tzinfo=timezone.utc).timestamp())},
        ),
        ({"since": 1718755200}, {"since": 1718755200}),
        ({"before": "2024-07-28T12:30:43+00:00"}, {"before": "2024-07-28T12:30:43+00:00"}),
        (
            {"before": "2023-01-01T00:00:00+00:00"},
            {"before": datetime(2023, 1, 1, tzinfo=timezone.utc)},
        ),
        (
            {"start_date": "2023-09-12T00:00:00-03:00", "end_date": "2023-10-12T00:00:00-01:00"},
            {"start_date": "2023-09-12T00:00:00-03:00", "end_date": "2023-10-12T00:00:00-01:00"},
        ),
    ),
)
def test_get_time_entries__with_datetime_query_params(
    mocked_datetime: Mock,
    query_params: Dict[str, Union[int, str]],
    method_kwargs: Dict[str, Union[datetime, str]],
    response_mock: MockRouter,
    authed_current_user: CurrentUser,
) -> None:
    query_params["meta"] = False
    # Required to pass `since` query param validation
    mocked_datetime.now.return_value = datetime(2024, 6, 20, tzinfo=timezone.utc)
    mocked_route = response_mock.get("/me/time_entries", params=query_params).mock(
        return_value=Response(status_code=200, json=[ME_TIME_ENTRY_RESPONSE]),
    )
    expected_result = [MeTimeEntryResponse.model_validate(ME_TIME_ENTRY_RESPONSE)]

    result = authed_current_user.get_time_entries(**method_kwargs)

    assert mocked_route.called is True
    assert result == expected_result


@pytest.mark.parametrize(
    argnames="query_params",
    argvalues=(
        {"start_date": "2010-01-01T00:00:00+08:00"},
        {"end_date": "2010-02-01T00:00:00+03:00"},
        {"since": 17223107204, "before": "2024-07-28T00:00:00+10:00"},
        {
            "since": 17223107204,
            "start_date": "2020-11-11T09:30:00-04:00",
            "end_date": "2021-01-11T09:30:00-04:00",
        },
        {
            "before": "2020-12-15T09:30:00-04:00",
            "start_date": "2020-11-11T09:30:00-04:00",
            "end_date": "2021-01-11T09:30:00-04:00",
        },
        {
            "since": 17223107204,
            "before": "2020-12-15T09:30:00-04:00",
            "start_date": "2020-11-11T09:30:00-04:00",
            "end_date": "2021-01-11T09:30:00-04:00",
        },
    ),
)
def test_get_time_entries__invalid_query_params(
    query_params: Dict[str, Union[int, str]],
    response_mock: MockRouter,
    authed_current_user: CurrentUser,
) -> None:
    error_message = "can not be present simultaneously"
    _ = response_mock.get("/me/time_entries", params=query_params).mock(
        return_value=Response(status_code=400, json=error_message),
    )

    with pytest.raises(BadRequest, match=error_message):
        _ = authed_current_user.get_time_entries(**query_params)


@patch("toggl_python.schemas.base.datetime")
def test_get_time_entries__too_old_since_value(
    mocked_datetime: Mock, authed_current_user: CurrentUser
) -> None:
    error_message = "Since cannot be older than 3 months"
    since = datetime(2020, 1, 1, tzinfo=timezone.utc)
    mocked_datetime.now.return_value = datetime(2020, 4, 1, tzinfo=timezone.utc)

    with pytest.raises(ValidationError, match=error_message):
        _ = authed_current_user.get_time_entries(since=since)


def test_get_web_timer__ok(response_mock: MockRouter, authed_current_user: CurrentUser) -> None:
    mocked_route = response_mock.get("/me/web-timer").mock(
        return_value=Response(status_code=200, json=ME_WEB_TIMER_RESPONSE),
    )
    expected_result = MeWebTimerResponse.model_validate(ME_WEB_TIMER_RESPONSE)

    result = authed_current_user.get_web_timer()

    assert mocked_route.called is True
    assert result == expected_result


@pytest.mark.parametrize(
    argnames=("field_name", "field_value"),
    argvalues=[
        ("billable", True),
        ("description", "updated description"),
        ("duration", -1),
        ("project_id", 757542305),
        ("shared_with_user_ids", [1243543643, 676586868]),
        ("start", "2020-11-11T09:30:00-04:00"),
        ("stop", "2010-01-29T19:50:00+02:00"),
        ("tag_ids", [24032, 354742502]),
        ("tags", ["new tag"]),
        ("task_id", 1593268409),
        ("user_id", 573250897),
    ],
)
def test_workspace_update_time_entry__ok(
    field_name: str,
    field_value: Union[bool, str, int, List[int]],
    response_mock: MockRouter,
    authed_workspace: Workspace,
) -> None:
    workspace_id = 123
    time_entry_id = 98765
    payload = {field_name: field_value}
    fake_response = ME_TIME_ENTRY_RESPONSE.copy()
    fake_response.update(**payload)
    mocked_route = response_mock.put(
        f"/workspaces/{workspace_id}/time_entries/{time_entry_id}"
    ).mock(
        return_value=Response(status_code=200, json=fake_response),
    )
    expected_result = MeTimeEntryResponse.model_validate(fake_response)

    result = authed_workspace.update_time_entry(workspace_id, time_entry_id, **payload)

    assert mocked_route.called is True
    assert result == expected_result


def test_update_time_entry__user_cannot_access_project(
    response_mock: MockRouter, authed_workspace: Workspace
) -> None:
    workspace_id = 123
    time_entry_id = 98765
    error_message = "User cannot access the selected project"
    mocked_route = response_mock.put(
        f"/workspaces/{workspace_id}/time_entries/{time_entry_id}"
    ).mock(
        return_value=Response(status_code=400, text=error_message),
    )

    with pytest.raises(BadRequest, match=error_message):
        _ = authed_workspace.update_time_entry(workspace_id, time_entry_id, project_id=125872350)

    assert mocked_route.called is True


def test_delete_time_entry__ok(response_mock: MockRouter, authed_workspace: Workspace) -> None:
    workspace_id = 123
    time_entry_id = 98765
    mocked_route = response_mock.delete(
        f"/workspaces/{workspace_id}/time_entries/{time_entry_id}"
    ).mock(
        return_value=Response(status_code=200),
    )

    result = authed_workspace.delete_time_entry(workspace_id, time_entry_id)

    assert mocked_route.called is True
    assert result is True


def test_bulk_edit_time_entries__too_much_ids(authed_workspace: Workspace) -> None:
    workspace_id = 123
    time_entry_ids = [randint(100000, 999999) for _ in range(101)]  # noqa: S311
    error_message = "Limit to max TimeEntry IDs exceeded. "

    with pytest.raises(ValueError, match=error_message):
        _ = authed_workspace.bulk_edit_time_entries(workspace_id, time_entry_ids, operations=[])


def test_bulk_edit_time_entries__empty_time_entry_ids(authed_workspace: Workspace) -> None:
    workspace_id = 123
    error_message = "Specify at least one TimeEntry ID"

    with pytest.raises(ValueError, match=error_message):
        _ = authed_workspace.bulk_edit_time_entries(workspace_id, time_entry_ids=[], operations=[])


def test_bulk_edit_time_entries__empty_operations(authed_workspace: Workspace) -> None:
    workspace_id = 123
    time_entry_ids = [12345677]
    error_message = "Specify at least one edit operation"

    with pytest.raises(ValueError, match=error_message):
        _ = authed_workspace.bulk_edit_time_entries(workspace_id, time_entry_ids, operations=[])


@pytest.mark.parametrize(
    argnames=("operation"), argvalues=[item.value for item in BulkEditTimeEntriesOperations]
)
@pytest.mark.parametrize(
    argnames=("field_name", "field_value"),
    argvalues=[
        (BulkEditTimeEntriesFieldNames.billable.value, True),
        (BulkEditTimeEntriesFieldNames.description.value, "updated description"),
        (BulkEditTimeEntriesFieldNames.duration.value, -1),
        (BulkEditTimeEntriesFieldNames.project_id.value, 757542305),
        (BulkEditTimeEntriesFieldNames.shared_with_user_ids.value, [1243543643, 676586868]),
        (BulkEditTimeEntriesFieldNames.start.value, datetime(2024, 5, 10, tzinfo=timezone.utc)),
        (BulkEditTimeEntriesFieldNames.stop.value, datetime(2022, 4, 15, tzinfo=timezone.utc)),
        (BulkEditTimeEntriesFieldNames.tag_ids.value, [24032, 354742502]),
        (BulkEditTimeEntriesFieldNames.tags.value, ["new tag"]),
        (BulkEditTimeEntriesFieldNames.task_id.value, 1593268409),
        (BulkEditTimeEntriesFieldNames.user_id.value, 573250897),
    ],
)
def test_bulk_edit_time_entries__ok(
    field_name: BulkEditTimeEntriesFieldNames,
    field_value: Union[str, int],
    operation: BulkEditTimeEntriesOperations,
    response_mock: MockRouter,
    authed_workspace: Workspace,
) -> None:
    workspace_id = 123
    time_entry_ids = [98765, 43210]
    edit_operation = BulkEditTimeEntriesOperation(
        operation=operation, field_name=field_name, field_value=field_value
    )
    mocked_route = response_mock.patch(
        f"/workspaces/{workspace_id}/time_entries/{time_entry_ids}"
    ).mock(
        return_value=Response(status_code=200, json=BULK_EDIT_TIME_ENTRIES_RESPONSE),
    )
    expected_result = BulkEditTimeEntriesResponse.model_validate(BULK_EDIT_TIME_ENTRIES_RESPONSE)

    result = authed_workspace.bulk_edit_time_entries(
        workspace_id, time_entry_ids, operations=[edit_operation]
    )

    assert mocked_route.called is True
    assert result == expected_result


def test_stop_time_entry__ok(response_mock: MockRouter, authed_workspace: Workspace) -> None:
    workspace_id = 123
    time_entry_id = 98765
    mocked_route = response_mock.patch(
        f"/workspaces/{workspace_id}/time_entries/{time_entry_id}/stop"
    ).mock(
        return_value=Response(status_code=200, json=ME_TIME_ENTRY_RESPONSE),
    )
    expected_result = MeTimeEntryResponse.model_validate(ME_TIME_ENTRY_RESPONSE)

    result = authed_workspace.stop_time_entry(workspace_id, time_entry_id)

    assert mocked_route.called is True
    assert result == expected_result


def test_stop_time_entry__already_stopped(
    response_mock: MockRouter, authed_workspace: Workspace
) -> None:
    workspace_id = 123
    time_entry_id = 98765
    error_message = "Time entry already stopped"
    mocked_route = response_mock.patch(
        f"/workspaces/{workspace_id}/time_entries/{time_entry_id}/stop"
    ).mock(
        return_value=Response(status_code=409, text=error_message),
    )

    with pytest.raises(BadRequest, match=error_message):
        _ = authed_workspace.stop_time_entry(workspace_id, time_entry_id)

    assert mocked_route.called is True
