# db connection related stuff
from typing import AsyncGenerator

from sqlalchemy import MetaData, NullPool
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import declarative_base

from src.config import settings

# Common interaction with database
Base = declarative_base()
metadata = MetaData()

# create async engine for interaction with database
engine = create_async_engine(
    settings.db_url,
    poolclass=NullPool,
    future=True,
    # verbose output of DB operations
    # echo=True,
    # autocommit (not need to use db.commit())
    execution_options={"isolation_level": "AUTOCOMMIT"},
)
async_session_maker = async_sessionmaker(
    engine,
    # class_=AsyncSession,
    expire_on_commit=False,
)


# async def create_db_and_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
