from __future__ import annotations

import os
import time
from typing import TYPE_CHECKING, List, Union

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
    # Field `status` is not set until first fetch request
    optional_fields = {"end_date", "status"}
    expected_result = set(ProjectResponse.model_fields.keys()) - optional_fields

    result = i_authed_workspace.create_project(workspace_id, name=fake.uuid4())

    assert result.model_fields_set == expected_result

    _ = i_authed_workspace.delete_project(workspace_id, result.id)


def test_create_project__all_params(i_authed_workspace: Workspace) -> None:
    workspace_id = int(os.environ["WORKSPACE_ID"])
    request_body = project_request_factory()
    # Requires existing object ids
    if "client_id" in request_body:
        del request_body["client_id"]
    optional_fields = {"status"}
    expected_result = set(ProjectResponse.model_fields.keys()) - optional_fields

    result = i_authed_workspace.create_project(workspace_id, **request_body)

    assert result.model_fields_set == expected_result

    _ = i_authed_workspace.delete_project(workspace_id, result.id)


def test_get_projects__without_query_params(i_authed_workspace: Workspace) -> None:
    workspace_id = int(os.environ["WORKSPACE_ID"])
    project = i_authed_workspace.create_project(workspace_id, name=fake.uuid4())
    # Field `status` is set to `archived` after first fetch request, `end_date` is still absent
    optional_fields = {"end_date"}
    expected_result = set(ProjectResponse.model_fields.keys()) - optional_fields

    result = i_authed_workspace.get_projects(workspace_id)

    assert result[0].model_fields_set == expected_result

    _ = i_authed_workspace.delete_project(workspace_id, project.id)


def test_get_projects__with_active_query_param(i_authed_workspace: Workspace) -> None:
    workspace_id = int(os.environ["WORKSPACE_ID"])
    project_prefix_name = fake.word()
    active_project = i_authed_workspace.create_project(
        workspace_id, active=True, name=f"{project_prefix_name}123"
    )
    irrelevant_project = i_authed_workspace.create_project(
        workspace_id, active=False, name=f"{project_prefix_name}456"
    )

    # Filter by common name to exclude irrelevant projects
    result = i_authed_workspace.get_projects(workspace_id, name=project_prefix_name, active=True)

    project_ids = {project.id for project in result}
    assert irrelevant_project.id not in project_ids
    assert active_project.id in project_ids

    _ = i_authed_workspace.delete_project(workspace_id, active_project.id)
    _ = i_authed_workspace.delete_project(workspace_id, irrelevant_project.id)


@pytest.mark.parametrize(
    ("field_name", "field_value"),
    [("billable", False), ("only_me", True)],
)
def test_get_projects__with_simple_query_params(
    field_name: str, field_value: Union[bool, List[int]], i_authed_workspace: Workspace
) -> None:
    workspace_id = int(os.environ["WORKSPACE_ID"])
    project_prefix_name = fake.word()
    first_project = i_authed_workspace.create_project(
        workspace_id, name=f"{project_prefix_name}123"
    )
    second_project = i_authed_workspace.create_project(
        workspace_id, name=f"{project_prefix_name}456"
    )

    # Filter by common name to exclude irrelevant projects
    result = i_authed_workspace.get_projects(
        workspace_id, name=project_prefix_name, **{field_name: field_value}
    )

    project_ids = {project.id for project in result}
    assert second_project.id in project_ids
    assert first_project.id in project_ids

    _ = i_authed_workspace.delete_project(workspace_id, first_project.id)
    _ = i_authed_workspace.delete_project(workspace_id, second_project.id)


def test_get_projects__since_query_param(i_authed_workspace: Workspace) -> None:
    workspace_id = int(os.environ["WORKSPACE_ID"])
    first_created_project = i_authed_workspace.create_project(
        workspace_id, active=True, name=fake.uuid4()
    )
    # Necessary to make Projects creation time different
    time.sleep(1)
    last_created_project = i_authed_workspace.create_project(
        workspace_id, active=True, name=fake.uuid4()
    )
    last_project_created_timestamp = int(last_created_project.created_at.timestamp())

    result = i_authed_workspace.get_projects(workspace_id, since=last_project_created_timestamp)

    project_ids = {project.id for project in result}
    assert last_created_project.id in project_ids
    assert first_created_project.id not in project_ids

    _ = i_authed_workspace.delete_project(workspace_id, first_created_project.id)
    _ = i_authed_workspace.delete_project(workspace_id, last_created_project.id)


def test_get_projects__with_statuses_query_params(i_authed_workspace: Workspace) -> None:
    workspace_id = int(os.environ["WORKSPACE_ID"])
    archived_project = i_authed_workspace.create_project(workspace_id, name=fake.uuid4())
    active_project = i_authed_workspace.create_project(
        workspace_id, active=True, name=fake.uuid4()
    )
    upcoming_project = i_authed_workspace.create_project(
        workspace_id, start_date=fake.future_date(), active=True, name=fake.uuid4()
    )
    start_date = fake.past_date()
    ended_project = i_authed_workspace.create_project(
        workspace_id,
        start_date=start_date.isoformat(),
        end_date=fake.date_between(start_date=start_date).isoformat(),
        active=True,
        name=fake.uuid4(),
    )
    status_to_instance_id = {
        "archived": archived_project.id,
        "active": active_project.id,
        "upcoming": upcoming_project.id,
        "ended": ended_project.id,
    }
    status = fake.random_element(elements=status_to_instance_id.keys())
    expected_result = status_to_instance_id[status]

    result = i_authed_workspace.get_projects(workspace_id, statuses=status)

    project_ids = {project.id for project in result}
    irrelevant_project_ids = set(status_to_instance_id.values())
    irrelevant_project_ids.remove(expected_result)
    assert expected_result in project_ids
    assert not irrelevant_project_ids.intersection(project_ids)

    _ = i_authed_workspace.delete_project(workspace_id, archived_project.id)
    _ = i_authed_workspace.delete_project(workspace_id, active_project.id)
    _ = i_authed_workspace.delete_project(workspace_id, upcoming_project.id)
    _ = i_authed_workspace.delete_project(workspace_id, ended_project.id)


def test_get_projects__with_page_and_per_page(i_authed_workspace: Workspace) -> None:
    workspace_id = int(os.environ["WORKSPACE_ID"])
    project_prefix_name = fake.word()
    first_created_project = i_authed_workspace.create_project(
        workspace_id, active=True, name=f"{project_prefix_name}123"
    )
    last_created_project = i_authed_workspace.create_project(
        workspace_id, active=True, name=f"{project_prefix_name}456"
    )

    # Filter by common name to exclude irrelevant projects
    result = i_authed_workspace.get_projects(
        workspace_id, name=project_prefix_name, page=2, per_page=1
    )

    project_ids = {project.id for project in result}
    assert last_created_project.id in project_ids
    assert first_created_project.id not in project_ids

    _ = i_authed_workspace.delete_project(workspace_id, first_created_project.id)
    _ = i_authed_workspace.delete_project(workspace_id, last_created_project.id)


def test_get_projects__only_templates(i_authed_workspace: Workspace) -> None:
    workspace_id = int(os.environ["WORKSPACE_ID"])
    template_project = i_authed_workspace.create_project(
        workspace_id, template=True, name=fake.uuid4()
    )
    usual_project = i_authed_workspace.create_project(workspace_id, active=True, name=fake.uuid4())

    result = i_authed_workspace.get_projects(workspace_id, only_templates=True)

    project_ids = {project.id for project in result}
    assert usual_project.id not in project_ids
    assert template_project.id in project_ids

    _ = i_authed_workspace.delete_project(workspace_id, template_project.id)
    _ = i_authed_workspace.delete_project(workspace_id, usual_project.id)


def test_get_projects__sort_field_and_sort_order(i_authed_workspace: Workspace) -> None:
    workspace_id = int(os.environ["WORKSPACE_ID"])
    project_suffix_name = fake.word()
    first_created_project = i_authed_workspace.create_project(
        workspace_id, active=True, name=f"a{project_suffix_name}"
    )
    last_created_project = i_authed_workspace.create_project(
        workspace_id, active=True, name=f"b{project_suffix_name}"
    )

    # Filter by common name to exclude irrelevant projects
    result = i_authed_workspace.get_projects(
        workspace_id, name=project_suffix_name, sort_field="name", sort_order="desc"
    )

    project_ids = [project.id for project in result]
    assert [last_created_project.id, first_created_project.id] == project_ids

    _ = i_authed_workspace.delete_project(workspace_id, first_created_project.id)
    _ = i_authed_workspace.delete_project(workspace_id, last_created_project.id)


def test_get_project_by_id(i_authed_workspace: Workspace) -> None:
    workspace_id = int(os.environ["WORKSPACE_ID"])
    project = i_authed_workspace.create_project(workspace_id, name=fake.uuid4())
    # Field `status` is set to `archived` after first fetch request, `end_date` is still absent
    optional_fields = {"end_date"}
    expected_result = set(ProjectResponse.model_fields.keys()) - optional_fields

    result = i_authed_workspace.get_project(workspace_id, project.id)

    assert result.model_fields_set == expected_result

    _ = i_authed_workspace.delete_project(workspace_id, project.id)


def test_me_get_projects__without_query_params(
    i_authed_user: CurrentUser, i_authed_workspace: Workspace
) -> None:
    workspace_id = int(os.environ["WORKSPACE_ID"])
    project = i_authed_workspace.create_project(workspace_id, name=fake.uuid4(), active=True)
    another_project = i_authed_workspace.create_project(
        workspace_id, name=fake.uuid4(), active=True
    )
    expected_result = set(ProjectResponse.model_fields.keys())

    result = i_authed_user.get_projects()

    project_ids = {item.id for item in result}
    assert result[0].model_fields_set == expected_result
    assert another_project.id in project_ids
    assert project.id in project_ids

    _ = i_authed_workspace.delete_project(workspace_id, project.id)
    _ = i_authed_workspace.delete_project(workspace_id, another_project.id)


def test_me_get_projects__include_archived_query_param(
    i_authed_user: CurrentUser, i_authed_workspace: Workspace
) -> None:
    workspace_id = int(os.environ["WORKSPACE_ID"])
    # Is archived and not active project is the same?
    project = i_authed_workspace.create_project(workspace_id, active=True, name=fake.uuid4())
    archived_project = i_authed_workspace.create_project(
        workspace_id, active=False, name=fake.uuid4()
    )
    optional_fields = {"end_date"}
    expected_result = set(ProjectResponse.model_fields.keys()) - optional_fields

    result = i_authed_user.get_projects(include_archived=True)

    project_ids = {project.id for project in result}
    assert result[0].model_fields_set == expected_result
    assert archived_project.id in project_ids
    assert project.id in project_ids

    _ = i_authed_workspace.delete_project(workspace_id, project.id)
    _ = i_authed_workspace.delete_project(workspace_id, archived_project.id)


def test_me_get_projects__since_query_param(
    i_authed_user: CurrentUser, i_authed_workspace: Workspace
) -> None:
    workspace_id = int(os.environ["WORKSPACE_ID"])
    first_created_project = i_authed_workspace.create_project(
        workspace_id, active=True, name=fake.uuid4()
    )
    # Necessary to make Projects creation time different
    time.sleep(1)
    last_created_project = i_authed_workspace.create_project(
        workspace_id, active=True, name=fake.uuid4()
    )
    optional_fields = {"end_date"}
    expected_result = set(ProjectResponse.model_fields.keys()) - optional_fields
    last_project_created_timestamp = int(last_created_project.created_at.timestamp())

    result = i_authed_user.get_projects(since=last_project_created_timestamp)

    project_ids = {project.id for project in result}
    assert result[0].model_fields_set == expected_result
    assert last_created_project.id in project_ids
    assert first_created_project.id not in project_ids

    _ = i_authed_workspace.delete_project(workspace_id, first_created_project.id)
    _ = i_authed_workspace.delete_project(workspace_id, last_created_project.id)


def test_me_get_paginated_projects__without_query_params(
    i_authed_user: CurrentUser, i_authed_workspace: Workspace
) -> None:
    workspace_id = int(os.environ["WORKSPACE_ID"])
    project = i_authed_workspace.create_project(workspace_id, active=True, name=fake.uuid4())
    optional_fields = {"end_date"}
    expected_result = set(ProjectResponse.model_fields.keys()) - optional_fields

    result = i_authed_user.get_paginated_projects()

    assert result[0].model_fields_set == expected_result
    assert any(item.id == project.id for item in result)

    _ = i_authed_workspace.delete_project(workspace_id, project.id)


def test_me_get_paginated_projects__since_query_param(
    i_authed_user: CurrentUser, i_authed_workspace: Workspace
) -> None:
    # ? Add archived projects and check that it is not present?
    workspace_id = int(os.environ["WORKSPACE_ID"])
    first_created_project = i_authed_workspace.create_project(
        workspace_id, active=True, name=fake.uuid4()
    )
    # Necessary to make Projects creation time different
    time.sleep(1)
    last_created_project = i_authed_workspace.create_project(
        workspace_id, active=True, name=fake.uuid4()
    )
    optional_fields = {"end_date"}
    expected_result = set(ProjectResponse.model_fields.keys()) - optional_fields
    last_project_created_timestamp = int(last_created_project.created_at.timestamp())

    result = i_authed_user.get_paginated_projects(since=last_project_created_timestamp)

    project_ids = {project.id for project in result}
    assert result[0].model_fields_set == expected_result
    assert last_created_project.id in project_ids
    assert first_created_project.id not in project_ids

    _ = i_authed_workspace.delete_project(workspace_id, first_created_project.id)
    _ = i_authed_workspace.delete_project(workspace_id, last_created_project.id)


def test_me_get_paginated_projects__start_project_id_param(
    i_authed_user: CurrentUser, i_authed_workspace: Workspace
) -> None:
    workspace_id = int(os.environ["WORKSPACE_ID"])
    first_project = i_authed_workspace.create_project(workspace_id, active=True, name=fake.uuid4())
    second_project = i_authed_workspace.create_project(
        workspace_id, active=True, name=fake.uuid4()
    )
    optional_fields = {"end_date"}
    expected_result = set(ProjectResponse.model_fields.keys()) - optional_fields

    result = i_authed_user.get_paginated_projects(start_project_id=second_project.id)

    project_ids = {project.id for project in result}
    assert result[0].model_fields_set == expected_result
    assert second_project.id in project_ids
    assert first_project.id not in project_ids

    _ = i_authed_workspace.delete_project(workspace_id, first_project.id)
    _ = i_authed_workspace.delete_project(workspace_id, second_project.id)


def test_me_get_paginated_projects__per_page(
    i_authed_user: CurrentUser, i_authed_workspace: Workspace
) -> None:
    workspace_id = int(os.environ["WORKSPACE_ID"])
    first_project = i_authed_workspace.create_project(workspace_id, active=True, name=fake.uuid4())
    second_project = i_authed_workspace.create_project(
        workspace_id, active=True, name=fake.uuid4()
    )
    optional_fields = {"end_date"}
    expected_result = set(ProjectResponse.model_fields.keys()) - optional_fields

    result = i_authed_user.get_paginated_projects(per_page=1)

    assert result[0].model_fields_set == expected_result
    assert len(result) == 1

    _ = i_authed_workspace.delete_project(workspace_id, first_project.id)
    _ = i_authed_workspace.delete_project(workspace_id, second_project.id)


def test_update_project(i_authed_workspace: Workspace) -> None:
    workspace_id = int(os.environ["WORKSPACE_ID"])
    project = i_authed_workspace.create_project(workspace_id, name=fake.uuid4())
    full_request_body = project_request_factory()
    random_param = fake.random_element(full_request_body.keys())
    request_body = {random_param: full_request_body[random_param]}
    old_param_value = getattr(project, random_param)
    optional_fields = {"end_date"}
    expected_result = set(ProjectResponse.model_fields.keys()) - optional_fields

    result = i_authed_workspace.update_project(workspace_id, project.id, **request_body)

    assert result.model_fields_set == expected_result
    assert getattr(result, random_param) != old_param_value

    _ = i_authed_workspace.delete_project(workspace_id, project.id)


def test_update_project__all_params(i_authed_workspace: Workspace) -> None:
    workspace_id = int(os.environ["WORKSPACE_ID"])
    project = i_authed_workspace.create_project(workspace_id, name=fake.uuid4())
    request_body = project_request_factory()
    # Requires existing object ids
    if "client_id" in request_body:
        del request_body["client_id"]
    expected_result = set(ProjectResponse.model_fields.keys())

    result = i_authed_workspace.update_project(workspace_id, project.id, **request_body)

    assert result.model_fields_set == expected_result

    _ = i_authed_workspace.delete_project(workspace_id, project.id)


def test_delete_project(i_authed_workspace: Workspace) -> None:
    workspace_id = int(os.environ["WORKSPACE_ID"])
    project = i_authed_workspace.create_project(workspace_id, name=fake.uuid4())

    result = i_authed_workspace.delete_project(workspace_id, project.id)

    assert result is True


def test_delete_project__project_does_not_exist(i_authed_workspace: Workspace) -> None:
    workspace_id = int(os.environ["WORKSPACE_ID"])
    project_id = fake.random_int(max=99999)

    with pytest.raises(BadRequest):
        _ = i_authed_workspace.delete_project(workspace_id, project_id)
