import typing

import httpx


class BasicAuth(httpx.BasicAuth):
    pass


class TokenAuth(httpx.BasicAuth):
    SECRET: str = "api_token"

    def __init__(self, token: typing.Union[str, bytes]):
        self.auth_header = self.build_auth_header(token, self.SECRET)
