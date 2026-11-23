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