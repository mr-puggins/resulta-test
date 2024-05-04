from typing import ForwardRef

from pydantic import BaseModel


APIError = ForwardRef('APIError')


class APIError(BaseModel):
    title: str
    status: int
    detail: str | None = None
    cause: APIError | None = None
