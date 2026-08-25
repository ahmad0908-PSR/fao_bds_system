"""
Page: Progress Matrix.

A color-coded master tracking grid — one row per business, grouped column
headers per phase, each stage cell colored by its current status. Styled
after the reference FAO-EFSP-BDS PROGRESS screenshot.
"""

import sys
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
from st_aggrid import AgGrid, JsCode

from app_dashboard.data_loader import load_businesses_df
from app_dashboard.filters import render_and_apply_filters
from shared.constants import (
    MATRIX_COLUMN_LABELS,
    MATRIX_GROUP_1_LABEL,
    MATRIX_GROUP_1_FIELDS,
    MATRIX_GROUP_2_LABEL,
    MATRIX_GROUP_2_FIELDS,
    STATUS_COLOR_MAP,
    DEFAULT_CELL_COLOR,
)

st.set_page_config(page_title="Progress Matrix", page_icon="🧮", layout="wide")
st.title("Progress Matrix")
st.caption("Master tracking grid — one row per business, color-coded by current stage status.")

df = load_businesses_df()
if df.empty:
    st.warning("No businesses have been registered yet.")
    st.stop()

filtered_df = render_and_apply_filters(df)

if filtered_df.empty:
    st.info("No businesses match the current filters.")
    st.stop()

# ----------------------------------------------------------------
# Build the display DataFrame: fixed identity columns + all matrix fields
# ----------------------------------------------------------------
display_df = filtered_df.reset_index(drop=True).copy()
display_df.insert(0, "row_num", display_df.index + 1)

fixed_columns = ["row_num", "business_id_fao", "enterprise_name", "province", "window", "women_led"]
matrix_fields = MATRIX_GROUP_1_FIELDS + MATRIX_GROUP_2_FIELDS
grid_df = display_df[fixed_columns + matrix_fields].fillna("")

# ----------------------------------------------------------------
# Cell color styling (shared JS function driven by STATUS_COLOR_MAP)
# ----------------------------------------------------------------
color_map_json = json.dumps(STATUS_COLOR_MAP)
cell_style_js = JsCode(f"""
function(params) {{
    const colorMap = {color_map_json};
    const value = params.value || "";
    const bg = (value in colorMap) ? colorMap[value] : "{DEFAULT_CELL_COLOR}";
    return {{backgroundColor: bg, color: "#1a1a1a", fontWeight: "500"}};
}}
""")

def stage_column_def(field: str) -> dict:
    return {
        "headerName": MATRIX_COLUMN_LABELS.get(field, field),
        "field": field,
        "cellStyle": cell_style_js,
        "minWidth": 150,
        "sortable": True,
        "filter": True,
    }

column_defs = [
    {"headerName": "#", "field": "row_num", "width": 60, "pinned": "left"},
    {"headerName": "App ID", "field": "business_id_fao", "width": 110, "pinned": "left"},
    {"headerName": "Enterprise Name", "field": "enterprise_name", "width": 240, "pinned": "left"},
    {"headerName": "Province", "field": "province", "width": 120, "pinned": "left"},
    {"headerName": "Window", "field": "window", "width": 90, "pinned": "left"},
    {"headerName": "Women Led", "field": "women_led", "width": 100, "pinned": "left"},
    {
        "headerName": MATRIX_GROUP_1_LABEL,
        "children": [stage_column_def(f) for f in MATRIX_GROUP_1_FIELDS],
    },
    {
        "headerName": MATRIX_GROUP_2_LABEL,
        "children": [stage_column_def(f) for f in MATRIX_GROUP_2_FIELDS],
    },
]

grid_options = {
    "columnDefs": column_defs,
    "defaultColDef": {"resizable": True, "sortable": True, "filter": True},
    "headerHeight": 36,
    "groupHeaderHeight": 36,
    "suppressMovableColumns": True,
    "domLayout": "normal",
}

custom_css = {
    ".ag-header": {"background-color": "#1f3864 !important"},
    ".ag-header-cell-label": {"color": "white !important", "font-weight": "600"},
    ".ag-header-group-cell-label": {"color": "white !important", "font-weight": "700", "justify-content": "center"},
    ".ag-header-cell": {"border-color": "#3a5680 !important"},
    ".ag-row-even": {"background-color": "#f7f9fc"},
    ".ag-cell": {"display": "flex", "align-items": "center"},
}

AgGrid(
    grid_df,
    gridOptions=grid_options,
    height=650,
    allow_unsafe_jscode=True,
    theme="balham",
    custom_css=custom_css,
    fit_columns_on_grid_load=False,
)

st.caption(
    "Tip: use the column filter icons or the global sidebar filters to narrow this grid. "
    "Cell colors follow the status legend used across the system."
)

with st.expander("Status Color Legend"):
    legend_cols = st.columns(4)
    for i, (status, color) in enumerate(STATUS_COLOR_MAP.items()):
        if not status:
            continue
        with legend_cols[i % 4]:
            st.markdown(
                f"<div style='background-color:{color};padding:6px 10px;border-radius:4px;"
                f"margin-bottom:4px;font-size:13px;'>{status}</div>",
                unsafe_allow_html=True,
            )
