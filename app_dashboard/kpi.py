"""
KPI calculations for the Dashboard homepage. Every KPI is computed fresh
from whatever DataFrame is passed in, so it's automatically filter-responsive
— call this AFTER applying global filters, not before.
"""

import pandas as pd


def compute_kpis(df: pd.DataFrame) -> dict:
    if df.empty:
        return {
            "total_businesses": 0,
            "women_led_count": 0,
            "youth_inclusive_count": 0,
            "total_grant_requested_usd": 0.0,
            "total_co_contribution_usd": 0.0,
            "avg_employee_count": 0.0,
            "total_farmers_linked": 0,
        }

    return {
        "total_businesses": len(df),
        "women_led_count": int((df["women_led"] == "Yes").sum()),
        "youth_inclusive_count": int((df["youth_inclusive"] == "Yes").sum()),
        "total_grant_requested_usd": float(df["grant_requested_usd"].fillna(0).sum()),
        "total_co_contribution_usd": float(df["total_co_contribution_usd"].fillna(0).sum()),
        "avg_employee_count": float(df["current_employee_count"].fillna(0).mean()),
        "total_farmers_linked": int(df["current_farmers_linked"].fillna(0).sum()),
    }
