from fastapi import APIRouter
from starlette.requests import Request

from app.schemas.eventsResponse import Event
from app.service.events_service import EventsService

router = APIRouter(prefix="/events")


@router.get("", response_model=list[Event])
async def get_events(request: Request) -> list[Event]:
    service = EventsService(...)
    events = await service.get_events()
    return events
