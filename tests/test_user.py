from __future__ import annotations

from typing import TYPE_CHECKING, Union

import httpx
import pytest
from pydantic import ValidationError
from toggl_python.auth import BasicAuth
from toggl_python.entities.user import CurrentUser
from toggl_python.exceptions import BadRequest
from toggl_python.schemas.current_user import (
    DateFormat,
    DurationFormat,
    MeFeaturesResponse,
    MePreferencesResponse,
    MeResponse,
    MeResponseWithRelatedData,
    TimeFormat,
    UpdateMeResponse,
)

from tests.conftest import fake
from tests.responses.me_get import (
    ME_FEATURES_RESPONSE,
    ME_PREFERENCES_RESPONSE,
    ME_RESPONSE,
    ME_RESPONSE_SHORT,
    ME_RESPONSE_WITH_RELATED_DATA,
)
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

    with pytest.raises(BadRequest):
        _ = authed_current_user.logged()

    assert mocked_route.called is True


def test_me__ok(response_mock: MockRouter, authed_current_user: CurrentUser) -> None:
    mocked_route = response_mock.get("/me").mock(
        return_value=httpx.Response(status_code=200, json=ME_RESPONSE),
    )
    expected_result = MeResponse.model_validate(ME_RESPONSE)

    result = authed_current_user.me()

    assert mocked_route.called is True
    assert result == expected_result


def test_me__ok__with_empty_fields(response_mock: MockRouter) -> None:
    mocked_route = response_mock.get("/me").mock(
        return_value=httpx.Response(status_code=200, json=ME_RESPONSE_SHORT),
    )
    auth = BasicAuth(username="username", password="pass")
    user = CurrentUser(auth=auth)
    expected_result = MeResponse.model_validate(ME_RESPONSE_SHORT)

    result = user.me()

    assert mocked_route.called is True
    assert result == expected_result


def test_me__ok_with_related_data(
    response_mock: MockRouter, authed_current_user: CurrentUser
) -> None:
    mocked_route = response_mock.get("/me").mock(
        return_value=httpx.Response(status_code=200, json=ME_RESPONSE_WITH_RELATED_DATA),
    )
    expected_result = MeResponseWithRelatedData.model_validate(ME_RESPONSE_WITH_RELATED_DATA)

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


def test_change_password__ok(response_mock: MockRouter, authed_current_user: CurrentUser) -> None:
    mocked_route = response_mock.put("/me").mock(
        return_value=httpx.Response(status_code=200, json=UPDATE_ME_RESPONSE),
    )

    result = authed_current_user.change_password(
        current_password="paSsw0rd",
        new_password="neW_passw0rd",
    )

    assert mocked_route.called is True
    assert result is True


def test_change_password__equal_current_and_new_passwords(
    authed_current_user: CurrentUser,
) -> None:
    error_message = "New password should differ from current password"

    with pytest.raises(ValidationError, match=error_message):
        _ = authed_current_user.change_password(
            current_password="current_Passw0rd", new_password="current_Passw0rd"
        )


def test_change_password__invalid_current_password(
    response_mock: MockRouter, authed_current_user: CurrentUser
) -> None:
    error_message = "Current password is not valid"
    mocked_route = response_mock.put("/me").mock(
        return_value=httpx.Response(status_code=400, text=error_message),
    )

    with pytest.raises(BadRequest, match=error_message):
        _ = authed_current_user.change_password(
            current_password="4incorrect_passworD",
            new_password="New_passw0rd",
        )

    assert mocked_route.called is True


@pytest.mark.parametrize(
    argnames=("value"),
    argvalues=["1", "12345678", "12345Qw"],
    ids=("Too short", "No symbols and chars", "No symbols"),
)
def test_change_password__weak_new_password(authed_current_user: CurrentUser, value: str) -> None:
    error_message = "Password is too weak"

    with pytest.raises(ValidationError, match=error_message):
        _ = authed_current_user.change_password(
            current_password="current_password",
            new_password=value,
        )


def test_features__ok(response_mock: MockRouter, authed_current_user: CurrentUser) -> None:
    mocked_route = response_mock.get("/me/features").mock(
        return_value=httpx.Response(status_code=200, json=ME_FEATURES_RESPONSE),
    )
    expected_result = [
        MeFeaturesResponse.model_validate(workspace_features)
        for workspace_features in ME_FEATURES_RESPONSE
    ]

    result = authed_current_user.features()

    assert mocked_route.called is True
    assert result == expected_result


def test_preferences__ok(response_mock: MockRouter, authed_current_user: CurrentUser) -> None:
    mocked_route = response_mock.get("/me/preferences").mock(
        return_value=httpx.Response(status_code=200, json=ME_PREFERENCES_RESPONSE),
    )
    expected_result = MePreferencesResponse.model_validate(ME_PREFERENCES_RESPONSE)

    result = authed_current_user.preferences()

    assert mocked_route.called is True
    assert result == expected_result


@pytest.mark.parametrize(
    argnames=("field_name", "field_value"),
    argvalues=[
        ("date_format", fake.random_element({item.value for item in DateFormat})),
        ("duration_format", fake.random_element({item.value for item in DurationFormat})),
        ("time_format", fake.random_element({item.value for item in TimeFormat})),
    ],
)
def test_update_preferences__ok(
    response_mock: MockRouter,
    authed_current_user: CurrentUser,
    field_name: str,
    field_value: str,
) -> None:
    payload = {field_name: field_value}
    mocked_route = response_mock.post("/me/preferences").mock(
        return_value=httpx.Response(status_code=200),
    )

    result = authed_current_user.update_preferences(**payload)

    assert mocked_route.called is True
    assert result is True


def test_update_preferences__invalid_duration_format(authed_current_user: CurrentUser) -> None:
    all_values = ", ".join(f"'{item.value}'" for item in DurationFormat)
    last_value = DurationFormat.decimal.value
    allowed_values = all_values.replace(f", '{last_value}'", f" or '{last_value}'")
    error_message = f"Input should be {allowed_values}"

    with pytest.raises(ValidationError, match=error_message):
        _ = authed_current_user.update_preferences(duration_format="extended")


def test_update_preferences__invalid_time_format(authed_current_user: CurrentUser) -> None:
    all_values = ", ".join(f"'{item.value}'" for item in TimeFormat)
    last_value = TimeFormat.hour_24.value
    allowed_values = all_values.replace(f", '{last_value}'", f" or '{last_value}'")
    error_message = f"Input should be {allowed_values}"

    with pytest.raises(ValidationError, match=error_message):
        _ = authed_current_user.update_preferences(time_format="hh:mm B")


def test_update_preferences__invalid_date_format(authed_current_user: CurrentUser) -> None:
    all_values = ", ".join(f"'{item.value}'" for item in DateFormat)
    last_value = DateFormat.dmy_dot.value
    allowed_values = all_values.replace(f", '{last_value}'", f" or '{last_value}'")
    error_message = f"Input should be {allowed_values}"

    with pytest.raises(ValidationError, match=error_message):
        _ = authed_current_user.update_preferences(date_format="DDMMYY")
