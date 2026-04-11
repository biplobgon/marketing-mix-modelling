# 📊 Marketing Mix Modelling (MMM)

> **End-to-end Marketing Mix Modelling system** covering Traditional Constrained Regression, Meta Robyn, Google Meridian & Bayesian PyMC-Marketing — with ROAS attribution, budget optimisation, Streamlit dashboard, and a stakeholder deck.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![R](https://img.shields.io/badge/R-4.3%2B-276DC3?style=flat-square&logo=r&logoColor=white)](https://www.r-project.org/)
[![PyMC](https://img.shields.io/badge/PyMC--Marketing-0.18%2B-orange?style=flat-square)](https://www.pymc-marketing.io/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Kaggle](https://img.shields.io/badge/Dataset-Kaggle-20BEFF?style=flat-square&logo=kaggle&logoColor=white)](https://www.kaggle.com/)

---

## 📌 Table of Contents

1. [Business Problem](#-business-problem)
2. [Key Business Questions](#-key-business-questions)
3. [What is Marketing Mix Modelling?](#-what-is-marketing-mix-modelling)
4. [MMM Frameworks Covered](#-mmm-frameworks-covered)
5. [Core MMM Concepts](#-core-mmm-concepts)
6. [Datasets](#-datasets)
7. [Project Architecture](#-project-architecture)
8. [Notebooks Walkthrough](#-notebooks-walkthrough)
9. [Streamlit Dashboard](#-streamlit-dashboard)
10. [Stakeholder Deck](#-stakeholder-deck)
11. [Key Results & Findings](#-key-results--findings)
12. [Tech Stack](#-tech-stack)
13. [How to Reproduce](#-how-to-reproduce)
14. [References](#-references)
15. [License](#-license)

---

## 🎯 Business Problem

Every marketing team faces the same fundamental question: **of all the money we spend on advertising, what is actually working?**

In a world of fragmented media — TV, digital, social, print, radio, trade promotions — attributing sales to the right channels is notoriously hard. Last-click attribution models fail to capture **offline effects**, **lagged returns**, and **diminishing returns**. Platform-reported ROAS is inflated by self-attribution bias. And with the deprecation of third-party cookies, privacy-safe measurement has become mission-critical.

**Marketing Mix Modelling (MMM)** is the gold-standard econometric approach that solves this problem using aggregated, top-down statistical analysis — immune to privacy changes, capable of measuring both online and offline channels simultaneously, and able to decompose macro, seasonal, and promotional effects from pure media contribution.

This repository demonstrates the full MMM workflow — from raw media spend data to actionable budget reallocation — across multiple industry-standard frameworks, applied to a realistic FMCG marketing dataset.

---

## ❓ Key Business Questions

| # | Question | MMM Component |
|---|----------|--------------|
| 1 | **What percentage of sales is driven by media vs. baseline?** | Sales Decomposition |
| 2 | **Which channels deliver the highest Return on Ad Spend (ROAS)?** | ROAS Attribution |
| 3 | **Are we over-investing in saturated channels?** | Saturation Analysis |
| 4 | **What is the optimal budget allocation to maximise revenue?** | Budget Optimisation |
| 5 | **How long does the effect of advertising persist after a campaign ends?** | Adstock / Carryover |
| 6 | **How do macroeconomic factors (CPI, seasonality, festivals) affect baseline sales?** | Macro Controls |
| 7 | **What is the marginal ROAS — i.e., what does the next £1 of spend actually return?** | mROAS Curves |
| 8 | **Are there geo-level differences in channel effectiveness?** | Hierarchical Geo MMM |
| 9 | **How does creative quality interact with media spend efficiency?** | Creative × Media |
| 10 | **What is the ROI improvement achievable through spend reallocation alone?** | Scenario Planning |

---

## 📐 What is Marketing Mix Modelling?

Marketing Mix Modelling is a statistical framework that decomposes sales (or any KPI) into its constituent drivers:

$$
\text{Sales}_t = \underbrace{\alpha}_{\text{Baseline}} + \underbrace{\sum_{m=1}^{M} \beta_m \cdot f(x_{m,t})}_{\text{Media Contribution}} + \underbrace{\sum_{c=1}^{C} \gamma_c \cdot z_{c,t}}_{\text{Control Variables}} + \underbrace{\varepsilon_t}_{\text{Error}}
$$

Where:
- $\alpha$ = intercept / baseline sales (what would sell without any marketing)
- $f(x_{m,t})$ = media transformation function (encoding **adstock** + **saturation** effects)
- $z_{c,t}$ = control variables: seasonality, CPI, promotions, holidays, distribution
- $\varepsilon_t$ = error term, assumed $\sim \mathcal{N}(0, \sigma^2)$

The transformation function $f(\cdot)$ encodes two critical phenomena:

**1. Adstock (Carryover Effect)** — The effect of advertising does not end when the campaign ends. It decays geometrically over time:

$$
x_{m,t}^{\text{adstock}} = x_{m,t} + \alpha_m \cdot x_{m,t-1}^{\text{adstock}}
$$

Where $\alpha_m \in [0, 1]$ is the **decay / retention rate** for channel $m$.

**2. Saturation (Diminishing Returns)** — Additional spend beyond a threshold yields progressively less incremental sales. Modelled via the Hill function:

$$
f(x) = \frac{x^{\beta}}{x^{\beta} + K^{\beta}}
$$

Where $K$ is the **half-saturation point** and $\beta$ controls the shape of the curve.

---

## 🔬 MMM Frameworks Covered

This repository implements and compares **four industry-standard MMM frameworks**:

### 1. Traditional Constrained Regression (Classical MMM)
- **Stack**: Python, `statsmodels`, `scikit-learn`, `scipy`
- Pre-applies adstock transformations to media variables as engineered features
- Fits Ridge/Lasso regression with **non-negativity constraints** on media coefficients (media can only help, not hurt)
- Uses `scipy.optimize.minimize` with constraint definitions
- Suitable for fast, interpretable, production-ready models
- **Benchmark**: This is the historical industry standard used by Nielsen, IRI, and traditional media agencies

### 2. Meta Robyn (Bayesian-Regularised Ridge + Evolutionary Optimisation)
- **Stack**: R, `Robyn` package, `reticulate` for Python interoperability
- Combines Ridge regression with **Nevergrad evolutionary algorithm** to explore thousands of model solutions
- Generates a **Pareto-optimal frontier** of models (accuracy vs. business fit)
- Automatically calculates response curves, saturation points, and one-pager summary charts
- **Key innovation**: Multi-objective optimisation avoids over-fitting to a single solution
- Produces budget allocator out of the box

### 3. Google Meridian (Bayesian Hierarchical MMM)
- **Stack**: Python, `meridian`, `JAX`, `TensorFlow Probability`
- Google's latest open-source MMM (released Jan 2025, successor to LightweightMMM)
- Supports **geo-level hierarchical modelling** with partial pooling across geographies
- Expresses adstock via **Weibull distribution** (more flexible than geometric)
- Fully Bayesian: uncertainty propagates through to budget recommendations
- **Key innovation**: Native geo-level support for large countries/markets

### 4. Bayesian MMM — PyMC-Marketing
- **Stack**: Python, `pymc-marketing`, `PyMC`, `ArviZ`, `NumPy`
- Implements the Google Carryover + Shape paper (Jin et al., 2017) in a Bayesian framework
- Prior distributions encode domain knowledge (e.g., spend share → media prior sigma)
- Full posterior distribution over **ROAS**, **adstock decay**, and **saturation parameters**
- Supports **lift-test calibration** to anchor priors from experiments
- Generates uncertainty-aware budget recommendations
- **Key innovation**: Bayesian credible intervals on ROI recommendations, not just point estimates

---

## 🧠 Core MMM Concepts

Understanding these concepts is essential for building credible, actionable MMMs. This repository demonstrates each one.

### Adstock Transformations

| Type | Formula | Best For |
|------|---------|---------|
| **Geometric Adstock** | $x_t^* = x_t + \alpha \cdot x_{t-1}^*$ | TV, Radio — simple decay |
| **Weibull Adstock** | $x_t^* = \sum_{\tau} x_{t-\tau} \cdot w(\tau; \lambda, k)$ | Digital — delayed peak effect |
| **No Adstock** | $x_t^* = x_t$ | Promotions, Price — immediate effect |

### Saturation Functions

| Type | Formula | Best For |
|------|---------|---------|
| **Hill/Power** | $S(x) = \frac{x^\beta}{x^\beta + K^\beta}$ | Most media channels |
| **Logistic** | $S(x) = \frac{1}{1 + e^{-\lambda(x - \mu)}}$ | Channels with clear saturation threshold |
| **Negative Exponential** | $S(x) = 1 - e^{-ax}$ | Linear-then-flat response |

### ROAS vs. mROAS

| Metric | Definition | Use Case |
|--------|-----------|---------|
| **ROAS** (Return on Ad Spend) | $\text{ROAS} = \frac{\text{Incremental Revenue}}{\text{Media Spend}}$ | Historical efficiency measurement |
| **mROAS** (Marginal ROAS) | $\text{mROAS} = \frac{\partial \text{Revenue}}{\partial \text{Spend}}$ | Forward-looking optimisation decisions |

> ⚠️ A channel with high historical ROAS may have low mROAS if it is already **saturated** — meaning the next pound spent will return diminishing incremental revenue. Budget optimisation should always be driven by **mROAS**, not ROAS.

### Sales Decomposition Components

```
Total Sales
├── Baseline (non-media driven)
│   ├── Structural Baseline (long-run demand)
│   ├── Macro Effects (CPI, economic cycles)
│   ├── Seasonal Effects (festivals, weather)
│   └── Distribution & Availability
└── Incremental (media & promotion driven)
    ├── TV Contribution
    ├── Digital (YouTube, Facebook, Instagram)
    ├── Print / Radio
    ├── Trade Promotions (Feature, Display, TPR)
    └── Price Elasticity Effects
```

### The Collinearity Challenge

MMM practitioners face a fundamental identification problem: media channels are often **bought simultaneously** (TV + Digital in the same festive burst), making it statistically difficult to attribute sales to individual channels. Solutions implemented in this repo:

- **Bayesian priors**: Inject domain knowledge to constrain implausible parameter ranges
- **Ridge regularisation**: Shrinks collinear coefficients towards zero
- **Hierarchical pooling** (Meridian): Borrow strength across geographies
- **Lift-test calibration** (PyMC-Marketing): Anchor channel effects using controlled experiments

---

## 📦 Datasets

### Primary Dataset — MMM Weekly Data: Geo India (Synthetic FMCG)

| Property | Detail |
|----------|--------|
| **Source** | [Kaggle — subhagatoadak](https://www.kaggle.com/datasets/subhagatoadak/mmm-weekly-data-geoindia) |
| **Rows** | 11,232 (156 weeks × 8 geographies × 3 brands × 3 SKUs) |
| **Columns** | 28 |
| **Date Range** | July 2022 – June 2025 (3 years, weekly) |
| **Geographies** | NORTH, SOUTH, EAST, WEST, CENTRAL, NORTHEAST, METRO_DELHI, METRO_MUMBAI |
| **Media Channels** | TV, YouTube, Facebook, Instagram, Print, Radio |
| **Promo Variables** | Feature Flag, Display Flag, TPR Flag, Trade Spend |
| **Macro Controls** | CPI, GDP Growth Index, Festival Index, Rainfall Index |
| **Creative Signals** | FB Banner Content Score, IG Banner Content Score (AI-generated, 0–100) |
| **Distribution** | Weighted Distribution, Numeric Distribution, TDP, NOS |
| **License** | Apache 2.0 |

*Note: Behaviourally realistic synthetic data designed to mirror Indian FMCG category dynamics — not proprietary commercial data.*

### Secondary Dataset — Synthetic MMM Weekly India (Saturation Variant)

| Property | Detail |
|----------|--------|
| **File** | `synthetic_mmm_weekly_india_SAT.csv` |
| **Rows** | 11,232 (156 weeks × 8 geographies × 3 brands × 3 SKUs) |
| **Columns** | 28 |
| **Purpose** | Saturation-pre-transformed variant of the primary dataset — used to validate adstock/saturation transform pipelines and benchmark models against pre-processed inputs |

### Baseline Dataset — Classic Advertising (TV / Radio / Newspaper → Sales)

| Property | Detail |
|----------|--------|
| **Source** | [Kaggle — mehmetisik](https://www.kaggle.com/datasets/mehmetisik/advertisingcsv) |
| **Rows** | 200 |
| **Columns** | 4 (TV, Radio, Newspaper spends + Sales) |
| **Purpose** | Pedagogical baseline — illustrates Classical OLS MMM, partial R², VIF |

---

## 🏗️ Project Architecture

```
marketing-mix-modelling/
│
├── README.md
├── LICENSE
├── requirements.txt                   ← Python dependencies
├── requirements_r.txt                 ← R / Robyn dependencies
├── app.py                             ← Streamlit dashboard entry point
│
├── data/
│   ├── raw/                           ← Gitignored; use download script
│   │   ├── synthetic_mmm_weekly_india.csv
│   │   ├── synthetic_mmm_weekly_india_SAT.csv
│   │   └── advertising.csv
│   └── processed/                     ← Feature-engineered datasets
│
├── notebooks/
│   ├── 01_eda_seasonality.ipynb
│   ├── 02_classical_mmm_regression.ipynb
│   ├── 03_adstock_saturation_transforms.ipynb
│   ├── 04_bayesian_mmm_pymc.ipynb
│   ├── 05_robyn_mmm_r.ipynb           ← R kernel (IRkernel)
│   ├── 06_meridian_mmm_google.ipynb
│   ├── 07_sales_decomposition.ipynb
│   ├── 08_roas_channel_efficiency.ipynb
│   └── 09_budget_optimisation.ipynb
│
├── src/
│   ├── data_prep.py
│   ├── transforms/
│   │   ├── adstock.py                 ← Geometric, Weibull adstock
│   │   └── saturation.py             ← Hill, Logistic saturation
│   ├── models/
│   │   ├── classical_mmm.py          ← Constrained Ridge regression
│   │   ├── bayesian_mmm.py           ← PyMC-Marketing wrapper
│   │   └── meridian_mmm.py           ← Google Meridian wrapper
│   ├── optimization/
│   │   └── budget_optimizer.py       ← scipy-based spend allocation
│   ├── app/
│   │   ├── pages/
│   │   │   ├── 1_overview.py
│   │   │   ├── 2_attribution.py
│   │   │   ├── 3_response_curves.py
│   │   │   ├── 4_budget_optimizer.py
│   │   │   ├── 5_scenario_planner.py
│   │   │   └── 6_framework_comparison.py
│   │   └── components.py
│   └── reports/
│       └── generate_pptx.py          ← Auto-generate stakeholder deck
│
├── outputs/
│   ├── figures/
│   ├── models/                        ← Serialised posteriors (.nc, .pkl)
│   └── reports/
│       └── MMM_Stakeholder_Deck.pptx
│
└── configs/
    └── model_config.yaml
```

---

## 📓 Notebooks Walkthrough

| # | Notebook | Framework | Key Topics |
|---|----------|-----------|------------|
| `01` | **EDA & Seasonality Decomposition** | — | Distribution analysis, STL decomposition, festive/monsoon signals, channel correlation heatmap, VIF screening |
| `02` | **Classical MMM — Constrained Regression** | Statsmodels / scikit-learn | OLS baseline → Ridge with Adstock pre-transforms → non-negativity constraints → partial R² attribution |
| `03` | **Adstock & Saturation Transform Library** | NumPy / SciPy | Geometric vs Weibull adstock curves; Hill vs Logistic saturation; parameter sensitivity; response curve visualisation |
| `04` | **Bayesian MMM with PyMC-Marketing** | PyMC / ArviZ | Prior elicitation, MCMC (NUTS), convergence diagnostics (R-hat, ESS), posterior predictive checks, contribution recovery |
| `05` | **MMM with Meta Robyn** | R / Robyn | Nevergrad evolutionary optimisation, Pareto frontier of model solutions, one-pager output, budget allocator |
| `06` | **MMM with Google Meridian** | Meridian / JAX | Bayesian hierarchical geo-level model, Weibull adstock, partial pooling, MCMC, geo-level ROAS |
| `07` | **Sales Decomposition & Attribution** | All frameworks | Waterfall chart, stacked area decomposition, baseline vs incremental, macro-adjusted baseline |
| `08` | **ROAS, mROAS & Channel Efficiency** | All frameworks | Per-channel ROAS ranking, marginal ROAS curves, saturation identification, spend-efficiency frontier |
| `09` | **Budget Optimisation & Scenario Planning** | PyMC + scipy | Constrained optimisation, flat / +10% / +25% budget scenarios, ROI lift quantification, reallocation recommendations |

---

## 🖥️ Streamlit Dashboard

An interactive budget allocation and scenario planning dashboard built with Streamlit.

**Launch:**
```bash
streamlit run app.py
```

**Dashboard Pages:**

| Page | Description |
|------|-------------|
| 📊 **Overview** | Total sales, total media spend, overall ROAS, data summary |
| 🎯 **Channel Attribution** | Interactive waterfall + stacked contribution chart (Plotly) |
| 📈 **Response Curves** | Adstock decay slider + saturation curve per channel |
| 💰 **Budget Optimiser** | Input total budget → optimal allocation + projected incremental sales |
| 🔮 **Scenario Planner** | Compare 3 budget scenarios side-by-side with ROI delta |
| ⚖️ **Framework Comparison** | Side-by-side ROAS estimates from all 4 frameworks |

---

## 📑 Stakeholder Deck

A professionally generated PowerPoint deck suitable for C-suite and board-level stakeholder presentations.

**Generate:**
```bash
python src/reports/generate_pptx.py
```

**Output**: `outputs/reports/MMM_Stakeholder_Deck.pptx`

**Slide Structure (15 slides):**

| Slide | Title |
|-------|-------|
| 1 | Cover — Project Title & Tagline |
| 2 | Executive Summary — 3-box "So What" |
| 3 | The Business Problem & Data Landscape |
| 4 | MMM Methodology Overview & DAG |
| 5 | Data & Channels in Scope |
| 6 | Adstock & Saturation Effects |
| 7 | Framework Comparison — 4-model ROAS side-by-side |
| 8 | Sales Decomposition Waterfall |
| 9 | Channel Contribution & ROAS Ranked |
| 10 | Marginal ROAS & Saturation Frontier |
| 11 | Budget Optimisation Results |
| 12 | Scenario Comparison Table |
| 13 | Strategic Recommendations (2×2 Efficiency vs Scale Matrix) |
| 14 | Risks & Model Limitations |
| 15 | Appendix — Technical Notes & Model Equations |

---

## 📊 Key Results & Findings

> *Results based on the synthetic India FMCG dataset. Directional findings are behaviourally realistic by design.*

| Finding | Detail |
|---------|--------|
| **Baseline vs. Media split** | ~55–65% of sales attributable to structural baseline; 35–45% media-driven |
| **Highest ROAS channel** | Facebook + Instagram (digital) — high frequency, strong creative quality effect |
| **Most saturated channel** | TV — festive-season heavy buys push spend past the half-saturation point |
| **Key adstock decay** | TV: ~8–10 week carryover; Digital: ~2–3 week carryover |
| **Macro effect** | Festival Index accounts for ~12–15% uplift during Sep–Nov Diwali window |
| **Creative quality** | 1-SD improvement in `FB_Banner_Content_Score` → ~6–8% uplift in Facebook ROAS |
| **Budget reallocation uplift** | Shifting ~15% of TV budget to under-invested digital channels → **~22–25% revenue uplift** under constant total spend |
| **Framework convergence** | All four frameworks agree directionally on channel ranking; Bayesian models provide uncertainty bounds of ±15–20% on ROAS estimates |

---

## 🛠️ Tech Stack

**Python**

| Library | Purpose |
|---------|---------|
| `pandas`, `numpy` | Data manipulation |
| `statsmodels` | OLS / GLS classical regression |
| `scikit-learn` | Ridge / Lasso, preprocessing |
| `scipy` | Constrained optimisation, curve fitting |
| `pymc` | Bayesian probabilistic programming |
| `pymc-marketing` | MMM-specific adstock / saturation transforms, ROAS |
| `meridian` | Google Bayesian hierarchical MMM |
| `arviz` | Bayesian diagnostics, posterior visualisation |
| `jax` | Accelerated numerical computation (Meridian backend) |
| `plotly` | Interactive visualisations |
| `matplotlib`, `seaborn` | Static charts |
| `streamlit` | Interactive dashboard |
| `python-pptx` | Automated PowerPoint generation |

**R**

| Package | Purpose |
|---------|---------|
| `Robyn` | Meta's MMM framework (evolutionary optimisation) |
| `reticulate` | R–Python interoperability |
| `nevergrad` (via Python) | Evolutionary algorithm backend for Robyn |

---

## ▶️ How to Reproduce

### 1. Clone the Repository
```bash
git clone https://github.com/biplobgon/marketing-mix-modelling.git
cd marketing-mix-modelling
```

### 2. Create Environment & Install Dependencies
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Download Datasets (Kaggle API)
```bash
pip install kaggle
# Place kaggle.json credentials in ~/.kaggle/
kaggle datasets download -d subhagatoadak/mmm-weekly-data-geoindia -p data/raw/ --unzip
kaggle datasets download -d mehmetisik/advertisingcsv -p data/raw/ --unzip
```

### 4. Run Notebooks
```bash
jupyter lab
```
Run notebooks in order: `01` → `09`

### 5. Launch Streamlit Dashboard
```bash
streamlit run app.py
```

### 6. Generate Stakeholder Deck
```bash
python src/reports/generate_pptx.py
```

### 7. Robyn (R Notebook, optional)
```r
install.packages("Robyn")
# Open notebooks/05_robyn_mmm_r.ipynb with R kernel (IRkernel)
```

---

## 📚 References

| Paper / Resource | Description |
|-----------------|-------------|
| [Jin et al. (2017) — Google](https://research.google/pubs/pub46001/) | Bayesian Methods for Media Mix Modelling with Carryover and Shape Effects |
| [Chan & Perry (2017) — Google](https://research.google/pubs/pub45998/) | Challenges and Opportunities in Media Mix Modelling |
| [Sun et al. (2017) — Google](https://research.google/pubs/pub46000/) | Geo-level Bayesian Hierarchical Media Mix Modelling |
| [Meta Robyn](https://facebookexperimental.github.io/Robyn/) | Meta's Open-Source MMM Framework |
| [Google Meridian](https://developers.google.com/meridian) | Google's Latest Bayesian MMM (2025) |
| [PyMC-Marketing Docs](https://www.pymc-marketing.io/) | Bayesian MMM with PyMC |
| [Binet & Field (2013)](https://ipa.co.uk/) | *The Long and the Short of It* — brand vs. activation balance |
| [Shapley Value Attribution](https://arxiv.org/abs/2109.05735) | Fair channel attribution using cooperative game theory |

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

Datasets are sourced from Kaggle under their respective licences (Apache 2.0 for primary dataset).

---

## 🙋‍♂️ About

Built by **[Biplob Gon](https://github.com/biplobgon)** — Data Scientist & ML Engineer with domain expertise in Marketing Analytics, MMM, and Causal Inference.

> *"Half the money I spend on advertising is wasted; the trouble is I don't know which half."* — John Wanamaker, 1919
>
> **MMM exists to answer exactly that question.**

---

*If you find this repository useful, please ⭐ star it — it helps others discover the project.*
