def test_register_success(client):
    payload = {
        "email": "daria@mail.ru",
        "password": "daria123123",
        "name": "daria",
        "phone": "+79999999999"
        }
    
    response = client.post("/auth/register", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "daria"
    assert "id" in data
    assert "password" not in data

def test_register_missing_required_field(client):
    payload = {
        "password": "daria123123",
        "name": "daria",
        "phone": "+79999999999"
    }

    response = client.post("auth/register", json=payload)

    assert response.status_code == 422

def test_register_duplicate_email(client):
    payload = {
        "email": "daria@mail.ru",
        "password": "daria123123",
        "name": "daria",
        "phone": "+79999999999"
    }

    response_1 = client.post("/auth/register", json=payload)
    assert response_1.status_code == 201

    payload["phone"] = "+79999999991"
    response_2 = client.post("/auth/register", json=payload)
    assert response_2.status_code == 400

def test_register_invalid_email(client):
    payload = {
        "email": "dariamail.ru",
        "password": "daria123123",
        "name": "daria",
        "phone": "+79999999999"
    }

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 422

def test_login_wrong_password(client):
    client.post("/auth/register", json = {
        "email": "daria@mail.ru",
        "password": "daria123123",
        "name": "daria",
        "phone": "+79999999999"
        })

    response = client.post("/auth/login", json = {
        "email": "daria@mail.ru",
        "password": "daria"
        })

    assert response.status_code == 401

def test_get_me_unauthorized(client):
    response = client.get("/auth/me")
    assert response.status_code == 401

def test_get_me_authorized(client, auth_headers):
    response = client.get("/auth/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test_auth@mail.ru"
    assert data["name"] == "Auth User"
    assert "password" not in data
    assert "pw_hash" not in data
