"""Landing gate (F4). Contract in docs/specs/2026-08-12-landing-gate-design.md.

Two things these tests are protecting and must not be "fixed" away:
  * W is advisory. A high search:fetch ratio must NEVER change the exit code -- FINDINGS
    records `single_source_flagged` as flawed for scoring honest budget triage as
    unfaithfulness, and a blocking W repeats it.
  * The gate never calls an LLM. test_gate_never_imports_judge is the structural guard;
    every other test runs with no key and no judge stub set.
"""

import json, os, subprocess, sys

from auditor.brief import parse_brief, resolve_citations
from auditor.checks import Finding, run_checks
from auditor.gate import MAX_ROUNDS, run_gate
from auditor.transcript import parse_transcript


# ---------------------------------------------------------------- helpers

def _fetch(i, url, text="evidence"):
    return [
        {"type": "assistant", "message": {"content": [
            {"type": "tool_use", "id": f"f{i}", "name": "WebFetch", "input": {"url": url}}]}},
        {"type": "user", "message": {"content": [
            {"type": "tool_result", "tool_use_id": f"f{i}", "content": text}]}},
    ]


def _search(i, q):
    return [
        {"type": "assistant", "message": {"content": [
            {"type": "tool_use", "id": f"s{i}", "name": "WebSearch", "input": {"query": q}}]}},
        {"type": "user", "message": {"content": [
            {"type": "tool_result", "tool_use_id": f"s{i}", "content": "results"}]}},
    ]


def _write(tmp_path, name, records):
    p = tmp_path / name
    p.write_text("\n".join(json.dumps(r) for r in records))
    return p


def _gate(tmp_path, draft, records, round_n=0, prev=None):
    t = _write(tmp_path, "t.jsonl", records)
    transcript = parse_transcript(str(t))
    brief = parse_brief(draft)
    resolve_citations(brief)
    prev_brief = None
    if prev is not None:
        prev_brief = parse_brief(prev)
        resolve_citations(prev_brief)
    checks = run_checks(brief, transcript)
    if brief.dropped_rows > 0:  # mirrors audit.py's D0 append
        checks.findings.append(Finding(
            "D0", "fail", f"{brief.dropped_rows} claims-log row(s)", "unrecognized status"))
    return run_gate(brief, transcript, checks, round_n=round_n, prev_brief=prev_brief)


def _gates(res):
    return {g for g, _s, _d in res.blocks}


LOG = """## Key claims log

| Claim | Status | Source(s) |
|---|---|---|
{rows}
"""


# ---------------------------------------------------------------- G1

def test_g1_blocks_verified_claim_citing_unfetched_url(tmp_path):
    draft = LOG.format(rows="| laundered | verified | [a](https://never.example.com/x) |")
    res = _gate(tmp_path, draft, _fetch(1, "https://read.example.com/p"))
    assert res.blocked and res.exit_code == 1
    assert "G1" in _gates(res)


def test_g1_ignores_unfetched_citation_on_a_non_verified_claim(tmp_path):
    """The contract constrains what may be CALLED verified, not what may be cited."""
    draft = LOG.format(rows="| honest | single-source | [a](https://never.example.com/x) |")
    res = _gate(tmp_path, draft, _fetch(1, "https://read.example.com/p"))
    assert not res.blocked and res.exit_code == 0


# ---------------------------------------------------------------- G2

def test_g2_blocks_a_lying_shelf_mark(tmp_path):
    draft = LOG.format(rows="| fine | single-source | [a](https://read.example.com/p) |") + """
## Source shelf

- [a](https://read.example.com/p) — real **(read)**
- [b](https://never.example.com/x) — claimed **(read)**
"""
    res = _gate(tmp_path, draft, _fetch(1, "https://read.example.com/p"))
    assert res.blocked and "G2" in _gates(res)


# ---------------------------------------------------------------- G3

def test_g3_blocks_verified_claim_whose_read_citations_share_one_origin(tmp_path):
    draft = LOG.format(rows=(
        "| vendor says so | verified | "
        "[x](https://gener8tor.com/gbeta), [y](https://gener8tor.com/gbeta/medtech) |"))
    res = _gate(tmp_path, draft,
                _fetch(1, "https://gener8tor.com/gbeta")
                + _fetch(2, "https://gener8tor.com/gbeta/medtech"))
    assert res.blocked and "G3" in _gates(res)


def test_g3_clears_once_the_claim_is_demoted(tmp_path):
    """Demotion is a legal remediation move -- the same evidence stops being a block."""
    draft = LOG.format(rows=(
        "| vendor says so | single-source | "
        "[x](https://gener8tor.com/gbeta), [y](https://gener8tor.com/gbeta/medtech) |"))
    res = _gate(tmp_path, draft,
                _fetch(1, "https://gener8tor.com/gbeta")
                + _fetch(2, "https://gener8tor.com/gbeta/medtech"))
    assert not res.blocked and res.exit_code == 0


def test_two_independent_origins_do_not_block(tmp_path):
    draft = LOG.format(rows=(
        "| real | verified | "
        "[a](https://read.example.com/p), [b](https://other.example.org/q) |"))
    res = _gate(tmp_path, draft,
                _fetch(1, "https://read.example.com/p")
                + _fetch(2, "https://other.example.org/q"))
    assert not res.blocked and res.exit_code == 0


# ---------------------------------------------------------------- G4

def test_g4_blocks_verified_resting_on_one_read_source(tmp_path):
    """The third F1 sub-form. Trips neither D1 (the source WAS fetched) nor D3
    (needs 2+ read URLs), so the deterministic stage missed it before the gate."""
    draft = LOG.format(rows="| ~$100k for 12 weeks | verified | [a](https://read.example.com/p) |")
    res = _gate(tmp_path, draft, _fetch(1, "https://read.example.com/p"))
    assert res.blocked and "G4" in _gates(res)
    assert "G1" not in _gates(res) and "G3" not in _gates(res)


def test_g4_blocks_verified_with_zero_citations(tmp_path):
    draft = LOG.format(rows="| bare assertion | verified | — |")
    res = _gate(tmp_path, draft, _fetch(1, "https://read.example.com/p"))
    assert res.blocked and "G4" in _gates(res)


def test_g4_silent_on_two_read_origins(tmp_path):
    draft = LOG.format(rows=(
        "| real | verified | "
        "[a](https://read.example.com/p), [b](https://other.example.org/q) |"))
    res = _gate(tmp_path, draft,
                _fetch(1, "https://read.example.com/p") + _fetch(2, "https://other.example.org/q"))
    assert "G4" not in _gates(res)


def test_g4_silent_on_non_verified_claims(tmp_path):
    draft = LOG.format(rows="| honest | single-source | [a](https://read.example.com/p) |")
    res = _gate(tmp_path, draft, _fetch(1, "https://read.example.com/p"))
    assert not res.blocked


def test_g4_counts_read_not_cited(tmp_path):
    """Two citations, one read -> both G1 (unread citation) and G4 (only one read)."""
    draft = LOG.format(rows=(
        "| padded | verified | "
        "[a](https://read.example.com/p), [b](https://never.example.com/x) |"))
    res = _gate(tmp_path, draft, _fetch(1, "https://read.example.com/p"))
    assert {"G1", "G4"} <= _gates(res)


# ---------------------------------------------------------------- G0

def test_g0_blocks_an_unrecognized_status(tmp_path):
    """Unauditable rows are findings, not omissions -- mirrors audit.py's D0."""
    draft = LOG.format(rows="| bogus | totally-made-up | — |")
    res = _gate(tmp_path, draft, _fetch(1, "https://read.example.com/p"))
    assert res.blocked and "G0" in _gates(res)


def test_invented_verified_by_absence_is_still_blocked(tmp_path):
    """Aug 3 invented `verified (by absence)`. parse_brief reads it as plain `verified`
    (the word matches), so G0 does NOT fire -- G4 catches it instead, on zero read
    sources. Documented here because the routing is non-obvious."""
    draft = LOG.format(rows="| no filings found | verified (by absence) | — |")
    res = _gate(tmp_path, draft, _fetch(1, "https://read.example.com/p"))
    assert res.blocked and "G4" in _gates(res) and "G0" not in _gates(res)


# ---------------------------------------------------------------- W (advisory)

def test_w_trips_on_high_ratio_but_never_blocks(tmp_path):
    records = []
    for i in range(20):
        records += _search(i, f"query {i}")
    records += _fetch(99, "https://read.example.com/p")
    draft = LOG.format(rows="| fine | single-source | [a](https://read.example.com/p) |")
    res = _gate(tmp_path, draft, records)
    assert res.stats["w_tripped"] is True
    assert res.directives
    assert not res.blocked and res.exit_code == 0


def test_w_silent_on_a_short_opening_burst(tmp_path):
    """3 searches / 0 fetches is a normal Phase 1 opening, not a violation."""
    records = _search(1, "a") + _search(2, "b") + _search(3, "c")
    res = _gate(tmp_path, LOG.format(rows="| none | single-source | — |"), records)
    assert res.stats["w_tripped"] is False


def test_w_fires_when_many_searches_produced_zero_fetches(tmp_path):
    records = []
    for i in range(14):
        records += _search(i, f"q{i}")
    res = _gate(tmp_path, LOG.format(rows="| none | single-source | — |"), records)
    assert res.stats["w_tripped"] is True
    assert not res.blocked


# ---------------------------------------------------------------- rounds

def test_round_budget_exhaustion_is_reported_and_still_blocks(tmp_path):
    draft = LOG.format(rows="| laundered | verified | [a](https://never.example.com/x) |")
    res = _gate(tmp_path, draft, _fetch(1, "https://read.example.com/p"),
                round_n=MAX_ROUNDS)
    assert res.blocked and res.exhausted
    md = __import__("auditor.gate", fromlist=["to_markdown"]).to_markdown(res)
    assert "do NOT search again" in md


def test_below_budget_offers_moves_not_exhaustion(tmp_path):
    draft = LOG.format(rows="| laundered | verified | [a](https://never.example.com/x) |")
    res = _gate(tmp_path, draft, _fetch(1, "https://read.example.com/p"), round_n=0)
    assert res.blocked and not res.exhausted


# ---------------------------------------------------------------- demotion reporting

def test_demotions_are_reported_never_blocked(tmp_path):
    """The hedging tell is a stat. Blocking it here would punish honest demotion; the
    counterweight is `verified_claim_as_established` in the rubric."""
    prev = LOG.format(rows="| c | verified | [a](https://read.example.com/p) |")
    now = LOG.format(rows="| c | single-source | [a](https://read.example.com/p) |")
    res = _gate(tmp_path, now, _fetch(1, "https://read.example.com/p"), prev=prev)
    assert not res.blocked
    demotions = res.stats["demotions"]
    assert len(demotions) == 1
    assert demotions[0]["from"] == "verified" and demotions[0]["to"] == "single-source"


def test_demotions_none_without_prev(tmp_path):
    draft = LOG.format(rows="| c | single-source | [a](https://read.example.com/p) |")
    res = _gate(tmp_path, draft, _fetch(1, "https://read.example.com/p"))
    assert res.stats["demotions"] is None


# ---------------------------------------------------------------- CLI + no-LLM contract

def _cli(tmp_path, draft, records, extra=()):
    b = tmp_path / "draft.md"; b.write_text(draft)
    t = _write(tmp_path, "t.jsonl", records)
    env = dict(os.environ, PYTHONPATH=os.getcwd())
    env.pop("ANTHROPIC_API_KEY", None)
    env.pop("VERIFIER_JUDGE", None)
    return subprocess.run(
        [sys.executable, "-m", "auditor.gate_cli",
         "--log", str(b), "--transcript", str(t), *extra],
        capture_output=True, text=True, env=env)


def test_cli_gate_exits_1_on_block_with_no_key_present(tmp_path):
    draft = LOG.format(rows="| laundered | verified | [a](https://never.example.com/x) |")
    p = _cli(tmp_path, draft, _fetch(1, "https://read.example.com/p"))
    assert p.returncode == 1, p.stderr
    assert "BLOCKED" in p.stdout


def test_cli_gate_exits_0_when_clear(tmp_path):
    draft = LOG.format(rows=(
        "| real | verified | "
        "[a](https://read.example.com/p), [b](https://other.example.org/q) |"))
    p = _cli(tmp_path, draft,
             _fetch(1, "https://read.example.com/p") + _fetch(2, "https://other.example.org/q"))
    assert p.returncode == 0, p.stderr


def test_cli_gate_json_shape(tmp_path):
    draft = LOG.format(rows="| laundered | verified | [a](https://never.example.com/x) |")
    p = _cli(tmp_path, draft, _fetch(1, "https://read.example.com/p"), extra=["--json"])
    data = json.loads(p.stdout)
    assert data["verdict"] == "blocked"
    assert "G1" in {b["gate"] for b in data["blocks"]}  # order-independent
    assert "search_fetch_ratio" in data["stats"]


def test_cli_gate_infra_exit_3_on_missing_transcript(tmp_path):
    b = tmp_path / "draft.md"; b.write_text(LOG.format(rows="| c | verified | — |"))
    env = dict(os.environ, PYTHONPATH=os.getcwd())
    p = subprocess.run(
        [sys.executable, "-m", "auditor.gate_cli", "--log", str(b),
         "--transcript", str(tmp_path / "nope.jsonl")],
        capture_output=True, text=True, env=env)
    assert p.returncode == 3


def test_gate_never_imports_judge(tmp_path):
    """Structural guard: the gate path must not load auditor.judge at all."""
    b = tmp_path / "draft.md"
    b.write_text(LOG.format(rows="| c | single-source | [a](https://read.example.com/p) |"))
    t = _write(tmp_path, "t.jsonl", _fetch(1, "https://read.example.com/p"))
    probe = (
        "import sys, runpy;"
        "sys.argv=['auditor.gate_cli','--log',%r,'--transcript',%r];"
        "\ntry:\n runpy.run_module('auditor.gate_cli', run_name='__main__')\n"
        "except SystemExit:\n pass\n"
        "print('JUDGE_LOADED' if 'auditor.judge' in sys.modules else 'JUDGE_ABSENT')"
    ) % (str(b), str(t))
    env = dict(os.environ, PYTHONPATH=os.getcwd())
    p = subprocess.run([sys.executable, "-c", probe], capture_output=True, text=True, env=env)
    assert "JUDGE_ABSENT" in p.stdout, p.stdout + p.stderr
