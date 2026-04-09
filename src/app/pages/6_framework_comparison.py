"""
Page 6 — Framework Comparison
================================
Side-by-side ROAS estimates from all four MMM frameworks:
  - Classical Constrained Ridge (Python)
  - Bayesian PyMC-Marketing (Python)
  - Meta Robyn (R, results imported as CSV)
  - Google Meridian (Python)

Displays:
  - Grouped bar chart: ROAS per channel × framework
  - Uncertainty ribbons (Bayesian frameworks only)
  - Convergence/agreement metrics across frameworks
  - Qualitative framework comparison table
"""

import streamlit as st

# TODO: import chart components
# from src.app.components import roas_bar_chart

# ---------------------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Framework Comparison | MMM Dashboard", layout="wide")
st.title("⚖️ Framework Comparison")
st.caption(
    "Compare ROAS estimates from Classical, Bayesian PyMC-Marketing, "
    "Meta Robyn, and Google Meridian."
)

st.divider()

# ---------------------------------------------------------------------------
# Sidebar — display options
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("Display Options")
    # TODO: checkboxes to toggle which frameworks to show
    show_classical = st.checkbox("Classical Ridge", value=True)
    show_pymc = st.checkbox("Bayesian (PyMC-Marketing)", value=True)
    show_robyn = st.checkbox("Meta Robyn", value=True)
    show_meridian = st.checkbox("Google Meridian", value=True)

    show_uncertainty = st.checkbox("Show Uncertainty Bands", value=True)
    st.caption("Only applicable to Bayesian frameworks.")

# ---------------------------------------------------------------------------
# TODO: load ROAS outputs from all frameworks
# ---------------------------------------------------------------------------
# classical_roas = pd.read_parquet("outputs/models/classical_roas.parquet")
# pymc_roas      = pd.read_parquet("outputs/models/bayesian_roas.parquet")
# robyn_roas     = pd.read_csv("outputs/models/robyn_roas.csv")
# meridian_roas  = pd.read_parquet("outputs/models/meridian_roas.parquet")

# ---------------------------------------------------------------------------
# TODO: grouped ROAS comparison chart
# ---------------------------------------------------------------------------
st.subheader("ROAS by Channel and Framework")
# TODO: st.plotly_chart(roas_comparison_chart(...), use_container_width=True)
st.info(
    "Run all notebooks (02, 04, 05, 06) to populate framework ROAS outputs.",
    icon="ℹ️",
)

st.divider()

# ---------------------------------------------------------------------------
# TODO: framework agreement metrics
# ---------------------------------------------------------------------------
st.subheader("Cross-Framework Agreement")
# TODO: compute pairwise Pearson correlation of ROAS vectors
# TODO: display correlation heatmap
st.info("Framework agreement heatmap will appear here.", icon="ℹ️")

st.divider()

# ---------------------------------------------------------------------------
# Qualitative framework comparison table (static reference)
# ---------------------------------------------------------------------------
st.subheader("Framework Characteristics")
st.markdown(
    """
    | Framework | Type | Uncertainty | Geo-Level | Speed | Key Strength |
    |-----------|------|-------------|-----------|-------|--------------|
    | Classical Ridge | Frequentist | ✗ | ✗ | ⚡ Fast | Interpretable, deployable |
    | PyMC-Marketing | Bayesian | ✓ | Partial | 🐢 Slow | Full posterior, lift-test calibration |
    | Meta Robyn | Bayesian Ridge + EA | Partial | ✗ | ⚡ Fast | Pareto-optimal model set |
    | Google Meridian | Bayesian Hierarchical | ✓ | ✓ | 🐢 Slow | Native geo, Weibull adstock |
    """
)
