import json
from typing import List, Tuple

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request, Body
from sqlalchemy.orm import Session

from service import TripManagementService
import models
from schemas import AcceptBookingRequest, GetOtpResponse, Ride
from database import engine
from constants import Routes


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post(Routes.RIDE, response_model=Ride)
def accept_booking(
    request: AcceptBookingRequest, svc: TripManagementService = Depends()
):
    return svc.accept_booking(request=request)


@app.get(Routes.RIDE_OTP, response_model=GetOtpResponse)
def get_otp(ride: int, svc: TripManagementService = Depends()):
    return svc.get_ride_by_id(ride_id=ride)


@app.post(Routes.RIDE_START, response_model=Ride)
def start_ride(ride: int, svc: TripManagementService = Depends()):
    return svc.start_ride(ride_id=ride)


@app.post(Routes.RIDE_COMPLETE, response_model=Ride)
def complete_ride(ride: int, svc: TripManagementService = Depends()):
    return svc.complete_ride(ride_id=ride)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
