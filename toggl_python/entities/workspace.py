from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union

from toggl_python.api import ApiWrapper
from toggl_python.schemas.project import ProjectQueryParams, ProjectResponse
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

    def get_project(self, workspace_id: int, project_id: int) -> ProjectResponse:
        response = self.client.get(url=f"{self.prefix}/{workspace_id}/projects/{project_id}")
        self.raise_for_status(response)

        response_body = response.json()

        return ProjectResponse.model_validate(response_body)

    def get_projects(  # noqa: PLR0913 - Too many arguments in function definition (15 > 12)
        self,
        workspace_id: int,
        active: Optional[bool] = None,
        billable: Optional[bool] = None,
        user_ids: Optional[List[int]] = None,
        client_ids: Optional[List[int]] = None,
        group_ids: Optional[List[int]] = None,
        statuses: Optional[str] = None,
        since: Union[int, datetime, None] = None,
        name: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        sort_field: Optional[str] = None,
        sort_order: Optional[str] = None,
        only_templates: Optional[bool] = None,
        only_me: Optional[bool] = None,
    ) -> List[ProjectResponse]:
        payload_schema = ProjectQueryParams(
            active=active,
            billable=billable,
            user_ids=user_ids,
            client_ids=client_ids,
            group_ids=group_ids,
            statuses=statuses,
            since=since,
            name=name,
            page=page,
            per_page=per_page,
            sort_field=sort_field,
            sort_order=sort_order,
            only_templates=only_templates,
            only_me=only_me,
        )
        payload = payload_schema.model_dump(mode="json", exclude_none=True)

        response = self.client.get(url=f"{self.prefix}/{workspace_id}/projects", params=payload)
        self.raise_for_status(response)

        response_body = response.json()

        return [ProjectResponse.model_validate(project_data) for project_data in response_body]
