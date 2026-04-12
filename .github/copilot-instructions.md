# Marketing Mix Modelling – Workspace Instructions

## Project Overview

This is an **Indian FMCG Marketing Mix Modelling** project that quantifies the incremental impact of 6 media channels (TV, YouTube, Facebook, Instagram, Print, Radio) on sales across 8 geographic regions over 156 weeks.

Read [`.github/PRD.md`](.github/PRD.md) for the full product specification.
Read [`.github/KNOWN_ISSUES.md`](.github/KNOWN_ISSUES.md) for all known pitfalls and their workarounds.

---

## Python Runtime

- **Interpreter:** `python3.14` (managed by `uv`)
- **pip install pattern:** Always use `--break-system-packages`:
  ```
  python3.14 -m pip install <package> --break-system-packages
  ```
- **UTF-8:** Pass `-X utf8` when running scripts that produce Unicode output
- **NumPy 2.0+:** Use `np.trapezoid` (not `np.trapz`). See KNOWN_ISSUES §1.3.
- **PyTensor:** Set `os.environ['PYTENSOR_FLAGS'] = 'cxx='` before `import pymc` to suppress g++ warnings

---

## Model Config Is Source of Truth

`configs/model_config.yaml` defines:
- Data file paths and column mappings
- Media channel names and adstock decay rates
- Saturation curve parameters (Hill K, beta)
- Model hyperparameters (draws, tune, chains, alpha)
- Optimization constraints (budget cap, SLSQP)

When the user changes parameters, update `model_config.yaml` first, then propagate to notebooks.

---

## Notebook Workflow Pattern

All 9 notebooks follow this execution pattern (see KNOWN_ISSUES §2.1 and §6.2):

1. **Write/edit cells** using `edit_notebook_file` (call `copilot_getNotebookSummary` first for fresh cell IDs)
2. **Execute entire notebook** via terminal:
   ```
   python3.14 -m nbconvert --to notebook --execute \
     --ExecutePreprocessor.timeout=900 \
     --output <name>.ipynb --output-dir notebooks \
     notebooks/<name>.ipynb
   ```
3. **Extract outputs** with a temporary Python script that reads the .ipynb JSON
4. **Append insights** markdown cell using a temporary Python script
5. **Delete helper scripts** after use

**NEVER** rely on `run_notebook_cell` — it is unreliable with externally modified notebooks.

---

## Cross-Notebook Data Flow

Notebooks build on each other. Respect these dependencies:

```
NB01 (EDA) → seasonal indices, VIF, collinearity matrix
    ↓
NB02 (Classical) → Ridge coefficients, R², baseline sales
    ↓
NB03 (Adstock/Saturation) → decay rates, Hill K values, transformed media
    ↓
NB04 (Bayesian) → posterior distributions, credible intervals, ROAS
    ↓
NB05 (Robyn) → hyperparameter ranges, decomposition
    ↓
NB06 (Meridian) → geo-level effects, comparison
    ↓
NB07 (Decomposition) → channel contributions from NB02/NB04
    ↓
NB08 (ROAS) → efficiency metrics from NB02/NB04
    ↓
NB09 (Budget Optimisation) → optimal allocation from NB08 + NB04
```

---

## Output Naming Conventions

- **Figures:** `outputs/figures/{NN}_{description}.png` (e.g., `01_seasonal_decomposition.png`)
- **Models:** `outputs/models/{name}.{ext}` (e.g., `classical_mmm.pkl`, `bayesian_mmm.nc`)
- **Data:** `outputs/models/{name}.parquet` (e.g., `classical_roas.parquet`)
- **Reports:** `outputs/reports/mmm_report.pptx`

---

## Key Data Facts

- Dataset: `data/raw/synthetic_mmm_weekly_india.csv` — 11,232 rows × 28 columns
- National weekly aggregate: 156 rows (filter by groupby or `Geo`)
- Date range: 2022-07-04 to 2025-06-23
- `Week` column is string — always convert with `pd.to_datetime()`
- Sales_Value is right-skewed — always log-transform for regression
- CPI_Value and CPI_Index are near-collinear (VIF=295) — use only one

---

## When Adding New Code

- Read `src/` modules before writing duplicate logic — transforms, data prep, and optimization utilities already exist
- All transforms (adstock, saturation) are in `src/transforms/`
- Budget optimizer is in `src/optimization/budget_optimizer.py`
- Streamlit app pages are in `src/app/pages/`
