from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
import sys

# import custom modules
# from MovieAPI.api import actors, movies, subscriptions, token, users
from app.utils.logs import logger
from app.middlewares import RequestID, RequestLogger
from app.api import heartbeat_router, events_router


app = FastAPI(title="Events API")

# add middlewares
app.add_middleware(RequestLogger)
app.add_middleware(RequestID)
#app.add_middleware(HTTPSRedirectMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["localhost"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=[
        "Access-Control-Allow-Headers",
        "Content-Type",
        "Authorization",
        "Access-Control-Allow-Origin",
        "Set-Cookie"
    ],
)

# Add prometheus asgi middleware to route /metrics requests
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# add routers
app.include_router(heartbeat_router)
app.include_router(events_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", port=8000, reload=True)
    logger.debug("Bye!")
