from pydantic import BaseModel


class HeartbeatResponse(BaseModel):
    version: str
    description: str | None = None
