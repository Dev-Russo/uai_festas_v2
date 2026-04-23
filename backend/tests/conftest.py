import os
from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Ensure required settings exist before app import.
os.environ.setdefault("DATABASE_URL", "sqlite://")
os.environ.setdefault("SECRET_KEY", "test-secret")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
os.environ.setdefault("ALGORITHM", "HS256")

from database import Base
from dependencies.db import get_db
from main import app
from models.event import Event
from models.products import Product
from models.sales import Sales


@compiles(UUID, "sqlite")
def _compile_uuid_sqlite(_type, _compiler, **_kwargs):
    return "CHAR(36)"


SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def setup_db():
    # Cada teste roda com banco limpo para evitar dependencia entre cenarios.
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    # Override da dependencia do FastAPI para usar a sessao SQLite de teste.
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def producer_user_payload():
    return {
        "name": "Producer Test",
        "email": "producer@test.com",
        "password": "12345678",
        "role": "producer",
        "is_active": True,
    }


@pytest.fixture
def auth_headers(client, producer_user_payload):
    # Fixture reutilizavel: registra e autentica um produtor, retornando Bearer token.
    client.post("/auth/register", json=producer_user_payload)
    response = client.post(
        "/auth/login",
        data={"username": producer_user_payload["email"], "password": producer_user_payload["password"]},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def created_event(client, auth_headers):
    # Cria um evento padrao para ser reutilizado nos testes de produto, venda e dashboard.
    payload = {
        "name": "Evento Teste",
        "description": "Teste",
        "status": "Not Realized",
        "event_date": datetime.utcnow().isoformat(),
        "sales_start_date": (datetime.utcnow() - timedelta(days=1)).isoformat(),
    }
    response = client.post("/events/", json=payload, headers=auth_headers)
    assert response.status_code == 200
    return response.json()


@pytest.fixture
def created_product(client, auth_headers, created_event):
    # Cria um produto associado ao evento padrao.
    event_id = created_event["id"]
    payload = {
        "name": "Lote 1",
        "price": 150,
        "start_selling_date": datetime.utcnow().isoformat(),
        "end_selling_date": (datetime.utcnow() + timedelta(days=7)).isoformat(),
    }
    response = client.post(f"/events/{event_id}/products/", json=payload, headers=auth_headers)
    assert response.status_code == 200
    return response.json()


@pytest.fixture
def create_sale_helper(client, auth_headers, created_event):
    # Factory fixture para criar vendas com variacoes de email/status sem repetir codigo.
    def _create_sale(product_id: int, buyer_email: str, status: str = "paid"):
        payload = {
            "buyer_name": "Buyer",
            "buyer_email": buyer_email,
            "product_id": product_id,
            "method_of_payment": "pix",
            "sale_date": datetime.utcnow().isoformat(),
            "status": status,
        }
        response = client.post(f"/events/{created_event['id']}/sales/", json=payload, headers=auth_headers)
        return response

    return _create_sale


@pytest.fixture
def created_sale(client, auth_headers, created_event, created_product, create_sale_helper):
    # Venda base usada por testes que precisam de um registro existente.
    response = create_sale_helper(created_product["id"], "buyer1@test.com", status="paid")
    assert response.status_code == 200
    return response.json()
