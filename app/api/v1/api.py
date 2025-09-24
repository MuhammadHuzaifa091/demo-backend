"""API v1 router configuration."""

from fastapi import APIRouter
from app.core.users import fastapi_users
from app.core.security import auth_backend
from app.api.v1.endpoints import test, repair_requests, service_providers, services, auth
from app.schemas.user import UserRead, UserCreate, UserUpdate

api_v1_router = APIRouter(prefix="/api/v1")

# FastAPI-Users routers
api_v1_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"],
)
api_v1_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
api_v1_router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
api_v1_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

# Custom routers
api_v1_router.include_router(test.router, tags=["Test"])
api_v1_router.include_router(auth.router, prefix="/auth", tags=["Custom Auth"])
api_v1_router.include_router(
    repair_requests.router, 
    prefix="/repair-requests", 
    tags=["Repair Requests"]
)
api_v1_router.include_router(
    service_providers.router, 
    prefix="/providers", 
    tags=["Service Providers"]
)
api_v1_router.include_router(
    services.router, 
    prefix="/services", 
    tags=["Services"]
)
