from core.managers import BaseManager
from users.models import User
from .models import Account, Transaction
from datetime import datetime


class AccountManager(BaseManager):
    model = Account

    def get_or_create(self, user: User):
        account = self.db.query(self.model).filter(self.model.user == user.id).first()
        if account:
            return account
        account = self.model(
            user=user.id,
            balance=0,
            last_updated=datetime.now()
        )
        self.db.add(account)
        self.db.commit()
        return account

    def add_amount(self, account: Account, amount: int):
        account.balance = account.balance + amount
        self.db.add(account)
        self.db.commit()

    def reset(self, account: Account):
        account.balance = 0
        self.db.add(account)
        self.db.commit()


class TransactionManager(BaseManager):
    model = Transaction

    def create(self, sender: User, receiver: User, amount):
        transaction = self.model(
            sender=sender.id,
            receiver=receiver.id,
            amount=amount,
            timestamp=datetime.now()
        )
        self.db.add(transaction)
        self.db.commit()
        return transaction
