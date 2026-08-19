# `/get-aligned` — design

**Date:** 2026-08-19
**Artifact:** `~/.claude/skills/get-aligned/SKILL.md` (single file)
**Status:** approved design, not yet implemented

## Purpose

You run several Claude sessions against one repo at once. They collide: two sessions edit the same
region, one waits on something another already shipped, a third is rebasing under everyone. There is
no way to ask "where is everyone" without visiting each terminal.

`/get-aligned` is invoked from an **overseer** session — fresh or long-running, it does not matter.
It polls every live session working this repo for a verified status report, finds the overlaps and
the mutual blockers, and publishes one ownership map back to all of them.

## Non-goals

- **Not arbitration.** The overseer reports contested regions to the human; it does not order a peer
  to abandon work. Where evidence settles ownership it says so; where it does not, the human decides.
- **Not a doctrine restatement.** `coordinating-with-peer-sessions` owns how peers talk. This skill
  owns the round: roster, poll, digest, map.
- **Not a subagent orchestrator.** Peers are independent sessions with their own contexts and
  permissions, not agents this session spawned. `superpowers:dispatching-parallel-agents` covers that.

## Invocation

User-invoked only — `disable-model-invocation: true`, following `wait-what`. A stray context match
that broadcasts to nine sessions is expensive and confusing; only the human fires this.

Optional argument: a focus line, appended verbatim to the poll so peers know what the alignment is
*for* ("we're all on the analyst seats"). Absent, the poll is generic.

## Phase 1 — roster

Sessions are discovered by joining two sources. Neither alone is sufficient.

1. `git worktree list --porcelain` → every path belonging to this repo, main checkout and linked
   worktrees alike.
2. `~/.claude/sessions/*.json` → one file per session, each holding `{pid, sessionId, cwd, name,
   startedAt, kind, entrypoint}`.
3. `ListAgents` → the live set. A session file can outlive its process; `ListAgents` cannot.

**Match on `cwd`, never on the name prefix.** Session names are derived from the cwd basename, so a
session in `<repo>/.claude/worktrees/critic-seat` is named `critic-seat-xx` and a `fund-*` prefix
misses it, while the separate checkout `fund-improvement-loops` matches a `fund-` prefix for the
wrong reason. Keep a session when its `cwd` is at or under any path from step 1.

**Identify the overseer by subtraction.** `ListAgents` lists every peer *except* the caller. Among
session files whose `pid` is still alive (`kill -0`), the one absent from `ListAgents` is this
session. Exclude it. The liveness check matters: session files outlive their processes, so raw
subtraction returns every dead session too.

**Rank by last activity, not by age.** `ListAgents` prints `started X ago`, which is `startedAt` and
says nothing about whether the session did anything since. Real last-activity is the mtime of the
transcript `~/.claude/projects/<escaped-cwd>/<sessionId>.jsonl`, where `<escaped-cwd>` is the cwd
with every `/` and `.` replaced by `-`.

Render the proposed roster — name, worktree, last activity — and **wait for the human's yes** before
sending anything. Nine sessions is nine turns spent; six of them may be two days stale. Duplicate
names get their `[ref]` from `ListAgents` appended, since two live sessions can share a name.

## Phase 2 — poll

One `SendMessage` per rostered peer. The message is **self-contained**: a receiving session may never
invoke `coordinating-with-peer-sessions`, and a bare pointer leaves it with nothing. This follows the
precedent already set in `handoff`, which inlines the same doctrine for the same reason.

The poll states three things.

**The facts must come from commands, not memory.** `git branch --show-current`, `git worktree list`,
`git status --short`, `git log --oneline -5`. A session that compacted an hour ago will confidently
report a branch it left.

**Answer at the next natural pause. Do not abandon work in flight.**

**The template**, answered field by field:

| Field | Source |
|---|---|
| `branch`, `worktree` | verified by command |
| `dirty` | paths from `git status --short` |
| `recent` | last commits, plus one line on what they were for |
| `owns` | **regions, not filenames** — `parse_config` and its callers; the retry block in `send()` |
| `doing` | current task, one line |
| `next` | what it picks up after, one line |
| `blocked` | what unblocks it, and **who owns that** — "nothing" is a valid answer |

`owns` is regions because one file routinely has three owners; a filename-level map produces false
conflicts and hides real ones.

Then the overseer **ends its turn**, stating who it is waiting on. Replies drain at each peer's next
tool round and arrive as `<cross-session-message>` notifications, which re-invoke the overseer.

## Phase 3 — digest, map, broadcast

**Deadline.** Immediately after the poll, start a background timer — `Bash` with
`run_in_background: true` running `sleep 300`. Its exit re-invokes the overseer. Whichever comes
first, a full house or the timer, ends collection. The run never hangs on a wedged session.

The overseer then produces three things.

**Digest** — one block per session: doing / next / blocked. Silent sessions are named as silent,
carrying their last-known state from the previous map if one exists.

**Findings** — the actual product:
- two sessions claiming the same region
- a `dirty` path claimed by no one's `owns`
- a blocker whose unblocker is another polled session that does not know it
- a `recent` commit that contradicts another session's stated assumption

**Ownership map** — region → owner, plus **landing order** wherever a refactor and an addition
collide. The refactor lands first and the addition conforms to the new shape; replaying a refactor
over new code is where the errors come from.

Write digest + findings + map to `~/.claude/align/<repo-basename>/map.md` — outside every repo, so no
session's working tree is dirtied. Then broadcast the map to the rostered peers with its authority
stated inline:

> Binding at your next task boundary, never mid-task. Do not abandon work in flight. Before your next
> edit, conform to this map. If you disagree, reply with the conflicting fact — do not silently
> ignore it.

Contested regions the evidence does not settle are surfaced to the human, not decided by the overseer.

## Failure behavior

| Situation | Behavior |
|---|---|
| No live sessions on this repo | Print the last map if one exists, say nothing was polled, stop |
| Peer answers in prose, not the template | One re-ask, then treat as silent |
| Peer never answers | Named as silent in the digest; still receives the map |
| Peer disputes the map | Surfaced to the human. **No automatic revised rebroadcast** — peers receiving contradictory maps in sequence is worse than one stale map |
| `git worktree list` fails (not a repo) | Stop with the error. Do not fall back to name matching |

## Relationship to `coordinating-with-peer-sessions`

That skill is the doctrine: checkable claims, regions over filenames, refactor-lands-first, crossed
messages. `/get-aligned` is one scheduled round of it, driven from one seat. The skill file cites it
once as the source and inlines only the three rules the poll and map messages depend on.

## Verification

A green read of the file proves nothing. Done means: run `/get-aligned` from a fresh overseer against
at least two live sessions on this repo, and show the real transcript — roster gate, actual replies,
the written `map.md`, and at least one finding. A skill that reads well and deadlocks is the default
failure mode for anything built on cross-session messaging.
