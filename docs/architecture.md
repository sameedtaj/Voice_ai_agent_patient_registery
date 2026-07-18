# Architecture Notes

## Component boundaries

- **Vapi:** phone number, speech recognition, speech synthesis, turn taking, interruption handling, and LLM execution.
- **Voice prompt and tools:** conversation policy and the small set of permitted application actions.
- **FastAPI routes:** HTTP transport, validation-error envelopes, webhook authentication, and REST resources.
- **Services:** duplicate detection, confirmation enforcement, patient workflows, and call logging.
- **Repositories:** SQLAlchemy queries and transactions.
- **PostgreSQL:** durable patient and call-session storage.

## Trust boundaries

The LLM is treated as untrusted input. It cannot access SQL directly. A patient create or update request is validated by Pydantic and is rejected unless `confirmed=true`. Webhook authentication is enabled whenever `VAPI_WEBHOOK_SECRET` is configured.

## Persistence behavior

Patients are stored in PostgreSQL in deployment. SQLite is the zero-configuration local fallback. Deletion is implemented by setting `deleted_at`; ordinary reads exclude soft-deleted rows. Call summaries are stored separately so a disconnected call cannot create a partial patient.

## Failure behavior

- Validation failures return HTTP 422 and field-level details.
- Missing records return HTTP 404.
- Duplicate active phone numbers return HTTP 409.
- Voice-tool exceptions return a safe failure message for the agent to speak.
- Database writes are committed only through repository methods.

## Production hardening beyond this assessment

This demonstration is not HIPAA-compliant. A real deployment would require a formal compliance program, vendor agreements, encryption and key management, strict access controls, audit trails, redaction, retention policies, monitoring, backups, and incident response.
