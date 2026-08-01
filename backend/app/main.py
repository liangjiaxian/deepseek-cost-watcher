from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import init_db
from app.api import usage, models_api, settings as settings_api, proxy, status, scheduler_api
from app.tasks.scheduler import start_scheduler
from app.tasks.scheduler import poll_api_key_usage


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await start_scheduler()
    # Seed key usage history once at startup; errors are retained in scheduler logs on later polls.
    await poll_api_key_usage()
    yield


app = FastAPI(
    title="DeepSeek Token Monitor",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usage.router)
app.include_router(models_api.router)
app.include_router(settings_api.router)
app.include_router(proxy.router)
app.include_router(status.router)
app.include_router(scheduler_api.router)


@app.get("/api/v1/health")
async def health():
    return {"status": "ok"}
