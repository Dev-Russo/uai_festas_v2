from datetime import datetime, timedelta


def test_create_event(client, auth_headers):
    # Cria um evento e valida que os dados principais voltam no response.
    payload = {
        "name": "Event Create",
        "description": "desc",
        "status": "Not Realized",
        "event_date": datetime.utcnow().isoformat(),
        "sales_start_date": (datetime.utcnow() - timedelta(days=1)).isoformat(),
    }
    response = client.post("/events/", json=payload, headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["name"] == "Event Create"


def test_get_events_list(client, auth_headers, created_event):
    # Lista de eventos deve retornar ao menos o evento criado pela fixture.
    response = client.get("/events/", headers=auth_headers)

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


def test_get_event_by_id(client, auth_headers, created_event):
    # Busca de evento por id deve retornar exatamente o evento esperado.
    event_id = created_event["id"]
    response = client.get(f"/events/{event_id}", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["id"] == event_id


def test_update_event(client, auth_headers, created_event):
    # Atualizacao parcial: alteramos apenas o nome e confirmamos persistencia.
    event_id = created_event["id"]
    payload = {"name": "Event Updated"}
    response = client.put(f"/events/{event_id}", json=payload, headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["name"] == "Event Updated"


def test_delete_event(client, auth_headers, created_event):
    # Delecao deve funcionar para o dono do evento autenticado.
    event_id = created_event["id"]
    response = client.delete(f"/events/{event_id}", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["id"] == event_id
