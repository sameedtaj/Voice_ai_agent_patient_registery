from datetime import date
from uuid import UUID

from fastapi import APIRouter, Query, status

from app.api.dependencies import DbSession
from app.schemas.patient import PatientCreate, PatientRead, PatientUpdate
from app.services.patient_service import PatientService

router = APIRouter(prefix="/patients", tags=["Patients"])


def serialize(patient) -> dict:
    return PatientRead.model_validate(patient).model_dump(mode="json")


@router.get("")
def list_patients(
    db: DbSession,
    last_name: str | None = Query(default=None, max_length=50),
    date_of_birth: date | None = None,
    phone_number: str | None = None,
) -> dict:
    patients = PatientService(db).list(last_name, date_of_birth, phone_number)
    return {"data": [serialize(patient) for patient in patients], "error": None}


@router.get("/{patient_id}")
def get_patient(patient_id: UUID, db: DbSession) -> dict:
    return {"data": serialize(PatientService(db).get(patient_id)), "error": None}


@router.post("", status_code=status.HTTP_201_CREATED)
def create_patient(payload: PatientCreate, db: DbSession) -> dict:
    return {"data": serialize(PatientService(db).create(payload)), "error": None}


@router.put("/{patient_id}")
def update_patient(patient_id: UUID, payload: PatientUpdate, db: DbSession) -> dict:
    return {"data": serialize(PatientService(db).update(patient_id, payload)), "error": None}


@router.delete("/{patient_id}")
def delete_patient(patient_id: UUID, db: DbSession) -> dict:
    patient = PatientService(db).delete(patient_id)
    return {"data": {"patient_id": str(patient.patient_id), "deleted": True}, "error": None}
