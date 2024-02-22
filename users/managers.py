from sqlalchemy.exc import IntegrityError

from core.exceptions import UserAlreadyExists
from core.managers import BaseManager
from .models import User, Role
from passlib.context import CryptContext


class RoleManager(BaseManager):
    model = Role

    def get_role(self, role: str):
        return self.db.query(self.model).filter(self.model.role == role).first()

    def create(self, role: str):
        role = self.model(
            role=role
        )
        self.db.add(role)
        self.db.commit()


class UserManager(BaseManager):
    model = User
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def is_admin(self, user: User):
        role = RoleManager(self.db).get_role('admin')
        return role in user.roles

    def is_seller(self, user):
        role = RoleManager(self.db).get_role('seller')
        return role in user.roles

    def get_by_email(self, email):
        return self.db.query(self.model).filter(self.model.email == email).first()

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str):
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def get_password_hash(cls, password):
        return cls.pwd_context.hash(password)

    def authenticate_user(self, email: str, password: str):
        user = self.get_by_email(email)
        if not user:
            return False
        if not self.verify_password(password, user.password):
            return False
        return user

    def create(self, user: User, role: str):
        try:
            role = RoleManager(self.db).get_role(role)
            role.users.append(user)
            user.password = self.get_password_hash(user.password)
            self.db.add(user)
            self.db.add(role)
            self.db.commit()
        except IntegrityError as e:
            raise UserAlreadyExists
        return user
