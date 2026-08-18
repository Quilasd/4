from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Character, User, World, WorldMember


async def get_or_create_user(session: AsyncSession, telegram_id: int, username: str | None) -> User:
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()
    if user is None:
        user = User(telegram_id=telegram_id, username=username)
        session.add(user)
        await session.flush()
    elif user.username != username:
        user.username = username
    return user


async def get_active_worlds(session: AsyncSession) -> list[World]:
    result = await session.execute(select(World).where(World.status == "active").order_by(World.id))
    return list(result.scalars().all())


async def join_world(session: AsyncSession, user: User, world: World) -> None:
    result = await session.execute(
        select(WorldMember).where(WorldMember.world_id == world.id, WorldMember.user_id == user.id)
    )
    if result.scalar_one_or_none() is None:
        session.add(WorldMember(world_id=world.id, user_id=user.id, role="player"))
        await session.flush()


async def create_character(
    session: AsyncSession,
    user: User,
    world: World,
    name: str,
    gender: str,
    race: str,
) -> Character:
    await join_world(session, user, world)
    character = Character(
        world_id=world.id,
        user_id=user.id,
        name=name,
        gender=gender,
        race=race,
        age=18,
        level=1,
        experience=0,
        status="alive",
    )
    session.add(character)
    await session.commit()
    return character
