# Local AI research stack

## Purpose

The local AI layer is a research interface, not a replacement for the numerical engine. Its job is to help review a large structured output, surface inconsistencies and organise a clear analyst handoff while keeping the evidence traceable.

## Safe architecture summary

1. A deterministic research run produces structured metrics, warnings, assumptions and status fields.
2. A local model runtime receives only the approved research artefacts.
3. Role-separated analyst stages review different parts of the evidence, such as data readiness, performance, robustness and failure conditions.
4. A synthesis stage drafts a concise research note with references back to the structured fields.
5. Explicit gates remain authoritative. The language model cannot turn a failed data check into a pass or invent a missing metric.

## Why local

A local deployment is useful for private research because it keeps working notes and intermediate prompts on the researcher’s machine, reduces dependence on external inference APIs and makes the interface available beside the research tools. It also makes limitations visible: local models can be helpful at organising evidence, but they still need constrained inputs, structured outputs and deterministic checks.

## Public-safe takeaway

The valuable engineering problem is the boundary: numerical code creates evidence; the local AI layer explains and routes it; policy gates decide what can be called ready.

Private prompts, model settings, data locations, credentials and deployment wiring are deliberately omitted.

