# claude-skills

My working set of [Claude Code](https://claude.com/claude-code) skills — 41 of them, curated, forked, and in a few cases written from scratch.

This repo *is* the install. `~/.claude/skills/` is a flat namespace where each directory name becomes the skill name, so cloning the repo to that path is the entire setup — no build step, no symlink farm, no install script.

```bash
git clone git@github.com:benjaminematton/claude-skills.git ~/.claude/skills
```

Already have skills there? Clone elsewhere and symlink the ones you want — Claude Code follows symlinks in the skills directory:

```bash
git clone git@github.com:benjaminematton/claude-skills.git ~/src/claude-skills
ln -s ~/src/claude-skills/whats-the-play ~/.claude/skills/whats-the-play
```

**`auto`** skills fire when Claude recognizes the situation. **`/name`** skills only you can invoke — nothing can trigger them on your behalf.

---

## Start here

| Skill | | What it does |
|---|---|---|
| [`whats-the-play`](whats-the-play/) | `/name` | Describe the work; get the optimal sequence of the skills below, then start it. A router over this whole repo — fourteen scenarios, an invocation law, and adaptation rules, retrieval-tested against fresh sessions. |

---

## Multi-session coordination

Running several Claude Code sessions against one repo. These are the original work here — the problem barely existed a year ago and the tooling for it still doesn't.

| Skill | | What it does |
|---|---|---|
| [`coordinating-with-peer-sessions`](coordinating-with-peer-sessions/) | `auto` | Ownership maps, message discipline, and the rule that a peer answers but never authorizes |
| [`huddle`](huddle/) | `/name` | Get every live session talking, agree one path, start work |
| [`get-aligned`](get-aligned/) | `/name` | One-round poll across sessions; publishes a single ownership map |
| [`morning-standup`](morning-standup/) | `/name` | Daily standup across active sessions — everyone reports, everyone hears the others |

## Design and decide

| Skill | | What it does |
|---|---|---|
| [`grilling`](grilling/) | `auto` | Relentless interview over a design tree; ends only when the frontier is empty |
| [`grill-me`](grill-me/) · [`grill-with-docs`](grill-with-docs/) | `/name` | The same, on demand — the second also writes ADRs and a glossary |
| [`codebase-design`](codebase-design/) | `auto` | Vocabulary for deep modules and where seams belong |
| [`domain-modeling`](domain-modeling/) | `auto` | Ubiquitous language and architecture decision records |
| [`prototype`](prototype/) | `auto` | Throwaway build that answers one design question |
| [`to-spec`](to-spec/) · [`to-questionnaire`](to-questionnaire/) | `/name` | Turn a conversation into a spec, or a decision you can't make into someone else's questionnaire |
| [`review-plan`](review-plan/) | `auto` | Adversarial review of a plan across four axes, before any code |

## Build and ship

| Skill | | What it does |
|---|---|---|
| [`implement`](implement/) | `/name` | Execute against a spec or set of tickets |
| [`linear-delegation`](linear-delegation/) | `auto` | Specs into Linear work, delegated at the outcome level — the engineer owns the breakdown |
| [`resolving-merge-conflicts`](resolving-merge-conflicts/) | `auto` | Work an in-progress merge or rebase |
| [`wizard`](wizard/) | `auto` | Generate a bash wizard for the steps only a human can do — dashboards, credentials, CI secrets |
| [`improve-codebase-architecture`](improve-codebase-architecture/) | `/name` | Survey a codebase for deepening opportunities, then grill your pick |

## Review

| Skill | | What it does |
|---|---|---|
| [`code-review`](code-review/) | `auto` | Two axes in parallel — repo standards, and whether it matches the spec |
| [`web-design-guidelines`](web-design-guidelines/) | `auto` | UI code against the Web Interface Guidelines |

## Evals

Building and validating LLM judges. The pairing matters: design the suite first, then measure whichever judges survive.

| Skill | | What it does |
|---|---|---|
| [`build-a-scorer`](build-a-scorer/) | `auto` | Pick atomic criteria, route each to the cheapest reliable check — code beats built-in beats judge |
| [`llm-judge-alignment`](llm-judge-alignment/) | `auto` | Measure a judge against human labels as two directional rates, and fix it when they diverge |
| [`prompt-engineer`](prompt-engineer/) | `auto` | Prompt templates, structured output schemas, evaluation frameworks |

## Research

| Skill | | What it does |
|---|---|---|
| [`become-expert`](become-expert/) | `auto` | Research a field to working expertise, then write a reusable field brief |
| [`last30days`](last30days/) | `auto` | What people actually said about a topic recently, across Reddit, X, HN, and the rest |

## Frontend

| Skill | | What it does |
|---|---|---|
| [`frontend-design`](frontend-design/) | `auto` | Commit to an aesthetic direction instead of defaulting to templated output |
| [`vercel-react-best-practices`](vercel-react-best-practices/) | `auto` | 70 React/Next performance rules, ordered by impact |
| [`gsap-core`](gsap-core/) · [`timeline`](gsap-timeline/) · [`scrolltrigger`](gsap-scrolltrigger/) · [`react`](gsap-react/) · [`plugins`](gsap-plugins/) · [`utils`](gsap-utils/) · [`performance`](gsap-performance/) | `auto` | Official GSAP animation reference, split by surface |

## Writing

| Skill | | What it does |
|---|---|---|
| [`google-devdocs-style`](google-devdocs-style/) | `auto` | Docs prose in the Google developer documentation voice |
| [`code-documenter`](code-documenter/) | `auto` | Docstrings, OpenAPI specs, JSDoc, doc portals |
| [`writing-for-agents`](writing-for-agents/) | `auto` | Wording documents agents consume by pointer — AGENTS.md, CLAUDE.md, context budget |

## Session plumbing

| Skill | | What it does |
|---|---|---|
| [`handoff`](handoff/) | `auto` | Compact a conversation into a document another agent can pick up |
| [`wait-what`](wait-what/) | `/name` | That message didn't land — re-pitch it |
| [`setup-matt-pocock-skills`](setup-matt-pocock-skills/) | `/name` | One-time per-repo configuration for the skills that need it |

---

## Conventions

Three rules this repo tries to hold to. They're the reason it's worth cloning rather than assembling your own from the same sources.

**Forks carry their provenance.** A vendored skill's header records its upstream URL and license, every local change, and — the part people skip — what was considered and deliberately left undone. [`llm-judge-alignment`](llm-judge-alignment/SKILL.md) is the heavily-patched case: ten numbered changes against a dead upstream, plus the one fix that was evaluated and rejected, with reasoning. [`build-a-scorer`](build-a-scorer/SKILL.md) is the opposite call: upstream is alive, so the body stays verbatim and the header says re-pull rather than edit. Either way a future reader can tell what upstream said, what I changed, and what I chose not to.

**Edits get a baseline first.** Changing a skill is changing behavior, so the change is tested the way code is: run the scenario against fresh sessions *before* the edit to see what actually goes wrong, make the smallest change that addresses it, then rerun. Most proposed edits die at the baseline because the failure isn't real — which is the point.

**Vendored means vendored.** Skills copied from elsewhere are copies, not claims. Attribution below.

## Attribution

Most of this repo is other people's work, kept here because it's good.

| Source | Skills |
|---|---|
| [Matt Pocock](https://github.com/mattpocock) | `code-review`, `codebase-design`, `domain-modeling`, `grill-me`, `grill-with-docs`, `grilling`, `handoff`, `implement`, `improve-codebase-architecture`, `prototype`, `resolving-merge-conflicts`, `setup-matt-pocock-skills`, `to-questionnaire`, `to-spec`, `wait-what`, `wizard`, `writing-for-agents` |
| [GreenSock](https://gsap.com) | the seven `gsap-*` skills |
| [Vercel](https://vercel.com) | `vercel-react-best-practices`, `web-design-guidelines` |
| [Anthropic](https://anthropic.com) | `frontend-design` |
| [MLflow](https://github.com/mlflow/skills) | `build-a-scorer` |
| [Latitude](https://github.com/latitude-dev/eval-skills) | `llm-judge-alignment` |
| [Jeffallan](https://github.com/Jeffallan) | `code-documenter`, `prompt-engineer` |

`review-plan` is adapted from Garry Tan's plan-mode workflow.

`become-expert`, `google-devdocs-style`, and `linear-delegation` arrived from somewhere I can no longer trace. If one is yours, open an issue and I'll credit or remove it.

Several vendored skills have been extended locally; each modified skill's header records what changed.

**Original here:** [`whats-the-play`](whats-the-play/) and the four multi-session coordination skills.

## License

Original work in this repo is MIT — see [LICENSE](LICENSE). Vendored skills keep the license of whatever they were copied from; where upstream declared one, it's preserved in that skill's frontmatter.
