"""
Page 1 — Overview
==================
Displays top-level marketing KPI summary:
  - Total Sales (actual vs. model fit)
  - Total Media Spend
  - Overall ROAS
  - Baseline vs. Media-driven revenue split (pie)
  - Data coverage summary (date range, geographies, brands)
"""

import streamlit as st

# TODO: import shared components
# from src.app.components import metric_card, stacked_area_chart
# from src.data_prep import load_config, load_data

# ---------------------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Overview | MMM Dashboard", layout="wide")
st.title("📊 Overview")
st.caption("Total sales performance, media spend, and baseline vs. media split.")

st.divider()

# ---------------------------------------------------------------------------
# TODO: load model outputs
# ---------------------------------------------------------------------------
# config = load_config()
# decomp_df = pd.read_parquet("outputs/models/decomposition.parquet")

# ---------------------------------------------------------------------------
# TODO: KPI metric cards (row 1)
# ---------------------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    # TODO: metric_card("Total Sales", "£XX.XM", "+X% YoY")
    st.metric("Total Sales", "– –", help="Load model outputs to populate.")

with col2:
    # TODO: metric_card("Total Media Spend", "£XX.XM", "")
    st.metric("Total Media Spend", "– –")

with col3:
    # TODO: metric_card("Overall ROAS", "X.Xx", "")
    st.metric("Overall ROAS", "– –")

with col4:
    # TODO: metric_card("Media-Driven Revenue Share", "XX%", "")
    st.metric("Media-Driven Revenue Share", "– –")

st.divider()

# ---------------------------------------------------------------------------
# TODO: stacked area decomposition chart
# ---------------------------------------------------------------------------
st.subheader("Sales Over Time — Decomposition")
# TODO: st.plotly_chart(stacked_area_chart(decomp_df), use_container_width=True)
st.info("Run notebooks 01–07 to generate decomposition outputs.", icon="ℹ️")

st.divider()

# ---------------------------------------------------------------------------
# TODO: data coverage summary table
# ---------------------------------------------------------------------------
st.subheader("Data Coverage")
# TODO: display date range, geo count, brand count, channel list
st.info("Data coverage summary will appear here after loading outputs.", icon="ℹ️")
