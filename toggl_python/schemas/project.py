from __future__ import annotations

from datetime import date, datetime
from typing import List, Optional

from pydantic import field_serializer

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
    end_date: Optional[datetime]
    estimated_hours: Optional[int]
    estimated_seconds: Optional[int]
    fixed_fee: Optional[int]
    id: int
    is_private: bool
    is_shared: bool
    name: str
    permissions: Optional[str]
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
    billable: Optional[bool] = None
    client_id: Optional[int] = None
    client_name: Optional[str] = None
    currency: Optional[str] = None
    end_date: Optional[date] = None
    estimated_hours: Optional[int] = None
    is_private: Optional[bool] = None
    is_shared: Optional[bool] = None
    name: Optional[str] = None
    rate: Optional[int] = None
    start_date: Optional[date] = None
    template: Optional[bool] = None
    template_id: Optional[int] = None

    @field_serializer("start_date", "end_date", when_used="json")
    def serialize_datetimes(self, value: Optional[date]) -> Optional[str]:
        if not value:
            return value

        return value.isoformat()
