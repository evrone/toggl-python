from datetime import datetime

import pydantic
import pytest

from toggl_python import (
    Activity,
    BaseEntity,
    Client,
    Dashboard,
    Group,
    MostActiveUser,
    Project,
    ProjectUser,
    Tag,
    Task,
    TimeEntry,
    User,
    Workspace,
    WorkspaceUser,
)


def test_base_entity():
    BaseEntity(id=1)
    BaseEntity(id="1")
    BaseEntity(id=1, at=datetime.now())

    with pytest.raises(pydantic.ValidationError):
        BaseEntity(id="foo")


def test_client_entity():
    Client(name="foo", wid=1)
    Client(name="foo", wid=1, notes="some string")

    with pytest.raises(pydantic.ValidationError):
        Client(name="foo")
    with pytest.raises(pydantic.ValidationError):
        Client(wid=1)
    with pytest.raises(pydantic.ValidationError):
        Client(name=1, wid=None)


def test_group_entity():
    Group(name="foo", wid=1)
    Group(name="foo", wid=1, notes="some string")

    with pytest.raises(pydantic.ValidationError):
        Group(name="foo")
    with pytest.raises(pydantic.ValidationError):
        Group(wid=1)
    with pytest.raises(pydantic.ValidationError):
        Group(name=1, wid=None)


def test_project_entity():
    Project(name="foo", wid=1)
    Project(name="foo", wid=1, notes="some string")

    with pytest.raises(pydantic.ValidationError):
        Project(name="foo")
    with pytest.raises(pydantic.ValidationError):
        Project(wid=1)
    with pytest.raises(pydantic.ValidationError):
        Project(name=1, wid=None)


def test_project_user_entity():
    ProjectUser(pid=1, uid=1, wid=1)

    with pytest.raises(pydantic.ValidationError):
        ProjectUser(pid=1, uid=1)
    with pytest.raises(pydantic.ValidationError):
        ProjectUser(pid=1, wid=1)
    with pytest.raises(pydantic.ValidationError):
        ProjectUser(uid=1, wid=1)
    with pytest.raises(pydantic.ValidationError):
        ProjectUser(pid="foo", uid=1, wid=1)


def test_tag_entity():
    Tag(name="foo", wid=1)

    with pytest.raises(pydantic.ValidationError):
        Tag(name="foo")
    with pytest.raises(pydantic.ValidationError):
        Tag(wid=1)


def test_task_entity():
    Task(name="foo", pid=1, wid=1)

    with pytest.raises(pydantic.ValidationError):
        Task(name="foo", pid=1)
    with pytest.raises(pydantic.ValidationError):
        Task(name="foo", wid=1)
    with pytest.raises(pydantic.ValidationError):
        Task(pid=1, wid=1)


def test_time_entry_entity():
    TimeEntry(wid=1, duration=1)

    with pytest.raises(pydantic.ValidationError):
        TimeEntry(wid=1)
    with pytest.raises(pydantic.ValidationError):
        TimeEntry(duration=1)
