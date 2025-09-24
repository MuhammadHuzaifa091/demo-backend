"""Security utilities using FastAPI-Users authentication backend."""

import uuid
from typing import Optional, Dict, Any

from fastapi_users.authentication import (
    JWTStrategy,
    AuthenticationBackend,
    BearerTransport,
)
from fastapi_users.jwt import decode_jwt, generate_jwt

from app.core.config import settings


# Bearer transport defines how tokens are sent by clients (Authorization header)
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


class RoleJWTStrategy(JWTStrategy):
    """Custom JWT strategy that includes user role in token claims."""
    
    async def write_token(self, user) -> str:
        """Generate JWT token with role claims."""
        data = {
            "sub": str(user.id),
            "aud": self.token_audience,
            "role": user.role.value if hasattr(user.role, 'value') else str(user.role),
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
        return generate_jwt(
            data, self.encode_key, self.lifetime_seconds, algorithm=self.algorithm
        )
    
    # Keep the default read_token behavior from parent class


def get_jwt_strategy() -> RoleJWTStrategy:
    """Return the custom JWT strategy with role claims."""
    return RoleJWTStrategy(
        secret=settings.SECRET_KEY,
        lifetime_seconds=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


# The authentication backend used by FastAPI-Users
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
