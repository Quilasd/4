from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import User


async def get_or_create_user(session: AsyncSession, telegram_id: int, username: str | None) -> tuple[User, bool]:
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()
    if user:
        if user.username != username:
            user.username = username
            await session.commit()
        return user, False

    user = User(telegram_id=telegram_id, username=username)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user, True
