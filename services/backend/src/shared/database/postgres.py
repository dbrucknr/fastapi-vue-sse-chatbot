# Python Dependencies
from typing import Any, AsyncGenerator

# SQLModel
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

# SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

# Local Dependencies
from src.settings import get_settings

async_engine = create_async_engine(
    url=get_settings().database_url, 
    echo=True, 
    future=True
)

async def initialize_postgres() -> None:
    """Create all Module Tables (must be imported in same file)"""
    async with async_engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)

async def get_postgres_session() -> AsyncGenerator[AsyncSession, Any]:
    """
        Access the established Postgres Session Connection to perform 
        CRUD operations
    """
    async_session = sessionmaker(
        async_engine, 
        class_=AsyncSession, 
        expire_on_commit=False
    )
    async with async_session() as session:
        yield session