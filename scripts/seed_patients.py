from datetime import date

from app.database.base import Base
from app.database.session import SessionLocal, engine
from app.schemas.patient import PatientCreate
from app.services.patient_service import PatientService


def main() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        payload = PatientCreate(
            first_name="Jane",
            last_name="Doe",
            date_of_birth=date(1990, 5, 21),
            sex="Female",
            phone_number="2025550147",
            email="jane.doe@example.com",
            address_line_1="1200 Main Street",
            address_line_2="Apt 4B",
            city="Washington",
            state="DC",
            zip_code="20001",
            preferred_language="English",
        )
        existing = PatientService(db).find_by_phone(payload.phone_number)
        if existing:
            print(f"Seed already exists: {existing.patient_id}")
        else:
            patient = PatientService(db).create(payload)
            print(f"Created seed patient: {patient.patient_id}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
