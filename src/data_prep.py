"""
src/data_prep.py
================
Data loading, preprocessing, and feature engineering for the MMM pipeline.

Typical usage:
    df_raw   = load_data(config)
    df_clean = preprocess(df_raw, config)
    df_feat  = feature_engineer(df_clean, config)
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
import yaml


# ---------------------------------------------------------------------------
# Config helper
# ---------------------------------------------------------------------------

def load_config(config_path: str = "configs/model_config.yaml") -> dict[str, Any]:
    """Load YAML configuration file.

    Args:
        config_path: Path to the YAML config file.

    Returns:
        Parsed config dictionary.
    """
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# ---------------------------------------------------------------------------
# 1. Data loading
# ---------------------------------------------------------------------------

def load_data(config: dict[str, Any]) -> pd.DataFrame:
    """Load the raw MMM dataset from disk.

    Args:
        config: Configuration dictionary (see configs/model_config.yaml).

    Returns:
        DataFrame with raw weekly media spend and KPI data.

    TODO:
        - Read `config["data"]["raw_path"]`
        - Parse date column to datetime
        - Set index if required
        - Log shape and dtypes
    """
    # TODO: implement data loading
    raise NotImplementedError("load_data is not yet implemented.")


def load_baseline_data(config: dict[str, Any]) -> pd.DataFrame:
    """Load the advertising.csv baseline dataset (TV/Radio/Newspaper → Sales).

    Args:
        config: Configuration dictionary.

    Returns:
        DataFrame with 200-row advertising dataset.

    TODO:
        - Read `config["data"]["baseline_path"]`
        - Validate expected columns: TV, Radio, Newspaper, Sales
    """
    # TODO: implement baseline data loading
    raise NotImplementedError("load_baseline_data is not yet implemented.")


# ---------------------------------------------------------------------------
# 2. Preprocessing
# ---------------------------------------------------------------------------

def preprocess(df: pd.DataFrame, config: dict[str, Any]) -> pd.DataFrame:
    """Clean and validate the raw dataset.

    Args:
        df: Raw input DataFrame.
        config: Configuration dictionary.

    Returns:
        Cleaned DataFrame.

    TODO:
        - Handle missing values (impute or flag)
        - Remove obvious outliers / data quality issues
        - Normalise / standardise spend columns (optional, framework-dependent)
        - Validate geo and brand codes against config lists
        - Sort by date and geo
    """
    # TODO: implement preprocessing
    raise NotImplementedError("preprocess is not yet implemented.")


# ---------------------------------------------------------------------------
# 3. Feature engineering
# ---------------------------------------------------------------------------

def feature_engineer(df: pd.DataFrame, config: dict[str, Any]) -> pd.DataFrame:
    """Create engineered features for the MMM models.

    Args:
        df: Cleaned DataFrame.
        config: Configuration dictionary.

    Returns:
        Feature-enriched DataFrame ready for modelling.

    TODO:
        - Create time-based features: week_of_year, month, quarter, year
        - Encode festival calendar (diwali_flag, holi_flag, eid_flag, etc.)
        - Lag features for macro variables (CPI, GDP) if applicable
        - Interaction terms: creative_score × spend
        - Apply adstock & saturation transforms (calls src/transforms/)
        - Split into train / validation periods
        - Save to `config["data"]["processed_path"]`
    """
    # TODO: implement feature engineering
    raise NotImplementedError("feature_engineer is not yet implemented.")


# ---------------------------------------------------------------------------
# 4. Train / validation split
# ---------------------------------------------------------------------------

def train_val_split(
    df: pd.DataFrame,
    val_weeks: int = 13,
    date_col: str = "date",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split dataset into train and validation sets by date.

    Args:
        df: Feature-engineered DataFrame.
        val_weeks: Number of most-recent weeks to hold out as validation.
        date_col: Name of the date column.

    Returns:
        Tuple of (train_df, val_df).

    TODO:
        - Sort by date_col
        - Hold out last `val_weeks` rows as validation
        - Log train/val period boundaries
    """
    # TODO: implement train/val split
    raise NotImplementedError("train_val_split is not yet implemented.")
