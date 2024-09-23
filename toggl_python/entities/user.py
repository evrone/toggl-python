from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union

from toggl_python.api import ApiWrapper
from toggl_python.schemas.current_user import (
    DateFormat,
    DurationFormat,
    MeFeaturesResponse,
    MePreferencesResponse,
    MeResponse,
    MeResponseWithRelatedData,
    TimeFormat,
    UpdateMePasswordRequest,
    UpdateMePreferencesRequest,
    UpdateMeRequest,
    UpdateMeResponse,
)
from toggl_python.schemas.time_entry import (
    MeTimeEntryQueryParams,
    MeTimeEntryResponse,
    MeTimeEntryWithMetaResponse,
    MeWebTimerResponse,
)


if TYPE_CHECKING:
    from datetime import datetime

    from pydantic import EmailStr


class CurrentUser(ApiWrapper):
    prefix: str = "/me"

    def logged(self) -> bool:
        response = self.client.get(url=f"{self.prefix}/logged")
        self.raise_for_status(response)

        # Returns 200 OK and empty response body
        return response.is_success

    def me(self, with_related_data: bool = False) -> MeResponse:
        response_schema = MeResponseWithRelatedData if with_related_data else MeResponse
        response = self.client.get(
            url=self.prefix,
            params={"with_related_data": with_related_data},
        )
        self.raise_for_status(response)

        response_body = response.json()

        return response_schema.model_validate(response_body)

    def update_me(
        self,
        beginning_of_week: Optional[int] = None,
        country_id: Optional[int] = None,
        default_workspace_id: Optional[int] = None,
        email: Optional[EmailStr] = None,
        fullname: Optional[str] = None,
        timezone: Optional[str] = None,
    ) -> UpdateMeResponse:
        """Update instance without validating if new value is equal to current one.

        So API request will be sent anyway.
        """
        payload_schema = UpdateMeRequest(
            beginning_of_week=beginning_of_week,
            country_id=country_id,
            default_workspace_id=default_workspace_id,
            email=email,
            fullname=fullname,
            timezone=timezone,
        )
        payload = payload_schema.model_dump(mode="json", exclude_none=True, exclude_unset=True)

        response = self.client.put(url=self.prefix, json=payload)
        self.raise_for_status(response)

        response_body = response.json()
        return UpdateMeResponse.model_validate(response_body)

    def change_password(self, current_password: str, new_password: str) -> bool:
        """Validate and change user password.

        API response does not indicate about successful password change,
        that is why return if response is successful.
        """
        payload_schema = UpdateMePasswordRequest(
            current_password=current_password, new_password=new_password
        )
        payload = payload_schema.model_dump_json()

        response = self.client.put(url=self.prefix, content=payload)
        self.raise_for_status(response)

        return response.is_success

    def features(self) -> List[MeFeaturesResponse]:
        response = self.client.get(url=f"{self.prefix}/features")
        self.raise_for_status(response)
        response_body = response.json()

        return [
            MeFeaturesResponse.model_validate(workspace_features)
            for workspace_features in response_body
        ]

    def preferences(self) -> MePreferencesResponse:
        response = self.client.get(url=f"{self.prefix}/preferences")
        self.raise_for_status(response)
        response_body = response.json()

        return MePreferencesResponse.model_validate(response_body)

    def update_preferences(
        self,
        date_format: Optional[DateFormat] = None,
        duration_format: Optional[DurationFormat] = None,
        time_format: Optional[TimeFormat] = None,
    ) -> bool:
        """Update different formats using pre-defined Enums.

        API documentation is not up to date, available fields to update are found manually.
        """
        payload_schema = UpdateMePreferencesRequest(
            date_format=date_format,
            duration_format=duration_format,
            timeofday_format=time_format,
        )
        payload = payload_schema.model_dump_json(exclude_none=True, exclude_unset=True)

        response = self.client.post(url=f"{self.prefix}/preferences", content=payload)
        self.raise_for_status(response)

        return response.is_success

    def get_time_entry(
        self, time_entry_id: int, meta: bool = False
    ) -> Union[MeTimeEntryResponse, MeTimeEntryWithMetaResponse]:
        """Intentionally use the same schema for requests with `include_sharing=true`.

        Tested responses do not differ from requests with `include_sharing=false`
        that is why there is no `include_sharing` method argument.
        """
        response = self.client.get(
            url=f"{self.prefix}/time_entries/{time_entry_id}",
            params={"meta": meta},
        )
        self.raise_for_status(response)

        response_schema = MeTimeEntryWithMetaResponse if meta else MeTimeEntryResponse

        response_body = response.json()
        return response_schema.model_validate(response_body)

    def get_current_time_entry(self) -> Optional[MeTimeEntryResponse]:
        """Return empty response if there is no running TimeEntry."""
        response = self.client.get(url=f"{self.prefix}/time_entries/current")
        self.raise_for_status(response)

        response_body = response.json()
        return MeTimeEntryResponse.model_validate(response_body) if response_body else None

    def get_time_entries(
        self,
        meta: bool = False,
        since: Union[int, datetime, None] = None,
        before: Union[str, datetime, None] = None,
        start_date: Union[str, datetime, None] = None,
        end_date: Union[str, datetime, None] = None,
    ) -> List[Union[MeTimeEntryResponse, MeTimeEntryWithMetaResponse]]:
        """Intentionally use the same schema for requests with `include_sharing=true`.

        Tested responses do not differ from requests with `include_sharing=false`
        that is why there is no `include_sharing` method argument.
        """
        payload_schema = MeTimeEntryQueryParams(
            meta=meta,
            since=since,
            before=before,
            start_date=start_date,
            end_date=end_date,
        )
        payload = payload_schema.model_dump(mode="json", exclude_none=True)

        response = self.client.get(url=f"{self.prefix}/time_entries", params=payload)
        self.raise_for_status(response)

        response_schema = MeTimeEntryWithMetaResponse if meta else MeTimeEntryResponse

        response_body = response.json()
        return [response_schema.model_validate(time_entry) for time_entry in response_body]

    def get_web_timer(self) -> MeWebTimerResponse:
        response = self.client.get(url=f"{self.prefix}/web-timer")
        self.raise_for_status(response)

        response_body = response.json()
        return MeWebTimerResponse.model_validate(response_body)
