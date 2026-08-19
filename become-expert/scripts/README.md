# scripts/ — the landing gate

The deterministic checker the skill runs at the Phase 2 → Phase 3 boundary. It reads the
draft claims log and the session transcript and refuses to let the run land while a claim
is marked `verified` that the transcript cannot support.

This directory is the **source of truth** for the checker. `faithfulness-suite` vendors it
in (`tools/sync_gate_core.sh`) to grade with; the product owns its own runtime.

## Run

```bash
cd scripts
python3 -m auditor.gate_cli \
    --log ../claims-log-<topic-slug>.md \
    --transcript <session>.jsonl \
    [--round N] [--prev previous-claims-log.md] [--json]
```

Exit `0` clear, `1` blocked, `3` infra (never a verdict on infra). Python 3.9+, standard
library only — no dependencies, no network, no API key, no model call.

## What it blocks

| Gate | Fires on |
|---|---|
| G0 | a claims-log row with an unrecognized status |
| G1 | a `verified` claim citing a URL the transcript never fetched |
| G2 | a source shelf entry marked `(read)` that was never fetched |
| G3 | a `verified` claim whose read citations all share one origin, or whose cited page relays another source's figure |
| G4 | a `verified` claim resting on fewer than two *read* citations |
| W | search:fetch ratio > 4.0 over ≥12 searches — **advisory, never blocks** |

Each block has three legal answers: fetch the unread source and re-run, demote the claim
and drop the citation, or declare the hole in Coverage edges. Two remediation rounds, then
stop searching and resolve by demotion or disclosure.

**W never blocks by design.** A wide search with honest triage is correct behavior, and a
blocking ratio would punish it.

**The gate cannot detect hedging.** Every block is satisfiable by demoting everything to
`single-source`. `--prev` reports status changes as a stat so the tell is visible, but
demoting purely to clear the gate — when a second independent origin is reachable within
budget — is itself a violation of evidence rule 1.

## Transcript format

A Claude Code session `.jsonl`. A URL counts as fetched only if its `WebFetch` tool_result
returned without `is_error`; `WebSearch` results are recorded and are never evidence.

## Tests

```bash
python3 run_tests.py auditor/tests
```

`run_tests.py` is a stdlib-only runner for environments without PyPI — it reports anything
it cannot support as `SKIP-UNSUPPORTED` rather than passing it silently. Use pytest where
you have it. Current: **85 passed, 0 failed, 1 skipped-unsupported.**

The fixtures under `auditor/tests/fixtures/synthetic/` are reconstructions of two real runs
documented in faithfulness-suite's `docs/2026-08-09-mining-report.md` — the Aug-3 shape must
block, the Aug-8 shape must clear. The real transcripts are personal and live only in that
repo's local-only fixture directory.

## Layout

```
auditor/
  urlnorm.py      URL identity and origin keys
  transcript.py   session jsonl -> searches + successful fetches
  brief.py        claims log / brief -> claims, statuses, citations, shelf
  checks.py       D1/D2/D3 deterministic findings
  gate.py         G0-G4 + W, remediation rounds, demotion reporting
  gate_cli.py     entry point
run_tests.py      stdlib test runner
```

`judge.py`, `report.py` and `audit.py` are **not** here: they are the post-hoc,
LLM-judged auditor and belong to faithfulness-suite, which owns evaluation.
