"""Create a Vapi assistant using the current project prompt and tool definitions."""
import json
import sys

import httpx

from app.core.config import settings
from app.voice_agent.prompts import FIRST_MESSAGE, SYSTEM_PROMPT
from app.voice_agent.tool_definitions import TOOLS


def main() -> None:
    if not settings.vapi_api_key:
        raise SystemExit("VAPI_API_KEY is missing from .env")
    if not settings.public_base_url.startswith("https://"):
        raise SystemExit("PUBLIC_BASE_URL must be a public HTTPS URL before configuring Vapi")

    payload = {
        "name": "Patient Registration Agent",
        "firstMessage": FIRST_MESSAGE,
        "model": {
            "provider": "openai",
            "model": "gpt-4o-mini",
            "temperature": 0.2,
            "messages": [{"role": "system", "content": SYSTEM_PROMPT}],
            "functions": TOOLS,
        },
        "voice": {"provider": "vapi", "voiceId": "Mia"},
        "server": {
            "url": f"{settings.public_base_url.rstrip('/')}/voice/webhook",
            "timeoutSeconds": 20,
        },
        "serverMessages": ["tool-calls", "end-of-call-report", "status-update"],
        "endCallMessage": "Thank you for calling. Goodbye.",
        "silenceTimeoutSeconds": 30,
        "maxDurationSeconds": 900,
    }
    response = httpx.post(
        "https://api.vapi.ai/assistant",
        headers={"Authorization": f"Bearer {settings.vapi_api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=30,
    )
    if response.is_error:
        print(response.text, file=sys.stderr)
        response.raise_for_status()
    assistant = response.json()
    print(json.dumps({"assistant_id": assistant.get("id"), "name": assistant.get("name")}, indent=2))
    print("Attach this assistant to a Vapi phone number in the dashboard.")


if __name__ == "__main__":
    main()
