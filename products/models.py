from sqlalchemy import Column, Integer, String, Float, ForeignKey
from core.db import Model


class Category(Model):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String)


class Product(Model):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    category = Column(Integer, ForeignKey('category.id'))
    seller = Column(Integer, ForeignKey("user.id"))

