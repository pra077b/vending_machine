from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from accounts.managers import AccountManager
from core.utils import get_db
from users.dependencies import get_current_user
from users.models import User


def get_or_create_buyer_account(current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    return AccountManager(db).get_or_create(user=current_user)


