"""
Shared CRUD operations for the Business model.
Both applications should go through these functions rather than writing
raw queries inline, so query logic stays consistent everywhere.
"""

from sqlalchemy import or_

from shared.config import BUSINESS_ID_PREFIX, BUSINESS_ID_PADDING
from shared.database.models import Business


def generate_next_business_id(session) -> str:
    """
    Generates the next sequential Business_ID, e.g. BDS-000001, BDS-000002...
    Based on the highest existing numeric suffix currently in the table.
    """
    last_business = (
        session.query(Business)
        .order_by(Business.id.desc())
        .first()
    )

    if last_business is None:
        next_number = 1
    else:
        # business_id looks like "BDS-000001" -> take the numeric part after the dash
        try:
            last_number = int(last_business.business_id.split("-")[-1])
        except (ValueError, AttributeError):
            last_number = last_business.id
        next_number = last_number + 1

    return f"{BUSINESS_ID_PREFIX}-{str(next_number).zfill(BUSINESS_ID_PADDING)}"


def create_business(session, data: dict) -> Business:
    """
    Creates a new Business row. Auto-generates business_id.
    `data` should be a dict of field_name -> value (only known model fields are used).
    """
    business_id = generate_next_business_id(session)

    valid_fields = {c.name for c in Business.__table__.columns}
    clean_data = {k: v for k, v in data.items() if k in valid_fields}

    business = Business(business_id=business_id, **clean_data)
    session.add(business)
    session.commit()
    session.refresh(business)
    return business


def update_business(session, business_id: str, data: dict) -> Business | None:
    """
    Updates an existing Business row (identified by business_id) in place.
    Returns the updated Business, or None if not found.
    """
    business = get_business_by_business_id(session, business_id)
    if business is None:
        return None

    valid_fields = {c.name for c in Business.__table__.columns}
    for key, value in data.items():
        if key in valid_fields and key not in ("id", "business_id", "created_at"):
            setattr(business, key, value)

    session.commit()
    session.refresh(business)
    return business


def get_business_by_business_id(session, business_id: str) -> Business | None:
    return session.query(Business).filter(Business.business_id == business_id).first()


def get_all_businesses(session) -> list[Business]:
    return session.query(Business).order_by(Business.id.desc()).all()


def search_businesses(session, keyword: str) -> list[Business]:
    """
    Simple case-insensitive search across the fields most useful for lookup:
    Business_ID, FAO ID, Enterprise Name, Owner names, Province.
    """
    if not keyword:
        return get_all_businesses(session)

    like_term = f"%{keyword.strip()}%"

    return (
        session.query(Business)
        .filter(
            or_(
                Business.business_id.ilike(like_term),
                Business.business_id_fao.ilike(like_term),
                Business.enterprise_name.ilike(like_term),
                Business.owner_name_primary.ilike(like_term),
                Business.owner_name_secondary.ilike(like_term),
                Business.province.ilike(like_term),
            )
        )
        .order_by(Business.id.desc())
        .all()
    )
