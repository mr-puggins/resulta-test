from unittest.mock import ANY

import httpx
import pytest
from pytest_mock import mocker

from app.schemas.events_request import EventsRequest
from app.schemas.scoreboard import ScoreboardItem
from app.schemas.team_rankings import TeamRankings
from app.service.events_service import EventsService
from tests.test_settings import test_settings


@pytest.fixture()
def events_service():
    return EventsService(test_settings)


@pytest.mark.asyncio
async def test_can_build_event(events_service):
    rankings = [{
        "teamId": "ae5132a4-e4b2-4bda-9933-b75c542b8d35",
        "rank": 1,
        "rankPoints": 100.3
    },
        {
            "teamId": "8da0c96d-7b3d-41f3-9e68-29607f3babcf",
            "rank": 3,
            "rankPoints": 33.4
        }]
    scoreboard_item = {
        "id": "5055c2a2-af68-4082-9834-ceb36dd0a807",
        "timestamp": "2023-01-11T14:00:00Z",
        "away": {
            "id": "ae5132a4-e4b2-4bda-9933-b75c542b8d35",
            "city": "Arizona",
            "nickName": "Arizona Cardinals"
        },
        "home": {
            "id": "8da0c96d-7b3d-41f3-9e68-29607f3babcf",
            "city": "Atlanta",
            "nickName": "Atlanta Falcons"
        }
    }
    event = await events_service._EventsService__build_event(
        ScoreboardItem(**scoreboard_item),
        TeamRankings(rankings)
    )
    assert str(event.eventId) == "5055c2a2-af68-4082-9834-ceb36dd0a807"
    assert str(event.eventDate) == "2023-01-11"
    assert str(event.eventTime) == "14:00:00"

    assert str(event.homeTeamId) == "8da0c96d-7b3d-41f3-9e68-29607f3babcf"
    assert event.homeTeamCity == "Atlanta"
    assert event.homeTeamNickName == "Atlanta Falcons"
    assert event.homeTeamRank == 3
    assert event.homeTeamRankPoints == 33.4

    assert str(event.awayTeamId) == "ae5132a4-e4b2-4bda-9933-b75c542b8d35"
    assert event.awayTeamCity == "Arizona"
    assert event.awayTeamNickName == "Arizona Cardinals"
    assert event.awayTeamRank == 1
    assert event.awayTeamRankPoints == 100.3


@pytest.mark.asyncio
async def test_can_get_event(events_service, mocker):
    mock_get = mocker.patch('httpx.AsyncClient.get', return_value=httpx.Response(200, json=[]))
    event_request = EventsRequest(
        league='NFL', startDate='2024-01-01', endDate='2024-05-04'
    )
    await events_service.get_events(event_request)
    expected_calls = [
        mocker.call(
            url='http://localhost:9000/NFL/scoreboard',
            params={'since': '2024-01-01', 'until': '2024-05-04'},
            headers={'X-API-Key': ANY, 'X-Request-ID': None}
        ),
        mocker.call(url='http://localhost:9000/NFL/team-rankings',
                    headers={'X-API-Key': ANY, 'X-Request-ID': None})
    ]
    mock_get.assert_has_calls(expected_calls)


@pytest.mark.asyncio
async def test_can_process_error(events_service, mocker):
    mock_get = mocker.patch('httpx.AsyncClient.get', return_value=httpx.Response(404, json={
        "title": "Goofed up",
        "status": 400,
        "detail": "My hovercraft is full of eels",
        "cause": None
    }))
    event_request = EventsRequest(
        league='NFL', startDate=None, endDate=None
    )
    with pytest.raises(Exception) as api_error_info:
        await events_service.get_events(event_request)
    assert api_error_info.typename == 'APIException'
    assert api_error_info.value.error.status == 400
    assert api_error_info.value.error.title == "Goofed up"
    assert api_error_info.value.error.detail == "My hovercraft is full of eels"

