from typing import List

import requests
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request, Body
from fastapi.security import OAuth2PasswordRequestForm

from client import InternalClient
from schemas.booking_service import CreateBookingRequest, DriverStateRequest
from schemas.trip_service import AcceptBookingRequest, Ride, GetOtpResponse
from schemas.user_service import LoginStruct, RegStruct, DriverStruct, AuthTokenResponse
from security import create_access_token, authenticated_user
from constants import Routes

router = FastAPI(title="Uber Backend")
client = InternalClient()


#######################################################################
# User Management Service
#######################################################################

@router.post(Routes.LOGIN, response_model=AuthTokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    request = LoginStruct(mobile=form_data.username, password=form_data.password)
    user = client.login(request)
    token = create_access_token(user_id=user["user_id"], username=user["mobile"], user_type=user["user_type"])
    return AuthTokenResponse(access_token=token, token_type="bearer")


@router.get(Routes.USER)
def profile(user: dict = Depends(authenticated_user)):
    return client.get_user(user_id=user["id"])


@router.post(Routes.USER)
def register_user(request: RegStruct):
    return client.register(request)


@router.delete(Routes.USER)
def delete_user(user: dict = Depends(authenticated_user)):
    return client.delete_user(user_id=user["id"])


@router.post(Routes.DRIVER)
def add_driver_profile(request: DriverStruct, user: dict = Depends(authenticated_user)):
    return client.add_driver(user_id=user["id"], _request=request)


#######################################################################
# Booking Service
#######################################################################


@router.get(Routes.BOOK)
def get_latest_booking(user: dict = Depends(authenticated_user)):
    return client.get_latest_user_booking(user_id=user["id"])


@router.get(Routes.BOOK + "/{booking}")
def get_booking(booking: int, user: dict = Depends(authenticated_user)):
    return client.get_booking_by_id(booking_id=booking, user_id=user["id"])


@router.post(Routes.SEARCH_RIDE)
def search_drivers(request: CreateBookingRequest, user: dict = Depends(authenticated_user)):
    return client.create_booking(_request=request, user_id=user["id"])


#######################################################################
# Driver State Service
#######################################################################


@router.post(Routes.SET_DRIVER_STATE)
def set_driver_state(request: DriverStateRequest, user: dict = Depends(authenticated_user)):
    return client.set_driver_state(_request=request, user_id=user["id"])


#######################################################################
# Trip Management Service
#######################################################################


@router.post(Routes.RIDE, response_model=Ride)
def accept_booking(
    request: AcceptBookingRequest, user: dict = Depends(authenticated_user)
):
    return client.accept_booking(user_id=user["id"], _request=request)


@router.get(Routes.RIDE_OTP, response_model=GetOtpResponse)
def get_ride_otp(ride: int, user: dict = Depends(authenticated_user)):
    return client.get_otp(ride_id=ride, user_id=user["id"])


@router.post(Routes.RIDE_START, response_model=Ride)
def start_ride(ride: int, user: dict = Depends(authenticated_user)):
    return client.start_ride(ride_id=ride, user_id=user["id"])


@router.post(Routes.RIDE_COMPLETE, response_model=Ride)
def complete_ride(ride: int, user: dict = Depends(authenticated_user)):
    return client.complete_ride(ride_id=ride, user_id=user["id"])


#######################################################################
# Payment Service is currently for internal use only
#######################################################################


if __name__ == "__main__":
    uvicorn.run(router, host="0.0.0.0", port=8000, log_level="info")

