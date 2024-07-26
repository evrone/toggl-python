from typing import Dict, List, Union

from tests.responses.me_get import FAKE_TOKEN


NESTED_RESPONSE_TYPE = Dict[str, Union[str, int, bool, List, None]]

UPDATE_ME_RESPONSE: NESTED_RESPONSE_TYPE = {
    "api_token": FAKE_TOKEN,
    "at": "2024-07-24T09:42:55.391879Z",
    "beginning_of_week": 1,
    "country_id": None,
    "created_at": "2024-05-16T12:01:04.834085Z",
    "default_workspace_id": 43644207,
    "email": "example@mail.com",
    "fullname": "Test User",
    "has_password": True,
    "id": 30809356,
    "image_url": "https://assets.track.toggl.com/images/profile.png",
    "openid_email": None,
    "openid_enabled": False,
    "options": [],
    "timezone": "Europe/London",
    "toggl_accounts_id": "uWGsHAeXZGhJvQ3XjdY63h",
    "toggl_accounts_updated_at": "2024-05-16T12:01:24.447981Z",
    "updated_at": "2024-05-16T12:01:24.447981Z",
}
