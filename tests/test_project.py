from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING, Dict, Union
from unittest.mock import Mock, patch

import pytest
from httpx import Response as HttpxResponse
from pydantic import ValidationError
from toggl_python.schemas.base import BulkEditOperation, BulkEditOperations, BulkEditResponse
from toggl_python.schemas.project import BulkEditProjectsFieldNames, ProjectResponse

from tests.conftest import fake
from tests.factories.base import bulk_edit_response_factory, datetime_repr_factory
from tests.factories.project import project_request_factory, project_response_factory
from tests.responses.project_get import PROJECT_RESPONSE


if TYPE_CHECKING:
    from respx import MockRouter
    from toggl_python.entities.user import CurrentUser
    from toggl_python.entities.workspace import Workspace


def test_create_project(response_mock: MockRouter, authed_workspace: Workspace) -> None:
    workspace_id = fake.random_int()
    full_request_body = project_request_factory()
    random_param = fake.random_element(full_request_body.keys())
    request_body = {random_param: full_request_body[random_param]}
    response = project_response_factory()
    mocked_route = response_mock.post(
        f"/workspaces/{workspace_id}/projects", json=request_body
    ).mock(
        return_value=HttpxResponse(status_code=200, json=response),
    )
    expected_result = ProjectResponse.model_validate(response)

    result = authed_workspace.create_project(workspace_id, **request_body)

    assert mocked_route.called is True
    assert result == expected_result


def test_create_project_all_params(response_mock: MockRouter, authed_workspace: Workspace) -> None:
    workspace_id = fake.random_int()
    request_body = project_request_factory()
    response = project_response_factory(workspace_id, end_date=request_body["end_date"])
    mocked_route = response_mock.post(
        f"/workspaces/{workspace_id}/projects", json=request_body
    ).mock(
        return_value=HttpxResponse(status_code=200, json=response),
    )

    expected_result = ProjectResponse.model_validate(response)

    result = authed_workspace.create_project(workspace_id, **request_body)

    assert mocked_route.called is True
    assert result == expected_result


def test_create_project_empty_request_body(
    response_mock: MockRouter, authed_workspace: Workspace
) -> None:
    workspace_id = fake.random_int()
    response = project_response_factory(workspace_id)
    mocked_route = response_mock.post(f"/workspaces/{workspace_id}/projects").mock(
        return_value=HttpxResponse(status_code=200, json=response),
    )
    expected_result = ProjectResponse.model_validate(response)

    result = authed_workspace.create_project(workspace_id)

    assert mocked_route.called is True
    assert result == expected_result


def test_get_project_by_id(response_mock: MockRouter, authed_workspace: Workspace) -> None:
    workspace_id = 123
    project_id = 123
    mocked_route = response_mock.get(f"/workspaces/{workspace_id}/projects/{project_id}").mock(
        return_value=HttpxResponse(status_code=200, json=PROJECT_RESPONSE),
    )
    expected_result = ProjectResponse.model_validate(PROJECT_RESPONSE)

    result = authed_workspace.get_project(workspace_id=workspace_id, project_id=project_id)

    assert mocked_route.called is True
    assert result == expected_result


def test_get_projects__without_query_params(
    response_mock: MockRouter, authed_workspace: Workspace
) -> None:
    workspace_id = 123
    mocked_route = response_mock.get(f"/workspaces/{workspace_id}/projects").mock(
        return_value=HttpxResponse(status_code=200, json=[PROJECT_RESPONSE]),
    )
    expected_result = [ProjectResponse.model_validate(PROJECT_RESPONSE)]

    result = authed_workspace.get_projects(workspace_id=workspace_id)

    assert mocked_route.called is True
    assert result == expected_result


@patch("toggl_python.schemas.base.datetime")
def test_get_projects__too_old_since_value(
    mocked_datetime: Mock, authed_workspace: Workspace
) -> None:
    error_message = "Since cannot be older than 3 months"
    since = datetime(2020, 1, 1, tzinfo=timezone.utc)
    mocked_datetime.now.return_value = datetime(2020, 4, 1, tzinfo=timezone.utc)

    with pytest.raises(ValidationError, match=error_message):
        _ = authed_workspace.get_projects(workspace_id=123, since=since)


@patch("toggl_python.schemas.base.datetime")
@pytest.mark.parametrize(
    argnames="query_params",
    argvalues=(
        {"active": False},
        {"since": int(datetime(2024, 5, 10, tzinfo=timezone.utc).timestamp())},
        {"billable": True},
        {"user_ids": [1234567]},
        {"client_ids": [209327532]},
        {"group_ids": [214327]},
        {"statuses": "active"},
        {"name": "random project name"},
        {"page": 1},
        {"per_page": 10},
        {"sort_field": "billable"},
        {"sort_order": "DESC"},
        {"only_templates": True},
        {"only_me": True},
    ),
)
def test_get_projects__with_query_params(
    mocked_datetime: Mock,
    query_params: Dict[str, Union[str, int]],
    response_mock: MockRouter,
    authed_workspace: Workspace,
) -> None:
    mocked_datetime.now.return_value = datetime(2024, 7, 20, tzinfo=timezone.utc)
    workspace_id = 123
    mocked_route = response_mock.get(
        f"/workspaces/{workspace_id}/projects", params=query_params
    ).mock(
        return_value=HttpxResponse(status_code=200, json=[PROJECT_RESPONSE]),
    )
    expected_result = [ProjectResponse.model_validate(PROJECT_RESPONSE)]

    result = authed_workspace.get_projects(workspace_id=workspace_id, **query_params)

    assert mocked_route.called is True
    assert result == expected_result


def test_me_get_projects__without_query_params(
    response_mock: MockRouter, authed_current_user: CurrentUser
) -> None:
    response = project_response_factory()
    mocked_route = response_mock.get("me/projects").mock(
        return_value=HttpxResponse(status_code=200, json=[response]),
    )
    expected_result = [ProjectResponse.model_validate(response)]

    result = authed_current_user.get_projects()

    assert mocked_route.called is True
    assert result == expected_result


def test_me_get_projects__include_archived(
    response_mock: MockRouter, authed_current_user: CurrentUser
) -> None:
    response = project_response_factory()
    include_archived = fake.boolean()
    mocked_route = response_mock.get(
        "me/projects", params={"include_archived": include_archived}
    ).mock(
        return_value=HttpxResponse(status_code=200, json=[response]),
    )
    expected_result = [ProjectResponse.model_validate(response)]

    result = authed_current_user.get_projects(include_archived=include_archived)

    assert mocked_route.called is True
    assert result == expected_result


def test_me_get_projects__since(
    response_mock: MockRouter, authed_current_user: CurrentUser
) -> None:
    response = project_response_factory()
    since = int(fake.past_datetime(start_date="-3m").timestamp())
    mocked_route = response_mock.get("me/projects", params={"since": since}).mock(
        return_value=HttpxResponse(status_code=200, json=[response]),
    )
    expected_result = [ProjectResponse.model_validate(response)]

    result = authed_current_user.get_projects(since=since)

    assert mocked_route.called is True
    assert result == expected_result


def test_me_get_projects__too_old_since_value(authed_current_user: CurrentUser) -> None:
    error_message = "Since cannot be older than 3 months"
    since = int(fake.date_time_between(end_date="-3m4d").timestamp())

    with pytest.raises(ValidationError, match=error_message):
        _ = authed_current_user.get_projects(since=since)


def test_me_get_paginated_projects__without_query_params(
    response_mock: MockRouter, authed_current_user: CurrentUser
) -> None:
    response = project_response_factory()
    mocked_route = response_mock.get("me/projects/paginated").mock(
        return_value=HttpxResponse(status_code=200, json=[response]),
    )
    expected_result = [ProjectResponse.model_validate(response)]

    result = authed_current_user.get_paginated_projects()

    assert mocked_route.called is True
    assert result == expected_result


def test_me_get_paginated_projects__since_query_param(
    response_mock: MockRouter, authed_current_user: CurrentUser
) -> None:
    response = project_response_factory()
    since = int(fake.past_datetime(start_date="-3m").timestamp())
    mocked_route = response_mock.get("me/projects/paginated", params={"since": since}).mock(
        return_value=HttpxResponse(status_code=200, json=[response]),
    )
    expected_result = [ProjectResponse.model_validate(response)]

    result = authed_current_user.get_paginated_projects(since=since)

    assert mocked_route.called is True
    assert result == expected_result


def test_me_get_paginated_projects__too_old_since_value(authed_current_user: CurrentUser) -> None:
    error_message = "Since cannot be older than 3 months"
    since = int(fake.date_time_between(end_date="-3m4d").timestamp())

    with pytest.raises(ValidationError, match=error_message):
        _ = authed_current_user.get_paginated_projects(since=since)


def test_me_get_paginated_projects__with_query_params(
    response_mock: MockRouter, authed_current_user: CurrentUser
) -> None:
    response = project_response_factory()
    query_params = {
        "start_project_id": fake.random_int(),
        "per_page": fake.random_int(min=50, max=200),
    }
    mocked_route = response_mock.get("me/projects/paginated", params=query_params).mock(
        return_value=HttpxResponse(status_code=200, json=[response]),
    )
    expected_result = [ProjectResponse.model_validate(response)]

    result = authed_current_user.get_paginated_projects(**query_params)

    assert mocked_route.called is True
    assert result == expected_result


def test_update_project(response_mock: MockRouter, authed_workspace: Workspace) -> None:
    workspace_id = fake.random_int()
    project_id = fake.random_int()
    full_request_body = project_request_factory()
    random_param = fake.random_element(full_request_body.keys())
    request_body = {random_param: full_request_body[random_param]}
    response = project_response_factory()
    mocked_route = response_mock.put(
        f"/workspaces/{workspace_id}/projects/{project_id}", json=request_body
    ).mock(
        return_value=HttpxResponse(status_code=200, json=response),
    )
    expected_result = ProjectResponse.model_validate(response)

    result = authed_workspace.update_project(workspace_id, project_id, **request_body)

    assert mocked_route.called is True
    assert result == expected_result


def test_update_project_all_params(response_mock: MockRouter, authed_workspace: Workspace) -> None:
    workspace_id = fake.random_int()
    project_id = fake.random_int()
    request_body = project_request_factory()
    response = project_response_factory(workspace_id, end_date=request_body["end_date"])
    mocked_route = response_mock.put(
        f"/workspaces/{workspace_id}/projects/{project_id}", json=request_body
    ).mock(
        return_value=HttpxResponse(status_code=200, json=response),
    )
    expected_result = ProjectResponse.model_validate(response)

    result = authed_workspace.update_project(workspace_id, project_id, **request_body)

    assert mocked_route.called is True
    assert result == expected_result


def test_update_project__both_client_id_and_client_name(authed_workspace: Workspace) -> None:
    workspace_id = fake.random_int()
    project_id = fake.random_int()
    error_message = "Both client_id and client_name provided"

    with pytest.raises(ValidationError, match=error_message):
        _ = authed_workspace.update_project(
            workspace_id, project_id, client_id=fake.random_int(), client_name=fake.name()
        )


def test_update_project__invalid_timeframe(authed_workspace: Workspace) -> None:
    workspace_id = fake.random_int()
    project_id = fake.random_int()
    start_date = fake.past_date()
    end_date = fake.date_between(end_date=start_date).isoformat()
    error_message = "Project timeframe is not valid"

    with pytest.raises(ValidationError, match=error_message):
        _ = authed_workspace.update_project(
            workspace_id,
            project_id,
            start_date=start_date.isoformat(),
            end_date=end_date,
        )


def test_bulk_edit_projects__too_much_ids(authed_workspace: Workspace) -> None:
    workspace_id = fake.random_int()
    project_ids = [fake.random_int() for _ in range(101)]
    error_message = "List should have at most 100 items after validation"

    with pytest.raises(ValueError, match=error_message):
        _ = authed_workspace.bulk_edit_projects(workspace_id, project_ids, operations=[])


def test_bulk_edit_projects__empty_projects_ids(authed_workspace: Workspace) -> None:
    workspace_id = fake.random_int()
    error_message = "List should have at least 1 item after validation"

    with pytest.raises(ValueError, match=error_message):
        _ = authed_workspace.bulk_edit_projects(workspace_id, project_ids=[], operations=[])


def test_bulk_edit_projects__empty_operations(authed_workspace: Workspace) -> None:
    workspace_id = fake.random_int()
    project_ids = [fake.random_int()]
    error_message = "List should have at least 1 item after validation"

    with pytest.raises(ValueError, match=error_message):
        _ = authed_workspace.bulk_edit_projects(workspace_id, project_ids, operations=[])


@pytest.mark.parametrize(
    argnames=("operation"), argvalues=[item.value for item in BulkEditOperations]
)
@pytest.mark.parametrize(
    argnames=("field_name", "field_value"),
    argvalues=[
        (BulkEditProjectsFieldNames.auto_estimates.value, fake.boolean()),
        (BulkEditProjectsFieldNames.end_date.value, datetime_repr_factory()),
        (BulkEditProjectsFieldNames.estimated_hours.value, fake.random_int()),
        (BulkEditProjectsFieldNames.is_private.value, fake.boolean()),
        (BulkEditProjectsFieldNames.project_name.value, fake.uuid4()),
        (BulkEditProjectsFieldNames.start_date.value, fake.date()),
    ],
)
def test_bulk_edit_time_entries__ok(
    field_name: BulkEditProjectsFieldNames,
    field_value: Union[str, int],
    operation: BulkEditOperations,
    response_mock: MockRouter,
    authed_workspace: Workspace,
) -> None:
    workspace_id = fake.random_int()
    project_ids = [fake.random_int(), fake.random_int()]
    project_ids_repr = ",".join(str(item) for item in project_ids)
    edit_operation = BulkEditOperation(
        operation=operation, field_name=field_name, field_value=field_value
    )
    response = bulk_edit_response_factory()
    mocked_route = response_mock.patch(
        f"/workspaces/{workspace_id}/projects/{project_ids_repr}"
    ).mock(
        return_value=HttpxResponse(status_code=200, json=response),
    )
    expected_result = BulkEditResponse.model_validate(response)

    result = authed_workspace.bulk_edit_projects(
        workspace_id, project_ids, operations=[edit_operation]
    )

    assert mocked_route.called is True
    assert result == expected_result


def test_delete_project(response_mock: MockRouter, authed_workspace: Workspace) -> None:
    workspace_id = fake.random_int()
    project_id = fake.random_int()
    mocked_route = response_mock.delete(f"/workspaces/{workspace_id}/projects/{project_id}").mock(
        return_value=HttpxResponse(status_code=200),
    )

    result = authed_workspace.delete_project(workspace_id, project_id)

    assert mocked_route.called is True
    assert result is True
