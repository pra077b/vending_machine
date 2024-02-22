from typing import Union

from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, field_validator

from core.db import db_context
from products.managers import CategoryManager, ProductManager
from users.managers import UserManager


class ProductSchema(BaseModel):
    name: str
    price: float
    category_id: int

    @field_validator("name")
    def validate_nane(cls, name: str):
        with db_context() as db:
            if ProductManager(db).get_by_name(name):
                raise RequestValidationError(
                    errors=["Product with given name already exists"],
                )
        return name


class ProductResponseSchema(BaseModel):
    name: str
    price: float
    category: int


class CategorySchema(BaseModel):
    name: str
    description: Union[str, None] = None

    @field_validator("name")
    def validate_nane(cls, name: str):
        with db_context() as db:
            if CategoryManager(db).get_by_name(name):
                raise RequestValidationError(
                    errors=["Category already exists"],
                )
        return name


class CategoryResponseSchema(BaseModel):
    name: str
    description: Union[str, None] = None
