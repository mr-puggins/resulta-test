from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from httpx import ConnectError
from starlette.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
import sys

from starlette.requests import Request
from starlette.responses import JSONResponse

from app.schemas.error import APIError
from app.settings import AppSettings
from app.utils.exceptions.api_exception import APIException

from app.depends import logger
from app.middlewares import RequestID, RequestLogger
from app.api import heartbeat_router, events_router

settings = AppSettings()

app = FastAPI(title="Events API", version="0.0.1")

# add middlewares
app.add_middleware(RequestLogger)
app.add_middleware(RequestID)


# Add prometheus asgi middleware to route /metrics requests
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# add routers
app.include_router(heartbeat_router)
app.include_router(events_router)


# Add connection error handling
@app.exception_handler(ConnectError)
async def connection_error_exception_handler(request: Request, exc: ConnectError):
    return JSONResponse(
        status_code=503,
        content=APIError(title='Connection failed',
                         status=503,
                         detail="All attempts to connect to downstream dependency failed").dict()
    )


# Add custom exception to handle 3rd party errors
@app.exception_handler(APIException)
async def api_error_exception_handler(request: Request, exc: APIException):
    return JSONResponse(
        status_code=503,
        content=exc.error.dict()
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", port=8000, reload=True)
    logger.debug("Bye!")
