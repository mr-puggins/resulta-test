"""Adds uuid to the request header for debugging."""

from uuid import uuid4
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.depends import logger


class RequestID(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        """
        Implement the dispatch method.

        Args:
            request (fastapi.Request): Instance of a FastAPI class.
            call_next (function): Function to call next middleware.
        """

        try:
            request_id = uuid4()
            request.state.request_id = request_id
            response = await call_next(request)
            response.headers["request_id"] = str(request_id)
            return response
        except Exception as e:
            logger.warning(
                f"method={request.method} | {request.url} | {request.state.request_id} | {e}"
            )
            return JSONResponse(status_code=500, content={"reason": str(e)})
