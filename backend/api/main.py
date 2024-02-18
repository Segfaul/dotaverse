import os
import json

from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from dotenv import load_dotenv

# from backend.api.service.db_service import DatabaseService
# from backend.api.router import user_router
# from backend.api.router import product_router


env = os.environ.get
load_dotenv('./.env')

DEBUG = (env('DEBUG').lower()=="true")
POSTGRE_CON = f"postgres://{env('POSTGRES_USER')}:{env('POSTGRES_PASSWORD')}" \
              f"@{env('POSTGRES_HOST')}:{env('POSTGRES_PORT')}/{env('POSTGRES_DB')}"

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
    openapi_tags=tags_metadata,
    docs_url=None, redoc_url=None,
)

# db_service = DatabaseService(DEBUG, POSTGRE_CON, ADMINS)


# app.include_router(user_router.router)
# app.include_router(product_router.router)



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


@app.on_event("startup")
async def startup() -> None:
    ...
    # await db_service.init_db()


@app.on_event("shutdown")
async def shutdown() -> None:
    ...
    # await db_service.close_db()
