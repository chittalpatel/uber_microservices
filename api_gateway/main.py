import requests
from fastapi import Depends, FastAPI, HTTPException, Request, Body
from fastapi.security import OAuth2PasswordRequestForm

from security import create_access_token, authenticated_user
from constants import Routes

router = FastAPI(title="Uber Backend")


@router.post(Routes.LOGIN)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    pass
