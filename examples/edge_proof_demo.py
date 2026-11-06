"""Public-safe, synthetic edge-proof demonstration.

This module is an independent educational example. It demonstrates a small
validation workflow with generated observations, a purged temporal split,
train-only candidate selection, out-of-sample evaluation, and a cost-stress
case.

It deliberately contains no production connectors, private research names,
credentials, URLs, local paths, or real market data. The candidates and
thresholds are synthetic examples and are not investment advice.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
import math
import random
from typing import Iterable, Sequence


@dataclass(frozen=True)
class Observation:
    """One synthetic observation and the next-period return innovation."""

    index: int
    signal_a: float
    signal_b: float
    next_return: float


@dataclass(frozen=True)
class Candidate:
    """A pre-declared toy rule; selection never changes its definition."""

    name: str
    signal: str
    tail: str
    threshold: float
    direction: int
    horizon: int


@dataclass(frozen=True)
class Score:
    observations: int
    trades: int
    mean_return: float | None
    win_rate: float | None
    profit_factor: float | None
    cumulative_return: float | None
    max_drawdown: float | None


CANDIDATES: tuple[Candidate, ...] = (
    Candidate("signal_a_low", "signal_a", "low", -0.80, -1, 5),
    Candidate("signal_a_high", "signal_a", "high", 0.80, 1, 5),
    Candidate("signal_b_low", "signal_b", "low", -0.90, 1, 8),
    Candidate("signal_b_high", "signal_b", "high", 0.90, -1, 8),
)


def synthetic_panel(n: int = 720, seed: int = 19) -> list[Observation]:
    """Generate deterministic observations without importing market data."""
    if n < 80:
        raise ValueError("n must be at least 80 so every split has room")

    rng = random.Random(seed)
    latent_state = 0.0
    panel: list[Observation] = []

    for index in range(n):
        latent_state = 0.82 * latent_state + rng.gauss(0.0, 0.65)
        signal_a = latent_state + rng.gauss(0.0, 0.50)
        signal_b = -0.35 * latent_state + rng.gauss(0.0, 0.80)
        next_return = 0.0004 * latent_state + rng.gauss(0.0, 0.010)
        panel.append(Observation(index, signal_a, signal_b, next_return))

    return panel


def purged_splits(
    n: int,
    *,
    train_end: int,
    validation_end: int,
    max_horizon: int,
    embargo: int,
) -> dict[str, list[int]]:
    """Create temporal splits with a horizon-aware gap at each boundary."""
    if not 0 < train_end < validation_end < n:
        raise ValueError("split endpoints must satisfy 0 < train_end < validation_end < n")
    if max_horizon < 1 or embargo < 0:
        raise ValueError("max_horizon must be positive and embargo cannot be negative")

    train_stop = train_end - max_horizon - embargo
    validation_start = train_end + embargo
    validation_stop = validation_end - max_horizon
    test_start = validation_end + embargo

    splits = {
        "train": list(range(0, max(0, train_stop))),
        "validation": list(range(validation_start, max(validation_start, validation_stop))),
        "test": list(range(test_start, max(test_start, n - max_horizon))),
    }
    if not all(splits.values()):
        raise ValueError("split configuration leaves an empty evaluation split")
    return splits


def _signal_value(observation: Observation, signal: str) -> float:
    if signal == "signal_a":
        return observation.signal_a
    if signal == "signal_b":
        return observation.signal_b
    raise ValueError(f"unknown synthetic signal: {signal}")


def _is_active(observation: Observation, candidate: Candidate) -> bool:
    value = _signal_value(observation, candidate.signal)
    if candidate.tail == "low":
        return value <= candidate.threshold
    if candidate.tail == "high":
        return value >= candidate.threshold
    raise ValueError(f"unknown tail: {candidate.tail}")


def evaluate(
    panel: Sequence[Observation],
    indices: Iterable[int],
    candidate: Candidate,
    *,
    cost_bps: float,
) -> Score:
    """Evaluate a fixed candidate on the supplied indices only."""
    if cost_bps < 0.0:
        raise ValueError("cost_bps cannot be negative")

    index_list = list(indices)
    outcomes: list[float] = []
    for index in index_list:
        if index < 0 or index >= len(panel):
            raise IndexError(f"index {index} is outside the panel")
        if index + candidate.horizon > len(panel):
            continue

        if not _is_active(panel[index], candidate):
            continue

        forward_return = sum(
            panel[offset].next_return
            for offset in range(index, index + candidate.horizon)
        )
        net_return = candidate.direction * forward_return - cost_bps / 10_000.0
        outcomes.append(net_return)

    if not outcomes:
        return Score(len(index_list), 0, None, None, None, None, None)

    equity = 1.0
    peak = equity
    max_drawdown = 0.0
    for outcome in outcomes:
        equity *= 1.0 + outcome
        peak = max(peak, equity)
        max_drawdown = min(max_drawdown, equity / peak - 1.0)

    gains = sum(outcome for outcome in outcomes if outcome > 0.0)
    losses = -sum(outcome for outcome in outcomes if outcome < 0.0)

    return Score(
        observations=len(index_list),
        trades=len(outcomes),
        mean_return=sum(outcomes) / len(outcomes),
        win_rate=sum(outcome > 0.0 for outcome in outcomes) / len(outcomes),
        profit_factor=(gains / losses) if losses else None,
        cumulative_return=equity - 1.0,
        max_drawdown=max_drawdown,
    )


def select_on_train(
    panel: Sequence[Observation],
    train_indices: Sequence[int],
    *,
    candidates: Sequence[Candidate] = CANDIDATES,
    cost_bps: float = 4.0,
) -> Candidate:
    """Select a candidate using TRAIN only, with deterministic tie-breaking."""
    ranked: list[tuple[float, str, Candidate]] = []
    for candidate in candidates:
        score = evaluate(panel, train_indices, candidate, cost_bps=cost_bps)
        ranked.append((score.mean_return if score.mean_return is not None else -math.inf, candidate.name, candidate))

    return max(ranked, key=lambda row: (row[0], row[1]))[2]


def run_demo(*, n: int = 720, seed: int = 19) -> dict[str, object]:
    """Run the complete synthetic proof workflow and return JSON-safe output."""
    panel = synthetic_panel(n=n, seed=seed)
    max_horizon = max(candidate.horizon for candidate in CANDIDATES)
    splits = purged_splits(
        len(panel),
        train_end=360,
        validation_end=540,
        max_horizon=max_horizon,
        embargo=5,
    )
    selected = select_on_train(panel, splits["train"])

    def score(indices: Sequence[int], cost_bps: float = 4.0) -> dict[str, object]:
        return asdict(evaluate(panel, indices, selected, cost_bps=cost_bps))

    return {
        "experiment": "synthetic_edge_proof",
        "selected_on": "TRAIN",
        "candidate": asdict(selected),
        "split_sizes": {name: len(indices) for name, indices in splits.items()},
        "train": score(splits["train"]),
        "validation": score(splits["validation"]),
        "test": score(splits["test"]),
        "test_stress": score(splits["test"], cost_bps=12.0),
        "checks": {
            "synthetic_data_only": True,
            "selection_uses_test": False,
            "selection_uses_validation": False,
            "production_connectors": False,
        },
        "notes": [
            "All observations are generated locally with a fixed seed.",
            "The candidate set and thresholds are toy examples, not private rules.",
            "Results are not a performance claim or investment advice.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, default=720, help="number of synthetic observations")
    parser.add_argument("--seed", type=int, default=19, help="deterministic random seed")
    args = parser.parse_args()
    print(json.dumps(run_demo(n=args.n, seed=args.seed), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

