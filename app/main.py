"""Main FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.api import api_v1_router


def create_application() -> FastAPI:
    """Create FastAPI app with middleware and routes."""

    application = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        version="0.1.0",
        openapi_url=None if settings.ENVIRONMENT == "production" else f"{settings.API_V1_STR}/openapi.json",
        docs_url=None if settings.ENVIRONMENT == "production" else f"{settings.API_V1_STR}/docs",
        redoc_url=None if settings.ENVIRONMENT == "production" else f"{settings.API_V1_STR}/redoc",
    )

    # Set up CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*", "demo-frontend-lac.vercel.app",
                       "https://demo-frontend-lac.vercel.app/", "https://demo-frontend-lac.vercel.app"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(api_v1_router)
    return application


app = create_application()

# Rebuild schemas to resolve forward references
try:
    from app.schemas.repair_request import RepairRequest as RepairRequestSchema
    from app.schemas.service import Service as ServiceSchema
    from app.schemas.user import UserRead

    # This ensures all forward references are resolved
    RepairRequestSchema.model_rebuild()
    ServiceSchema.model_rebuild()
    UserRead.model_rebuild()
except Exception as e:
    print(f"Schema rebuild warning: {e}")


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "version": "0.1.0",
        "docs": f"{settings.API_V1_STR}/docs",
    }
