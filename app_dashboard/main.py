"""
FAO EFSP - Dashboard & Monitoring System (Application 2)
Read-only. No data entry happens in this app.

Run with:
    streamlit run app_dashboard/main.py
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
import streamlit.components.v1 as components

from app_dashboard.data_loader import load_businesses_df
from app_dashboard.filters import render_and_apply_filters
from app_dashboard.kpi import compute_kpis
from app_dashboard import charts
from shared.constants import PHASE_1_STAGES, PHASE_2_STAGES

st.set_page_config(page_title="FAO EFSP — Dashboard", page_icon="📊", layout="wide")

# ----------------------------------------------------------------
# Header
# ----------------------------------------------------------------
ASSETS_DIR = ROOT_DIR / "assets"
col_logo1, col_title, col_logo2 = st.columns([1, 3, 1])
with col_logo1:
    fao_logo = ASSETS_DIR / "fao_logo.png"
    if fao_logo.exists():
        st.image(str(fao_logo), width=100)
with col_title:
    st.markdown(
        "<h2 style='text-align:center;margin-bottom:0;'>FAO EFSP — Business Development Support</h2>"
        "<p style='text-align:center;color:gray;margin-top:0;'>Monitoring & Reporting Dashboard</p>",
        unsafe_allow_html=True,
    )
with col_logo2:
    project_logo = ASSETS_DIR / "project_logo.png"
    if project_logo.exists():
        st.image(str(project_logo), width=100)



st.divider()

# ----------------------------------------------------------------
# Load + filter data
# ----------------------------------------------------------------
df = load_businesses_df()

if df.empty:
    st.warning("No businesses have been registered yet. Add some in the Data Entry app first.")
    st.stop()

filtered_df = render_and_apply_filters(df)
st.caption(f"Showing {len(filtered_df)} of {len(df)} businesses based on current filters.")

# ----------------------------------------------------------------
# KPI Cards
# ----------------------------------------------------------------
kpis = compute_kpis(filtered_df)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Businesses", kpis["total_businesses"])
c2.metric("Women-Led", kpis["women_led_count"])
c3.metric("Youth-Inclusive", kpis["youth_inclusive_count"])
c4.metric("Avg. Employees / Business", f"{kpis['avg_employee_count']:.1f}")

c5, c6, c7 = st.columns(3)
c5.metric("Total Grant Requested (USD)", f"${kpis['total_grant_requested_usd']:,.0f}")
c6.metric("Total Co-Contribution (USD)", f"${kpis['total_co_contribution_usd']:,.0f}")
c7.metric("Total Farmers Linked", kpis["total_farmers_linked"])

st.divider()

# ----------------------------------------------------------------
# Charts
# ----------------------------------------------------------------
st.subheader("Distribution")
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(charts.businesses_by_province(filtered_df), use_container_width=True)
with col2:
    st.plotly_chart(charts.businesses_by_window(filtered_df), use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(charts.women_youth_distribution(filtered_df), use_container_width=True)
with col2:
    st.plotly_chart(charts.verification_status_distribution(filtered_df), use_container_width=True)

st.subheader("Resources")
st.plotly_chart(charts.financials_by_province(filtered_df), use_container_width=True)
st.plotly_chart(charts.employees_farmers_by_province(filtered_df), use_container_width=True)

st.subheader("Phase & Stage Progress")
phase_fig = charts.phase_distribution(filtered_df)
if phase_fig:
    st.plotly_chart(phase_fig, use_container_width=True)
else:
    st.info("No businesses have a Current Phase set yet.")

col1, col2 = st.columns(2)
with col1:
    fig1 = charts.stage_distribution(filtered_df, PHASE_1_STAGES)
    if fig1:
        st.plotly_chart(fig1, use_container_width=True)
with col2:
    fig2 = charts.stage_distribution(filtered_df, PHASE_2_STAGES)
    if fig2:
        st.plotly_chart(fig2, use_container_width=True)

funnel_fig = charts.phase_progress_funnel(filtered_df)
if funnel_fig:
    st.plotly_chart(funnel_fig, use_container_width=True)

st.subheader("Growth Analytics")
svg = charts.registrations_growth_pygal(filtered_df)
components.html(svg, height=420, scrolling=False)
