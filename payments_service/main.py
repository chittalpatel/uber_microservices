import json
from typing import List, Tuple

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request, Body
from sqlalchemy.orm import Session

from service import PaymentService
import models
from schemas import PayRideRequest
from database import engine
from constants import Routes
from kafka_producer import Producer


models.Base.metadata.create_all(bind=engine)

producer = Producer()
app = FastAPI()


@app.post(Routes.PAY)
def start_payment(request: PayRideRequest, svc: PaymentService = Depends()):
    payments = svc.pay_ride(request=request)
    for payment in payments:
        payload = {
            "user_id": payment.user_id,
            "amount": payment.amount,
        }
        producer.produce(key=payment.id, value=json.dumps(payload))

    return {"message": "Payments processing started"}


@app.post(Routes.PAYMENT)
def complete_payment(payment: int, svc: PaymentService = Depends()):
    return svc.payment_complete(payment_id=payment)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
