import requests
from fastapi import HTTPException

from schemas.booking_service import CreateBookingRequest, DriverStateRequest
from settings import Config
from schemas.user_service import LoginStruct, RegStruct, DriverStruct
from schemas.trip_service import AcceptBookingRequest, Ride, GetOtpResponse


class InternalClient:
    def __init__(self):
        self.user_domain = Config.USER_SERVICE
        self.booking_domain = Config.BOOKING_SERVICE
        self.trip_domain = Config.TRIP_SERVICE
        self.driver_state_domain = Config.DRIVER_STATE_SERVICE
        self.payment_domain = Config.PAYMENT_SERVICE

    @classmethod
    def get_request(cls, url: str):
        r = requests.get(url=url)
        try:
            r.raise_for_status()
        except:
            raise HTTPException(r.status_code)
        return r.json()

    @classmethod
    def post_request(cls, url: str, data: dict = None):
        r = requests.post(url=url, json=data)
        try:
            r.raise_for_status()
        except:
            raise HTTPException(r.status_code)
        return r.json()

    def login(self, _request: LoginStruct):
        return self.post_request(url=f"{self.user_domain}/login", data=_request.dict())

    def register(self, _request: RegStruct):
        return self.post_request(url=f"{self.user_domain}/register", data=_request.dict())

    def delete_user(self, user_id: int):
        return self.post_request(url=f"{self.user_domain}/delete/{user_id}")

    def get_user(self, user_id: int):
        return self.get_request(url=f"{self.user_domain}/profile/{user_id}")

    def add_driver(self, user_id: int, _request: DriverStruct):
        return self.post_request(url=f"{self.user_domain}/add-driver/{user_id}", data=_request.dict())

    def accept_booking(self, user_id: int, _request: AcceptBookingRequest):
        data = _request.dict()
        data["driver_id"] = user_id
        return self.post_request(url=f"{self.trip_domain}/ride", data=data)

    def get_otp(self, ride_id: int, user_id: int):
        return self.get_request(url=f"{self.trip_domain}/ride/{ride_id}/otp")

    def start_ride(self, ride_id: int, user_id: int):
        return self.post_request(f"{self.trip_domain}/ride/{ride_id}/start")

    def complete_ride(self, ride_id: int, user_id: int):
        return self.post_request(f"{self.trip_domain}/ride/{ride_id}/complete")

    def get_latest_user_booking(self, user_id: int):
        return self.get_request(f"{self.booking_domain}/booking?passenger_id={user_id}")

    def get_booking_by_id(self, booking_id: int, user_id: int):
        return self.get_request(f"{self.booking_domain}/booking?booking_id={booking_id}")

    def create_booking(self, _request: CreateBookingRequest, user_id: int):
        return self.post_request(f"{self.booking_domain}/booking?passenger_id={user_id}&pickup_location={_request.pickup_location}&drop_location={_request.drop_location}&vehicle_type={_request.vehicle_type}")

    def set_driver_state(self, _request: DriverStateRequest, user_id: int):
        data = _request.dict()
        data["driver_id"] = user_id
        return self.post_request(f"{self.driver_state_domain}/changestate", data=data)


