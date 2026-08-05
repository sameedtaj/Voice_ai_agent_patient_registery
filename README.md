# Voice AI Patient Registration Agent

A voice-based patient intake system that allows callers to register through a natural phone conversation. The agent collects and validates U.S. patient demographics, confirms the information with the caller, persists the record in PostgreSQL, and exposes the stored records through a FastAPI REST API.

> Technical assessment project. Use synthetic demonstration data only. This application is not intended for real clinical use and is not represented as HIPAA-compliant.

## Live Demo

Replace these placeholders after deployment:

- **Phone number:** `[+1(651)386 9157]`
- **API base URL:** `http://localhost:8000/docs`
- **Health check:** `https://angelic-fascination-production-ef1c.up.railway.app/health`
- **Interactive API documentation:** `https://angelic-fascination-production-ef1c.up.railway.app/docs`

## Features

- Natural, LLM-powered patient registration over a real U.S. phone number
- Required demographic collection with optional insurance, language, and emergency-contact details
- Field-specific validation and conversational re-prompts
- Caller corrections, interruptions, and out-of-order responses
- Full read-back and explicit confirmation before saving
- Persistent PostgreSQL storage
- Duplicate detection by phone number with an update option
- REST endpoints to create, list, retrieve, update, and soft-delete patients
- Consistent JSON response envelope and HTTP status codes
- Conversation and final-payload logging
- Automated API and validation tests

## Architecture

```mermaid
flowchart LR
    A[Caller] --> B[Vapi phone number]
    B --> C[Voice AI agent]
    C --> D[Agent tools]
    D --> E[FastAPI]
    E --> F[Service and validation]
    F --> G[(PostgreSQL)]
    E --> H[REST API]
```

### Registration flow

1. A caller dials the Vapi-managed U.S. phone number.
2. The voice agent explains the intake process and collects required fields naturally.
3. Invalid values are re-requested for the specific field without restarting the conversation.
4. The agent offers optional insurance, emergency-contact, and language fields.
5. The agent reads the collected information back to the caller.
6. The caller confirms the information or corrects individual fields.
7. After explicit confirmation, the agent calls the backend patient tool.
8. FastAPI performs independent server-side validation and saves the record in PostgreSQL.
9. The agent reports success or a graceful failure message and ends the call.

The LLM never connects directly to the database. It can only invoke narrowly defined backend tools, while the API remains responsible for validation, business rules, and persistence.

## Technology Stack

| Layer | Technology | Reason |
|---|---|---|
| Telephony and voice | Vapi | Provides phone provisioning, speech recognition, speech synthesis, interruptions, and tool calling |
| Language model | OpenAI | Strong instruction following and structured tool use |
| Backend | FastAPI | Fast development, automatic OpenAPI documentation, and Pydantic validation |
| Database | PostgreSQL | Durable relational persistence and strong schema constraints |
| ORM | SQLAlchemy | Clear persistence layer and database portability |
| Migrations | Alembic | Reproducible schema changes |
| Deployment | Railway | Simple application and managed PostgreSQL deployment |
| Tests | Pytest | Lightweight unit and API integration testing |

## Project Structure

```text
voice-ai-patient-registration/
├── app/
│   ├── api/
│   │   ├── dependencies.py
│   │   └── routes/
│   │       ├── health.py
│   │       ├── patients.py
│   │       └── voice.py
│   ├── core/
│   │   ├── config.py
│   │   ├── exceptions.py
│   │   └── logging.py
│   ├── database/
│   │   ├── base.py
│   │   ├── models.py
│   │   └── session.py
│   ├── repositories/
│   │   └── patient_repository.py
│   ├── schemas/
│   │   ├── common.py
│   │   ├── patient.py
│   │   └── voice.py
│   ├── services/
│   │   ├── patient_service.py
│   │   └── voice_service.py
│   ├── utils/
│   │   ├── constants.py
│   │   └── validators.py
│   ├── voice_agent/
│   │   ├── prompts.py
│   │   ├── tool_definitions.py
│   │   └── tool_handlers.py
│   └── main.py
├── alembic/
│   └── versions/
├── docs/
│   ├── architecture.md
│   └── vapi-setup.md
├── scripts/
│   ├── configure_vapi.py
│   └── seed_patients.py
├── tests/
│   ├── conftest.py
│   ├── test_health.py
│   ├── test_patient_api.py
│   ├── test_patient_validation.py
│   └── test_voice_tools.py
├── .env.example
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── railway.json
├── requirements.txt
└── README.md
```

## Data Collected

Required fields:

- First name and last name
- Date of birth
- Sex
- U.S. phone number
- Address line 1, city, state, and ZIP code

Optional fields:

- Email and address line 2
- Insurance provider and member ID
- Preferred language
- Emergency-contact name and phone number

The database automatically generates `patient_id`, `created_at`, and `updated_at`. Deleting a patient through the API sets `deleted_at`; records are never hard-deleted.

## Prerequisites

- Python 3.11 or later
- PostgreSQL 15 or later, or Docker Desktop
- A Vapi account and phone number
- An OpenAI model provider enabled in the Vapi account
- ngrok for testing Vapi against a local backend

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/voice-ai-patient-registration.git
cd voice-ai-patient-registration
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```bat
python -m venv .venv
.venv\Scripts\activate
```

macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example environment file:

```bash
cp .env.example .env
```

On Windows Command Prompt:

```bat
copy .env.example .env
```

Update `.env` with your credentials:

```env
APP_NAME=Voice AI Patient Registration
APP_ENV=development
DEBUG=true
LOG_LEVEL=INFO

DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/voice_patient_db

VAPI_API_KEY=your_vapi_private_api_key
VAPI_WEBHOOK_SECRET=generate_a_long_random_secret
VAPI_ASSISTANT_ID=
VAPI_PHONE_NUMBER_ID=

PUBLIC_BASE_URL=https://your-ngrok-or-production-domain
```

Never commit `.env` or real credentials to Git.

### 5. Start PostgreSQL

If the repository includes Docker Compose:

```bash
docker compose up -d db
```

Alternatively, create a local database manually:

```sql
CREATE DATABASE voice_patient_db;
```

### 6. Apply database migrations

```bash
alembic upgrade head
```

Optional demonstration records:

```bash
python scripts/seed_patients.py
```

### 7. Start the API

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open:

- API documentation: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`
- Patient list: `http://localhost:8000/patients`

## Vapi Configuration

### 1. Expose the local API

Start ngrok while FastAPI is running:

```bash
ngrok http 8000
```

Copy the HTTPS forwarding URL into `PUBLIC_BASE_URL`, for example:

```env
PUBLIC_BASE_URL=https://example.ngrok-free.app
```

Restart FastAPI after changing the environment file.

### 2. Create the assistant

Create the Vapi assistant using one of these approaches:

```bash
python scripts/configure_vapi.py
```

Or configure it through the Vapi dashboard using the prompt and tools defined in:

```text
app/voice_agent/prompts.py
app/voice_agent/tool_definitions.py
```

### 3. Configure backend URLs

If you create reusable tools in the Vapi dashboard, set each tool's server URL to:

```text
https://YOUR-PUBLIC-DOMAIN/voice/tools
```

Set the event webhook URL to:

```text
https://YOUR-PUBLIC-DOMAIN/voice/webhook
```

The included setup script configures a single assistant server URL at `/voice/webhook`.
That endpoint handles both tool calls and end-of-call reports. `/voice/tools` is retained
for dashboard-created tools and local testing.

Configure the webhook secret in both Vapi and `VAPI_WEBHOOK_SECRET` so the backend can reject unauthorized requests.

### 4. Attach a phone number

Provision or import a U.S. number in Vapi and attach it to the assistant. Add the returned assistant and phone-number IDs to `.env`, then make a test call.

## Voice Agent Behavior

The assistant follows these rules:

- Introduce itself as an automated patient-registration assistant.
- Ask one concise question at a time while accepting information in any order.
- Do not ask again for information already provided.
- Confirm spelling when a name or address is uncertain.
- Normalize spoken phone numbers, dates, state names, and ZIP codes.
- Re-prompt only for an invalid or ambiguous field.
- Accept corrections such as: “Actually, my last name is Davis.”
- Allow the caller to say “start over” before saving.
- Collect required information first, then offer optional information.
- Read back every collected field and require explicit confirmation.
- Never save before confirmation.
- Report database errors gracefully without claiming the record was saved.
- Do not provide medical advice or collect unnecessary sensitive information.

## Voice Agent Tools

| Tool | Purpose |
|---|---|
| `find_patient_by_phone` | Detect a possible existing record before creation |
| `create_patient` | Validate and create a patient after verbal confirmation |
| `update_patient` | Update a confirmed existing patient record |
| `save_call_summary` | Persist call status, transcript summary, and final payload |

## REST API

All successful and failed responses use a consistent envelope:

```json
{
  "data": {},
  "error": null
}
```

For an error:

```json
{
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The supplied phone number is invalid",
    "details": []
  }
}
```

### List patients

```http
GET /patients
```

Supported filters:

```http
GET /patients?last_name=Doe
GET /patients?date_of_birth=1990-05-21
GET /patients?phone_number=2025550147
```

### Retrieve one patient

```http
GET /patients/{patient_id}
```

### Create a patient

```http
POST /patients
Content-Type: application/json
```

Example payload:

```json
{
  "first_name": "Jane",
  "last_name": "Doe",
  "date_of_birth": "1990-05-21",
  "sex": "Female",
  "phone_number": "2025550147",
  "email": "jane.doe@example.com",
  "address_line_1": "1200 Main Street",
  "address_line_2": "Apt 4B",
  "city": "Washington",
  "state": "DC",
  "zip_code": "20001",
  "insurance_provider": "Example Health",
  "insurance_member_id": "EX123456",
  "preferred_language": "English",
  "emergency_contact_name": "John Doe",
  "emergency_contact_phone": "2025550188"
}
```

### Partially update a patient

```http
PUT /patients/{patient_id}
Content-Type: application/json
```

Only supplied fields are changed:

```json
{
  "email": "new.email@example.com",
  "address_line_2": "Suite 500"
}
```

### Soft-delete a patient

```http
DELETE /patients/{patient_id}
```

This sets `deleted_at` in UTC. Deleted records are excluded from ordinary list, lookup, and duplicate-detection operations.

## Validation

Validation is applied at two levels:

1. The voice agent identifies unclear or invalid speech and asks a targeted follow-up question.
2. The FastAPI backend independently validates every request before persistence.

Important rules include:

- Names: 1–50 characters using letters, spaces, hyphens, and apostrophes
- Date of birth: valid date that is not in the future
- Sex: `Male`, `Female`, `Other`, or `Decline to Answer`
- Phone numbers: valid 10-digit U.S. numbers after normalization
- State: valid two-letter U.S. abbreviation
- ZIP code: five digits or ZIP+4
- Email: valid format when supplied
- Optional phone numbers: validated when supplied

## Testing

Run the automated test suite:

```bash
pytest -v
```

Run with coverage:

```bash
pytest --cov=app --cov-report=term-missing
```

Recommended manual call scenarios:

1. Complete a normal registration and retrieve it through `GET /patients`.
2. Call again and verify the first record still exists.
3. Provide a future date of birth and verify a targeted re-prompt.
4. Give a three-digit phone number and then correct it.
5. Spell a last name, then change its spelling before confirmation.
6. Provide several fields out of order.
7. Interrupt the agent while it is speaking.
8. Say “start over” before confirmation.
9. Reject the read-back and correct one field.
10. Register with an existing phone number and choose the update path.
11. Simulate a database failure and verify that the agent does not announce success.
12. End a call mid-registration and verify that no unconfirmed patient is created.

## Docker

Start the API and PostgreSQL together:

```bash
docker compose up --build
```

Apply migrations in the application container if they are not run automatically:

```bash
docker compose exec api alembic upgrade head
```

Stop the services:

```bash
docker compose down
```

Database data is stored in a named Docker volume and survives container restarts.

## Railway Deployment

1. Push the repository to GitHub.
2. Create a Railway project from the GitHub repository.
3. Add a PostgreSQL service.
4. Set `DATABASE_URL` to Railway's PostgreSQL connection string. If necessary, convert the scheme to the SQLAlchemy driver format expected by the application.
5. Add all other environment variables from `.env.example`.
6. Generate a public domain for the API service.
7. Set `PUBLIC_BASE_URL` to that HTTPS domain.
8. Run `alembic upgrade head` as the release or pre-deploy command.
9. Deploy and verify `/health`, `/docs`, and `/patients`.
10. Replace the ngrok URLs in Vapi with the Railway voice-tool and webhook URLs.
11. Call the number and confirm that a record is visible through the deployed API.

Suggested start command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
```

## Observability and Failure Handling

The application emits structured logs for:

- Call lifecycle events
- Voice tool name and call identifier
- Validation failures without exposing secrets
- Final collected payload used for the assessment
- Patient create or update outcome
- Database and webhook failures

Expected failure behavior:

- Invalid data: ask again for the affected field.
- Database failure: apologize, state that registration could not be completed, and avoid a false success message.
- Duplicate phone number: identify the matching record and ask whether to update it.
- Dropped call: retain the call event or summary, but do not create an unconfirmed patient.
- Repeated webhook event: process idempotently where an event or tool-call identifier is available.

Logs must never include API keys. In a real healthcare system, protected health information would require stricter redaction, access controls, encryption, retention policies, audit logging, and compliant vendors.

## Security

- Secrets are loaded from environment variables and excluded from version control.
- Voice webhooks are authenticated using a shared secret or provider signature.
- All external payloads are validated by Pydantic.
- Database access uses parameterized ORM queries.
- The LLM has no direct database or arbitrary HTTP access.
- Patient deletion is soft-delete only.
- CORS should be restricted to approved origins in production.
- Demonstration data must be fictional.

## Design Decisions and Trade-offs

### Vapi instead of custom STT/TTS

Vapi reduces telephony and audio-streaming implementation time and provides interruption handling and tool calling. This allows the assessment to focus on conversation quality, validation, persistence, and integration. The trade-off is vendor dependency and less low-level control.

### PostgreSQL instead of SQLite

PostgreSQL offers durable hosted persistence, constraints, concurrent access, and a straightforward Railway deployment. SQLite would be faster for a purely local demonstration but is less appropriate for a live multi-service deployment.

### REST tools instead of direct LLM database access

Backend tools provide a controlled boundary around validation and persistence. This improves safety, testability, observability, and separation of concerns.

### Confirmation before persistence

Patient creation occurs only after explicit verbal confirmation. This prevents partial or incorrectly transcribed records from being stored.

## Known Limitations

- This assessment implementation is not HIPAA-compliant and must not store real patient information.
- Phone and address validation checks format; it does not prove ownership or deliverability.
- Duplicate detection by phone number can produce false matches for shared household numbers.
- Speech accuracy depends on call quality, accents, names, and provider transcription.
- The initial version supports English; multilingual conversation requires additional prompts, voices, and testing.
- Authentication for general REST API consumers is outside the assessment's core scope.
- Call recovery after a telephony disconnect is limited to logged state unless a resumable session feature is enabled.

## Future Improvements

- Encrypt sensitive fields and introduce role-based API access
- Add production-grade audit logs and PHI redaction
- Add a patient-review dashboard
- Support Spanish and additional languages
- Store recordings or full transcripts with explicit consent
- Add mocked appointment scheduling
- Improve duplicate matching using multiple demographic fields
- Add rate limiting and retry queues for provider outages
- Add contract tests for Vapi webhook payloads
- Add metrics and distributed tracing

## Assessment Coverage

| Evaluation area | Implementation evidence |
|---|---|
| Working system | Live phone number, persistent PostgreSQL data, and REST API |
| Conversational quality | Natural prompt, corrections, interruptions, targeted re-prompts, and confirmation |
| Technical architecture | Separation between telephony, agent tools, service layer, API, and database |
| Code and documentation | Organized modules, migrations, tests, setup instructions, and documented trade-offs |
| Edge cases and resilience | Validation, duplicate detection, dropped-call behavior, graceful database errors, and restart support |

## Submission Checklist

- [ ] Replace the phone-number placeholder
- [ ] Replace the API and repository URL placeholders
- [ ] Confirm the deployed `/health` endpoint returns HTTP 200
- [ ] Confirm `/docs` is accessible to reviewers
- [ ] Complete one full phone registration
- [ ] Retrieve the saved patient through the API
- [ ] Restart or redeploy the service and verify persistence
- [ ] Test correction and invalid-input scenarios
- [ ] Confirm no secret is committed to Git
- [ ] Run the automated tests
- [ ] Add known deployment-specific limitations
- [ ] Send the repository URL, phone number, and API base URL to the reviewer

## Author

**Muhammad Sameed**  
AI Engineer Candidate

## License

This repository is provided for technical-assessment and demonstration purposes. It must not be used to process real patient information.
