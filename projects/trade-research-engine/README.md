# Trade research engine

## Research question

Given a signal and a defined instrument, how should a researcher test exits, costs, holding horizons and risk without allowing the test set to choose the answer?

## Private-system design

The engine is split conceptually into four layers:

- **Data readiness:** coverage, duplicates, session consistency, OHLC integrity, provenance and explicit exclusions.
- **Numerical research:** trade-path construction, exit families, costs, carry, borrow, exposure and drawdown calculations.
- **Diagnostics:** nested walk-forward checks, parameter neighbourhoods, temporal and regime views, stress scenarios, dependence-aware effective sample size and Monte Carlo paths.
- **Orchestration:** frozen manifests, machine-readable output, audit metadata and a human-readable review surface.

The central invariant is simple: TRAIN can discover a structure, VALIDATION can rank a bounded shortlist, and FINAL TEST can confirm, review or veto the frozen structure. TEST cannot select a replacement or silently resize the position.

## Engineering evidence

A private implementation audit recorded:

- 61/61 tests passing in the final verification run;
- 6.97x lower optimisation runtime on a controlled benchmark after refactoring;
- explicit retention of ruin paths rather than dropping returns at or below -100%;
- separate sequential-trade and calendar-portfolio drawdown definitions;
- null outputs for unavailable or mathematically infinite values rather than invented precision.

These are software and research-process observations, not a claim of live investment performance.

## Public-safe takeaway

I care about the boundary between a backtest that runs and a research result that deserves attention. Data integrity, sample dependence, holdout discipline and explicit failure states are part of the model—not reporting afterthoughts.

The production code, data, configurations and result files are intentionally not published.

