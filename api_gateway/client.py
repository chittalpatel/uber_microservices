import requests

from settings import Config
from schemas.user_service import LoginStruct, RegStruct, DriverStruct
from schemas.trip_service import AcceptBookingRequest, Ride, GetOtpResponse

from requests import request


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
        r.raise_for_status()
        return r.json()

    @classmethod
    def post_request(cls, url: str, data: dict = None):
        r = requests.post(url=url, data=data)
        r.raise_for_status()
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


