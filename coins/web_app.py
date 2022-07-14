import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

import coins.controller
from coins import __version__, controller
from coins.models.database import Base, engine
from coins.models.schemas import ResponseModel


# Todo: add sentry.
sentry_sdk.init("")

# noinspection PyUnresolvedReferences
from coins.core.config import settings  # noqa

def create_app() -> FastAPI:
    app = FastAPI()
    # app = FastAPI()
    origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(controller.route)
    app.add_middleware(SentryAsgiMiddleware)
    return app


app = create_app()
app.include_router(coins.controller.route)


@app.get("/status", response_model=ResponseModel)
def home():
    return {"message": {"version": __version__}}


@app.on_event("startup")
def setup():
    logger.info("coins Startup")

@app.get('/sentry')
async def sentry():
    raise Exception('Test sentry integration')



if __name__ == "__main__":
    uvicorn.run("coins:webapp", host="0.0.0.0", port=8065, reload=True)



