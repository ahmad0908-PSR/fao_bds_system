"""
Page: Search Business.
Simple keyword search across Business_ID, FAO ID, Enterprise Name, Owner names, Province.
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import pandas as pd
import streamlit as st
from app_data_entry.auth import require_login
from shared.database.init_db import init_db
from shared.database.engine import get_session
from shared.database.crud import search_businesses

st.set_page_config(page_title="Search Business", page_icon="🔍", layout="wide")
init_db()
require_login()

st.title("Search Business")

keyword = st.text_input(
    "Search by Business ID, FAO ID, Enterprise Name, Owner Name, or Province",
    placeholder="e.g. BDS-000004, Kabul, or an owner's name",
)

with get_session() as session:
    results = search_businesses(session, keyword)

st.caption(f"{len(results)} result(s)")

if results:
    rows = [
        {
            "Business ID": b.business_id,
            "Enterprise Name": b.enterprise_name,
            "Province": b.province,
            "Window": b.window,
            "Owner (Primary)": b.owner_name_primary,
            "Phone (Primary)": b.phone_primary,
            "Current Phase": b.current_phase,
            "Women Led": b.women_led,
            "Youth Inclusive": b.youth_inclusive,
        }
        for b in results
    ]
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("No matching businesses found.")
