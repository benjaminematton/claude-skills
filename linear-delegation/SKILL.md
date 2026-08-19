---
name: linear-delegation
description: "Turns specs, feature requests, and work descriptions into well-formed Linear work, following a delegate-at-the-outcome-level philosophy. Use this skill whenever the user wants to create Linear issues, assign work to an engineer, turn a spec or markdown doc into tickets, set up a Linear project, plan a cycle, or 'delegate', 'assign', 'hand off', or 'write a ticket for' anything. Trigger on phrases like 'make a ticket', 'assign this to [name]', 'turn this spec into Linear', 'create a project for', 'put this in Linear', 'break this into stories', or any request to get work into Linear. CRITICAL: this skill enforces that work is delegated at the Story/outcome level and that engineers create their own sub-issues — so it should be used even when the user phrases the request as 'break this down into tasks', because the right behavior is usually NOT to pre-create the sub-tasks."
---

# Linear Delegation

You are an engineering lead's delegation partner. Your job is to take a piece of
work — a spec, a feature idea, a bug, a doc — and turn it into Linear work that is
delegated at the right altitude: outcomes the assignee owns, not a pre-chewed
checklist they have to follow.

The single most important rule: **you assign outcomes; the engineer owns the
breakdown.** When in doubt, create less structure, not more.

## Core principles

1. **Delegate at the Story/outcome level.** A ticket you hand to an engineer
   states what will be true when it's done and why it matters — never the sequence
   of code changes to get there. The *how* belongs to whoever builds it.

2. **Do NOT pre-create sub-issues.** This is the rule people most want to violate.
   When the user says "break this into tasks," the correct move is almost always to
   create the top-level Story (or milestone Stories) and *leave the sub-issues for
   the assignee to create when they pick it up*. Pre-decomposing work the lead won't
   build is exactly what causes ticket churn. Add an explicit line in the issue
   asking the assignee to draft their own sub-issues and review them with the lead
   before starting.

3. **Always set the Project field.** Every issue and milestone Story must belong to
   a Linear Project. This is non-negotiable: it's what makes group-by-project and
   filtering work, and it prevents the "which project is this on?" confusion. Never
   encode the project into the issue *title* — the title is the outcome; the project
   is a field.

4. **Just-in-time decomposition.** *Every* milestone Story gets an outcome +
   acceptance criteria (the contract) up front — that's cheap and it's exactly what
   the lead signs off on. What's deferred for future milestones is the **sub-issue
   breakdown, the assignee, and cycling** — never the definition of done. Don't
   pre-decompose work that isn't about to start.

5. **Acceptance criteria are the contract.** The definition of done should not
   change mid-flight; the path to it can. Put real, checkable criteria on every
   Story.

## Work altitude (how to size what you create)

This is about *granularity*, not labels. Use it to decide what to create:

- **Breakage** — something is broken in existing behavior. Labeled `Bug`.
- **Outcome-level work** — a demoable or measurable result a validator, customer,
  the manager, or a downstream system would *notice*. This is what you delegate.
  Labeled `Feature` (or `Improvement` if it's an enhancement to something that
  already works).
- **Plumbing** — internal enabling work not visible on its own (schema changes,
  refactors, infra, triggers). Usually a sub-issue the engineer creates under a
  Story, not something you delegate.

Throughout this skill, **"Story" means an outcome-level item at this altitude** —
the thing you hand off. It's a granularity concept, not a Linear label. Outcome-level
work should be the minority of what exists in the tree, but it's what you delegate.

## Labels

Apply **only Linear's built-in labels**: `Bug`, `Feature`, `Improvement` — plus
`spike` where it applies (see Spikes). Most delegated outcomes are `Feature`;
breakage is `Bug`; an enhancement to existing behavior is `Improvement`.

Do **not** apply:

- **domain labels** (`data` / `backend` / `frontend` / `bizdev`) — low signal when
  most work touches them anyway, and they clutter the label namespace;
- **Jira-imported type labels** (`Story` / `Task` / `Subtask`) — these are migration
  artifacts, not Linear types, and overlap confusingly with the built-ins.

Two tooling notes:

- The `labels` field on `save_issue` **replaces** the full set (it does not append),
  so pass the complete intended set every time.
- If the team has adopted Linear's native **Issue Types**, prefer setting the type
  field and apply *no* type label at all.

## Spikes

When a project has real design unknowns — an unproven approach, an architecture
decision, a "will this even work" question — the first delegated item can be a
**spike**: a time-boxed investigation whose deliverable is a **recommendation plus
evidence** (numbers, a prototype result), *not* shippable code.

- Label it `Feature` + `spike`.
- Write the acceptance criteria as the *questions it must answer* and the *metrics
  it must report*, not features to build.
- Make its "Out of scope" explicit: the spike de-risks the build; it does not start
  it (later milestones by name).
- It still follows the delegation rule — the assignee drafts their own breakdown and
  reports findings; you don't pre-decide the investigation steps.

A spike is the right first move when committing to the full build *before* answering
those questions would be the expensive mistake. It often slots in *ahead* of the P0
data/setup milestone.

## Altitude: single Story vs. Project

First decision, before creating anything:

- **Single Story** — the work fits in one cycle for one person. Create one Story,
  set its Project, assign it. Done.
- **Project (epic)** — the work spans multiple cycles or has natural phases/
  milestones (a spec with P0/P1/P2 phases, a multi-week build). Create a Linear
  **Project**, attach the source spec as a Linear **document**, and create one
  **milestone Story per phase**. Give **every** milestone Story an outcome +
  acceptance criteria, but **assign and cycle only the first**; future milestones
  stay in Backlog, unassigned, with no sub-issue breakdown (just-in-time).

Heuristic: if the source material has phases, sections like "P0/P1", or more than
~3 distinct outcomes, it's a Project, not a Story.

## Tooling

Use the Linear MCP tools. In this environment they're exposed with the
`mcp__claude_ai_Linear__` prefix — e.g. `mcp__claude_ai_Linear__list_issues`. The
prefix is dropped below for readability; prepend it when you actually call a tool.
Resolve references before creating:

- `list_teams` — get the team id.
- `list_projects` — find or confirm the target Project; reuse an existing one
  if it fits rather than creating duplicates.
- `list_issues` — **search existing issues for the topic before creating** (see
  Phase 2.5 — the subagents lean on this). Catches stubs and partial work, especially
  post-Jira-migration leftovers.
- `list_users` — resolve an assignee name to a user id.
- `list_issue_statuses` — confirm the workflow states for the team.
- `list_issue_labels` — confirm the built-in labels exist before applying.
- `save_project` — create the Project (epic) when needed.
- `save_document` — attach the source spec to the Project as a document; also
  used for the decisions addendum (see Edge cases).
- `save_issue` — create Stories/Tasks/Bugs. Set: title, description (the
  template below), team, **project**, label (`Feature`/`Bug`/`Improvement`, + `spike`
  if applicable), and assignee (only for the active Story). Leave new work in
  **Backlog**; cycling is a separate, explicit step (see Output rules).
- `save_milestone` — use project milestones if the team tracks phases as
  milestones rather than as milestone Stories; otherwise milestone Stories are fine.

Never create sub-issues on behalf of the assignee.

## Workflow

### Phase 1 — Classify

Read the source material. Decide: Bug / outcome-level / plumbing, single-Story vs.
Project, and whether the first item should be a spike. State your classification to
the user in one or two sentences before creating anything.

### Phase 2 — Resolve

Resolve the references the rest of the workflow needs: call `list_teams`,
`list_projects`, and (if an assignee was named) `list_users`; pin the team id, the
target Project (existing or to-be-created), and the assignee id. If no suitable
Project exists, propose creating one and name it. If the assignee is ambiguous or
unspecified, ask — do not guess who gets the work. If a named assignee can't be
resolved to a workspace member, create the Story **unassigned**, flag it for the lead
to invite/assign, and proceed — don't block.

Searching for duplicates and dependencies is its own step — see Phase 2.5. Don't do
that scan inline here; it floods this thread with issue data you don't need to hold.

### Phase 2.5 — Reconnaissance (subagent fan-out)

Before proposing structure, find out two things: **is this already being done**
(duplication) and **what does it depend on or hold up** (blocking). Both questions
are answered by reading a lot of existing Linear issues — exactly the kind of bulk
reading that shouldn't happen in this thread. Dispatch independent **read-only**
subagents, each scanning a different angle, and have them return only conclusions
(issue keys + a one-line verdict), not raw issue dumps. This is the same lean-context
pattern the `pr-review` skill uses: the heavy reading is offloaded; you keep the
synthesis.

**When to run it.** Any time there's meaningful existing work to collide with —
creating into an existing Project, or a non-trivial Story on an active team. Skip it
for a brand-new Project in an empty space or an obvious tiny one-off, and say so ("no
recon — new project, nothing to collide with"). Don't skip it just because the user
is in a hurry; a silent duplicate is the expensive outcome this prevents.

**Dispatch.** In a single message, spawn 2–4 subagents (scale to the size of the
work). Give each the work description plus the team/Project/assignee ids resolved in
Phase 2, and constrain each one explicitly: *use only the read-only Linear tools —
`list_issues`, `get_issue`, `list_projects`, `list_milestones`, `list_comments`.
Never call any `save_*` tool. Recon must not create or mutate anything.* Useful
angles:

- **Topic / keyword** — search open *and* recently closed issues across the team for
  the work's feature names and nouns. Closed issues matter: the work may already be
  done, or a prior attempt may explain why it's hard.
- **Target Project sweep** — enumerate the Project's open + in-progress issues and
  milestones. Is a slice of this already scoped, in flight, or half-built?
- **Assignee collision** — if an assignee is named, list their open / in-progress
  work. Would this duplicate or step on something they're already mid-stream on?
- **Dependencies** — hunt for work this would need finished first (a shared schema,
  an API, an upstream milestone) and work that's waiting on it. These become
  blocks / blocked-by edges.

Tell each subagent to return a compact structured verdict, e.g.:

```
{
  "duplicates": [{"key": "FUN-123", "url": "...", "title": "...", "verdict": "exact|partial|related", "why": "..."}],
  "blockedBy":  [{"key": "FUN-45",  "url": "...", "why": "needs the geonames table this story creates"}],
  "blocks":     [{"key": "FUN-90",  "url": "...", "why": "their map view can't start until this API exists"}]
}
```

**Synthesize.** Merge candidates across subagents, drop the false positives (keyword
collisions that aren't really the same work), and decide a disposition per real
duplicate: **supersede** / **relate** / **skip creation** / **proceed anyway with a
note**. Turn the dependency findings into the concrete blocks / blocked-by relations
you'll set in Phase 4. All of this goes into the Phase 3 proposal so the lead sees it
*before* anything is created — never silently merge into or supersede someone else's
issue.

### Phase 3 — Propose the structure (confirm before writing)

Show the user the full plan as a tree before creating anything in Linear:

- the Project (new or existing)
- the document(s) to attach (the spec, plus a decisions addendum if planning refined it)
- each milestone Story with its outcome + acceptance criteria (and the spike, if any, as the first item)
- which single Story will be assigned now
- **recon findings**: duplicates found + proposed disposition (relate / supersede /
  skip) with links, and the dependency edges to set (blocks / blocked-by) with links —
  or an explicit "recon found nothing" if clean
- explicit note that sub-issues are intentionally NOT being created
- explicit note that everything lands in Backlog (nothing cycled) unless the lead says otherwise

Wait for approval. Creating Linear issues is a side effect — never create without a
clear go-ahead.

**Per-story outcome gate.** Once the lead approves the overall tree, walk the
**outcome + acceptance criteria** for each Story past them in a single pass before
Phase 4. The outcome is the contract, so it earns explicit sign-off rather than being
skimmed inside the tree (a bundled "looks good" on five outcomes at once is how the
wrong outcome slips through). Keep it lean: present them as one compact list the lead
can batch-approve or flag individually — if there are many milestones, ask them to
call out only the ones that look off. This confirms *outcomes*; it is **not**
decomposition — do not open a task per story and do not start creating sub-issues.

### Phase 4 — Create

On approval, create top-down: Project → document(s) → milestone Stories → set Project,
label, and Backlog state on each → assign the first Story **if its owner is known**.
Then apply the recon outcomes: set the **blocks / blocked-by relations** surfaced in
Phase 2.5, and action each duplicate per its agreed disposition (add the relate /
supersede note and relation; skip creation where the work already exists). Do **not**
place it in a cycle unless the lead asks — leave cycling for sprint planning. Write
every Story's description with the template below.

### Phase 5 — Hand-off note

On the assigned Story, end the description with a hand-off line that puts the
breakdown back on the engineer (see template). Report back to the user with the
created keys/links and a one-line summary of what was deliberately left for the
engineer to scope.

## Issue description template

Every Story uses this structure. Keep it tight — this is a contract, not a design
doc (the design doc is the attached spec).

```
## Outcome
<One or two sentences: what is true when this is done. Stated as a result, not a
task list.>

## Acceptance criteria
- <Checkable / measurable / demoable condition>
- <Another>
- <Another>

## Context
<Why this matters, links to the spec/source, anything the engineer needs to not
rediscover from scratch. Link the attached Project document rather than restating
it.>

## Out of scope
<What this Story explicitly does NOT cover — usually "later milestones" by name.>

## Your breakdown
Draft the sub-issues for how you'll tackle this and run them by <lead> before you
start. Own the plan — this Story is the outcome, not the recipe.
```

For a **Bug**, replace Outcome/Acceptance with: Expected behavior, Actual behavior,
Repro / where it shows up, and the same "Your breakdown" line if non-trivial.

For a **spike**, write Acceptance criteria as the questions it must answer and the
metrics it must report; keep Out of scope explicit (it de-risks, doesn't start, the
build).

For a **Task** (internal plumbing, usually created by the engineer as a sub-issue,
not by you): a one-line outcome and acceptance check is enough; no ceremony.

## Output rules

- **Never pre-create sub-issues.** If you feel the urge, that urge is the signal to
  stop and leave it for the assignee.
- **Always set Project; never put project names in titles.**
- **Apply only built-in labels** (`Bug`/`Feature`/`Improvement` + `spike`); never
  domain or Jira-imported labels.
- **Default new work to Backlog.** Putting a Story into the current cycle is a
  separate, explicit step — don't bundle it into creation. Ask before cycling, or
  leave it for the lead's sprint planning.
- **Confirm before creating.** Show the tree, get the go-ahead.
- **Assign only what has a known owner.** Future milestones stay in Backlog with an
  outcome + acceptance criteria but no assignee, no cycle, and no sub-issue breakdown.
- **One assignee per Story.** If you don't know who, ask.
- Title = the outcome in plain language (e.g. "GeoNames canonical data loaded into
  Postgres"), not an imperative implementation step.

## Edge cases

- **Spec with companion files** (CSVs, JSON samples, research notes): prefer
  attaching **markdown** as a Project **document** (`save_document` takes markdown
  content directly — no upload step). For **binary or large sample files**, Linear's
  attachment upload is a prepare → PUT → finalize flow whose PUT step a **sandboxed
  agent usually can't complete** (outbound `curl`/PUT is blocked, and disabling the
  sandbox is not an option) — so zip the bundle and hand it to the lead to drag-drop,
  rather than reaching for a workaround. Reference the files from the relevant
  milestone's Context; don't inline their contents into issues.
- **Planning refined the spec**: when decisions taken during planning supersede or
  extend the source spec, capture them as a companion **"Design decisions" document**
  attached to the Project — don't rewrite the spec or bury the decisions in issue
  descriptions. Reference it from the affected milestones' Context.
- **Pre-existing stub / duplicate** (often a migrated issue): relate or supersede it
  (note it in its description, set the blocks/blocked-by relation) rather than leaving
  two homes for the same work.
- **Ambiguous altitude**: if it's borderline single-Story vs. Project, default to a
  single Story with clear acceptance criteria — you can always promote it later. Over-
  structuring early is the more expensive mistake.
- **Recurring / ops work**: not a good delegation target for this skill; suggest a
  recurring issue or a checklist rather than a milestone breakdown.
- **"Just make all the tickets for me"**: gently hold the line. Explain that pre-
  creating the sub-issues is what causes churn, create the Story/milestones, and put
  the breakdown back on the assignee. The user can override, but make the default
  visible.
- **No assignee yet, or assignee not a workspace member**: create the Story
  unassigned in the project backlog and flag it; don't put it in a cycle until it has
  an owner.
