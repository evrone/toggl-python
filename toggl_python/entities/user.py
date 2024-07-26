from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from httpx import HTTPStatusError

from toggl_python.api import ApiWrapper
from toggl_python.exceptions import BadRequest
from toggl_python.schemas.current_user import (
    MeResponse,
    MeResponseWithRelatedData,
    UpdateMeRequest,
    UpdateMeResponse,
)


if TYPE_CHECKING:
    from pydantic import EmailStr
class CurrentUser(ApiWrapper):
    prefix: str = "/me"

    def logged(self) -> bool:
        response = self.client.get(url=f"{self.prefix}/logged")
        _ = response.raise_for_status()

        # Returns 200 OK and empty response body
        return response.is_success

    def me(self, with_related_data: bool = False) -> MeResponse:
        response_schema = MeResponseWithRelatedData if with_related_data else MeResponse
        response = self.client.get(
            url=self.prefix,
            params={"with_related_data": with_related_data},
        )
        _ = response.raise_for_status()

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

        try:
            _ = response.raise_for_status()
        except HTTPStatusError as base_exception:
            # Disable exception chaining to avoid huge not informative traceback
            raise BadRequest(base_exception.response.text) from None

        response_body = response.json()
        return UpdateMeResponse.model_validate(response_body)
