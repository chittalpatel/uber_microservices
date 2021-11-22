import datetime
import secrets

from sqlalchemy import Column, Integer, String, DateTime

from database import Base


class Ride(Base):
    __tablename__ = "rides"

    id = Column(Integer, primary_key=True, index=True)
    started_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime)
    otp = Column(String, nullable=False)
    state = Column(String, nullable=False)

    # Foreign Keys
    booking_id = Column(Integer, nullable=False, unique=True)
    driver_id = Column(Integer, nullable=False)
