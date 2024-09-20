from __future__ import annotations

import os
from typing import TYPE_CHECKING

from tests.factories.project import project_request_factory
from toggl_python.schemas.project import ProjectResponse

# Necessary to mark all tests in module as integration
from tests.integration import pytestmark  # noqa: F401 - imported but unused
from tests.conftest import fake


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


def test_update_project(i_authed_workspace: Workspace) -> None:
    # delete it at the end
    # Now this actions are not implemented
    workspace_id = int(os.environ["WORKSPACE_ID"])
    project = i_authed_workspace.create_project(workspace_id)
    expected_result = set(ProjectResponse.model_fields.keys())
    full_request_body = project_request_factory()
    random_param = fake.random_element(full_request_body.keys())
    request_body = {random_param: full_request_body[random_param]}

    result = i_authed_workspace.update_project(workspace_id, project.id, **request_body)

    assert result.model_fields_set == expected_result

    # _ = i_authed_workspace.delete_project(workspace_id, project.id)


def test_update_project__all_params(i_authed_workspace: Workspace) -> None:
    # delete it at the end
    # Now this actions are not implemented
    workspace_id = int(os.environ["WORKSPACE_ID"])
    project = i_authed_workspace.create_project(workspace_id)
    expected_result = set(ProjectResponse.model_fields.keys())
    request_body = project_request_factory()

    result = i_authed_workspace.update_project(workspace_id, project.id, **request_body)

    assert result.model_fields_set == expected_result

    # _ = i_authed_workspace.delete_project(workspace_id, project.id)
