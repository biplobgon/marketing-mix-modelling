"""
src/app/components.py
======================
Shared reusable Streamlit / Plotly chart components for the MMM dashboard.

All chart functions return Plotly figure objects (go.Figure / px.*) so they
can be rendered by individual page scripts with st.plotly_chart().
"""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


# ---------------------------------------------------------------------------
# 1. Sales Decomposition Waterfall Chart
# ---------------------------------------------------------------------------

def waterfall_chart(
    components: dict[str, float],
    title: str = "Sales Decomposition Waterfall",
) -> go.Figure:
    """Render a waterfall chart of sales decomposition components.

    Args:
        components: Ordered dict mapping component name → incremental value.
                    Example: {"Baseline": 60000, "TV": 8000, "Facebook": 5000}
        title: Chart title.

    Returns:
        Plotly Figure object.

    TODO:
        - Create go.Waterfall trace
        - Set measure types: 'absolute' for baseline, 'relative' for channels
        - Add a 'total' bar at the end
        - Style with MMM colour palette
    """
    # TODO: implement waterfall chart
    raise NotImplementedError("waterfall_chart is not yet implemented.")


# ---------------------------------------------------------------------------
# 2. Stacked Area Decomposition Chart
# ---------------------------------------------------------------------------

def stacked_area_chart(
    decomp_df: pd.DataFrame,
    date_col: str = "date",
    title: str = "Sales Decomposition Over Time",
) -> go.Figure:
    """Render a stacked area chart of sales contributions over time.

    Args:
        decomp_df: DataFrame with date column + one column per component.
                   Example columns: date, baseline, tv, youtube, facebook, ...
        date_col: Name of the date column.
        title: Chart title.

    Returns:
        Plotly Figure object.

    TODO:
        - Use go.Figure() with add_trace(go.Scatter(stackgroup='one')) per component
        - Apply consistent colour mapping across pages
        - Add hover template with date + contribution values
    """
    # TODO: implement stacked area chart
    raise NotImplementedError("stacked_area_chart is not yet implemented.")


# ---------------------------------------------------------------------------
# 3. ROAS Bar Chart
# ---------------------------------------------------------------------------

def roas_bar_chart(
    roas_df: pd.DataFrame,
    channel_col: str = "channel",
    roas_col: str = "mean_roas",
    error_col: str | None = None,
    title: str = "Channel ROAS",
) -> go.Figure:
    """Render a horizontal bar chart of ROAS by channel.

    Args:
        roas_df: DataFrame with channel names and ROAS values.
        channel_col: Column name for channel identifiers.
        roas_col: Column name for ROAS values.
        error_col: Optional column for ROAS uncertainty (±1 SD or HDI width).
        title: Chart title.

    Returns:
        Plotly Figure object.

    TODO:
        - Use go.Bar with orientation='h'
        - Sort bars by ROAS descending
        - Add error bars if error_col is provided
        - Colour-code by ROAS tier (green / amber / red)
    """
    # TODO: implement ROAS bar chart
    raise NotImplementedError("roas_bar_chart is not yet implemented.")


# ---------------------------------------------------------------------------
# 4. Response / Saturation Curve
# ---------------------------------------------------------------------------

def response_curve_chart(
    spend: "ArrayLike",
    response: "ArrayLike",
    channel_name: str,
    current_spend: float | None = None,
    title: str | None = None,
) -> go.Figure:
    """Render a response / saturation curve for a single channel.

    Args:
        spend: Array of spend values (x-axis).
        response: Array of saturation-transformed response values (y-axis).
        channel_name: Channel name for labelling.
        current_spend: Optional vertical line marking current spend level.
        title: Chart title. Defaults to f"{channel_name} Response Curve".

    Returns:
        Plotly Figure object.

    TODO:
        - Plot smooth response curve
        - Add vertical dashed line at current_spend if provided
        - Mark the half-saturation point K
        - Add annotation for current spend ROAS and mROAS
    """
    # TODO: implement response curve chart
    raise NotImplementedError("response_curve_chart is not yet implemented.")


# ---------------------------------------------------------------------------
# 5. Budget Allocation Comparison (Bar chart)
# ---------------------------------------------------------------------------

def allocation_comparison_chart(
    scenarios: dict[str, dict[str, float]],
    title: str = "Budget Allocation by Scenario",
) -> go.Figure:
    """Grouped bar chart comparing spend allocation across scenarios.

    Args:
        scenarios: Dict mapping scenario_name → {channel: spend}.
                   Example: {"Baseline": {"TV": 500, "FB": 300},
                              "Optimised": {"TV": 400, "FB": 400}}
        title: Chart title.

    Returns:
        Plotly Figure object.

    TODO:
        - Create one go.Bar trace per scenario
        - Group bars by channel
        - Add total budget annotation per scenario
    """
    # TODO: implement allocation comparison chart
    raise NotImplementedError("allocation_comparison_chart is not yet implemented.")


# ---------------------------------------------------------------------------
# 6. KPI Metric Cards
# ---------------------------------------------------------------------------

def metric_card(label: str, value: str, delta: str | None = None) -> None:
    """Render a Streamlit metric card (thin wrapper around st.metric).

    Args:
        label: KPI label text.
        value: Current KPI value (pre-formatted string, e.g., '£2.3M').
        delta: Optional delta vs. comparison period (e.g., '+12%').

    TODO:
        - Import streamlit as st within the function (lazy import)
        - Call st.metric(label, value, delta)
    """
    # TODO: implement metric card
    raise NotImplementedError("metric_card is not yet implemented.")
