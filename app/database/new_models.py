from sqlalchemy import BigInteger, String, ForeignKey, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy import JSON

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


class Exemption_admin(Base):
    __tablename__ = 'Exemption_admins'

    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))



class Request(Base):
    __tablename__ = 'Requests'

    request_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    text: Mapped[str] = mapped_column(String(500))
    photo_ids: Mapped[list[int]] = mapped_column(JSON, default=list)
    approved: Mapped[str] = mapped_column(String, default="Unprocessed")


class Secretary(Base):
    __tablename__ = 'Secretaries'

    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
