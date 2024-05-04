from typing import Any, Annotated

from fastapi import APIRouter, Depends
from starlette.requests import Request

from app.schemas.events_request import EventsRequest
from app.schemas.events_response import Event
from app.service.events_service import EventsService

router = APIRouter(prefix="/events")


async def retrieve_events(events_request: EventsRequest):
    service = EventsService(...)
    events = await service.get_events(events_request)
    return events


@router.get("", response_model=list[Event])
async def get_events(events_request: Annotated[Any, Depends(EventsRequest)]) -> list[Event]:
    return await retrieve_events(events_request)


@router.post("", deprecated=True)
async def get_events_but_silly(events_request: EventsRequest) -> list[Event]:
    return await retrieve_events(events_request)
