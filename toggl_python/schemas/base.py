from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional

from pydantic import AwareDatetime, BaseModel, field_serializer, field_validator


class BaseSchema(BaseModel):
    pass


class SinceParamSchemaMixin(BaseSchema):
    since: Optional[AwareDatetime]

    @field_validator("since")
    @classmethod
    def check_if_since_is_too_old(cls, value: Optional[datetime]) -> Optional[datetime]:
        if not value:
            return value

        now = datetime.now(tz=timezone.utc)
        three_months = timedelta(days=90)
        utc_value = value.astimezone(tz=timezone.utc)

        if now - three_months > utc_value:
            error_message = "Since cannot be older than 3 months"
            raise ValueError(error_message)

        return value

    @field_serializer("since", when_used="json")
    def serialize_since(self, value: Optional[datetime]) -> Optional[int]:
        if not value:
            return value

        return int(value.timestamp())
