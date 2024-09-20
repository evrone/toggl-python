from __future__ import annotations

import os
from datetime import datetime
from typing import TYPE_CHECKING

import pytest
from toggl_python.exceptions import BadRequest
from toggl_python.schemas.project import ProjectResponse

from tests.conftest import fake
from tests.factories.project import project_request_factory

# Necessary to mark all tests in module as integration
from tests.integration import pytestmark  # noqa: F401 - imported but unused


if TYPE_CHECKING:
    from toggl_python.entities.user import CurrentUser
    from toggl_python.entities.workspace import Workspace


def test_create_project__without_query_params(i_authed_workspace: Workspace) -> None:
    workspace_id = int(os.environ["WORKSPACE_ID"])
    expected_result = set(ProjectResponse.model_fields.keys())

    result = i_authed_workspace.create_project(workspace_id)

    assert result.model_fields_set == expected_result

    _ = i_authed_workspace.delete_project(workspace_id, result.id)


def test_get_projects__without_query_params(i_authed_workspace: Workspace) -> None:
    workspace_id = int(os.environ["WORKSPACE_ID"])
    project = i_authed_workspace.create_project(workspace_id)
    expected_result = set(ProjectResponse.model_fields.keys())

    result = i_authed_workspace.get_projects(workspace_id)

    assert result[0].model_fields_set == expected_result

    _ = i_authed_workspace.delete_project(workspace_id, project.id)


def test_get_project_by_id(i_authed_workspace: Workspace) -> None:
    workspace_id = int(os.environ["WORKSPACE_ID"])
    project = i_authed_workspace.create_project(workspace_id)
    expected_result = set(ProjectResponse.model_fields.keys())

    result = i_authed_workspace.get_project(workspace_id, project.id)

    assert result.model_fields_set == expected_result

    _ = i_authed_workspace.delete_project(workspace_id, project.id)


def test_me_get_projects__without_query_params(
    i_authed_user: CurrentUser, i_authed_workspace: Workspace
) -> None:
    workspace_id = int(os.environ["WORKSPACE_ID"])
    project = i_authed_workspace.create_project(workspace_id)
    another_project = i_authed_workspace.create_project(workspace_id)
    expected_result = set(ProjectResponse.model_fields.keys())

    result = i_authed_user.get_projects()

    assert result[0].model_fields_set == expected_result
    assert len(result) == 2

    _ = i_authed_workspace.delete_project(workspace_id, project.id)
    _ = i_authed_workspace.delete_project(workspace_id, another_project.id)


def test_me_get_projects__include_archived_query_param(
    i_authed_user: CurrentUser, i_authed_workspace: Workspace
) -> None:
    workspace_id = int(os.environ["WORKSPACE_ID"])
    project = i_authed_workspace.create_project(workspace_id, active=True)
    archived_project = i_authed_workspace.create_project(workspace_id, active=False)
    expected_result = set(ProjectResponse.model_fields.keys())

    result = i_authed_user.get_projects(include_archived=True)

    assert result[0].model_fields_set == expected_result
    assert len(result) == 1
    assert result[0].id == archived_project.id
    assert result[0].active == archived_project.active

    _ = i_authed_workspace.delete_project(workspace_id, project.id)
    _ = i_authed_workspace.delete_project(workspace_id, archived_project.id)


def test_me_get_projects__since_query_param(
    i_authed_user: CurrentUser, i_authed_workspace: Workspace
) -> None:
    workspace_id = int(os.environ["WORKSPACE_ID"])
    since = int(fake.date_time_between(start_date="-3m").timestamp())
    start_date = datetime.fromtimestamp(since)
    project = i_authed_workspace.create_project(workspace_id, start_date=start_date)
    earlier_start_date = fake.date_time_between(start_date=start_date)
    earlier_project = i_authed_workspace.create_project(
        workspace_id, start_date=earlier_start_date
    )
    expected_result = set(ProjectResponse.model_fields.keys())

    result = i_authed_user.get_projects(since=since)

    assert result[0].model_fields_set == expected_result
    assert len(result) == 1
    assert result[0].id == project.id

    _ = i_authed_workspace.delete_project(workspace_id, project.id)
    _ = i_authed_workspace.delete_project(workspace_id, earlier_project.id)


def test_me_get_paginated_projects__without_query_params(
    i_authed_user: CurrentUser, i_authed_workspace: Workspace
) -> None:
    workspace_id = int(os.environ["WORKSPACE_ID"])
    project = i_authed_workspace.create_project(workspace_id)
    expected_result = set(ProjectResponse.model_fields.keys())

    result = i_authed_user.get_paginated_projects()

    assert result[0].model_fields_set == expected_result
    assert len(result) == 1

    _ = i_authed_workspace.delete_project(workspace_id, project.id)


def test_me_get_paginated_projects__since_query_param(
    i_authed_user: CurrentUser, i_authed_workspace: Workspace
) -> None:
    workspace_id = int(os.environ["WORKSPACE_ID"])
    since = int(fake.date_time_between(start_date="-3m").timestamp())
    start_date = datetime.fromtimestamp(since)
    project = i_authed_workspace.create_project(workspace_id, start_date=start_date)
    earlier_start_date = fake.date_time_between(start_date=start_date)
    earlier_project = i_authed_workspace.create_project(
        workspace_id, start_date=earlier_start_date
    )
    expected_result = set(ProjectResponse.model_fields.keys())

    result = i_authed_user.get_paginated_projects(since=since)

    assert result[0].model_fields_set == expected_result
    assert len(result) == 1
    assert result[0].id == project.id

    _ = i_authed_workspace.delete_project(workspace_id, project.id)
    _ = i_authed_workspace.delete_project(workspace_id, earlier_project.id)


def test_me_get_paginated_projects__start_project_id_param(
    i_authed_user: CurrentUser, i_authed_workspace: Workspace
) -> None:
    workspace_id = int(os.environ["WORKSPACE_ID"])
    project = i_authed_workspace.create_project(workspace_id)
    another_project = i_authed_workspace.create_project(workspace_id)
    expected_result = set(ProjectResponse.model_fields.keys())

    result = i_authed_user.get_paginated_projects(start_project_id=another_project.id)

    assert result[0].model_fields_set == expected_result
    assert len(result) == 1
    assert result[0].id == another_project.id

    _ = i_authed_workspace.delete_project(workspace_id, project.id)
    _ = i_authed_workspace.delete_project(workspace_id, another_project.id)


def test_me_get_paginated_projects__per_page(
    i_authed_user: CurrentUser, i_authed_workspace: Workspace
) -> None:
    workspace_id = int(os.environ["WORKSPACE_ID"])
    project = i_authed_workspace.create_project(workspace_id)
    another_project = i_authed_workspace.create_project(workspace_id)
    expected_result = set(ProjectResponse.model_fields.keys())

    result = i_authed_user.get_paginated_projects(per_page=1)

    assert result[0].model_fields_set == expected_result
    assert len(result) == 1
    assert result[0].id == another_project.id

    _ = i_authed_workspace.delete_project(workspace_id, project.id)
    _ = i_authed_workspace.delete_project(workspace_id, another_project.id)


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

    _ = i_authed_workspace.delete_project(workspace_id, project.id)


def test_update_project__all_params(i_authed_workspace: Workspace) -> None:
    workspace_id = int(os.environ["WORKSPACE_ID"])
    project = i_authed_workspace.create_project(workspace_id)
    expected_result = set(ProjectResponse.model_fields.keys())
    request_body = project_request_factory()

    result = i_authed_workspace.update_project(workspace_id, project.id, **request_body)

    assert result.model_fields_set == expected_result

    _ = i_authed_workspace.delete_project(workspace_id, project.id)


def test_delete_project(i_authed_workspace: Workspace) -> None:
    workspace_id = int(os.environ["WORKSPACE_ID"])
    project = i_authed_workspace.create_project(workspace_id)

    result = i_authed_workspace.delete_project(workspace_id, project.id)

    assert result is True


def test_delete_project__project_does_not_exist(i_authed_workspace: Workspace) -> None:
    workspace_id = int(os.environ["WORKSPACE_ID"])
    project_id = fake.random_int(max=99999)

    with pytest.raises(BadRequest):
        _ = i_authed_workspace.delete_project(workspace_id, project_id)
