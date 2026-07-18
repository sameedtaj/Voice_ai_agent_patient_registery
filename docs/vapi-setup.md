# Vapi Setup

## Fastest dashboard path

1. Run FastAPI locally and expose port 8000 with ngrok.
2. Create a bearer-token custom credential in Vapi. Use the same value as `VAPI_WEBHOOK_SECRET`.
3. Create an assistant and copy the system prompt from `app/voice_agent/prompts.py`.
4. Set its first message from `FIRST_MESSAGE` in the same file.
5. Select OpenAI `gpt-4o-mini`, low temperature, and a natural English voice.
6. Create three function tools using the schemas in `app/voice_agent/tool_definitions.py`.
7. Set the tool server URL to `https://YOUR-DOMAIN/voice/tools` and attach the bearer credential.
8. Set the assistant event server URL to `https://YOUR-DOMAIN/voice/webhook` and attach the same credential.
9. Enable at least `tool-calls` and `end-of-call-report` server messages.
10. Provision a U.S. number and attach the assistant.

## Script path

After setting `VAPI_API_KEY` and a public HTTPS `PUBLIC_BASE_URL`, run:

```bash
python scripts/configure_vapi.py
```

The command prints the created assistant ID. Attach that assistant to a phone number from the Vapi dashboard. For production, add a Vapi custom bearer credential to the assistant server configuration.

## Required call tests

- Normal registration
- Invalid future date of birth
- Invalid phone number followed by correction
- Spelled-name correction
- Fields provided out of order
- Rejected read-back followed by a correction
- Duplicate phone lookup and update
- Caller says “start over”
- Call drops before confirmation
- Simulated backend write failure
