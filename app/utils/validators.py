import re

from app.utils.constants import US_STATES

NAME_RE = re.compile(r"^[A-Za-z][A-Za-z '\-]{0,49}$")
ZIP_RE = re.compile(r"^\d{5}(?:-\d{4})?$")
MEMBER_ID_RE = re.compile(r"^[A-Za-z0-9._\- ]+$")


def normalize_phone(value: str) -> str:
    digits = re.sub(r"\D", "", value)
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]
    if len(digits) != 10:
        raise ValueError("Phone number must contain exactly 10 U.S. digits")
    return digits


def normalize_state(value: str) -> str:
    state = value.strip().upper()
    if state not in US_STATES:
        raise ValueError("State must be a valid two-letter U.S. abbreviation")
    return state
