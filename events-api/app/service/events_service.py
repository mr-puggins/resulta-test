import httpx

from app.schemas.events_request import EventsRequest
from app.schemas.events_response import Event
from app.schemas.scoreboard import ScoreboardItem, Scoreboard
from app.schemas.team_rankings import TeamRanking, TeamRankings
from app.utils.logs import logger


class EventsService:
    """
    Service class for handling requests to the 3rd party API
    """
    def __init__(self, client_config):
        self._config = client_config
        self._client = httpx.AsyncClient()

    async def get_events(self, events_request: EventsRequest):
        async with self._client:
            date_filter = {
                "since": events_request.startDate,
                "until": events_request.endDate
            }
            headers = {"X-API-Key": "MY-VERY-SECRET-API-KEY"}
            url = "http://localhost:9000/{league}/scoreboard".format(league=events_request.league)
            scoreboard_resp = await self._client.get(url=url, params=date_filter, headers=headers)
            logger.debug("Got a scoreboard response")
            logger.debug(scoreboard_resp)
            scoreboard = Scoreboard(scoreboard_resp.json())

            url = "http://localhost:9000/{league}/team-rankings".format(league=events_request.league)
            team_rankings_response = await self._client.get(url)
            logger.debug("Got a team rankings response")
            logger.debug(team_rankings_response)
            team_rankings = TeamRankings(team_rankings_response.json())

            events = []

            for scoreboard_item in scoreboard.root:
                home_team_info = scoreboard_item.home
                away_team_info = scoreboard_item.away
                # assuming there are no duplicates
                home_team_rankings = next((tr for tr in team_rankings.root if tr.teamId == home_team_info.id), None)
                away_team_rankings = next((tr for tr in team_rankings.root if tr.teamId == away_team_info.id), None)
                event = Event(
                    eventId=scoreboard_item.id,
                    eventDate=scoreboard_item.timestamp.date(),
                    eventTime=scoreboard_item.timestamp.time(),
                    homeTeamId=home_team_info.id,
                    homeTeamNickName=home_team_info.nickName,
                    homeTeamCity=home_team_info.city,
                    homeTeamRank=home_team_rankings.rank,
                    homeTeamRankPoints=home_team_rankings.rankPoints,
                    awayTeamId=away_team_info.id,
                    awayTeamNickName=away_team_info.nickName,
                    awayTeamCity=away_team_info.city,
                    awayTeamRank=away_team_rankings.rank,
                    awayTeamRankPoints=away_team_rankings.rankPoints
                )
                events.append(event)

        return events
