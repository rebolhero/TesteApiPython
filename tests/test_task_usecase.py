import pytest
from app.domain.task import Task
from app.domain.taskupdate import TaskUpdate
from app.usecases.task_usecase import TaskUseCase

class FakeRepository:
    def __init__(self):
        self.tasks = []

    def get_all(self):
        return self.tasks

    def get_by_id(self, task_id):
        self.tasks = [t for t in self.tasks if t.id != task_id]

    def create(self, task):
        task.id = len(self.tasks) + 1
        self.tasks.append(task)
        return task

    def update(self, task_id, task_update: TaskUpdate):
        for idx, t in enumerate(self.tasks):
            if t.id == task_id:
                if task_update.title is not None and task_update.title != '':
                    t.title = task_update.title
                if task_update.description is not None and task_update.description != '':
                    t.description = task_update.description
                if task_update.is_completed is not None:
                    t.is_completed = task_update.is_completed
                return t
        return None

    def delete(self, task_id):
        self.tasks = [t for t in self.tasks if t.id != task_id]

@pytest.fixture
def usecase():
    repo = FakeRepository()
    return TaskUseCase(repo)

def test_create_task(usecase):
    task = Task(title="Test", description="Test desc", id=0, is_completed=False)
    created = usecase.create_task(task)
    assert created.id == 1
    assert created.title == "Test"

def test_get_tasks(usecase):
    task = Task(title="Test", description="Test desc", id=0, is_completed=False)
    usecase.create_task(task)
    tasks = usecase.get_tasks()
    assert len(tasks) == 1


def test_get_by_id(usecase):
    task = Task(title="Test", description="Test desc", id=0, is_completed=False)
    created = usecase.create_task(task)
    usecase.get_by_id(created.id)
    assert len(usecase.get_tasks()) == 0

def test_update_task(usecase):
    task = Task(title="Test", description="Test desc", id=0, is_completed=False)
    created = usecase.create_task(task)
    
    update_data = TaskUpdate(title="Updated")
    updated = usecase.update_task(created.id, update_data)
    
    assert updated.title == "Updated"
    assert updated.description == "Test desc"

def test_delete_task(usecase):
    task = Task(title="Test", description="Test desc", id=0, is_completed=False)
    created = usecase.create_task(task)
    usecase.delete_task(created.id)
    assert len(usecase.get_tasks()) == 0

def test_update_task_no_changes(usecase):
    task = Task(title="Test", description="Test desc", id=0, is_completed=False)
    created = usecase.create_task(task)
    
    update_data = TaskUpdate()  # Nenhum campo alterado
    updated = usecase.update_task(created.id, update_data)
    
    assert updated.title == "Test"
    assert updated.description == "Test desc"
    assert updated.is_completed is False

def test_update_task_empty_strings(usecase):
    task = Task(title="Test", description="Test desc", id=0, is_completed=False)
    created = usecase.create_task(task)
    
    update_data = TaskUpdate(title="", description="")
    updated = usecase.update_task(created.id, update_data)
    
    assert updated.title == "Test"  # Não alterou
    assert updated.description == "Test desc"

def test_update_task_all_fields(usecase):
    task = Task(title="Test", description="Test desc", id=0, is_completed=False)
    created = usecase.create_task(task)
    
    update_data = TaskUpdate(title="Updated", description="New Desc", is_completed=True)
    updated = usecase.update_task(created.id, update_data)
    
    assert updated.title == "Updated"
    assert updated.description == "New Desc"
    assert updated.is_completed is True

def test_update_nonexistent_task(usecase):
    update_data = TaskUpdate(title="Doesn't matter")
    updated = usecase.update_task(999, update_data)  # ID inexistente
    assert updated is None

def test_delete_nonexistent_task(usecase):
    # Não deve lançar exceção, apenas não fazer nada
    usecase.delete_task(999)
    assert len(usecase.get_tasks()) == 0

def test_create_multiple_tasks(usecase):
    t1 = Task(title="T1", description="D1", id=0, is_completed=False)
    t2 = Task(title="T2", description="D2", id=0, is_completed=False)
    
    created1 = usecase.create_task(t1)
    created2 = usecase.create_task(t2)
    
    assert created1.id == 1
    assert created2.id == 2
    tasks = usecase.get_tasks()
    assert len(tasks) == 2

