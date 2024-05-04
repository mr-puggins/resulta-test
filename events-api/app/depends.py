"""
Dependency injection file
"""
from .settings import app_settings
from app.service.events_service import EventsService

events_service = EventsService(app_settings)


def get_events_service() -> EventsService:
    return events_service
