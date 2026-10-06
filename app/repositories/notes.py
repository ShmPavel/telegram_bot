from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Note


async def create_note(session: AsyncSession, user_id: int, text: str) -> Note:
    note = Note(user_id=user_id, text=text)
    session.add(note)
    await session.flush()
    return note


async def get_last_notes(session: AsyncSession, user_id: int, limit: int = 10) -> list[Note]:
    result = await session.execute(
        select(Note)
        .where(Note.user_id == user_id)
        .order_by(Note.created_at.desc())
        .limit(limit)
    )
    return list(result.scalars().all())