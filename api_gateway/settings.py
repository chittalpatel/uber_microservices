import os
import secrets


class Config:
    SECRET = os.getenv("SECRET", secrets.token_urlsafe(16))
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60 * 24 * 7)
