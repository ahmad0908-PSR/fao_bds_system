"""
Global filters, rendered in the sidebar on every Dashboard page.

All widgets use fixed `key=` values, which Streamlit backs with
st.session_state automatically — since session_state is shared across
every page in a multipage app, a filter selection made on the Dashboard
Homepage is still applied when you navigate to the Progress Matrix, the
Map, etc. Call render_and_apply_filters(df) at the top of every page.
"""

import pandas as pd
import streamlit as st

from shared.constants import (
    WINDOWS,
    AFGHANISTAN_PROVINCES,
    YES_NO_OPTIONS,
    PHASE_OPTIONS,
    PHASE_1_STAGES,
    PHASE_2_STAGES,
    VERIFICATION_STATUS_OPTIONS,
    STAGE_FIELD_OPTIONS,
)

# Combined {label: field_name} across both phases, used when no phase is selected
ALL_STAGES = {**PHASE_1_STAGES, **PHASE_2_STAGES}


def render_and_apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Renders the sidebar filter controls and returns the filtered DataFrame."""
    st.sidebar.header("Global Filters")

    if df.empty:
        st.sidebar.info("No data yet.")
        return df

    provinces = st.sidebar.multiselect(
        "Province", options=sorted(df["province"].dropna().unique().tolist()), key="filter_province"
    )
    windows = st.sidebar.multiselect("Window", options=WINDOWS, key="filter_window")
    women_led = st.sidebar.selectbox("Women Led", YES_NO_OPTIONS, key="filter_women_led")
    youth_inclusive = st.sidebar.selectbox("Youth Inclusive", YES_NO_OPTIONS, key="filter_youth_inclusive")
    verification_status = st.sidebar.multiselect(
        "Verification Status", options=[v for v in VERIFICATION_STATUS_OPTIONS if v], key="filter_verification_status"
    )

    st.sidebar.markdown("**Phase / Stage**")
    phases = st.sidebar.multiselect("Phase", options=[p for p in PHASE_OPTIONS if p], key="filter_phase")

    # Stage options depend on which phase(s) are selected
    if phases and "Phase 1: Pre-Qualification Verification" in phases and "Phase 2: Business Development Support" not in phases:
        stage_choices = PHASE_1_STAGES
    elif phases and "Phase 2: Business Development Support" in phases and "Phase 1: Pre-Qualification Verification" not in phases:
        stage_choices = PHASE_2_STAGES
    else:
        stage_choices = ALL_STAGES

    stages = st.sidebar.multiselect("Stage", options=list(stage_choices.keys()), key="filter_stage")

    # If specific stages are selected, let the user narrow to specific statuses for those stages
    stage_status_filter = []
    if stages:
        stage_fields = [stage_choices[s] for s in stages]
        possible_statuses = sorted({
            status for field in stage_fields for status in STAGE_FIELD_OPTIONS.get(field, []) if status
        })
        stage_status_filter = st.sidebar.multiselect(
            "Stage Status (optional — leave blank to include any status except 'Not Started')",
            options=possible_statuses, key="filter_stage_status",
        )

    if st.sidebar.button("Reset Filters", use_container_width=True):
        for key in [
            "filter_province", "filter_window", "filter_women_led", "filter_youth_inclusive",
            "filter_verification_status", "filter_phase", "filter_stage", "filter_stage_status",
        ]:
            st.session_state.pop(key, None)
        st.rerun()

    # ------------------------------------------------------------
    # Apply filters
    # ------------------------------------------------------------
    filtered = df.copy()

    if provinces:
        filtered = filtered[filtered["province"].isin(provinces)]
    if windows:
        filtered = filtered[filtered["window"].isin(windows)]
    if women_led:
        filtered = filtered[filtered["women_led"] == women_led]
    if youth_inclusive:
        filtered = filtered[filtered["youth_inclusive"] == youth_inclusive]
    if verification_status:
        filtered = filtered[filtered["verification_status"].isin(verification_status)]
    if phases:
        filtered = filtered[filtered["current_phase"].isin(phases)]

    if stages:
        stage_fields = [stage_choices[s] for s in stages]
        if stage_status_filter:
            mask = pd.Series(False, index=filtered.index)
            for field in stage_fields:
                if field in filtered.columns:
                    mask = mask | filtered[field].isin(stage_status_filter)
            filtered = filtered[mask]
        else:
            # No specific status chosen -> just "has engaged this stage"
            # (status present and not the blank/Not Started default)
            mask = pd.Series(False, index=filtered.index)
            for field in stage_fields:
                if field in filtered.columns:
                    mask = mask | (~filtered[field].isin(["", "Not Started", None]))
            filtered = filtered[mask]

    return filtered
