from __future__ import annotations

from typing import TYPE_CHECKING

from httpx import Client


if TYPE_CHECKING:
    from toggl_python.auth import BasicAuth, TokenAuth

COMMON_HEADERS: dict[str, str] = {"content-type": "application/json"}
ROOT_URL: str = "https://api.track.toggl.com/api/v9"


class ApiWrapper:
    def __init__(self, auth: BasicAuth | TokenAuth) -> None:
        self.client = Client(
            base_url=ROOT_URL,
            auth=auth,
            headers=COMMON_HEADERS,
            http2=True,
        )
