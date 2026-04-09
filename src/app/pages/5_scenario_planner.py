"""
Page 5 — Scenario Planner
==========================
Compare three budget scenarios side-by-side:
  - Flat (same total budget)
  - +10% budget increase
  - +25% budget increase

For each scenario, displays:
  - Optimal allocation bar chart
  - Projected incremental revenue
  - Revenue uplift vs. current spend
  - Per-channel mROAS at optimal allocation
"""

import streamlit as st

# TODO: import optimiser and components
# from src.optimization.budget_optimizer import BudgetOptimizer
# from src.app.components import allocation_comparison_chart

# ---------------------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Scenario Planner | MMM Dashboard", layout="wide")
st.title("🔮 Scenario Planner")
st.caption(
    "Compare budget scenarios side-by-side: Flat / +10% / +25%. "
    "All scenarios use the same constrained optimisation engine."
)

st.divider()

# ---------------------------------------------------------------------------
# Sidebar — baseline spend inputs
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("Baseline Spend")
    baseline_budget = st.number_input(
        "Current Total Budget (£)",
        min_value=0,
        value=1_000_000,
        step=50_000,
        format="%d",
    )

    st.subheader("Custom Scenarios")
    st.caption("Define up to 3 budget multipliers.")
    # TODO: dynamic scenario multiplier inputs
    mult_1 = st.number_input("Scenario 1 Multiplier", value=1.0, step=0.05)
    mult_2 = st.number_input("Scenario 2 Multiplier", value=1.10, step=0.05)
    mult_3 = st.number_input("Scenario 3 Multiplier", value=1.25, step=0.05)

    run_scenarios = st.button("▶️ Run All Scenarios", type="primary")

# ---------------------------------------------------------------------------
# Main area
# ---------------------------------------------------------------------------
if run_scenarios:
    # TODO:
    # 1. Load fitted response function from outputs/models/
    # 2. Instantiate BudgetOptimizer
    # 3. result = optimizer.run_scenarios(
    #        baseline_allocation,
    #        scenarios={"Flat": mult_1, f"+{(mult_2-1)*100:.0f}%": mult_2,
    #                   f"+{(mult_3-1)*100:.0f}%": mult_3}
    #    )
    # 4. Display 3-column layout with scenario cards

    col1, col2, col3 = st.columns(3)
    scenario_labels = [
        f"Scenario 1 (×{mult_1:.2f})",
        f"Scenario 2 (×{mult_2:.2f})",
        f"Scenario 3 (×{mult_3:.2f})",
    ]
    for col, label in zip([col1, col2, col3], scenario_labels):
        with col:
            st.subheader(label)
            # TODO: render allocation chart and metrics
            st.info("Coming soon.", icon="⚙️")
else:
    st.info(
        "Configure scenarios in the sidebar and click **Run All Scenarios**.",
        icon="💡",
    )

st.divider()

# ---------------------------------------------------------------------------
# TODO: scenario comparison summary table
# ---------------------------------------------------------------------------
st.subheader("Scenario Comparison Summary")
# TODO: st.dataframe(scenario_comparison.comparison_table, use_container_width=True)
st.info(
    "Side-by-side scenario comparison table will appear after running scenarios.",
    icon="ℹ️",
)
