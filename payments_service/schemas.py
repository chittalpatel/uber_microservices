from datetime import datetime

from pydantic import BaseModel


class PayRideRequest(BaseModel):
    booking_id: int
    ride_id: int
    driver_id: int
