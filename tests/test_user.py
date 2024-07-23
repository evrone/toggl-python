from typing import TYPE_CHECKING

import httpx
import pytest
from toggl_python.auth import TokenAuth
from toggl_python.entities.user import CurrentUser


if TYPE_CHECKING:
    from respx import MockRouter


def test_logged__ok(response_mock: "MockRouter") -> None:
    mocked_route = response_mock.get("/me/logged").mock(
        return_value=httpx.Response(status_code=200),
    )
    auth = TokenAuth("token")
    user = CurrentUser(auth=auth)

    result = user.logged()

    assert mocked_route.called is True
    assert result is True


def test_logged__exception_is_raised(response_mock: "MockRouter") -> None:
    mocked_route = response_mock.get("/me/logged").mock(
        return_value=httpx.Response(status_code=403),
    )
    auth = TokenAuth("token")
    user = CurrentUser(auth=auth)

    with pytest.raises(httpx.HTTPStatusError):
        _ = user.logged()

    assert mocked_route.called is True
