from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AcceptBookingRequest(BaseModel):
    booking_id: int


class GetOtpResponse(BaseModel):
    otp: int


class Ride(BaseModel):
    id: int
    started_at: datetime
    completed_at: Optional[datetime]
    otp: int
    state: str

    booking_id: int
    driver_id: int

    class Config:
        orm_mode = True
