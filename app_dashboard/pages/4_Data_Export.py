"""
Page: Data Export.
Exports the currently filtered business list as Excel (.xlsx) or a
summary PDF report. Respects global filters.
"""

import sys
from io import BytesIO
from pathlib import Path
from datetime import datetime

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import pandas as pd
import streamlit as st
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

from app_dashboard.data_loader import load_businesses_df
from app_dashboard.filters import render_and_apply_filters
from app_dashboard.kpi import compute_kpis

st.set_page_config(page_title="Data Export", page_icon="📤", layout="wide")
st.title("Data Export")
st.caption("Exports respect the current global filters.")

df = load_businesses_df()
if df.empty:
    st.warning("No businesses have been registered yet.")
    st.stop()

filtered_df = render_and_apply_filters(df)

if filtered_df.empty:
    st.info("No businesses match the current filters — nothing to export.")
    st.stop()

st.write(f"**{len(filtered_df)}** businesses match the current filters and will be included in the export.")
st.dataframe(filtered_df.head(20), use_container_width=True, hide_index=True)
if len(filtered_df) > 20:
    st.caption(f"Showing first 20 rows of {len(filtered_df)} — the full set is included in the export files.")

export_df = filtered_df.drop(columns=["id"], errors="ignore")

# ----------------------------------------------------------------
# Excel export
# ----------------------------------------------------------------
def build_excel(df) -> bytes:
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Businesses")
        worksheet = writer.sheets["Businesses"]
        for i, col in enumerate(df.columns):
            max_len = max(df[col].astype(str).map(len).max() if len(df) else 0, len(col)) + 2
            worksheet.set_column(i, i, min(max_len, 40))
    buffer.seek(0)
    return buffer.getvalue()


# ----------------------------------------------------------------
# PDF export (summary report)
# ----------------------------------------------------------------
def build_pdf(df, kpis: dict) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("FAO EFSP — BDS Tracking Summary Report", styles["Title"]))
    elements.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    kpi_rows = [
        ["Total Businesses", kpis["total_businesses"]],
        ["Women-Led", kpis["women_led_count"]],
        ["Youth-Inclusive", kpis["youth_inclusive_count"]],
        ["Total Grant Requested (USD)", f"{kpis['total_grant_requested_usd']:,.2f}"],
        ["Total Co-Contribution (USD)", f"{kpis['total_co_contribution_usd']:,.2f}"],
        ["Avg. Employees / Business", f"{kpis['avg_employee_count']:.1f}"],
        ["Total Farmers Linked", kpis["total_farmers_linked"]],
    ]
    kpi_table = Table(kpi_rows, colWidths=[220, 150])
    kpi_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#1f3864")),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(kpi_table)
    elements.append(Spacer(1, 20))

    elements.append(Paragraph(f"Business List ({len(df)} records)", styles["Heading2"]))
    elements.append(Spacer(1, 6))

    summary_cols = ["business_id", "enterprise_name", "province", "window", "current_phase", "verification_status"]
    summary_cols = [c for c in summary_cols if c in df.columns]
    table_data = [["ID", "Enterprise Name", "Province", "Window", "Phase", "Verification Status"]]
    for row in df[summary_cols].itertuples(index=False):
        table_data.append([str(v) if v else "—" for v in row])

    data_table = Table(table_data, repeatRows=1, colWidths=[70, 200, 90, 60, 190, 130])
    data_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f3864")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0f4fa")]),
        ("PADDING", (0, 0), (-1, -1), 4),
    ]))
    elements.append(data_table)

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()


st.divider()
col1, col2 = st.columns(2)

with col1:
    st.subheader("Excel Export")
    excel_bytes = build_excel(export_df)
    st.download_button(
        "Download Excel (.xlsx)",
        data=excel_bytes,
        file_name=f"bds_businesses_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )

with col2:
    st.subheader("PDF Summary Report")
    kpis = compute_kpis(filtered_df)
    pdf_bytes = build_pdf(export_df, kpis)
    st.download_button(
        "Download PDF Report",
        data=pdf_bytes,
        file_name=f"bds_summary_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
        mime="application/pdf",
        use_container_width=True,
    )
