from fastapi import APIRouter, HTTPException
from typing import List
from app.domain.task import Task
from app.usecases.task_usecase import TaskUseCase
from app.infra.db.repositories import TaskRepository

router = APIRouter()
usecase = TaskUseCase(TaskRepository())

@router.get("/tasks", response_model=List[Task], summary="Listar todas as tarefas", description="Retorna uma lista de todas as tarefas cadastradas no sistema.")
def get_tasks():
    return usecase.get_tasks()

@router.get("/tasks/{task_id}", summary="Buscar tarefa por ID", description="Retorna os dados de uma tarefa atraves do seu ID")
def get_by_id(task_id: int):
    get_id = usecase.get_by_id(task_id)
    if not get_id:
        raise HTTPException(status_code=404, detail="Erro ao buscar: Tarefa nao encontrada")
    return get_id

@router.post("/tasks", response_model=Task, summary="Criar tarefa", description="Criacao de uma nova tarefa")
def create_task(task: Task):
    return usecase.create_task(task)

@router.put("/tasks/{task_id}", response_model=Task, summary="Alterar tarefa pelo ID", description="Altera os dados da tarefa pelo ID fornecido")
def update_task(task_id: int, task: Task):
    updated_task = usecase.update_task(task_id, task)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Erro ao atualizar: Tarefa nao encontrada")
    return updated_task

@router.delete("/tasks/{task_id}", summary="Excluir tarefa", description="Exclui a tarefa pelo ID")
def delete_task(task_id: int):
    deleted_task = usecase.delete_task(task_id)
    if not deleted_task:
        raise HTTPException(status_code=404, detail="Erro ao excluir: Tarefa nao encontrada")
    return {"message": "Tarefa excluida com sucesso"}

