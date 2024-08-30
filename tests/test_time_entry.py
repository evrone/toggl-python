from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING, Dict, Union
from unittest.mock import Mock, patch

import pytest
from httpx import Response
from pydantic import ValidationError
from toggl_python.exceptions import BadRequest
from toggl_python.schemas.time_entry import (
    MeTimeEntryResponse,
    MeTimeEntryWithMetaResponse,
    MeWebTimerResponse,
)

from tests.responses.me_get import ME_WEB_TIMER_RESPONSE
from tests.responses.time_entry_get import ME_TIME_ENTRY_RESPONSE, ME_TIME_ENTRY_WITH_META_RESPONSE


if TYPE_CHECKING:
    from respx import MockRouter
    from toggl_python.entities.user import CurrentUser


def test_get_time_entry__without_query_params(
    response_mock: MockRouter, authed_current_user: CurrentUser
) -> None:
    fake_time_entry_id = 123
    mocked_route = response_mock.get(f"/me/time_entries/{fake_time_entry_id}").mock(
        return_value=Response(status_code=200, json=ME_TIME_ENTRY_RESPONSE),
    )
    expected_result = MeTimeEntryResponse.model_validate(ME_TIME_ENTRY_RESPONSE)

    result = authed_current_user.get_time_entry(fake_time_entry_id)

    assert mocked_route.called is True
    assert result == expected_result


def test_get_time_entry__with_meta_query_param(
    response_mock: MockRouter, authed_current_user: CurrentUser
) -> None:
    fake_time_entry_id = 123
    mocked_route = response_mock.get(f"/me/time_entries/{fake_time_entry_id}?meta=true").mock(
        return_value=Response(status_code=200, json=ME_TIME_ENTRY_WITH_META_RESPONSE),
    )
    expected_result = MeTimeEntryWithMetaResponse.model_validate(ME_TIME_ENTRY_WITH_META_RESPONSE)

    result = authed_current_user.get_time_entry(fake_time_entry_id, meta=True)

    assert mocked_route.called is True
    assert result == expected_result


def test_get_current_time_entry__ok(
    response_mock: MockRouter, authed_current_user: CurrentUser
) -> None:
    mocked_route = response_mock.get("/me/time_entries/current").mock(
        return_value=Response(status_code=200, json=ME_TIME_ENTRY_RESPONSE),
    )
    expected_result = MeTimeEntryResponse.model_validate(ME_TIME_ENTRY_RESPONSE)

    result = authed_current_user.get_current_time_entry()

    assert mocked_route.called is True
    assert result == expected_result


def test_get_current_time_entry__no_current_entry(
    response_mock: MockRouter, authed_current_user: CurrentUser
) -> None:
    mocked_route = response_mock.get("/me/time_entries/current").mock(
        return_value=Response(status_code=200, json={}),
    )

    result = authed_current_user.get_current_time_entry()

    assert mocked_route.called is True
    assert result is None


def test_get_time_entries__without_query_params(
    response_mock: MockRouter, authed_current_user: CurrentUser
) -> None:
    fake_response = [ME_TIME_ENTRY_RESPONSE]
    mocked_route = response_mock.get("/me/time_entries").mock(
        return_value=Response(status_code=200, json=fake_response),
    )
    expected_result = [MeTimeEntryResponse.model_validate(ME_TIME_ENTRY_RESPONSE)]

    result = authed_current_user.get_time_entries()

    assert mocked_route.called is True
    assert result == expected_result


def test_get_time_entries__with_meta_query_param(
    response_mock: MockRouter, authed_current_user: CurrentUser
) -> None:
    mocked_route = response_mock.get("/me/time_entries", params={"meta": True}).mock(
        return_value=Response(status_code=200, json=[ME_TIME_ENTRY_WITH_META_RESPONSE]),
    )
    expected_result = [
        MeTimeEntryWithMetaResponse.model_validate(ME_TIME_ENTRY_WITH_META_RESPONSE)
    ]

    result = authed_current_user.get_time_entries(meta=True)

    assert mocked_route.called is True
    assert result == expected_result


@patch("toggl_python.schemas.time_entry.datetime")
@pytest.mark.parametrize(
    argnames="query_params, method_kwargs",
    argvalues=(
        (
            {"since": 1715299200},
            {"since": int(datetime(2024, 5, 10, tzinfo=timezone.utc).timestamp())},
        ),
        ({"since": 1718755200}, {"since": 1718755200}),
        ({"before": "2024-07-28T12:30:43+00:00"}, {"before": "2024-07-28T12:30:43+00:00"}),
        (
            {"before": "2023-01-01T00:00:00+00:00"},
            {"before": datetime(2023, 1, 1, tzinfo=timezone.utc)},
        ),
        (
            {"start_date": "2023-09-12T00:00:00-03:00", "end_date": "2023-10-12T00:00:00-01:00"},
            {"start_date": "2023-09-12T00:00:00-03:00", "end_date": "2023-10-12T00:00:00-01:00"},
        ),
    ),
)
def test_get_time_entries__with_datetime_query_params(
    mocked_datetime: Mock,
    query_params: Dict[str, Union[int, str]],
    method_kwargs: Dict[str, Union[datetime, str]],
    response_mock: MockRouter,
    authed_current_user: CurrentUser,
) -> None:
    query_params["meta"] = False
    # Required to pass `since` query param validation
    mocked_datetime.now.return_value = datetime(2024, 6, 20, tzinfo=timezone.utc)
    mocked_route = response_mock.get("/me/time_entries", params=query_params).mock(
        return_value=Response(status_code=200, json=[ME_TIME_ENTRY_RESPONSE]),
    )
    expected_result = [MeTimeEntryResponse.model_validate(ME_TIME_ENTRY_RESPONSE)]

    result = authed_current_user.get_time_entries(**method_kwargs)

    assert mocked_route.called is True
    assert result == expected_result


@pytest.mark.parametrize(
    argnames="query_params",
    argvalues=(
        {"start_date": "2010-01-01T00:00:00+08:00"},
        {"end_date": "2010-02-01T00:00:00+03:00"},
        {"since": 17223107204, "before": "2024-07-28T00:00:00+10:00"},
        {
            "since": 17223107204,
            "start_date": "2020-11-11T09:30:00-04:00",
            "end_date": "2021-01-11T09:30:00-04:00",
        },
        {
            "before": "2020-12-15T09:30:00-04:00",
            "start_date": "2020-11-11T09:30:00-04:00",
            "end_date": "2021-01-11T09:30:00-04:00",
        },
        {
            "since": 17223107204,
            "before": "2020-12-15T09:30:00-04:00",
            "start_date": "2020-11-11T09:30:00-04:00",
            "end_date": "2021-01-11T09:30:00-04:00",
        },
    ),
)
def test_get_time_entries__invalid_query_params(
    query_params: Dict[str, Union[int, str]],
    response_mock: MockRouter,
    authed_current_user: CurrentUser,
) -> None:
    error_message = "can not be present simultaneously"
    _ = response_mock.get("/me/time_entries", params=query_params).mock(
        return_value=Response(status_code=400, json=error_message),
    )

    with pytest.raises(BadRequest, match=error_message):
        _ = authed_current_user.get_time_entries(**query_params)


@patch("toggl_python.schemas.time_entry.datetime")
def test_get_time_entries__too_old_since_value(
    mocked_datetime: Mock, authed_current_user: CurrentUser
) -> None:
    error_message = "Since cannot be older than 3 months"
    since = datetime(2020, 1, 1, tzinfo=timezone.utc)
    mocked_datetime.now.return_value = datetime(2020, 4, 1, tzinfo=timezone.utc)

    with pytest.raises(ValidationError, match=error_message):
        _ = authed_current_user.get_time_entries(since=since)


def test_get_web_timer__ok(response_mock: MockRouter, authed_current_user: CurrentUser) -> None:
    mocked_route = response_mock.get("/me/web-timer").mock(
        return_value=Response(status_code=200, json=ME_WEB_TIMER_RESPONSE),
    )
    expected_result = MeWebTimerResponse.model_validate(ME_WEB_TIMER_RESPONSE)

    result = authed_current_user.get_web_timer()

    assert mocked_route.called is True
    assert result == expected_result
