from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.utils import get_db
from products.schemas import ProductSchema, CategorySchema, CategoryResponseSchema, ProductResponseSchema
from products.managers import ProductManager, CategoryManager
from users.dependencies import get_current_seller
from users.models import User

router = APIRouter()


@router.get("", description="Get Products")
def get_products(db: Session = Depends(get_db)):
    return [product.as_dict() for product in ProductManager(db).get_all()]


@router.post("", description="Create Product")
def create_product(current_seller: Annotated[User, Depends(get_current_seller)], product: Annotated[ProductSchema, Depends()], db: Session = Depends(get_db)):
    product = ProductManager(db).create(
        name=product.name,
        price=product.price,
        category_id=product.category_id,
        seller=current_seller
    )
    return ProductResponseSchema(**product.as_dict())


@router.get("/category", description="Get Categories")
def get_categories(db: Session = Depends(get_db)):
    return [category.as_dict() for category in CategoryManager(db).get_all()]


@router.post("/category", description="Create Category")
def create_product_category(current_seller: Annotated[User, Depends(get_current_seller)], category: Annotated[CategorySchema, Depends()], db: Session = Depends(get_db)):
    category = CategoryManager(db).create(
        name=category.name,
        description=category.description
    )
    return CategoryResponseSchema(**category.as_dict())

