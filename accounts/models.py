from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, Enum
from core.db import Model
import enum


class Account(Model):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey('user.id'))
    balance = Column(Float, default=0)
    last_updated = Column(DateTime)


class Transaction(Model):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True)
    sender = Column(Integer, ForeignKey("user.id"))
    receiver = Column(Integer, ForeignKey("user.id"))
    amount = Column(Float)
    timestamp = Column(DateTime, nullable=False)


