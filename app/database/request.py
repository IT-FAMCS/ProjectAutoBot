from app.database.models import async_session
from app.database.models import Admin, Budget_admin, Release_admin, User, Request, Secretary
from sqlalchemy import select


async def set_user(tg_id, username):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id, username=username))
            await session.commit()


async def set_admin(fio, tg_id):
    async with async_session() as session:
        admin = await session.scalar(select(Admin).where(Admin.tg_id == tg_id))

        if not admin:
            session.add(Admin(tg_id=tg_id, name=fio))
            await session.commit()


async def set_release_admin(fio, tg_id):
    async with async_session() as session:
        name = await session.scalar(select(Release_admin).where(Release_admin.name == fio))
        id = await session.scalar(select(Release_admin).where(Release_admin.tg_id == tg_id))
        if not name and not id:
            session.add(Release_admin(tg_id=tg_id, name=fio))
            await session.commit()


async def set_budget_admin(fio, tg_id):
    async with async_session() as session:
        name = await session.scalar(select(Budget_admin).where(Budget_admin.name == fio))
        id = await session.scalar(select(Budget_admin).where(Budget_admin.tg_id == tg_id))
        if not name and not id:
            session.add(Budget_admin(tg_id=tg_id, name=fio))
            await session.commit()


async def set_secretary(fio, tg_id):
    async with async_session() as session:
        name = await session.scalar(select(Secretary).where(Secretary.name == fio))
        id = await session.scalar(select(Secretary).where(Secretary.tg_id == tg_id))
        if not name and not id:
            session.add(Secretary(tg_id=tg_id, name=fio))
            await session.commit()


async def find_user(username):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.username == username))
        return user.tg_id


async def get_admins():
    async with async_session() as session:
        result = await session.execute(select(Admin.tg_id))
        return [row[0] for row in result.all()]


async def get_release_admins():
    async with async_session() as session:
        result = await session.execute(select(Release_admin.tg_id))
        return [row[0] for row in result.all()]


async def get_budget_admins():
    async with async_session() as session:
        result = await session.execute(select(Budget_admin.tg_id))
        return [row[0] for row in result.all()]


async def get_secretaries():
    async with async_session() as session:
        result = await session.execute(select(Secretary.tg_id))
        return [row[0] for row in result.all()]


async def set_request(text):
    async with async_session() as session:
        session.add(Request(text=text))
        await session.commit()


async def set_request_accepted(id):
    async with async_session() as session:
        request = await session.scalar(select(Request).where(Request.id == id))
        request.accepted = "True"
        await session.commit()


async def get_request_accepted(id):
    async with async_session() as session:
        request = await session.scalar(select(Request).where(Request.id == id))
        if request is None:
            return "False"
        return request.accepted


async def get_request_id(text):
    async with async_session() as session:
        request = await session.scalar(select(Request).where(Request.text == text))
        return request.id


async def delete_release_admin(tg_id):
    async with async_session() as session:
        admin = await session.scalar(select(Release_admin).where(Release_admin.tg_id == tg_id))
        await session.delete(admin)
        await session.commit()


async def delete_budget_admin(tg_id):
    async with async_session() as session:
        admin = await session.scalar(select(Budget_admin).where(Budget_admin.tg_id == tg_id))
        await session.delete(admin)
        await session.commit()
