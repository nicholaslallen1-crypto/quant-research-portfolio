# Synthetic validation example

Run:

```text
python examples/synthetic_validation_demo.py
```

The script generates a deterministic synthetic price series, purges entries that would overlap a split boundary, selects a small candidate on TRAIN only, evaluates it on VALIDATION and TEST, and reports a simple cost-stress case.

The output is intentionally synthetic. It is included to demonstrate coding style and research discipline, not to disclose the private research engines or make a performance claim.

