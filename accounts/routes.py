from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from accounts.dependencies import get_or_create_buyer_account
from accounts.managers import AccountManager, TransactionManager
from accounts.models import Account
from accounts.schemas import PurchaseSchema, CoinSchema, CoinTypes
from core.utils import get_db
from products.managers import ProductManager
from products.schemas import ProductResponseSchema
from users.dependencies import get_current_user
from users.managers import UserManager
from users.models import User

router = APIRouter()


@router.post("/deposit", description="Deposit Amount")
def deposit(account: Annotated[Account, Depends(get_or_create_buyer_account)], deposit_schema: Annotated[CoinSchema, Depends()], db: Session = Depends(get_db)):
    deposit_schema = deposit_schema.dict()
    total_deposit = sum([deposit_schema[field] * CoinTypes.__getitem__(field).value for field in deposit_schema])
    AccountManager(db).add_amount(account, total_deposit)
    return {
        "deposit": deposit_schema,
        "current_balance": account.balance
    }


@router.post("/reset", description="Reset Amount")
def reset(account: Annotated[Account, Depends(get_or_create_buyer_account)], db: Session = Depends(get_db)):
    AccountManager(db).reset(account)
    return {
        "success": "Account Reset Successfully",
        "balance": account.balance
    }


@router.post("/buy", description="Buy")
def buy(purchase: Annotated[PurchaseSchema, Depends()], buyer: Annotated[User, Depends(get_current_user)], buyer_account: Annotated[Account, Depends(get_or_create_buyer_account)], db: Session = Depends(get_db)):
    product = ProductManager(db).get_by_id(purchase.product_id)
    total_price = purchase.product_count * product.price
    if total_price > buyer_account.balance:
        raise HTTPException(status_code=422, detail="Insufficient Balance")

    seller = UserManager(db).get_by_id(product.seller)
    seller_account = AccountManager(db).get_or_create(seller)
    seller_account.balance += total_price
    buyer_account.balance -= total_price
    db.add(seller_account)
    db.add(buyer_account)
    db.commit()
    TransactionManager(db).create(buyer, seller, total_price)
    return {
        "success": True,
        "purchased_product": ProductResponseSchema(**product.as_dict()),
        "product_quantity": purchase.product_count,
        "spend_amount": total_price,
        "remaining_change": buyer_account.balance,
    }
