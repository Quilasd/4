from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Character


async def get_character(session: AsyncSession, telegram_id: int, world_id: int | None = None) -> Character | None:
    query = select(Character).join(Character.__table__.metadata.tables["users"]).where(
        Character.__table__.metadata.tables["users"].c.telegram_id == telegram_id
    ).order_by(Character.id.desc())
    if world_id is not None:
        query = query.where(Character.world_id == world_id)
    result = await session.execute(query)
    return result.scalars().first()
