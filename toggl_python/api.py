from __future__ import annotations

from typing import TYPE_CHECKING

from httpx import Client, HTTPStatusError, Response

from toggl_python.exceptions import BadRequest


if TYPE_CHECKING:
    from toggl_python.auth import BasicAuth, TokenAuth

COMMON_HEADERS: dict[str, str] = {"content-type": "application/json"}
ROOT_URL: str = "https://api.track.toggl.com/api/v9"


class ApiWrapper:
    def __init__(self, auth: BasicAuth | TokenAuth, base_url: str = ROOT_URL) -> None:
        self.client = Client(
            base_url=base_url,
            auth=auth,
            headers=COMMON_HEADERS,
            http2=True,
        )

    def raise_for_status(self, response: Response) -> None:
        """Disable exception chaining to avoid huge not informative traceback."""
        try:
            _ = response.raise_for_status()
        except HTTPStatusError as base_exception:
            raise BadRequest(base_exception.response.text) from None
