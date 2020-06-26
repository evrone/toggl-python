"""Module contains simple Web API wraper."""

import typing
from functools import partial

import httpx

from .auth import BasicAuth, TokenAuth
from .exceptions import STATUS_2_EXCEPTION


class Api:
    """Simple api wraper."""

    BASE_URL: httpx.URL = httpx.URL("https://www.toggl.com/api/v8/")
    HEADERS = {
        "content-type": "application/json",
        "user_agent": "toggl-python",
    }

    def __init__(
        self,
        base_url: typing.Optional[str] = None,
        auth: typing.Union[BasicAuth, TokenAuth] = None,
    ):
        if base_url:
            self.BASE_URL = httpx.URL(base_url)
        self.client = httpx.Client(base_url=self.BASE_URL, auth=auth)

    def __getattr__(self, httpmethod):
        try:
            method = getattr(self.client, httpmethod)
        except AttributeError:
            raise AttributeError(f"No such http method ({httpmethod})!")

        return partial(self.api_method, method)

    def api_method(
        self,
        method: typing.Callable,
        url: str,
        params: dict = None,
        data: dict = None,
        files: dict = None,
    ) -> httpx.Response:
        """
        Call http method with specified url and params
        """

        _url = self.BASE_URL.join(url)

        response = (
            method(_url, headers=self.HEADERS)
            if method.__name__ == "get"
            else method(_url, json=data, files=files)
        )

        if response.status_code == httpx.codes.OK:
            return response
        else:
            exception_class = STATUS_2_EXCEPTION[response.status_code]
            raise exception_class
