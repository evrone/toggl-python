"""Module contains simple Web API wraper."""

import typing
from functools import partial
from typing import Any, Dict, Optional

import httpx

from .auth import BasicAuth, TokenAuth
from .exceptions import raise_from_response


class Api:
    """
    Simple api wrapper.
    Allow to interact with official Toggl API via httpx.
    """

    BASE_URL: httpx.URL = httpx.URL("https://api.track.toggl.com/api/v9/")
    HEADERS = {
        "content-type": "application/json",
        "user_agent": "toggl-python",
    }

    def __init__(
        self,
        base_url: typing.Optional[str] = None,
        auth: Optional[typing.Union[BasicAuth, TokenAuth]] = None,
    ):
        if base_url:
            self.BASE_URL = httpx.URL(base_url)
        self.client = httpx.Client(base_url=self.BASE_URL, auth=auth)

    def __getattr__(self, httpmethod: str) -> Any:
        """
        Checking existence of `httpmethod` method in httpx-client
        and `partial` it to our client `api_method`

        :param httpmethod: method name we trying to serve
        :return:
        """
        try:
            method = getattr(self.client, httpmethod)
        except AttributeError:
            raise AttributeError(f"No such http method ({httpmethod})!")

        return partial(self.api_method, method)

    def api_method(
        self,
        method: Any,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """
        Call httpx method with specified url and params

        :param method: method we throwed from httpx-client via `__getattr__`
        :param url: target url we nesting on `BASE_URL`
        :param params: params to pass
        :param data: json-data to pass
        :param files: files to pass
        :return:
        """

        _url = self.BASE_URL.join(url)

        response = (
            method(_url, params=params, headers=self.HEADERS)
            if method.__name__ == "get"
            else method(
                _url,
                params=params,
                json=data,
                files=files,
                headers=self.HEADERS,
            )
        )

        raise_from_response(response)

        return response
