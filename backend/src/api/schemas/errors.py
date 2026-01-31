from pydantic import BaseModel
from typing import Optional


class ErrorResponse(BaseModel):
    detail: str


class NotFoundResponse(ErrorResponse):
    detail: str = "Item not found"


class ForbiddenResponse(ErrorResponse):
    detail: str = "Access denied"


class UnauthorizedResponse(ErrorResponse):
    detail: str = "Unauthorized"


class BadRequestResponse(ErrorResponse):
    detail: str = "Bad request"