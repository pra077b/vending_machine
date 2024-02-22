from sqlalchemy import Column, Integer, String, DateTime, Table, ForeignKey
from core.db import Model, Base
from datetime import datetime
from sqlalchemy.orm import relationship


user_role_association = Table(
    'user_role',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('role.id')),
    Column('user_id', Integer, ForeignKey('user.id'))
)


class Role(Model):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True)
    role = Column(String, unique=True)
    users = relationship('User', secondary=user_role_association, back_populates="roles")


class User(Model):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created = Column(DateTime, default=datetime.utcnow())
    roles = relationship('Role', secondary=user_role_association, back_populates="users")

