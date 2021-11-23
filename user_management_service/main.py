import os
from typing import Optional
import decimal

import requests
import uvicorn as uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.sqltypes import String
import models
from database import engine, SessionLocal
from pydantic import BaseModel
from models import User, Driver, Vehicle

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class RegStruct(BaseModel):
    name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    mobile: Optional[str]
    user_type: Optional[str]

class LoginStruct(BaseModel):
    mobile: str
    password: str

class DriverStruct(BaseModel):
    acc_no: str
    vehicle_number: str
    vehicle_type: str


class ProcessPaymentRequest(BaseModel):
    payment_id: int
    amount: int


app = FastAPI()



@app.get("/")
def read_root():
    return {"Service": "User Management"}

@app.post("/register")
def create_user(userInfo: RegStruct, db: Session = Depends(get_db)):
    user = User()
    if db.query(User).filter_by(mobile=userInfo.mobile).first() is not None:
        return HTTPException(status_code=403, detail="mobile number already in use")

    elif db.query(User).filter_by(email=userInfo.email).first() is not None:
        return HTTPException(status_code=403, detail="email already in use")

    try:
        user.name = userInfo.name
        user.email = userInfo.email
        user.password = userInfo.password
        user.user_type = userInfo.user_type
        user.mobile = userInfo.mobile
        user.balance = 0
        
        db.add(user)
        db.commit()

    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

    return {"Message:" : "user "+user.name+" Created", "Status": True}


@app.post("/login")
def login(userInfo: LoginStruct, db: Session = Depends(get_db)):
    print(userInfo.dict())
    user: User = db.query(User).filter_by(mobile=userInfo.mobile).first()
    print(user.mobile, user.password)
    if user is not None and user.password == userInfo.password:
        return {"Status": True, "user_id": user.id, "mobile": userInfo.mobile, "user_type": user.user_type}
    else:
        return HTTPException(status_code=401, detail="invalid credentials")


@app.post("/delete/{user_id}")
def delete(user_id, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)

    if user:
        if user.user_type == 'driver':
            driver = db.query(Driver).get(user_id)
            vehicle = db.query(Vehicle).get(driver.vehicle_number)
            db.delete(vehicle)
            db.delete(driver)
        db.delete(user)
        db.commit()
        #db.close()
    else:
        return HTTPException(status_code=404, detail="user not found")

    return {"Message": "user deleted", "Status": True}


@app.get("/profile/{user_id}")
def getProfile(user_id, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)

    if user:
        user_dict = {}
        user_dict['id'] = user.id
        user_dict['name'] = user.name
        user_dict['email'] = user.email
        user_dict['user_type'] = user.user_type
        user_dict['balance'] = user.balance
        return {"content" : user_dict, "Status": True}
    
    return HTTPException(status_code=404, detail="user not found")


@app.post("/add-driver/{user_id}")
def add_driver(driverInfo: DriverStruct, user_id: int, db: Session = Depends(get_db)):
    if db.query(User).filter_by(id=user_id).first() is not None:
        if db.query(Driver).filter_by(acc_no=driverInfo.acc_no).first() is None:
            if db.query(Driver).filter_by(user_id=user_id).first() is None:
                if db.query(User).filter_by(id=user_id).first().user_type == 'driver':
                    if db.query(Vehicle).filter_by(vehicle_number=driverInfo.vehicle_number).first() is None:
                        driver = Driver()
                        vehicle = Vehicle()
                        vehicle.vehicle_number = driverInfo.vehicle_number
                        vehicle.vehicle_type = driverInfo.vehicle_type
                        driver.user_id = user_id
                        driver.acc_no = driverInfo.acc_no
                        driver.vehicle_number = driverInfo.vehicle_number
                        db.add(driver)
                        db.add(vehicle)
                        db.commit()
                        #db.close()
                        return {"Message": "Driver added", "Status": True}
                    
                    else:
                        return HTTPException(status_code=403, detail="vehicle already exixts")
                else:
                    return HTTPException(status_code=404, detail="user is not a driver")
            else:
                return HTTPException(status_code=403, detail="driver already exixts")
        else:
            return HTTPException(status_code=403, detail="account no already registered")
    else:
        return HTTPException(status_code=404, detail="user does not exist")


@app.post("/update-user/{user_id}")
def update_user(user_id: int, userInfo: RegStruct, db: Session = Depends(get_db)):
    user_dict = userInfo.dict(exclude_unset=True)
    user = db.query(User).get(user_id)
    

    for key in user_dict:
        if key == "balance":
            user.balance += decimal.Decimal(user_dict[key])

        elif key == "name":
            user.name = userInfo.name
        
        elif key == "mobile":
            if db.query(User).filter_by(mobile=user_dict[key]).first() is not None:
                return HTTPException(status_code=403, detail="mobile number already in use")
            user.mobile = userInfo.mobile

        elif key == "email":
            if db.query(User).filter_by(email=user_dict[key]).first() is not None:
                return HTTPException(status_code=403, detail="email number already in use")
            user.email = userInfo.email

        elif key == "password":
            user.password = userInfo.password

        elif key == "user_type":
            if user.user_type == 'driver' & user_dict[key] == 'passenger':
                delete_driver(user.id)
            user.user_type = userInfo.user_type


        else:
            print(user[key])
            user[key] = user_dict[key]

    db.commit()
    return {"Message": "User updated", "Status": True}    


@app.post("/delete-driver/{user_id}")
def delete_driver(user_id: int, db: Session = Depends(get_db)):
    
    driver = db.query(Driver).get(user_id)

    if driver != null:
        vehicle = db.query(Vehicle).get(driver.vehicle_number)
        db.delete(vehicle)
        db.delete(driver)
        db.commit()
        return {"Message": "Driver and vehicle deleted", "Status": True}   

    else:
         return {"Message": "No driver entry found", "Status": False} 


@app.post("/user/{user_id}/process-payment")
def process_payment(user_id: int, _request: ProcessPaymentRequest, db: Session = Depends(get_db)):
    user: User = db.query(User).get(user_id)
    if user is None:
        raise HTTPException(404, "User doesn't not exist")
    user.balance += _request.amount
    db.add(user)
    db.commit()
    db.refresh(user)
    r = requests.post(f"{os.getenv('PAYMENT_SERVICE')}/payment/{_request.payment_id}")
    try:
        r.raise_for_status()
    except:
        raise HTTPException(status_code=r.status_code)
    return user


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")


