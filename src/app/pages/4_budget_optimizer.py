"""
Page 4 — Budget Optimiser
==========================
Interactive optimal budget allocation tool:
  - Input: total budget slider / numeric input
  - Input: per-channel min/max bounds
  - Output: optimal allocation bar chart vs. current allocation
  - Output: projected incremental revenue uplift
  - Output: per-channel mROAS at optimal vs. current spend
"""

import streamlit as st

# TODO: import optimiser and components
# from src.optimization.budget_optimizer import BudgetOptimizer
# from src.app.components import allocation_comparison_chart, roas_bar_chart

# ---------------------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Budget Optimiser | MMM Dashboard", layout="wide")
st.title("💰 Budget Optimiser")
st.caption(
    "Find the optimal spend allocation to maximise incremental revenue "
    "for a given total budget."
)

st.divider()

# ---------------------------------------------------------------------------
# Sidebar — budget inputs
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("Budget Inputs")

    total_budget = st.number_input(
        "Total Budget (£)",
        min_value=0,
        value=1_000_000,
        step=50_000,
        format="%d",
    )

    st.subheader("Per-Channel Constraints")
    st.caption("Optional min/max spend bounds as % of total budget.")

    # TODO: dynamic per-channel min/max sliders from config["media_channels"]
    st.info("Per-channel constraint inputs coming soon.", icon="⚙️")

    run_optimisation = st.button("🚀 Run Optimisation", type="primary")

# ---------------------------------------------------------------------------
# Main area
# ---------------------------------------------------------------------------
if run_optimisation:
    # TODO:
    # 1. Load fitted response function from outputs/models/
    # 2. Instantiate BudgetOptimizer(response_fn, channel_names, config)
    # 3. result = optimizer.optimise(total_budget, baseline_allocation, ...)
    # 4. Display allocation_comparison_chart
    # 5. Display revenue uplift metrics
    st.info("Optimisation not yet implemented. Run notebooks first.", icon="⚙️")
else:
    st.info(
        "Set a total budget in the sidebar and click **Run Optimisation** to see "
        "the recommended allocation.",
        icon="💡",
    )

st.divider()

# ---------------------------------------------------------------------------
# TODO: allocation comparison — current vs. optimal
# ---------------------------------------------------------------------------
st.subheader("Allocation: Current vs. Optimal")
# TODO: st.plotly_chart(allocation_comparison_chart(scenarios), use_container_width=True)
st.info("Allocation chart will appear here after running optimisation.", icon="ℹ️")

st.divider()

# ---------------------------------------------------------------------------
# TODO: projected revenue uplift metrics
# ---------------------------------------------------------------------------
st.subheader("Projected Impact")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Current Revenue (Incremental)", "– –")
with col2:
    st.metric("Projected Revenue (Optimal)", "– –")
with col3:
    st.metric("Revenue Uplift", "– –", delta="– –")
