from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import List, Optional

from pydantic import AwareDatetime, field_serializer, field_validator
from pydantic.fields import Field

from toggl_python.schemas.base import BaseSchema


class WorkspaceResponseBase(BaseSchema):
    admin: bool
    api_token: Optional[str] = Field(default=None, deprecated=True)
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
    permissions: Optional[List[str]]
    premium: bool
    profile: int = Field(deprecated=True)
    projects_billable_by_default: bool
    projects_enforce_billable: bool
    projects_private_by_default: bool
    rate_last_updated: Optional[datetime]
    reports_collapse: bool
    role: str
    rounding: int = Field(le=1, ge=-1)
    rounding_minutes: int
    server_deleted_at: Optional[datetime]
    subscription: Optional[List]
    suspended_at: Optional[datetime]
    working_hours_in_minutes: Optional[int]

class WorkspaceResponse(WorkspaceResponseBase):
    pass

class GetWorkspacesQueryParams(BaseSchema):
    since: Optional[AwareDatetime] = None

    @field_validator("since")
    @classmethod
    def check_if_since_is_too_old(cls, value: Optional[datetime]) -> Optional[datetime]:
        if not value:
            return value

        now = datetime.now(tz=timezone.utc)
        three_months = timedelta(days=90)
        utc_value = value.astimezone(tz=timezone.utc)

        if now - three_months > utc_value:
            error_message = "Since cannot be older than 3 months"
            raise ValueError(error_message)

        return value

    @field_serializer("since", when_used="json")
    def serialize_since(self, value: Optional[datetime]) -> Optional[int]:
        if not value:
            return value

        return int(value.timestamp())
