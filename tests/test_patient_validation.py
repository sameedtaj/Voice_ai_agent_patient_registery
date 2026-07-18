from datetime import date, timedelta

import pytest
from pydantic import ValidationError

from app.schemas.patient import PatientCreate


def test_normalizes_phone_and_state(patient_payload):
    patient = PatientCreate.model_validate(patient_payload)
    assert patient.phone_number == "2025550147"
    assert patient.state == "DC"


def test_rejects_future_birth_date(patient_payload):
    patient_payload["date_of_birth"] = str(date.today() + timedelta(days=1))
    with pytest.raises(ValidationError, match="future"):
        PatientCreate.model_validate(patient_payload)


def test_rejects_short_phone(patient_payload):
    patient_payload["phone_number"] = "123"
    with pytest.raises(ValidationError, match="10 U.S. digits"):
        PatientCreate.model_validate(patient_payload)


def test_rejects_invalid_state(patient_payload):
    patient_payload["state"] = "ZZ"
    with pytest.raises(ValidationError, match="state"):
        PatientCreate.model_validate(patient_payload)
