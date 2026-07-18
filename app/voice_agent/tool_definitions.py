PATIENT_PROPERTIES = {
    "first_name": {"type": "string", "description": "Patient first name"},
    "last_name": {"type": "string", "description": "Patient last name"},
    "date_of_birth": {"type": "string", "format": "date", "description": "YYYY-MM-DD"},
    "sex": {
        "type": "string",
        "enum": ["Male", "Female", "Other", "Decline to Answer"],
    },
    "phone_number": {"type": "string", "description": "Ten-digit U.S. phone number"},
    "email": {"type": "string", "description": "Optional email address"},
    "address_line_1": {"type": "string"},
    "address_line_2": {"type": "string"},
    "city": {"type": "string"},
    "state": {"type": "string", "description": "Two-letter U.S. state abbreviation"},
    "zip_code": {"type": "string"},
    "insurance_provider": {"type": "string"},
    "insurance_member_id": {"type": "string"},
    "preferred_language": {"type": "string", "default": "English"},
    "emergency_contact_name": {"type": "string"},
    "emergency_contact_phone": {"type": "string"},
    "confirmed": {
        "type": "boolean",
        "description": "True only after the caller explicitly confirms the full read-back",
    },
}

REQUIRED_PATIENT_FIELDS = [
    "first_name", "last_name", "date_of_birth", "sex", "phone_number",
    "address_line_1", "city", "state", "zip_code", "confirmed",
]

TOOLS = [
    {
        "name": "find_patient_by_phone",
        "description": "Check whether an active patient already exists for a validated phone number.",
        "parameters": {
            "type": "object",
            "properties": {"phone_number": PATIENT_PROPERTIES["phone_number"]},
            "required": ["phone_number"],
        },
    },
    {
        "name": "create_patient",
        "description": "Create a patient only after all required data is collected and explicitly confirmed.",
        "parameters": {
            "type": "object",
            "properties": PATIENT_PROPERTIES,
            "required": REQUIRED_PATIENT_FIELDS,
        },
    },
    {
        "name": "update_patient",
        "description": "Partially update a matched patient only after the caller explicitly confirms changes.",
        "parameters": {
            "type": "object",
            "properties": {
                "patient_id": {"type": "string", "description": "Existing patient UUID"},
                **PATIENT_PROPERTIES,
            },
            "required": ["patient_id", "confirmed"],
        },
    },
]
