---
name: whats-the-play
description: "Given what you're about to build or do, name the optimal skill sequence and start it. Only use when the user asks for it by name."
---

# What's the play?

The user described work they're about to start. Return the **optimal sequence of skills** for that work, then offer to begin.

You are a router: you diagnose the scenario and hand back a plan of attack. You do not do the work itself.

## Process

### 1. Classify

Read what the user wants. Match it against [`SCENARIOS.md`](SCENARIOS.md) — each entry has trigger patterns and a canonical sequence.

Ask a clarifying question **only** if the scenario is genuinely ambiguous between two entries with materially different sequences. One question, multiple choice. Otherwise classify silently and move on — the user came here for an answer, not an interview.

If nothing matches cleanly, say so and compose a sequence from the closest entry plus the adaptation rules. Never force a bad fit.

### 2. Apply adaptation rules

Walk every adaptation rule in `SCENARIOS.md`. These are what make the sequence specific to *this* work rather than generic. State each adaptation you applied and why, in one line — the user should see the reasoning, not just the output.

### 3. Check what's actually installed

Before naming a skill, confirm it exists. Check `~/.claude/skills/`, the project's `.claude/skills/`, and the account-level skills visible in your context.

**A router that names a skill the user doesn't have is worse than no router.** If a step's skill is missing, say what's missing and give the manual fallback for that step.

### 4. Emit the sequence

Numbered steps. For each:

- **What to type** — the exact command, or "(fires automatically)" for model-invoked skills
- **What comes out** — the artifact (design doc, spec, plan file, diff, report). A step with no artifact is a step you can't verify happened.
- **Why it's here** — one clause, specific to this work. Not "to plan the work" but "to pin down what 'edit' means when three events match."

Then two short sections:

- **Skipping** — which normally-present steps you left out and why. Being explicit about omissions is how the user catches a bad call.
- **Watch for** — the one or two places this particular work tends to go wrong.

Scale honestly. Small work gets a short sequence; if the work is genuinely trivial, say **"no pipeline needed — just do it"** and stop. Ceremonial over-prescription trains the user to ignore you.

### 5. Offer to start

Ask: *"Start with step 1?"*

On yes:

The invocation law in [`SCENARIOS.md`](SCENARIOS.md) owns both lists. Do not restate them here — a second copy drifts, and a skill missing from one list is a step the router can't act on.

- **On the chainable list** — invoke it now.
- **On the human-only list** — you cannot fire it. Print the exact command on its own line for the user to send.
  - Exception worth knowing: `/grill-with-docs` is a thin wrapper that runs `grilling` informed by `domain-modeling`. If that's step 1 and the user says yes, invoke those two directly rather than making them re-type.
- **On neither** — the lists lag what's installed. If your platform exposes it as invocable, treat it as chainable; otherwise print the command. Either way, add it to the right list in `SCENARIOS.md` before you finish.

Do not chain past step 1. Each step's skill owns its own handoff to the next.
