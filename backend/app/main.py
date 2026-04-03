from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routes_health import router as health_router
from app.api.routes_workflows import router as workflows_router
from app.core.config import get_settings
from app.core.exceptions import WorkflowError
from app.core.logging import configure_logging
from app.db.sqlite import init_db

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    configure_logging()
    init_db()
    yield


app = FastAPI(title=settings.app_name, version="0.2.0", lifespan=lifespan)


@app.exception_handler(WorkflowError)
def workflow_error_handler(_: Request, exc: WorkflowError) -> JSONResponse:
    return JSONResponse(status_code=400, content={"status": "error", "message": str(exc)})


app.include_router(health_router)
app.include_router(workflows_router, prefix=settings.api_prefix)
