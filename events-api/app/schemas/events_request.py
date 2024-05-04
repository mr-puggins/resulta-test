import datetime
from typing import Literal

from fastapi_async_safe import async_safe
from pydantic import BaseModel


@async_safe
class EventsRequest(BaseModel):
    league: Literal['NFL']
    startDate: datetime.date | None = None
    endDate: datetime.date | None = None
