import datetime
import os
import secrets

import requests
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Payment
from schemas import PayRideRequest
from constants import PaymentStatus


class ExternalServiceClients:
    def __init__(self):
        self.user_service = os.getenv("USER_SERVICE")
        self.booking_service = os.getenv("BOOKING_SERVICE")

    def send_payment(self, user_id: int, amount: int, payment_id: int):
        r = requests.post(url=f"{self.user_service}/user/{user_id}/process-payment", json={"amount": amount, "payment_id": payment_id})
        try:
            r.raise_for_status()
        except:
            raise HTTPException(r.status_code)
        return r.json()

    def get_booking(self, booking_id: int):
        r = requests.get(url=f"{self.booking_service}/booking?booking_id={booking_id}")
        try:
            r.raise_for_status()
        except:
            raise HTTPException(r.status_code)
        return r.json()


class PaymentService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.external_client = ExternalServiceClients()

    def pay_ride(self, request: PayRideRequest):
        booking = self.external_client.get_booking(booking_id=request.booking_id)

        passenger_payment = Payment(
            amount=-int(booking["cost"]),
            ride_id=request.ride_id,
            user_id=int(booking["passenger_id"]),
            status=PaymentStatus.INITIATED,
        )
        driver_payment = Payment(
            amount=int(booking["cost"]),
            ride_id=request.ride_id,
            user_id=request.driver_id,
            status=PaymentStatus.INITIATED,
        )

        self.db.add_all([passenger_payment, driver_payment])
        self.db.commit()
        self.external_client.send_payment(user_id=passenger_payment.user_id, amount=passenger_payment.amount,
                                          payment_id=passenger_payment.id)
        self.external_client.send_payment(user_id=driver_payment.user_id, amount=driver_payment.amount,
                                          payment_id=driver_payment.id)
        self.db.refresh(passenger_payment)
        self.db.refresh(driver_payment)
        return [passenger_payment, driver_payment]

    def payment_complete(self, payment_id: int):
        payment = self.db.query(Payment).get(payment_id)
        if payment is None:
            raise HTTPException(404, "Payment not found")

        payment.status = PaymentStatus.COMPLETED
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        return payment
