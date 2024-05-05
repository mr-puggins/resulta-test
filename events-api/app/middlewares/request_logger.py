"""Provides request logging functionality"""

import time
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.depends import logger


class RequestLogger(BaseHTTPMiddleware):
    def __init__(self, app) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> Response:
        """
        Implement the dispatch method.

        Args:
            request (fastapi.Request): Instance of a FastAPI class.
            call_next (function): Function to call next middleware.
        """

        try:
            start = time.time()
            response = await call_next(request)
            end = time.time()
            logger.info(
                f"method={request.method} | {request.url} | {response.status_code} | {end - start}s"
            )
            return response
        except Exception as e:
            logger.error(
                f"method={request.method} | {request.url} | {e}"
            )
