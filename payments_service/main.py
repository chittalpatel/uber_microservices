from typing import List

import uvicorn
from fastapi import Depends, FastAPI

import models
from constants import Routes
from database import engine
from schemas import PayRideRequest, Payment
from service import PaymentService

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post(Routes.PAY, response_model=List[Payment])
def start_payment(request: PayRideRequest, svc: PaymentService = Depends()):
    return svc.pay_ride(request=request)


@app.post(Routes.PAYMENT, response_model=Payment)
def complete_payment(payment: int, svc: PaymentService = Depends()):
    return svc.payment_complete(payment_id=payment)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
