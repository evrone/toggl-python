from __future__ import annotations

from typing import TYPE_CHECKING, Union

import httpx
import pytest
from pydantic import ValidationError
from toggl_python.auth import BasicAuth
from toggl_python.entities.user import CurrentUser
from toggl_python.exceptions import BadRequest
from toggl_python.schemas.current_user import (
    MeResponse,
    MeResponseWithRelatedData,
    UpdateMeResponse,
)

from tests.responses.me_get import ME_RESPONSE, ME_RESPONSE_SHORT, ME_RESPONSE_WITH_RELATED_DATA
from tests.responses.me_put import UPDATE_ME_RESPONSE


if TYPE_CHECKING:
    from respx import MockRouter


def test_logged__ok(response_mock: MockRouter, authed_current_user: CurrentUser) -> None:
    mocked_route = response_mock.get("/me/logged").mock(
        return_value=httpx.Response(status_code=200),
    )

    result = authed_current_user.logged()

    assert mocked_route.called is True
    assert result is True


def test_logged__exception_is_raised(
    response_mock: MockRouter, authed_current_user: CurrentUser
) -> None:
    mocked_route = response_mock.get("/me/logged").mock(
        return_value=httpx.Response(status_code=403),
    )

    with pytest.raises(httpx.HTTPStatusError):
        _ = authed_current_user.logged()

    assert mocked_route.called is True


def test_me__ok(response_mock: MockRouter, authed_current_user: CurrentUser) -> None:
    mocked_route = response_mock.get("/me").mock(
        return_value=httpx.Response(status_code=200, json=ME_RESPONSE),
    )
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

    result = authed_current_user.me()

    assert mocked_route.called is True
    assert result == expected_result


def test_me__ok__with_empty_fields(response_mock: MockRouter) -> None:
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


def test_me__ok_with_related_data(
    response_mock: MockRouter, authed_current_user: CurrentUser
) -> None:
    mocked_route = response_mock.get("/me").mock(
        return_value=httpx.Response(status_code=200, json=ME_RESPONSE_WITH_RELATED_DATA),
    )
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

    result = authed_current_user.me(with_related_data=True)

    assert mocked_route.called is True
    assert result == expected_result


@pytest.mark.parametrize(
    argnames=("field_name", "field_value"),
    argvalues=[
        ("beginning_of_week", 0),
        ("country_id", 123),
        ("default_workspace_id", 12345678),
        ("email", "new_user@mail.com"),
        ("fullname", "New User"),
        ("timezone", "Europe/Moscow"),
    ],
    ids=(
        "beginning_of_week",
        "country_id",
        "default_workspace_id",
        "email",
        "fullname",
        "timezone",
    ),
)
def test_update_me__ok(
    response_mock: MockRouter,
    authed_current_user: CurrentUser,
    field_name: str,
    field_value: Union[str, int],
) -> None:
    payload = {field_name: field_value}
    fake_response = UPDATE_ME_RESPONSE.copy()
    fake_response.update(**payload)
    mocked_route = response_mock.put("/me").mock(
        return_value=httpx.Response(status_code=200, json=fake_response),
    )
    expected_result = UpdateMeResponse.model_validate(fake_response)

    result = authed_current_user.update_me(**payload)

    assert mocked_route.called is True
    assert result == expected_result


def test_update_me__invalid_email(authed_current_user: CurrentUser) -> None:
    """Raise default Pydantic ValidationError on invalid email.

    Later, it will be wrapped into custom exception with clear error message.
    """
    error_message = "value is not a valid email address"

    with pytest.raises(ValidationError, match=error_message):
        _ = authed_current_user.update_me(email="invalid_mail@@mail.com")


def test_update_me__email_is_already_used(
    response_mock: MockRouter, authed_current_user: CurrentUser
) -> None:
    error_message = "user with this email already exists"
    mocked_route = response_mock.put("/me").mock(
        return_value=httpx.Response(status_code=400, text=error_message),
    )

    with pytest.raises(BadRequest, match=error_message):
        _ = authed_current_user.update_me(email="existing_address@mail.com")

    assert mocked_route.called is True


@pytest.mark.parametrize(
    argnames=("value"),
    argvalues=["Canada", "Europe/Beerlin", "Materic/City"],
    ids=("No city", "Typo", "Not existing timezone"),
)
def test_update_me__invalid_timezone(authed_current_user: CurrentUser, value: str) -> None:
    error_message = f"Specified timezone {value} is invalid"

    with pytest.raises(ValidationError, match=error_message):
        _ = authed_current_user.update_me(timezone=value)


def test_update_me__invalid_default_workspace_id(authed_current_user: CurrentUser) -> None:
    error_message = "Input should be greater than or equal to 1"

    with pytest.raises(ValidationError, match=error_message):
        _ = authed_current_user.update_me(default_workspace_id=0)


def test_update_me__unavailable_default_workspace_id(
    response_mock: MockRouter, authed_current_user: CurrentUser
) -> None:
    """Raise if user is trying to set unavailable Workspace."""
    error_message = "Invalid default_workspace_id"
    mocked_route = response_mock.put("/me").mock(
        return_value=httpx.Response(status_code=400, text=error_message),
    )

    with pytest.raises(BadRequest, match=error_message):
        _ = authed_current_user.update_me(default_workspace_id=11111111)

    assert mocked_route.called is True


@pytest.mark.parametrize(
    argnames=("value", "error_message"),
    argvalues=[
        (-1, "Input should be greater than or equal to 0"),
        (7, "Input should be less than or equal to 6"),
    ],
    ids=("Negative", "More than max allowed value"),
)
def test_update_me__invalid_beginning_of_week(
    authed_current_user: CurrentUser, value: int, error_message: str
) -> None:
    with pytest.raises(ValidationError, match=error_message):
        _ = authed_current_user.update_me(beginning_of_week=value)


def test_update_me__invalid_country_id(authed_current_user: CurrentUser) -> None:
    error_message = "Input should be greater than or equal to 1"

    with pytest.raises(ValidationError, match=error_message):
        _ = authed_current_user.update_me(country_id=0)


def test_update_me__invalid_fullname(authed_current_user: CurrentUser) -> None:
    error_message = "String should have at least 1 character"

    with pytest.raises(ValidationError, match=error_message):
        _ = authed_current_user.update_me(fullname="")
