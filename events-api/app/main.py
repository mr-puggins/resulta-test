import uuid

from asgi_correlation_id import CorrelationIdMiddleware
from asgi_correlation_id.middleware import is_valid_uuid4
from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from httpx import ConnectError
from starlette.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
import sys

from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.schemas.error import APIError
from app.settings import AppSettings
from app.utils.exceptions.api_exception import APIException

from app.depends import logger
from app.middlewares import RequestLogger
from app.api import heartbeat_router, events_router

settings = AppSettings()

app = FastAPI(title="Events API", version="0.0.1")

# add middlewares
app.add_middleware(RequestLogger)
app.add_middleware(
    CorrelationIdMiddleware,
    header_name='X-Request-ID',
    update_request_header=True,
    generator=lambda: uuid.uuid4().hex,
    validator=is_valid_uuid4,
    transformer=lambda a: a,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['X-Requested-With', 'X-Request-ID'],
    expose_headers=['X-Request-ID']
)


# Add prometheus asgi middleware to route /metrics requests
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# add routers
app.include_router(heartbeat_router)
app.include_router(events_router)


# Add connection error handling
@app.exception_handler(ConnectError)
async def connection_error_exception_handler(exc: ConnectError):
    logger.error(exc)
    return JSONResponse(
        status_code=503,
        content=APIError(title='Connection failed',
                         status=503,
                         detail="All attempts to connect to downstream dependency failed").dict()
    )


# Add custom exception to handle 3rd party errors
@app.exception_handler(APIException)
async def api_error_exception_handler(exc: APIException):
    logger.error(exc)
    return JSONResponse(
        status_code=503,
        content=exc.error.dict()
    )


# Add custom exception to handle 3rd party data errors
@app.exception_handler(AttributeError)
async def api_error_exception_handler(exc: AttributeError):
    logger.error(exc)
    return JSONResponse(
        status_code=503,
        content=format("Data integrity or dependency contract issue: {}", str(exc))
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", port=8000, reload=True)
    logger.debug("Bye!")
