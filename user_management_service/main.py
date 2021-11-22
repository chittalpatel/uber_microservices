from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm.session import Session
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
    name: str
    email: str
    password: str
    mobile: str
    user_type: str

class LoginStruct(BaseModel):
    mobile: str
    password: str

class DriverStruct(BaseModel):
    user_id: int
    acc_no: str
    vehicle_number: str
    vehicle_type: str


app = FastAPI()



@app.get("/")
def read_root():
    return {"Service": "User Management"}

@app.post("/register")
def create_user(userInfo: RegStruct, db: Session = Depends(get_db)):
    user = User()
    if db.query(User).filter_by(id=userInfo.id).first() is not None:
        return {"Error: " : "user id "+userInfo.id+" already in use", "Status": False}

    elif db.query(User).filter_by(email=userInfo.email).first() is not None:
        return {"Error: " : "email "+ userInfo.email+" already in use", "Status": False}

    try:
        user.id = userInfo.id
        user.name = userInfo.name
        user.email = userInfo.email
        user.password = userInfo.password
        user.user_type = userInfo.user_type
        user.balance = userInfo.balance
        
        db.add(user)
        db.commit()

    except Exception as e:
        return {"Exception": e}

    return {"Message:" : "user "+user.name+" Created", "Status": True}


@app.post("/login")
def login(userInfo: LoginStruct, db: Session = Depends(get_db)):
    if db.query(User).filter_by(id=userInfo.id).first() is not None and db.query(User).filter_by(id=userInfo.id).first().password == userInfo.password:
        return {"Status": True}
    else:
        return {"Status": False}


@app.delete("/delete/{user_id}")
def delete(user_id, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)

    if user:
        db.delete(user)
        db.commit()
        db.close()
    else:
        return {"Message": "user with id "+user_id+" not found", "Status": False}

    return {"Message": "user with id "+user_id+" deleted", "Status": True}


@app.get("/profile/{user_id}")
def getProfile(user_id, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)

    if user:
        user_dict = {}
        user_dict['id'] = user.id
        user_dict['name'] = user.name
        user_dict['email'] = user.email
        user_dict['password'] = user.password
        user_dict['user_type'] = user.user_type
        user_dict['balance'] = user.balance
        return {"content" : user_dict, "Status": True}
    
    return {"Message": "user with id "+user_id+" not found", "Status": False}


@app.post("/add_driver")
def add_driver(driverInfo: DriverStruct, db: Session = Depends(get_db)):
    if db.query(User).filter_by(id=driverInfo.user_id).first() is not None:
        if db.query(Driver).filter_by(user_id=driverInfo.user_id).first() is None:
            if db.query(User).filter_by(id=driverInfo.user_id).first().user_type == 'driver':
                if db.query(Vehicle).filter_by(vehicle_number=driverInfo.vehicle_number).first() is None:
                    driver = Driver()
                    vehicle = Vehicle()
                    vehicle.vehicle_number = driverInfo.vehicle_number
                    vehicle.vehicle_type = driverInfo.vehicle_type
                    driver.user_id = driverInfo.user_id
                    driver.acc_no = driverInfo.acc_no
                    driver.vehicle_number = driverInfo.vehicle_number
                    db.add(driver)
                    db.add(vehicle)
                    db.commit()
                    db.close()
                    return {"Message": "Driver added", "Status": True}
                
                else:
                    return {"Message": "Vehicle already exists in database", "Status": False}
            else:
                return {"Message": "The user with id "+driverInfo.user_id+" is not a driver", "Status": False}
        else:
                return {"Message": "The driver with id "+driverInfo.user_id+" already exists", "Status": False}
    else:
        return {"Message": "The user with id "+driverInfo.user_id+" does not exist in database", "Status": False}
    

