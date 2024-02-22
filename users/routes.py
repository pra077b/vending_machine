from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.utils import get_db
from users.helpers import create_access_token
from users.models import User
from users.schemas import Token, OAuth2EmailPasswordSchema, UserSignupSchema, UserDetails
from core.settings import api_settings
from users.managers import UserManager

router = APIRouter()


@router.post('/token', response_model=Token)
def login_for_access_token(form_data: Annotated[OAuth2EmailPasswordSchema, Depends()], db: Session = Depends(get_db)):
    user = UserManager(db).authenticate_user(form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=api_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"email": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/signup", description="Signup User")
def signup(signup_user: Annotated[UserSignupSchema, Depends()], db: Session = Depends(get_db)) -> UserDetails:
    user = User(
        email=signup_user.email,
        first_name=signup_user.first_name,
        last_name=signup_user.last_name,
        password=signup_user.password
    )
    user_manager = UserManager(db)
    user_manager.create(user, signup_user.role.value)
    return UserDetails(**user.as_dict())

