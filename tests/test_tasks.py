from datetime import datetime, timezone
from sqlalchemy.orm import Session
import pytest

from src.classes.task import Task
from src.controllers.tasks import TaskCtrl
from src.enums import TaskStatus


def test_task_creation(db_session: Session):
    """Black-box test for task creation."""
    task = TaskCtrl.create(
        db=db_session,
        title="Test Task",
        description="A test task",
        due_date=datetime.now(timezone.utc),
        status=TaskStatus.PENDING,
    )
    assert task.task_id
    assert task.title == "Test Task"
    assert task.status == TaskStatus.PENDING
    assert not task.deleted


def test_task_creation_no_title(db_session: Session):
    """Boundary test for task creation with no title."""
    with pytest.raises(ValueError):
        TaskCtrl.create(
            db=db_session,
            title="",
            description="A test task",
            due_date=datetime.now(timezone.utc),
            status=TaskStatus.PENDING,
        )


def test_task_soft_delete(db_session: Session):
    """White-box test for task soft delete."""
    task = TaskCtrl.create(
        db=db_session,
        title="Delete Me",
        description="This task will be deleted.",
        due_date=datetime.now(timezone.utc),
        status=TaskStatus.CREATED,
    )
    TaskCtrl.safe_delete(task, db_session)
    deleted_task = TaskCtrl.load(task.task_id, db_session)
    assert deleted_task is None

    deleted_task_in_db = db_session.query(Task).filter(Task.task_id == task.task_id).first()
    assert deleted_task_in_db
    assert deleted_task_in_db.deleted
