import asyncio
from typing import Any, AsyncGenerator, Generator

import asyncpg
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.pool import NullPool

from src.auth.models import *
from src.config import settings
from src.database import Base, get_async_session
from src.main import app

# DATABASE
metadata = Base.metadata

CLEAN_TABLES = [
    "user",
]

engine_test = create_async_engine(
    settings.test_db_url,
    poolclass=NullPool,
    future=True,
    echo=True,
)
test_async_session_maker = async_sessionmaker(
    engine_test,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with test_async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)


# SETUP
@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# Test clients
@pytest.fixture(scope="function")
def client() -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `test_async_session_maker`
    to override the `get_async_session` dependency that is injected into routes.
    """

    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    """
    Create a new FastAPI test AsyncClient that uses the 
    `test_async_session_maker` to override the `get_async_session` dependency
    that is injected into routes.
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def async_session_test():
    """
    Create an async session to interact with database.
    """
    engine = create_async_engine(settings.test_db_url, future=True, echo=True)
    async_session = async_sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    yield async_session


@pytest.fixture(scope="function", autouse=True)
async def clean_tables(async_session_test):
    """Clean data in all tables before running test function"""
    async with async_session_test() as session:
        async with session.begin():
            for table_for_cleaning in CLEAN_TABLES:
                await session.execute(
                    text(f"""TRUNCATE TABLE "{table_for_cleaning}";""")
                )


@pytest.fixture(scope="session")
async def asyncpg_pool():
    """Create an asyncpg connection pool for interaction with database"""
    pool = await asyncpg.create_pool("".join(settings.test_db_url.split("+asyncpg")))
    yield pool
    await pool.close()


@pytest.fixture
async def get_user_from_database(asyncpg_pool):
    async def get_user_from_database_by_uuid(id: str):
        async with asyncpg_pool.acquire() as connection:
            return await connection.fetch("""SELECT * FROM "user" WHERE id = $1;""", id)

    return get_user_from_database_by_uuid


@pytest.fixture
async def create_user_in_database(asyncpg_pool):
    async def create_user_in_database(
        id: str,
        username: str,
        email: str,
        is_active: bool,
        hashed_password: str,
        # roles: list[PortalRole],
    ):
        async with asyncpg_pool.acquire() as connection:
            return await connection.execute(
                """INSERT INTO "user" VALUES ($1, $2, $3, $4, $5)""",
                id,
                username,
                email,
                is_active,
                hashed_password,
                # roles,
            )

    return create_user_in_database


# def create_test_auth_headers_for_user(email: str) -> dict[str, str]:
#     access_token = create_access_token(
#         data={"sub": email},
#         expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
#     )
#     return {"Authorization": f"Bearer {access_token}"}
