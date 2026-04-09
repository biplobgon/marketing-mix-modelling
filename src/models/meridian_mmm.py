"""
src/models/meridian_mmm.py
===========================
Google Meridian Bayesian Hierarchical MMM wrapper.

Meridian (released Jan 2025) is Google's latest open-source MMM framework,
successor to LightweightMMM. Key capabilities:

- Native geo-level hierarchical modelling with partial pooling
- Weibull adstock (more flexible than geometric decay)
- Fully Bayesian: uncertainty propagates to budget recommendations
- JAX + TensorFlow Probability backend for fast GPU/TPU inference
- Unified treatment of national and geo-level models

References:
    Google Meridian docs — https://developers.google.com/meridian
    Sun et al. (2017) — Geo-level Bayesian Hierarchical MMM
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


class MeridianMMM:
    """Google Meridian Bayesian Hierarchical Marketing Mix Model wrapper.

    Wraps the `meridian` library to provide a consistent interface with
    other framework wrappers in this project.

    Attributes:
        config: Model configuration dictionary.
        model_: Fitted Meridian model instance (set after fitting).
        trace_: Posterior samples (set after fitting).
        is_fitted_: Boolean flag, True after fit() is called.

    Typical usage:
        mmm = MeridianMMM(config)
        mmm.build_model(df, media_cols, geo_col, kpi_col)
        mmm.fit()
        roas_by_geo = mmm.geo_roas()
        mmm.save("outputs/models/meridian_mmm/")
    """

    def __init__(self, config: dict[str, Any]) -> None:
        """Initialise MeridianMMM with model configuration.

        Args:
            config: Full config dict from configs/model_config.yaml.
                    Keys used: config["meridian"], config["geographies"],
                                config["media_channels"].
        """
        self.config = config
        self.model_ = None
        self.trace_ = None
        self.is_fitted_: bool = False

        # TODO: extract meridian sub-config
        # self._n_chains  = config["meridian"]["n_chains"]
        # self._n_samples = config["meridian"]["n_samples"]
        # self._n_warmup  = config["meridian"]["n_warmup"]
        # self._geo_level = config["meridian"]["geo_level"]

    # ------------------------------------------------------------------
    # Data preparation
    # ------------------------------------------------------------------

    def prepare_input_data(
        self,
        df: pd.DataFrame,
        media_cols: list[str],
        geo_col: str,
        kpi_col: str,
        date_col: str = "date",
    ) -> Any:
        """Convert DataFrame to Meridian InputData format.

        Args:
            df: Processed DataFrame with media spend, controls, and KPI.
            media_cols: Media channel column names.
            geo_col: Geography identifier column name.
            kpi_col: Target KPI column name (e.g., 'sales').
            date_col: Date column name.

        Returns:
            meridian.data.InputData object ready for model construction.

        TODO:
            - Import meridian.data.InputData
            - Pivot data to (time × geo × channel) xarray format
            - Pass media spend as coords xr.DataArray
            - Pass KPI as coords xr.DataArray
            - Include control variables
        """
        # TODO: implement InputData preparation
        raise NotImplementedError(
            "MeridianMMM.prepare_input_data is not yet implemented."
        )

    # ------------------------------------------------------------------
    # Model building
    # ------------------------------------------------------------------

    def build_model(
        self,
        df: pd.DataFrame,
        media_cols: list[str],
        geo_col: str,
        kpi_col: str,
    ) -> None:
        """Construct the Meridian model specification.

        Args:
            df: Processed DataFrame.
            media_cols: Media channel column names.
            geo_col: Geography identifier column name.
            kpi_col: Target KPI column name.

        TODO:
            - Call prepare_input_data()
            - Import meridian.model.Meridian, meridian.model.ModelSpec
            - Define ModelSpec with:
                - Weibull adstock prior: PriorAdstockWeibull(...)
                - Hill saturation prior: PriorROIRF(...)
                - Geo-level hierarchical pooling
            - Instantiate self.model_ = Meridian(input_data, model_spec)
        """
        # TODO: implement model building
        raise NotImplementedError("MeridianMMM.build_model is not yet implemented.")

    # ------------------------------------------------------------------
    # Fitting
    # ------------------------------------------------------------------

    def fit(self) -> None:
        """Run MCMC sampling to obtain posterior.

        TODO:
            - Validate model_ is built
            - sampler = model_.sample_posterior(
                  n_chains, n_samples, n_warmup, seed=...)
            - Store results in self.trace_
            - Log R-hat and ESS diagnostics
            - Set is_fitted_ = True
        """
        # TODO: implement fitting
        raise NotImplementedError("MeridianMMM.fit is not yet implemented.")

    # ------------------------------------------------------------------
    # ROAS & Attribution
    # ------------------------------------------------------------------

    def roas(self) -> pd.DataFrame:
        """Compute national-level posterior ROAS per channel.

        Returns:
            DataFrame: channel | mean_roas | hdi_3% | hdi_97%

        TODO:
            - Use model_.get_roas() or compute from trace
            - Return summary DataFrame
        """
        # TODO: implement national ROAS
        raise NotImplementedError("MeridianMMM.roas is not yet implemented.")

    def geo_roas(self) -> pd.DataFrame:
        """Compute geo-level posterior ROAS per channel.

        Returns:
            DataFrame: geo | channel | mean_roas | hdi_3% | hdi_97%

        TODO:
            - Leverage Meridian's partial-pooling geo-level estimates
            - Return long-format DataFrame indexed by (geo, channel)
        """
        # TODO: implement geo-level ROAS
        raise NotImplementedError("MeridianMMM.geo_roas is not yet implemented.")

    def decompose(self) -> pd.DataFrame:
        """Return sales decomposition (baseline + channel contributions).

        Returns:
            DataFrame with posterior mean contributions indexed by (date, geo).

        TODO:
            - Use model_.get_decomposition()
            - Return DataFrame
        """
        # TODO: implement decompose
        raise NotImplementedError("MeridianMMM.decompose is not yet implemented.")

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save(self, path: str) -> None:
        """Save model and posterior to disk.

        Args:
            path: Directory path (e.g., 'outputs/models/meridian_mmm/').

        TODO:
            - Create directory if not exists
            - Save model spec as JSON
            - Save trace as NetCDF
        """
        # TODO: implement save
        raise NotImplementedError("MeridianMMM.save is not yet implemented.")

    @classmethod
    def load(cls, path: str, config: dict[str, Any]) -> "MeridianMMM":
        """Load a saved Meridian model from disk.

        Args:
            path: Directory path containing saved model files.
            config: Configuration dictionary.

        Returns:
            MeridianMMM instance with loaded model_ and trace_.

        TODO:
            - Load model spec and trace from path
            - Return fitted instance
        """
        # TODO: implement load
        raise NotImplementedError("MeridianMMM.load is not yet implemented.")
