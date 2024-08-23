from __future__ import annotations

from typing import Dict, List, Union


SEARCH_REPORT_TIME_ENTRY_RESPONSE: Dict[str, Union[bool, None, str, int, List]] = {
    "billable": False,
    "billable_amount_in_cents": None,
    "currency": "USD",
    "description": "sample description",
    "hourly_rate_in_cents": None,
    "project_id": 202793182,
    "row_number": 1,
    "tag_ids": [16501871],
    "task_id": None,
    "time_entries": [
        {
            "at": "2024-07-30T08:14:38+00:00",
            "at_tz": "2024-07-30T11:14:38+03:00",
            "id": 3545645770,
            "seconds": 52,
            "start": "2024-07-30T11:13:46+03:00",
            "stop": "2024-07-30T11:14:38+03:00",
        }
    ],
    "user_id": 30809356,
    "username": "test user",
}
