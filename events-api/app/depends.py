"""
Dependency injection file
"""
import sys
from loguru import logger

from app.service.events_service import EventsService
from .settings import app_settings
from asgi_correlation_id.context import correlation_id


def correlation_id_filter(record):
    record['correlation_id'] = correlation_id.get()
    return record['correlation_id']


logger.remove()
fmt = "{level}: \t  {time} {name}:{line} [{correlation_id}] - {message}"
logger.add(sys.stderr, format=fmt, colorize=True, level="DEBUG", filter=correlation_id_filter)

events_service = EventsService(app_settings)


def get_events_service() -> EventsService:
    return events_service
