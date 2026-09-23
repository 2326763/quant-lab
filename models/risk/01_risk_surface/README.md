# Model 01 — Portfolio Risk Surface

This project studies how a single-position portfolio's stressed potential loss
changes with annualized volatility, position size, and stop-loss distance. It is
an analytical research model, not a backtest and not investment advice.

## Research question

For a portfolio with a fixed account value, how do exposure size and the
distance to a stop-loss interact with market volatility to determine a
conservative one-period loss estimate?

## Model definition

The model uses a normalized asset price and a one-sided normal volatility shock.
The loss estimate is:

```text
L = V × w × (d + zα × σ × sqrt(h / D))
```

where:

- `L` is modeled potential loss in currency units.
- `V` is portfolio value.
- `w` is position size as a fraction of portfolio value.
- `d` is stop-loss distance as a decimal return.
- `σ` is annualized volatility as a decimal.
- `zα` is the standard-normal quantile for confidence level `α`.
- `h` is the holding horizon in trading days.
- `D` is the number of trading days in a year.

The stop-loss term represents the planned loss threshold. The volatility term
represents an additional adverse one-sided shock over the holding horizon. This
additive construction is deliberately conservative and makes the interaction
between operational risk controls and market variability explicit.

The notebook uses illustrative assumptions only:

- portfolio value: `$100,000`
- confidence level: `99%`
- horizon: `1` trading day
- trading days per year: `252`
- annualized volatility: `10%` to `60%`
- position size: `5%` to `100%`
- stop-loss distance: `1%` to `10%`

No fabricated market data is used.

## Contents

- `portfolio_risk_surface.py`: validated, reusable model functions and
  sensitivity helpers.
- `../../notebooks/01_risk_surface.ipynb`: executable research notebook with
  derivation, 3D visualization, sensitivity analysis, interpretation, and
  limitations.

## Reproducing the analysis

From the repository root:

```bash
jupyter lab notebooks/01_risk_surface.ipynb
```

The notebook adds this directory to `sys.path` and imports the implementation,
so the formulas can be reused by future notebooks or tests.

## Limitations

This is a stylized risk surface rather than a production risk engine. It assumes
normal, independent returns; constant volatility; a single position; linear
exposure; immediate execution at the stop level; no gaps, slippage, fees,
financing, taxes, or liquidity effects; and a fixed confidence quantile. Real
returns can be fat-tailed, skewed, autocorrelated, and regime-dependent.
Accordingly, the output should be interpreted as a transparent scenario tool,
not as a forecast or a guarantee of maximum loss.
