import datetime
from uuid import UUID

from pydantic import BaseModel, Field, RootModel


class Event(BaseModel):
    eventId: UUID
    eventDate: datetime.date
    eventTime: datetime.time
    homeTeamId: UUID
    homeTeamNickName: str
    homeTeamCity: str
    homeTeamRank: int = Field(ge=1)
    homeTeamRankPoints: float = Field(ge=0)
    awayTeamId: UUID
    awayTeamNickName: str
    awayTeamCity: str
    awayTeamRank: int = Field(ge=1)
    awayTeamRankPoints: float = Field(ge=0)
