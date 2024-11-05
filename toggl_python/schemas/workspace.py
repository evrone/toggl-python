from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic.fields import Field

from toggl_python.schemas.base import BaseSchema, SinceParamSchemaMixin


class WorkspaceResponseBase(BaseSchema):
    admin: bool
    at: datetime
    business_ws: bool = Field(description="Is workspace on Premium subscription")
    csv_upload: Optional[List]
    default_currency: str
    default_hourly_rate: Optional[float]
    hide_start_end_times: bool
    ical_enabled: bool
    ical_url: Optional[str]
    id: int
    last_modified: Optional[datetime]
    logo_url: str
    name: str
    only_admins_may_create_projects: bool
    only_admins_may_create_tags: bool
    only_admins_see_billable_rates: bool
    only_admins_see_team_dashboard: bool
    organization_id: int
    premium: bool
    projects_billable_by_default: bool
    projects_enforce_billable: bool
    projects_private_by_default: bool
    rate_last_updated: Optional[datetime]
    reports_collapse: bool
    role: str
    rounding: int = Field(le=1, ge=-1)
    rounding_minutes: int
    server_deleted_at: Optional[datetime]
    suspended_at: Optional[datetime]
    working_hours_in_minutes: Optional[int]


class WorkspaceResponse(WorkspaceResponseBase):
    pass


class GetWorkspacesQueryParams(SinceParamSchemaMixin, BaseSchema):
    pass


class UpdateWorkspaceRequest(BaseSchema):
    admins: Optional[List[int]] = None
    only_admins_may_create_tags: Optional[bool] = None
    only_admins_see_team_dashboard: Optional[bool] = None
    reports_collapse: Optional[bool] = None
    name: Optional[str] = Field(default=None, min_length=1, max_length=140)
