"""Standalone synthetic validation example for the public portfolio.

This file is intentionally self-contained. It uses generated prices only and is
not copied from the private research systems. The point is to show a clear
experiment boundary, horizon-aware purging and conservative reporting.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import math
import random
from typing import Iterable


@dataclass(frozen=True)
class Score:
    trades: int
    average_return: float | None
    win_rate: float | None
    profit_factor: float | None
    max_drawdown: float | None


def synthetic_prices(n: int = 720, seed: int = 7) -> list[float]:
    """Create a deterministic, non-financial series for demonstration only."""
    rng = random.Random(seed)
    price = 100.0
    values = [price]

    for i in range(1, n):
        cycle = 0.00025 * math.sin(i / 17.0)
        shock = rng.gauss(0.0, 0.008)
        price *= math.exp(cycle + shock)
        values.append(price)

    return values


def purge_indices(
    indices: Iterable[int],
    *,
    split_end: int,
    max_horizon: int,
    embargo: int,
) -> list[int]:
    """Remove entries whose forward horizon touches the next split."""
    last_allowed = split_end - max_horizon - embargo
    return [i for i in indices if i < last_allowed]


def evaluate(
    prices: list[float],
    indices: Iterable[int],
    *,
    horizon: int,
    threshold: float,
    cost_bps: float,
) -> Score:
    """Evaluate a toy directional rule with explicit costs."""
    outcomes: list[float] = []
    for i in indices:
        if i + horizon >= len(prices):
            continue

        move = prices[i] / prices[i - 1] - 1.0
        direction = 1.0 if move >= threshold else -1.0
        future_return = direction * (prices[i + horizon] / prices[i] - 1.0)
        net_return = future_return - (cost_bps / 10_000.0)
        outcomes.append(net_return)

    if not outcomes:
        return Score(0, None, None, None, None)

    equity = 1.0
    peak = equity
    drawdown = 0.0
    for outcome in outcomes:
        equity *= 1.0 + outcome
        peak = max(peak, equity)
        drawdown = min(drawdown, equity / peak - 1.0)

    gains = sum(value for value in outcomes if value > 0.0)
    losses = -sum(value for value in outcomes if value < 0.0)

    return Score(
        trades=len(outcomes),
        average_return=sum(outcomes) / len(outcomes),
        win_rate=sum(value > 0.0 for value in outcomes) / len(outcomes),
        profit_factor=(gains / losses) if losses else None,
        max_drawdown=drawdown,
    )


def choose_on_train(prices: list[float], train: list[int]) -> tuple[int, float]:
    """Select using TRAIN only; ties resolve deterministically."""
    candidates = [(5, 0.0000), (10, 0.0005), (15, 0.0010)]
    ranked: list[tuple[float, int, float]] = []

    for horizon, threshold in candidates:
        score = evaluate(
            prices,
            train,
            horizon=horizon,
            threshold=threshold,
            cost_bps=4.0,
        )
        ranked.append((score.average_return or float("-inf"), horizon, threshold))

    best = max(ranked, key=lambda row: (row[0], -row[1], -row[2]))
    return best[1], best[2]


def run_demo() -> dict[str, object]:
    prices = synthetic_prices()

    train_end = 360
    validation_end = 540
    max_horizon = 15
    embargo = 5

    train = purge_indices(
        range(1, train_end),
        split_end=train_end,
        max_horizon=max_horizon,
        embargo=embargo,
    )
    validation = list(range(train_end + embargo, validation_end))
    test = list(range(validation_end + embargo, len(prices) - max_horizon))

    horizon, threshold = choose_on_train(prices, train)
    selected = {"horizon": horizon, "threshold": threshold}

    return {
        "experiment": "synthetic_only",
        "selected_on": "TRAIN",
        "candidate": selected,
        "train": asdict(evaluate(prices, train, horizon=horizon, threshold=threshold, cost_bps=4.0)),
        "validation": asdict(evaluate(prices, validation, horizon=horizon, threshold=threshold, cost_bps=4.0)),
        "test": asdict(evaluate(prices, test, horizon=horizon, threshold=threshold, cost_bps=4.0)),
        "test_stress": asdict(evaluate(prices, test, horizon=horizon, threshold=threshold, cost_bps=12.0)),
        "notes": [
            "Generated prices only; not market data.",
            "The example is not a representation of private strategy logic.",
            "Synthetic output is not evidence of future profitability.",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run_demo(), indent=2, sort_keys=True))

