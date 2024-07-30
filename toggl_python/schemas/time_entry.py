from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from toggl_python.schemas.base import BaseSchema


class MeTimeEntryResponseBase(BaseSchema):
    at: datetime
    billable: bool
    description: str
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
