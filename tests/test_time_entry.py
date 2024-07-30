from __future__ import annotations

from typing import TYPE_CHECKING

from httpx import Response
from toggl_python.schemas.time_entry import MeTimeEntryResponse, MeTimeEntryWithMetaResponse

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
    mocked_route = response_mock.get(
        f"/me/time_entries/{fake_time_entry_id}?meta=true"
    ).mock(
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
