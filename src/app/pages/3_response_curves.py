"""
Page 3 — Response Curves
==========================
Interactive visualisation of adstock decay and saturation curves:
  - Adstock decay curve: geometric vs. Weibull with slider for decay rate
  - Saturation curve: Hill function with sliders for K (half-saturation) and β
  - Current spend marker on response curve
  - mROAS annotation at current spend level
  - Per-channel fitted parameter display
"""

import numpy as np
import streamlit as st

# TODO: import transform functions and chart component
# from src.transforms.adstock import geometric_adstock, weibull_adstock
# from src.transforms.saturation import hill_saturation, hill_response_curve
# from src.app.components import response_curve_chart

# ---------------------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Response Curves | MMM Dashboard", layout="wide")
st.title("📈 Response Curves")
st.caption(
    "Explore adstock (carryover) decay and saturation (diminishing returns) "
    "for each media channel."
)

st.divider()

# ---------------------------------------------------------------------------
# Sidebar — channel & parameter controls
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("Controls")

    # TODO: populate channel options from config
    channel = st.selectbox(
        "Channel",
        ["TV", "YouTube", "Facebook", "Instagram", "Print", "Radio"],
    )

    st.subheader("Adstock Parameters")
    decay_rate = st.slider("Decay Rate (α)", 0.0, 1.0, 0.5, step=0.01)

    st.subheader("Saturation Parameters")
    K = st.slider("Half-Saturation Point (K)", 0.01, 1.0, 0.5, step=0.01)
    beta = st.slider("Hill Shape (β)", 0.1, 5.0, 2.0, step=0.1)

# ---------------------------------------------------------------------------
# Column layout: adstock | saturation
# ---------------------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"{channel} — Adstock Decay Curve")
    # TODO: compute decay impulse response
    # weeks = np.arange(0, 20)
    # impulse = geometric_adstock_impulse(decay_rate, n_weeks=20)
    # fig = px.line(x=weeks, y=impulse, labels={"x": "Weeks", "y": "Adstock Weight"})
    # st.plotly_chart(fig, use_container_width=True)
    st.info(
        f"Decay rate α = {decay_rate:.2f} → "
        f"half-life ≈ {np.log(0.5)/np.log(decay_rate + 1e-9):.1f} weeks"
        if decay_rate > 0 else "Set α > 0 to see decay.",
        icon="📉",
    )

with col2:
    st.subheader(f"{channel} — Saturation Curve")
    # TODO: compute response curve
    # x_vals, s_vals = hill_response_curve(K, beta)
    # fig = response_curve_chart(x_vals, s_vals, channel, current_spend=...)
    # st.plotly_chart(fig, use_container_width=True)
    st.info(
        f"Hill curve: K = {K:.2f}, β = {beta:.1f}. "
        "Load fitted parameters from model outputs to overlay current spend.",
        icon="📈",
    )

st.divider()

# ---------------------------------------------------------------------------
# TODO: fitted parameters table (from model outputs)
# ---------------------------------------------------------------------------
st.subheader(f"Fitted Parameters — {channel}")
# TODO: load and display fitted decay + saturation params for selected channel
st.info(
    "Fitted adstock and saturation parameters will appear here after running "
    "notebooks 02–06.",
    icon="ℹ️",
)
