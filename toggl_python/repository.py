from functools import partial

import httpx

from .api import Api
from .entities import (
    BaseEntity,
    Client,
    Dashboard,
    Group,
    Project,
    ProjectUser,
    Tag,
    Task,
    TimeEntry,
    User,
    Workspace,
    WorkspaceUser,
)
from .exceptions import MethodNotAllowed, NotSupported


class BaseRepository(Api):
    LIST_URL = ""
    DETAIL_URL = None
    ENTITY_CLASS = BaseEntity
    ADDITIONAL_METHODS = {}
    EXCLUDED_METHODS = ()

    def __init__(self, base_url=None, auth=None):
        super().__init__(base_url=base_url, auth=auth)
        if not self.DETAIL_URL:
            self.DETAIL_URL = self.LIST_URL + "/{id}"

    def __getattr__(self, method: str):
        if method in self.EXCLUDED_METHODS:
            raise MethodNotAllowed
        try:
            method = super().__getattr__(method)
        except AttributeError:
            if method in self.ADDITIONAL_METHODS.keys():
                method = partial(
                    self.additionat_method, **self.ADDITIONAL_METHODS[method]
                )
            else:
                raise AttributeError(f"No such method ({method})!")
        return method

    def additionat_method(
        self,
        url: str,
        _id: int = None,
        additional_id: int = None,
        entity: object = None,
        detail: bool = False,
        single_item: bool = False,
        data_key: str = None,
        params: dict = None,
        data: dict = None,
        files: dict = None,
    ) -> httpx.Response:
        """
        Call additional method with specified url and params
        """

        if detail:
            _url = (self.DETAIL_URL + "/" + url + "/{additional_id}").format(
                id=_id, additional_id=additional_id
            )
            return self._retrieve(_url, entity, headers=self.HEADERS)
        elif _id:
            _url = (self.DETAIL_URL + "/" + url).format(id=_id)
            return self._list(_url, entity, headers=self.HEADERS)
        elif single_item:
            _url = str(self.BASE_URL) + "/" + url
            return self._retrieve(
                _url, entity, headers=self.HEADERS, data_key="data"
            )
        else:
            raise NotSupported

    def _retrieve(self, _url, entity_class, data_key: str = None, **kwargs):
        response = self.get(_url)
        data = response.json()
        if data_key:
            data = data[data_key]
            return entity_class(**data)
        else:
            return entity_class(**data)

    def retrieve(self, id: int = None, **kwargs):
        full_url = self.BASE_URL.join(self.DETAIL_URL.format(id=id))
        return self._retrieve(full_url, self.ENTITY_CLASS)

    def _list(self, _url, entity_class, **kwargs):
        response = self.get(_url)
        return [entity_class(**entity) for entity in response.json()]

    def list(self, **kwargs):
        if "list" in self.EXCLUDED_METHODS:
            raise MethodNotAllowed
        full_url = self.BASE_URL.join(self.LIST_URL)
        return self._list(full_url, self.ENTITY_CLASS)

    def create(self, entity: ENTITY_CLASS):
        if "create" in self.EXCLUDED_METHODS:
            raise MethodNotAllowed
        full_url = self.BASE_URL.join(self.LIST_URL)
        response = self.post(full_url, data=entity.dict())
        return self.ENTITY_CLASS(**response.json())

    def update(self, entity: ENTITY_CLASS):
        if "update" in self.EXCLUDED_METHODS:
            raise MethodNotAllowed
        full_url = self.BASE_URL.join(self.DETAIL_URL.format(id=entity.id))
        response = self.put(full_url, data=entity.dict())
        return self.ENTITY_CLASS(**response.json())

    def partial_update(self, entity: ENTITY_CLASS):
        if "partial_update" in self.EXCLUDED_METHODS:
            raise MethodNotAllowed
        full_url = self.BASE_URL.join(self.DETAIL_URL.format(id=entity.id))
        response = self.patch(full_url, data=entity.dict())
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
