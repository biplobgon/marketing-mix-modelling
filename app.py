"""
app.py — Streamlit Multi-Page Dashboard Entry Point
====================================================
Marketing Mix Modelling Interactive Dashboard

Launch:
    streamlit run app.py

Pages (defined in src/app/pages/):
    1_overview.py           — Sales & spend summary KPIs
    2_attribution.py        — Channel contribution waterfall
    3_response_curves.py    — Adstock decay & saturation curves
    4_budget_optimizer.py   — Optimal spend allocation
    5_scenario_planner.py   — Multi-scenario comparison
    6_framework_comparison.py — ROAS across all 4 frameworks
"""

import streamlit as st

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="MMM Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Landing page
# ---------------------------------------------------------------------------
st.title("📊 Marketing Mix Modelling Dashboard")
st.caption("End-to-end MMM: Classical · PyMC-Marketing · Meta Robyn · Google Meridian")

st.markdown(
    """
    Use the **sidebar** to navigate between dashboard pages:

    | Page | Description |
    |------|-------------|
    | 📊 Overview | Total sales, media spend, overall ROAS |
    | 🎯 Channel Attribution | Waterfall & stacked contribution chart |
    | 📈 Response Curves | Adstock decay slider + saturation curve per channel |
    | 💰 Budget Optimiser | Input budget → optimal allocation & projected sales |
    | 🔮 Scenario Planner | Compare 3 budget scenarios side-by-side |
    | ⚖️ Framework Comparison | ROAS estimates from all 4 frameworks |
    """
)

st.divider()
st.info(
    "**Getting started:** Run notebooks `01` → `09` first to generate model outputs, "
    "then relaunch this dashboard to load results from `outputs/models/`.",
    icon="ℹ️",
)
