from __future__ import annotations

import os
from typing import TYPE_CHECKING

from toggl_python.schemas.project import ProjectResponse

# Necessary to mark all tests in module as integration
from tests.integration import pytestmark  # noqa: F401 - imported but unused


if TYPE_CHECKING:
    from toggl_python.entities.user import CurrentUser
    from toggl_python.entities.workspace import Workspace


def test_create_project__without_query_params(i_authed_workspace: Workspace) -> None:
    # delete it at the end
    # Now this actions are not implemented
    workspace_id = int(os.environ["WORKSPACE_ID"])
    expected_result = set(ProjectResponse.model_fields.keys())

    result = i_authed_workspace.create_project(workspace_id)

    assert result.model_fields_set == expected_result


def test_get_projects__without_query_params(i_authed_workspace: Workspace) -> None:
    # Later Create project and init and delete it at the end
    # Now this actions are not implemented
    workspace_id = int(os.environ["WORKSPACE_ID"])
    expected_result = set(ProjectResponse.model_fields.keys())

    result = i_authed_workspace.get_projects(workspace_id)

    assert result[0].model_fields_set == expected_result


def test_get_project_by_id(i_authed_workspace: Workspace) -> None:
    # Later Create project and init and delete it at the end
    # Now this actions are not implemented
    workspace_id = int(os.environ["WORKSPACE_ID"])
    project_id = int(os.environ["PROJECT_ID"])
    expected_result = set(ProjectResponse.model_fields.keys())

    result = i_authed_workspace.get_project(workspace_id, project_id)

    assert result.model_fields_set == expected_result


def test_me_get_projects__without_query_params(i_authed_user: CurrentUser) -> None:
    # Later Create project and init and delete it at the end
    # Now this actions are not implemented
    expected_result = set(ProjectResponse.model_fields.keys())

    result = i_authed_user.get_projects()

    assert result[0].model_fields_set == expected_result




def test_me_get_paginated_projects__without_query_params(i_authed_user: CurrentUser) -> None:
    # Later Create project and init and delete it at the end
    # Now this actions are not implemented
    expected_result = set(ProjectResponse.model_fields.keys())

    result = i_authed_user.get_paginated_projects()

    assert result[0].model_fields_set == expected_result
