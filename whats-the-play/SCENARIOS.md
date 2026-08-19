# Scenario library

Trigger patterns → canonical sequence. Coding work only.

**Provenance markers.** `[D]` = declared by a skill file (authoritative — the skill says so itself). `[J]` = judgment (engineering opinion; challenge it freely). Trust `[D]` over your instinct; treat `[J]` as a default worth overriding.

Notation: `/name` = user must type it (user-invoked; nothing can fire it for them). `name` = model-invoked (fires on description of the situation, and other skills can reach it).

---

## Index

| # | Scenario | Fires on |
|---|---|---|
| 1 | New system or subsystem | greenfield, doesn't exist yet |
| 2 | Feature in existing code | "add X to Y", "support Z" |
| 3 | LLM-agent / prompt feature | agent, chatbot, tool-calling |
| 4 | Bug or failure | broken, failing, wrong output |
| 5 | Refactor / architecture | "this is a mess", too coupled |
| 6 | Spike | "will this even work" |
| 7 | Trivial change | one-liner, config, rename |
| 8 | Third-party integration | named external API or SDK |
| 9 | Test coverage | "add tests", untested |
| 10 | Too big for one plan | multi-subsystem, weeks of work |
| 11 | UI-heavy / visual | screen, page, redesign |
| 12 | Delegating | assign, hand off, Linear |
| 13 | Schema migration / backfill | migration, backfill, prod data |
| 14 | Acting on review feedback | PR comments, reviewer disagrees |

---

## Invocation law — read before composing any sequence

**A user-invoked skill can never fire another user-invoked skill.** `[D]` Only the human can. So any sequence mixing them is a human-driven checklist, not an automated chain — and the router can only ever start step 1.

**Skills that only the human can invoke:** `/grill-with-docs`, `/grill-me`, `/to-spec`, `/implement`, `/improve-codebase-architecture`, `/to-questionnaire`, `/wait-what`, `/setup-matt-pocock-skills`.

**Skills that fire from context (and can be chained):** `brainstorming`, `grilling`, `domain-modeling`, `codebase-design`, `prototype`, `writing-plans`, `subagent-driven-development`, `executing-plans`, `test-driven-development`, `systematic-debugging`, `code-review`, `review-plan`, `verification-before-completion`, `finishing-a-development-branch`, `using-git-worktrees`, `wizard`, `resolving-merge-conflicts`, `prompt-engineer`, `become-expert`, `frontend-design`, `web-design-guidelines`, `receiving-code-review`, `linear-delegation`, `simplify`, `handoff`, `writing-skills`, `coordinating-with-peer-sessions`.

`handoff` moved to the chainable list on 2026-08-18: Claude Code exposes it as a model-invocable skill, so the router can produce a handoff doc itself rather than printing the command.

---

## 1. New system or subsystem from scratch

**Triggers:** "build a X", "new service/app/agent", "from scratch", greenfield, a capability that doesn't exist yet.

1. `/grill-with-docs` → design + `CONTEXT.md` terms + ADRs. `[D]` It is a thin wrapper: it runs `grilling` informed by `domain-modeling`. If the user can't type it, fire those two directly. `[D]` Grilling ends when "the frontier is empty" — every branch visited, nothing silently assumed.
2. `prototype` — **only** if a state model or UX shape is genuinely uncertain. `[D]` Output is committed to a throwaway branch with a pointer left on the implementation issue — *not* deleted, and *not* promoted to production.
3. `/to-spec` → spec. `[D]` Needed here because grill-with-docs does **not** write one. `[D]` It forbids interviewing ("just synthesize what you already know") and includes a gate: it checks the proposed test seams with you.
4. `writing-plans` → plan file, 2–5 min tasks with exact paths. `[D]` Requires a spec as input; its self-review step reads the spec side by side with the plan.
5. `review-plan` → adversarial pass. `[D]` Its declared pairing is *after* writing-plans, before execution. `[D]` It also accepts a spec, so running it earlier is legitimate — just don't skip it entirely on > 1 day of work `[J]`.
6. `using-git-worktrees` → isolated branch, clean baseline. `[D]` Belongs at **execution** time, not plan time. **`[D]` Neither executor actually invokes it — they only list it as required — so you must.**
7. `subagent-driven-development` with `test-driven-development` inside. `[D]` Runs continuously; it explicitly will *not* pause between tasks for check-ins.
8. `simplify` → applied cleanups. `[D]` Reads the **changed** code and applies fixes; quality only, no bug hunting. `[J]` The slot is forced: it needs the whole diff (a per-task pass can't see two subagents writing the same helper), and it applies changes, so review must follow it. Greenfield is its best case — no conventions to converge on, so N agents invent N versions of one thing.
9. `code-review` → two-axis review. `[D]` Hard-fails early on a bad ref or empty diff. `[D]` Standards axis always runs (Fowler baseline applies even with zero repo docs); Spec axis skips and says so if no spec is found.
10. `verification-before-completion` → evidence. `[D]` The command must be run *in the current message*; for agent-completed work the required evidence is a **VCS diff**, not the agent's own success report.
11. `finishing-a-development-branch`. `[D]` Hard gate: tests must pass before merge/PR — it stops otherwise.

## 2. New feature in an existing codebase

**Triggers:** "add X to Y", "support Z", a feature request against code that exists.

1. `brainstorming` *(fires automatically)* → design **and spec doc**, with a user approval gate on each.
2. `writing-plans`. **`[D]` Go here directly. brainstorming declares a whitelist of exactly one successor: "The ONLY skill you invoke after brainstorming is writing-plans." Do not insert `/to-spec` (brainstorming already wrote the spec), `codebase-design`, or `review-plan` between them.**
3. `review-plan` — only if > 1 day of work `[J]`.
4. `using-git-worktrees` → `subagent-driven-development` + `test-driven-development`.
5. `simplify` — same slot as scenario 1, gated (see the adaptation table). `[J]` Different catch: "reuse" here means what **already exists in the repo**. A subagent unaware of a helper three directories over writes a second one, and nothing else catches it — `TDD` only asks whether it passes, and the Standards axis asks whether it conforms to documented standards, not whether the function already existed.
6. `code-review` → `verification-before-completion` → `finishing-a-development-branch`.

Need seam design? `[D]` `codebase-design` is a *reference to consult*, not a session to run — read it while designing, don't schedule it as a step.

## 3. LLM-agent / prompt-driven feature

**Triggers:** an agent, chatbot, assistant, natural-language interface, tool-calling, "it should decide".

Scenario 1 or 2 as the spine, plus the following — which are the actual product, not the CRUD underneath `[J]`:

- **Force these at design time:** what happens on **ambiguous reference**; what the **confirmation gate** is for destructive actions; what it does when it **can't tell** which entity you meant.
- **Seam:** the agent talks to a narrow tool interface, never the data layer. `[D]` This clears the bar for a real seam — production + test are two adapters ("one adapter means a hypothetical seam, two means a real one"). Without it, agent behavior can't be tested.
- **Split the implementation:** deterministic layer (tool functions, validation, gates — pure TDD, no LLM in tests) vs agent layer (system prompt, tool schemas, disambiguation).
- **`prompt-engineer` owns the agent layer** and must produce an **eval set**, not just a prompt. `[D]` Its own checkpoint: below 80% accuracy on the test set, find failure patterns before iterating. Tool *descriptions* decide whether it calls `edit` or `delete`.
- `[D]` `prompt-engineer` declares no handoff into the dev pipeline — you re-enter the spine manually.
- **Verification** must include a real transcript of the hard case, not a green suite `[J]`.

## 4. Bug, failure, or unexpected behavior

**Triggers:** "broken", "failing", "throwing", "wrong output", "slow", "why is it doing X".

1. `systematic-debugging` *(fires automatically)*. `[D]` Hard gate: "no fixes without root cause investigation first."
2. `test-driven-development` → the failing test that reproduces it. `[D]` systematic-debugging hands off here by name.
3. Fix.
4. `verification-before-completion`. `[D]` For a regression test, the required evidence is the full red-green cycle: write → pass → revert fix → **must fail** → restore → pass.

No spec, no plan file. The repro test is the spec `[J]`.

**`[D]` Escape hatch: after 3 failed fixes, stop and question the architecture with your human partner.** Don't attempt a fourth.

**`[D]` Multiple *unrelated* failures** (different subsystems, different root causes) → `dispatching-parallel-agents`. **Never for plan tasks** — `subagent-driven-development` bans parallel implementation subagents outright.

## 5. Refactor / architecture improvement

**Triggers:** "clean up", "this is a mess", "hard to change", "too coupled".

- **Don't know what to fix:** `/improve-codebase-architecture` → HTML report (`[D]` written to the OS temp dir, never the repo) → pick exactly one candidate → `[D]` it then runs a grilling loop on your pick. `[D]` It is a **survey, not a rescue** — on genuinely old code it finds real candidates but won't untangle the mud. `[D]` It weights recently-changed files, so scope it or let git history scope it.
- **Know exactly what to fix:** consult `codebase-design` → `writing-plans` → `subagent-driven-development` → `code-review`.

`[J]` Precondition either way: tests green and meaningful first. Refactoring without a safety net is rewriting. (No skill declares this — it's my rule.)

`[D]` Note the division of labor: TDD deliberately excludes refactoring from its loop and defers it to the review stage.

## 6. Spike / prototype / "will this even work"

**Triggers:** "try", "spike", "proof of concept", "see if it's possible".

1. `prototype` → the artifact that answers the one question. `[D]` No persistence, no tests, no error handling, no abstractions, no new top-level structure, no framework/bundler/server.
2. `[D]` Commit it to a throwaway branch off main and leave a pointer on the implementation issue. Throwaway means *not promoted*, not *deleted*.
3. Stop. Decide. Re-enter at scenario 1 or 2 with what you learned.

`[D]` TDD's exceptions list includes throwaway prototypes — but you must ask your human partner before skipping tests, not assume it.

## 7. Trivial change

**Triggers:** one-liner, config value, rename, copy tweak, dependency bump.

**No pipeline.** Make the change, run the tests, commit. Say so plainly and stop.

`[D]` One caveat: `brainstorming`'s hard gate claims *every* project needs a presented design, however short. If the work touches behavior at all, a two-sentence design still beats none.

## 8. Third-party integration

**Triggers:** "integrate with", "connect to", a named external API/SDK/service.

1. `become-expert` — if unfamiliar. `[D]` It verifies against real sources rather than training data, and hands off to nothing; you re-enter the spine yourself.
2. `brainstorming` → design including failure modes: rate limits, auth expiry, partial failures, retries `[J]`.
3. `wizard` → for human-only steps: credentials, dashboards, webhook config, CI secrets. `[D]` Do **not** use it for anything the agent could do itself, and do not run the generated script end-to-end yourself — it blocks on human input.
4. Adapter seam: `[D]` justified here, since production + test = two adapters.
5. `writing-plans` → `subagent-driven-development`, with recorded/replayed responses so tests don't hit the network `[J]`.
6. `code-review` → `verification-before-completion` (one real live call as evidence).

## 9. Test coverage work

**Triggers:** "add tests", "no coverage", "untested".

1. `[J]` If the code is hard to test, that's a design problem wearing a testing costume — consult `codebase-design` and fix the seam first. `[D]` Related rule from TDD: "no test is written at an unconfirmed seam."
2. `test-driven-development` for anything you change while there.
3. `simplify` — its cheapest instance `[J]`. Test files normalize copy-paste (setup, fixtures, near-identical arrange blocks), `[D]` TDD excludes refactoring from its loop and that covers test code too, and extracting a fixture can't change production behavior — the tests are their own safety net. The broadens-the-diff objection doesn't apply here.
4. `code-review`, Standards axis.

## 10. Too big for one plan

**Triggers:** multiple independent subsystems, "platform", "rebuild", weeks of work.

1. **Decompose first.** `[D]` `brainstorming` does this explicitly — it flags multi-subsystem scope and breaks it into sub-project specs before refining details.
2. Each piece runs scenario 1 or 2 independently — its own spec, plan, and branch. `[D]` writing-plans assumes this decomposition already happened.
3. **Executor choice — the one genuinely contested call:**
   - `[D]` `subagent-driven-development` for same-session work with mostly-independent tasks. It runs continuously and *will not* check in between tasks.
   - `[D]` `executing-plans` for separate-session work with review checkpoints — **but note it self-defers**: "if subagents are available, use subagent-driven-development instead."
   - `[J]` Resolution: default to `sdd`; choose `executing-plans` only when you actively want checkpoints between tasks, because that behavior is what `sdd` refuses to do.
   - `[D]` Tightly-coupled tasks route to neither — sdd sends them to manual execution or back to brainstorming.
4. `[D]` Between sessions, `/compact` is the default. Reach for `/handoff` only in its four declared cases: new harness, new directory, handing to a colleague, or forking mid-phase.

`[J]` `simplify` runs **per piece**, never as one cross-piece pass at the end — pieces merge through separate review gates, so a spanning pass rewrites already-reviewed code. Cross-piece duplication is a survey problem: scenario 5.

## 11. UI-heavy / visual work

**Triggers:** "new screen", "page", "component", "redesign", "make it look good" — anything whose deliverable is something a person looks at.

Scenario 2's spine answers *behavior*. Nothing in it asks what the thing should look like, so the aesthetic gets decided by default at implementation time `[J]`.

**The fork decides who owns the visuals `[J]`:** greenfield or deliberate redesign → `frontend-design` (`[D]` it mandates a BOLD direction and "NEVER converge on common choices across generations"). New screen in an existing product → `frontend-patterns` / `rn-patterns` win; that novelty mandate is written for standalone artifacts and produces incoherence inside a live design system. Borrow only its purpose/tone/differentiation questions.

1. `brainstorming` → design + spec **with the aesthetic direction written down** `[J]` — `[D]` `sdd` never checks in, so an unrecorded direction means each subagent picks its own.
2. `writing-plans` → worktree → `sdd` + `TDD`. `[D]` `frontend-design` implements working code itself and hands off to nothing: it *is* the visual layer's implementation, not a design-doc phase.
3. Consult while building, never schedule: `frontend-patterns` / `rn-patterns`, and `vercel-react-best-practices` (`[D]` 70 rules, framed "reference these guidelines when"). `[J]` Its `server-` category is Next.js-only; `Frontend/` is Vite.
4. `web-design-guidelines` alongside `code-review`. `[D]` Re-fetches the Vercel guidelines over the network each run, reviews only files you name, emits `file:line`. It reports, it does not fix.
5. `verification-before-completion` → `run` + a screenshot `[J]`. A green suite is not evidence a screen looks right.

**Watch for:** dark mode and accessibility — invisible to tests, caught only by step 4.

## 12. Delegating instead of building

**Triggers:** "assign", "hand off", "make a ticket", "put this in Linear" — work you're scoping for someone else to build.

Every other scenario terminates in *you* implementing. This is the exit ramp, and its defining property is where it **stops**.

1. Design as scenario 1 or 2.
2. `/to-spec` → spec. Required: `[D]` for multi-phase work `linear-delegation` attaches it to the Linear Project as a document.
3. `review-plan` against the spec `[J]` — `[D]` acceptance criteria are the contract and "should not change mid-flight," so this is the last cheap moment to challenge them.
4. `linear-delegation`. `[D]` First decision is altitude: **single Story** (one person, one cycle) vs **Project** (phases, or more than ~3 outcomes). `[D]` Every milestone Story gets outcome + acceptance criteria; only the first is assigned and cycled. `[D]` Always set the Project field, never encode it in the title; built-in labels only.
5. **Stop. Do not run `writing-plans`.** `[D]` "You assign outcomes; the engineer owns the breakdown" — pre-decomposing is the exact anti-pattern the skill blocks, *including* when the ask is phrased "break this into tasks." `[D]` Add a line asking the assignee to draft their own sub-issues and review them with you.

**Real unknowns?** `[D]` Delegate a **spike** first — `Feature` + `spike`, acceptance criteria written as the questions it must answer and the metrics it must report, out-of-scope explicit — rather than running `prototype` yourself.

**Skipping:** worktree, `sdd`, `TDD`, `code-review`, verification, finishing. All of it belongs to whoever takes the ticket.

**Watch for:** `[D]` the skill targets a Linear team via Linear MCP (`mcp__claude_ai_Linear__*`). Confirm those tools are connected — they're absent in some sessions — and that the team is right.

## 13. Schema migration or data backfill

**Triggers:** EF migration, "backfill", "add a column", "change the shape of", any edit to production data.

Scenarios 2 and 5 assume the blast radius is code. Here it's **data**, which has no `git revert` `[J]`. Two consequences:

1. **The evidence changes.** `[D]` `verification-before-completion` names a VCS diff as the required evidence. A diff cannot show that 40k rows migrated correctly. Decide the real evidence up front: before/after counts plus spot-checked rows from a dry run on a restored prod copy.
2. **The plan's shape changes.** **expand → backfill → contract**, three separately shippable steps `[J]` — both shapes readable at once, nothing dropped until traffic is off the old one. `[D]` `writing-plans` won't infer this; hand it the decomposition.

Sequence: `brainstorming` → spec with per-step rollback **and what happens to rows written *during* the backfill** `[J]` → `writing-plans` → `review-plan` (already required for irreversible ops) → worktree → `sdd` + `TDD` → `code-review` → dry run → real run.

**Repo landmines** `[D]`:

- Two migration folders in `Infrastructure`; the `ModelSnapshot` lives in the old one. **Always pass `--output-dir`.**
- Audit snapshot drift before adding a migration if schema work has happened since.
- Localities carry different UUIDs local vs prod — remap by canonical name, never literal id.

**Watch for:** reversible in EF, irreversible in reality. A generated `Down()` recreates a dropped column, not its contents.

## 14. Acting on review feedback

**Triggers:** PR comments, a reviewer disagreeing, "they said X", or `code-review` output you now have to do something about.

Every scenario ends at `code-review` as though its output were terminal. It's an input `[J]`.

1. `receiving-code-review` *(fires automatically)*. `[D]` READ → UNDERSTAND → VERIFY → EVALUATE → RESPOND → IMPLEMENT; the core rule is **verify before implementing**. `[D]` Opening with agreement or thanks is a declared violation.
2. `[D]` **Hard gate: if *any* item is unclear, implement nothing and ask.** Items may be related, and partial understanding produces the wrong implementation. That gate is why this is a scenario and not "address the comments."
3. `[D]` Source decides handling. Human partner → trusted, implement once understood. External reviewer → five checks first (correct for *this* codebase, breaks existing behavior, reason for the current implementation, platform/version, full context) and push back with reasoning if it fails one.
4. `[D]` YAGNI check on "implement this properly": grep for usage; nothing calls it → propose deleting it.
5. `[D]` Order: blocking (breaks, security) → simple (typos, imports) → complex (logic, refactor). Test each individually, not in a batch.
6. Behavioral → `TDD` `[J]`. `[D]` No handoff declared, so re-enter the spine yourself: `verification-before-completion` → `finishing-a-development-branch`.

`[D]` Conflicts with a prior architectural decision of yours → stop and discuss, don't implement. `[D]` GitHub inline replies go in the comment thread (`gh api repos/{owner}/{repo}/pulls/{pr}/comments/{id}/replies`), not top-level.

---

# Adaptation rules

Apply to any matched scenario; state which ones fired.

| Condition | Adaptation | |
|---|---|---|
| Domain unfamiliar or fast-moving | Prepend `become-expert`; it hands off to nothing, so re-enter the spine manually | `[D]` |
| LLM, prompt, or agent behavior involved | Add `prompt-engineer` + eval set; apply scenario 3's constraints | `[J]` |
| Destructive/irreversible ops (delete, money, prod, sending) | Design the confirmation gate at spec time; add `review-plan`; `code-review` must inspect the destructive path | `[J]` |
| Introducing a new module boundary | Only if **two adapters** are justified — a single-adapter seam is just indirection | `[D]` |
| More than one day of work | Add `review-plan`; commit the plan file | `[J]` |
| Diff spans several files, or subagents wrote it | Add `simplify` after implementation, before `code-review` — it *applies* fixes, so review must see final code | `[J]` |
| Surgical work (bugfix, hotfix, one-liner, prototype) | **Skip `simplify`** — its reuse and altitude axes broaden a diff by design, and `prototype` forbids the abstractions it adds | `[J]` |
| You want oversight between tasks | Use `executing-plans` — `sdd` explicitly refuses to pause | `[D]` |
| First time in this repo | `/setup-matt-pocock-skills` first | `[D]` |
| Setup was never run | Only `to-spec`, `to-tickets`, `triage` hard-depend on it; everything else degrades silently — do **not** flag its absence | `[D]` |
| Human-only setup needed (dashboards, keys, CI secrets) | Add `wizard` at the point of need | `[D]` |
| Design already settled (spec exists, prior session decided) | Say so explicitly so `brainstorming` doesn't re-fire and re-interview | `[J]` |
| Runs unattended (cron, daemon, scheduled) | `code-review` before it ships; verification needs runtime evidence, not tests | `[J]` |
| No `CONTEXT.md` and this is ongoing work | Prefer `/grill-with-docs` over `brainstorming` — builds the glossary as a side effect | `[J]` |
| Refactor with red or absent tests | Stop. Get green first | `[J]` |
| Multiple unrelated failures | `dispatching-parallel-agents` — never for plan tasks | `[D]` |
| Work is on main/master | Both executors require explicit user consent before implementing there | `[D]` |
