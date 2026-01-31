from sqlmodel import create_engine, SQLModel

# Export Base for SQLAlchemy models
Base = SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
from src.config import settings

# 1. Neon requires 'postgresql+asyncpg' for async
async_engine = create_async_engine(str(settings.DATABASE_URL))

# 2. Sync engine for creating tables (removes +asyncpg if present)
sync_url = str(settings.DATABASE_URL).replace("+asyncpg", "")
sync_engine = create_engine(sync_url)

# Synchronous SessionLocal for sync DB operations
from sqlalchemy.orm import sessionmaker as sync_sessionmaker
SessionLocal = sync_sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

def init_db(): # Renamed to match your CLI command
    """Create database tables synchronously"""
    from src.models.task import Task 
    SQLModel.metadata.create_all(sync_engine)

async def create_db_and_tables_async():
    """Create database tables asynchronously"""
    from src.models.task import Task 
    async with async_engine.begin() as conn:
        # Corrected: run_sync passes the 'conn' automatically
        await conn.run_sync(SQLModel.metadata.create_all)