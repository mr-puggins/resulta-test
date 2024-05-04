from pydantic import BaseModel


class Error(BaseModel):
    title: str
    status: int
    detail: str | None
    cause: dict | {}
