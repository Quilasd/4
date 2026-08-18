from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Character


async def get_character(session: AsyncSession, user_id: int, world_id: int) -> Character | None:
    result = await session.execute(
        select(Character).where(Character.user_id == user_id, Character.world_id == world_id)
    )
    return result.scalar_one_or_none()


async def create_character(
    session: AsyncSession,
    user_id: int,
    world_id: int,
    name: str,
    race: str | None = None,
    gender: str | None = None,
) -> Character:
    character = Character(
        user_id=user_id,
        world_id=world_id,
        name=name,
        race=race,
        gender=gender,
    )
    session.add(character)
    await session.commit()
    await session.refresh(character)
    return character
