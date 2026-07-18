from datetime import date, datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import Patient
from app.schemas.patient import PatientCreate, PatientUpdate


class PatientRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(
        self,
        last_name: str | None = None,
        date_of_birth: date | None = None,
        phone_number: str | None = None,
    ) -> list[Patient]:
        stmt = select(Patient).where(Patient.deleted_at.is_(None))
        if last_name:
            stmt = stmt.where(Patient.last_name.ilike(last_name.strip()))
        if date_of_birth:
            stmt = stmt.where(Patient.date_of_birth == date_of_birth)
        if phone_number:
            stmt = stmt.where(Patient.phone_number == phone_number)
        return list(self.db.scalars(stmt.order_by(Patient.created_at.desc())).all())

    def get(self, patient_id: UUID) -> Patient | None:
        return self.db.scalar(
            select(Patient).where(Patient.patient_id == patient_id, Patient.deleted_at.is_(None))
        )

    def find_by_phone(self, phone_number: str) -> Patient | None:
        return self.db.scalar(
            select(Patient)
            .where(Patient.phone_number == phone_number, Patient.deleted_at.is_(None))
            .order_by(Patient.updated_at.desc())
        )

    def create(self, payload: PatientCreate) -> Patient:
        patient = Patient(**payload.model_dump())
        self.db.add(patient)
        self.db.commit()
        self.db.refresh(patient)
        return patient

    def update(self, patient: Patient, payload: PatientUpdate) -> Patient:
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(patient, field, value)
        patient.updated_at = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(patient)
        return patient

    def soft_delete(self, patient: Patient) -> Patient:
        patient.deleted_at = datetime.now(timezone.utc)
        patient.updated_at = patient.deleted_at
        self.db.commit()
        self.db.refresh(patient)
        return patient
