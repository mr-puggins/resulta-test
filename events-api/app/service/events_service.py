import httpx

from app.schemas.error import APIError
from app.schemas.events_request import EventsRequest
from app.schemas.events_response import Event
from app.schemas.scoreboard import ScoreboardItem, Scoreboard
from app.schemas.team_rankings import TeamRanking, TeamRankings
from app.settings import AppSettings
from app.utils.exceptions.api_exception import APIException
from app.utils.logs import logger


class EventsService:
    """
    Service class for handling requests to the 3rd party API
    """
    def __init__(self, settings: AppSettings):
        self._config = settings
        self._client = httpx.AsyncClient()

    async def get_events(self, events_request: EventsRequest) -> list[Event]:
        async with self._client:
            date_filter = {
                "since": str(events_request.startDate),
                "until": str(events_request.endDate)
            }
            api_key = self._config.api_key
            headers = {"X-API-Key": api_key}
            url = "{url}/{league}{endpoint}".format(
                url=self._config.third_party_url,
                league=events_request.league,
                endpoint=self._config.scoreboard_endpoint
            )
            scoreboard_resp = await self._client.get(url=url, params=date_filter, headers=headers)
            logger.debug("Got a scoreboard response")
            logger.debug(scoreboard_resp)

            await self.__process_response(scoreboard_resp)

            scoreboard = Scoreboard(scoreboard_resp.json())

            url = "{url}/{league}{endpoint}".format(
                url=self._config.third_party_url,
                league=events_request.league,
                endpoint=self._config.team_rankings_endpoint
            )
            team_rankings_resp = await self._client.get(url=url, headers=headers)
            logger.debug("Got a team rankings response")
            logger.debug(team_rankings_resp)

            await self.__process_response(team_rankings_resp)

            team_rankings = TeamRankings(team_rankings_resp.json())

            events = []

            for scoreboard_item in scoreboard.root:
                event = await self.__build_event(scoreboard_item, team_rankings)
                events.append(event)

        return events

    async def __process_response(self, resp):
        # It is not clear what error code will be returned by requesting a wrong league,
        # so let's assume it's 404, even though it is not explicitly documented.
        # Another assumption is that the default/unexpected error from the spec is 500,
        # because it is most likely the only error the server could have thrown in a
        # managed fashion.
        match resp.status_code:
            case 200:
                logger.debug("And it's not an error \\o/")
            case 400 | 401 | 403 | 404 | 500:
                logger.debug("And it was an error :(")
                error = APIError(**resp.json())
                raise APIException(message=error.title, error=error)
            case _:
                logger.debug("Expected a response, but got a surprise")
                raise APIException(message="Unexpected error",
                                   error=APIError(title="Unexpected error", status=resp.status_code))

    async def __build_event(self, scoreboard_item, team_rankings):
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
        return event
