from core.managers import BaseManager
from users.models import User
from .models import Product, Category


class ProductManager(BaseManager):
    model = Product

    def get_by_name(self, name: str):
        return self.db.query(self.model).filter(self.model.name == name).first()

    def create(self, name: str, price: float, category_id: int, seller: User):
        category = CategoryManager(self.db).get_by_id(category_id)
        product = self.model(
            category=category.id,
            name=name,
            price=price,
            seller=seller.id,
        )
        self.db.add(product)
        self.db.commit()
        return product


class CategoryManager(BaseManager):
    model = Category

    def get_by_name(self, name: str):
        return self.db.query(self.model).filter(self.model.name == name).first()

    def create(self, name: str, description: str):
        category = self.model(
            name=name,
            description=description
        )
        self.db.add(category)
        self.db.commit()
        return category
