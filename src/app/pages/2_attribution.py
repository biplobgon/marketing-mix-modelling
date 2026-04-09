"""
Page 2 — Channel Attribution
=============================
Displays media channel contribution breakdown:
  - Waterfall chart: Baseline → each channel → Total
  - Stacked area chart: contribution over time per channel
  - Attribution table: absolute contribution + % share per channel
  - Framework selector: view results from Classical / Bayesian / Meridian
"""

import streamlit as st

# TODO: import shared components
# from src.app.components import waterfall_chart, stacked_area_chart

# ---------------------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Attribution | MMM Dashboard", layout="wide")
st.title("🎯 Channel Attribution")
st.caption("Sales decomposition: how much of revenue is driven by each media channel.")

st.divider()

# ---------------------------------------------------------------------------
# TODO: sidebar — framework selector
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("Settings")
    # framework = st.selectbox(
    #     "MMM Framework",
    #     ["Classical (Ridge)", "Bayesian (PyMC)", "Google Meridian"],
    # )
    # geo_filter = st.multiselect("Geography", options=config["geographies"])
    st.info("Framework selector coming soon.")

# ---------------------------------------------------------------------------
# TODO: load decomposition results for selected framework
# ---------------------------------------------------------------------------
# decomp_df = load_decomposition(framework, geo_filter)

# ---------------------------------------------------------------------------
# TODO: waterfall chart
# ---------------------------------------------------------------------------
st.subheader("Sales Decomposition Waterfall")
# TODO: st.plotly_chart(waterfall_chart(components), use_container_width=True)
st.info("Run notebooks 01–07 then reload to see the decomposition waterfall.", icon="ℹ️")

st.divider()

# ---------------------------------------------------------------------------
# TODO: stacked area chart
# ---------------------------------------------------------------------------
st.subheader("Channel Contributions Over Time")
# TODO: st.plotly_chart(stacked_area_chart(decomp_df), use_container_width=True)
st.info("Time-series decomposition chart will appear here.", icon="ℹ️")

st.divider()

# ---------------------------------------------------------------------------
# TODO: attribution summary table
# ---------------------------------------------------------------------------
st.subheader("Attribution Summary")
# TODO: st.dataframe(attribution_table, use_container_width=True)
st.info("Attribution table will appear here.", icon="ℹ️")
