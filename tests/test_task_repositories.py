import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.infra.db.models import Base, TaskModel
from app.domain.task import Task
from app.domain.taskupdate import TaskUpdate
from app.infra.db.repositories import TaskRepository

# Configuração de banco SQLite em memória
@pytest.fixture
def db_session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    yield db
    db.close()

@pytest.fixture
def repo(db_session):
    return TaskRepository(db_session)

def test_create_task(repo):
    task = Task(id=0, title="Test", description="Desc", is_completed=False)
    created = repo.create(task)
    assert created.id == 1
    assert created.title == "Test"

def test_get_all_tasks(repo):
    task = Task(id=0, title="Test", description="Desc", is_completed=False)
    repo.create(task)
    tasks = repo.get_all()
    assert len(tasks) == 1
    assert tasks[0].title == "Test"

def test_get_by_id(repo):
    task = Task(id=0, title="Test", description="Desc", is_completed=False)
    created = repo.create(task)
    found = repo.get_by_id(created.id)
    assert found is not None
    assert found.id == created.id

def test_update_task_partial(repo):
    task = Task(id=0, title="Test", description="Desc", is_completed=False)
    created = repo.create(task)
    
    update_data = TaskUpdate(title="Updated")
    updated = repo.update(created.id, update_data)
    
    assert updated.title == "Updated"
    assert updated.description == "Desc"  # Não alterado

def test_update_task_all_fields(repo):
    task = Task(id=0, title="Test", description="Desc", is_completed=False)
    created = repo.create(task)
    
    update_data = TaskUpdate(title="Updated", description="New Desc", is_completed=True)
    updated = repo.update(created.id, update_data)
    
    assert updated.title == "Updated"
    assert updated.description == "New Desc"
    assert updated.is_completed is True

def test_update_nonexistent_task(repo):
    update_data = TaskUpdate(title="Nope")
    result = repo.update(999, update_data)
    assert result is None

def test_delete_task(repo):
    task = Task(id=0, title="Test", description="Desc", is_completed=False)
    created = repo.create(task)
    deleted = repo.delete(created.id)
    assert deleted is True
    assert repo.get_by_id(created.id) is None

def test_delete_nonexistent_task(repo):
    result = repo.delete(999)
    assert result is False
