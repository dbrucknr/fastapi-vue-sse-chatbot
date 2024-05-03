# Typing
from typing import Any, AsyncGenerator

# FastAPI
from fastapi import Depends

# SQLModel
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

# SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

# Local Dependencies
from src.settings import get_settings, Settings

def build_async_engine(
    settings: Settings = Depends(get_settings)
) -> AsyncEngine:
    return create_async_engine(
        settings.database_url, echo=True, future=True
    )

async def initialize_postgres(
    async_engine: AsyncEngine = Depends(build_async_engine)
) -> None:
    async with async_engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)

async def get_postgres_session(
    async_engine: AsyncEngine = Depends(build_async_engine)
) -> AsyncGenerator[AsyncSession, Any]:
    
    async_session = sessionmaker(
        async_engine, 
        class_=AsyncSession, 
        expire_on_commit=False
    )
    async with async_session() as session:
        yield session