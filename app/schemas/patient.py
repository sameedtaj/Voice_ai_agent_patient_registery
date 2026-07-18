import re
from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.database.models import Sex
from app.utils.constants import US_STATES
from app.utils.validators import MEMBER_ID_RE, NAME_RE, ZIP_RE, normalize_phone


class PatientFields(BaseModel):
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    date_of_birth: date
    sex: Sex
    phone_number: str
    email: EmailStr | None = None
    address_line_1: str = Field(min_length=1, max_length=200)
    address_line_2: str | None = Field(default=None, max_length=100)
    city: str = Field(min_length=1, max_length=100)
    state: str
    zip_code: str
    insurance_provider: str | None = Field(default=None, max_length=100)
    insurance_member_id: str | None = Field(default=None, max_length=100)
    preferred_language: str = Field(default="English", min_length=1, max_length=50)
    emergency_contact_name: str | None = Field(default=None, max_length=100)
    emergency_contact_phone: str | None = None

    @field_validator("first_name", "last_name")
    @classmethod
    def valid_name(cls, value: str) -> str:
        value = value.strip()
        if not NAME_RE.fullmatch(value):
            raise ValueError("Name may contain letters, spaces, hyphens, and apostrophes")
        return value

    @field_validator("date_of_birth")
    @classmethod
    def dob_not_future(cls, value: date) -> date:
        if value > date.today():
            raise ValueError("Date of birth cannot be in the future")
        return value

    @field_validator("phone_number")
    @classmethod
    def valid_phone(cls, value: str) -> str:
        return normalize_phone(value)

    @field_validator("emergency_contact_phone")
    @classmethod
    def valid_optional_phone(cls, value: str | None) -> str | None:
        return normalize_phone(value) if value else None

    @field_validator("state")
    @classmethod
    def valid_state(cls, value: str) -> str:
        value = value.strip().upper()
        if value not in US_STATES:
            raise ValueError("Use a valid two-letter U.S. state abbreviation")
        return value

    @field_validator("zip_code")
    @classmethod
    def valid_zip(cls, value: str) -> str:
        value = value.strip()
        if not ZIP_RE.fullmatch(value):
            raise ValueError("ZIP code must be 5 digits or ZIP+4")
        return value

    @field_validator("insurance_member_id")
    @classmethod
    def valid_member_id(cls, value: str | None) -> str | None:
        if value and not MEMBER_ID_RE.fullmatch(value):
            raise ValueError("Insurance member ID contains unsupported characters")
        return value


class PatientCreate(PatientFields):
    pass


class PatientUpdate(BaseModel):
    first_name: str | None = Field(default=None, min_length=1, max_length=50)
    last_name: str | None = Field(default=None, min_length=1, max_length=50)
    date_of_birth: date | None = None
    sex: Sex | None = None
    phone_number: str | None = None
    email: EmailStr | None = None
    address_line_1: str | None = Field(default=None, min_length=1, max_length=200)
    address_line_2: str | None = Field(default=None, max_length=100)
    city: str | None = Field(default=None, min_length=1, max_length=100)
    state: str | None = None
    zip_code: str | None = None
    insurance_provider: str | None = Field(default=None, max_length=100)
    insurance_member_id: str | None = Field(default=None, max_length=100)
    preferred_language: str | None = Field(default=None, min_length=1, max_length=50)
    emergency_contact_name: str | None = Field(default=None, max_length=100)
    emergency_contact_phone: str | None = None

    @field_validator("first_name", "last_name")
    @classmethod
    def valid_name(cls, value: str | None) -> str | None:
        if value is not None and not NAME_RE.fullmatch(value.strip()):
            raise ValueError("Name may contain letters, spaces, hyphens, and apostrophes")
        return value.strip() if value else value

    @field_validator("date_of_birth")
    @classmethod
    def dob_not_future(cls, value: date | None) -> date | None:
        if value and value > date.today():
            raise ValueError("Date of birth cannot be in the future")
        return value

    @field_validator("phone_number", "emergency_contact_phone")
    @classmethod
    def valid_phone(cls, value: str | None) -> str | None:
        return normalize_phone(value) if value else value

    @field_validator("state")
    @classmethod
    def valid_state(cls, value: str | None) -> str | None:
        if value is None:
            return None
        state = value.strip().upper()
        if state not in US_STATES:
            raise ValueError("Use a valid two-letter U.S. state abbreviation")
        return state

    @field_validator("zip_code")
    @classmethod
    def valid_zip(cls, value: str | None) -> str | None:
        if value is not None and not ZIP_RE.fullmatch(value.strip()):
            raise ValueError("ZIP code must be 5 digits or ZIP+4")
        return value.strip() if value else value


class PatientRead(PatientFields):
    patient_id: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
