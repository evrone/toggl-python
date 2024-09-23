from __future__ import annotations

from datetime import datetime
from typing import List, Optional

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
