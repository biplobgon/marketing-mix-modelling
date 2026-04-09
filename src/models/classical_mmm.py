"""
src/models/classical_mmm.py
============================
Classical Constrained Ridge Regression MMM.

Workflow:
    1. Pre-apply adstock & saturation transforms to media variables
    2. Fit Ridge regression with non-negativity constraints on media coefficients
    3. Decompose sales into baseline + per-channel contributions
    4. Compute ROAS per channel

This is the historical industry-standard approach used by Nielsen, IRI, and
traditional media agencies. It is fast, interpretable, and production-ready.

References:
    - Ridge regression: Hoerl & Kennard (1970)
    - Non-negativity constraints: scipy.optimize.minimize(method='SLSQP')
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
from numpy.typing import NDArray


class ClassicalMMM:
    """Constrained Ridge Regression Marketing Mix Model.

    Attributes:
        config: Model configuration dictionary.
        coefs_: Fitted coefficient array (set after fitting).
        intercept_: Fitted intercept (baseline) value.
        feature_names_: List of feature column names.
        is_fitted_: Boolean flag, True after fit() is called.

    Typical usage:
        model = ClassicalMMM(config)
        model.fit(X_train, y_train)
        decomp = model.decompose(X)
        roas   = model.roas(X, spend_cols)
    """

    def __init__(self, config: dict[str, Any]) -> None:
        """Initialise ClassicalMMM with model configuration.

        Args:
            config: Full configuration dict from configs/model_config.yaml.
                    Key used: config["classical_mmm"].
        """
        self.config = config
        self.coefs_: NDArray[np.float64] | None = None
        self.intercept_: float | None = None
        self.feature_names_: list[str] | None = None
        self.is_fitted_: bool = False

        # TODO: extract classical_mmm sub-config
        # self._alpha = config["classical_mmm"]["alpha"]
        # self._non_negativity = config["classical_mmm"]["non_negativity"]

    # ------------------------------------------------------------------
    # Fitting
    # ------------------------------------------------------------------

    def fit(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        media_cols: list[str],
    ) -> "ClassicalMMM":
        """Fit constrained Ridge regression to training data.

        Args:
            X: Feature matrix (adstock + saturation transforms pre-applied).
               Shape (T, p).
            y: Target KPI series (e.g., weekly sales). Shape (T,).
            media_cols: Column names corresponding to media spend features.
                        Non-negativity constraints applied to these only.

        Returns:
            self (fitted model instance).

        TODO:
            - Store feature_names_ from X.columns
            - Standardise features (optional, configurable)
            - Define Ridge objective: ||y - Xβ||² + α||β||²
            - Define non-negativity constraints for media_cols indices
            - Solve with scipy.optimize.minimize(method='SLSQP',
                constraints=[{'type': 'ineq', 'fun': lambda b: b[media_idx]}])
            - Store coefs_ and intercept_
            - Set is_fitted_ = True
            - Log R², MAE, MAPE on training set
        """
        # TODO: implement fit
        raise NotImplementedError("ClassicalMMM.fit is not yet implemented.")

    # ------------------------------------------------------------------
    # Prediction
    # ------------------------------------------------------------------

    def predict(self, X: pd.DataFrame) -> NDArray[np.float64]:
        """Generate sales predictions from fitted model.

        Args:
            X: Feature matrix. Must have same columns as training X.

        Returns:
            1-D array of predicted sales values.

        TODO:
            - Validate is_fitted_
            - Return intercept_ + X @ coefs_
        """
        # TODO: implement predict
        raise NotImplementedError("ClassicalMMM.predict is not yet implemented.")

    # ------------------------------------------------------------------
    # Decomposition
    # ------------------------------------------------------------------

    def decompose(
        self,
        X: pd.DataFrame,
        spend_cols: list[str],
    ) -> pd.DataFrame:
        """Decompose total sales into baseline + per-channel contributions.

        Args:
            X: Feature matrix (same format as fit).
            spend_cols: Media spend column names.

        Returns:
            DataFrame with columns:
                - baseline: intercept + non-media contributions
                - <channel>_contribution for each media channel
                - total_predicted: sum of all contributions

        TODO:
            - baseline = intercept_ + sum of non-media coef * feature
            - channel_contribution[m] = coef[m] * X[m] (adstock-saturated)
            - Verify contributions sum to predict()
        """
        # TODO: implement decompose
        raise NotImplementedError("ClassicalMMM.decompose is not yet implemented.")

    # ------------------------------------------------------------------
    # ROAS
    # ------------------------------------------------------------------

    def roas(
        self,
        X: pd.DataFrame,
        spend_data: pd.DataFrame,
        media_cols: list[str],
    ) -> pd.Series:
        """Compute ROAS per channel: incremental revenue / actual spend.

        ROAS_m = Σ_t contribution_m(t) / Σ_t spend_m(t)

        Args:
            X: Adstock-saturated feature matrix (for decompose).
            spend_data: DataFrame of raw (un-transformed) spend per channel.
            media_cols: Media channel column names.

        Returns:
            Series indexed by channel name with ROAS values.

        TODO:
            - Call decompose() to get incremental contributions
            - Divide total contribution by total raw spend per channel
            - Return pd.Series
        """
        # TODO: implement ROAS
        raise NotImplementedError("ClassicalMMM.roas is not yet implemented.")

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save(self, path: str) -> None:
        """Serialise fitted model to disk.

        Args:
            path: File path (e.g., 'outputs/models/classical_mmm.pkl').

        TODO:
            - Use joblib.dump(self, path)
            - Validate is_fitted_ before saving
        """
        # TODO: implement save
        raise NotImplementedError("ClassicalMMM.save is not yet implemented.")

    @classmethod
    def load(cls, path: str) -> "ClassicalMMM":
        """Load a fitted model from disk.

        Args:
            path: File path to the serialised model.

        Returns:
            Loaded ClassicalMMM instance.

        TODO:
            - Use joblib.load(path)
        """
        # TODO: implement load
        raise NotImplementedError("ClassicalMMM.load is not yet implemented.")
