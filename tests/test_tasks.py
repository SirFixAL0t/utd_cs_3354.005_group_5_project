from datetime import datetime, timezone
from sqlalchemy.orm import Session
import pytest
from hypothesis import given, strategies as st, settings, HealthCheck

from src.classes.task import Task
from src.controllers.tasks import TaskCtrl
from src.enums import TaskStatus
from src.constants import CALENDAR_TITLE


aware_datetimes = st.datetimes(min_value=datetime(2000, 1, 1), max_value=datetime(2030, 1, 1)).map(
    lambda dt: dt.replace(tzinfo=timezone.utc)
)

task_strategy = st.builds(
    Task,
    title=st.text(min_size=CALENDAR_TITLE[0], max_size=CALENDAR_TITLE[1]),
    description=st.text(max_size=255),
    due_date=aware_datetimes,
    status=st.sampled_from(TaskStatus),
)

@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(task_data=task_strategy)
def test_task_creation_and_retrieval_property(db_session: Session, task_data: Task):
    """Property-based test for task creation and retrieval."""
    try:
        created_task = TaskCtrl.create(
            db=db_session,
            title=task_data.title,
            description=task_data.description,
            due_date=task_data.due_date,
            status=TaskStatus(task_data.status),
        )
    except Exception:
        db_session.rollback()
        return

    loaded_task = TaskCtrl.load(created_task.task_id, db_session)

    assert loaded_task is not None
    assert loaded_task.title == created_task.title
    assert loaded_task.status == created_task.status


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


def test_task_creation_long_title(db_session: Session):
    """Boundary test for task creation with a title that is too long."""
    long_title = "a" * (CALENDAR_TITLE[1] + 1)
    with pytest.raises(ValueError):
        TaskCtrl.create(
            db=db_session,
            title=long_title,
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
