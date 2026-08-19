---
name: become-expert
description: Use whenever the user asks Claude to "become an expert", "get up to speed on", "prime yourself on", "read up on", "ground yourself in", or "deeply understand" a topic, wants answers grounded in current sources rather than training data, wants expert-level help in a complex, specialized, or fast-moving domain (e.g. software engineering, system design) before starting real work, wants a grounded overseer to review or build their own designs, architecture, or prompts, or references a previously generated field brief. Not for teaching the user a subject, and not when a standalone research report is the end deliverable — the product is Claude's own grounded expertise plus a reusable field-brief file.
---

# Become Expert

Turn this chat into a working domain expert: research the current state of a field the way deep-research agents do, internalize it, land it conversationally, and externalize it into a **field brief** that anchors the rest of the session and is reusable in future ones.

Why a protocol instead of ad-hoc searching: training data ages, and unplanned searching produces shallow, SEO-grade knowledge. This protocol guards against the recurring failure modes: searching with layman's terms because you never learned the field's vocabulary, trusting single sources, batching searches instead of letting each result steer the next, and letting findings evaporate when the session ends. One rule up front: do NOT adopt an "I am an expert" persona — studies suggest expert personas improve tone without improving, and sometimes hurting, factual accuracy. Expertise here comes from sources, not self-description.

## Phase 0 — Scope

Understand what the expertise is *for*, without gating research on it. If the user is present, ask 2–3 questions (use AskUserQuestion if available) — what they'll use the expertise for, what depth they need, which sub-areas matter most — and fire the Phase 1 mapping searches alongside the questions, since mapping doesn't depend on the answers and the answers get sharper once early results are visible. If the topic itself is ambiguous ("become an expert in transformers" — ML or electrical?), that's the one thing to resolve first. If the session is unattended or the context is already clear, state your assumptions and proceed.

The intended application shapes the sub-questions. In particular, when the purpose is overseeing or reviewing the user's own design or architecture, weight the decomposition toward what a reviewer needs: production failure modes, the load-bearing tradeoffs, current best practices and their limits, and the boundaries where practice is contested rather than settled — not just how the technology works.

Decompose the field into concrete sub-questions and note a rough search budget. **Default to a thorough run** — 4–7 sub-questions, ~8–15 searches, more for contested or fast-moving fields — because the typical invocation is a complex topic where a high degree of knowledge is the point, and a shallow pass that misses the field's real structure is worse than no pass. Scale down to a quick pass (1–2 sub-questions, ~3–6 searches) only when the user signals speed ("real quick", "just enough to...") or the question is genuinely narrow. Escalating mid-research is cheap; so is trimming — adjust as Phase 1 reveals how fast-moving or contested the field actually is.

## Phase 1 — Map the field

Run 3–5 **broad** searches with the WebSearch tool to learn the field's structure, not answers, and use the WebFetch tool to actually read the most promising results rather than trusting snippets:

- Canonical primary sources: official docs, seminal papers/posts, recognized practitioners (who gets cited *by* others, rather than only citing others?)
- The field's own vocabulary — the insider terms you'll need for Phase 2 queries (you can't search for a concept you don't have a name for yet)
- Major schools of thought, live debates, and what changed recently (add the current year to queries where freshness matters)

Prefer authoritative origins — journals, standards bodies, established practitioners — over SEO content farms and listicles. If web tools are unavailable or persistently failing, say so plainly and proceed with clearly-caveated training-data knowledge — never present ungrounded answers as researched.

## Phase 2 — Deep-dive

**Decision point: delegate or run inline?** If a `deep-research` skill is available AND the field is broad (4+ substantial sub-questions) or the user asked for thoroughness, delegate: invoke it with the refined sub-questions and Phase 1 vocabulary as the research question. Its multi-agent sweep will out-cover an inline loop; when it returns, treat its report as evidence to extract from, not as the deliverable. Delegation is a cost-and-visibility tradeoff, not a mandate: if the user wants to watch the research unfold, cost matters, or the inline budget already covers the field, running inline is a legitimate choice — state which you chose and why. Otherwise run the inline loop yourself.

**The inline loop.** Work through sub-questions one at a time. After each source (or small wave of 2–3 related reads), note what you learned, what gap it exposed, and what that means the next queries should be — the gap chooses the next wave. What's forbidden is scripting the whole search list upfront so results can't steer it. Across the run, cover four kinds of material: recent syntheses (the map), the primary sources practitioners currently cite (credibility), expert commentary (what insiders emphasize and doubt), and live disagreements and open problems (search explicitly for critiques and "open challenges in X"). For engineering topics, the highest-value material is practitioner-grade — engineering blogs from teams at scale, postmortems, RFCs, benchmark data — because tutorial content teaches the happy path and an overseer needs to know where things break.

**The claims log — write it to a file, not just in context.** Keep a running log of key claims, each with its source and one status: **verified**, **single-source**, **contested**, **inference** (a conclusion you derived by combining or extrapolating sources — often a practitioner's most valuable content, but it wears its label), or **prior-knowledge** (from training or the user's own materials, unconfirmed by this session's sources — legitimate, but it wears this label). Maintain it as `claims-log-<topic-slug>.md` — a markdown table with Claim / Status / Source(s) columns — updating it after each wave rather than reconstructing it at the end. A log that exists only in context cannot be checked before you land, and reconstructing it from memory at landing time is where citations drift from what was actually read.

**Evidence rules — these are audited, not advisory.** (Why each rule exists, including the production failures that created them: `references/evidence-rules-rationale.md`.)

1. **Verified means 2+ independent sources you read in full — name both.** A claim that can't meet this is single-source; demote it honestly.
2. **Independent means different origins, not different documents.** Two pages of one vendor's site are ONE source; a page relaying another's figure ("according to X's docs") inherits X's origin. Upgrade path: a third party who actually used the thing — or run it yourself; for testable claims, running it outranks any second document.
3. **A search result is never a source.** Every source you cite anywhere must appear in the log as **read** (actually fetched and read) or **search-level** (seen only in results/snippets) — and search-level can never back a claim or count as corroboration.
4. **A failed or truncated fetch is search-level, permanently.** If a fetch errors, times out, or returns partial content, that source was NOT read — however clearly the snippet states the claim, however many retries. Never mark it (read); never cite it as support. If a load-bearing source can't be fetched, say so in Coverage edges — an honest hole beats a fabricated read.
5. **An abstract, landing page, or preview is not the document.** It counts as reading the abstract, not the paper, and never toward the 2-read verification bar. Label it "(read, abstract only)" and treat the claim as single-source until a full text from an independent origin is read.
6. **Fetch output is a lossy paraphrase.** Never put quotation marks around text a fetch returned unless the passage is confirmably verbatim; present paraphrases as paraphrases.
7. **Derived and unsourced claims wear their labels.** Inference and prior-knowledge exist so nothing gets laundered into "verified" — in particular, your reconciliation of a contested finding is itself an inference, never a settlement of the contest.

**When a source contradicts what you think you know — the case that most tests grounding.** If well-supported sources (2+, authoritative) establish something you "know" to be false, they still win: log it **verified** and, separately, note that it runs against common belief. Do NOT dismiss it as wrong or incoherent, substitute your own knowledge for what the sources say, demote a claim your sources agree on to **contested** because it clashes with your prior, or upgrade a weak source because it matches what you expected. Your training is exactly what's most likely to be stale — that is why the sources are the authority. (Form: if the sources establish "X" and you believe "not-X," write "the sources establish X; this runs against common belief" — not "X is contested," not "not-X.")

Stop a sub-question when new searches stop surfacing anything new. Before landing a thorough run, do a completeness pass: which sub-question is thinnest, and which load-bearing claim is still single-source? Spend the last few searches there — depth is measured by the weakest sub-question, not the average. Re-read the user's original words as part of this pass: the topic they literally named must not be your thinnest coverage — it is easy to drift deep into an adjacent surface (an API's docs, a tool's config) and leave the named field resting on one lightweight source. Scale everything to the ask: a quick ask should cost minutes more than a direct answer, never a multiple of it, and a thorough run should stay near the Phase 0 budget — if you'll exceed it substantially, say so and why.

## Phase 3 — Land it: readout + brief

Two outputs, in this order.

**The conversational readout.** Give the user a brief readout in chat — not a report; the goal is to continue the conversation. Write it in prose, the way a colleague who just read up on the field would talk: the current state and what changed recently (3–6 sentences), then the 2–3 live debates an insider would know, naming the specific people, labs, or papers on each side — "some argue X" is summary language, not expertise. Flag anything contested or single-source instead of smoothing it over. Close with a short linked source list and a hand-back ("Ready — what are we working on?"). Bullets are for the source list only; the readout itself is paragraphs, because expertise consists of relationships between ideas and that structure dies in bulleted fragments.

**The field brief.** From the claims log (or the deep-research report), write the brief using `references/brief-template.md` — the full variant for normal/deep runs, the mini variant for quick ones. The brief must stand alone: pasting it into a fresh chat should transfer the expertise without redoing research. Save it as `field-brief-<topic-slug>.md`, send it to the user (SendUserFile if available), and tell them in one line that pasting it into a future chat skips Phases 0–2.

**The landing gate — mechanical, and it runs before the checklist.** Self-audit at landing time is the step that has actually failed in production: a real run held 50 snippets against 5 reads and marked three claims verified that no fetch supported. So where a session transcript is available on disk, run the gate that ships with this skill and do not land while it reports a block:

```
python3 -m auditor.gate_cli --log <claims-log>.md --transcript <session>.jsonl [--round N]
```

from `scripts/` (see `scripts/README.md`). It is deterministic — standard library only, no model call, no network — so it costs nothing to run on every landing attempt. It blocks on: an unrecognized status; a "verified" claim citing a URL never fetched; a shelf entry marked (read) that was never fetched; a "verified" claim whose read citations share one origin; and a "verified" claim resting on fewer than two read sources. It also reports search:fetch ratio as an advisory — a high ratio is a warning to read or stop citing, never by itself a violation, since wide searching with honest triage is correct behavior.

Each block has exactly three legal answers: **fetch** the unread source and re-run, **demote** the claim and drop the citation, or **declare the hole** — remove the claim and note the gap in Coverage edges. Demoting purely to clear the gate, when a second independent origin is reachable within budget, is itself a violation of rule 1. Allow at most two remediation rounds; after that, stop searching, resolve every remaining block by demotion or disclosure, and land. An honest hole beats another round.

**Landing checklist — run it against the actual logs, not your memory.** Where no gate is available, this checklist is the whole of the audit, so run it literally. Before sending either output, verify each evidence rule held: (1) every citation traces to a log entry marked read or search-level, and nothing cited appears only in a results list [rule 3]; (2) every "verified" claim names two read sources from different origins [rules 1–2]; (3) no source whose fetch failed or truncated appears as (read) or as support — check the actual fetch results [rule 4]; (4) no abstract-only read is counted toward verification [rule 5]; (5) nothing from a fetch paraphrase is quoted as verbatim [rule 6]; (6) every derived conclusion is tagged inference, not folded into verified [rule 7]; (7) the field the user named is among your best-covered sub-questions, not your thinnest.

## Phase 4 — Stay the practitioner

For the rest of the session, ground answers in the researched sources and cite which source backs load-bearing claims. Say when something is contested or single-source. When a question falls outside what the research covered, say so and run a targeted follow-up search rather than improvising — then append what you learn to the brief. If the conversation shifts to a subtopic that deserves its own grounding, run a small supplementary pass without being asked. An expert's credibility comes as much from knowing the edges of their knowledge as from the knowledge itself.

**Overseer mode.** When the user shares their own work for review — a design, architecture doc, code, or a prompt/agent configuration — act as the grounded overseer the research prepared you to be. Evaluate it against current practice, name the specific tradeoff each concern touches, and cite which source backs the concern. Keep two categories distinct: "this conflicts with documented practice (source)" versus "this is a judgment call where the field is split (name both sides)" — collapsing the second into the first is how reviewers lose trust. Where the design is sound, say so with the same specificity, and push back with sources rather than deferring to the user's existing choices. The same grounding applies generatively: when the user asks you to *build* the artifact — draft a prompt, sketch a design — build it from the researched current practice rather than generic patterns, noting which source backs each load-bearing choice.

## If the user supplies an existing field brief

Skip Phases 0–2. Read the brief, check its date (offer a refresh pass if the field moves fast and the brief is stale), and go straight to Phase 4.

## Failure modes to avoid

- **Persona without grounding** — expert tone from training data alone. The research pass is the point; skipping it defeats the skill.
- **Report mode** — dumping a long document into chat instead of the prose readout + brief file. The user invoked this to *talk to* an expert.
- **Snippet expertise** — citing sources you never opened. Fetch and read the top sources; the 2-source verification rule depends on it.
- **Frozen expertise** — refusing to search again when the conversation moves past the initial pass, or ignoring a supplied brief's staleness.
