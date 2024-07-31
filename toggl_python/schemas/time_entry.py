from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import List, Optional

from pydantic import AwareDatetime, field_serializer, field_validator

from toggl_python.schemas.base import BaseSchema


class MeTimeEntryResponseBase(BaseSchema):
    at: datetime
    billable: bool
    description: Optional[str]
    duration: int
    duronly: bool
    id: int
    permissions: Optional[List]
    project_id: Optional[int]
    server_deleted_at: Optional[datetime]
    start: datetime
    stop: Optional[datetime]
    tag_ids: List[int]
    tags: List[str]
    task_id: Optional[int]
    user_id: int
    workspace_id: int


class MeTimeEntryResponse(MeTimeEntryResponseBase):
    pass


class MeTimeEntryWithMetaResponse(MeTimeEntryResponseBase):
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
