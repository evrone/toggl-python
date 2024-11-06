from __future__ import annotations

import sys
from typing import Dict, List, Optional, Set, Union

from tests.conftest import fake
from tests.factories.base import datetime_repr_factory


if sys.version_info < (3, 9):
    from backports import zoneinfo
else:
    import zoneinfo


def workspace_request_factory(
    exclude: Optional[Set[str]] = None,
) -> Dict[str, Union[str, bool, List[int]]]:
    request = {
        "admins": [fake.random_int() for _ in range(fake.random_int(max=5))],
        "name": fake.text(max_nb_chars=139),
        "only_admins_may_create_tags": fake.boolean(),
        "only_admins_see_team_dashboard": fake.boolean(),
        "reports_collapse": fake.boolean(),
    }

    if exclude:
        for excluded_field in exclude:
            del request[excluded_field]

    return request


def workspace_response_factory(
    workspace_id: Optional[int] = None,
) -> Dict[str, Union[str, bool, int, None]]:
    timezone_name = fake.timezone()
    timezone = zoneinfo.ZoneInfo(timezone_name)

    return {
        "admin": fake.boolean(),
        "at": datetime_repr_factory(timezone),
        "business_ws": fake.boolean(),
        "csv_upload": None,
        "default_currency": fake.currency_code(),
        "default_hourly_rate": str(fake.pyfloat()) if fake.boolean() else None,
        "hide_start_end_times": fake.boolean(),
        "ical_enabled": fake.boolean(),
        "ical_url": fake.url() if fake.boolean() else None,
        "id": workspace_id or fake.random_int(),
        "last_modified": datetime_repr_factory(timezone) if fake.boolean() else None,
        "logo_url": fake.image_url(),
        "name": fake.text(max_nb_chars=139),
        "only_admins_may_create_projects": fake.boolean(),
        "only_admins_may_create_tags": fake.boolean(),
        "only_admins_see_billable_rates": fake.boolean(),
        "only_admins_see_team_dashboard": fake.boolean(),
        "organization_id": 8364520,
        "premium": fake.boolean(),
        "projects_billable_by_default": fake.boolean(),
        "projects_enforce_billable": fake.boolean(),
        "projects_private_by_default": fake.boolean(),
        "rate_last_updated": datetime_repr_factory(timezone) if fake.boolean() else None,
        "reports_collapse": fake.boolean(),
        "role": "admin",
        "rounding": fake.random_element(elements=(-1, 0, 1)),
        "rounding_minutes": 0,
        "server_deleted_at": datetime_repr_factory(timezone) if fake.boolean() else None,
        "suspended_at": datetime_repr_factory(timezone) if fake.boolean() else None,
        "working_hours_in_minutes": fake.random_int(min=0, max=59) if fake.boolean() else None,
    }
