from __future__ import annotations

import logging
import time
from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.routes import router
from app.core.config import settings
from app.core.errors import ErrorResponse
from app.core.logging import configure_logging
from app.core.request_context import get_request_id, set_request_id
from app.db.session import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging(settings.log_level)
    await init_db()
    yield


app = FastAPI(
    title="Multi-Agent Workflow System",
    description="Orchestrates Research, Summarizer, and Planner agents into a structured workflow.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger(__name__)


@app.middleware("http")
async def request_context_middleware(request: Request, call_next):
    header = settings.request_id_header
    request_id = request.headers.get(header) or str(uuid4())
    set_request_id(request_id)

    started_at = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = round((time.perf_counter() - started_at) * 1000, 2)

    response.headers[header] = request_id
    logger.info("request_completed", extra={"path": request.url.path, "elapsed_ms": elapsed_ms})
    return response


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    body = ErrorResponse(detail=str(exc.detail), request_id=get_request_id())
    return JSONResponse(status_code=exc.status_code, content=body.model_dump())


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    detail = (
        exc.errors()[0].get("msg", "Invalid request payload")
        if exc.errors()
        else "Invalid request payload"
    )
    body = ErrorResponse(detail=detail, request_id=get_request_id())
    return JSONResponse(status_code=422, content=body.model_dump())


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("unhandled_exception")
    body = ErrorResponse(detail="Internal server error", request_id=get_request_id())
    return JSONResponse(status_code=500, content=body.model_dump())


app.include_router(router)


@app.get("/health", tags=["health"])
async def health() -> dict:
    return {
        "status": "ok",
        "environment": settings.app_env,
        "llm_provider": settings.llm_provider,
    }
