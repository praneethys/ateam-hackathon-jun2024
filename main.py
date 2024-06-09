import logging
import os
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.api.routers.user import user_router
from app.api.routers.ingredient import ingredient_router
from app.api.routers.recipe import recipe_router
from app.api.routers.story import story_router
from app.settings import init_settings
from fastapi.staticfiles import StaticFiles


from app.engine.postgresdb import postgresdb
from config.index import config as env

logger = logging.getLogger("uvicorn")


init_settings()
# init_observability()


def init_app(init_db: bool = True) -> FastAPI:
    lifespan = None

    if init_db:
        postgresdb.init(env.SQLALCHEMY_DATABASE_URL, {"echo": True, "future": True})

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            yield
            if postgresdb.get_engine() is not None:
                await postgresdb.close()

    app = FastAPI(lifespan=lifespan)

    if env.ENVIRONMENT == "dev":
        logger.warning("Running in development mode - allowing CORS for all origins")
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    if os.path.exists("data"):
        app.mount("/api/data", StaticFiles(directory="data"), name="static")
    app.include_router(user_router)
    app.include_router(ingredient_router)
    app.include_router(recipe_router)
    app.include_router(story_router)

    return app


app = init_app()


# Redirect to documentation page when accessing base URL
@app.get("/")
async def redirect_to_docs():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    uvicorn.run(app="main:app", host=env.APP_HOST, port=env.APP_PORT, reload=(env.ENVIRONMENT == "dev"))
