"""
Page: Update Business Phase & Stage Progress.

Since there is no history table, saving here overwrites the current
status columns on the Business row in place.
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
from app_data_entry.auth import require_login
from shared.database.init_db import init_db
from shared.database.engine import get_session
from shared.database.crud import get_all_businesses, get_business_by_business_id, update_business
from shared.constants import (
    PHASE_OPTIONS,
    PHASE_1_STAGES,
    PHASE_2_STAGES,
    STAGE_STATUS_OPTIONS,
    YES_NO_OPTIONS,
)

st.set_page_config(page_title="Update Phase & Stage", page_icon="📈", layout="wide")
init_db()
require_login()

st.title("Update Business Phase & Stage Progress")

with get_session() as session:
    all_businesses = get_all_businesses(session)

if not all_businesses:
    st.info("No businesses in the system yet. Register one first.")
    st.stop()

options = {f"{b.business_id} — {b.enterprise_name or 'Unnamed'}": b.business_id for b in all_businesses}
selected_label = st.selectbox("Select a business", list(options.keys()))
selected_business_id = options[selected_label]

with get_session() as session:
    business = get_business_by_business_id(session, selected_business_id)
    existing_data = {c.name: getattr(business, c.name) for c in business.__table__.columns}

st.divider()

current_phase = st.selectbox(
    "Current Phase",
    PHASE_OPTIONS,
    index=PHASE_OPTIONS.index(existing_data.get("current_phase")) if existing_data.get("current_phase") in PHASE_OPTIONS else 0,
)

update_payload = {"current_phase": current_phase}

if current_phase == "Phase 1: Pre-Qualification Verification":
    st.subheader("Phase 1: Pre-Qualification Verification")

    st.markdown("**Stage 3: Verification Status** *(shared with the business profile field)*")
    verification_status = st.text_input("Verification Status", value=existing_data.get("verification_status", "") or "")
    update_payload["verification_status"] = verification_status.strip()

    for label, field_name in PHASE_1_STAGES.items():
        if field_name == "p1_s4_selected_for_bds":
            value = st.selectbox(
                label, YES_NO_OPTIONS,
                index=YES_NO_OPTIONS.index(existing_data.get(field_name)) if existing_data.get(field_name) in YES_NO_OPTIONS else 0,
                key=field_name,
            )
        else:
            value = st.selectbox(
                label, STAGE_STATUS_OPTIONS,
                index=STAGE_STATUS_OPTIONS.index(existing_data.get(field_name)) if existing_data.get(field_name) in STAGE_STATUS_OPTIONS else 0,
                key=field_name,
            )
        update_payload[field_name] = value

elif current_phase == "Phase 2: Business Development Support":
    st.subheader("Phase 2: Business Development Support")

    st.caption("Stage 4a and 4b (Virtual / In-Person Capacity Building) can run in parallel.")

    for label, field_name in PHASE_2_STAGES.items():
        value = st.selectbox(
            label, STAGE_STATUS_OPTIONS,
            index=STAGE_STATUS_OPTIONS.index(existing_data.get(field_name)) if existing_data.get(field_name) in STAGE_STATUS_OPTIONS else 0,
            key=field_name,
        )
        update_payload[field_name] = value

else:
    st.info("Select a phase above to update its stage statuses.")

st.divider()

if st.button("Save Phase & Stage Update", type="primary", use_container_width=True):
    with get_session() as session:
        update_business(session, selected_business_id, update_payload)
    st.success(f"Phase & stage progress updated for **{selected_business_id}**.")
