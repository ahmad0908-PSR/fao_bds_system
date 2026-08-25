"""
Chart builders for the Dashboard homepage. Every function takes the
already-filtered DataFrame and returns a ready-to-render figure, so
charts stay filter-responsive automatically.
"""

import pandas as pd
import plotly.express as px
import pygal
from pygal.style import LightSolarizedStyle

from shared.constants import PHASE_1_STAGES, PHASE_2_STAGES, MATRIX_COLUMN_LABELS


def businesses_by_province(df: pd.DataFrame):
    counts = df["province"].dropna().value_counts().reset_index()
    counts.columns = ["Province", "Businesses"]
    return px.bar(counts, x="Province", y="Businesses", title="Businesses by Province")


def businesses_by_window(df: pd.DataFrame):
    counts = df["window"].dropna().value_counts().reset_index()
    counts.columns = ["Window", "Businesses"]
    return px.bar(counts, x="Window", y="Businesses", title="Businesses by Window", color="Window")


def women_youth_distribution(df: pd.DataFrame):
    data = pd.DataFrame({
        "Category": ["Women-Led", "Not Women-Led", "Youth-Inclusive", "Not Youth-Inclusive"],
        "Count": [
            (df["women_led"] == "Yes").sum(),
            (df["women_led"] != "Yes").sum(),
            (df["youth_inclusive"] == "Yes").sum(),
            (df["youth_inclusive"] != "Yes").sum(),
        ],
        "Group": ["Women Led", "Women Led", "Youth Inclusive", "Youth Inclusive"],
    })
    return px.bar(
        data, x="Group", y="Count", color="Category", barmode="stack",
        title="Women-Led & Youth-Inclusive Distribution",
    )


def verification_status_distribution(df: pd.DataFrame):
    counts = df["verification_status"].replace("", pd.NA).dropna().value_counts().reset_index()
    counts.columns = ["Verification Status", "Businesses"]
    return px.bar(counts, x="Verification Status", y="Businesses", title="Verification Status Distribution")


def financials_by_province(df: pd.DataFrame):
    grouped = df.groupby("province", dropna=True)[["grant_requested_usd", "total_co_contribution_usd"]].sum().reset_index()
    grouped = grouped.melt(id_vars="province", var_name="Metric", value_name="USD")
    grouped["Metric"] = grouped["Metric"].map({
        "grant_requested_usd": "Grant Requested",
        "total_co_contribution_usd": "Co-Contribution",
    })
    return px.bar(
        grouped, x="province", y="USD", color="Metric", barmode="group",
        title="Grant Requested & Co-Contribution by Province",
        labels={"province": "Province"},
    )


def employees_farmers_by_province(df: pd.DataFrame):
    grouped = df.groupby("province", dropna=True)[["current_employee_count", "current_farmers_linked"]].sum().reset_index()
    grouped = grouped.melt(id_vars="province", var_name="Metric", value_name="Count")
    grouped["Metric"] = grouped["Metric"].map({
        "current_employee_count": "Employees",
        "current_farmers_linked": "Farmers Linked",
    })
    return px.bar(
        grouped, x="province", y="Count", color="Metric", barmode="group",
        title="Employees & Farmers Linked by Province",
        labels={"province": "Province"},
    )


def phase_distribution(df: pd.DataFrame):
    counts = df["current_phase"].replace("", pd.NA).dropna().value_counts().reset_index()
    counts.columns = ["Phase", "Businesses"]
    if counts.empty:
        return None
    return px.pie(counts, names="Phase", values="Businesses", title="Phase Distribution", hole=0.4)


def stage_distribution(df: pd.DataFrame, phase_stages: dict):
    """Stacked bar of status counts per stage, for either PHASE_1_STAGES or PHASE_2_STAGES."""
    records = []
    for label, field in phase_stages.items():
        if field not in df.columns:
            continue
        short_label = MATRIX_COLUMN_LABELS.get(field, label)
        counts = df[field].replace("", pd.NA).dropna().value_counts()
        for status, count in counts.items():
            records.append({"Stage": short_label, "Status": status, "Count": count})

    if not records:
        return None

    chart_df = pd.DataFrame(records)
    return px.bar(
        chart_df, x="Stage", y="Count", color="Status", barmode="stack",
        title="Stage Status Distribution",
    )


def phase_progress_funnel(df: pd.DataFrame):
    """
    A sequential funnel: how many businesses have engaged (non-blank, non-"Not
    Started") each stage in order, across both phases.
    """
    all_stages = {**PHASE_1_STAGES, **PHASE_2_STAGES}
    stage_names, counts = [], []
    for label, field in all_stages.items():
        if field not in df.columns:
            continue
        engaged = df[field].apply(lambda v: v not in (None, "", "Not Started")).sum()
        stage_names.append(MATRIX_COLUMN_LABELS.get(field, label))
        counts.append(int(engaged))

    if not stage_names:
        return None

    funnel_df = pd.DataFrame({"Stage": stage_names, "Businesses": counts})
    return px.funnel(funnel_df, x="Businesses", y="Stage", title="Phase Progress Funnel (Businesses Engaged per Stage)")


def registrations_growth_pygal(df: pd.DataFrame) -> str:
    """
    Growth analytics: cumulative business registrations over time, rendered
    with Pygal (per project spec: Plotly Express + Pygal). Returns raw SVG
    as a string, to be embedded with st.components.v1.html.
    """
    if df.empty or "created_at" not in df.columns or df["created_at"].dropna().empty:
        chart = pygal.Line(style=LightSolarizedStyle, show_legend=False, x_label_rotation=45)
        chart.title = "Cumulative Business Registrations Over Time"
        chart.x_labels = ["No Data"]
        chart.add("Registrations", [0])
        return chart.render(is_unicode=True)

    monthly = (
        df.dropna(subset=["created_at"])
        .set_index("created_at")
        .resample("MS")
        .size()
        .cumsum()
    )

    chart = pygal.Line(style=LightSolarizedStyle, show_legend=False, x_label_rotation=45)
    chart.title = "Cumulative Business Registrations Over Time"
    chart.x_labels = [d.strftime("%b %Y") for d in monthly.index]
    chart.add("Cumulative Registrations", monthly.values.tolist())
    return chart.render(is_unicode=True)
