from pydantic import BaseModel


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
    acc_no: str
    vehicle_number: str
    vehicle_type: str
