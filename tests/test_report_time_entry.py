from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING, Dict, Union

import pytest
from httpx import Response
from pydantic import ValidationError
from toggl_python.schemas.report_time_entry import SearchReportTimeEntriesResponse

from tests.responses.report_time_entry_post import SEARCH_REPORT_TIME_ENTRY_RESPONSE


if TYPE_CHECKING:
    from respx import MockRouter
    from toggl_python.entities.report_time_entry import ReportTimeEntry


def test_search_report_time_entries__without_params(
    authed_report_time_entry: ReportTimeEntry,
) -> None:
    error_message = "At least one parameter must be set"

    with pytest.raises(ValidationError, match=error_message):
        _ = authed_report_time_entry.search(workspace_id=123)


@pytest.mark.parametrize(
    argnames="request_body, start_date, end_date",
    argvalues=(
        (
            {"start_date": "2020-06-10T00:00:00+00:00", "end_date": "2020-10-01T00:00:00+00:00"},
            datetime(2020, 6, 10, tzinfo=timezone.utc),
            datetime(2020, 10, 1, tzinfo=timezone.utc),
        ),
        (
            {"start_date": "2023-09-12T00:00:00-03:00", "end_date": "2023-10-12T00:00:00-01:00"},
            "2023-09-12T00:00:00-03:00",
            "2023-10-12T00:00:00-01:00",
        ),
    ),
)
def test_search_report_time_entries__with_start_and_end_date(
    request_body: Dict[str, str],
    start_date: Union[datetime, str],
    end_date: Union[datetime, str],
    response_report_mock: MockRouter,
    authed_report_time_entry: ReportTimeEntry,
) -> None:
    fake_workspace_id = 123
    uri = f"/{fake_workspace_id}/search/time_entries"
    mocked_route = response_report_mock.post(uri, json=request_body).mock(
        return_value=Response(status_code=200, json=[SEARCH_REPORT_TIME_ENTRY_RESPONSE]),
    )
    expected_result = [
        SearchReportTimeEntriesResponse.model_validate(SEARCH_REPORT_TIME_ENTRY_RESPONSE)
    ]

    result = authed_report_time_entry.search(
        workspace_id=fake_workspace_id, start_date=start_date, end_date=end_date
    )

    assert mocked_route.called is True
    assert result == expected_result


def test_search_report_time_entries__with_all_params(
    response_report_mock: MockRouter,
    authed_report_time_entry: ReportTimeEntry,
) -> None:
    fake_workspace_id = 123
    request_body = {
        "start_date": "2021-12-20T00:00:00+00:00",
        "end_date": "2021-12-30T00:00:00+00:00",
        "user_ids": [30809356],
        "project_ids": [202793182],
        "page_size": 10,
        "first_row_number": 11,
    }
    uri = f"/{fake_workspace_id}/search/time_entries"
    mocked_route = response_report_mock.post(uri, json=request_body).mock(
        return_value=Response(status_code=200, json=[SEARCH_REPORT_TIME_ENTRY_RESPONSE]),
    )
    expected_result = [
        SearchReportTimeEntriesResponse.model_validate(SEARCH_REPORT_TIME_ENTRY_RESPONSE)
    ]

    result = authed_report_time_entry.search(
        workspace_id=fake_workspace_id,
        start_date=request_body["start_date"],
        end_date=request_body["end_date"],
        user_ids=request_body["user_ids"],
        project_ids=request_body["project_ids"],
        page_size=request_body["page_size"],
        page_number=1,
    )

    assert mocked_route.called is True
    assert result == expected_result
