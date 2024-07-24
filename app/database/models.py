from sqlalchemy import BigInteger, String, ForeignKey, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine


import os


engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'Users'

    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String(50))


class Admin(Base):
    __tablename__ = 'Admins'

    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))


class Budget_admin(Base):
    __tablename__ = 'Budget_admins'

    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))


class Release_admin(Base):
    __tablename__ = 'Release_admins'

    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))


class Locker_admin(Base):
    __tablename__ = 'Locker_admins'

    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))


class Request(Base):
    __tablename__ = 'Requests'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(String(500))
    accepted: Mapped[str] = mapped_column(String, default="False")


class Secretary(Base):
    __tablename__ = 'Secretaries'

    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
