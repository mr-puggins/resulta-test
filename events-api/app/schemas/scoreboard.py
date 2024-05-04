import datetime
from uuid import UUID

from pydantic import BaseModel, RootModel


class TeamInfo(BaseModel):
    id: UUID
    city: str
    nickName: str


class ScoreboardItem(BaseModel):
    id: UUID
    timestamp: datetime.datetime
    home: TeamInfo
    away: TeamInfo


class Scoreboard(RootModel):
    root: list[ScoreboardItem]
