import pytest
from datetime import datetime, timedelta


# ---------------------------------------------------------------------------
# Fixtures locais
# ---------------------------------------------------------------------------

@pytest.fixture
def commissioner_payload():
    return {
        "username": "comm_joao",
        "name": "Joao Silva",
        "password": "senha1234",
        "role": "commissioner",
        "full_access": False,
        "is_active": True,
    }


@pytest.fixture
def created_commissioner(client, auth_headers, created_event, commissioner_payload):
    event_id = created_event["id"]
    response = client.post(
        f"/events/{event_id}/commissioners/",
        json=commissioner_payload,
        headers=auth_headers,
    )
    assert response.status_code == 201
    return response.json()


@pytest.fixture
def commissioner_auth_headers(client, created_commissioner, commissioner_payload):
    response = client.post(
        "/auth/login",
        data={"username": commissioner_payload["username"], "password": commissioner_payload["password"]},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# ---------------------------------------------------------------------------
# Testes de criação
# ---------------------------------------------------------------------------

def test_create_commissioner_success(client, auth_headers, created_event, commissioner_payload):
    event_id = created_event["id"]
    response = client.post(
        f"/events/{event_id}/commissioners/",
        json=commissioner_payload,
        headers=auth_headers,
    )

    assert response.status_code == 201
    data = response.json()
    assert data["username"] == commissioner_payload["username"]
    assert data["name"] == commissioner_payload["name"]
    assert data["role"] == "commissioner"
    assert data["full_access"] is False
    assert data["is_active"] is True
    assert data["event_id"] == event_id
    assert "hashed_password" not in data


def test_create_commissioner_duplicate_username(client, auth_headers, created_event, created_commissioner, commissioner_payload):
    event_id = created_event["id"]
    response = client.post(
        f"/events/{event_id}/commissioners/",
        json=commissioner_payload,
        headers=auth_headers,
    )

    assert response.status_code == 400
    assert "Username" in response.json()["detail"]


def test_create_commissioner_event_not_found(client, auth_headers, commissioner_payload):
    response = client.post(
        "/events/99999/commissioners/",
        json=commissioner_payload,
        headers=auth_headers,
    )

    assert response.status_code == 404


def test_create_commissioner_unauthorized_user(client, created_event, commissioner_payload):
    # Outro produtor (sem token) não pode criar comissário
    response = client.post(
        f"/events/{created_event['id']}/commissioners/",
        json=commissioner_payload,
    )

    assert response.status_code == 401


def test_create_commissioner_other_owner_forbidden(client, created_event, commissioner_payload):
    # Produtor de outro evento não pode criar comissário no evento alheio
    other_payload = {
        "name": "Other Producer",
        "email": "other@test.com",
        "password": "12345678",
        "role": "producer",
        "is_active": True,
    }
    client.post("/auth/register", json=other_payload)
    login = client.post(
        "/auth/login",
        data={"username": other_payload["email"], "password": other_payload["password"]},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    other_headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

    response = client.post(
        f"/events/{created_event['id']}/commissioners/",
        json=commissioner_payload,
        headers=other_headers,
    )

    assert response.status_code == 403


def test_create_commissioner_admin_role(client, auth_headers, created_event):
    payload = {
        "username": "comm_admin_maria",
        "name": "Maria Admin",
        "password": "senha1234",
        "role": "commissioner_admin",
        "full_access": True,
        "is_active": True,
    }
    response = client.post(
        f"/events/{created_event['id']}/commissioners/",
        json=payload,
        headers=auth_headers,
    )

    assert response.status_code == 201
    data = response.json()
    assert data["role"] == "commissioner_admin"
    assert data["full_access"] is True


# ---------------------------------------------------------------------------
# Testes de listagem e busca
# ---------------------------------------------------------------------------

def test_list_commissioners(client, auth_headers, created_event, created_commissioner):
    event_id = created_event["id"]
    response = client.get(f"/events/{event_id}/commissioners/", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["username"] == created_commissioner["username"]


def test_get_commissioner_by_id(client, auth_headers, created_event, created_commissioner):
    event_id = created_event["id"]
    comm_id = created_commissioner["id"]
    response = client.get(f"/events/{event_id}/commissioners/{comm_id}", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["id"] == comm_id


def test_get_commissioner_not_found(client, auth_headers, created_event):
    event_id = created_event["id"]
    response = client.get(f"/events/{event_id}/commissioners/99999", headers=auth_headers)

    assert response.status_code == 404


# ---------------------------------------------------------------------------
# Testes de atualização
# ---------------------------------------------------------------------------

def test_update_commissioner_name(client, auth_headers, created_event, created_commissioner):
    event_id = created_event["id"]
    comm_id = created_commissioner["id"]
    response = client.patch(
        f"/events/{event_id}/commissioners/{comm_id}",
        json={"name": "Nome Atualizado"},
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Nome Atualizado"


def test_update_commissioner_role_to_admin(client, auth_headers, created_event, created_commissioner):
    event_id = created_event["id"]
    comm_id = created_commissioner["id"]
    response = client.patch(
        f"/events/{event_id}/commissioners/{comm_id}",
        json={"role": "commissioner_admin", "full_access": True},
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["role"] == "commissioner_admin"
    assert data["full_access"] is True


def test_update_commissioner_deactivate(client, auth_headers, created_event, created_commissioner):
    event_id = created_event["id"]
    comm_id = created_commissioner["id"]
    response = client.patch(
        f"/events/{event_id}/commissioners/{comm_id}",
        json={"is_active": False},
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["is_active"] is False


def test_update_commissioner_password(client, auth_headers, created_event, created_commissioner):
    event_id = created_event["id"]
    comm_id = created_commissioner["id"]
    response = client.patch(
        f"/events/{event_id}/commissioners/{comm_id}",
        json={"password": "nova_senha_123"},
        headers=auth_headers,
    )
    assert response.status_code == 200

    # Confirma que consegue logar com a nova senha
    login = client.post(
        "/auth/login",
        data={"username": created_commissioner["username"], "password": "nova_senha_123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert login.status_code == 200


# ---------------------------------------------------------------------------
# Testes de deleção
# ---------------------------------------------------------------------------

def test_delete_commissioner(client, auth_headers, created_event, created_commissioner):
    event_id = created_event["id"]
    comm_id = created_commissioner["id"]
    response = client.delete(f"/events/{event_id}/commissioners/{comm_id}", headers=auth_headers)
    assert response.status_code == 204

    # Confirma que sumiu da listagem
    list_response = client.get(f"/events/{event_id}/commissioners/", headers=auth_headers)
    assert all(c["id"] != comm_id for c in list_response.json())


# ---------------------------------------------------------------------------
# Testes de login do comissário
# ---------------------------------------------------------------------------

def test_commissioner_login_with_username(client, created_commissioner, commissioner_payload):
    response = client.post(
        "/auth/login",
        data={"username": commissioner_payload["username"], "password": commissioner_payload["password"]},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user_type"] == "commissioner"
    assert data["event_id"] == created_commissioner["event_id"]


def test_user_login_returns_user_type(client, producer_user_payload):
    client.post("/auth/register", json=producer_user_payload)
    response = client.post(
        "/auth/login",
        data={"username": producer_user_payload["email"], "password": producer_user_payload["password"]},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 200
    assert response.json()["user_type"] == "user"


def test_commissioner_login_wrong_password(client, created_commissioner, commissioner_payload):
    response = client.post(
        "/auth/login",
        data={"username": commissioner_payload["username"], "password": "senha_errada"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 401


def test_commissioner_login_inactive(client, auth_headers, created_event, created_commissioner, commissioner_payload):
    # Desativa o comissário
    client.patch(
        f"/events/{created_event['id']}/commissioners/{created_commissioner['id']}",
        json={"is_active": False},
        headers=auth_headers,
    )

    response = client.post(
        "/auth/login",
        data={"username": commissioner_payload["username"], "password": commissioner_payload["password"]},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 401


def test_unknown_credentials_return_401(client):
    response = client.post(
        "/auth/login",
        data={"username": "nao_existe", "password": "qualquer"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 401


# ---------------------------------------------------------------------------
# Testes de GET /commissioners/me
# ---------------------------------------------------------------------------

def test_commissioner_get_me(client, created_commissioner, commissioner_auth_headers):
    response = client.get("/commissioners/me", headers=commissioner_auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == created_commissioner["username"]
    assert data["id"] == created_commissioner["id"]


def test_user_token_cannot_access_commissioner_me(client, auth_headers):
    # Token de produtor não é aceito em /commissioners/me
    response = client.get("/commissioners/me", headers=auth_headers)

    assert response.status_code == 401


def test_commissioner_token_cannot_access_users_me(client, commissioner_auth_headers):
    # Token de comissário não é aceito em /users/me
    response = client.get("/users/me", headers=commissioner_auth_headers)

    assert response.status_code == 401
