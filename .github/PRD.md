# Product Requirements Document — Marketing Mix Modelling

> **Purpose:** This document is the single source of truth for any AI agent (Copilot, Claude, Cursor, Devin, etc.) regenerating this repository. It specifies what to build, in what order, and what "done" looks like for every component.

---

## 1. Business Context

An Indian FMCG company runs media across 6 channels (TV, YouTube, Facebook, Instagram, Print, Radio) in 8 geographies. They need to:
- Decompose sales into baseline vs. media-driven components
- Rank channels by Return on Ad Spend (ROAS)
- Identify saturation points and diminishing returns per channel
- Optimise budget allocation across channels and scenarios
- Validate results across multiple MMM frameworks

**Domain:** Fast-Moving Consumer Goods (FMCG), India  
**KPI:** Weekly Sales_Value (INR)  
**Time range:** 156 weeks (July 2022 — June 2025)  
**Granularity:** Weekly × 8 Geos × 3 Brands × 3 SKUs = 11,232 rows  
**National aggregate:** 156 rows (sum/mean by Week)

---

## 2. Dataset Schema

### Primary dataset: `data/raw/synthetic_mmm_weekly_india.csv`

| Column | Type | Description | Known Quirks |
|--------|------|-------------|-------------|
| Week | string | `YYYY-MM-DD` format | Must `pd.to_datetime()` — stored as string |
| Geo | string | 8 values: NORTH, SOUTH, EAST, WEST, CENTRAL, NORTHEAST, METRO_DELHI, METRO_MUMBAI | National aggregate: filter or groupby |
| Brand | string | 3 brands | |
| SKU | string | 3 SKUs per brand | |
| Sales_Value | float | Weekly sales in INR | **Right-skewed** — always log-transform for regression |
| Sales_Units | float | Weekly units sold | |
| TV_Impressions | float | Weekly TV impressions | Largest volume (~1.8B/week nationally) |
| YouTube_Impressions | float | Weekly YouTube impressions | **r=0.96 with Instagram** (raw) — collinearity |
| Facebook_Impressions | float | Weekly Facebook impressions | |
| Instagram_Impressions | float | Weekly Instagram impressions | Correlated with YouTube; Ridge forces beta=0 |
| Print_Readership | float | Weekly print readership reach | Smallest volume (~148M/week) but highest ROAS |
| Radio_Listenership | float | Weekly radio audience reach | |
| CPI_Value | float | Consumer Price Index | **VIF=295** — do NOT include both CPI_Value and CPI_Index |
| CPI_Index | float | Indexed CPI | Use log(CPI_Index) or log(CPI_Value), not both |
| GDP_Growth_Index | float | GDP growth proxy | |
| Weighted_Distribution | float | Distribution metric (0-100) | Strong predictor; Ridge coef ~0.169 |
| Numeric_Distribution | float | Outlet count metric | |
| TDP | float | Total Distribution Points | |
| NOS | float | Number of Stores | |
| Feature_Flag | binary | Trade feature promotion | |
| Display_Flag | binary | In-store display flag | |
| TPR_Flag | binary | Temporary price reduction | |
| Trade_Spend | float | Trade promotion spend | VIF=2.18 (safe) |
| Festival_Index | float | Binary/indexed festive period | **+17.7% sales uplift** (NB01 STL finding) |
| Rainfall_Index | float | Monsoon proxy | |
| is_festive | binary | Derived festive flag | |
| week_num | int | Week-of-year (1-52) | Trend proxy |

### Secondary dataset: `data/raw/synthetic_mmm_weekly_india_SAT.csv`
Same schema, used for saturation validation and sensitivity analysis.

### Baseline dataset: `data/raw/advertising.csv`
200 rows, 4 columns: Sales, TV, Radio, Newspaper. Classic advertising dataset for basic regression examples.

---

## 3. Configuration

All model parameters live in `configs/model_config.yaml`. This is the **single source of truth** — notebooks read from it; never hardcode parameters.

Key parameter groups:
- **Adstock decay rates:** TV=0.7, YouTube=0.4, Facebook=0.35, Instagram=0.3, Print=0.5, Radio=0.45
- **Saturation:** Hill function, K=0.5, beta=2.0
- **Classical MMM:** Ridge alpha=0.1, non-negativity constraint
- **Bayesian MMM:** 1000 draws, 500 tune, 4 chains, target_accept=0.9
- **Meridian:** 4 chains, 1000 samples, 500 warmup, geo_level=true
- **Optimisation:** SLSQP, budget=1M, scenarios: flat/+10%/+25%

---

## 4. Notebook Pipeline Specification

### Cross-Notebook Data Flow

```
NB01 (EDA) ──→ Seasonality (F_S=0.78), Festive uplift (+17.7%), VIF screening
    │
    ▼
NB02 (Classical Ridge) ──→ Decay rates, R²=0.81, ROAS point estimates
    │
    ▼
NB03 (Transform Library) ──→ Hill K values per channel, Geo vs Weibull comparison
    │
    ▼
NB04 (Bayesian PyMC) ──→ Posteriors, ROAS with CIs, lift-test calibration
    │
    ├──→ NB05 (Robyn R) ──→ Auto-optimised adstock, budget allocation curves
    │
    └──→ NB06 (Meridian) ──→ Hierarchical geo model, JAX-based inference
              │
              ▼
         NB07 (Decomposition) ──→ Waterfall charts, baseline vs media split
              │
              ▼
         NB08 (ROAS Analysis) ──→ Cross-framework ROAS comparison, mROAS curves
              │
              ▼
         NB09 (Budget Optim.) ──→ Optimal allocation, scenario tables, recommendations
```

### Per-Notebook Specification

#### NB01: `01_eda_seasonality.ipynb`
- **Purpose:** Exploratory Data Analysis, seasonality decomposition, data quality, VIF screening
- **Input:** `data/raw/synthetic_mmm_weekly_india.csv`
- **Processing:** Load → national aggregate (156 rows) → STL decomposition → correlation matrix → VIF
- **Outputs:**
  - 6 figures: `01_sales_distribution.png`, `01_media_distribution.png`, `01_stl_decomposition.png`, `01_festival_monsoon_signals.png`, `01_correlation_heatmap.png`, `01_vif_screening.png`
  - No model artifacts
- **Acceptance Criteria:**
  - STL F_S > 0.7 (strong seasonality confirmed)
  - Festive uplift quantified (expect +15-20%)
  - Instagram-YouTube correlation flagged (r > 0.90)
  - CPI VIF > 100 flagged — recommend dropping one CPI column
  - Insights markdown cell appended at end

#### NB02: `02_classical_mmm_regression.ipynb`
- **Purpose:** Constrained Ridge regression, ROAS attribution, sales decomposition
- **Input:** `data/raw/synthetic_mmm_weekly_india.csv`, decay rates from config
- **Processing:** National aggregate → geometric adstock → Hill saturation → log(Sales) regression → ROAS → decomposition
- **Outputs:**
  - 4 figures: `02_adstock_saturation_transforms.png`, `02_model_diagnostics.png`, `02_sales_decomposition.png`, `02_roas_attribution.png`
  - `outputs/models/classical_mmm.pkl`, `outputs/models/classical_roas.parquet`
- **Acceptance Criteria:**
  - R² > 0.75, MAPE < 15%, Durbin-Watson 1.5-2.5
  - All media coefficients ≥ 0 (non-negativity constraint satisfied)
  - Instagram coefficient may be 0 (expected — collinearity with YouTube)
  - Insights markdown cell appended

#### NB03: `03_adstock_saturation_transforms.ipynb`
- **Purpose:** Full transform function library — geometric/Weibull adstock, Hill/Logistic/NegExp saturation, sensitivity analysis
- **Input:** `data/raw/synthetic_mmm_weekly_india.csv`
- **Processing:** Implement all transform functions → visualise impulse responses → compare geometric vs Weibull → run 6-channel pipeline → sensitivity heatmaps
- **Outputs:**
  - 7 figures: `03_geometric_adstock_impulse.png`, `03_weibull_adstock.png`, `03_geo_vs_weibull_tv.png`, `03_hill_saturation.png`, `03_saturation_comparison.png`, `03_full_transform_pipeline.png`, `03_sensitivity_analysis.png`
  - No model artifacts (library notebook)
- **Acceptance Criteria:**
  - Geometric vs Weibull correlation > 0.95 (validates geometric as simpler default)
  - Hill K values extracted per channel
  - Near-linear saturation regime confirmed (all channels Corr > 0.95 with raw)
  - Insights markdown cell appended

#### NB04: `04_bayesian_mmm_pymc.ipynb`
- **Purpose:** Bayesian MMM with PyMC 5, MCMC NUTS, ROAS with credible intervals, lift-test calibration
- **Input:** `data/raw/synthetic_mmm_weekly_india.csv`, prior specs informed by NB01-NB03
- **Processing:** Fixed transforms (NB03 params) → PyMC model (12 params) → NUTS sampling → convergence diagnostics → posterior predictive → ROAS with HDI → synthetic lift-test calibration
- **Outputs:**
  - 6 figures: `04_prior_elicitation.png`, `04_trace_plots.png`, `04_posterior_forest.png`, `04_posterior_predictive.png`, `04_roas_credible_intervals.png`, `04_lift_test_calibration.png`
  - `outputs/models/bayesian_mmm.nc` (InferenceData), `outputs/models/bayesian_roas.parquet`
- **Acceptance Criteria:**
  - All R-hat ≤ 1.05, ESS > 200 for all parameters
  - Instagram posterior mean > 0 (Bayesian recovers it unlike Ridge)
  - beta_Festive ≈ 0.16 (consistent with NB01 +17.7% finding)
  - Test MAPE competitive with or better than Ridge
  - Insights markdown cell appended
- **Critical Notes:**
  - Cache `.nc` file — if it exists, load instead of re-sampling
  - Use `draws=500, tune=500, chains=2` in Python-mode (no g++ compiler)
  - Use `np.trapezoid` not `np.trapz` (NumPy 2.0+)

#### NB05: `05_robyn_mmm_r.ipynb`
- **Purpose:** Meta Robyn framework — evolutionary optimisation, automatic adstock/saturation estimation
- **Input:** `data/raw/synthetic_mmm_weekly_india.csv`
- **Processing:** R kernel via IRkernel → Robyn::robyn_inputs() → robyn_run() → budget allocator
- **Outputs:**
  - Robyn one-pager figures, budget allocation curves
  - Model object (RDS file)
- **Acceptance Criteria:**
  - NRMSE < 0.15
  - Budget reallocation recommendation generated
  - Comparison table vs NB02/NB04 ROAS
- **Note:** Requires R 4.3+, IRkernel, Robyn, nevergrad (via reticulate)

#### NB06: `06_meridian_mmm_google.ipynb`
- **Purpose:** Google Meridian — Bayesian hierarchical geo-level model with JAX
- **Input:** `data/raw/synthetic_mmm_weekly_india.csv` (geo-level)
- **Processing:** Meridian model spec → MCMC via JAX → geo-level ROAS → national roll-up
- **Outputs:**
  - Geo-level ROAS heatmap, posterior summaries
  - Meridian model checkpoint
- **Acceptance Criteria:**
  - Geo-level variation in ROAS captured
  - National ROAS consistent (±30%) with NB02/NB04
- **Note:** Requires google-meridian, jax[cpu], tensorflow-probability — install separately

#### NB07: `07_sales_decomposition.ipynb`
- **Purpose:** Waterfall decomposition of sales into baseline, media, controls, error
- **Input:** Model artifacts from NB02, NB04 (and optionally NB05, NB06)
- **Outputs:** Waterfall charts, time-series decomposition plots, contribution tables

#### NB08: `08_roas_channel_efficiency.ipynb`
- **Purpose:** Cross-framework ROAS comparison, marginal ROAS curves, efficiency frontier
- **Input:** ROAS parquets from NB02, NB04, NB05, NB06
- **Outputs:** ROAS comparison tables, mROAS curves, efficiency scatter

#### NB09: `09_budget_optimisation.ipynb`
- **Purpose:** Constrained optimisation — optimal budget allocation under scenarios
- **Input:** Response curves from NB02/NB04, budget constraints from config
- **Outputs:** Optimal allocation tables, scenario comparison, recommendation summary

---

## 5. Streamlit Dashboard Specification

**Entry point:** `app.py` → 6 pages in `src/app/pages/`

| Page | File | Purpose |
|------|------|---------|
| Overview | `1_overview.py` | KPI cards, trend charts, data summary |
| Attribution | `2_attribution.py` | Sales decomposition waterfall, channel contributions |
| Response Curves | `3_response_curves.py` | Interactive adstock/saturation curves per channel |
| Budget Optimizer | `4_budget_optimizer.py` | Drag sliders to reallocate budget, see predicted sales |
| Scenario Planner | `5_scenario_planner.py` | Compare flat/+10%/+25% scenarios side by side |
| Framework Comparison | `6_framework_comparison.py` | Ridge vs Bayesian vs Robyn vs Meridian ROAS table |

---

## 6. PowerPoint Deck Specification

**Generator:** `src/reports/generate_pptx.py`  
**Output:** `outputs/reports/MMM_Stakeholder_Deck.pptx`  
**Slides:** 15 (Cover → Executive Summary → Problem → Methodology → Channel Overview → Adstock/Saturation → Framework Comparison → Decomposition → Attribution → mROAS → Optimization → Scenarios → Recommendations → Risks/Caveats → Appendix)

---

## 7. Output Artifact Inventory

### Figures (`outputs/figures/`)
| Notebook | Count | Naming Pattern |
|----------|-------|---------------|
| NB01 | 6 | `01_{description}.png` |
| NB02 | 4 | `02_{description}.png` |
| NB03 | 7 | `03_{description}.png` |
| NB04 | 6 | `04_{description}.png` |
| NB05-09 | ~10 | `{NN}_{description}.png` |

### Models (`outputs/models/`)
| File | Source | Format |
|------|--------|--------|
| `classical_mmm.pkl` | NB02 | scikit-learn pickle |
| `classical_roas.parquet` | NB02 | pandas parquet |
| `bayesian_mmm.nc` | NB04 | ArviZ NetCDF (InferenceData) |
| `bayesian_roas.parquet` | NB04 | pandas parquet |

---

## 8. Customization Points

When adapting this project for a different dataset/market, change these:

| What to Change | Where | Example |
|---------------|-------|---------|
| Dataset CSV | `configs/model_config.yaml` → `data.raw_path` | Your company's weekly media data |
| Channel names | `configs/model_config.yaml` → `media_channels` | Add TikTok, remove Print |
| Geographies | `configs/model_config.yaml` → `geographies` | US states instead of Indian regions |
| Decay rates | `configs/model_config.yaml` → `adstock.decay_rates` | Channel-specific, start with defaults |
| KPI column | `configs/model_config.yaml` → `data.kpi_column` | Revenue, Conversions, Leads |
| Control variables | `configs/model_config.yaml` → `control_variables` | Unemployment, weather, competitor activity |
| Budget | `configs/model_config.yaml` → `optimisation.total_budget` | Your actual media budget |

---

## 9. Tech Stack

**Python 3.10+:** pandas, numpy, statsmodels, scikit-learn, scipy, pymc, pymc-marketing, arviz, plotly, matplotlib, seaborn, streamlit, python-pptx  
**R 4.3+:** Robyn, reticulate, nevergrad  
**Optional:** google-meridian, jax[cpu], tensorflow-probability

Full dependency list: `requirements.txt` (Python), `requirements_r.txt` (R)

---

## 10. References

- [README.md](../README.md) — Full project documentation
- [configs/model_config.yaml](../configs/model_config.yaml) — All model parameters
- [KNOWN_ISSUES.md](./KNOWN_ISSUES.md) — Loopholes, pitfalls, and workarounds for AI agents
