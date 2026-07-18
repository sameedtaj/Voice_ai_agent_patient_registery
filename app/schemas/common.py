from typing import Any

from pydantic import BaseModel


class ErrorDetail(BaseModel):
    code: str
    message: str
    details: Any | None = None


class Envelope(BaseModel):
    data: Any | None = None
    error: ErrorDetail | None = None
