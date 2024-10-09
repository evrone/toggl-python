from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union

from toggl_python.api import ApiWrapper
from toggl_python.schemas.base import (
    BulkEditMethodParams,
    BulkEditOperation,
    BulkEditResponse,
)
from toggl_python.schemas.project import CreateProjectRequest, ProjectQueryParams, ProjectResponse
from toggl_python.schemas.time_entry import (
    MeTimeEntryResponse,
    TimeEntryCreateRequest,
    TimeEntryRequest,
)
from toggl_python.schemas.workspace import (
    GetWorkspacesQueryParams,
    UpdateWorkspaceRequest,
    WorkspaceResponse,
)


if TYPE_CHECKING:
    from datetime import date, datetime


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

    def update(
        self,
        workspace_id: int,
        admins: Optional[List[int]] = None,
        only_admins_may_create_tags: Optional[bool] = None,
        only_admins_see_team_dashboard: Optional[bool] = None,
        reports_collapse: Optional[bool] = None,
        name: Optional[str] = None,
    ) -> WorkspaceResponse:
        """Allow to update Workspace instance fields which are available on free plan.

        Request body parameters `default_hourly_rate`, `default_currency`, `rounding`,
        `rounding_minutes`, `only_admins_see_billable_rates`, `projects_billable_by_default`,
        `rate_change_mode`, `project_private_by_default`, `projects_enforce_billable` are
        available only on paid plan. That is why they are not listed in method arguments.
        """
        request_body_schema = UpdateWorkspaceRequest(
            admins=admins,
            only_admins_may_create_tags=only_admins_may_create_tags,
            only_admins_see_team_dashboard=only_admins_see_team_dashboard,
            reports_collapse=reports_collapse,
            name=name,
        )
        request_body = request_body_schema.model_dump(
            mode="json", exclude_none=True, exclude_unset=True
        )

        response = self.client.put(url=f"{self.prefix}/{workspace_id}", json=request_body)
        self.raise_for_status(response)

        response_body = response.json()
        return WorkspaceResponse.model_validate(response_body)

    def create_project(  # noqa: PLR0913 - Too many arguments in function definition
        self,
        workspace_id: int,
        active: Optional[bool] = None,
        auto_estimates: Optional[bool] = None,
        client_id: Optional[int] = None,
        client_name: Optional[str] = None,
        currency: Optional[str] = None,
        end_date: Union[date, str, None] = None,
        estimated_hours: Optional[int] = None,
        is_private: Optional[bool] = None,
        is_shared: Optional[bool] = None,
        name: Optional[str] = None,
        start_date: Union[date, str, None] = None,
        template: Optional[bool] = None,
        template_id: Optional[int] = None,
    ) -> ProjectResponse:
        """Allow to update Project instance fields which are available on free plan.

        Request body parameters `billable`, `color`, `rate`, `fixed_fee` are available
        only on paid plan. That is why they are not listed in method arguments.

        Field `status` is affected by fields `active`, `start_date`, `end_date` and
        cannot be changed explicitly.
        """
        request_body_schema = CreateProjectRequest(
            active=active,
            auto_estimates=auto_estimates,
            client_id=client_id,
            client_name=client_name,
            currency=currency,
            end_date=end_date,
            estimated_hours=estimated_hours,
            is_private=is_private,
            is_shared=is_shared,
            name=name,
            start_date=start_date,
            template=template,
            template_id=template_id,
        )
        request_body = request_body_schema.model_dump(
            mode="json", exclude_none=True, exclude_unset=True
        )

        response = self.client.post(
            url=f"{self.prefix}/{workspace_id}/projects", json=request_body
        )
        self.raise_for_status(response)

        response_body = response.json()
        return ProjectResponse.model_validate(response_body)

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

    def update_project(  # noqa: PLR0913 - Too many arguments in function definition
        self,
        workspace_id: int,
        project_id: int,
        active: Optional[bool] = None,
        auto_estimates: Optional[bool] = None,
        client_id: Optional[int] = None,
        client_name: Optional[str] = None,
        currency: Optional[str] = None,
        end_date: Union[date, str, None] = None,
        estimated_hours: Optional[int] = None,
        is_private: Optional[bool] = None,
        is_shared: Optional[bool] = None,
        name: Optional[str] = None,
        start_date: Union[date, str, None] = None,
        template: Optional[bool] = None,
        template_id: Optional[int] = None,
    ) -> ProjectResponse:
        """Allow to update Project instance fields which are available on free plan.

        Request body parameters `billable`, `color`, `rate`, `fixed_fee` are available
        only on paid plan. That is why they are not listed in method arguments.

        Field `status` is affected by fields `active`, `start_date`, `end_date` and
        cannot be changed explicitly.
        """
        request_body_schema = CreateProjectRequest(
            active=active,
            auto_estimates=auto_estimates,
            client_id=client_id,
            client_name=client_name,
            currency=currency,
            end_date=end_date,
            estimated_hours=estimated_hours,
            is_private=is_private,
            is_shared=is_shared,
            name=name,
            start_date=start_date,
            template=template,
            template_id=template_id,
        )
        request_body = request_body_schema.model_dump(
            mode="json", exclude_none=True, exclude_unset=True
        )

        response = self.client.put(
            url=f"{self.prefix}/{workspace_id}/projects/{project_id}", json=request_body
        )
        self.raise_for_status(response)

        response_body = response.json()
        return ProjectResponse.model_validate(response_body)

    def bulk_edit_projects(
        self,
        workspace_id: int,
        project_ids: List[int],
        operations: List[BulkEditOperation],
    ) -> BulkEditResponse:
        """Bulk edit Projects with limited fields set.

        It is not possible to bulk edit fields `active`, `client_id`, `client_name`, `is_shared`,
        `template_id`.
        `currency` is also not allowed for non-admin users.
        """
        validated_args_schema = BulkEditMethodParams(ids=project_ids, operations=operations)
        validated_args = validated_args_schema.model_dump(mode="json")
        ids = validated_args["ids"]
        request_body = [
            operation.model_dump(mode="json", exclude_none=True) for operation in operations
        ]

        response = self.client.patch(
            url=f"{self.prefix}/{workspace_id}/projects/{ids}", json=request_body
        )
        self.raise_for_status(response)

        response_body = response.json()

        return BulkEditResponse.model_validate(response_body)

    def delete_project(self, workspace_id: int, project_id: int) -> bool:
        response = self.client.delete(url=f"{self.prefix}/{workspace_id}/projects/{project_id}")
        self.raise_for_status(response)

        return response.is_success

    def create_time_entry(
        self,
        workspace_id: int,
        start_datetime: Union[datetime, str],
        created_with: str,
        billable: Optional[bool] = None,
        description: Optional[str] = None,
        duration: Optional[int] = None,
        stop: Optional[str] = None,
        project_id: Optional[int] = None,
        tag_ids: Optional[List[int]] = None,
        tags: Optional[List[str]] = None,
        task_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> MeTimeEntryResponse:
        request_body_schema = TimeEntryCreateRequest(
            created_with=created_with,
            start=start_datetime,
            workspace_id=workspace_id,
            billable=billable,
            description=description,
            duration=duration,
            stop=stop,
            project_id=project_id,
            tag_ids=tag_ids,
            tags=tags,
            task_id=task_id,
            user_id=user_id,
        )
        request_body = request_body_schema.model_dump(
            mode="json", exclude_none=True, exclude_unset=True
        )

        response = self.client.post(
            url=f"{self.prefix}/{workspace_id}/time_entries", json=request_body
        )
        self.raise_for_status(response)

        response_body = response.json()

        return MeTimeEntryResponse.model_validate(response_body)

    def update_time_entry(  # noqa: PLR0913 - Too many arguments in function definition (13 > 12)
        self,
        workspace_id: int,
        time_entry_id: int,
        billable: Optional[bool] = None,
        description: Optional[str] = None,
        duration: Optional[int] = None,
        project_id: Optional[int] = None,
        shared_with_user_ids: Optional[List[int]] = None,
        start: Optional[datetime] = None,
        stop: Optional[datetime] = None,
        tag_ids: Optional[List[int]] = None,
        tags: Optional[List[str]] = None,
        task_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> MeTimeEntryResponse:
        """Some params from docs are not listed because API don't use them to change object."""
        request_body_schema = TimeEntryRequest(
            billable=billable,
            description=description,
            duration=duration,
            project_id=project_id,
            shared_with_user_ids=shared_with_user_ids,
            start=start,
            stop=stop,
            tag_ids=tag_ids,
            tags=tags,
            task_id=task_id,
            user_id=user_id,
        )
        request_body = request_body_schema.model_dump(mode="json", exclude_none=True)

        response = self.client.put(
            url=f"{self.prefix}/{workspace_id}/time_entries/{time_entry_id}", json=request_body
        )
        self.raise_for_status(response)

        response_body = response.json()

        return MeTimeEntryResponse.model_validate(response_body)

    def delete_time_entry(self, workspace_id: int, time_entry_id: int) -> bool:
        response = self.client.delete(
            url=f"{self.prefix}/{workspace_id}/time_entries/{time_entry_id}"
        )
        self.raise_for_status(response)

        return response.is_success

    def bulk_edit_time_entries(
        self,
        workspace_id: int,
        time_entry_ids: List[int],
        operations: List[BulkEditOperation],
    ) -> BulkEditResponse:
        validated_args_schema = BulkEditMethodParams(ids=time_entry_ids, operations=operations)
        validated_args = validated_args_schema.model_dump(mode="json")
        ids = validated_args["ids"]

        request_body = [
            operation.model_dump(mode="json", exclude_none=True) for operation in operations
        ]

        response = self.client.patch(
            url=f"{self.prefix}/{workspace_id}/time_entries/{ids}", json=request_body
        )
        self.raise_for_status(response)

        response_body = response.json()

        return BulkEditResponse.model_validate(response_body)

    def stop_time_entry(self, workspace_id: int, time_entry_id: int) -> MeTimeEntryResponse:
        response = self.client.patch(
            url=f"{self.prefix}/{workspace_id}/time_entries/{time_entry_id}/stop"
        )
        self.raise_for_status(response)

        response_body = response.json()

        return MeTimeEntryResponse.model_validate(response_body)
