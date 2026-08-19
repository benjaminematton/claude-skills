# Evidence rules — rationale and provenance

Why each rule in SKILL.md's Phase 2 exists, including the measured failures that created
them. Rules are numbered as in SKILL.md. This file is background: read it when questioning
or revising a rule, not during a normal run.

**Rule 1 (verified = 2 independent full reads).** Verification is a known weak link in
research agents; the failure mode is rarely lying — it's *rounding up*: a plausible claim
attributed to a source you didn't read gets promoted to "verified" under time pressure.
The 2-source rule is load-bearing, not polish.

**Rule 2 (independent = origins).** The most findable sources about a product are always
the vendor's own, so vendor-origin claims are the tag most prone to silent inflation —
two vendor pages feel like corroboration and aren't. Measured caveat: two controlled A/Bs
(sealed corpora, 2026-08-08) found this rule behaviorally *inert* at current model
capability — agents traced origins correctly even with the rule reverted. It stays because
it defines what "verified" means (removing it would change the output contract), not
because it changes behavior.

**Rule 3 (search-level never backs a claim).** A real production brief (2026-08-03) marked
claims "verified" citing sources that appeared only in search results and were never
fetched. The read/search-level bookkeeping makes that laundering mechanically auditable.

**Rule 4 (failed fetch = search-level).** Caught live by a transcript audit (2026-08-09):
a fetch of a load-bearing PDF failed on a size limit, and the brief cited it as verified
support AND shelf-marked it "(read)". The trigger is wanting a source badly: the snippet
states the claim, the fetch fails, and memory of the snippet gets promoted to a read.
Verified fixed in the next live run (an ECONNREFUSED source was handled honestly).

**Rule 5 (abstract is not the document).** Same audit series: an abstract-only read was
honestly labeled but still counted toward a verified claim that rested on the full text's
content. Honest labeling doesn't raise the evidence bar; only reading does.

**Rule 6 (fetch output is paraphrase).** WebFetch-style tools summarize pages with a
smaller model. Quoting that output as verbatim fabricates quotations.

**Rule 7 (labels don't launder).** Inference and prior-knowledge exist as statuses so that
derived or unsourced content has somewhere honest to live; without them, everything
gravitates to "verified". A reconciliation of contested sources is a conclusion you
derived — presenting it as settled misstates the field.

**The anti-prior paragraph** (kept verbatim in SKILL.md, not summarized here): validated
causally, twice — on a counter-factual corpus that inverts a strong prior, runs went 0/5
faithful without it and 5/5 with it (muscle-fiber-types A/B with byte-identical control
arm), and it generalized to a held-out domain (seasons A/B, 1/5 vs 5/5, Fisher p = 0.048).
Do not weaken or bury it.

**Provenance:** the failures and A/Bs above are documented in the `faithfulness-suite`
repo (FINDINGS.md and docs/2026-08-09-mining-report.md), which also contains the auditor
that checks rules 1–5 deterministically against real session transcripts.
