---
mode: "agent"
description: "Regenerate the entire Marketing Mix Modelling repository from scratch"
---

# Regenerate MMM Repository

You are rebuilding an Indian FMCG Marketing Mix Modelling project from scratch. Follow the specification in `.github/PRD.md` exactly. Read `.github/KNOWN_ISSUES.md` before writing any code — it contains critical workarounds.

## Phase 1: Scaffold

1. Create the directory structure:
   ```
   configs/, data/raw/, data/processed/, notebooks/, outputs/figures/,
   outputs/models/, outputs/reports/, src/, src/transforms/, src/models/,
   src/optimization/, src/reports/, src/app/pages/
   ```
2. Create `configs/model_config.yaml` with all parameters from the PRD §4 (Customisation Points).
3. Create `requirements.txt` with pinned versions:
   - numpy, pandas, matplotlib, seaborn, scikit-learn, statsmodels
   - pymc, arviz, pytensor, pymc-marketing
   - streamlit, python-pptx, pyyaml, openpyxl
4. Create `src/` modules: `data_prep.py`, `transforms/adstock.py`, `transforms/saturation.py`, `models/classical_mmm.py`, `models/bayesian_mmm.py`, `optimization/budget_optimizer.py`, `reports/generate_pptx.py`.

## Phase 2: Data Preparation

5. Place `synthetic_mmm_weekly_india.csv` in `data/raw/`.
6. In `src/data_prep.py`: load CSV, convert `Week` to datetime, aggregate to national weekly (156 rows), log-transform Sales_Value, compute adstock & saturation transforms.

## Phase 3: Notebooks (execute in order)

For each notebook, follow the execution workflow in `.github/instructions/notebook-execution.instructions.md`.

7. **NB01** — EDA & Seasonality: STL decomposition, correlation heatmap, VIF analysis, Festive uplift.
8. **NB02** — Classical MMM: Ridge regression with cross-validation, DW test, MAPE, ROAS table.
9. **NB03** — Adstock & Saturation: Geometric vs Weibull comparison, Hill curves, grid search for optimal params.
10. **NB04** — Bayesian MMM (PyMC): Informative priors from NB01-03, NUTS sampling (500+500×2), posterior diagnostics, ROAS with credible intervals.
11. **NB05** — Robyn MMM (R): Install Robyn, hyperparameter calibration, Pareto-optimal model selection.
12. **NB06** — Meridian MMM (Google): Geo-level hierarchical model, national vs regional effects.
13. **NB07** — Sales Decomposition: Stack channel contributions from NB02 + NB04, base vs incremental split.
14. **NB08** — ROAS Comparison: Classical vs Bayesian ROAS side-by-side, marginal vs average ROAS.
15. **NB09** — Budget Optimisation: SLSQP optimizer using Bayesian response curves, scenarios at ±20% budget.

## Phase 4: Dashboard & Reporting

16. Build Streamlit app (`app.py` + `src/app/pages/`) with 6 pages per PRD spec.
17. Generate PowerPoint report (`src/reports/generate_pptx.py`) with 15 slides per PRD spec.
18. Create `README.md` with project overview, setup instructions, and results summary.

## Customisation Points

If you are regenerating for a **different market or dataset**, update these before starting:

| Parameter | Where | Default |
|-----------|-------|---------|
| Country / market | PRD §1 | India |
| Media channels | `model_config.yaml` → `media_channels` | 6 channels |
| Geographic regions | `model_config.yaml` → `geo_regions` | 8 regions |
| Time granularity | `model_config.yaml` → implied by data | Weekly |
| Adstock decay rates | `model_config.yaml` → `adstock` | TV=0.7, YT=0.4, etc. |
| Budget constraint | `model_config.yaml` → `optimization.total_budget` | 1,000,000 |
| MCMC draws | `model_config.yaml` → `bayesian.draws` | 500 |

## Critical Rules

- Read `.github/KNOWN_ISSUES.md` FIRST — every pitfall is documented there
- Use `python3.14 -m pip install --break-system-packages` for all installs
- Use `np.trapezoid` not `np.trapz` (NumPy 2.0+)
- Set `PYTENSOR_FLAGS='cxx='` before importing PyMC
- Cache MCMC results to `.nc` files — never re-sample unnecessarily
- Execute notebooks via `nbconvert`, never via `run_notebook_cell`
- Compute posterior sample counts dynamically, never hardcode
