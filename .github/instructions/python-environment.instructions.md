---
applyTo: "**/*.py"
---

# Python Environment Instructions

These instructions apply automatically when working with any Python file in this project.

## Runtime

- **Interpreter:** `python3.14` (managed by `uv`)
- **Executable path:** `C:\Users\BIPLOB GON\.local\bin\python3.14.exe` (Windows; varies on Linux/Mac)
- **Package manager:** `uv` — but pip is used for installs

## Package Installation

Always use `--break-system-packages` because the environment is `uv`-managed (PEP 668):

```bash
python3.14 -m pip install <package> --break-system-packages
```

Never use bare `pip install`. Always prefix with `python3.14 -m pip`.

## NumPy 2.0+ Compatibility

This project uses NumPy 2.x. The following functions were removed or renamed:

| Removed | Replacement |
|---------|------------|
| `np.trapz()` | `np.trapezoid()` |
| `np.bool` | `bool` |
| `np.int` | `int` |
| `np.float` | `float` |
| `np.str` | `str` |
| `np.object` | `object` |

Use this compatibility pattern when supporting both NumPy 1.x and 2.x:

```python
_trapz = np.trapezoid if hasattr(np, 'trapezoid') else np.trapz
```

## PyTensor / PyMC Configuration

PyTensor needs a C++ compiler for fast sampling. On systems without `g++`:

```python
import os
os.environ['PYTENSOR_FLAGS'] = 'cxx='  # MUST be set before import pymc
import pymc as pm
```

This suppresses the `g++ not available` warning and explicitly uses Python-mode.

## UTF-8 Output

When running Python scripts that produce Unicode characters (tables, box-drawing, arrows):

```bash
python3.14 -X utf8 script.py
```

## Import Conventions

Standard import aliases used across this project:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import arviz as az
import pymc as pm
```

## Key Modules in `src/`

Before writing new code, check if the functionality already exists:

| Module | Purpose |
|--------|---------|
| `src/data_prep.py` | Data loading, cleaning, aggregation |
| `src/transforms/adstock.py` | Geometric and Weibull adstock transforms |
| `src/transforms/saturation.py` | Hill saturation function |
| `src/models/classical_mmm.py` | Ridge regression MMM |
| `src/models/bayesian_mmm.py` | PyMC Bayesian MMM |
| `src/models/meridian_mmm.py` | Google Meridian wrapper |
| `src/optimization/budget_optimizer.py` | SLSQP budget optimization |
| `src/reports/generate_pptx.py` | PowerPoint report generation |
| `src/app/pages/` | Streamlit dashboard pages |

## Windows PowerShell Equivalents

When running from PowerShell (no Unix coreutils):

```powershell
# head -20
Get-Content file.txt | Select-Object -First 20

# tail -10
Get-Content file.txt | Select-Object -Last 10

# grep pattern
Select-String -Pattern "pattern" -Path file.txt

# wc -l
(Get-Content file.txt | Measure-Object -Line).Lines
```
