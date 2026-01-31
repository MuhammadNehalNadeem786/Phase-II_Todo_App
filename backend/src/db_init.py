"""Database initialization script for Neon PostgreSQL."""
import asyncio
import sys
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from src.models.task import Task  # Import all models to register them
from src.config import settings


async def create_tables():
    """Create all tables in the database."""
    print("Connecting to database...")

    # Create async engine
    engine = create_async_engine(str(settings.DATABASE_URL))

    try:
        print("Creating tables...")
        # Create tables
        async with engine.begin() as conn:
            # Drop all tables first (optional, for development)
            # await conn.run_sync(SQLModel.metadata.drop_all)

            # Create all tables
            await conn.run_sync(SQLModel.metadata.create_all)

        print("Tables created successfully!")

    except Exception as e:
        print(f"Error creating tables: {e}")
        raise
    finally:
        await engine.dispose()


def run_init():
    """Run the database initialization."""
    print("Starting database initialization...")

    # Check if we have a valid database URL
    if not settings.DATABASE_URL or "your-neon-url-here" in settings.DATABASE_URL:
        print("ERROR: Please set a valid DATABASE_URL in your .env file")
        print("Example: DATABASE_URL=postgresql+asyncpg://username:password@ep-xxxxxx.us-east-1.aws.neon.tech/dbname?sslmode=require")
        sys.exit(1)

    try:
        asyncio.run(create_tables())
        print("Database initialization completed successfully!")
    except Exception as e:
        print(f"Failed to initialize database: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run_init()