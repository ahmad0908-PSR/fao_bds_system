"""
Lightweight validators for the registration/edit form.
Every field is optional per project spec, so a validator only fires
when the field is non-empty. Returns (is_valid, error_message).
"""

import re

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_REGEX = re.compile(r"^[0-9+\-\s()]{6,20}$")


def validate_email(value: str):
    if not value:
        return True, ""
    if not EMAIL_REGEX.match(value.strip()):
        return False, "Enter a valid email address (e.g. name@example.com)."
    return True, ""


def validate_phone(value: str):
    if not value:
        return True, ""
    if not PHONE_REGEX.match(value.strip()):
        return False, "Enter a valid phone number (digits, spaces, +, -, () only)."
    return True, ""


def validate_year(value: str):
    if not value:
        return True, ""
    if not value.isdigit() or not (1900 <= int(value) <= 2100):
        return False, "Enter a valid 4-digit year between 1900 and 2100."
    return True, ""


def validate_latitude(value):
    if value is None or value == 0:
        return True, ""
    if not (-90 <= value <= 90):
        return False, "Latitude must be between -90 and 90."
    return True, ""


def validate_longitude(value):
    if value is None or value == 0:
        return True, ""
    if not (-180 <= value <= 180):
        return False, "Longitude must be between -180 and 180."
    return True, ""
