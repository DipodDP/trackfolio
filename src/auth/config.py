# local configs
import uuid

from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    # BearerTransport,
    CookieTransport,
    JWTStrategy,
)

from src.auth.models import User
from src.auth.service import get_user_manager
from src.config import settings

# bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")
cookie_transport = CookieTransport(
    "tracfolio",
    cookie_max_age=3600,
    cookie_secure=False,
)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.auth_key, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    # transport=bearer_transport,
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)


fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
