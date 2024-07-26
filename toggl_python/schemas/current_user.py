from __future__ import annotations


try:
    import zoneinfo
except ImportError:
    from backports import zoneinfo
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, field_validator
from pydantic.fields import Field
from pydantic_core import Url


class MeResponseBase(BaseModel):
    api_token: Optional[str] = Field(default=None, min_length=32, max_length=32)
    at: datetime
    beginning_of_week: int = Field(ge=0, le=6, description="0 equals to Sunday, 1 - Monday, etc.")
    country_id: Optional[int] = None
    created_at: datetime
    default_workspace_id: int
    email: EmailStr
    fullname: str
    has_password: bool
    id: int
    image_url: Url
    oauth_provides: Optional[List[str]] = None
    openid_email: Optional[EmailStr] = None
    openid_enabled: bool
    options: Optional[List] = None  # not sure, maybe not a list
    timezone: str
    toggl_accounts_id: str = Field(min_length=22, max_length=22)
    updated_at: datetime


class MeResponse(MeResponseBase):
    authorization_updated_at: datetime
    intercom_hash: Optional[str] = Field(default=None, min_length=64, max_length=64)


class UpdateMeRequest(BaseModel):
    beginning_of_week: Optional[int] = Field(default=None, ge=0, le=6)
    country_id: Optional[int] = Field(
        default=None,
        ge=1,
        description="Cannot validate, api documentation does not contain available county_ids",
    )
    default_workspace_id: Optional[int] = Field(
        default=None,
        ge=1,
        description="Cannot check workspace_id availability without making API request",
    )
    email: Optional[EmailStr] = None  # Cannot check uniqueness without making API request
    fullname: Optional[str] = Field(default=None, min_length=1)
    timezone: Optional[str] = None

    @field_validator("timezone")
    @classmethod
    def check_if_timezone_exists(cls, value: Optional[str]) -> Optional[str]:
        if not value or value in zoneinfo.available_timezones():
            return value

        error_message = f"Specified timezone {value} is invalid"
        raise ValueError(error_message)


class UpdateMeResponse(MeResponseBase):
    # Not present in API documentation
    toggl_accounts_updated_at: datetime


class MeResponseWithRelatedData(MeResponse):
    clients: Optional[List]
    projects: Optional[List]
    tags: Optional[List]
    time_entries: Optional[List]
    workspaces: List  # Default workspace is created after signup,
    # check if it is possible not to have workspace at all
