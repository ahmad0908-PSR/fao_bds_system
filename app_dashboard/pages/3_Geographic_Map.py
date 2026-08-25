"""
Page: Geographic Mapping.
Plots businesses with valid Latitude/Longitude on a Folium map, clustered
and colored by Current Phase. Respects global filters.

NOTE: This shows point markers only. A true province-boundary choropleth
would require an Afghanistan provinces GeoJSON file, which isn't bundled
here — if you have one (or want me to source one), I can add a province
shading layer on top of this.
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import folium
import pandas as pd
import streamlit as st
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

from app_dashboard.data_loader import load_businesses_df
from app_dashboard.filters import render_and_apply_filters

st.set_page_config(page_title="Geographic Map", page_icon="🗺️", layout="wide")
st.title("Geographic Mapping")

df = load_businesses_df()
if df.empty:
    st.warning("No businesses have been registered yet.")
    st.stop()

filtered_df = render_and_apply_filters(df)

mappable = filtered_df.dropna(subset=["latitude", "longitude"])
mappable = mappable[(mappable["latitude"] != 0) & (mappable["longitude"] != 0)]

st.caption(
    f"{len(mappable)} of {len(filtered_df)} filtered businesses have coordinates set "
    "and can be plotted."
)

if mappable.empty:
    st.info("No businesses in the current filter have Latitude/Longitude set.")
    st.stop()

PHASE_COLORS = {
    "Phase 1: Pre-Qualification Verification": "blue",
    "Phase 2: Business Development Support": "green",
}
DEFAULT_COLOR = "gray"

center_lat = mappable["latitude"].mean()
center_lon = mappable["longitude"].mean()

fmap = folium.Map(location=[center_lat, center_lon], zoom_start=6, tiles="CartoDB positron")
cluster = MarkerCluster().add_to(fmap)

for row in mappable.itertuples():
    color = PHASE_COLORS.get(row.current_phase, DEFAULT_COLOR)
    popup_html = (
        f"<b>{row.enterprise_name or 'Unnamed'}</b><br>"
        f"ID: {row.business_id}<br>"
        f"Province: {row.province or '—'}<br>"
        f"Window: {row.window or '—'}<br>"
        f"Phase: {row.current_phase or 'Not Set'}"
    )
    folium.Marker(
        location=[row.latitude, row.longitude],
        popup=folium.Popup(popup_html, max_width=250),
        tooltip=row.enterprise_name or row.business_id,
        icon=folium.Icon(color=color, icon="briefcase", prefix="fa"),
    ).add_to(cluster)

legend_html = """
<div style="position: fixed; bottom: 30px; left: 30px; z-index: 9999;
            background: white; padding: 10px 14px; border-radius: 6px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.3); font-size: 13px;">
  <b>Legend</b><br>
  <span style="color:blue;">&#9679;</span> Phase 1: Pre-Qualification<br>
  <span style="color:green;">&#9679;</span> Phase 2: BDS<br>
  <span style="color:gray;">&#9679;</span> Phase Not Set
</div>
"""
fmap.get_root().html.add_child(folium.Element(legend_html))

st_folium(fmap, use_container_width=True, height=600, returned_objects=[])

st.divider()
st.subheader("Businesses Plotted")
st.dataframe(
    mappable[["business_id", "enterprise_name", "province", "window", "current_phase", "latitude", "longitude"]],
    use_container_width=True,
    hide_index=True,
)
