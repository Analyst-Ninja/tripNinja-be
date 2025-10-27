"""...starting code..."""

from typing import Optional
import logging

from fastapi import FastAPI, APIRouter, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

APP_NAME = "tripNinja"
APP_VERSION = "0.1.0"

logger = logging.getLogger(APP_NAME)


def create_app() -> FastAPI:
    """Create App"""
    app = FastAPI(title=APP_NAME, version=APP_VERSION)

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Simple health endpoint
    @app.get("/health", tags=["health"])
    async def health():
        return {"status": "ok", "app": APP_NAME, "version": APP_VERSION}

    # Root
    @app.get("/", tags=["root"])
    async def root():
        return {"message": f"Welcome to {APP_NAME} API", "version": APP_VERSION}

    # Error handlers
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        logger.warning("HTTPException: %s %s", request.url, exc.detail)
        return JSONResponse({"error": exc.detail}, status_code=exc.status_code)

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.exception("Unhandled exception for request %s", request.url)
        print(request, exc)
        return JSONResponse(
            {"error": "internal_server_error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    # Example router (replace with real routers)
    router = APIRouter(prefix="/api/v1", tags=["api"])

    @router.get("/trips", summary="List trips")
    async def list_trips(limit: Optional[int] = 10):
        # Replace with real DB call / business logic
        sample = [{"id": 1, "name": "Sample Trip"}][:limit]
        return {"items": sample, "count": len(sample)}

    @router.post("/trips", status_code=status.HTTP_201_CREATED, summary="Create trip")
    async def create_trip(payload: dict):
        # Validate and persist payload
        return {"id": 1, "data": payload}

    app.include_router(router)

    return app


trip_app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.app:trip_app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
