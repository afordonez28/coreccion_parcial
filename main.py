from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from utils.conection_db import init_db, get_session
from data.models import Pet
from operations.operations_db import create_pet, get_all_pets

#pip install fastapi uvicorn sqlmodel asyncpg python-dotenv
#univorn main:app --reload

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/pets/")
async def add_pet(pet: Pet, session: AsyncSession = Depends(get_session)):
    return await create_pet(pet, session)

@app.get("/pets/")
async def list_pets(session: AsyncSession = Depends(get_session)):
    return await get_all_pets(session)
