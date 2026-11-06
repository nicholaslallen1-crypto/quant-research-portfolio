# Nicholas Allen — Quant Research Portfolio

A public, sanitized showcase of quantitative research engineering.

The work behind this portfolio spans macro signal discovery, systematic trade-structure research, reproducible validation, data-quality controls and a local AI analyst workflow. The production repositories, raw research data, private results exports and deployment details remain private by design. This repository contains only public-safe documentation and small synthetic demonstrations written for this portfolio.

## What I build

### Macro edge discovery

A research workflow for exploring macro indicator signals across a multi-asset universe. The private system separates:

- signal discovery from independent validation;
- single-indicator effects from controlled pairwise confirmation;
- threshold variants from consolidated edge families;
- historical association from robustness evidence;
- research hypotheses from promotion decisions.

The workflow includes event-date alignment, temporal checks, random-date baselines, overlap-aware diagnostics, lineage metadata, versioned local caches and bounded worker stages. A surviving candidate is still treated as a research hypothesis until it clears the next validation layer.

See [the sanitized project note](projects/macro-edge-discovery/README.md).

### Trade research engine

A private multi-asset engine for researching entry signals, exits, costs and risk. Its design is deliberately validation-first:

- strict market-data readiness and provenance checks;
- explicit purging and embargoes around train, validation and test;
- parameter-plateau analysis rather than a single best grid point;
- gap-aware execution, costs, carry and short-borrow assumptions;
- walk-forward, temporal, regime, stress and Monte Carlo diagnostics;
- effective-sample-size and overlap diagnostics;
- a frozen pre-test structure so final test data cannot select a replacement;
- machine-readable outputs for downstream review.

The engineering audit recorded 61/61 tests passing and a 6.97x optimisation-runtime reduction on a controlled benchmark after refactoring. Those figures are implementation evidence, not a live-trading claim.

See [the sanitized engine note](projects/trade-research-engine/README.md).

### Local AI research stack

I built a local analyst workflow that consumes structured research outputs rather than screenshots or unbounded prose. It separates numerical computation from interpretation: deterministic checks produce the evidence, local model agents organise diagnostics and draft review summaries, and the final status remains bounded by explicit gates.

The public description intentionally omits private prompts, model configuration, data locations and deployment wiring.

See [the sanitized AI note](projects/local-ai-research-stack/README.md).

## Sanitized reports

- [Quantitative research report](reports/quantitative-research-report.md)
- [Qualitative research report](reports/qualitative-research-report.md)
- [CFTC COT data pipeline report](reports/cot-data-pipeline-report.md)

## Public-safe demonstrations

- [Synthetic validation demo](examples/synthetic_validation_demo.py) — generated prices, a train/validation/test boundary, horizon-aware purging and cost stress.
- [Edge-proof demo](examples/edge_proof_demo.py) — generated observations, pre-declared candidate rules, train-only selection, out-of-sample scoring and deterministic audit flags.
- [Edge-proof tests](tests/test_edge_proof_demo.py) — deterministic tests for split gaps, train-only selection and output contracts.

Run the edge-proof demo with `python examples/edge_proof_demo.py` and its tests with `python -m unittest discover -s tests -p "test_*.py"`.

These examples are standalone, use generated data only and are not copied from private systems. Their thresholds, candidates and outputs are educational examples rather than investment advice or performance claims.

## What is deliberately excluded

- production source code and proprietary research logic;
- raw market data, spreadsheets and cached artefacts;
- credentials, service-account files, API keys and private URLs;
- local machine paths and deployment configuration;
- unpublished research results that could be mistaken for an audited track record.

The purpose of this repository is to make the research thinking and engineering standards legible without publishing the underlying intellectual property.

## Contact

Nicholas Allen — [GitHub](https://github.com/nicholaslallen1-crypto)

