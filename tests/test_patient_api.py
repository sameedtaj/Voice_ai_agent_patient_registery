def test_patient_crud_and_soft_delete(client, patient_payload):
    created = client.post("/patients", json=patient_payload)
    assert created.status_code == 201
    record = created.json()["data"]
    patient_id = record["patient_id"]
    assert record["phone_number"] == "2025550147"
    assert record["state"] == "DC"

    listed = client.get("/patients", params={"last_name": "Doe"})
    assert listed.status_code == 200
    assert len(listed.json()["data"]) == 1

    fetched = client.get(f"/patients/{patient_id}")
    assert fetched.status_code == 200
    assert fetched.json()["data"]["first_name"] == "Jane"

    updated = client.put(f"/patients/{patient_id}", json={"email": "new@example.com"})
    assert updated.status_code == 200
    assert updated.json()["data"]["email"] == "new@example.com"

    deleted = client.delete(f"/patients/{patient_id}")
    assert deleted.status_code == 200
    assert deleted.json()["data"]["deleted"] is True
    assert client.get(f"/patients/{patient_id}").status_code == 404
    assert client.get("/patients").json()["data"] == []


def test_duplicate_phone_returns_conflict(client, patient_payload):
    assert client.post("/patients", json=patient_payload).status_code == 201
    patient_payload["first_name"] = "Janet"
    response = client.post("/patients", json=patient_payload)
    assert response.status_code == 409
    assert response.json()["error"]["code"] == "CONFLICT"


def test_invalid_payload_has_consistent_envelope(client, patient_payload):
    patient_payload["phone_number"] = "123"
    response = client.post("/patients", json=patient_payload)
    assert response.status_code == 422
    body = response.json()
    assert body["data"] is None
    assert body["error"]["code"] == "VALIDATION_ERROR"
