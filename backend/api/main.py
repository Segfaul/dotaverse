from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

from backend.api.router import player_router, team_router

tags_metadata = [
    {
        "name": "User",
        "description": "...",
        "externalDocs": {
            "description": "...",
            "url": "...",
        },
    },
    {
        "name": "Admin",
        "description": "...",
    },
]

app = FastAPI(
    title="Dotaverse API",
    summary="Chilled api service for predicting Dota 2 matches 🐍",
    description="Web application for predicting dota 2 matches based on mathematical expectations. CRUD operations with **Admin / User**",
    contact={
        "name": "Segfaul",
        "url": "https://github.com/segfaul",
    },
    # openapi_tags=tags_metadata,
    docs_url=None, redoc_url=None,
)

app.include_router(player_router)
app.include_router(team_router)


@app.get("/docs", include_in_schema=False)
def overridden_swagger():
	return get_swagger_ui_html(
        openapi_url="/openapi.json", title="DotaverseAPI",
        swagger_favicon_url="https://i.postimg.cc/3RqsMjMv/logo.png"
    )


@app.get("/redoc", include_in_schema=False)
def overridden_redoc():
    return get_redoc_html(
        openapi_url="/openapi.json", title="DotaverseAPI",
        redoc_favicon_url="https://i.postimg.cc/3RqsMjMv/logo.png"
    )
