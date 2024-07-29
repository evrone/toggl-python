from __future__ import annotations

from typing import Dict, Final, List, Union


FLAT_RESPONSE_TYPE = Dict[str, Union[str, int, bool, None]]
NESTED_RESPONSE_TYPE = Dict[str, Union[str, int, bool, List, None]]

FAKE_TOKEN: str = "flstsapa42cdwiueii2tjg2t08f91kdr"

ME_RESPONSE_SHORT: Final[FLAT_RESPONSE_TYPE] = {
    "at": "2024-07-24T09:42:55.391879Z",
    "authorization_updated_at": "2024-07-02T16:13:32.109174Z",
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
    "timezone": "Europe/London",
    "toggl_accounts_id": "uWGsHAeXZGhJvQ3XjdY63h",
    "updated_at": "2024-05-16T12:01:24.447981Z",
}

ME_RESPONSE: NESTED_RESPONSE_TYPE = {
    "api_token": FAKE_TOKEN,
    "at": "2024-07-24T09:42:55.391879Z",
    "authorization_updated_at": "2024-07-02T16:13:32.109174Z",
    "beginning_of_week": 1,
    "country_id": None,
    "created_at": "2024-05-16T12:01:04.834085Z",
    "default_workspace_id": 43644207,
    "email": "example@mail.com",
    "fullname": "Test User",
    "has_password": True,
    "id": 30809356,
    "image_url": "https://assets.track.toggl.com/images/profile.png",
    "intercom_hash": "78hcsq59lsca33ivsd5iwy42yu3gdf0sctutuku5gvjfk1qbj71puu7r1z74dzdp",
    "openid_email": None,
    "openid_enabled": False,
    "timezone": "Europe/London",
    "toggl_accounts_id": "uWGsHAeXZGhJvQ3XjdY63h",
    "updated_at": "2024-05-16T12:01:24.447981Z",
}

ME_RESPONSE_WITH_RELATED_DATA: NESTED_RESPONSE_TYPE = {
    "api_token": FAKE_TOKEN,
    "at": "2024-07-24T09:42:55.391879Z",
    "authorization_updated_at": "2024-07-02T16:13:32.109174Z",
    "beginning_of_week": 1,
    "country_id": None,
    "created_at": "2024-05-16T12:01:04.834085Z",
    "default_workspace_id": 43644207,
    "email": "example@mail.com",
    "fullname": "Test User",
    "has_password": True,
    "id": 30809356,
    "image_url": "https://assets.track.toggl.com/images/profile.png",
    "intercom_hash": "78hcsq59lsca33ivsd5iwy42yu3gdf0sctutuku5gvjfk1qbj71puu7r1z74dzdp",
    "openid_email": None,
    "openid_enabled": False,
    "timezone": "Europe/London",
    "toggl_accounts_id": "uWGsHAeXZGhJvQ3XjdY63h",
    "updated_at": "2024-05-16T12:01:24.447981Z",
    "clients": [],
    "projects": [],
    "time_entries": [],
    "tags": [],
    "workspaces": [],
}
