"""
FAO EFSP - Data Entry & Business Tracking System (Application 1)

Run with:
    streamlit run app_data_entry/main.py
"""

import sys
from pathlib import Path

# Make the project root importable (so "shared.*" and "app_data_entry.*" resolve)
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
from app_data_entry.auth import require_login
from shared.database.init_db import init_db
from shared.database.engine import get_session
from shared.database.crud import get_all_businesses

st.set_page_config(
    page_title="FAO EFSP — Data Entry System",
    page_icon="📋",
    layout="wide",
)

# Make sure the DB/table exist before anything else runs
init_db()

require_login()

# ----------------------------------------------------------------
# Landing page (shown after login)
# ----------------------------------------------------------------
st.title("FAO EFSP — Business Development Support")
st.subheader("Data Entry & Business Tracking System")

st.markdown(
    """
    Use the sidebar to navigate:

    - **Register Business** — add a new business profile
    - **Edit Business** — update an existing profile
    - **Search Business** — look up a business by ID, name, owner, or province
    - **Update Phase & Stage** — change current phase/stage status
    - **Business Overview** — full read-only view of a single business
    """
)

with get_session() as session:
    total_businesses = len(get_all_businesses(session))

col1, col2 = st.columns(2)
col1.metric("Total Businesses in System", total_businesses)

if st.sidebar.button("Log Out"):
    st.session_state.authenticated = False
    st.rerun()
