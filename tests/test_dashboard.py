from datetime import datetime


def test_sale_appears_immediately_in_dashboard(client, auth_headers, created_event, created_product):
    # Registra uma venda e valida que o dashboard reflete os numeros imediatamente.
    create_sale_payload = {
        "buyer_name": "Buyer Dashboard",
        "buyer_email": "buyer-dashboard@test.com",
        "product_id": created_product["id"],
        "method_of_payment": "pix",
        "sale_date": datetime.utcnow().isoformat(),
        "status": "paid",
    }
    create_sale_response = client.post(
        f"/events/{created_event['id']}/sales/", json=create_sale_payload, headers=auth_headers
    )
    assert create_sale_response.status_code == 200

    dashboard_response = client.get(f"/events/{created_event['id']}/dashboard/", headers=auth_headers)
    assert dashboard_response.status_code == 200

    data = dashboard_response.json()
    assert data["total_paid_sales"] == 1
    assert data["total_revenue"] == created_product["price"]
    assert data["average_ticket"] == created_product["price"]


def test_cancel_sale_updates_dashboard_totals(client, auth_headers, created_event, created_product):
    # Depois de cancelar a venda, os totais de paid e cancelled devem ser recalculados.
    payload = {
        "buyer_name": "Buyer Cancel",
        "buyer_email": "buyer-cancel@test.com",
        "product_id": created_product["id"],
        "method_of_payment": "pix",
        "sale_date": datetime.utcnow().isoformat(),
        "status": "paid",
    }
    create_sale_response = client.post(f"/events/{created_event['id']}/sales/", json=payload, headers=auth_headers)
    sale = create_sale_response.json()

    cancel_response = client.patch(f"/events/{created_event['id']}/sales/{sale['id']}/cancel", headers=auth_headers)
    assert cancel_response.status_code == 200

    dashboard_response = client.get(f"/events/{created_event['id']}/dashboard/", headers=auth_headers)
    assert dashboard_response.status_code == 200

    data = dashboard_response.json()
    assert data["total_paid_sales"] == 0
    assert data["total_canceled_sales"] == 1


def test_dashboard_returns_all_7_fields_with_valid_types(client, auth_headers, created_event, created_product):
    # Garante o contrato do endpoint: 7 campos obrigatorios e tipos coerentes.
    payload = {
        "buyer_name": "Buyer Fields",
        "buyer_email": "buyer-fields@test.com",
        "product_id": created_product["id"],
        "method_of_payment": "pix",
        "sale_date": datetime.utcnow().isoformat(),
        "status": "paid",
    }
    client.post(f"/events/{created_event['id']}/sales/", json=payload, headers=auth_headers)

    response = client.get(f"/events/{created_event['id']}/dashboard/", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()

    required_fields = {
        "total_paid_sales",
        "total_canceled_sales",
        "total_revenue",
        "average_ticket",
        "sales_by_product",
        "sales_by_day",
        "cancellation_rate",
    }
    assert required_fields.issubset(set(data.keys()))

    assert isinstance(data["total_paid_sales"], int)
    assert isinstance(data["total_canceled_sales"], int)
    assert isinstance(data["total_revenue"], (int, float))
    assert isinstance(data["average_ticket"], (int, float))
    assert isinstance(data["sales_by_product"], list)
    assert isinstance(data["sales_by_day"], list)
    assert isinstance(data["cancellation_rate"], (int, float))
