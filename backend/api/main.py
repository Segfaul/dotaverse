import time
import asyncio

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from backend.config import limiter
from backend.api.router import hero_router, \
    match_router, matchplayer_router, matchteam_router, \
    player_router, playerherochance_router, \
    request_router, team_router, teamplayer_router, \
    user_router

tags_metadata = [
    {
        "name": "Hero",
        "description": "Dota 2 hero endpoint",
    },
    {
        "name": "Match",
        "description": "Dota 2 match record endpoint",
    },
    {
        "name": "MatchPlayer",
        "description": "Dota 2 match player record endpoint",
    },
    {
        "name": "MatchTeam",
        "description": "Dota 2 match team record endpoint",
    },
    {
        "name": "Player",
        "description": "Dota 2 player endpoint",
    },
    {
        "name": "PlayerHeroChance",
        "description": "Dota 2 pro player win chance per hero endpoint",
    },
    {
        "name": "Request",
        "description": "DotaBuff request endpoint",
    },
    {
        "name": "Team",
        "description": "Dota 2 pro team endpoint",
    },
    {
        "name": "TeamPlayer",
        "description": "Dota 2 pro player endpoint",
    },
]

app = FastAPI(
    title="Dotaverse API",
    summary="Chilled api service for predicting Dota 2 matches 🐍",
    description="Web application for predicting dota 2 matches based " \
        "on mathematical expectations. CRUD operations for **Auth / Non-Auth**",
    version='0.0.1',
    contact={
        "name": "Segfaul",
        "url": "https://github.com/segfaul",
    },
    openapi_tags=tags_metadata,
    docs_url=None, redoc_url=None,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(user_router, prefix="/api")
app.include_router(hero_router, prefix="/api")
app.include_router(match_router, prefix="/api")
app.include_router(matchplayer_router, prefix="/api")
app.include_router(matchteam_router, prefix="/api")
app.include_router(player_router, prefix="/api")
app.include_router(playerherochance_router, prefix="/api")
app.include_router(request_router, prefix="/api")
app.include_router(team_router, prefix="/api")
app.include_router(teamplayer_router, prefix="/api")


@app.middleware("http")
async def timeout_middleware(request: Request, call_next):
    """
    TIMEOUT Middleware, throws an error if request exceeds 5s
    """
    start_time = time.time()
    try:
        return await asyncio.wait_for(call_next(request), timeout=5)

    except asyncio.TimeoutError:
        process_time = time.time() - start_time
        return JSONResponse(
            {
                'detail': 'Request processing time excedeed limit',
                'processing_time': process_time
            },
            status_code=status.HTTP_504_GATEWAY_TIMEOUT
        )


@app.get("/api/swagger", include_in_schema=False)
def overridden_swagger():
    return get_swagger_ui_html(
        openapi_url="/openapi.json", title="DotaverseAPI",
        swagger_favicon_url="https://i.postimg.cc/3RqsMjMv/logo.png"
    )


@app.get("/api/redoc", include_in_schema=False)
def overridden_redoc():
    return get_redoc_html(
        openapi_url="/openapi.json", title="DotaverseAPI",
        redoc_favicon_url="https://i.postimg.cc/3RqsMjMv/logo.png"
    )
