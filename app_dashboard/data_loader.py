"""
Loads Business rows from the shared SQLite database into a pandas
DataFrame for use across all Dashboard pages.

App 2 is read-only: nothing in this app ever calls create_business /
update_business / delete — only SELECT-style reads via crud.get_all_businesses.
"""

import streamlit as st
import pandas as pd

from shared.database.engine import get_session
from shared.database.crud import get_all_businesses


@st.cache_data(ttl=30, show_spinner="Loading business data...")
def load_businesses_df() -> pd.DataFrame:
    """
    Returns all businesses as a DataFrame, one row per business, columns
    matching the Business model fields. Cached for 30s so navigating
    between dashboard pages doesn't re-hit the DB on every rerun, but a
    new registration/edit in App 1 shows up within half a minute.
    """
    with get_session() as session:
        businesses = get_all_businesses(session)
        rows = [
            {c.name: getattr(b, c.name) for c in b.__table__.columns}
            for b in businesses
        ]

    df = pd.DataFrame(rows)

    if df.empty:
        return df

    # Normalize numeric columns (SQLite can return None for optional fields)
    numeric_cols = [
        "latitude", "longitude", "current_employee_count", "current_farmers_linked",
        "annual_turnover_usd", "grant_requested_usd", "total_co_contribution_usd",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "created_at" in df.columns:
        df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")

    return df
