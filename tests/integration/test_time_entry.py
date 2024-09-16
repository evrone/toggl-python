from __future__ import annotations

import os
from typing import TYPE_CHECKING

from toggl_python.schemas.time_entry import MeTimeEntryResponse

from tests.factories.time_entry import (
    time_entry_extended_request_factory,
    time_entry_request_factory,
)

# Necessary to mark all tests in module as integration
from tests.integration import pytestmark  # noqa: F401 - imported but unused


if TYPE_CHECKING:
    from toggl_python.entities.workspace import Workspace


def test_create_time_entry__only_necessary_fields(i_authed_workspace: Workspace) -> None:
    workspace_id = int(os.environ["WORKSPACE_ID"])
    request_body = time_entry_request_factory(workspace_id)
    expected_result = set(MeTimeEntryResponse.model_fields.keys())

    result = i_authed_workspace.create_time_entry(
        workspace_id,
        start_datetime=request_body["start"],
        created_with=request_body["created_with"],
    )

    assert result.model_fields_set == expected_result

    _ = i_authed_workspace.delete_time_entry(workspace_id=workspace_id, time_entry_id=result.id)


def test_create_time_entry__all_fields(i_authed_workspace: Workspace) -> None:
    """Create TimeEntry without fields `tag_ids` and `task_id`.

    `tag_ids` requires existing Tags and it is complicated to test
    and `task_id` is available on paid plan.
    """
    workspace_id = int(os.environ["WORKSPACE_ID"])
    request_body = time_entry_extended_request_factory(workspace_id)
    expected_result = set(MeTimeEntryResponse.model_fields.keys())

    result = i_authed_workspace.create_time_entry(
        workspace_id,
        start_datetime=request_body["start"],
        created_with=request_body["created_with"],
        billable=request_body["billable"],
        description=request_body["description"],
        duration=request_body["duration"],
        project_id=os.environ["PROJECT_ID"],
        stop=request_body["stop"],
        tags=request_body["tags"],
        user_id=os.environ["USER_ID"],
    )

    assert result.model_fields_set == expected_result

    _ = i_authed_workspace.delete_time_entry(workspace_id=workspace_id, time_entry_id=result.id)
