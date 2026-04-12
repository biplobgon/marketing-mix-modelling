---
mode: "agent"
description: "Execute a single MMM notebook end-to-end with insights"
---

# Run Notebook {{NB_NUMBER}}

Execute notebook `notebooks/{{NB_NUMBER}}_*.ipynb` end-to-end, extract outputs, and append an insights markdown cell.

Read `.github/KNOWN_ISSUES.md` before starting — it contains critical execution workarounds.

## Steps

1. **Refresh cell IDs** — call `copilot_getNotebookSummary` to get current cell IDs.

2. **Review existing cells** — read the notebook to understand what code is already present. If cells contain TODO placeholders, replace them with production code.

3. **Edit cells if needed** — use `edit_notebook_file` with the fresh cell IDs.

4. **Execute via terminal:**
   ```bash
   python3.14 -m nbconvert --to notebook --execute \
     --ExecutePreprocessor.timeout=900 \
     --output {{NB_FILENAME}}.ipynb \
     --output-dir notebooks \
     notebooks/{{NB_FILENAME}}.ipynb
   ```

5. **If execution fails:** Read the traceback, fix the failing cell, and re-execute. Common issues:
   - Timeout → increase `--ExecutePreprocessor.timeout`
   - `np.trapz` → replace with `np.trapezoid`
   - `n_post` mismatch → compute dynamically from posterior shape
   - Import error → install missing package with `--break-system-packages`

6. **Extract outputs** — write a temporary Python script:
   ```python
   import json
   with open('notebooks/{{NB_FILENAME}}.ipynb', encoding='utf-8') as f:
       nb = json.load(f)
   for i, cell in enumerate(nb['cells']):
       if cell['cell_type'] == 'code':
           for out in cell.get('outputs', []):
               if out.get('output_type') == 'stream':
                   print(f"--- Cell {i} ---")
                   print(''.join(out['text']))
   ```
   Run with: `python3.14 -X utf8 check_script.py`

7. **Append insights markdown cell** — write a merge script that adds a `## Key Insights` cell at the end summarising:
   - Top 3-5 quantitative findings (with numbers)
   - Comparison to prior notebook results
   - Implications for downstream notebooks
   - Any anomalies or caveats

8. **Clean up** — delete all temporary helper scripts.

## Output Verification

After execution, confirm:
- [ ] All code cells executed without error
- [ ] Expected figures saved to `outputs/figures/{NN}_*.png`
- [ ] Expected model artifacts saved to `outputs/models/`
- [ ] Key metrics printed (R², MAPE, ROAS, etc.)
- [ ] Insights markdown cell appended at end of notebook
