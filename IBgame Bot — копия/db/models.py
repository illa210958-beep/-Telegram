

from sqlalchemy import Integer, BigInteger, String, ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine=create_async_engine(url='sqlite+aiosqlite:///dp.sqlite3')
async_session =async_sessionmaker(engine)

class Base(AsyncAttrs,DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id:Mapped[int] = mapped_column(primary_key=True)
    tg_id=mapped_column(BigInteger)
    name:Mapped[str]=mapped_column(String(100))

class Progr(Base):
    __tablename__ = 'progress'
    id: Mapped[int] = mapped_column(primary_key=True)
    et1:Mapped[int] = mapped_column()
    et2: Mapped[int] = mapped_column()
    et3: Mapped[int] = mapped_column()
    #user: Mapped[int] == mapped_column(ForeignKey('users.id'))

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)