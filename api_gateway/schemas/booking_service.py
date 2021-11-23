from datetime import datetime

from pydantic import BaseModel


class CreateBookingRequest(BaseModel):
    pickup_location: str
    drop_location: str
    vehicle_type: str


class Booking(CreateBookingRequest):
    passenger_id: int
    cost: int
    est: int
    created_at: datetime
    state: str


class DriverStateRequest(BaseModel):
    latitude: float
    longitude: float
    state: str
    vehicle_type: str

