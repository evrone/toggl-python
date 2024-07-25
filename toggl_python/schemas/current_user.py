from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr
from pydantic.fields import Field
from pydantic_core import Url


class MeResponse(BaseModel):
    api_token: Optional[str] = Field(default=None, min_length=32, max_length=32)
    at: datetime
    authorization_updated_at: datetime
    beginning_of_week: int = Field(ge=1, le=7)
    country_id: Optional[int] = None
    created_at: datetime
    default_workspace_id: int
    email: EmailStr
    fullname: str
    has_password: bool
    id: int
    image_url: Url
    intercom_hash: Optional[str] = Field(default=None, min_length=64, max_length=64)
    oauth_provides: Optional[list[str]] = None
    openid_email: Optional[EmailStr] = None
    openid_enabled: bool
    options: Optional[list] = None  # not sure, maybe not a list
    timezone: str
    toggl_accounts_id: str = Field(min_length=22, max_length=22)
    updated_at: datetime


class MeResponseWithRelatedData(MeResponse):
    clients: Optional[list]
    projects: Optional[list]
    tags: Optional[list]
    time_entries: Optional[list]
    workspaces: list  # Default workspace is created after signup,
    # check if it is possible not to have workspace at all
