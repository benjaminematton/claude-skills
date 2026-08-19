# Field brief template

Two variants. Use the **full brief** for a normal or deep run; use the **mini brief** when the ask was quick or narrow. Both must stand alone: a reader (or a fresh chat) with no other context should absorb the field from the brief alone. Honor the prose mandate — sections marked *(prose)* are paragraphs, not bullets.

## Full brief

```markdown
# Field brief: <Topic>

**Date:** <YYYY-MM-DD> · **Prepared for:** <the user's stated purpose> · **Depth:** <quick / normal / deep, N searches>

## State of the field *(prose)*

3–6 sentences: what the field is, where it stands today, and what has changed
recently. Write it the way a practitioner would orient a new colleague.

## Core concepts and vocabulary

- **<insider term>** — one-line working definition, noting where usage is contested
- (5–15 terms; this is one of the few sections where a list is correct)

## Live debates and open questions *(prose)*

One short paragraph per debate (2–3 debates). Name the specific people, labs,
papers, or institutions on each side — "some argue X" is summary language, not
expertise.

## Key claims log

| Claim | Status | Source(s) |
|---|---|---|
| <claim> | verified / single-source / contested / inference / prior-knowledge | <linked source(s)> |

Only claims that matter for the user's purpose. Status rules are in SKILL.md:
"verified" means two independently read sources from different origins, both
named — a vendor's own docs count once, however many pages; "inference" means
a conclusion you derived by combining or extrapolating sources (name what it
was derived from); "prior-knowledge" means training or user-supplied grounding
not confirmed by this session's sources.

## Practitioner heuristics *(prose)*

How people who do this well actually operate: rules of thumb, default tools,
what insiders roll their eyes at. This is the section that makes the brief feel
like expertise rather than an encyclopedia entry.

## Source shelf

- [Title](url) — one clause on why it's on the shelf (canonical / best survey / dissenting view / ...), marked **(read)** or **(search-level)**
- (ordered by usefulness, not discovery order; search-level sources are context, never corroboration)

## Coverage edges *(prose)*

2–4 sentences: what this brief does NOT cover and which sub-areas were
deliberately skipped or only single-sourced. This is what makes Phase 4's
"say when a question falls outside coverage" possible.
```

## Mini brief

Same standalone rule, compressed to fit a quick run. Target: fits on one screen.

```markdown
# Field brief (mini): <Topic>

**Date:** <YYYY-MM-DD> · **Scope:** <the narrow question this run answered> · <N> searches

<One paragraph: state of the field as it bears on the question, and the answer
or orientation the run produced.>

<One short paragraph: the main live debate or uncertainty, with named sides,
plus any claim that is single-source or contested.>

**Key terms:** <term> — <gloss>; <term> — <gloss> (3–6 max)

**Sources:** [Title](url) · [Title](url) · [Title](url)

**Not covered:** <one sentence on the edges — what a deeper run would add.>
```

## Rules for both variants

Fill every section from the running log or deep-research report — never from ungrounded memory; a section you can't source gets thinner, not padded. Keep the file self-contained (no references to "above conversation" or session-local paths). Name the file `field-brief-<topic-slug>.md`. When appending Phase 4 follow-up findings, add them to the relevant section and update the date line rather than tacking on a changelog.
