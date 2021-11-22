import os
import secrets


class Config:
    SECRET = os.getenv("SECRET", secrets.token_urlsafe(16))
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60 * 24 * 7)
    USER_SERVICE = os.getenv("USER_SERVICE")
    BOOKING_SERVICE = os.getenv("BOOKING_SERVICE")
    TRIP_SERVICE = os.getenv("TRIP_SERVICE")
    DRIVER_STATE_SERVICE = os.getenv("DRIVER_STATE_SERVICE")
    PAYMENT_SERVICE = os.getenv("PAYMENT_SERVICE")
