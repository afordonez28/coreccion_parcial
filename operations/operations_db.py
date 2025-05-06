from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from data.models import Pet

async def create_pet(pet: Pet, session: AsyncSession):
    session.add(pet)
    await session.commit()
    await session.refresh(pet)
    return pet

async def get_all_pets(session: AsyncSession):
    result = await session.exec(select(Pet))
    return result.all()
