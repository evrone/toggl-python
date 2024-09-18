from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union

from toggl_python.api import ApiWrapper
from toggl_python.schemas.report_time_entry import (
    SearchReportTimeEntriesRequest,
    SearchReportTimeEntriesResponse,
)


if TYPE_CHECKING:
    from datetime import date

    from toggl_python.auth import BasicAuth, TokenAuth

REPORT_ROOT_URL: str = "https://api.track.toggl.com/reports/api/v3/workspace"
DEFAULT_PAGE_SIZE: int = 50


class ReportTimeEntry(ApiWrapper):
    def __init__(self, auth: Union[BasicAuth, TokenAuth]) -> None:
        super().__init__(auth, base_url=REPORT_ROOT_URL)

    def search(
        self,
        workspace_id: int,
        start_date: Union[date, str, None] = None,
        end_date: Union[date, str, None] = None,
        user_ids: Optional[List[int]] = None,
        project_ids: Optional[List[int]] = None,
        page_size: Optional[int] = None,
        page_number: Optional[int] = None,
    ) -> List[SearchReportTimeEntriesResponse]:
        """Return TimeEntries grouped by common values."""
        # API does not support page number but allows to specify first row number on current page
        # So pagination is achieved by changing its value
        if page_number:
            current_page_size = page_size or DEFAULT_PAGE_SIZE
            first_row_number = page_number * current_page_size + 1
        else:
            first_row_number = None

        payload_schema = SearchReportTimeEntriesRequest(
            start_date=start_date,
            end_date=end_date,
            user_ids=user_ids,
            project_ids=project_ids,
            page_size=page_size,
            first_row_number=first_row_number,
        )
        payload = payload_schema.model_dump(mode="json", exclude_none=True, exclude_unset=True)

        response = self.client.post(url=f"/{workspace_id}/search/time_entries", json=payload)
        self.raise_for_status(response)

        response_body = response.json()
        return [
            SearchReportTimeEntriesResponse.model_validate(report_time_entry_data)
            for report_time_entry_data in response_body
        ]
