"""Analytical portfolio risk surface model.

The functions in this module intentionally use no market data. Inputs are
scenario assumptions expressed as decimal returns and portfolio fractions.
"""

from __future__ import annotations

from statistics import NormalDist

import numpy as np
import pandas as pd


def _validate_positive(name: str, value: float | np.ndarray) -> None:
    if np.any(np.asarray(value) <= 0):
        raise ValueError(f"{name} must be strictly positive.")


def _validate_fraction(name: str, value: float | np.ndarray) -> None:
    if np.any((np.asarray(value) < 0) | (np.asarray(value) > 1)):
        raise ValueError(f"{name} must be between 0 and 1.")


def loss_rate(
    annualized_volatility: float | np.ndarray,
    stop_loss_distance: float | np.ndarray,
    *,
    confidence: float = 0.99,
    horizon_days: int = 1,
    trading_days: int = 252,
) -> float | np.ndarray:
    """Return the stressed loss rate before applying position size.

    The result is ``stop_loss_distance + z(confidence) * sigma * sqrt(T)``.
    """
    _validate_positive("annualized_volatility", annualized_volatility)
    _validate_fraction("stop_loss_distance", stop_loss_distance)
    _validate_positive("horizon_days", horizon_days)
    _validate_positive("trading_days", trading_days)
    _validate_fraction("confidence", confidence)
    if confidence <= 0.5:
        raise ValueError("confidence must be greater than 0.5.")

    z_score = NormalDist().inv_cdf(confidence)
    shock = z_score * np.asarray(annualized_volatility) * np.sqrt(
        horizon_days / trading_days
    )
    result = np.asarray(stop_loss_distance) + shock
    return float(result) if result.ndim == 0 else result


def modeled_loss(
    annualized_volatility: float | np.ndarray,
    position_size: float | np.ndarray,
    stop_loss_distance: float | np.ndarray,
    *,
    portfolio_value: float = 100_000,
    confidence: float = 0.99,
    horizon_days: int = 1,
    trading_days: int = 252,
) -> float | np.ndarray:
    """Return modeled potential loss in portfolio currency units."""
    _validate_positive("portfolio_value", portfolio_value)
    _validate_fraction("position_size", position_size)
    result = (
        portfolio_value
        * np.asarray(position_size)
        * loss_rate(
            annualized_volatility,
            stop_loss_distance,
            confidence=confidence,
            horizon_days=horizon_days,
            trading_days=trading_days,
        )
    )
    return float(result) if result.ndim == 0 else result


def sensitivity_table(
    parameter: str,
    values: np.ndarray,
    *,
    annualized_volatility: float = 0.30,
    position_size: float = 0.25,
    stop_loss_distance: float = 0.05,
    **model_kwargs: float,
) -> pd.DataFrame:
    """Evaluate one model input over a one-dimensional scenario grid."""
    scenarios = {
        "annualized_volatility": annualized_volatility,
        "position_size": position_size,
        "stop_loss_distance": stop_loss_distance,
    }
    if parameter not in scenarios:
        raise ValueError(f"parameter must be one of {tuple(scenarios)}")
    scenarios[parameter] = np.asarray(values)
    losses = modeled_loss(**scenarios, **model_kwargs)
    return pd.DataFrame({parameter: values, "modeled_loss": losses})
