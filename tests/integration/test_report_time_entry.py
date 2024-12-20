from __future__ import annotations

import os
import sys
from datetime import timedelta
from typing import TYPE_CHECKING

import pytest
from toggl_python.schemas.report_time_entry import (
    SearchReportTimeEntriesResponse,
)

from tests.conftest import fake

# Necessary to mark all tests in module as integration
from tests.integration import pytestmark  # noqa: F401 - imported but unused


if TYPE_CHECKING:
    from toggl_python.entities.report_time_entry import ReportTimeEntry
    from toggl_python.entities.workspace import Workspace


if sys.version_info < (3, 9):
    from backports import zoneinfo
else:
    import zoneinfo



@pytest.mark.parametrize(
    argnames="use_dates_repr",
    argvalues=(True, False),
    ids=("str date arguments", "date date arguments"),
)
def test_search_report_time_entries__with_start_and_end_dates(
    use_dates_repr: bool,
    i_authed_report_time_entry: ReportTimeEntry,
    i_authed_workspace: Workspace,
) -> None:
    workspace_id = int(os.environ["WORKSPACE_ID"])
    timezone_name = fake.timezone()
    tz = zoneinfo.ZoneInfo(timezone_name)
    start_date = fake.date_this_decade()
    delta = fake.random_int(min=1, max=364)
    end_date = start_date + timedelta(days=delta)
    time_entry = i_authed_workspace.create_time_entry(
        workspace_id,
        start_datetime=fake.date_time_between_dates(start_date, end_date, tzinfo=tz),
        created_with=fake.word(),
    )

    expected_result = set(SearchReportTimeEntriesResponse.model_fields.keys())

    result = i_authed_report_time_entry.search(
        workspace_id,
        start_date=start_date.isoformat() if use_dates_repr else start_date,
        end_date=end_date.isoformat() if use_dates_repr else end_date,
    )

    assert result[0].model_fields_set == expected_result

    _ = i_authed_workspace.delete_time_entry(workspace_id, time_entry.id)


def test_search_report_time_entries__not_found(
    i_authed_report_time_entry: ReportTimeEntry,
) -> None:
    workspace_id = int(os.environ["WORKSPACE_ID"])
    # Set explicit date range to avoid finding unexpected existing test TimeEntries
    time_entry_start_date = fake.date_between(start_date="-15y", end_date="-2y")
    delta = fake.random_int(min=1, max=364)
    end_date = time_entry_start_date + timedelta(days=delta)
    start_date = fake.date_between_dates(time_entry_start_date, end_date)

    result = i_authed_report_time_entry.search(
        workspace_id,
        start_date=start_date,
        end_date=end_date,
    )

    assert result == []
