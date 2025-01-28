from __future__ import annotations

import os
from typing import TYPE_CHECKING

from toggl_python.schemas.workspace import WorkspaceResponse

from tests.conftest import fake
from tests.factories.workspace import workspace_request_factory

# Necessary to mark all tests in module as integration
from tests.integration import pytestmark  # noqa: F401 - imported but unused


if TYPE_CHECKING:
    from toggl_python.entities.workspace import Workspace


def test_get_workspace_by_id(i_authed_workspace: Workspace) -> None:
    workspace_id = int(os.environ["WORKSPACE_ID"])
    expected_result = set(WorkspaceResponse.model_fields.keys())

    result = i_authed_workspace.get(workspace_id)

    assert result.model_fields_set == expected_result


def test_get_workspaces__without_query_params(i_authed_workspace: Workspace) -> None:
    expected_result = set(WorkspaceResponse.model_fields.keys())

    result = i_authed_workspace.list()

    assert result[0].model_fields_set == expected_result


def test_update(i_authed_workspace: Workspace) -> None:
    workspace_id = int(os.environ["WORKSPACE_ID"])
    excluded_fields = {
        "admins",
        "only_admins_may_create_tags",
        "reports_collapse",
        "only_admins_see_team_dashboard",
    }
    full_request_body = workspace_request_factory(exclude=excluded_fields)
    random_param = fake.random_element(full_request_body.keys())
    request_body = {random_param: full_request_body[random_param]}
    workspace = i_authed_workspace.get(workspace_id)
    old_param_value = getattr(workspace, random_param)
    expected_result = set(WorkspaceResponse.model_fields.keys())

    result = i_authed_workspace.update(workspace_id, **request_body)

    assert result.model_fields_set == expected_result
    assert getattr(result, random_param) != old_param_value

    request_body[random_param] = old_param_value
    _ = i_authed_workspace.update(workspace_id, **request_body)


def test_update__all_params(i_authed_workspace: Workspace) -> None:
    workspace_id = int(os.environ["WORKSPACE_ID"])
    # Workspace response model does not return `admins`
    # `only_admins_may_create_tags` is available only for premium plan (but available in curl)
    excluded_fields = {"admins", "only_admins_may_create_tags"}
    request_body = workspace_request_factory(exclude=excluded_fields)
    workspace = i_authed_workspace.get(workspace_id)
    existing_model_fields = set(request_body.keys()) - excluded_fields
    old_params = {
        param_name: getattr(workspace, param_name) for param_name in existing_model_fields
    }
    expected_result = set(WorkspaceResponse.model_fields.keys())

    result = i_authed_workspace.update(workspace_id, **request_body)

    assert result.model_fields_set == expected_result

    _ = i_authed_workspace.update(workspace_id, **old_params)
