from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING, Dict, Union
from unittest.mock import Mock, patch

import pytest
from httpx import Response as HttpxResponse
from pydantic import ValidationError
from toggl_python.schemas.workspace import WorkspaceResponse

from tests.responses.workspace_get import WORKSPACE_RESPONSE


if TYPE_CHECKING:
    from respx import MockRouter
    from toggl_python.entities.workspace import Workspace


def test_get_workspace_by_id(response_mock: MockRouter, authed_workspace: Workspace) -> None:
    workspace_id = 123
    mocked_route = response_mock.get(f"/workspaces/{workspace_id}").mock(
        return_value=HttpxResponse(status_code=200, json=WORKSPACE_RESPONSE),
    )
    expected_result = WorkspaceResponse.model_validate(WORKSPACE_RESPONSE)

    result = authed_workspace.get(workspace_id=workspace_id)

    assert mocked_route.called is True
    assert result == expected_result


def test_get_workspaces__without_query_params(
    response_mock: MockRouter, authed_workspace: Workspace
) -> None:
    mocked_route = response_mock.get("/workspaces").mock(
        return_value=HttpxResponse(status_code=200, json=[WORKSPACE_RESPONSE]),
    )
    expected_result = [WorkspaceResponse.model_validate(WORKSPACE_RESPONSE)]

    result = authed_workspace.list()

    assert mocked_route.called is True
    assert result == expected_result


@patch("toggl_python.schemas.workspace.datetime")
@pytest.mark.parametrize(
    argnames="query_params, method_kwargs",
    argvalues=(
        (
            {"since": 1721433600},
            {"since": datetime(2024, 7, 20, tzinfo=timezone.utc)},
        ),
        ({"since": 1718755200}, {"since": 1718755200}),
    ),
)
def test_get_workspaces__with_query_param_since(
    mocked_datetime: Mock,
    query_params: Dict[str, int],
    method_kwargs: Dict[str, Union[datetime, int]],
    response_mock: MockRouter,
    authed_workspace: Workspace,
) -> None:
    mocked_datetime.now.return_value = datetime(2024, 8, 20, tzinfo=timezone.utc)
    mocked_route = response_mock.get("/workspaces", params=query_params).mock(
        return_value=HttpxResponse(status_code=200, json=[WORKSPACE_RESPONSE]),
    )
    expected_result = [WorkspaceResponse.model_validate(WORKSPACE_RESPONSE)]

    result = authed_workspace.list(**method_kwargs)

    assert mocked_route.called is True
    assert result == expected_result


@patch("toggl_python.schemas.workspace.datetime")
def test_get_workspaces__too_old_since_value(
    mocked_datetime: Mock, authed_workspace: Workspace
) -> None:
    since = datetime(2024, 5, 20, tzinfo=timezone.utc)
    mocked_datetime.now.return_value = datetime(2024, 8, 21, tzinfo=timezone.utc)
    error_message = "Since cannot be older than 3 months"

    with pytest.raises(ValidationError, match=error_message):
        _ = authed_workspace.list(since=since)
