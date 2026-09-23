# Quant Lab

Quant Lab is a long-term quantitative finance research laboratory for developing,
testing, and documenting quantitative models, mathematical methods, simulations,
financial analyses, and visualizations.

The repository is intentionally organized by research domain rather than by a
single application. This keeps individual projects discoverable and allows the
lab to grow over time without requiring a structural redesign.

## Goals

- Provide one central home for quantitative finance research.
- Keep exploratory work reproducible and easy to inspect.
- Separate research inputs, analysis, and outputs from reusable model code.
- Make it straightforward to add new models without coupling unrelated work.
- Build a clear portfolio of quantitative research over time.

## Repository structure

```text
Quant Lab/
├── models/          # Shared model components and reusable abstractions
├── risk/            # Risk measurement and risk-management research
├── portfolio/       # Portfolio construction and optimization
├── options/         # Options and derivatives research
├── simulation/      # Monte Carlo and other simulation methods
├── factors/         # Factor research and systematic strategies
├── pricing/         # Asset-pricing and valuation methods
├── market_models/   # Market dynamics and stochastic-process models
├── notebooks/       # Jupyter notebooks for experiments and investigations
├── data/            # Local or retrieved datasets; do not commit secrets
├── figures/         # Charts and other generated visual outputs
├── requirements.txt  # Python dependencies for the research environment
└── README.md        # Project overview and working conventions
```

## Working conventions

- Use notebooks for exploration, explanation, and visual analysis.
- Move stable, reusable logic into the appropriate research domain directory.
- Keep each research question or experiment self-contained and clearly named.
- Record data sources, assumptions, parameter choices, and results in the
  relevant notebook or accompanying documentation.
- Treat files in `data/` and `figures/` as research artifacts. Prefer scripts or
  notebooks that can regenerate them rather than relying on manual edits.
- Do not commit credentials, private datasets, or other sensitive information.

## Getting started

Create and activate a virtual environment, then install the research stack:

```bash
python -m venv .venv

# macOS/Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt
jupyter lab
```

## Adding future research

When a new line of research begins, place reusable implementation in the
closest research domain directory, and place the corresponding investigation in
`notebooks/`. Use `data/` for inputs and `figures/` for generated outputs.
This separation keeps notebooks readable while making the underlying methods
available for later reuse and extension.

Quant Lab currently contains architecture only. Quantitative models and
experiments will be added incrementally as the research program develops.
