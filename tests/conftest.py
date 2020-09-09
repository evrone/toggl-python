import pytest

from tests.fixtures import REPORT_TIME_ENTRIES_RESPONSE, TIME_ENTRIES_RESPONSE
from toggl_python import ReportTimeEntries, TimeEntries


@pytest.fixture
def patch_report_time_entries(monkeypatch):
    class MockResponse:
        def __init__(self, *args, **kwargs):
            pass

        @staticmethod
        def json():
            return REPORT_TIME_ENTRIES_RESPONSE

    monkeypatch.setattr(ReportTimeEntries, "get", MockResponse, raising=False)


@pytest.fixture
def patch_time_entries(monkeypatch):
    class MockResponse:
        def __init__(self, *args, **kwargs):
            pass

        @staticmethod
        def json():
            return TIME_ENTRIES_RESPONSE

    monkeypatch.setattr(TimeEntries, "get", MockResponse, raising=False)
