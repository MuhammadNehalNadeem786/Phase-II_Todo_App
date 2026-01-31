import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel
from starlette.testclient import TestClient
from src.main import app
from src.models.database import get_async_session
from src.api.deps.auth import get_current_user_id
from src.models.task import Task


@pytest.fixture(scope="function")
def test_db_session():
    """Create a test database session."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(bind=engine)

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def async_client(test_db_session):
    """Create a test client for testing with mocked authentication."""

    # Import here to avoid circular imports
    from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
    from sqlalchemy.ext.asyncio import create_async_engine

    # Create an async version of the test session
    async_engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    async def override_get_async_session():
        async_session = async_sessionmaker(async_engine, expire_on_commit=False)()
        try:
            yield async_session
        finally:
            await async_session.close()

    def override_get_current_user_id():
        # Return a mock user ID for testing
        return "test_user_123"

    # Apply overrides
    app.dependency_overrides[get_async_session] = override_get_async_session
    app.dependency_overrides[get_current_user_id] = override_get_current_user_id

    with TestClient(app) as tc:
        yield tc

    # Clear overrides after test
    app.dependency_overrides.clear()