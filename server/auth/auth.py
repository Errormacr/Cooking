from fastapi_users.authentication import CookieTransport, AuthenticationBackend, JWTStrategy
from config import SECRET

cookie_transport = CookieTransport(cookie_name="Cook", cookie_max_age=1209600, cookie_samesite="None")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=1209600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
