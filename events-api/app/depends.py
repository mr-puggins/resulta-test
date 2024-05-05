"""
Dependency injection file
"""
import sys
from loguru import logger

from app.service.events_service import EventsService
from .settings import app_settings


logger.remove()  # Remove pre-attached stderr sink
logger.add(sys.stderr, colorize=True,
           level="DEBUG",
           enqueue=True)

events_service = EventsService(app_settings)


def get_events_service() -> EventsService:
    return events_service
