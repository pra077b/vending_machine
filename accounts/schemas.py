from enum import Enum
from typing import Union

from pydantic import BaseModel


class PurchaseSchema(BaseModel):
    product_id: int
    product_count: int


class CoinTypes(Enum):
    five = 5
    ten = 10
    twenty = 20
    fifty = 50
    hundred = 100


class CoinSchema(BaseModel):
    five: int = 0
    ten: int = 0
    twenty: int = 0
    fifty: int = 0
    hundred: int = 0


