import pytest
from datetime import datetime, timedelta


# ---------------------------------------------------------------------------
# Fixtures locais
# ---------------------------------------------------------------------------

@pytest.fixture
def product_a(client, auth_headers, created_event):
    r = client.post(
        f"/events/{created_event['id']}/products/",
        json={
            "name": "Lote Pista",
            "price": 100,
            "start_selling_date": datetime.utcnow().isoformat(),
            "end_selling_date": (datetime.utcnow() + timedelta(days=7)).isoformat(),
        },
        headers=auth_headers,
    )
    assert r.status_code == 200
    return r.json()


@pytest.fixture
def product_b(client, auth_headers, created_event):
    r = client.post(
        f"/events/{created_event['id']}/products/",
        json={
            "name": "Lote VIP",
            "price": 300,
            "start_selling_date": datetime.utcnow().isoformat(),
            "end_selling_date": (datetime.utcnow() + timedelta(days=7)).isoformat(),
        },
        headers=auth_headers,
    )
    assert r.status_code == 200
    return r.json()


@pytest.fixture
def created_group(client, auth_headers, created_event):
    r = client.post(
        f"/events/{created_event['id']}/product-groups/",
        json={"name": "Grupo Geral"},
        headers=auth_headers,
    )
    assert r.status_code == 201
    return r.json()


@pytest.fixture
def full_access_headers(client, auth_headers, created_event):
    """Commissioner admin com full_access no mesmo evento."""
    client.post(
        f"/events/{created_event['id']}/commissioners/",
        json={
            "username": "comm_full",
            "name": "Full Comm",
            "password": "senha1234",
            "role": "commissioner_admin",
            "full_access": True,
            "is_active": True,
        },
        headers=auth_headers,
    )
    login = client.post(
        "/auth/login",
        data={"username": "comm_full", "password": "senha1234"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


@pytest.fixture
def limited_headers(client, auth_headers, created_event):
    """Commissioner comum sem full_access."""
    client.post(
        f"/events/{created_event['id']}/commissioners/",
        json={
            "username": "comm_limited",
            "name": "Limited Comm",
            "password": "senha1234",
            "role": "commissioner",
            "full_access": False,
            "is_active": True,
        },
        headers=auth_headers,
    )
    login = client.post(
        "/auth/login",
        data={"username": "comm_limited", "password": "senha1234"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


# ---------------------------------------------------------------------------
# Criação de grupos
# ---------------------------------------------------------------------------

def test_create_group_success(client, auth_headers, created_event):
    r = client.post(
        f"/events/{created_event['id']}/product-groups/",
        json={"name": "Grupo VIP"},
        headers=auth_headers,
    )
    assert r.status_code == 201
    data = r.json()
    assert data["name"] == "Grupo VIP"
    assert data["is_default"] is False
    assert data["is_active"] is True
    assert data["event_id"] == created_event["id"]
    assert data["parent_group_id"] is None
    assert data["children"] == []
    assert data["memberships"] == []


def test_create_default_group(client, auth_headers, created_event):
    r = client.post(
        f"/events/{created_event['id']}/product-groups/",
        json={"name": "Padrao", "is_default": True},
        headers=auth_headers,
    )
    assert r.status_code == 201
    assert r.json()["is_default"] is True


def test_only_one_default_per_event(client, auth_headers, created_event):
    eid = created_event["id"]
    client.post(f"/events/{eid}/product-groups/", json={"name": "D1", "is_default": True}, headers=auth_headers)
    r = client.post(f"/events/{eid}/product-groups/", json={"name": "D2", "is_default": True}, headers=auth_headers)
    assert r.status_code == 400


def test_create_child_group(client, auth_headers, created_event, created_group):
    r = client.post(
        f"/events/{created_event['id']}/product-groups/",
        json={"name": "Subgrupo", "parent_group_id": created_group["id"]},
        headers=auth_headers,
    )
    assert r.status_code == 201
    assert r.json()["parent_group_id"] == created_group["id"]


def test_create_child_invalid_parent(client, auth_headers, created_event):
    r = client.post(
        f"/events/{created_event['id']}/product-groups/",
        json={"name": "X", "parent_group_id": 99999},
        headers=auth_headers,
    )
    assert r.status_code == 404


def test_create_group_unauthenticated(client, created_event):
    r = client.post(f"/events/{created_event['id']}/product-groups/", json={"name": "X"})
    assert r.status_code == 401


# ---------------------------------------------------------------------------
# Listagem e busca
# ---------------------------------------------------------------------------

def test_list_returns_only_roots(client, auth_headers, created_event, created_group):
    eid = created_event["id"]
    client.post(
        f"/events/{eid}/product-groups/",
        json={"name": "Filho", "parent_group_id": created_group["id"]},
        headers=auth_headers,
    )
    r = client.get(f"/events/{eid}/product-groups/", headers=auth_headers)
    assert r.status_code == 200
    groups = r.json()
    assert all(g["parent_group_id"] is None for g in groups)


def test_list_children_nested_in_parent(client, auth_headers, created_event, created_group):
    eid = created_event["id"]
    client.post(
        f"/events/{eid}/product-groups/",
        json={"name": "Filho", "parent_group_id": created_group["id"]},
        headers=auth_headers,
    )
    groups = client.get(f"/events/{eid}/product-groups/", headers=auth_headers).json()
    root = next(g for g in groups if g["id"] == created_group["id"])
    assert len(root["children"]) == 1
    assert root["children"][0]["name"] == "Filho"


def test_get_group_by_id(client, auth_headers, created_event, created_group):
    r = client.get(
        f"/events/{created_event['id']}/product-groups/{created_group['id']}",
        headers=auth_headers,
    )
    assert r.status_code == 200
    assert r.json()["id"] == created_group["id"]


def test_get_group_not_found(client, auth_headers, created_event):
    r = client.get(f"/events/{created_event['id']}/product-groups/99999", headers=auth_headers)
    assert r.status_code == 404


# ---------------------------------------------------------------------------
# Atualização
# ---------------------------------------------------------------------------

def test_update_group_name(client, auth_headers, created_event, created_group):
    r = client.patch(
        f"/events/{created_event['id']}/product-groups/{created_group['id']}",
        json={"name": "Atualizado"},
        headers=auth_headers,
    )
    assert r.status_code == 200
    assert r.json()["name"] == "Atualizado"


def test_update_group_deactivate(client, auth_headers, created_event, created_group):
    r = client.patch(
        f"/events/{created_event['id']}/product-groups/{created_group['id']}",
        json={"is_active": False},
        headers=auth_headers,
    )
    assert r.status_code == 200
    assert r.json()["is_active"] is False


def test_update_set_default_conflict(client, auth_headers, created_event):
    eid = created_event["id"]
    client.post(f"/events/{eid}/product-groups/", json={"name": "Default", "is_default": True}, headers=auth_headers)
    outro = client.post(f"/events/{eid}/product-groups/", json={"name": "Outro"}, headers=auth_headers).json()
    r = client.patch(
        f"/events/{eid}/product-groups/{outro['id']}",
        json={"is_default": True},
        headers=auth_headers,
    )
    assert r.status_code == 400


# ---------------------------------------------------------------------------
# Deleção
# ---------------------------------------------------------------------------

def test_delete_group(client, auth_headers, created_event, created_group):
    eid = created_event["id"]
    r = client.delete(f"/events/{eid}/product-groups/{created_group['id']}", headers=auth_headers)
    assert r.status_code == 204
    assert client.get(f"/events/{eid}/product-groups/{created_group['id']}", headers=auth_headers).status_code == 404


def test_delete_group_with_children_fails(client, auth_headers, created_event, created_group):
    eid = created_event["id"]
    client.post(
        f"/events/{eid}/product-groups/",
        json={"name": "Filho", "parent_group_id": created_group["id"]},
        headers=auth_headers,
    )
    r = client.delete(f"/events/{eid}/product-groups/{created_group['id']}", headers=auth_headers)
    assert r.status_code == 400


# ---------------------------------------------------------------------------
# Membership produto <-> grupo
# ---------------------------------------------------------------------------

def test_add_product_to_group(client, auth_headers, created_event, created_group, product_a):
    eid = created_event["id"]
    r = client.post(
        f"/events/{eid}/product-groups/{created_group['id']}/products",
        params={"product_id": product_a["id"]},
        headers=auth_headers,
    )
    assert r.status_code == 201
    data = r.json()
    assert data["product_id"] == product_a["id"]
    assert data["group_id"] == created_group["id"]
    assert data["is_active"] is True
    assert data["product"]["name"] == product_a["name"]


def test_add_same_product_twice_fails(client, auth_headers, created_event, created_group, product_a):
    eid = created_event["id"]
    client.post(f"/events/{eid}/product-groups/{created_group['id']}/products", params={"product_id": product_a["id"]}, headers=auth_headers)
    r = client.post(f"/events/{eid}/product-groups/{created_group['id']}/products", params={"product_id": product_a["id"]}, headers=auth_headers)
    assert r.status_code == 400


def test_add_product_not_in_event_fails(client, auth_headers, created_event, created_group):
    r = client.post(
        f"/events/{created_event['id']}/product-groups/{created_group['id']}/products",
        params={"product_id": 99999},
        headers=auth_headers,
    )
    assert r.status_code == 404


def test_toggle_product_inactive(client, auth_headers, created_event, created_group, product_a):
    eid = created_event["id"]
    client.post(f"/events/{eid}/product-groups/{created_group['id']}/products", params={"product_id": product_a["id"]}, headers=auth_headers)
    r = client.patch(
        f"/events/{eid}/product-groups/{created_group['id']}/products/{product_a['id']}",
        json={"is_active": False},
        headers=auth_headers,
    )
    assert r.status_code == 200
    assert r.json()["is_active"] is False


def test_toggle_product_back_active(client, auth_headers, created_event, created_group, product_a):
    eid = created_event["id"]
    client.post(f"/events/{eid}/product-groups/{created_group['id']}/products", params={"product_id": product_a["id"]}, headers=auth_headers)
    client.patch(f"/events/{eid}/product-groups/{created_group['id']}/products/{product_a['id']}", json={"is_active": False}, headers=auth_headers)
    r = client.patch(
        f"/events/{eid}/product-groups/{created_group['id']}/products/{product_a['id']}",
        json={"is_active": True},
        headers=auth_headers,
    )
    assert r.status_code == 200
    assert r.json()["is_active"] is True


def test_toggle_product_not_in_group_fails(client, auth_headers, created_event, created_group, product_a):
    r = client.patch(
        f"/events/{created_event['id']}/product-groups/{created_group['id']}/products/{product_a['id']}",
        json={"is_active": False},
        headers=auth_headers,
    )
    assert r.status_code == 404


def test_remove_product_from_group(client, auth_headers, created_event, created_group, product_a):
    eid = created_event["id"]
    client.post(f"/events/{eid}/product-groups/{created_group['id']}/products", params={"product_id": product_a["id"]}, headers=auth_headers)
    r = client.delete(f"/events/{eid}/product-groups/{created_group['id']}/products/{product_a['id']}", headers=auth_headers)
    assert r.status_code == 204
    group = client.get(f"/events/{eid}/product-groups/{created_group['id']}", headers=auth_headers).json()
    assert not any(m["product_id"] == product_a["id"] for m in group["memberships"])


def test_memberships_visible_in_list(client, auth_headers, created_event, created_group, product_a, product_b):
    eid = created_event["id"]
    client.post(f"/events/{eid}/product-groups/{created_group['id']}/products", params={"product_id": product_a["id"]}, headers=auth_headers)
    client.post(f"/events/{eid}/product-groups/{created_group['id']}/products", params={"product_id": product_b["id"]}, headers=auth_headers)
    groups = client.get(f"/events/{eid}/product-groups/", headers=auth_headers).json()
    group = next(g for g in groups if g["id"] == created_group["id"])
    assert len(group["memberships"]) == 2


# ---------------------------------------------------------------------------
# Permissões: commissioner full_access vs limitado
# ---------------------------------------------------------------------------

def test_full_access_can_create_group(client, full_access_headers, created_event):
    r = client.post(
        f"/events/{created_event['id']}/product-groups/",
        json={"name": "Grupo Comm Admin"},
        headers=full_access_headers,
    )
    assert r.status_code == 201


def test_full_access_can_add_product(client, full_access_headers, created_event, created_group, product_a):
    r = client.post(
        f"/events/{created_event['id']}/product-groups/{created_group['id']}/products",
        params={"product_id": product_a["id"]},
        headers=full_access_headers,
    )
    assert r.status_code == 201


def test_full_access_can_toggle_product(client, full_access_headers, auth_headers, created_event, created_group, product_a):
    eid = created_event["id"]
    client.post(f"/events/{eid}/product-groups/{created_group['id']}/products", params={"product_id": product_a["id"]}, headers=auth_headers)
    r = client.patch(
        f"/events/{eid}/product-groups/{created_group['id']}/products/{product_a['id']}",
        json={"is_active": False},
        headers=full_access_headers,
    )
    assert r.status_code == 200
    assert r.json()["is_active"] is False


def test_limited_commissioner_blocked(client, limited_headers, created_event):
    r = client.post(
        f"/events/{created_event['id']}/product-groups/",
        json={"name": "Bloqueado"},
        headers=limited_headers,
    )
    assert r.status_code == 403


def test_full_access_wrong_event_denied(client, auth_headers, created_event):
    """Comissário full_access de outro evento não acessa grupos deste evento."""
    other = {"name": "Other", "email": "cross@test.com", "password": "12345678", "role": "producer", "is_active": True}
    client.post("/auth/register", json=other)
    other_login = client.post(
        "/auth/login",
        data={"username": other["email"], "password": other["password"]},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    other_h = {"Authorization": f"Bearer {other_login.json()['access_token']}"}
    other_ev = client.post(
        "/events/",
        json={"name": "Ev2", "description": "x", "status": "Not Realized",
              "event_date": datetime.utcnow().isoformat(),
              "sales_start_date": datetime.utcnow().isoformat()},
        headers=other_h,
    ).json()
    client.post(
        f"/events/{other_ev['id']}/commissioners/",
        json={"username": "comm_cross", "name": "Cross", "password": "senha1234",
              "role": "commissioner_admin", "full_access": True, "is_active": True},
        headers=other_h,
    )
    cross_login = client.post(
        "/auth/login",
        data={"username": "comm_cross", "password": "senha1234"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    cross_h = {"Authorization": f"Bearer {cross_login.json()['access_token']}"}

    r = client.post(
        f"/events/{created_event['id']}/product-groups/",
        json={"name": "Invasao"},
        headers=cross_h,
    )
    assert r.status_code == 403
