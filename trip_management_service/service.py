import datetime
import os
import secrets

import requests
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Ride
from schemas import AcceptBookingRequest
from constants import RideStates


class ExternalServiceRequests:
    def __init__(self):
        self.PAYMENTS_DOMAIN = os.getenv("PAYMENTS_DOMAIN", "localhost:8000")

    def start_payment(self, booking_id: int, ride_id: int, driver_id: int):
        payload = {
            "booking_id": booking_id,
            "ride_id": ride_id,
            "driver_id": driver_id,
        }
        r = requests.post(url=f"{self.PAYMENTS_DOMAIN}/pay", data=payload)
        r.raise_for_status()
        print(r.json())


class TripManagementService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.external_client = ExternalServiceRequests()

    def accept_booking(self, request: AcceptBookingRequest):
        otp = secrets.randbits(10)
        ride = Ride(
            otp=otp,
            state=RideStates.ACCEPTED,
            booking_id=request.booking_id,
            driver_id=request.driver_id,
        )
        self.db.add(ride)
        self.db.commit()
        self.db.refresh(ride)
        return ride

    def get_ride_by_id(self, ride_id: int):
        ride = self.db.query(Ride).get(ride_id)
        if ride is None:
            raise HTTPException(status_code=404, detail="Ride not found")
        return ride

    def start_ride(self, ride_id: int) -> Ride:
        ride = self.get_ride_by_id(ride_id=ride_id)
        ride.state = RideStates.STARTED
        self.db.add(ride)
        self.db.commit()
        self.db.refresh(ride)
        return ride

    def complete_ride(self, ride_id: int) -> Ride:
        ride = self.get_ride_by_id(ride_id=ride_id)

        self.external_client.start_payment(
            booking_id=ride.booking_id, ride_id=ride.id, driver_id=ride.driver_id
        )

        ride.state = RideStates.COMPLETED
        ride.completed_at = datetime.datetime.utcnow()
        self.db.add(ride)
        self.db.commit()
        self.db.refresh(ride)
        return ride
