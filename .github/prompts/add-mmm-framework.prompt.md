---
mode: "agent"
description: "Add a new MMM framework notebook to the project"
---

# Add New MMM Framework: {{FRAMEWORK_NAME}}

Add a new Marketing Mix Modelling framework to this project as notebook `notebooks/{{NB_NUMBER}}_{{FRAMEWORK_SLUG}}.ipynb`.

Read `.github/PRD.md` for the full project specification and `.github/KNOWN_ISSUES.md` for execution pitfalls.

## Pre-Requisites

1. **Install the framework** — use `python3.14 -m pip install {{PACKAGE_NAME}} --break-system-packages`
2. **Read existing notebooks** — especially NB03 (transforms) and NB04 (Bayesian) to understand:
   - How adstock and saturation transforms are applied
   - The training/test split (80/20 = 124/32 weeks)
   - Figure and artifact naming conventions
   - How ROAS and channel contributions are computed

## Notebook Structure

Create the notebook with these cells:

### Cell 1: Setup & Imports
- Standard imports (numpy, pandas, matplotlib, seaborn)
- Framework-specific imports
- Load `configs/model_config.yaml`
- Set output directories

### Cell 2: Data Loading
- Load `data/raw/synthetic_mmm_weekly_india.csv`
- Convert `Week` to datetime
- Aggregate to national weekly level (156 rows)
- Log-transform `Sales_Value`

### Cell 3: Feature Engineering
- Apply adstock transforms using decay rates from config (TV=0.7, YouTube=0.4, Facebook=0.35, Instagram=0.3, Print=0.5, Radio=0.45)
- Apply Hill saturation transforms using K and beta from config
- Include control variables: `log(CPI_Index)`, `Weighted_Distribution`, `Avg_Temperature`
- Include binary indicators: `Is_Festive`, `Is_Promo`
- Train/test split: first 124 weeks / last 32 weeks

### Cell 4: Model Specification
- Define the {{FRAMEWORK_NAME}} model
- Use parameter settings from `model_config.yaml` where applicable
- Reference priors or hyperparameters from NB01-NB03 findings

### Cell 5: Model Fitting
- Fit the model on training data
- Print training metrics (R², MAPE, or equivalent)
- Save the trained model to `outputs/models/{{FRAMEWORK_SLUG}}_mmm.{ext}`

### Cell 6: Diagnostics
- Framework-specific diagnostic plots
- Convergence checks (if Bayesian/MCMC)
- Residual analysis
- Save diagnostic figures to `outputs/figures/{{NB_NUMBER}}_*.png`

### Cell 7: Channel Contributions
- Decompose sales into base + channel contributions
- Plot stacked contribution chart
- Save to `outputs/figures/{{NB_NUMBER}}_channel_contributions.png`

### Cell 8: ROAS Computation
- Compute per-channel ROAS (average and/or marginal)
- Compare with NB02 (Classical) and NB04 (Bayesian) ROAS values
- Save to `outputs/models/{{FRAMEWORK_SLUG}}_roas.parquet`

### Cell 9: Test-Set Evaluation
- Predict on test set (last 32 weeks)
- Compute test MAPE and R²
- Plot predicted vs actual
- Save figure to `outputs/figures/{{NB_NUMBER}}_pred_vs_actual.png`

## After Execution

1. Execute using the workflow in `.github/instructions/notebook-execution.instructions.md`
2. Append an insights markdown cell comparing this framework to existing ones
3. Update the cross-notebook data flow in `.github/copilot-instructions.md` if this notebook feeds into NB07-NB09
4. Update `README.md` frameworks section if applicable

## Example Frameworks to Add

| Framework | Package | Type | Notes |
|-----------|---------|------|-------|
| Orbit | `orbit-ml` | Bayesian structural time series | DLT or LGT models |
| CausalImpact | `causalimpact` | Bayesian structural time series | Intervention analysis |
| LightweightMMM | `lightweight_mmm` | Bayesian (Numpyro) | Google's predecessor to Meridian |
| Prophet + Regressors | `prophet` | Additive decomposition | Media as extra regressors |
| XGBoost MMM | `xgboost` | Gradient boosting | SHAP for attribution |
