from typing import Any, Annotated

from fastapi import APIRouter, Depends
from starlette.requests import Request

from app.depends import get_events_service
from app.schemas.events_request import EventsRequest
from app.schemas.events_response import Event
from app.service.events_service import EventsService

router = APIRouter(prefix="/events")


async def retrieve_events(request: Request, events_request: EventsRequest, events_service: EventsService):
    events = await events_service.get_events(request, events_request)
    return events


@router.get("", response_model=list[Event])
async def get_events(request: Request,
                     events_request: Annotated[Any, Depends(EventsRequest)],
                     events_service: EventsService = Depends(get_events_service)) -> list[Event]:
    return await retrieve_events(request, events_request, events_service)


@router.post("", deprecated=True,
             description="I'm leaving it here only because it was in the original requirements. "
                         "Getting resources with POST hurts my feelings.")
async def get_events_but_silly(request: Request,
                               events_request: EventsRequest,
                               events_service: EventsService = Depends(get_events_service)) -> list[Event]:
    return await retrieve_events(request, events_request, events_service)
