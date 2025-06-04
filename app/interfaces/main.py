from fastapi import FastAPI
from app.interfaces.api.task_controller import router
from app.infra.db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de uma lista de tarefas em python",
    description="Esta API gerencia tarefas com funcionalidades de CRUD"
    )

app.include_router(router)
