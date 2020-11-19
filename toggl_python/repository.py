from functools import partial
from typing import Any, Dict, Optional, Tuple, Type, Union

import httpx

from .api import Api
from .entities import (
    BaseEntity,
    Client,
    Dashboard,
    Group,
    Project,
    ProjectUser,
    ReportTimeEntry,
    Tag,
    Task,
    TimeEntry,
    User,
    Workspace,
    WorkspaceUser,
)
from .exceptions import MethodNotAllowed, NotSupported
from .response import ListResponse, ReportTimeEntriesList
from .auth import BasicAuth, TokenAuth


class BaseRepository(Api):
    LIST_URL = ""
    DETAIL_URL: Optional[str] = None
    ENTITY_CLASS: Type[BaseEntity] = BaseEntity
    ADDITIONAL_METHODS: Dict[str, Dict[str, Any]] = {}
    EXCLUDED_METHODS: Optional[Tuple[str, ...]] = None
    ADDITIONAL_PARAMS: Dict[str, Dict[str, Any]] = {}
    DATA_CONTAINER: Dict[str, Optional[str]] = {}
    LIST_RESPONSE: Optional[Type[ListResponse]] = None

    def __init__(
        self,
        base_url: Optional[str] = None,
        auth: Optional[Union[BasicAuth, TokenAuth]] = None,
    ) -> None:
        super().__init__(base_url=base_url, auth=auth)
        if not self.DETAIL_URL:
            self.DETAIL_URL = self.LIST_URL + "/{id}"

    def __getattr__(self, attr: str) -> Any:
        if self.EXCLUDED_METHODS and attr in self.EXCLUDED_METHODS:
            raise MethodNotAllowed
        try:
            method = super().__getattr__(attr)
        except AttributeError:
            if attr in self.ADDITIONAL_METHODS.keys():
                method = partial(
                    self.additionat_method, **self.ADDITIONAL_METHODS[attr]
                )
            else:
                raise AttributeError(f"No such method ({attr})!")
        return method

    def additionat_method(
        self,
        url: str,
        _id: Optional[int] = None,
        additional_id: Optional[int] = None,
        entity: Any = None,
        detail: bool = False,
        single_item: bool = False,
        data_key: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """
        Call additional method with specified url and params
        """

        if detail:
            if not self.DETAIL_URL:
                raise AttributeError("Not defined DETAIL_URL")
            _url = (self.DETAIL_URL + "/" + url + "/{additional_id}").format(
                id=_id, additional_id=additional_id
            )
            return self._retrieve(
                _url, entity, headers=self.HEADERS, params=params
            )
        elif _id:
            if not self.DETAIL_URL:
                raise AttributeError("Not defined DETAIL_URL")
            _url = (self.DETAIL_URL + "/" + url).format(id=_id)
            return self._list(_url, entity, headers=self.HEADERS, param=params)
        elif single_item:
            _url = str(self.BASE_URL) + "/" + url
            return self._retrieve(
                _url,
                entity,
                headers=self.HEADERS,
                params=params,
                data_key="data",
            )
        else:
            raise NotSupported

    def _retrieve(
        self,
        _url: Union[str, httpx.URL],
        entity_class: Any,
        data_key: Optional[str] = "data",
        **kwargs: Any,
    ) -> Any:
        params = kwargs
        params.update(self.ADDITIONAL_PARAMS.get("retrieve", {}))

        response = self.get(_url, params=params)
        data = response.json()
        data_key = data_key or self.DATA_CONTAINER.get("retrieve", None)
        if data_key:
            data = data[data_key]
        if data:
            return entity_class(**data)

    def retrieve(self, id: Optional[int] = None) -> Any:
        if not self.DETAIL_URL:
            raise AttributeError("Not defined DETAIL_URL")
        full_url = self.BASE_URL.join(self.DETAIL_URL.format(id=id))
        return self._retrieve(full_url, self.ENTITY_CLASS)

    def _list(
        self,
        _url: Union[str, httpx.URL],
        entity_class: Any,
        data_key: Optional[str] = None,
        **kwargs: Any,
    ) -> Any:
        params = kwargs
        params.update(self.ADDITIONAL_PARAMS.get("list", {}))

        response = self.get(_url, params=params)
        response_body = response.json()

        data = response_body
        data_key = data_key or self.DATA_CONTAINER.get("list", None)
        if data_key:
            data = data[data_key]
        if data:
            value = [entity_class(**entity) for entity in data]
            if self.LIST_RESPONSE:
                value = self.LIST_RESPONSE(value, response_body)
            return value

    def list(self, **kwargs: Any) -> Any:
        if self.EXCLUDED_METHODS and "list" in self.EXCLUDED_METHODS:
            raise MethodNotAllowed
        full_url = self.BASE_URL.join(self.LIST_URL)
        return self._list(full_url, self.ENTITY_CLASS, **kwargs)

    def create(self, entity: Any, **kwargs: Any) -> Any:
        if self.EXCLUDED_METHODS and "create" in self.EXCLUDED_METHODS:
            raise MethodNotAllowed
        full_url = self.BASE_URL.join(self.LIST_URL)
        response = self.post(full_url, data=entity.dict(), **kwargs)
        return self.ENTITY_CLASS(**response.json())

    def update(self, entity: Any, **kwargs: Any) -> Any:
        if self.EXCLUDED_METHODS and "update" in self.EXCLUDED_METHODS:
            raise MethodNotAllowed
        if not self.DETAIL_URL:
            raise AttributeError("Not defined DETAIL_URL")
        full_url = self.BASE_URL.join(self.DETAIL_URL.format(id=entity.id))
        response = self.put(full_url, data=entity.dict(), **kwargs)
        return self.ENTITY_CLASS(**response.json())

    def partial_update(self, entity: Any, **kwargs: Any) -> Any:
        if self.EXCLUDED_METHODS and "partial_update" in self.EXCLUDED_METHODS:
            raise MethodNotAllowed
        if not self.DETAIL_URL:
            raise AttributeError("Not defined DETAIL_URL")
        full_url = self.BASE_URL.join(self.DETAIL_URL.format(id=entity.id))
        response = self.patch(full_url, data=entity.dict(), **kwargs)
        return self.ENTITY_CLASS(**response.json())


class Clients(BaseRepository):
    LIST_URL = "clients"
    ENTITY_CLASS = Client


class Groups(BaseRepository):
    LIST_URL = "groups"
    ENTITY_CLASS = Group


class Projects(BaseRepository):
    LIST_URL = "projects"
    ENTITY_CLASS = Project


class ProjectUsers(BaseRepository):
    LIST_URL = "project_users"
    ENTITY_CLASS = ProjectUser


class Tags(BaseRepository):
    LIST_URL = "tags"
    ENTITY_CLASS = Tag


class Tasks(BaseRepository):
    LIST_URL = "tasks"
    ENTITY_CLASS = Task


class TimeEntries(BaseRepository):
    LIST_URL = "time_entries"
    ENTITY_CLASS = TimeEntry


class ReportTimeEntries(BaseRepository):
    BASE_URL: httpx.URL = httpx.URL("https://toggl.com/reports/api/v2/")
    ADDITIONAL_PARAMS = {"list": {"user_agent": "toggl_python"}}
    DATA_CONTAINER = {"list": "data"}
    LIST_URL = "details"
    ENTITY_CLASS = ReportTimeEntry
    LIST_RESPONSE = ReportTimeEntriesList


class Users(BaseRepository):
    EXCLUDED_METHODS = ("list", "create", "update", "partial_update")
    LIST_URL = "users"
    ENTITY_CLASS = User
    ADDITIONAL_METHODS = {
        "me": {"url": "me", "entity": User, "single_item": True},
    }


class Workspaces(BaseRepository):
    LIST_URL = "workspaces"
    ENTITY_CLASS = Workspace
    ADDITIONAL_METHODS = {
        "projects": {"url": "projects", "entity": Project, "detail": False},
        "users": {"url": "users", "entity": User, "detail": False},
        "clients": {"url": "clients", "entity": Client, "detail": False},
        "groups": {"url": "groups", "entity": Group, "detail": False},
        "tasks": {"url": "tasks", "entity": Task, "detail": False},
        "tags": {"url": "tags", "entity": Tag, "detail": False},
        "workspace_users": {
            "url": "workspace_users",
            "entity": WorkspaceUser,
            "detail": False,
        },
    }


class WorkspaceUsers(BaseRepository):
    LIST_URL = "workspace_users"
    ENTITY_CLASS = WorkspaceUser


class Dashboards(BaseRepository):
    LIST_URL = "dashboards"
    ENTITY_CLASS = Dashboard
