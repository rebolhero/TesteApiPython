from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.task import Task
from app.domain.taskupdate import TaskUpdate
from app.infra.db.models import TaskModel
from app.infra.db.database import SessionLocal

class TaskRepository:
    def __init__(self, db_session: Session = None):
        self.db = db_session or SessionLocal()

    def _to_domain(self, task_model: TaskModel) -> Task:
        return Task(
            id=task_model.id,
            title=task_model.title,
            description=task_model.description,
            is_completed=task_model.is_completed
        )

    def get_all(self) -> List[Task]:
        db_tasks = self.db.query(TaskModel).all()
        return [self._to_domain(task) for task in db_tasks]

    def get_by_id(self, task_id: int) -> Optional[Task]:
        task_model = self.db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if task_model:
            return self._to_domain(task_model)
        return None

    def create(self, task: Task) -> Task:
        db_task = TaskModel(
            title=task.title,
            description=task.description,
            is_completed=task.is_completed
        )
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return self._to_domain(db_task)

    def update(self, task_id: int, task_update: TaskUpdate) -> Optional[Task]:
        db_task = self.db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if not db_task:
            return None

        if task_update.title is not None and task_update.title != '':
            db_task.title = task_update.title
        if task_update.description is not None and task_update.description != '':
            db_task.description = task_update.description
        if task_update.is_completed is not None:
            db_task.is_completed = task_update.is_completed

        self.db.commit()
        self.db.refresh(db_task)
        return self._to_domain(db_task)

    def delete(self, task_id: int) -> bool:
        db_task = self.db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if not db_task:
            return False

        self.db.delete(db_task)
        self.db.commit()
        return True
