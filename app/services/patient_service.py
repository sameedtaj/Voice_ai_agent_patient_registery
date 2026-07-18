from datetime import date
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, NotFoundError
from app.database.models import Patient
from app.repositories.patient_repository import PatientRepository
from app.schemas.patient import PatientCreate, PatientUpdate
from app.utils.validators import normalize_phone


class PatientService:
    def __init__(self, db: Session):
        self.repo = PatientRepository(db)

    def list(self, last_name: str | None, date_of_birth: date | None, phone_number: str | None):
        normalized = normalize_phone(phone_number) if phone_number else None
        return self.repo.list(last_name, date_of_birth, normalized)

    def get(self, patient_id: UUID) -> Patient:
        patient = self.repo.get(patient_id)
        if not patient:
            raise NotFoundError("Patient not found")
        return patient

    def find_by_phone(self, phone_number: str) -> Patient | None:
        return self.repo.find_by_phone(normalize_phone(phone_number))

    def create(self, payload: PatientCreate) -> Patient:
        existing = self.repo.find_by_phone(payload.phone_number)
        if existing:
            raise ConflictError(
                f"A patient named {existing.first_name} {existing.last_name} already uses this phone number"
            )
        return self.repo.create(payload)

    def update(self, patient_id: UUID, payload: PatientUpdate) -> Patient:
        patient = self.get(patient_id)
        if payload.phone_number:
            existing = self.repo.find_by_phone(payload.phone_number)
            if existing and existing.patient_id != patient.patient_id:
                raise ConflictError("Another patient already uses this phone number")
        return self.repo.update(patient, payload)

    def delete(self, patient_id: UUID) -> Patient:
        return self.repo.soft_delete(self.get(patient_id))
