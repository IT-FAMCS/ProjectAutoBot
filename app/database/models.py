from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine


import os


engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Admin(Base):
    __tablename__ = 'Admins'

    id = mapped_column(BigInteger, primary_key=True)
    tg_id = mapped_column(String)
    name = mapped_column(String)


class Budget_admin(Base):
    __tablename__ = 'Budget_admins'

    id = mapped_column(BigInteger, primary_key=True)
    tg_id = mapped_column(String)
    name = mapped_column(String)


class Release_admin(Base):
    __tablename__ = 'Release_admins'

    name: Mapped[str] = mapped_column(String(50))
    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)


class Locker_admin(Base):
    __tablename__ = 'Locker_admins'

    id = mapped_column(BigInteger, primary_key=True)
    tg_id = mapped_column(String)
    name = mapped_column(String)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
