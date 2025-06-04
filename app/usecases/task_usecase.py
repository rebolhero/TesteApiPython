from typing import List
from app.domain.task import Task
from app.infra.db.repositories import TaskRepository

class TaskUseCase:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def get_tasks(self) -> List[Task]:
        return self.repository.get_all()

    def get_by_id(self, task_id: int) -> Task:
        return self.repository.get_by_id(task_id)
    
    def create_task(self, task: Task) -> Task:
        return self.repository.create(task)

    def update_task(self, task_id: int, task: Task) -> Task:
        return self.repository.update(task_id, task)

    def delete_task(self, task_id: int) -> None:
        return self.repository.delete(task_id)
