import datetime
from typing import Literal

from pydantic import BaseModel


class EventsRequest(BaseModel):
    league: Literal['NFL']
    startDate: datetime.date | None = None
    endDate: datetime.date | None = None
