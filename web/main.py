from fastapi import FastAPI
from web.routes import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title = "Platform Stonks API"
)
origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
