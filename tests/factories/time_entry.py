from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Dict, List, Optional, Union

from tests.conftest import fake


if TYPE_CHECKING:
    from backports.zoneinfo import ZoneInfo
    from pydantic_core import TzInfo


try:
    import zoneinfo
except ImportError:
    from backports import zoneinfo


def _datetime_repr_factory(timezone: Union[ZoneInfo, TzInfo, None] = None) -> str:
    if not timezone:
        timezone_name = fake.timezone()
        timezone = zoneinfo.ZoneInfo(timezone_name)

    return fake.date_time_this_decade(tzinfo=timezone).isoformat(timespec="seconds")


def _stop_datetime_repr_factory(
    duration: int, start_repr: str, timezone: Union[ZoneInfo, TzInfo]
) -> str:
    if duration:
        start_datetime = datetime.fromisoformat(start_repr)
        stop_datetime = start_datetime + timedelta(seconds=duration)
    else:
        stop_datetime = fake.date_time_this_decade(tzinfo=timezone)

    return stop_datetime.isoformat(timespec="seconds")


def time_entry_request_factory(workspace_id: Optional[int] = None) -> Dict[str, Union[str, int]]:
    return {
        "created_with": fake.color_name(),
        "start": _datetime_repr_factory(),
        "workspace_id": workspace_id or fake.random_int(),
    }


def time_entry_extended_request_factory(
    workspace_id: Optional[int] = None,
) -> Dict[str, Union[str, bool, int, None, List[Union[str, int]]]]:
    timezone_name = fake.timezone()
    timezone = zoneinfo.ZoneInfo(timezone_name)
    duration = fake.random_int(min=-1)
    start = _datetime_repr_factory(timezone)

    return {
        "created_with": fake.color_name(),
        "billable": fake.boolean(),
        "description": fake.text(max_nb_chars=100),
        "duration": duration,
        "project_id": fake.random_int(),
        "start": start,
        "stop": _stop_datetime_repr_factory(duration, start, timezone),
        "tag_ids": [fake.random_int() for _ in range(fake.random_int(min=0, max=20))],
        "tags": [fake.word() for _ in range(fake.random_int(min=0, max=20))],
        "task_id": fake.random_int(),
        "user_id": fake.random_int(),
        "workspace_id": workspace_id or fake.random_int(),
    }


def time_entry_response_factory(
    workspace_id: int,
    start: Optional[str] = None,
    billable: Optional[bool] = None,
    description: Optional[str] = None,
    duration: Optional[int] = None,
    stop: Optional[str] = None,
    project_id: Optional[int] = None,
    tag_ids: Optional[List[int]] = None,
    tags: Optional[List[str]] = None,
    task_id: Optional[int] = None,
    user_id: Optional[int] = None,
) -> Dict[str, Union[str, bool, int, None, List[Union[str, int]]]]:
    if start:
        tz = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S%z").tzinfo
    else:
        timezone_name = fake.timezone()
        tz = zoneinfo.ZoneInfo(timezone_name)

    return {
        "at": _datetime_repr_factory(tz),
        "billable": billable or fake.boolean(),
        "description": description or fake.text(max_nb_chars=100),
        "duration": duration or fake.random_int(),
        "duronly": fake.boolean(),
        "id": fake.random_number(digits=11, fix_len=True),
        "permissions": None,
        "project_id": project_id or fake.random_int() if fake.boolean() else None,
        "server_deleted_at": (
            fake.date_time_this_month(tzinfo=tz).isoformat(timespec="seconds")
            if fake.boolean()
            else None
        ),
        "start": start or _datetime_repr_factory(tz),
        "stop": stop or _datetime_repr_factory(tz),
        "tag_ids": tag_ids or [],
        "tags": tags or [],
        "task_id": task_id or fake.random_int() if fake.boolean() else None,
        "user_id": user_id or fake.random_int(),
        "workspace_id": workspace_id,
    }
