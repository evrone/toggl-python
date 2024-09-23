from typing import Final

from httpx import BasicAuth as HttpxBasicAuth


class BasicAuth(HttpxBasicAuth):
    pass


class TokenAuth(HttpxBasicAuth):
    SECRET: Final[str] = "api_token"

    def __init__(self, token: str) -> None:
        """Render `Authorization` header with required by Toggl API format `<token>:api_token`."""
        super().__init__(username=token, password=self.SECRET)
