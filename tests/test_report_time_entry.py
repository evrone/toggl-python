from __future__ import annotations

from typing import TYPE_CHECKING, Union

import pytest
from httpx import Response
from pydantic import ValidationError
from toggl_python.schemas.report_time_entry import SearchReportTimeEntriesResponse

from tests.conftest import fake
from tests.responses.report_time_entry_post import SEARCH_REPORT_TIME_ENTRY_RESPONSE


if TYPE_CHECKING:
    from datetime import date

    from respx import MockRouter
    from toggl_python.entities.report_time_entry import ReportTimeEntry


def test_search_report_time_entries__without_params(
    authed_report_time_entry: ReportTimeEntry,
) -> None:
    error_message = "At least one parameter must be set"

    with pytest.raises(ValidationError, match=error_message):
        _ = authed_report_time_entry.search(workspace_id=123)


@pytest.mark.parametrize(
    argnames="start_date, end_date",
    argvalues=(
        (
            fake.date_this_decade(before_today=True).isoformat(),
            fake.date_this_decade(before_today=True).isoformat(),
        ),
        (
            fake.date_this_decade(before_today=True),
            fake.date_this_decade(before_today=True),
        ),
    ),
)
def test_search_report_time_entries__with_start_and_end_date(
    start_date: Union[date, str],
    end_date: Union[date, str],
    response_report_mock: MockRouter,
    authed_report_time_entry: ReportTimeEntry,
) -> None:
    fake_workspace_id = 123
    uri = f"/{fake_workspace_id}/search/time_entries"
    request_body = {
        "start_date": start_date if isinstance(start_date, str) else start_date.isoformat(),
        "end_date": end_date if isinstance(end_date, str) else end_date.isoformat(),
    }
    mocked_route = response_report_mock.post(uri, json=request_body).mock(
        return_value=Response(status_code=200, json=[SEARCH_REPORT_TIME_ENTRY_RESPONSE]),
    )
    expected_result = [
        SearchReportTimeEntriesResponse.model_validate(SEARCH_REPORT_TIME_ENTRY_RESPONSE)
    ]

    result = authed_report_time_entry.search(
        workspace_id=fake_workspace_id,
        start_date=start_date,
        end_date=end_date,
    )

    assert mocked_route.called is True
    assert result == expected_result


def test_search_report_time_entries__with_all_params(
    response_report_mock: MockRouter,
    authed_report_time_entry: ReportTimeEntry,
) -> None:
    fake_workspace_id = fake.random_int(min=1)
    page_size = fake.random_int(min=1, max=100)
    request_body = {
        "start_date": fake.date(),
        "end_date": fake.date(),
        "user_ids": [fake.random_int()],
        "project_ids": [fake.random_int()],
        "page_size": page_size,
        "first_row_number": page_size + 1,
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
