from users.routes import router as users_router
from accounts.routes import router as accounts_router
from products.routes import router as products_router
from fastapi import FastAPI


def setup_router(app: FastAPI):
    app.include_router(
        users_router,
        prefix="/user",
        tags=["User"]
    )
    app.include_router(
        accounts_router,
        prefix="/account",
        tags=["Account"]
    )
    app.include_router(
        products_router,
        prefix="/product",
        tags=["Product"]
    )

