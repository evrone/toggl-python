from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import List, Optional

from pydantic import AwareDatetime, field_serializer, field_validator

from toggl_python.schemas.base import BaseSchema


class MeTimeEntryResponseBase(BaseSchema):
    billable: bool
    description: Optional[str]
    project_id: Optional[int]
    tag_ids: List[int]
    task_id: Optional[int]
    user_id: int
    workspace_id: int


class MeTimeEntryResponse(MeTimeEntryResponseBase):
    at: datetime
    duration: int
    duronly: bool
    id: int
    permissions: Optional[List]
    server_deleted_at: Optional[datetime]
    start: datetime
    stop: Optional[datetime]
    tags: List[str]


class MeTimeEntryWithMetaResponse(MeTimeEntryResponse):
    user_avatar_url: str
    user_name: str


class MeTimeEntryQueryParams(BaseSchema):
    meta: bool
    since: Optional[AwareDatetime] = None
    before: Optional[AwareDatetime] = None
    start_date: Optional[AwareDatetime] = None
    end_date: Optional[AwareDatetime] = None

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

    @field_serializer("before", "start_date", "end_date", when_used="json")
    def serialize_datetimes(self, value: Optional[datetime]) -> Optional[str]:
        if not value:
            return value

        return value.isoformat()


class WebTimerTimeEntryResponse(MeTimeEntryResponseBase):
    deleted: Optional[datetime]
    duration_in_seconds: int
    ignore_start_and_stop: bool
    planned_task_id: Optional[int]
    updated_at: datetime
    utc_start: datetime
    utc_stop: datetime


class MeWebTimerResponse(BaseSchema):
    clients: Optional[List]
    projects: Optional[List]
    tags: List
    time_entries: List[WebTimerTimeEntryResponse]
