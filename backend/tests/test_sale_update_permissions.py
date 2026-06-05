from datetime import datetime


def test_producer_owner_can_update_buyer_fields(client, auth_headers, created_event, created_product, create_sale_helper):
    # Cria uma venda e o produtor (auth_headers) deve ser capaz de atualizar dados do comprador
    event_id = created_event["id"]
    prod = created_product
    r = create_sale_helper(prod["id"], "buyer-update@test.com", status="paid")
    assert r.status_code == 200
    sale = r.json()

    update_payload = {
        "buyer_name": "Updated Buyer",
        "buyer_email": "updated@test.com",
        "buyer_cpf": "99999999999",
    }

    res = client.put(f"/events/{event_id}/sales/{sale['id']}", json=update_payload, headers=auth_headers)
    assert res.status_code == 200
    updated = res.json()

    assert updated["buyer_name"] == update_payload["buyer_name"]
    assert updated["buyer_email"] == update_payload["buyer_email"]
    # Audit field should record who edited (producer@test.com per conftest fixture)
    assert updated.get("last_edited_by") == "producer@test.com"
