# CFTC COT data pipeline report

## Scope

This is a public-safe description of the Commitment of Traders data pipeline. It covers the design and data-quality controls, not a current positioning recommendation. Raw CFTC downloads, spreadsheet identifiers, credentials and private output workbooks are excluded.

## Data model

The pipeline synchronises annual Disaggregated Futures Only COT files from 2010 onward and maintains a separate Traders in Financial Futures Futures Only branch. Wide source files are reduced to compact, stable staging schemas before downstream history is built.

For the disaggregated branch, the canonical staging fields are market name, contract code, report date, open interest, manager long and manager short. The TFF branch keeps asset-manager and leveraged-fund positions separate so the two participant taxonomies cannot be mixed accidentally.

Configured contract histories are matched by CFTC contract code rather than display name. The summary layer can then calculate date coverage and positioning flips without relying on fragile column positions or renamed market labels.

## Reliability controls

- annual source discovery is year-aware and validates that the report family matches the requested branch;
- transient HTTP failures use bounded retries while permission and network errors remain visible;
- ZIP contents are inspected for the correct report payload before parsing;
- date parsing supports known CFTC formats and retains invalid, future and duplicate rows for audit;
- source lag, asset lag, missing report dates and long calendar gaps receive separate statuses;
- stable record keys allow added, corrected, removed and unchanged rows to be reconciled explicitly;
- dry-run mode calculates the exact diff without mutating the destination;
- an unchanged source produces no spreadsheet writes; and
- temporary downloads are isolated and cleaned up after the run.

## Why it matters

The useful output is not just a chart of long and short positions. It is a reproducible history with visible coverage, freshness and correction states, so a researcher can distinguish a genuine positioning change from a delayed source, a contract rename or a missing weekly observation.

## Public-safe boundary

This report intentionally omits the private workbook configuration, service-account material, source snapshots and full synchroniser implementation. It documents the engineering approach without publishing access details or proprietary integration code.

