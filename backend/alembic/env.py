from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from src.config import settings
from src.db.base import Base

# Import all your models here 👇
from src.models.user import User
from src.models.task import Task

# Alembic Config object
config = context.config

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata for autogenerate
target_metadata = Base.metadata

# Set the database URL dynamically
config.set_main_option('sqlalchemy.url', str(settings.DATABASE_URL))


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # Use the same engine you already use in your app
    from src.models.database import sync_engine  # your engine
    connectable = sync_engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


# Determine mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
