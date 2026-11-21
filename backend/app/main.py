from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.database import init_db
from app.api import usage, models_api, settings as settings_api, proxy, status, scheduler_api, auth
from app.api.auth import verify_token
from app.tasks.scheduler import start_scheduler
from app.tasks.scheduler import poll_api_key_usage, poll_api_key_cost


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await start_scheduler()
    # Seed key usage/cost history once at startup; errors are retained in
    # scheduler logs on later polls.
    await poll_api_key_usage()
    await poll_api_key_cost()
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

# Paths that do not require a dashboard session token.
PUBLIC_API_PATHS = {"/api/v1/auth/login", "/api/v1/health"}


@app.middleware("http")
async def require_dashboard_auth(request: Request, call_next):
    """Protect dashboard APIs with the Bearer token issued by /auth/login."""
    path = request.url.path
    if path.startswith("/api/v1/") and path not in PUBLIC_API_PATHS and request.method != "OPTIONS":
        header = request.headers.get("authorization", "")
        token = header[7:].strip() if header.lower().startswith("bearer ") else ""
        if not verify_token(token):
            return JSONResponse(
                status_code=401,
                content={"code": 401, "message": "unauthorized", "data": None},
            )
    return await call_next(request)


app.include_router(auth.router)
app.include_router(usage.router)
app.include_router(models_api.router)
app.include_router(settings_api.router)
app.include_router(proxy.router)
app.include_router(status.router)
app.include_router(scheduler_api.router)


@app.get("/api/v1/health")
async def health():
    return {"status": "ok"}
