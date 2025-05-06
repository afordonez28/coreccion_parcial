from sqlmodel import select, Session
from sqlalchemy.future import select
from data.models import Task, User, TaskState


async def create_task(task: Task, session: Session):
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def create_user(user: User, session: Session):
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_all_tasks(session: Session):
    result = await session.execute(select(Task))
    return result.scalars().all()


async def get_task_by_id(task_id: int, session: Session):
    result = await session.execute(select(Task).where(Task.id == task_id))
    return result.scalar_one_or_none()


async def update_task_state(task_id: int, state: TaskState, session: Session):
    task = await get_task_by_id(task_id, session)
    if task:
        task.state = state
        await session.commit()
        await session.refresh(task)
    return task


async def set_user_premium(user_id: int, session: Session):
    user = await session.get(User, user_id)
    if user:
        user.is_premium = True
        await session.commit()
        await session.refresh(user)
    return user


async def get_active_users(session: Session):
    result = await session.execute(select(User).where(User.is_premium == False))
    return result.scalars().all()


async def get_active_and_premium_users(session: Session):
    result = await session.execute(select(User).where(User.is_premium == True))
    return result.scalars().all()
