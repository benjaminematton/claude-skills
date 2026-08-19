"""Regression: the gate must block the Aug-3 failure shape and clear the Aug-8 shape.

These fixtures are SYNTHETIC reconstructions of the two runs in
docs/2026-08-09-mining-report.md — the real transcripts are personal and local-only
(auditor/fixtures/README.md). They reproduce the documented *shape*: the Aug-3 draft
carries all four deterministic sub-forms of F1 at an ~11:1 search:fetch ratio; the Aug-8
draft is compliant at ~1:1. Run tools/gate_retro.sh against the real fixtures to confirm
the same verdicts on real data — that is the load-bearing check, this is the committed one.
"""

import json, os, pathlib, subprocess, sys

FIX = pathlib.Path(__file__).resolve().parent / "fixtures" / "synthetic"
ROOT = pathlib.Path(__file__).resolve().parents[2]  # dir containing the auditor package


def _gate(stem, extra=()):
    env = dict(os.environ, PYTHONPATH=str(ROOT))
    env.pop("ANTHROPIC_API_KEY", None)
    p = subprocess.run(
        [sys.executable, "-m", "auditor.gate_cli", "--json",
         "--log", str(FIX / f"{stem}-draft.md"),
         "--transcript", str(FIX / f"{stem}-transcript.jsonl"), *extra],
        capture_output=True, text=True, env=env, cwd=str(ROOT))
    assert p.returncode in (0, 1), f"infra exit {p.returncode}: {p.stderr}"
    return p.returncode, json.loads(p.stdout)


def test_aug03_shape_is_blocked():
    code, data = _gate("aug03-shape")
    assert code == 1 and data["verdict"] == "blocked"


def test_aug03_shape_trips_every_documented_f1_subform():
    """Mining report F1 lists three sub-forms; the shelf lie is the fourth tell."""
    _code, data = _gate("aug03-shape")
    gates = {b["gate"] for b in data["blocks"]}
    assert "G1" in gates, "search-level corroboration (never-fetched citations)"
    assert "G3" in gates, "same-origin double-count (gener8tor x2)"
    assert "G4" in gates, "single-citation verified (~$100k/12-week)"
    assert "G2" in gates, "shelf marks (read) on a page never fetched"


def test_aug03_shape_trips_w_at_the_documented_ratio():
    _code, data = _gate("aug03-shape")
    assert data["stats"]["w_tripped"] is True
    assert data["stats"]["search_fetch_ratio"] > 10  # mining report recorded ~11:1


def test_aug08_shape_is_clear():
    code, data = _gate("aug08-shape")
    assert code == 0 and data["verdict"] == "clear"
    assert not data["blocks"]
    assert data["stats"]["w_tripped"] is False


def test_aug03_shape_reports_exhaustion_at_the_round_cap():
    _code, data = _gate("aug03-shape", extra=["--round", "2"])
    assert data["exhausted"] is True
