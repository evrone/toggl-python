from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Union

from pydantic import AwareDatetime, field_serializer, model_serializer

from toggl_python.schemas.base import BaseSchema, SinceParamSchemaMixin


class BulkEditTimeEntriesOperations(str, Enum):
    add = "add"
    remove = "remove"
    # Renamed to avoid using system keyword
    change = "replace"


class BulkEditTimeEntriesFieldNames(str, Enum):
    billable = "billable"
    description = "description"
    duration = "duration"
    project_id = "project_id"
    shared_with_user_ids = "shared_with_user_ids"
    start = "start"
    stop = "stop"
    tag_ids = "tag_ids"
    tags = "tags"
    task_id = "task_id"
    user_id = "user_id"


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


class MeTimeEntryQueryParams(SinceParamSchemaMixin, BaseSchema):
    meta: bool
    before: Optional[AwareDatetime] = None
    start_date: Optional[AwareDatetime] = None
    end_date: Optional[AwareDatetime] = None

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


class TimeEntryRequest(BaseSchema):
    billable: Optional[bool]
    description: Optional[str]
    project_id: Optional[int]
    tag_ids: Optional[List[int]]
    task_id: Optional[int]
    user_id: Optional[int]
    duration: Optional[int]
    start: Optional[AwareDatetime]
    stop: Optional[AwareDatetime]
    shared_with_user_ids: Optional[List[int]]
    tags: Optional[List[str]]

    @field_serializer("start", "stop", when_used="json")
    def serialize_datetimes(self, value: Optional[datetime]) -> Optional[str]:
        if not value:
            return value

        return value.isoformat()


class TimeEntryCreateRequest(BaseSchema):
    created_with: str
    start: AwareDatetime
    workspace_id: int

    @field_serializer("start", when_used="json")
    def serialize_datetimes(self, value: Optional[datetime]) -> Optional[str]:
        if not value:
            return value

        return value.isoformat()


class BulkEditTimeEntriesOperation(BaseSchema):
    operation: BulkEditTimeEntriesOperations
    field_name: BulkEditTimeEntriesFieldNames
    field_value: Union[bool, str, int, AwareDatetime, List[int], List[str]]

    @model_serializer(when_used="json")
    def serialize_schema(self) -> Dict:
        return {
            "op": self.operation,
            "path": f"/{self.field_name}",
            "value": self.field_value,
        }


class BulkEditTimeEntriesResponseFailure(BaseSchema):
    id: int
    message: str


class BulkEditTimeEntriesResponse(BaseSchema):
    success: List[int]
    failure: List[BulkEditTimeEntriesResponseFailure]
