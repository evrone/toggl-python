from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Dict, List, Optional, Union

from pydantic import field_serializer, model_validator

from toggl_python.schemas.base import BaseSchema, SinceParamSchemaMixin


class ProjectResponse(BaseSchema):
    active: bool
    actual_hours: Optional[int]
    actual_seconds: Optional[int]
    at: datetime
    auto_estimates: Optional[bool]
    billable: Optional[bool]
    can_track_time: bool
    client_id: Optional[int]
    color: str
    created_at: datetime
    currency: Optional[str]
    # Present if Project has end_date
    end_date: Optional[datetime] = None
    estimated_hours: Optional[int]
    estimated_seconds: Optional[int]
    fixed_fee: Optional[int]
    id: int
    is_private: bool
    is_shared: bool
    name: str
    rate: Optional[int]
    rate_last_updated: Optional[datetime]
    recurring: bool
    recurring_parameters: Optional[List]
    server_deleted_at: Optional[datetime]
    start_date: datetime
    status: Optional[str] = None
    template: Optional[bool]
    template_id: Optional[int]
    workspace_id: int

    @model_validator(mode="after")
    def remove_optional_fields(self) -> ProjectResponse:
        """Remove field if Project object does not have it."""
        if self.end_date is None:
            del self.end_date
        if self.status is None:
            del self.status

        return self


class ProjectQueryParams(SinceParamSchemaMixin, BaseSchema):
    active: Optional[bool]
    billable: Optional[bool]
    user_ids: Optional[List[int]]
    client_ids: Optional[List[int]]
    group_ids: Optional[List[int]]
    statuses: Optional[str]
    name: Optional[str]
    page: Optional[int]
    per_page: Optional[int]
    sort_field: Optional[str]
    sort_order: Optional[str]
    only_templates: Optional[bool]
    only_me: Optional[bool]


class MeProjectsQueryParams(SinceParamSchemaMixin, BaseSchema):
    include_archived: Optional[bool]


class MePaginatedProjectsQueryParams(SinceParamSchemaMixin, BaseSchema):
    start_project_id: Optional[int]
    per_page: Optional[int]


class CreateProjectRequest(BaseSchema):
    active: Optional[bool] = None
    auto_estimates: Optional[bool] = None
    client_id: Optional[int] = None
    client_name: Optional[str] = None
    currency: Optional[str] = None
    end_date: Optional[date] = None
    estimated_hours: Optional[int] = None
    is_private: Optional[bool] = None
    is_shared: Optional[bool] = None
    name: Optional[str] = None
    start_date: Optional[date] = None
    template: Optional[bool] = None
    template_id: Optional[int] = None

    @field_serializer("start_date", "end_date", when_used="json")
    def serialize_datetimes(self, value: Optional[date]) -> Optional[str]:
        if not value:
            return value

        return value.isoformat()

    @model_validator(mode="before")
    @classmethod
    def validate_model(
        cls, data: Dict[str, Union[bool, int, str, date, None]]
    ) -> Dict[str, Union[bool, int, str, date, None]]:
        if data["client_id"] and data["client_name"]:
            error_message = "Both client_id and client_name provided"
            raise ValueError(error_message)

        if (
            data["start_date"]
            and data["end_date"]
            and (
                datetime.fromisoformat(data["start_date"])
                > datetime.fromisoformat(data["end_date"])
            )
        ):
            error_message = "Project timeframe is not valid"
            raise ValueError(error_message)

        return data


class BulkEditProjectsFieldNames(str, Enum):
    auto_estimates = "auto_estimates"
    end_date = "end_date"
    estimated_hours = "estimated_hours"
    is_private = "is_private"
    project_name = "name"
    start_date = "start_date"
    template = "template"
