from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Union

from tests.conftest import fake


if TYPE_CHECKING:
    from backports.zoneinfo import ZoneInfo
    from pydantic_core import TzInfo


try:
    import zoneinfo
except ImportError:
    from backports import zoneinfo


def datetime_repr_factory(timezone: Union[ZoneInfo, TzInfo, None] = None) -> str:
    if not timezone:
        timezone_name = fake.timezone()
        timezone = zoneinfo.ZoneInfo(timezone_name)

    return fake.date_time_this_decade(tzinfo=timezone).isoformat(timespec="seconds")


def bulk_edit_response_factory() -> Dict[str, List[Union[int, Dict[str, Union[int, str]]]]]:
    return {
        "success": [fake.random_int() for _ in range(fake.random_int(10))],
        "failure": [
            {"id": fake.random_int(), "message": fake.text(max_nb_chars=64)}
            for _ in range(fake.random_int(4))
        ],
    }
