from typing import Optional
from sqlmodel import SQLModel, Field
from enum import Enum


class TaskState(str, Enum):
    pendiente = "pendiente"
    en_progreso = "en_progreso"
    completada = "completada"


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    is_premium: bool = False


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    state: TaskState = Field(default=TaskState.pendiente)
    user_id: int = Field(foreign_key="user.id")  # Relación con el modelo de usuario
