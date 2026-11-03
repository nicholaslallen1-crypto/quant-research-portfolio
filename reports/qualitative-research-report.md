# Qualitative research report

## Scope

This is a public-safe summary of an official-source qualitative equity research and governance pipeline. The underlying collector, downloaded documents, cached filing paths and issuer-level working files are not included.

## Point-in-time and provenance controls

The pipeline builds a source-linked store of people, roles, career records, board memberships, education, insider links, operating outcomes, guidance, strategic commitments and capital-allocation events.

Each record keeps its source identity, filing metadata, period boundaries and revision history. Restatements are retained instead of averaged away. Derived operating facts retain their source IDs and formulas. Annual, quarterly and year-to-date periods remain separate, and tenure boundaries prevent facts from being attributed outside the relevant role period.

## Evidence discipline

The system separates:

- current and historical roles;
- company-level statements from person-attributed claims;
- guidance revisions from later actuals;
- acquisition announcements from completion;
- buyback authorisations from execution; and
- source coverage gaps from negative conclusions.

It rejects unsupported causal attribution and does not infer an executive’s prior employer when the official evidence does not provide defensible dates. Unknown, blocked and unresolved states remain visible in the output.

## Reproducibility

The audit suite covers identity resolution, period safety, restatements, derived metrics, guidance diagnostics, role changes, event reconciliation, source provenance and rerun idempotency. Cached reruns are checked for unintended additions, updates or duplicate stable IDs, while network reuse is separated from new acquisition.

## Collection engineering

Official corporate and investor-relations discovery is kept separate from transport accessibility. The collector records whether a page is official, accessible, content-validated, blocked or incomplete. Archive limits, missing webcasts and unavailable documents are reported as limitations rather than silently converted into successful coverage.

## Limitations

Official-source coverage is not the same as complete market coverage. Some guidance, historical employer mappings and webcast media may remain unavailable or unresolved; the pipeline records those states explicitly rather than filling them with guesses.

