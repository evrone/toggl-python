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


class BaseRepository(Api):
    LIST_URL = ""
    DETAIL_URL = None
    ENTITY_CLASS = BaseEntity
    ADDITIONAL_METHODS = {}

    def __init__(self, base_url=None, auth=None):
        super().__init__(base_url=base_url, auth=auth)
        if not self.DETAIL_URL:
            self.DETAIL_URL = self.LIST_URL + "/{id}"

    def __getattr__(self, method: str):
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
        id: int,
        url: str,
        additional_id: int = None,
        entity: object = None,
        detail: bool = False,
        params: dict = None,
        data: dict = None,
        files: dict = None,
    ) -> httpx.Response:
        """
        Call additional method with specified url and params
        """

        if detail:
            _url = (self.DETAIL_URL + "/" + url + "/{additional_id}").format(
                id=id, additional_id=additional_id
            )
            return self._retrieve(_url, entity, headers=self.HEADERS)
        else:
            _url = (self.DETAIL_URL + "/" + url).format(id=id)
            return self._list(_url, entity, headers=self.HEADERS)

    def _retrieve(self, _url, entity_class, **kwargs):
        response = self.get(_url)
        return entity_class(**response.json())

    def retrieve(self, id: int = None, **kwargs):
        full_url = self.BASE_URL.join(self.DETAIL_URL.format(id=id))
        return self._retrieve(full_url, self.ENTITY_CLASS)

    def _list(self, _url, entity_class, **kwargs):
        response = self.get(_url)
        return [entity_class(**entity) for entity in response.json()]

    def list(self, **kwargs):
        full_url = self.BASE_URL.join(self.LIST_URL)
        return self._list(full_url, self.ENTITY_CLASS)

    def create(self, entity: ENTITY_CLASS):
        full_url = self.BASE_URL.join(self.LIST_URL)
        response = self.post(full_url, data=entity.dict())
        return self.ENTITY_CLASS(**response.json())

    def update(self, entity: ENTITY_CLASS):
        full_url = self.BASE_URL.join(self.DETAIL_URL.format(id=entity.id))
        response = self.put(full_url, data=entity.dict())
        return self.ENTITY_CLASS(**response.json())

    def partial_update(self, entity: ENTITY_CLASS):
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
    LIST_URL = "users"
    ENTITY_CLASS = User


class Workspaces(BaseRepository):
    LIST_URL = "workspaces"
    ENTITY_CLASS = Workspace
    ADDITIONAL_METHODS = {
        "projects": {"url": "projects", "entity": Project, "detail": False}
    }


class WorkspaceUsers(BaseRepository):
    LIST_URL = "workspace_users"
    ENTITY_CLASS = WorkspaceUser


class Dashboards(BaseRepository):
    LIST_URL = "dashboards"
    ENTITY_CLASS = Dashboard
