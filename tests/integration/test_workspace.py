from __future__ import annotations

import os
from typing import TYPE_CHECKING

from toggl_python.schemas.workspace import WorkspaceResponse

# Necessary to mark all tests in module as integration
from tests.integration import pytestmark  # noqa: F401 - imported but unused


if TYPE_CHECKING:
    from toggl_python.entities.workspace import Workspace


def test_get_workspace_by_id(i_authed_workspace: Workspace) -> None:
    workspace_id = int(os.environ["WORKSPACE_ID"])
    expected_result = set(WorkspaceResponse.model_fields.keys())

    result = i_authed_workspace.get(workspace_id)

    assert result.model_fields_set == expected_result


def test_get_workspaces__without_query_params(i_authed_workspace: Workspace)-> None:
    expected_result = set(WorkspaceResponse.model_fields.keys())

    result = i_authed_workspace.list()

    assert result[0].model_fields_set == expected_result
