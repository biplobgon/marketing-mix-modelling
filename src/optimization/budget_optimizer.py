"""
src/optimization/budget_optimizer.py
======================================
Constrained budget optimisation and scenario planning for MMM.

Given a trained MMM (any framework), this module finds the optimal spend
allocation across channels to maximise predicted incremental sales, subject
to a total budget constraint and per-channel min/max bounds.

The optimisation is driven by marginal ROAS (mROAS) curves derived from the
fitted response functions — NOT by historical ROAS. Channels near saturation
have low mROAS and should receive less budget; under-invested channels with
steep response curves should receive more.

Optimiser: scipy.optimize.minimize with method='SLSQP'

References:
    Jin et al. (2017) — Bayesian Methods for Media Mix Modelling
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

import numpy as np
import pandas as pd
from numpy.typing import NDArray
from scipy.optimize import minimize, OptimizeResult


# ---------------------------------------------------------------------------
# Data classes for results
# ---------------------------------------------------------------------------

@dataclass
class OptimisationResult:
    """Container for a single budget optimisation result.

    Attributes:
        scenario_name: Human-readable label for this scenario.
        total_budget: Total spend constraint (currency units).
        allocation: Series mapping channel → optimal spend.
        baseline_allocation: Series mapping channel → current/reference spend.
        predicted_revenue: Predicted incremental revenue at optimal allocation.
        baseline_revenue: Predicted incremental revenue at baseline allocation.
        revenue_uplift: predicted_revenue - baseline_revenue.
        revenue_uplift_pct: Revenue uplift as percentage of baseline_revenue.
        success: Whether the optimiser converged.
        message: Optimiser status message.
    """
    scenario_name: str
    total_budget: float
    allocation: pd.Series
    baseline_allocation: pd.Series
    predicted_revenue: float
    baseline_revenue: float
    revenue_uplift: float
    revenue_uplift_pct: float
    success: bool
    message: str


@dataclass
class ScenarioComparison:
    """Container for multi-scenario comparison results.

    Attributes:
        scenarios: List of OptimisationResult objects.
        comparison_table: Wide-format DataFrame for display.
    """
    scenarios: list[OptimisationResult] = field(default_factory=list)
    comparison_table: pd.DataFrame = field(default_factory=pd.DataFrame)


# ---------------------------------------------------------------------------
# BudgetOptimizer
# ---------------------------------------------------------------------------

class BudgetOptimizer:
    """Constrained spend optimiser using MMM response curves.

    Supports:
        - Single-scenario optimisation (fixed total budget)
        - Multi-scenario comparison (flat / +10% / +25% budget)
        - Per-channel min/max bounds (e.g., TV must get ≥ 15% of budget)
        - Marginal ROAS curve generation for visualisation

    Args:
        response_fn: Callable that maps a spend allocation array of shape
                     (M,) → predicted incremental revenue (scalar).
                     Usually a partial function wrapping a fitted MMM model.
        channel_names: List of channel names matching the order of the
                       spend array passed to response_fn.
        config: Configuration dictionary (see configs/model_config.yaml).
    """

    def __init__(
        self,
        response_fn: Callable[[NDArray[np.float64]], float],
        channel_names: list[str],
        config: dict[str, Any],
    ) -> None:
        self.response_fn = response_fn
        self.channel_names = channel_names
        self.config = config
        self._n_channels = len(channel_names)

        # TODO: extract optimisation sub-config
        # self._method = config["optimisation"]["method"]
        # self._seed   = config["optimisation"]["seed"]

    # ------------------------------------------------------------------
    # Core optimisation
    # ------------------------------------------------------------------

    def optimise(
        self,
        total_budget: float,
        baseline_allocation: NDArray[np.float64],
        min_bounds: NDArray[np.float64] | None = None,
        max_bounds: NDArray[np.float64] | None = None,
        scenario_name: str = "Optimised",
    ) -> OptimisationResult:
        """Find spend allocation that maximises incremental revenue.

        Args:
            total_budget: Total budget constraint (Σ spends = total_budget).
            baseline_allocation: Current/reference spend array of shape (M,).
                                 Used to compute uplift vs. status quo.
            min_bounds: Per-channel minimum spend bounds. Shape (M,).
                        Defaults to zero for all channels.
            max_bounds: Per-channel maximum spend bounds. Shape (M,).
                        Defaults to total_budget for all channels.
            scenario_name: Label for this scenario.

        Returns:
            OptimisationResult with optimal allocation and revenue metrics.

        TODO:
            - Set default bounds: min_bounds = zeros, max_bounds = total_budget
            - Define objective: f(x) = -response_fn(x)  (minimise negative)
            - Define equality constraint: sum(x) == total_budget
            - Define bounds: scipy.optimize.Bounds(min_bounds, max_bounds)
            - Call scipy.optimize.minimize(objective, x0, method='SLSQP',
                  constraints=[...], bounds=[...])
            - Compute baseline_revenue = response_fn(baseline_allocation)
            - Compute revenue metrics
            - Return OptimisationResult
        """
        # TODO: implement core optimisation
        raise NotImplementedError("BudgetOptimizer.optimise is not yet implemented.")

    # ------------------------------------------------------------------
    # Multi-scenario comparison
    # ------------------------------------------------------------------

    def run_scenarios(
        self,
        baseline_allocation: NDArray[np.float64],
        scenarios: dict[str, float] | None = None,
        min_bounds: NDArray[np.float64] | None = None,
        max_bounds: NDArray[np.float64] | None = None,
    ) -> ScenarioComparison:
        """Run multiple budget scenarios and return comparison results.

        Args:
            baseline_allocation: Current spend per channel. Shape (M,).
            scenarios: Mapping from scenario_name → budget_multiplier.
                       Defaults to config["optimisation"]["scenarios"].
                       Example: {"Flat": 1.0, "+10%": 1.1, "+25%": 1.25}
            min_bounds: Per-channel minimum spend. Shape (M,).
            max_bounds: Per-channel maximum spend. Shape (M,).

        Returns:
            ScenarioComparison with all scenario results and comparison table.

        TODO:
            - Load scenarios from config if not provided
            - Compute total_budget = sum(baseline_allocation)
            - For each scenario: optimise(total_budget * multiplier, ...)
            - Build comparison_table (wide-format DataFrame)
            - Return ScenarioComparison
        """
        # TODO: implement multi-scenario
        raise NotImplementedError(
            "BudgetOptimizer.run_scenarios is not yet implemented."
        )

    # ------------------------------------------------------------------
    # Marginal ROAS curves
    # ------------------------------------------------------------------

    def mroas_curve(
        self,
        channel_idx: int,
        baseline_allocation: NDArray[np.float64],
        spend_range: tuple[float, float] | None = None,
        n_points: int = 100,
    ) -> tuple[NDArray, NDArray]:
        """Compute marginal ROAS (mROAS) curve for a single channel.

        Holds all other channels fixed at baseline_allocation and varies
        the target channel spend across spend_range.

        mROAS(x) ≈ ΔRevenue / Δspend (finite difference approximation)

        Args:
            channel_idx: Index of target channel in channel_names.
            baseline_allocation: Baseline spend array. Shape (M,).
            spend_range: (min_spend, max_spend) for the curve. Defaults to
                         (0, 2 × baseline_allocation[channel_idx]).
            n_points: Number of points on the curve.

        Returns:
            Tuple of (spend_values, mroas_values) arrays.

        TODO:
            - Create spend grid from spend_range
            - For each spend level: perturb allocation, compute revenue gradient
            - Use finite differences: mROAS(x) ≈ (R(x+δ) - R(x)) / δ
            - Return (spend_values, mroas_values)
        """
        # TODO: implement mROAS curve
        raise NotImplementedError(
            "BudgetOptimizer.mroas_curve is not yet implemented."
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _validate_allocation(
        self, allocation: NDArray[np.float64], total_budget: float
    ) -> None:
        """Validate that an allocation array sums to total_budget.

        Args:
            allocation: Spend array to validate. Shape (M,).
            total_budget: Expected total.

        Raises:
            ValueError: If allocation does not sum to total_budget (within 1e-6).

        TODO:
            - Check len(allocation) == self._n_channels
            - Check abs(sum(allocation) - total_budget) < 1e-6
            - Check all(allocation >= 0)
        """
        # TODO: implement validation
        raise NotImplementedError(
            "BudgetOptimizer._validate_allocation is not yet implemented."
        )
