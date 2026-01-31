from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    __tablename__ = "users"  # type: ignore

    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, nullable=False, unique=True)
    email: str = Field(index=True, nullable=False, unique=True)
    hashed_password: str = Field(nullable=False)

















# from sqlalchemy import Column
# from sqlalchemy.ext.declarative import declared_attr
# from sqlmodel import SQLModel, Field


# class User(SQLModel, table=True):
#     @declared_attr
#     def __tablename__(cls) -> str:
#         return "users"

#     id: int | None = Field(default=None, primary_key=True)
#     username: str = Field(index=True, nullable=False, unique=True)
#     email: str = Field(index=True, nullable=False, unique=True)
#     hashed_password: str = Field(nullable=False)
