import datetime
import secrets

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Payment
from schemas import PayRideRequest
from constants import PaymentStatus


class ExternalServiceClients:
    pass


class PaymentService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def pay_ride(self, request: PayRideRequest):
        passenger_id = 123
        amount = 100

        passenger_payment = Payment(
            amount=-amount,
            ride_id=request.ride_id,
            user_id=passenger_id,
            status=PaymentStatus.INITIATED,
        )
        driver_payment = Payment(
            amount=amount,
            ride_id=request.ride_id,
            user_id=request.driver_id,
            status=PaymentStatus.INITIATED,
        )

        self.db.add_all([passenger_payment, driver_payment])
        self.db.commit()
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
