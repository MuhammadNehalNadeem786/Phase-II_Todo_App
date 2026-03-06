from sqlmodel import create_engine, SQLModel

# Export Base for SQLAlchemy models
Base = SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
from src.config import settings

# Helper function to convert database URL for async engines
def get_async_url(url: str) -> str:
    """Convert database URL to async-compatible format"""
    url_str = str(url)
    # For SQLite, use aiosqlite driver
    if url_str.startswith("sqlite://"):
        return url_str.replace("sqlite://", "sqlite+aiosqlite://")
    # For PostgreSQL, ensure asyncpg driver is present
    elif url_str.startswith("postgresql://") and "+asyncpg" not in url_str:
        return url_str.replace("postgresql://", "postgresql+asyncpg://")
    # Already has async driver or other database
    return url_str

# Helper function to convert database URL for sync engines
def get_sync_url(url: str) -> str:
    """Convert database URL to sync-compatible format"""
    url_str = str(url)
    # Remove async drivers
    url_str = url_str.replace("+asyncpg", "")
    url_str = url_str.replace("+aiosqlite", "")
    return url_str

# 1. Create async engine with proper driver
async_url = get_async_url(settings.DATABASE_URL)
async_engine = create_async_engine(async_url)

# 2. Sync engine for creating tables (removes async drivers)
sync_url = get_sync_url(settings.DATABASE_URL)
sync_engine = create_engine(sync_url)

# Synchronous SessionLocal for sync DB operations
from sqlalchemy.orm import sessionmaker as sync_sessionmaker
SessionLocal = sync_sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

# Async SessionLocal for async DB operations
AsyncSessionLocal = async_sessionmaker(
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