from app.database.models import async_session
from app.database.models import Admin, Budget_admin, Release_admin, Locker_admin
from sqlalchemy import select


async def set_release_admin(fio, tg_id):
    async with async_session() as session:
        name = await session.scalar(select(Release_admin).where(Release_admin.name == fio))
        id = await session.scalar(select(Release_admin).where(Release_admin.tg_id == tg_id))
        if not name and not id:
            session.add(Release_admin(tg_id=tg_id, name=fio))
            await session.commit()
