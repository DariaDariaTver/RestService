import pytest
from typing import Annotated, Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker, Session

from app.main import app
from app.database import Base, get_db

from app.models.category import Category
from app.models.user import User
from app.models.category import Category
from app.models.product import Product
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.order_status import OrderStatus
from app.models.role import Role
from app.models.payment_method import PaymentMethod
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.address import Address

engine = create_engine("sqlite://",
                       connect_args={"check_same_thread": False},
                       poolclass=StaticPool)

TestingSessionLocal = sessionmaker(autocommit=False,
                                   autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    user_role = Role(name="user")
    db.add(user_role)
    db.commit()
    try:
        yield db
    finally:
        db.close()
    Base.metadata.drop_all(bind=engine)
    
@pytest.fixture(scope="function")
def client(
    db_session: Annotated[Session, pytest.fixture]) -> Generator[TestClient, None, None]:
        def override_get_db():
            try:
                yield db_session
            finally:
                pass
        app.dependency_overrides[get_db] = override_get_db
        with TestClient(app) as c:
            yield c
        app.dependency_overrides.clear()
@pytest.fixture(scope="function")
def auth_headers(client: TestClient) -> dict:
    payload = {
        "email": "test_auth@mail.ru",
        "password": "testtest123",
        "name": "Auth User",
        "phone": "+79998887766"
    }
    client.post("/auth/register", json=payload)
    login_resp = client.post("/auth/login", json={
        "email": payload["email"],
        "password": payload["password"]
    })
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}