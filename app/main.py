from contextlib import asynccontextmanager
from app.routers import auth
from app.routers import category
from app.routers import products
from app.routers import admin_products
from app.routers import admin_category
from app.database import engine, Base
from app.config import settings
from fastapi import FastAPI
from app.models import (
    Role, User, Product, Cart, CartItem, 
    Order, OrderStatus, PaymentMethod, Address,
    RefreshToken, Category, OrderItem
    )

@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.DEBUG:
        Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="Restaurant API",
    description="Backend сервис для ресторана",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(auth.router)
app.include_router(category.router)
app.include_router(products.router)
app.include_router(admin_products.router)
app.include_router(admin_category.router)

@app.get("/")
def root():
    return {"message": "Restaurant API работает"}