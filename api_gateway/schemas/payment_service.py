from datetime import datetime

from pydantic import BaseModel


class Payment(BaseModel):
    created_at = datetime
    status = str
    amount = int
    ride_id = int
    user_id = int
