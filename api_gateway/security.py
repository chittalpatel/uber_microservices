from datetime import timedelta, datetime

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from constants import Routes
from settings import Config

oauth_token = OAuth2PasswordBearer(tokenUrl=Routes.LOGIN)


def create_access_token(user_id: int, username: str, user_type: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "exp": expire,
        "sub": username,
        "user_id": user_id,
        "user_type": user_type,
    }
    encoded_jwt = jwt.encode(to_encode, Config.SECRET, algorithm=Config.JWT_ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    try:
        token = jwt.decode(token, Config.SECRET, algorithms=Config.JWT_ALGORITHM)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token"
        )

    if datetime.now().timestamp() > token.get("exp"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token expired"
        )
    return token


def authenticated_user(token: str = Depends(oauth_token)):
    token_payload = decode_access_token(token=token)
    return {
        "id": token_payload["user_id"],
    }
