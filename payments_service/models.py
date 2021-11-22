import datetime
import secrets

from sqlalchemy import Column, Integer, String, DateTime

from database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    status = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)

    ride_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
