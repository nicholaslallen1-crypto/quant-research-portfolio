# Public-safe examples

The examples in this directory are standalone and use generated data only.

## Edge-proof demo

```text
python examples/edge_proof_demo.py
```

This demonstrates a fixed candidate set, a horizon-aware temporal gap, train-only selection, validation and test scoring, and a higher-cost stress case. It reports JSON so the result can be consumed by another process without scraping prose.

## Synthetic validation demo

```text
python examples/synthetic_validation_demo.py
```

This demonstrates deterministic synthetic prices, purging around a split boundary, train-only selection, and out-of-sample evaluation.

Neither example represents private strategy logic, uses real market data, or makes a performance claim.

