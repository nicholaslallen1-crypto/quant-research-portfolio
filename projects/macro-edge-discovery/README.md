# Macro edge discovery

## Research question

Can a macro indicator, or a controlled combination of indicators, identify a repeatable conditional change in a chosen asset or basket without relying on a single lucky threshold?

## Private-system design

The private workflow is organised into separate stages:

1. **Canonicalise inputs** — align observations to explicit signal dates and record the source lineage.
2. **Discover candidates** — search indicator tails and threshold families within bounded, reproducible search spaces.
3. **Measure evidence** — calculate conditional outcomes, sample depth, overlap and event-cluster diagnostics.
4. **Challenge the result** — compare against random-date baselines, temporal splits and controlled pairwise tests.
5. **Consolidate families** — avoid presenting adjacent threshold variants as independent discoveries.
6. **Promote conservatively** — apply severity, non-overlap, parent-quality and independent-validation gates.
7. **Persist reproducibly** — store versioned cache metadata and hashes so a rerun can distinguish a valid reuse from stale or mismatched evidence.

## What matters to a hedge fund

The interesting part is not finding the largest historical number. It is controlling the ways a research process can fool itself:

- overlapping events can inflate apparent sample size;
- adjacent thresholds can create false multiplicity;
- macro observations must be aligned to the information available at the time;
- a pairwise result should earn its improvement over its parent signals;
- a random baseline is evidence, not a promotion verdict;
- incomplete lineage or stale cache state should fail closed.

The public repository does not include the indicator names, thresholds, raw dates, research exports or production search code.

## Public-safe takeaway

I approach macro research as a staged evidence problem: discover broadly, validate independently, preserve lineage, and make the promotion decision stricter than the discovery decision.

