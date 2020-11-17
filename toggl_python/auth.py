import typing

import httpx


class BasicAuth(httpx.BasicAuth):
    """"""


class TokenAuth(httpx.BasicAuth):
    SECRET: str = "api_token"

    def __init__(self, token: typing.Union[str, bytes]):
        super().__init__(token, self.SECRET)
