"""
Page: Edit Existing Business.
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
from app_data_entry.auth import require_login
from app_data_entry.forms.business_form import render_business_form
from shared.database.init_db import init_db
from shared.database.engine import get_session
from shared.database.crud import get_all_businesses, get_business_by_business_id, update_business

st.set_page_config(page_title="Edit Business", page_icon="✏️", layout="wide")
init_db()
require_login()

st.title("Edit Existing Business")

with get_session() as session:
    all_businesses = get_all_businesses(session)

if not all_businesses:
    st.info("No businesses in the system yet. Register one first.")
    st.stop()

options = {f"{b.business_id} — {b.enterprise_name or 'Unnamed'}": b.business_id for b in all_businesses}
selected_label = st.selectbox("Select a business to edit", list(options.keys()))
selected_business_id = options[selected_label]

with get_session() as session:
    business = get_business_by_business_id(session, selected_business_id)
    existing_data = {c.name: getattr(business, c.name) for c in business.__table__.columns}

st.divider()

submitted, data, errors = render_business_form(existing=existing_data, form_key=f"edit_form_{selected_business_id}")

if submitted:
    if errors:
        for err in errors:
            st.error(err)
    else:
        with get_session() as session:
            update_business(session, selected_business_id, data)
        st.success(f"Business **{selected_business_id}** updated successfully.")
