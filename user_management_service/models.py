from sqlalchemy import Boolean, Column, ForeignKey, Integer, Float, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Numeric

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, unique=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    mobile = Column(String)
    user_type = Column(String)
    balance = Column(Numeric(10, 2))

    driver = relationship("Driver", back_populates="user")

class Driver(Base):
    __tablename__ = "drivers"

    user_id = Column(String, ForeignKey("users.id"),  index=True, primary_key=True)
    acc_no = Column(String, unique=True)
    vehicle_number = Column(String, ForeignKey("vehicles.vehicle_number"),  index=True, unique=True)

    user = relationship("User", back_populates="driver")
    vehicles = relationship("Vehicle", back_populates="driver")

class Vehicle(Base):
    __tablename__ = "vehicles"

    vehicle_number = Column(String, unique=True, index=True, primary_key=True)
    vehicle_type = Column(String)

    driver = relationship("Driver", back_populates="vehicles") 
