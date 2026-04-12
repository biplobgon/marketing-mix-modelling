# Known Issues, Loopholes & Workarounds

> **Purpose:** This file documents every pitfall, bug, and non-obvious behaviour encountered while building this repository with an AI agent. Any AI framework reading this file before starting work will avoid hours of wasted time on known issues.

> **Format:** Each entry is structured as **Problem → Root Cause → Workaround** so any agent (Copilot, Claude, Cursor, Devin, etc.) can parse and apply these automatically.

---

## 1. Python Environment Issues

### 1.1 pip install fails with "externally-managed-environment"

**Problem:** `pip install <package>` fails with error: `This environment is externally managed`.

**Root Cause:** Python is installed via `uv` (Astral's package manager), which marks the environment as externally managed per PEP 668.

**Workaround:** Always append `--break-system-packages` to pip install commands:
```bash
python3.14 -m pip install pymc arviz --break-system-packages
```

---

### 1.2 PyTensor runs ~10x slower without g++ compiler

**Problem:** NUTS MCMC sampling takes 5-10 minutes for 500 draws instead of ~30 seconds.

**Root Cause:** PyTensor's compiled C backend requires `g++`. On Windows without MinGW/MSYS2, it falls back to pure Python/NumPy mode. The warning `g++ not available` confirms this.

**Workaround:**
1. Accept slower speed — 500 draws + 500 tune × 2 chains ≈ 5-7 min is tolerable.
2. Set environment variable BEFORE importing pymc to suppress warning noise:
```python
import os
os.environ['PYTENSOR_FLAGS'] = 'cxx='
```
3. For production speed: install MinGW `g++` or use JAX backend (`pip install jax[cpu]`).
4. Always cache sampling results to `.nc` file — skip re-sampling on subsequent runs.

---

### 1.3 NumPy 2.0+ removed `np.trapz`

**Problem:** `AttributeError: module 'numpy' has no attribute 'trapz'`

**Root Cause:** NumPy 2.0 (released 2024) removed the deprecated `np.trapz` function and replaced it with `np.trapezoid`.

**Workaround:** Use a compatibility shim:
```python
_trapz = np.trapezoid if hasattr(np, 'trapezoid') else np.trapz
result = _trapz(y, x)
```

---

### 1.4 ArviZ FutureWarning noise

**Problem:** Every `import arviz` prints a multi-line FutureWarning about refactoring and migration.

**Root Cause:** ArviZ 0.23+ is undergoing a major refactor. The warning is cosmetic.

**Workaround:** Safe to ignore. Does not affect functionality. Can suppress with:
```python
import warnings
warnings.filterwarnings('ignore', category=FutureWarning, module='arviz')
```

---

## 2. Notebook Execution Issues

### 2.1 VS Code `run_notebook_cell` tool is unreliable

**Problem:** The `run_notebook_cell` tool (and `edit_notebook_file` with cell IDs) frequently fails with "invalid cell ID" errors, even with correct IDs.

**Root Cause:** VS Code's internal cell ID mapping drifts when the notebook is modified externally (e.g., by a Python script) or when VS Code reloads the file. The `#VSC-` prefix IDs become stale.

**Workaround:** NEVER rely on `run_notebook_cell` for execution. Instead:
1. Write cells using `edit_notebook_file` (which does work when cell IDs are fresh).
2. Execute the entire notebook via terminal:
```bash
python3.14 -m nbconvert --to notebook --execute \
  --ExecutePreprocessor.timeout=900 \
  --output notebook_name.ipynb \
  --output-dir notebooks \
  notebooks/notebook_name.ipynb
```
3. If cell IDs become stale, call `copilot_getNotebookSummary` to get fresh IDs before editing.

---

### 2.2 nbconvert `--output` path creates nested directories

**Problem:** Running `--output notebooks/04_foo.ipynb` creates `notebooks/notebooks/04_foo.ipynb` (double-nested).

**Root Cause:** `--output` is relative to `--output-dir`. If you include a directory in `--output`, it nests. The `--output` parameter should be just the filename.

**Workaround:** Always separate filename from directory:
```bash
# WRONG — creates nested path
--output notebooks/04_bayesian_mmm_pymc.ipynb

# CORRECT — file goes to notebooks/ as expected
--output 04_bayesian_mmm_pymc.ipynb --output-dir notebooks
```

---

### 2.3 Default nbconvert timeout (30s) is insufficient

**Problem:** `CellTimeoutError` during MCMC sampling, data loading, or heavy computation.

**Root Cause:** nbconvert default cell timeout is 30 seconds. MCMC cells in PyTensor Python-mode can take 5-10 minutes.

**Workaround:** Always set timeout explicitly:
```bash
--ExecutePreprocessor.timeout=900   # 15 minutes — safe for MCMC cells
```

Timeout recommendations by notebook:
| Notebook | Recommended Timeout |
|----------|-------------------|
| NB01-NB03 | 300 (5 min) |
| NB04 (Bayesian) | 900 (15 min) |
| NB05 (Robyn) | 600 (10 min) |
| NB06 (Meridian) | 900 (15 min) |
| NB07-NB09 | 300 (5 min) |

---

### 2.4 Extracting cell outputs from executed notebooks

**Problem:** After `nbconvert --execute`, outputs are embedded in the `.ipynb` JSON but you need to read them programmatically.

**Root Cause:** `.ipynb` files are JSON. Cell outputs live in `cell['outputs']` as stream text or display_data (base64 images).

**Workaround:** Use a Python extraction script:
```python
import json
with open('notebooks/04_bayesian_mmm_pymc.ipynb', encoding='utf-8') as f:
    nb = json.load(f)
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        for out in cell.get('outputs', []):
            if out.get('output_type') == 'stream':
                print(''.join(out['text']))
```

---

### 2.5 Cell IDs shift after VS Code reloads

**Problem:** `edit_notebook_file` fails with "invalid cell ID" after the notebook has been modified by another tool (e.g., nbconvert, a merge script, or manual edit).

**Root Cause:** VS Code's internal cell ID mapping (`#VSC-XXXXXXXX`) is generated from the notebook JSON `id` field. When a Python script modifies the JSON and saves, VS Code's mapping becomes stale.

**Workaround:** Always call `copilot_getNotebookSummary` immediately before using `edit_notebook_file` to get fresh cell IDs.

---

## 3. MCMC / Bayesian Modelling Issues

### 3.1 MCMC sampling exceeds cell timeout in Python-mode

**Problem:** 1000 draws × 2 chains takes ~600s in PyTensor Python-mode, exceeding the 600s cell timeout.

**Root Cause:** Without a compiled C backend (g++), NUTS evaluation is ~0.27s/step in pure Python. With 1000 tune + 1000 draws × 2 chains = 4000 steps ≈ 1080s.

**Workaround:**
- Use `draws=500, tune=500, chains=2` — achieves ~1000 total samples in ~5-7 min.
- This is statistically sufficient: ESS > 400 for most parameters, R-hat diagnostics valid.
- For production: install g++ or use JAX backend for 10x speedup.

---

### 3.2 Always cache InferenceData to `.nc` file

**Problem:** Re-running the notebook re-samples MCMC (5-10 min wasted on every execution).

**Root Cause:** No caching logic in the sampling cell.

**Workaround:** Add cache-first logic:
```python
nc_path = f'{MODEL_DIR}/bayesian_mmm.nc'
if os.path.exists(nc_path):
    idata = az.from_netcdf(nc_path)
else:
    with model:
        idata = pm.sample(draws=500, tune=500, chains=2, ...)
    idata.to_netcdf(nc_path)
```

---

### 3.3 `n_post` must be computed dynamically, not hardcoded

**Problem:** `ValueError: cannot reshape array of size 1000 into shape (2000,)` when computing ROAS from posterior samples.

**Root Cause:** Code hardcoded `n_post = 2000` (assuming 1000 draws × 2 chains), but actual sampling used 500 draws × 2 chains = 1000 samples.

**Workaround:** Always compute dynamically:
```python
n_post = int(idata.posterior['beta_TV'].values.size)
```

---

### 3.4 Instagram-YouTube collinearity requires Bayesian priors

**Problem:** Ridge regression forces `beta_Instagram = 0` because of multicollinearity (r=0.96 raw, r=0.91 post-transform).

**Root Cause:** L2 regularisation cannot distinguish between two highly correlated predictors — it shrinks one to zero instead of sharing the effect.

**Workaround:** Use Bayesian HalfNormal priors — soft regularisation that allows both channels to have positive posteriors:
```python
beta_Instagram = pm.HalfNormal('beta_Instagram', sigma=0.10)
```
This gives Instagram a positive posterior mean (~0.085 with 94% HDI excluding zero), consistent with industry expectations.

---

### 3.5 Prior specification should be informed by earlier notebooks

**Problem:** Uninformative priors produce wide, unhelpful posteriors or slow convergence.

**Root Cause:** With only 124 training observations and 12 parameters, weakly informative priors are critical.

**Workaround:** Use findings from NB01, NB02, NB03 to inform priors:
| Parameter | Prior | Justification |
|-----------|-------|--------------|
| intercept | Normal(14.556, 0.5) | Mean log-sales from data |
| beta_TV | HalfNormal(0.20) | Largest channel in NB02 |
| beta_Festive | Normal(0.17, 0.10) | NB01 STL: +17.7% uplift |
| beta_WeightedDist | Normal(0.15, 0.20) | NB02 Ridge coef=0.169 |
| beta_Instagram | HalfNormal(0.10) | Own prior (wider than Ridge) |

---

## 4. Windows / PowerShell Issues

### 4.1 No `head`, `tail`, `grep` commands

**Problem:** Unix commands like `head -20 file.txt` or `grep pattern file` fail in PowerShell.

**Root Cause:** These are Unix coreutils, not available in Windows PowerShell by default.

**Workaround:**
```powershell
# Instead of: head -20 file.txt
Get-Content file.txt | Select-Object -First 20

# Instead of: tail -10 file.txt
Get-Content file.txt | Select-Object -Last 10

# Instead of: grep "pattern" file.txt
Select-String -Pattern "pattern" -Path file.txt

# Instead of: wc -l file.txt
(Get-Content file.txt | Measure-Object -Line).Lines
```

---

### 4.2 UTF-8 handling requires explicit flag

**Problem:** Scripts that print Unicode characters (box-drawing, arrows, etc.) produce garbled output or encoding errors.

**Root Cause:** Windows PowerShell defaults to system locale encoding (often CP1252), not UTF-8.

**Workaround:** Always use the `-X utf8` flag:
```bash
python3.14 -X utf8 notebooks/check_nb4.py
```

---

### 4.3 MCMC chain processes appear as `python` not `python3.14`

**Problem:** When monitoring MCMC with `Get-Process`, the kernel spawns child processes named `python`, not `python3.14`.

**Root Cause:** The Jupyter kernel executable resolves to the base Python name in the process table.

**Workaround:**
```powershell
Get-Process python 2>$null | Sort-Object CPU -Descending | Select-Object -First 5 Id, CPU
```
The top 2 processes by CPU are the MCMC chains.

---

## 5. Data-Specific Issues

### 5.1 CPI columns have extreme multicollinearity (VIF=295)

**Problem:** Including both `CPI_Value` and `CPI_Index` in the regression produces unstable coefficients.

**Root Cause:** These two columns are near-perfect linear transforms of each other.

**Workaround:** NEVER include both. Use `log(CPI_Index)` as the single CPI control variable. VIF screening in NB01 confirms this — all other VIFs are below 10.

---

### 5.2 Sales_Value is right-skewed — must log-transform

**Problem:** Linear regression on raw Sales_Value produces heteroscedastic residuals and poor fit.

**Root Cause:** FMCG sales data is inherently right-skewed — large festive spikes, log-normal distribution.

**Workaround:** Always use `np.log(Sales_Value)` as the dependent variable. All notebooks in this project operate in log-sales space.

---

### 5.3 `Week` column is stored as string

**Problem:** Time-series operations fail because the date column isn't a datetime type.

**Root Cause:** CSV parsing reads dates as strings by default.

**Workaround:**
```python
df['date'] = pd.to_datetime(df['Week'])
```

---

### 5.4 National aggregate requires explicit filtering or grouping

**Problem:** Running models on all 11,232 rows treats geos/brands as independent observations (wrong for national-level MMM).

**Root Cause:** The dataset is at Geo × Brand × SKU granularity. National models need weekly aggregates.

**Workaround:**
```python
# Aggregate to national weekly level (156 rows)
media_cols = ['TV_Impressions', 'YouTube_Impressions', ...]
data_natl = df.groupby('date')[media_cols + ['Sales_Value']].sum().reset_index()
```

---

## 6. General Workflow Issues

### 6.1 Notebook insights cell must be appended programmatically

**Problem:** After executing a notebook with nbconvert, you can't easily add a markdown cell via the VS Code tool API.

**Root Cause:** `edit_notebook_file` with `add_after` sometimes rejects markdown content with special characters (tables, Unicode).

**Workaround:** Use a Python script to append the cell:
```python
import json, uuid
with open('notebooks/04_foo.ipynb', encoding='utf-8') as f:
    nb = json.load(f)
nb['cells'].append({
    "cell_type": "markdown",
    "id": uuid.uuid4().hex[:8],
    "metadata": {},
    "source": "## Insights\n\nYour markdown here..."
})
with open('notebooks/04_foo.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
```

---

### 6.2 The tested notebook workflow pattern

After extensive trial and error, this is the most reliable workflow for AI agents:

1. **Write/edit cells** using `edit_notebook_file` (refresh cell IDs first with `copilot_getNotebookSummary`)
2. **Execute** via terminal: `python3.14 -m nbconvert --to notebook --execute --ExecutePreprocessor.timeout=900 --output name.ipynb --output-dir notebooks notebooks/name.ipynb`
3. **Extract outputs** using a Python script that reads the JSON (see 2.4)
4. **Append insights** using a Python script that modifies the JSON (see 6.1)
5. **Clean up** temp helper scripts

This pattern was validated across NB01-NB04 (40+ cell executions, 23+ figures generated).
