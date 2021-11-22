from datetime import datetime
from typing import List

from pydantic import BaseModel


class PayRideRequest(BaseModel):
    booking_id: int
    ride_id: int
    driver_id: int


class Payment(BaseModel):
    created_at: datetime
    status: str
    amount: int
    ride_id: int
    user_id: int

    class Config:
        orm_mode = True
