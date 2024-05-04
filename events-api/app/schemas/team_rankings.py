from uuid import UUID

from pydantic import BaseModel, Field, RootModel


class TeamRanking(BaseModel):
    teamId: UUID
    rank: int = Field(ge=1)
    rankPoints: float = Field(ge=0)


class TeamRankings(RootModel):
    root: list[TeamRanking]
