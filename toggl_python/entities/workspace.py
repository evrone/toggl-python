from __future__ import annotations

from typing import TYPE_CHECKING, List, Union

from toggl_python.api import ApiWrapper
from toggl_python.schemas.workspace import GetWorkspacesQueryParams, WorkspaceResponse


if TYPE_CHECKING:
    from datetime import datetime


class Workspace(ApiWrapper):
    prefix: str = "/workspaces"

    def get(self, workspace_id: int) -> WorkspaceResponse:
        response = self.client.get(url=f"{self.prefix}/{workspace_id}")
        self.raise_for_status(response)

        response_body = response.json()

        return WorkspaceResponse.model_validate(response_body)

    def list(self, since: Union[int, datetime, None] = None) -> List[WorkspaceResponse]:
        payload_schema = GetWorkspacesQueryParams(since=since)
        params = payload_schema.model_dump(mode="json", exclude_none=True)

        response = self.client.get(url=self.prefix, params=params)
        self.raise_for_status(response)

        response_body = response.json()

        return [
            WorkspaceResponse.model_validate(workspace_data) for workspace_data in response_body
        ]
