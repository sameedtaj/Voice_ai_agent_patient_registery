def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"data": {"status": "ok", "database": "connected"}, "error": None}
