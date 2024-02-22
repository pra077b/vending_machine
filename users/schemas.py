from enum import Enum
from typing import Union, Annotated

from fastapi import Form
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, EmailStr, field_validator, ValidationError
from typing_extensions import Doc

from core.db import db_context
from users.managers import UserManager


class Roles(Enum):
    seller = "seller"
    buyer = "buyer"


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None


class UserDetails(BaseModel):
    email: str = None
    first_name: str = None
    last_name: str = None
    roles: Union[list, None] = None


class UserSignupSchema(BaseModel):
    email: Union[EmailStr, None] = None
    first_name: str
    last_name: str
    password: str
    role: Roles = Roles.buyer

    @field_validator("email")
    def validate_email(cls, email: str):
        with db_context() as db:
            if UserManager(db).get_by_email(email):
                raise RequestValidationError(
                    errors=["Email already exists"],
                )
        return email


class OAuth2EmailPasswordSchema:
    def __init__(
            self,
            *,
            email: Annotated[
                str,
                Form(),
                Doc(
                    """
                    `username` string. The OAuth2 spec requires the exact field name
                    `username`.
                    """
                ),
            ],
            password: Annotated[
                str,
                Form(),
                Doc(
                    """
                    `password` string. The OAuth2 spec requires the exact field name
                    `password".
                    """
                ),
            ],
    ):
        self.email = email
        self.password = password

