from datetime import datetime


def test_create_sale(client, auth_headers, created_event, created_product):
    # Testa criacao de venda com payload completo e status inicial pago.
    payload = {
        "buyer_name": "Buyer One",
        "buyer_email": "buyer-one@test.com",
        "product_id": created_product["id"],
        "method_of_payment": "credit_card",
        "sale_date": datetime.utcnow().isoformat(),
        "status": "paid",
    }
    response = client.post(f"/events/{created_event['id']}/sales/", json=payload, headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["status"] == "paid"


def test_get_sales_list(client, auth_headers, created_event, created_product, create_sale_helper):
    # Depois de criar uma venda, o endpoint de listagem deve retornar ao menos 1 item.
    create_sale_helper(created_product["id"], "buyer-list@test.com", status="paid")

    response = client.get(f"/events/{created_event['id']}/sales/", headers=auth_headers)

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


def test_get_sale_by_id(client, auth_headers, created_event, created_sale):
    # Busca individual deve encontrar a venda criada no setup.
    response = client.get(f"/events/{created_event['id']}/sales/{created_sale['id']}", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["id"] == created_sale["id"]


def test_cancel_sale_updates_status(client, auth_headers, created_event, created_sale):
    # Cancelamento deve atualizar somente o status para cancelled.
    response = client.patch(f"/events/{created_event['id']}/sales/{created_sale['id']}/cancel", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["status"] == "cancelled"


def test_checkin_sale_registers_timestamp_without_changing_status(client, auth_headers, created_event, created_sale):
    # Novo comportamento: check-in marca horario em checkin_at sem trocar status da venda.
    response = client.patch(f"/events/{created_event['id']}/sales/{created_sale['id']}/check-in", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "paid"
    assert data["checkin_at"] is not None


def test_sales_unique_code_is_uuid_and_unique(client, auth_headers, created_event, created_product, create_sale_helper):
    # Cada venda precisa gerar um unique_code distinto (na pratica, UUID).
    r1 = create_sale_helper(created_product["id"], "buyer-uuid-1@test.com", status="paid")
    r2 = create_sale_helper(created_product["id"], "buyer-uuid-2@test.com", status="paid")

    assert r1.status_code == 200
    assert r2.status_code == 200

    sale1 = r1.json()
    sale2 = r2.json()
    assert sale1["unique_code"]
    assert sale2["unique_code"]
    assert sale1["unique_code"] != sale2["unique_code"]
