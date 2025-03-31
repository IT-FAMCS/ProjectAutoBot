from app.database.models import async_session
from app.database.models import Admin, Budget_admin, Exemption_admin, User, Request, Secretary
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


async def set_exemption_admin(fio, tg_id):
    async with async_session() as session:
        name = await session.scalar(select(Exemption_admin).where(Exemption_admin.name == fio))
        id = await session.scalar(select(Exemption_admin).where(Exemption_admin.tg_id == tg_id))
        if not name and not id:
            session.add(Exemption_admin(tg_id=tg_id, name=fio))
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


async def get_exemption_admins():
    async with async_session() as session:
        result = await session.execute(select(Exemption_admin.tg_id))
        return [row[0] for row in result.all()]


async def get_budget_admins():
    async with async_session() as session:
        result = await session.execute(select(Budget_admin.tg_id))
        return [row[0] for row in result.all()]


async def get_secretaries():
    async with async_session() as session:
        result = await session.execute(select(Secretary.tg_id))
        return [row[0] for row in result.all()]



async def delete_exemption_admin(tg_id):
    async with async_session() as session:
        admin = await session.scalar(select(Exemption_admin).where(Exemption_admin.tg_id == tg_id))
        await session.delete(admin)
        await session.commit()

async def delete_budget_admin(tg_id):
    async with async_session() as session:
        admin = await session.scalar(select(Budget_admin).where(Budget_admin.tg_id == tg_id))
        await session.delete(admin)
        await session.commit()

async def delete_secretary(tg_id):
    async with async_session() as session:
        admin = await session.scalar(select(Secretary).where(Secretary.tg_id == tg_id))
        await session.delete(admin)
        await session.commit()


async def set_request(text, tg_id, photo_ids = []):
    async with async_session() as session:
        session.add(Request(tg_id = tg_id, text=text, photo_ids = photo_ids))
        await session.commit()

async def set_request_approved(request_id):
    async with async_session() as session:
        request = await session.scalar(select(Request).where(Request.request_id == request_id))
        request.approved = "Approved"
        await session.commit()

async def set_request_declined(request_id):
    async with async_session() as session:
        request = await session.scalar(select(Request).where(Request.request_id == request_id))
        request.approved = "Declined"
        await session.commit()

async def is_request_approved(request_id):
    async with async_session() as session:
        request = await session.scalar(select(Request).where(Request.request_id == request_id))
        if request_id is None:
            return "False"
        return request.approved

async def get_request_data(request_id):
    async with async_session() as session:
        request = await session.scalar(select(Request).where(Request.request_id == request_id))
        if request is None:
            return "Undefined"
        return request.text

async def get_request_id(text):
    async with async_session() as session:
        request = await session.scalar(select(Request).where(Request.text == text))
        return request.request_id
    
async def get_request_tg_id(request_id):
    async with async_session() as session:
        request = await session.scalar(select(Request).where(Request.request_id == request_id))
        if request is None:
            return 0
        return request.tg_id
    
