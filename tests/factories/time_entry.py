from __future__ import annotations

from datetime import datetime
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


def time_entry_request_factory(workspace_id: Optional[int] = None) -> Dict[str, Union[str, int]]:
    return {
        "created_with": fake.color_name(),
        "start": _datetime_repr_factory(),
        "workspace_id": workspace_id or fake.random_int(),
    }


def time_entry_response_factory(
    workspace_id: int,
    start: Optional[str] = None,
) -> Dict[str, Union[str, bool, int, None, List]]:
    if start:
        tz = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S%z").tzinfo
    else:
        timezones = fake.timezone()
        tz = zoneinfo.ZoneInfo(timezones)

    return {
        "at": _datetime_repr_factory(tz),
        "billable": fake.boolean(),
        "description": fake.text(max_nb_chars=100),
        "duration": fake.random_int(),
        "duronly": fake.boolean(),
        "id": fake.random_number(digits=11, fix_len=True),
        "permissions": None,
        "project_id": fake.random_int() if fake.boolean() else None,
        "server_deleted_at": (
            fake.date_time_this_month(tzinfo=tz).isoformat(timespec="seconds")
            if fake.boolean()
            else None
        ),
        "start": start or _datetime_repr_factory(tz),
        "stop": _datetime_repr_factory(tz),
        "tag_ids": [],
        "tags": [],
        "task_id": fake.random_int() if fake.boolean() else None,
        "user_id": fake.random_int(),
        "workspace_id": workspace_id,
    }
