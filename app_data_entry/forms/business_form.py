"""
Shared business profile form, used by both the Register and Edit pages.
All fields are optional per project spec.
"""

import streamlit as st

from shared.constants import WINDOWS, AFGHANISTAN_PROVINCES, YES_NO_OPTIONS
from app_data_entry.forms.validators import (
    validate_email,
    validate_phone,
    validate_year,
    validate_latitude,
    validate_longitude,
)


def _select_index(options: list, value) -> int:
    """Safely find the index of `value` in `options`, defaulting to 0 (blank)."""
    if value in options:
        return options.index(value)
    return 0


def render_business_form(existing: dict | None = None, form_key: str = "business_form"):
    """
    Renders the full business profile form.

    Args:
        existing: dict of current values, used to pre-fill fields when editing.
                  Pass None for a blank Registration form.
        form_key: unique Streamlit form key (register vs edit pages need different keys).

    Returns:
        (submitted: bool, data: dict, errors: list[str])
    """
    existing = existing or {}
    errors: list[str] = []

    with st.form(form_key, clear_on_submit=False):

        # ------------------------------------------------------------
        st.subheader("1. Business Information")
        col1, col2, col3 = st.columns(3)
        with col1:
            business_id_fao = st.text_input("Business ID (FAO)", value=existing.get("business_id_fao", "") or "")
            window = st.selectbox("Window", [""] + WINDOWS, index=_select_index([""] + WINDOWS, existing.get("window", "")))
        with col2:
            enterprise_name = st.text_input("Enterprise Name", value=existing.get("enterprise_name", "") or "")
            verification_status = st.text_input("Verification Status", value=existing.get("verification_status", "") or "")
        with col3:
            year_of_establishment = st.text_input("Year of Establishment", value=existing.get("year_of_establishment", "") or "")

        col4, col5 = st.columns(2)
        with col4:
            women_led = st.selectbox("Women Led", YES_NO_OPTIONS, index=_select_index(YES_NO_OPTIONS, existing.get("women_led", "")))
        with col5:
            youth_inclusive = st.selectbox("Youth Inclusive", YES_NO_OPTIONS, index=_select_index(YES_NO_OPTIONS, existing.get("youth_inclusive", "")))

        st.divider()

        # ------------------------------------------------------------
        st.subheader("2. Contact Information")
        st.markdown("**Primary Contact**")
        col1, col2 = st.columns(2)
        with col1:
            owner_name_primary = st.text_input("Owner Name (Primary)", value=existing.get("owner_name_primary", "") or "")
            phone_primary = st.text_input("Phone (Primary)", value=existing.get("phone_primary", "") or "")
        with col2:
            owner_position_primary = st.text_input("Owner Position (Primary)", value=existing.get("owner_position_primary", "") or "")
            email_primary = st.text_input("Email (Primary)", value=existing.get("email_primary", "") or "")

        st.markdown("**Secondary Contact**")
        col1, col2 = st.columns(2)
        with col1:
            owner_name_secondary = st.text_input("Owner Name (Secondary)", value=existing.get("owner_name_secondary", "") or "")
            phone_secondary = st.text_input("Phone (Secondary)", value=existing.get("phone_secondary", "") or "")
        with col2:
            owner_position_secondary = st.text_input("Owner Position (Secondary)", value=existing.get("owner_position_secondary", "") or "")
            email_secondary = st.text_input("Email (Secondary)", value=existing.get("email_secondary", "") or "")

        st.divider()

        # ------------------------------------------------------------
        st.subheader("3. Location Information")
        col1, col2, col3 = st.columns(3)
        with col1:
            province = st.selectbox(
                "Province", [""] + AFGHANISTAN_PROVINCES,
                index=_select_index([""] + AFGHANISTAN_PROVINCES, existing.get("province", "")),
            )
        with col2:
            district = st.text_input("District", value=existing.get("district", "") or "")
        with col3:
            village = st.text_input("Village", value=existing.get("village", "") or "")

        exact_address = st.text_area("Exact Address", value=existing.get("exact_address", "") or "")

        col1, col2 = st.columns(2)
        with col1:
            latitude = st.number_input(
                "Latitude", value=float(existing.get("latitude") or 0.0),
                format="%.6f", step=0.000001,
            )
        with col2:
            longitude = st.number_input(
                "Longitude", value=float(existing.get("longitude") or 0.0),
                format="%.6f", step=0.000001,
            )

        st.divider()

        # ------------------------------------------------------------
        st.subheader("4. Business Statistics")
        col1, col2 = st.columns(2)
        with col1:
            current_employee_count = st.number_input(
                "Current Employee Count", min_value=0, step=1,
                value=int(existing.get("current_employee_count") or 0),
            )
        with col2:
            current_farmers_linked = st.number_input(
                "Current Farmers Linked", min_value=0, step=1,
                value=int(existing.get("current_farmers_linked") or 0),
            )

        st.divider()

        # ------------------------------------------------------------
        st.subheader("5. Financial Information")
        col1, col2, col3 = st.columns(3)
        with col1:
            annual_turnover_usd = st.number_input(
                "Annual Turnover (USD)", min_value=0.0, step=100.0,
                value=float(existing.get("annual_turnover_usd") or 0.0),
            )
        with col2:
            grant_requested_usd = st.number_input(
                "Grant Requested (USD)", min_value=0.0, step=100.0,
                value=float(existing.get("grant_requested_usd") or 0.0),
            )
        with col3:
            total_co_contribution_usd = st.number_input(
                "Total Co-Contribution (USD)", min_value=0.0, step=100.0,
                value=float(existing.get("total_co_contribution_usd") or 0.0),
            )

        submitted = st.form_submit_button("Save Business", type="primary", use_container_width=True)

    data = {
        "business_id_fao": business_id_fao.strip(),
        "window": window,
        "enterprise_name": enterprise_name.strip(),
        "verification_status": verification_status.strip(),
        "year_of_establishment": year_of_establishment.strip(),
        "women_led": women_led,
        "youth_inclusive": youth_inclusive,
        "owner_name_primary": owner_name_primary.strip(),
        "owner_position_primary": owner_position_primary.strip(),
        "phone_primary": phone_primary.strip(),
        "email_primary": email_primary.strip(),
        "owner_name_secondary": owner_name_secondary.strip(),
        "owner_position_secondary": owner_position_secondary.strip(),
        "phone_secondary": phone_secondary.strip(),
        "email_secondary": email_secondary.strip(),
        "province": province,
        "district": district.strip(),
        "village": village.strip(),
        "exact_address": exact_address.strip(),
        "latitude": latitude,
        "longitude": longitude,
        "current_employee_count": int(current_employee_count),
        "current_farmers_linked": int(current_farmers_linked),
        "annual_turnover_usd": annual_turnover_usd,
        "grant_requested_usd": grant_requested_usd,
        "total_co_contribution_usd": total_co_contribution_usd,
    }

    if submitted:
        for check in (
            validate_email(data["email_primary"]),
            validate_email(data["email_secondary"]),
            validate_phone(data["phone_primary"]),
            validate_phone(data["phone_secondary"]),
            validate_year(data["year_of_establishment"]),
            validate_latitude(data["latitude"]),
            validate_longitude(data["longitude"]),
        ):
            is_valid, message = check
            if not is_valid:
                errors.append(message)

    return submitted, data, errors
