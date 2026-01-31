# src/db/base.py
from sqlmodel import SQLModel

# Alembic will use this metadata
Base = SQLModel
