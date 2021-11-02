from unittest import mock

import httpx
import pytest

from toggl_python import ReportTimeEntries, TokenAuth
from toggl_python.exceptions import TooManyRequests


def test_raises_too_many_requests():
    auth = TokenAuth("token")
    report_time_entries_api = ReportTimeEntries(auth=auth)
    with mock.patch.object(
        report_time_entries_api.client,
        "get",
        mock.MagicMock(__name__="get", return_value=httpx.Response(status_code=429, text="test")),
    ):
        with pytest.raises(TooManyRequests):
            report_time_entries_api.list()
