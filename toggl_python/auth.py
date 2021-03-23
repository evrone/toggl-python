import typing

import httpx


class BasicAuth(httpx.BasicAuth):
    """Httpx basic auth class"""


class TokenAuth(httpx.BasicAuth):
    """Httpx basic auth class with token insertion on class init"""

    SECRET: str = "api_token"

    def __init__(self, token: typing.Union[str, bytes]):
        super().__init__(token, self.SECRET)
