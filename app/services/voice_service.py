import json
import logging
from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from app.database.models import CallSession
from app.schemas.patient import PatientCreate, PatientRead, PatientUpdate
from app.services.patient_service import PatientService

logger = logging.getLogger(__name__)


class VoiceService:
    def __init__(self, db: Session):
        self.db = db
        self.patients = PatientService(db)

    def run_tool(self, name: str, parameters: dict[str, Any], call_id: str | None = None) -> dict:
        logger.info("voice_tool name=%s call_id=%s", name, call_id)
        if name == "find_patient_by_phone":
            patient = self.patients.find_by_phone(parameters["phone_number"])
            return {
                "found": patient is not None,
                "patient": PatientRead.model_validate(patient).model_dump(mode="json") if patient else None,
            }
        if name == "create_patient":
            if parameters.pop("confirmed", False) is not True:
                return {"success": False, "message": "Caller confirmation is required before saving."}
            patient = self.patients.create(PatientCreate.model_validate(parameters))
            logger.info("patient_created patient_id=%s final_payload=%s", patient.patient_id, json.dumps(parameters))
            return {
                "success": True,
                "message": f"Registration saved for {patient.first_name} {patient.last_name}.",
                "patient": PatientRead.model_validate(patient).model_dump(mode="json"),
            }
        if name == "update_patient":
            patient_id = UUID(str(parameters.pop("patient_id")))
            if parameters.pop("confirmed", False) is not True:
                return {"success": False, "message": "Caller confirmation is required before updating."}
            patient = self.patients.update(patient_id, PatientUpdate.model_validate(parameters))
            return {
                "success": True,
                "message": f"Record updated for {patient.first_name} {patient.last_name}.",
                "patient": PatientRead.model_validate(patient).model_dump(mode="json"),
            }
        if name == "save_call_summary":
            return self.save_call_summary(parameters, call_id)
        return {"success": False, "message": f"Unknown tool: {name}"}

    def save_call_summary(self, parameters: dict[str, Any], fallback_call_id: str | None) -> dict:
        call_id = str(parameters.get("call_id") or fallback_call_id or "unknown")
        session = self.db.get(CallSession, call_id) or CallSession(call_id=call_id)
        session.caller_phone = parameters.get("caller_phone")
        session.status = parameters.get("status", "ended")
        session.transcript = parameters.get("transcript")
        payload = parameters.get("collected_payload")
        session.collected_payload = json.dumps(payload) if payload is not None else None
        session.ended_at = datetime.now(timezone.utc)
        self.db.add(session)
        self.db.commit()
        return {"success": True, "message": "Call summary saved."}
