from datetime import datetime
from typing import Callable, List, Optional, Union

from pydantic import BaseModel, EmailStr, HttpUrl


class BaseEntity(BaseModel):
    id: Optional[int] = None
    at: Optional[datetime] = None


class Client(BaseEntity):
    name: str
    wid: int
    notes: Optional[str] = None


class Group(BaseEntity):
    name: str
    wid: int


class Project(BaseEntity):
    name: str
    wid: int
    cid: Optional[int] = None
    active: bool = True
    is_private: bool = True
    template: Optional[bool] = None
    template_id: Optional[int] = None
    billable: bool = True
    auto_estimates: Optional[bool] = False
    estimated_hours: Optional[int] = None
    color: Union[str, int] = None
    rate: Optional[float] = None
    created_at: Optional[datetime] = None


class ProjectUser(BaseEntity):
    pid: int
    uid: int
    wid: int
    notes: Optional[str] = None
    manage: Optional[bool] = False
    rate: Optional[float] = None
    full_name: Optional[float] = None


class Tag(BaseEntity):
    name: str
    wid: int


class Task(BaseEntity):
    name: str
    pid: int
    wid: int
    uid: Optional[int] = None
    estimated_seconds: Optional[int] = None
    active: Optional[bool] = True


class TimeEntry(BaseEntity):
    wid: int
    pid: Optional[int] = None
    tid: Optional[int] = None
    description: Optional[str] = None
    billable: Optional[bool] = False
    start: Union[datetime, Callable] = datetime.now
    stop: Union[datetime, Callable] = None
    duration: int
    created_with: Optional[str]
    tags: List[str] = []
    duronly: Optional[bool] = None


class User(BaseEntity):
    api_token: Optional[str] = None
    default_wid: Optional[int] = None
    email: EmailStr
    fullname: str
    jquery_timeofday_format: str
    jquery_date_format: str
    timeofday_format: str
    date_format: str
    store_start_and_stop_time: bool
    beginning_of_week: int = 0
    language: str
    image_url: HttpUrl
    sidebar_piechart: bool
    new_blog_post: dict
    send_product_emails: bool
    send_weekly_report: bool
    send_timer_notifications: bool
    openid_enabled: bool
    timezone: str


class Workspace(BaseEntity):
    name: str
    premium: bool
    admin: bool
    default_hourly_rate: float
    default_currency: str
    only_admins_may_create_projects: bool
    only_admins_see_billable_rates: bool
    rounding: int
    rounding_minutes: int
    logo_url: Optional[HttpUrl] = None


class WorkspaceUser(BaseEntity):
    uid: int
    wid: int
    admin: bool
    active: bool
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    invite_url: Optional[HttpUrl] = None


class Activity(BaseEntity):
    user_id: int
    project_id: int
    duration: int
    description: str
    stop: datetime
    tid: int


class MostActiveUser(BaseEntity):
    user_id: int
    duration: int


class Dashboard(BaseEntity):
    most_active_user: List[MostActiveUser] = []
    activity: List[Activity]
