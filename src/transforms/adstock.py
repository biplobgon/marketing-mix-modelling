"""
src/transforms/adstock.py
=========================
Adstock (carryover) transformation functions.

Adstock models the persistent effect of advertising after a campaign ends.
Two variants are implemented:

1. Geometric Adstock — simple geometric decay (standard industry method)
   x*_t = x_t + α·x*_{t-1}         α ∈ [0, 1]

2. Weibull Adstock — flexible delay + decay (used by Google Meridian / LightweightMMM)
   x*_t = Σ_{τ} x_{t-τ} · w(τ; shape, scale)
   where w is the Weibull PDF evaluated at lag τ

References:
    Jin et al. (2017) — Bayesian Methods for Media Mix Modelling
    Google Meridian docs — https://developers.google.com/meridian
"""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy.stats import weibull_min


# ---------------------------------------------------------------------------
# 1. Geometric Adstock
# ---------------------------------------------------------------------------

def geometric_adstock(
    x: ArrayLike,
    decay: float,
    normalise: bool = True,
) -> NDArray[np.float64]:
    """Apply geometric adstock (carryover) transformation.

    Recursively applies: x*_t = x_t + decay * x*_{t-1}

    Args:
        x: 1-D array of media spend values ordered by time (oldest → newest).
        decay: Retention/decay rate α ∈ [0, 1].
               0 = no carryover (immediate effect only).
               1 = full carryover (effect never decays).
        normalise: If True, scale output so the sum equals the sum of the
                   input (preserves spend scale for coefficient interpretation).

    Returns:
        1-D array of adstock-transformed values, same length as x.

    Raises:
        ValueError: If decay is not in [0, 1].

    TODO:
        - Validate decay ∈ [0, 1]
        - Implement the recursive loop or cumulative-sum formulation
        - Apply normalisation if requested
        - Add unit tests in tests/test_adstock.py
    """
    # TODO: implement geometric adstock
    raise NotImplementedError("geometric_adstock is not yet implemented.")


def geometric_adstock_matrix(
    X: ArrayLike,
    decays: dict[str, float],
    normalise: bool = True,
) -> NDArray[np.float64]:
    """Apply geometric adstock to each channel column in a DataFrame/matrix.

    Args:
        X: 2-D array of shape (T, M) — T time periods, M media channels.
        decays: Mapping from channel name to decay rate.
                Keys must match column order in X.
        normalise: Passed through to geometric_adstock().

    Returns:
        2-D array of adstock-transformed values, same shape as X.

    TODO:
        - Iterate over columns, applying geometric_adstock per channel
        - Return np.ndarray with same shape as X
    """
    # TODO: implement matrix version
    raise NotImplementedError("geometric_adstock_matrix is not yet implemented.")


# ---------------------------------------------------------------------------
# 2. Weibull Adstock
# ---------------------------------------------------------------------------

def weibull_adstock(
    x: ArrayLike,
    shape: float,
    scale: float,
    max_lag: int = 13,
    normalise: bool = True,
) -> NDArray[np.float64]:
    """Apply Weibull-based adstock (delayed peak + decay) transformation.

    Models the impulse response as a Weibull distribution, allowing for a
    delayed peak effect before decay — more realistic for digital channels.

    x*_t = Σ_{τ=0}^{max_lag} x_{t-τ} · w(τ+1; shape, scale)

    where w is the Weibull PDF (shape=k, scale=λ).

    Args:
        x: 1-D array of media spend values ordered by time (oldest → newest).
        shape: Weibull shape parameter k > 0.
               k < 1 → front-loaded decay (fast initial drop).
               k = 1 → exponential decay (equivalent to geometric).
               k > 1 → delayed peak (ramp up before decay).
        scale: Weibull scale parameter λ > 0 (controls lag length).
        max_lag: Maximum number of lags to include in the convolution.
        normalise: If True, normalise the Weibull weights to sum to 1.

    Returns:
        1-D array of Weibull adstock-transformed values, same length as x.

    TODO:
        - Compute Weibull PDF weights for lags [0, max_lag]
        - Normalise weights if requested
        - Convolve x with weights using np.convolve (mode='full')[:len(x)]
        - Preserve leading zeros for early time steps
    """
    # TODO: implement Weibull adstock
    raise NotImplementedError("weibull_adstock is not yet implemented.")


# ---------------------------------------------------------------------------
# 3. Utility: half-life → decay rate conversion
# ---------------------------------------------------------------------------

def half_life_to_decay(half_life_weeks: float) -> float:
    """Convert half-life in weeks to a geometric decay rate.

    α = 0.5 ^ (1 / half_life_weeks)

    Args:
        half_life_weeks: Number of weeks for effect to decay to 50%.

    Returns:
        Decay rate α ∈ (0, 1).

    Example:
        >>> half_life_to_decay(4)  # 4-week half-life
        0.8408964152537145

    TODO:
        - Implement the formula above
        - Validate half_life_weeks > 0
    """
    # TODO: implement conversion
    raise NotImplementedError("half_life_to_decay is not yet implemented.")


def decay_to_half_life(decay: float) -> float:
    """Convert geometric decay rate to half-life in weeks.

    half_life = log(0.5) / log(α)

    Args:
        decay: Geometric decay rate α ∈ (0, 1).

    Returns:
        Half-life in weeks.

    TODO:
        - Implement the formula above
        - Validate decay ∈ (0, 1)
    """
    # TODO: implement conversion
    raise NotImplementedError("decay_to_half_life is not yet implemented.")
