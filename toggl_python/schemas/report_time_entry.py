from __future__ import annotations

from datetime import date
from typing import Dict, List, Optional

from pydantic import AwareDatetime, field_serializer, model_validator

from toggl_python.schemas.base import BaseSchema


class SearchReportTimeEntriesResponse(BaseSchema):
    billable: bool
    billable_amount_in_cents: Optional[int]
    currency: str
    description: Optional[str]
    hourly_rate_in_cents: Optional[int]
    project_id: Optional[int]
    row_number: int
    tag_ids: List[int]
    task_id: Optional[int]
    time_entries: List[ReportTimeEntryItem]
    user_id: int
    username: str


class ReportTimeEntryItem(BaseSchema):
    at: AwareDatetime
    at_tz: AwareDatetime
    id: int
    seconds: int
    start: AwareDatetime
    stop: AwareDatetime


class SearchReportTimeEntriesRequest(BaseSchema):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    project_ids: Optional[List[int]] = None
    user_ids: Optional[List[int]] = None
    page_size: Optional[int] = None
    first_row_number: Optional[int] = None

    @model_validator(mode="before")
    @classmethod
    def check_if_at_least_one_param_is_set(cls, data: Dict[str, str]) -> Dict[str, str]:
        if any(data.values()):
            return data

        error_message = "At least one parameter must be set"
        raise ValueError(error_message)

    @field_serializer("start_date", "end_date", when_used="json")
    def serialize_datetimes(self, value: Optional[date]) -> Optional[str]:
        if not value:
            return value

        return value.isoformat()
