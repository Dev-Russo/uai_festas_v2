def test_register_user_success(client):
    # Esse teste valida o fluxo basico de cadastro e o retorno do usuario criado.
    payload = {
        "name": "Auth User",
        "email": "auth@test.com",
        "password": "12345678",
        "role": "producer",
        "is_active": True,
    }
    response = client.post("/auth/register", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == payload["email"]
    assert data["name"] == payload["name"]


def test_login_success(client):
    # Aqui garantimos que um usuario cadastrado consegue autenticar e receber JWT.
    payload = {
        "name": "Login User",
        "email": "login@test.com",
        "password": "12345678",
        "role": "producer",
        "is_active": True,
    }
    client.post("/auth/register", json=payload)

    response = client.post(
        "/auth/login",
        data={"username": payload["email"], "password": payload["password"]},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_invalid_token_returns_401(client):
    # Token invalido deve retornar 401 para rotas protegidas.
    response = client.get("/users/me", headers={"Authorization": "Bearer invalid.token"})

    assert response.status_code == 401
