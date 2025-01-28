from __future__ import annotations

import sys
from typing import Dict, Optional, Union

from tests.conftest import fake
from tests.factories.base import datetime_repr_factory


if sys.version_info < (3, 9):
    from backports import zoneinfo
else:
    import zoneinfo


def project_request_factory() -> Dict[str, Union[str, bool, int]]:
    start_date = fake.future_date()

    request_body = {
        "active": fake.boolean(),
        "auto_estimates": fake.boolean(),
        "currency": fake.currency_code(),
        "end_date": fake.date_between(start_date=start_date, end_date="+90d").isoformat(),
        "estimated_hours": fake.random_int(),
        "is_private": fake.boolean(),
        "is_shared": fake.boolean(),
        "name": str(fake.uuid4()),
        "start_date": start_date.isoformat(),
    }

    if fake.boolean():
        request_body["client_id"] = fake.random_int()
    else:
        request_body["client_name"] = fake.word()

    return request_body


def project_response_factory(
    workspace_id: Optional[int] = None,
    end_date: Optional[str] = None,
) -> Dict[str, Union[str, bool, int, None]]:
    timezone_name = fake.timezone()
    timezone = zoneinfo.ZoneInfo(timezone_name)

    response = {
        "active": fake.boolean(),
        "actual_hours": fake.random_int() if fake.boolean() else None,
        "actual_seconds": fake.random_int() if fake.boolean() else None,
        "at": datetime_repr_factory(timezone),
        "auto_estimates": fake.null_boolean(),
        "billable": fake.null_boolean(),
        "can_track_time": fake.boolean(),
        "cid": fake.random_int() if fake.boolean() else None,
        "client_id": fake.random_int() if fake.boolean() else None,
        "color": fake.color(),
        "created_at": datetime_repr_factory(timezone),
        "currency": fake.currency_code() if fake.boolean() else None,
        "estimated_hours": fake.random_int() if fake.boolean() else None,
        "estimated_seconds": fake.random_int() if fake.boolean() else None,
        "fixed_fee": fake.random_int() if fake.boolean() else None,
        "id": fake.random_int(),
        "is_private": fake.boolean(),
        "name": fake.word(),
        "rate": fake.random_int() if fake.boolean() else None,
        "rate_last_updated": datetime_repr_factory(timezone) if fake.boolean() else None,
        "recurring": fake.boolean(),
        "recurring_parameters": None,
        "server_deleted_at": datetime_repr_factory(timezone) if fake.boolean() else None,
        "start_date": fake.past_date().isoformat(),
        "status": fake.word() if fake.boolean() else None,
        "template": fake.null_boolean(),
        "template_id": fake.random_int() if fake.boolean() else None,
        "wid": workspace_id or fake.random_int(),
        "workspace_id": workspace_id or fake.random_int(),
    }
    if fake.boolean() or end_date:
        response["end_date"] = end_date or fake.past_date().isoformat()

    return response
