from fastapi import FastAPI, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from enum import Enum
from data.models import User, Task, TaskState
from operations.operations_db import create_task, create_user, get_all_tasks, get_task_by_id, update_task_state, set_user_premium, get_active_users, get_active_and_premium_users
from utils.conection_db import get_session

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Metodo POST para adicionar un usuario
@app.post("/users/")
async def add_user(user: User, session: AsyncSession = Depends(get_session)):
    return await create_user(user, session)

# Metodo POST para adicionar una tarea
@app.post("/tasks/")
async def add_task(task: Task, session: AsyncSession = Depends(get_session)):
    return await create_task(task, session)

# Metodo GET para consultar todas las tareas
@app.get("/tasks/")
async def list_tasks(session: AsyncSession = Depends(get_session)):
    return await get_all_tasks(session)

# Metodo GET para consultar una tarea por ID
@app.get("/tasks/{task_id}")
async def get_task(task_id: int, session: AsyncSession = Depends(get_session)):
    task = await get_task_by_id(task_id, session)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# Metodo PATCH para actualizar el estado de la tarea
@app.patch("/tasks/{task_id}/state/")
async def update_task(task_id: int, state: TaskState, session: AsyncSession = Depends(get_session)):
    task = await update_task_state(task_id, state, session)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# Metodo PATCH para hacer un usuario premium
@app.patch("/users/{user_id}/premium/")
async def make_user_premium(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await set_user_premium(user_id, session)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Metodo GET para consultar usuarios activos (no premium)
@app.get("/users/active/")
async def get_active_users_list(session: AsyncSession = Depends(get_session)):
    return await get_active_users(session)

# Metodo GET para consultar usuarios activos y premium
@app.get("/users/active_and_premium/")
async def get_active_and_premium_users_list(session: AsyncSession = Depends(get_session)):
    return await get_active_and_premium_users(session)
