from datetime import datetime, timedelta


def test_create_courtesy_sale(client, auth_headers, created_event):
    # Cria um produto com preco 0 (cortesia)
    event_id = created_event["id"]
    payload = {
        "name": "Lote Cortesia",
        "price": 0,
        "start_selling_date": datetime.utcnow().isoformat(),
        "end_selling_date": (datetime.utcnow() + timedelta(days=7)).isoformat(),
    }
    res = client.post(f"/events/{event_id}/products/", json=payload, headers=auth_headers)
    assert res.status_code == 200
    product = res.json()

    # Cria venda para o produto cortesia
    sale_payload = {
        "buyer_name": "Free Buyer",
        "buyer_email": "free@test.com",
        "buyer_cpf": "00000000000",
        "product_id": product["id"],
        "method_of_payment": "pix",
        "sale_date": datetime.utcnow().isoformat(),
        "status": "paid",
    }

    r = client.post(f"/events/{event_id}/sales/", json=sale_payload, headers=auth_headers)
    assert r.status_code == 200
    data = r.json()

    assert data["price"] == 0
    assert data["sale_type"] == "courtesy"
    assert data["buyer_email"] == sale_payload["buyer_email"]
