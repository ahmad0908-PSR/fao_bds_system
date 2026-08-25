"""
Page: Business Profile Lookup.
Read-only — no editing happens in App 2. Respects global filters, then
lets you search/select within the filtered set for a full profile view.
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import pandas as pd
import streamlit as st

from app_dashboard.data_loader import load_businesses_df
from app_dashboard.filters import render_and_apply_filters
from shared.constants import PHASE_1_STAGES, PHASE_2_STAGES, MATRIX_COLUMN_LABELS

st.set_page_config(page_title="Business Profile Lookup", page_icon="🔎", layout="wide")
st.title("Business Profile Lookup")

df = load_businesses_df()
if df.empty:
    st.warning("No businesses have been registered yet.")
    st.stop()

filtered_df = render_and_apply_filters(df)

if filtered_df.empty:
    st.info("No businesses match the current filters.")
    st.stop()

search = st.text_input("Search within filtered results (name, ID, owner, province)")
if search:
    s = search.strip().lower()
    mask = (
        filtered_df["business_id"].str.lower().str.contains(s, na=False)
        | filtered_df["business_id_fao"].astype(str).str.lower().str.contains(s, na=False)
        | filtered_df["enterprise_name"].astype(str).str.lower().str.contains(s, na=False)
        | filtered_df["owner_name_primary"].astype(str).str.lower().str.contains(s, na=False)
        | filtered_df["province"].astype(str).str.lower().str.contains(s, na=False)
    )
    filtered_df = filtered_df[mask]

if filtered_df.empty:
    st.info("No matches.")
    st.stop()

options = {
    f"{row.business_id} — {row.enterprise_name or 'Unnamed'}": row.business_id
    for row in filtered_df.itertuples()
}
selected_label = st.selectbox(f"Select a business ({len(options)} match(es))", list(options.keys()))
selected_id = options[selected_label]
b = filtered_df[filtered_df["business_id"] == selected_id].iloc[0]

st.divider()
st.header(f"{b['business_id']} — {b['enterprise_name'] or 'Unnamed'}")

col1, col2, col3 = st.columns(3)
col1.metric("Window", b["window"] or "—")
col2.metric("Province", b["province"] or "—")
col3.metric("Current Phase", b["current_phase"] or "Not Set")

st.subheader("Business Information")
st.write(f"**FAO Business ID:** {b['business_id_fao'] or '—'}")
st.write(f"**Verification Status:** {b['verification_status'] or '—'}")
st.write(f"**Year of Establishment:** {b['year_of_establishment'] or '—'}")
st.write(f"**Women Led:** {b['women_led'] or '—'}  |  **Youth Inclusive:** {b['youth_inclusive'] or '—'}")

st.subheader("Contact Information")
c1, c2 = st.columns(2)
with c1:
    st.markdown("**Primary**")
    st.write(f"{b['owner_name_primary'] or '—'} — {b['owner_position_primary'] or '—'}")
    st.write(f"{b['phone_primary'] or '—'} | {b['email_primary'] or '—'}")
with c2:
    st.markdown("**Secondary**")
    st.write(f"{b['owner_name_secondary'] or '—'} — {b['owner_position_secondary'] or '—'}")
    st.write(f"{b['phone_secondary'] or '—'} | {b['email_secondary'] or '—'}")

st.subheader("Location")
st.write(f"{b['district'] or '—'}, {b['village'] or '—'}, {b['province'] or '—'}")
st.write(f"**Address:** {b['exact_address'] or '—'}")
st.write(f"**Coordinates:** {b['latitude'] if pd.notna(b['latitude']) else '—'}, {b['longitude'] if pd.notna(b['longitude']) else '—'}")

st.subheader("Statistics & Finance")
c1, c2, c3 = st.columns(3)
c1.metric("Employees", int(b["current_employee_count"]) if pd.notna(b["current_employee_count"]) else 0)
c2.metric("Farmers Linked", int(b["current_farmers_linked"]) if pd.notna(b["current_farmers_linked"]) else 0)
c3.metric("Annual Turnover (USD)", f"{b['annual_turnover_usd'] or 0:,.2f}")
c1.metric("Grant Requested (USD)", f"{b['grant_requested_usd'] or 0:,.2f}")
c2.metric("Co-Contribution (USD)", f"{b['total_co_contribution_usd'] or 0:,.2f}")

st.divider()
st.subheader("Phase & Stage Status")

st.markdown("**Phase 1: Pre-Qualification Verification**")
st.write(f"- Verification Status: **{b['verification_status'] or 'Not Set'}**")
for label, field in PHASE_1_STAGES.items():
    st.write(f"- {MATRIX_COLUMN_LABELS.get(field, label)}: **{b[field] or 'Not Set'}**")

st.markdown("**Phase 2: Business Development Support**")
for label, field in PHASE_2_STAGES.items():
    st.write(f"- {MATRIX_COLUMN_LABELS.get(field, label)}: **{b[field] or 'Not Started'}**")
