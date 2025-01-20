from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING, Dict, Union
from unittest.mock import Mock, patch

import pytest
from httpx import Response as HttpxResponse
from pydantic import ValidationError
from toggl_python.schemas.workspace import WorkspaceResponse

from tests.conftest import fake
from tests.factories.workspace import workspace_request_factory, workspace_response_factory
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


@patch("toggl_python.schemas.base.datetime")
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


@patch("toggl_python.schemas.base.datetime")
def test_get_workspaces__too_old_since_value(
    mocked_datetime: Mock, authed_workspace: Workspace
) -> None:
    since = datetime(2024, 5, 20, tzinfo=timezone.utc)
    mocked_datetime.now.return_value = datetime(2024, 8, 21, tzinfo=timezone.utc)
    error_message = "Since cannot be older than 3 months"

    with pytest.raises(ValidationError, match=error_message):
        _ = authed_workspace.list(since=since)


@pytest.mark.parametrize(
    argnames="workspace_name, error_message",
    argvalues=(
        ("", "String should have at least 1 character"),
        (fake.pystr(min_chars=141, max_chars=200), "String should have at most 140 character"),
    ),
)
def test_update__invalid_workspace_name(
    workspace_name: str, error_message: str, authed_workspace: Workspace
) -> None:
    workspace_id = fake.random_int()

    with pytest.raises(ValidationError, match=error_message):
        _ = authed_workspace.update(workspace_id, name=workspace_name)


def test_update(response_mock: MockRouter, authed_workspace: Workspace) -> None:
    workspace_id = fake.random_int()
    full_request_body = workspace_request_factory()
    random_param = fake.random_element(full_request_body.keys())
    request_body = {random_param: full_request_body[random_param]}
    response = workspace_response_factory()
    mocked_route = response_mock.put(f"/workspaces/{workspace_id}", json=request_body).mock(
        return_value=HttpxResponse(status_code=200, json=response),
    )
    expected_result = WorkspaceResponse.model_validate(response)

    result = authed_workspace.update(workspace_id, **request_body)

    assert mocked_route.called is True
    assert result == expected_result


def test_update__all_params(
    response_mock: MockRouter, authed_workspace: Workspace
) -> None:
    workspace_id = fake.random_int()
    request_body = workspace_request_factory()
    response = workspace_response_factory(workspace_id)
    mocked_route = response_mock.put(f"/workspaces/{workspace_id}", json=request_body).mock(
        return_value=HttpxResponse(status_code=200, json=response),
    )
    expected_result = WorkspaceResponse.model_validate(response)

    result = authed_workspace.update(workspace_id, **request_body)

    assert mocked_route.called is True
    assert result == expected_result
