from __future__ import annotations

import os
from typing import Union

import pytest
from toggl_python.auth import TokenAuth
from toggl_python.entities.user import CurrentUser
from toggl_python.exceptions import BadRequest
from toggl_python.schemas.current_user import (
    AlphaFeatureResponse,
    DateFormat,
    DurationFormat,
    MeFeatureResponse,
    MePreferencesResponse,
    MeResponse,
    MeResponseWithRelatedData,
    TimeFormat,
)

from tests.conftest import fake

# Necessary to mark all tests in module as integration
from tests.integration import pytestmark  # noqa: F401 - imported but unused


def test_logged(i_authed_user: CurrentUser) -> None:
    result = i_authed_user.logged()

    assert result is True


def test_logged__unauthorized() -> None:
    token_auth = TokenAuth(token="invalid token")
    user = CurrentUser(auth=token_auth)
    error_message = "Incorrect username and/or password"

    with pytest.raises(BadRequest, match=error_message):
        _ = user.logged()


def test_me__ok(i_authed_user: CurrentUser) -> None:
    expected_result = set(MeResponse.model_fields.keys())

    result = i_authed_user.me()

    assert result.model_fields_set == expected_result


def test_me__with_related_data(i_authed_user: CurrentUser) -> None:
    expected_result = set(MeResponseWithRelatedData.model_fields.keys())

    result = i_authed_user.me(with_related_data=True)

    # Clients fields is present if at least 1 client exists, on test account clients number
    # is unpredictable
    if "clients" not in result.model_fields_set:
        expected_result.remove("clients")

    assert result.model_fields_set == expected_result
    assert result.workspaces[0] is not None


@pytest.mark.parametrize(
    argnames=("field_name", "field_value"),
    argvalues=[
        ("beginning_of_week", fake.random_int(min=0, max=6)),
        ("country_id", fake.random_int(min=100, max=200)),
        ("email", fake.email()),
        ("fullname", fake.name()),
        ("timezone", fake.timezone()),
    ],
    ids=(
        "beginning_of_week",
        "country_id",
        "email",
        "fullname",
        "timezone",
    ),
)
def test_update_me__ok(
    i_authed_user: CurrentUser,
    me_response: MeResponse,
    field_name: str,
    field_value: Union[str, int],
) -> None:
    # default_workspace_id is not tested because it requires method to create and delete workspace
    update_body = {field_name: field_value}
    current_state_body = {field_name: getattr(me_response, field_name)}

    result = i_authed_user.update_me(**update_body)

    assert getattr(result, field_name) == field_value

    _ = i_authed_user.update_me(**current_state_body)


def test_update_me__email_is_already_used(i_authed_user: CurrentUser) -> None:
    error_message = "user with this email already exists"
    used_email = "test@gmail.com"

    with pytest.raises(BadRequest, match=error_message):
        _ = i_authed_user.update_me(email=used_email)


def test_update_me__unavailable_default_workspace_id(i_authed_user: CurrentUser) -> None:
    error_message = "Invalid default_workspace_id"
    invalid_default_workspace_id = fake.random_int(min=2, max=999)

    with pytest.raises(BadRequest, match=error_message):
        _ = i_authed_user.update_me(default_workspace_id=invalid_default_workspace_id)


def test_change_password__ok(i_authed_user: CurrentUser) -> None:
    current_password = os.environ["TOGGL_PASSWORD"]
    new_password = fake.password()

    result = i_authed_user.change_password(current_password, new_password)

    assert result is True

    result = i_authed_user.change_password(
        current_password=new_password, new_password=current_password
    )


def test_change_password__invalid_current_password(i_authed_user: CurrentUser) -> None:
    current_password = fake.password()
    new_password = fake.password()
    error_message = "Current password is not valid"

    with pytest.raises(BadRequest, match=error_message):
        _ = i_authed_user.change_password(current_password, new_password)


def test_features__ok(i_authed_user: CurrentUser) -> None:
    expected_result = set(MeFeatureResponse.model_fields.keys())

    result = i_authed_user.features()

    assert result[0].workspace_id is not None
    assert len(result[0].features) > 0
    assert result[0].features[0].model_fields_set == expected_result


def test_preferences__ok(i_authed_user: CurrentUser) -> None:
    expected_result = set(MePreferencesResponse.model_fields.keys())
    expected_alpha_feature = set(AlphaFeatureResponse.model_fields.keys())

    result = i_authed_user.preferences()

    assert result.model_fields_set == expected_result
    assert len(result.alpha_features) > 0
    assert result.alpha_features[0].model_fields_set == expected_alpha_feature


@pytest.mark.parametrize(
    argnames=("field_name", "schema_field_name", "field_value"),
    argvalues=[
        (
            "date_format",
            "date_format",
            fake.random_element(item.value for item in DateFormat),
        ),
        (
            "duration_format",
            "duration_format",
            fake.random_element(item.value for item in DurationFormat),
        ),
        (
            "time_format",
            "timeofday_format",
            fake.random_element(item.value for item in TimeFormat),
        ),
    ],
    ids=("date_format", "duration_format", "time_format"),
)
def test_update_preferences__ok(
    i_authed_user: CurrentUser,
    me_preferences_response: MePreferencesResponse,
    field_name: str,
    schema_field_name: str,
    field_value: Union[DateFormat, DurationFormat, TimeFormat],
) -> None:
    update_body = {field_name: field_value}
    current_state_body = {field_name: getattr(me_preferences_response, schema_field_name)}

    result = i_authed_user.update_preferences(**update_body)

    assert result is True

    _ = i_authed_user.update_preferences(**current_state_body)
