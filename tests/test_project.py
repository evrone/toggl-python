from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING, Dict, Union
from unittest.mock import Mock, patch

import pytest
from httpx import Response as HttpxResponse
from pydantic import ValidationError
from toggl_python.schemas.project import ProjectResponse

from tests.responses.project_get import PROJECT_RESPONSE


if TYPE_CHECKING:
    from respx import MockRouter
    from toggl_python.entities.workspace import Workspace


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
