from typing import Union
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer
from jose import jwt

from core.settings import api_settings


oauth2_scheme = HTTPBearer()


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, api_settings.SECRET_KEY, algorithm=api_settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    return jwt.decode(token, api_settings.SECRET_KEY, algorithms=[api_settings.ALGORITHM])
