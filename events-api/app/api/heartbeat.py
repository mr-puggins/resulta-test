from fastapi import APIRouter, status
from starlette.requests import Request

from app.schemas.heartbeat_response import HeartbeatResponse
from app.utils.logs import logger

router = APIRouter(prefix="/heartbeat")


@router.get("", status_code=status.HTTP_200_OK)
async def get_heartbeat(request: Request) -> HeartbeatResponse:
    logger.debug("PING!")
    return HeartbeatResponse(version=request.app.version, description=request.app.title)
