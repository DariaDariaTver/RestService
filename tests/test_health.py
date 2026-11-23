def test_health_check(client):
    response = client.get("/categories")
    assert response.status_code == 200