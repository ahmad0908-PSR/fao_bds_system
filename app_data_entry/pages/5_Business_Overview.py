"""
Page: Business Overview.

Original spec item 5 was "View Business Tracking History" — since the
history table was removed, this page instead shows a full, read-only
snapshot of a single business: profile + current phase/stage status.
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
from shared.database.crud import get_all_businesses, get_business_by_business_id
from shared.constants import PHASE_1_STAGES, PHASE_2_STAGES

st.set_page_config(page_title="Business Overview", page_icon="📄", layout="wide")
init_db()
require_login()

st.title("Business Overview")

with get_session() as session:
    all_businesses = get_all_businesses(session)

if not all_businesses:
    st.info("No businesses in the system yet. Register one first.")
    st.stop()

options = {f"{b.business_id} — {b.enterprise_name or 'Unnamed'}": b.business_id for b in all_businesses}
selected_label = st.selectbox("Select a business", list(options.keys()))
selected_business_id = options[selected_label]

with get_session() as session:
    b = get_business_by_business_id(session, selected_business_id)

    st.header(f"{b.business_id} — {b.enterprise_name or 'Unnamed'}")

    col1, col2, col3 = st.columns(3)
    col1.metric("Window", b.window or "—")
    col2.metric("Province", b.province or "—")
    col3.metric("Current Phase", b.current_phase or "Not Set")

    st.divider()
    st.subheader("Business Information")
    st.write(f"**FAO Business ID:** {b.business_id_fao or '—'}")
    st.write(f"**Verification Status:** {b.verification_status or '—'}")
    st.write(f"**Year of Establishment:** {b.year_of_establishment or '—'}")
    st.write(f"**Women Led:** {b.women_led or '—'}  |  **Youth Inclusive:** {b.youth_inclusive or '—'}")

    st.subheader("Contact Information")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Primary**")
        st.write(f"{b.owner_name_primary or '—'} — {b.owner_position_primary or '—'}")
        st.write(f"{b.phone_primary or '—'} | {b.email_primary or '—'}")
    with c2:
        st.markdown("**Secondary**")
        st.write(f"{b.owner_name_secondary or '—'} — {b.owner_position_secondary or '—'}")
        st.write(f"{b.phone_secondary or '—'} | {b.email_secondary or '—'}")

    st.subheader("Location")
    st.write(f"{b.district or '—'}, {b.village or '—'}, {b.province or '—'}")
    st.write(f"**Address:** {b.exact_address or '—'}")
    st.write(f"**Coordinates:** {b.latitude or '—'}, {b.longitude or '—'}")

    st.subheader("Statistics & Finance")
    c1, c2, c3 = st.columns(3)
    c1.metric("Employees", b.current_employee_count or 0)
    c2.metric("Farmers Linked", b.current_farmers_linked or 0)
    c3.metric("Annual Turnover (USD)", f"{b.annual_turnover_usd or 0:,.2f}")
    c1.metric("Grant Requested (USD)", f"{b.grant_requested_usd or 0:,.2f}")
    c2.metric("Co-Contribution (USD)", f"{b.total_co_contribution_usd or 0:,.2f}")

    st.divider()
    st.subheader("Phase & Stage Status")

    st.markdown("**Phase 1: Pre-Qualification Verification**")
    st.write(f"- Stage 3 (Verification Status): **{b.verification_status or 'Not Set'}**")
    for label, field_name in PHASE_1_STAGES.items():
        st.write(f"- {label}: **{getattr(b, field_name) or 'Not Set'}**")

    st.markdown("**Phase 2: Business Development Support**")
    for label, field_name in PHASE_2_STAGES.items():
        st.write(f"- {label}: **{getattr(b, field_name) or 'Not Started'}**")

    st.caption(f"Created: {b.created_at} | Last Updated: {b.updated_at}")
