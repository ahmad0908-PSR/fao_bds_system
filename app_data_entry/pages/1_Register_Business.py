"""
Page: Register New Business.

NOTE: Streamlit's multipage "pages/" mechanism runs this file standalone
(it does not run main.py first), so each page re-does the path setup,
DB init, and login check independently.
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
from shared.database.crud import create_business

st.set_page_config(page_title="Register Business", page_icon="🆕", layout="wide")
init_db()
require_login()

st.title("Register New Business")
st.caption("All fields are optional except the auto-generated Business ID.")

submitted, data, errors = render_business_form(existing=None, form_key="register_form")

if submitted:
    if errors:
        for err in errors:
            st.error(err)
    else:
        with get_session() as session:
            business = create_business(session, data)
        st.success(f"Business registered successfully — assigned ID: **{business.business_id}**")
        st.balloons()
