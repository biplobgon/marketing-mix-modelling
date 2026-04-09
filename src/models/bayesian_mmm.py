"""
src/models/bayesian_mmm.py
===========================
Bayesian MMM wrapper using PyMC-Marketing.

PyMC-Marketing implements the Google Carryover + Shape paper (Jin et al., 2017)
in a fully Bayesian framework. Key capabilities:

- Prior elicitation with domain knowledge (spend share → media prior sigma)
- Full posterior over ROAS, adstock decay, and saturation parameters
- Lift-test calibration to anchor priors from controlled experiments
- Uncertainty-aware budget recommendations (credible intervals on ROI)

References:
    Jin et al. (2017) — Bayesian Methods for Media Mix Modelling
    PyMC-Marketing docs — https://www.pymc-marketing.io/
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


class BayesianMMM:
    """PyMC-Marketing Bayesian Marketing Mix Model wrapper.

    Wraps pymc_marketing.mmm.MMM to provide a consistent interface
    with the other framework wrappers in this project.

    Attributes:
        config: Model configuration dictionary.
        model_: Fitted pymc_marketing.mmm.MMM instance (set after fitting).
        trace_: ArviZ InferenceData object with posterior samples.
        is_fitted_: Boolean flag, True after fit() is called.

    Typical usage:
        bmmm = BayesianMMM(config)
        bmmm.build_model(X_train, y_train, media_cols, control_cols)
        bmmm.fit()
        trace = bmmm.trace_
        roas  = bmmm.roas()
        bmmm.save("outputs/models/bayesian_mmm.nc")
    """

    def __init__(self, config: dict[str, Any]) -> None:
        """Initialise BayesianMMM with model configuration.

        Args:
            config: Full config dict from configs/model_config.yaml.
                    Keys used: config["bayesian_mmm"], config["adstock"],
                                config["saturation"].
        """
        self.config = config
        self.model_ = None
        self.trace_ = None
        self.is_fitted_: bool = False

        # TODO: extract relevant sub-configs
        # self._draws   = config["bayesian_mmm"]["draws"]
        # self._tune    = config["bayesian_mmm"]["tune"]
        # self._chains  = config["bayesian_mmm"]["chains"]
        # self._seed    = config["bayesian_mmm"]["random_seed"]

    # ------------------------------------------------------------------
    # Model building
    # ------------------------------------------------------------------

    def build_model(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        media_cols: list[str],
        control_cols: list[str],
    ) -> None:
        """Construct the PyMC-Marketing MMM model graph.

        Args:
            X: Feature DataFrame (raw spend + control variables).
            y: Target KPI series (weekly sales).
            media_cols: Column names for media spend channels.
            control_cols: Column names for control/macro variables.

        TODO:
            - Import pymc_marketing.mmm.MMM
            - Define adstock prior: GeometricAdstock(alpha=Prior("Beta", alpha=1, beta=3))
            - Define saturation prior: LogisticSaturation() or TanhSaturation()
            - Configure channel-level priors using spend-share scaling
            - Instantiate MMM with date_column, channel_columns, control_columns
            - Store as self.model_
        """
        # TODO: implement model building
        raise NotImplementedError("BayesianMMM.build_model is not yet implemented.")

    # ------------------------------------------------------------------
    # Fitting (MCMC)
    # ------------------------------------------------------------------

    def fit(self) -> None:
        """Run NUTS MCMC sampling to obtain posterior distribution.

        TODO:
            - Validate model_ is built
            - Call self.model_.sample(draws, tune, chains, target_accept, seed)
            - Store result in self.trace_
            - Log convergence diagnostics: max R-hat, min ESS
            - Set is_fitted_ = True
        """
        # TODO: implement MCMC fitting
        raise NotImplementedError("BayesianMMM.fit is not yet implemented.")

    # ------------------------------------------------------------------
    # Diagnostics
    # ------------------------------------------------------------------

    def diagnostics(self) -> pd.DataFrame:
        """Compute MCMC convergence diagnostics.

        Returns:
            DataFrame with R-hat, ESS bulk, and ESS tail for each parameter.

        TODO:
            - Validate is_fitted_
            - Use arviz.summary(self.trace_, var_names=[...])
            - Return filtered summary DataFrame
        """
        # TODO: implement diagnostics
        raise NotImplementedError("BayesianMMM.diagnostics is not yet implemented.")

    # ------------------------------------------------------------------
    # Posterior predictive
    # ------------------------------------------------------------------

    def posterior_predictive(self) -> Any:
        """Sample from the posterior predictive distribution.

        Returns:
            ArviZ InferenceData with posterior_predictive group.

        TODO:
            - Call self.model_.sample_posterior_predictive(self.trace_)
            - Return the posterior predictive InferenceData
        """
        # TODO: implement posterior predictive sampling
        raise NotImplementedError(
            "BayesianMMM.posterior_predictive is not yet implemented."
        )

    # ------------------------------------------------------------------
    # Attribution & ROAS
    # ------------------------------------------------------------------

    def roas(self) -> pd.DataFrame:
        """Compute posterior ROAS distribution per channel.

        Returns:
            DataFrame with columns: channel, mean_roas, hdi_3%, hdi_97%

        TODO:
            - Use self.model_.get_channel_contributions()
            - Divide posterior contributions by raw spend
            - Compute mean + 94% HDI using arviz.hdi()
            - Return summary DataFrame
        """
        # TODO: implement Bayesian ROAS
        raise NotImplementedError("BayesianMMM.roas is not yet implemented.")

    def decompose(self) -> pd.DataFrame:
        """Return mean sales decomposition (baseline + per-channel).

        Returns:
            DataFrame with posterior mean contributions over time.

        TODO:
            - Use self.model_.get_decomposition()
            - Return DataFrame indexed by date
        """
        # TODO: implement decompose
        raise NotImplementedError("BayesianMMM.decompose is not yet implemented.")

    # ------------------------------------------------------------------
    # Lift-test calibration
    # ------------------------------------------------------------------

    def add_lift_test_measurements(
        self,
        channel: str,
        date_start: str,
        date_end: str,
        lift_pct: float,
        lift_pct_std: float,
    ) -> None:
        """Calibrate channel prior using lift-test experimental data.

        Args:
            channel: Channel name (must be in media_cols).
            date_start: Experiment start date (YYYY-MM-DD).
            date_end: Experiment end date (YYYY-MM-DD).
            lift_pct: Observed lift in KPI (as a fraction, e.g., 0.05 = 5%).
            lift_pct_std: Standard deviation of lift estimate.

        TODO:
            - Use pymc_marketing.mmm.MMM.add_lift_test_measurements()
            - Document expected units and date parsing
        """
        # TODO: implement lift-test calibration
        raise NotImplementedError(
            "BayesianMMM.add_lift_test_measurements is not yet implemented."
        )

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save(self, path: str) -> None:
        """Save posterior trace to NetCDF format.

        Args:
            path: File path (e.g., 'outputs/models/bayesian_mmm.nc').

        TODO:
            - Validate is_fitted_
            - Use self.trace_.to_netcdf(path)
        """
        # TODO: implement save
        raise NotImplementedError("BayesianMMM.save is not yet implemented.")

    @classmethod
    def load(cls, path: str, config: dict[str, Any]) -> "BayesianMMM":
        """Load a saved trace from NetCDF.

        Args:
            path: File path to the NetCDF trace.
            config: Configuration dictionary.

        Returns:
            BayesianMMM instance with loaded trace_.

        TODO:
            - Use arviz.from_netcdf(path)
        """
        # TODO: implement load
        raise NotImplementedError("BayesianMMM.load is not yet implemented.")
