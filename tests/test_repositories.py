from tests.fixtures import REPORT_TIME_ENTRIES_RESPONSE, TIME_ENTRIES_RESPONSE

from toggl_python import ReportTimeEntries, ReportTimeEntry, TimeEntries, TimeEntry, TokenAuth


def test_report_time_entries_pagination(patch_report_time_entries):
    auth = TokenAuth("token")
    report_time_entries = ReportTimeEntries(auth=auth).list()
    total_count = REPORT_TIME_ENTRIES_RESPONSE["total_count"]
    per_page = REPORT_TIME_ENTRIES_RESPONSE["per_page"]
    assert report_time_entries.total_count == total_count
    assert report_time_entries.per_page == per_page
    assert len(report_time_entries) == len(REPORT_TIME_ENTRIES_RESPONSE["data"])
    for report_time_entry in report_time_entries:
        assert isinstance(report_time_entry, ReportTimeEntry)


def test_time_entries_no_pagination(patch_time_entries):
    auth = TokenAuth("token")
    time_entries = TimeEntries(auth=auth).list()
    assert not hasattr(time_entries, "total_count")
    assert not hasattr(time_entries, "per_page")
    assert len(time_entries) == len(TIME_ENTRIES_RESPONSE)
    for time_entry in time_entries:
        assert isinstance(time_entry, TimeEntry)
