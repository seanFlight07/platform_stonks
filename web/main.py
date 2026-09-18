from fastapi import FastAPI
from web.routes import router

app = FastAPI(
    title = "Platform Stonks API"
)

app.include_router(router)
