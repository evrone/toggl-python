from typing import TYPE_CHECKING

import httpx
import pytest
from toggl_python.auth import BasicAuth, TokenAuth
from toggl_python.entities.user import CurrentUser
from toggl_python.schemas.current_user import MeResponse, MeResponseWithRelatedData

from tests.responses import (
    FAKE_TOKEN,
    ME_RESPONSE,
    ME_RESPONSE_SHORT,
    ME_RESPONSE_WITH_RELATED_DATA,
)


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


def test_me__ok(response_mock: "MockRouter") -> None:
    mocked_route = response_mock.get("/me").mock(
        return_value=httpx.Response(status_code=200, json=ME_RESPONSE),
    )
    auth = TokenAuth(FAKE_TOKEN)
    user = CurrentUser(auth=auth)
    expected_result = MeResponse(
        api_token=ME_RESPONSE["api_token"],
        at=ME_RESPONSE["at"],
        authorization_updated_at=ME_RESPONSE["authorization_updated_at"],
        beginning_of_week=ME_RESPONSE["beginning_of_week"],
        country_id=ME_RESPONSE["country_id"],
        created_at=ME_RESPONSE["created_at"],
        default_workspace_id=ME_RESPONSE["default_workspace_id"],
        email=ME_RESPONSE["email"],
        fullname=ME_RESPONSE["fullname"],
        has_password=ME_RESPONSE["has_password"],
        id=ME_RESPONSE["id"],
        image_url=ME_RESPONSE["image_url"],
        intercom_hash=ME_RESPONSE["intercom_hash"],
        openid_email=ME_RESPONSE["openid_email"],
        openid_enabled=ME_RESPONSE["openid_enabled"],
        options=ME_RESPONSE["options"],
        timezone=ME_RESPONSE["timezone"],
        toggl_accounts_id=ME_RESPONSE["toggl_accounts_id"],
        updated_at=ME_RESPONSE["updated_at"],
    )

    result = user.me()

    assert mocked_route.called is True
    assert result == expected_result


def test_me__ok__with_empty_fields(response_mock: "MockRouter") -> None:
    mocked_route = response_mock.get("/me").mock(
        return_value=httpx.Response(status_code=200, json=ME_RESPONSE_SHORT),
    )
    auth = BasicAuth(username="username", password="pass")  # noqa: S106
    user = CurrentUser(auth=auth)
    expected_result = MeResponse(
        at=ME_RESPONSE_SHORT["at"],
        authorization_updated_at=ME_RESPONSE_SHORT["authorization_updated_at"],
        beginning_of_week=ME_RESPONSE_SHORT["beginning_of_week"],  # limit to 1-7
        country_id=ME_RESPONSE_SHORT["country_id"],
        created_at=ME_RESPONSE_SHORT["created_at"],
        default_workspace_id=ME_RESPONSE_SHORT["default_workspace_id"],
        email=ME_RESPONSE_SHORT["email"],
        fullname=ME_RESPONSE_SHORT["fullname"],
        has_password=ME_RESPONSE_SHORT["has_password"],
        id=ME_RESPONSE_SHORT["id"],
        image_url=ME_RESPONSE_SHORT["image_url"],
        openid_email=ME_RESPONSE_SHORT["openid_email"],
        openid_enabled=ME_RESPONSE_SHORT["openid_enabled"],
        timezone=ME_RESPONSE_SHORT["timezone"],
        toggl_accounts_id=ME_RESPONSE_SHORT["toggl_accounts_id"],
        updated_at=ME_RESPONSE_SHORT["updated_at"],
    )

    result = user.me()

    assert mocked_route.called is True
    assert result == expected_result


def test_me__ok_with_related_data(response_mock: "MockRouter") -> None:
    mocked_route = response_mock.get("/me").mock(
        return_value=httpx.Response(status_code=200, json=ME_RESPONSE_WITH_RELATED_DATA),
    )
    auth = TokenAuth(FAKE_TOKEN)
    user = CurrentUser(auth=auth)
    expected_result = MeResponseWithRelatedData(
        api_token=ME_RESPONSE_WITH_RELATED_DATA["api_token"],
        at=ME_RESPONSE_WITH_RELATED_DATA["at"],
        authorization_updated_at=ME_RESPONSE_WITH_RELATED_DATA["authorization_updated_at"],
        beginning_of_week=ME_RESPONSE_WITH_RELATED_DATA["beginning_of_week"],
        clients=ME_RESPONSE_WITH_RELATED_DATA["clients"],
        country_id=ME_RESPONSE_WITH_RELATED_DATA["country_id"],
        created_at=ME_RESPONSE_WITH_RELATED_DATA["created_at"],
        default_workspace_id=ME_RESPONSE_WITH_RELATED_DATA["default_workspace_id"],
        email=ME_RESPONSE_WITH_RELATED_DATA["email"],
        fullname=ME_RESPONSE_WITH_RELATED_DATA["fullname"],
        has_password=ME_RESPONSE_WITH_RELATED_DATA["has_password"],
        id=ME_RESPONSE_WITH_RELATED_DATA["id"],
        image_url=ME_RESPONSE_WITH_RELATED_DATA["image_url"],
        intercom_hash=ME_RESPONSE_WITH_RELATED_DATA["intercom_hash"],
        openid_email=ME_RESPONSE_WITH_RELATED_DATA["openid_email"],
        openid_enabled=ME_RESPONSE_WITH_RELATED_DATA["openid_enabled"],
        options=ME_RESPONSE_WITH_RELATED_DATA["options"],
        projects=ME_RESPONSE_WITH_RELATED_DATA["projects"],
        tags=ME_RESPONSE_WITH_RELATED_DATA["tags"],
        time_entries=ME_RESPONSE_WITH_RELATED_DATA["time_entries"],
        timezone=ME_RESPONSE_WITH_RELATED_DATA["timezone"],
        toggl_accounts_id=ME_RESPONSE_WITH_RELATED_DATA["toggl_accounts_id"],
        updated_at=ME_RESPONSE_WITH_RELATED_DATA["updated_at"],
        workspaces=ME_RESPONSE_WITH_RELATED_DATA["workspaces"],
    )

    result = user.me(with_related_data=True)

    assert mocked_route.called is True
    assert result == expected_result
