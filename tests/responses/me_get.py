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

ME_FEATURES_RESPONSE: List[Dict[str, Union[int, List[Dict]]]] = [
    {
        "features": [
            {"enabled": True, "feature_id": 0, "name": "free"},
            {"enabled": False, "feature_id": 13, "name": "pro"},
            {"enabled": False, "feature_id": 15, "name": "business"},
            {"enabled": False, "feature_id": 55, "name": "tracking_reminders"},
            {"enabled": False, "feature_id": 64, "name": "tasks"},
            {"enabled": False, "feature_id": 65, "name": "project_dashboard"},
        ],
        "workspace_id": 43644207,
    }
]

ME_PREFERENCES_RESPONSE: Dict[str, Union[int, str, List[Dict]]] = {
    "BeginningOfWeek": 1,
    "alpha_features": [
        {"code": "paging_project_list", "enabled": False},
        {"code": "jira_v2", "enabled": False},
        {"code": "alerts_v2", "enabled": True},
        {"code": "analytics", "enabled": True},
    ],
    "date_format": "MM/DD/YYYY",
    "duration_format": "improved",
    "pg_time_zone_name": "Europe/Moscow",
    "record_timeline": False,
    "send_product_emails": False,
    "send_timer_notifications": True,
    "send_weekly_report": False,
    "timeofday_format": "H:mm",
}
