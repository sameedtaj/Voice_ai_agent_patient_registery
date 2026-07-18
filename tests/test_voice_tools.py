def tool_request(name, parameters, tool_id="tool-1"):
    return {
        "message": {
            "type": "tool-calls",
            "call": {"id": "call-1"},
            "toolCallList": [{"id": tool_id, "name": name, "parameters": parameters}],
        }
    }


def tool_result(response):
    import json

    return json.loads(response.json()["results"][0]["result"])


def test_voice_agent_cannot_save_without_confirmation(client, patient_payload):
    payload = {**patient_payload, "confirmed": False}
    response = client.post("/voice/tools", json=tool_request("create_patient", payload))
    assert response.status_code == 200
    result = tool_result(response)
    assert result["success"] is False
    assert client.get("/patients").json()["data"] == []


def test_voice_create_then_duplicate_lookup(client, patient_payload):
    create_payload = {**patient_payload, "confirmed": True}
    created_response = client.post(
        "/voice/tools", json=tool_request("create_patient", create_payload)
    )
    created = tool_result(created_response)
    assert created["success"] is True

    lookup_response = client.post(
        "/voice/tools",
        json=tool_request("find_patient_by_phone", {"phone_number": "2025550147"}, "tool-2"),
    )
    lookup = tool_result(lookup_response)
    assert lookup["found"] is True
    assert lookup["patient"]["first_name"] == "Jane"


def test_vapi_legacy_tool_shape_is_supported(client):
    body = {
        "message": {
            "type": "tool-calls",
            "call": {"id": "call-2"},
            "toolWithToolCallList": [
                {
                    "name": "find_patient_by_phone",
                    "toolCall": {"id": "legacy-1", "parameters": {"phone_number": "2025550199"}},
                }
            ],
        }
    }
    response = client.post("/voice/webhook", json=body)
    assert response.status_code == 200
    assert tool_result(response)["found"] is False
