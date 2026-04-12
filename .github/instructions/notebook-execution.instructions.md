---
applyTo: "notebooks/*.ipynb"
---

# Notebook Execution Instructions

These instructions apply automatically when working with any Jupyter notebook in the `notebooks/` folder.

## Execution Workflow

**NEVER** use `run_notebook_cell` — it is unreliable (see KNOWN_ISSUES §2.1).

Follow this 5-step workflow for every notebook:

### Step 1: Write or Edit Cells

```
copilot_getNotebookSummary  →  get fresh cell IDs
edit_notebook_file           →  write cell content
```

Always refresh cell IDs before editing. IDs become stale after any external modification.

### Step 2: Execute via Terminal

```bash
python3.14 -m nbconvert --to notebook --execute \
  --ExecutePreprocessor.timeout=900 \
  --output <notebook_name>.ipynb \
  --output-dir notebooks \
  notebooks/<notebook_name>.ipynb
```

**Critical:** `--output` must be just the filename (not a path). The `--output-dir` handles the directory. See KNOWN_ISSUES §2.2.

Timeout by notebook type:
- NB01-NB03, NB07-NB09: `--ExecutePreprocessor.timeout=300`
- NB04 (Bayesian PyMC): `--ExecutePreprocessor.timeout=900`
- NB05 (Robyn R): `--ExecutePreprocessor.timeout=600`
- NB06 (Meridian): `--ExecutePreprocessor.timeout=900`

### Step 3: Extract Outputs

Write a temporary Python script to read the executed `.ipynb` JSON and print cell outputs:

```python
import json
with open('notebooks/<name>.ipynb', encoding='utf-8') as f:
    nb = json.load(f)
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        for out in cell.get('outputs', []):
            if out.get('output_type') == 'stream':
                print(f"--- Cell {i} ---")
                print(''.join(out['text']))
```

Run with: `python3.14 -X utf8 check_script.py`

### Step 4: Append Insights Markdown Cell

Write a temporary Python script to append a markdown cell:

```python
import json, uuid
with open('notebooks/<name>.ipynb', encoding='utf-8') as f:
    nb = json.load(f)
nb['cells'].append({
    "cell_type": "markdown",
    "id": uuid.uuid4().hex[:8],
    "metadata": {},
    "source": "## Key Insights\n\n- Finding 1\n- Finding 2"
})
with open('notebooks/<name>.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
```

### Step 5: Clean Up

Delete all temporary helper scripts after use.

---

## Cross-Notebook Dependencies

Each notebook inherits parameters and findings from earlier notebooks:

| Notebook | Reads From | Produces |
|----------|-----------|----------|
| NB01 | Raw CSV | Seasonal indices, VIF table, collinearity matrix |
| NB02 | Raw CSV | Ridge coefficients, R², baseline sales, `classical_mmm.pkl` |
| NB03 | Raw CSV, NB02 insights | Adstock decay rates, Hill K values, transformed media columns |
| NB04 | Raw CSV, NB03 transforms | Posterior distributions, ROAS, `bayesian_mmm.nc` |
| NB05 | Raw CSV | Robyn decomposition (R-based) |
| NB06 | Raw CSV | Meridian geo-level effects |
| NB07 | NB02 + NB04 outputs | Channel contribution decomposition |
| NB08 | NB02 + NB04 outputs | ROAS efficiency comparison |
| NB09 | NB08 + NB04 outputs | Optimal budget allocation |

**Key inherited values:**
- Adstock decay rates (NB03 → NB04, NB05, NB06): TV=0.7, YouTube=0.4, Facebook=0.35, Instagram=0.3, Print=0.5, Radio=0.45
- Hill saturation K (NB03 → NB04): K=0.5, beta=2.0 per config
- Prior means (NB01/NB02 → NB04): intercept~14.556, beta_Festive~0.17
- Training/test split: 80/20 (first 124 weeks train, last 32 weeks test)

---

## MCMC Notebook-Specific Rules (NB04, NB06)

1. Set `os.environ['PYTENSOR_FLAGS'] = 'cxx='` BEFORE `import pymc`
2. Use `draws=500, tune=500, chains=2` for PyTensor Python-mode
3. Cache InferenceData to `.nc` file — skip re-sampling if file exists
4. Compute `n_post` dynamically: `int(idata.posterior['param'].values.size)`
5. Use `np.trapezoid` (not `np.trapz`) for marginal ROAS

---

## Figure and Artifact Naming

- Figures: `outputs/figures/{NN}_{description}.png` — `NN` is the notebook number
- Models: `outputs/models/{name}.{pkl|nc}` — pickle for sklearn, NetCDF for PyMC
- Data: `outputs/models/{name}.parquet` — ROAS tables, decomposition data
