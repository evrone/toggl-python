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
    DETAIL_URL = LIST_URL + "/{id}"
    ENTITY_CLASS = BaseEntity

    def retrieve(self, id: int = None, **kwargs):
        full_url = self.BASE_URL.join(self.DETAIL_URL.format(id=id))
        response = self.get(full_url)
        return self.ENTITY_CLASS(**response.json())

    def list(self, **kwargs):
        full_url = self.BASE_URL.join(self.LIST_URL)
        response = self.get(full_url)
        return [self.ENTITY_CLASS(**entity) for entity in response.json()]

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


class WorkspaceUsers(BaseRepository):
    LIST_URL = "workspace_users"
    ENTITY_CLASS = WorkspaceUser


class Dashboards(BaseRepository):
    LIST_URL = "dashboards"
    ENTITY_CLASS = Dashboard
