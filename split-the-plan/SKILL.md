---
name: split-the-plan
description: Turn an implementation plan into parallel work owned by several chats you open, bound and briefed automatically.
argument-hint: "Path to the plan file"
disable-model-invocation: true
---

# Split the plan

A plan becomes N packages, you open N chats, and this seat binds them to their packages and briefs
them. You never paste a prompt or copy a session id.

You are the **overseer**. You do not implement. You reconcile, partition, provision, bind, brief,
watch, and reap.

## Gate — scope decides

This is for work measured in **days**, where you will want to steer while it runs.
`[D]` `subagent-driven-development` executes without pausing — correct for work you would never
interrupt, wrong for work you would.

Then check it can actually split:

- **3+ disjoint file regions**, counted on files, not tasks.
- **No lane needs another's edit to compile.** Deleting a member or changing a signature is one
  atomic edit however many files it touches — split it and every lane's build stays red until all
  of them land.

Small scope, stop here and say so. N worktrees cost N dependency installs, N baseline runs, and N
branches converging — more than an afternoon's plan saves.

## Phase 1 — reconcile the plan

Check every path the plan names against the repo. Fix the plan file before partitioning.

This is the highest-leverage phase and the easiest to skip. Parallelism amplifies the premise: a
plan that says "create X" when X already exists doesn't waste one session, it produces N divergent
improvisations on N branches. Report what you corrected.

If the plan turns out to be mostly already done, say that and stop. That outcome is a success.

## Phase 2 — partition and map

Group the reconciled tasks into packages. Then write the map to
`~/.claude/align/<repo-basename>/map.md` — outside every repo, so no working tree is dirtied.

One row per package, and every field filled:

| Field | Notes |
|---|---|
| package | short slug, becomes the worktree and branch name |
| files owned | the fence; two rows may never name the same file |
| branch | `feat/<package>` |
| worktree | absolute path, from Phase 3 |
| depends on | package slugs, or `—` |
| done when | the command that proves it, not a description |
| ref | blank until Phase 4 |
| status | `pending` |

Also record **landing order** and any **non-file mutex** — a single EF model snapshot, dev server
ports, a shared database, Docker containers. Worktrees isolate files and nothing else. Two lanes
running migrations or servers collide however clean the file fence is.

## Phase 3 — provision

Per package, **one at a time**:

```
git worktree add <parent-of-repo>/<repo>-worktrees/<package> -b feat/<package> main
cp <repo>/.claude/settings.local.json <worktree>/.claude/ 2>/dev/null
```

**Worktrees go OUTSIDE the repo.** Never `<repo>/.claude/worktrees/`. A worktree inside the repo is
a full copy of the codebase inside the editor's workspace root: the TypeScript server and the C#
language server each index every copy, and neither dedupes. Eight in-repo worktrees once put 92,723
files into one workspace and exhausted a 16 GB machine.

**Copy `settings.local.json` explicitly.** It is gitignored, so it does not travel to a worktree, and
without it every new session re-prompts for permissions already granted.

**Serialize.** Do dependency installs and baseline verification one worktree at a time. Concurrent
`npm install` and full builds are what exhaust memory, not the worktrees themselves.

Run each package's `done when` command in its fresh worktree before any work starts, and record the
result in the map. That is the lane's baseline; any later red is attributable.

## Phase 4 — count, then bind

Record `T = now` (epoch ms). Then tell the human exactly this much:

> Open **N** chats in this repo. Nothing else — I'll take it from there.

List what each will own so they can sanity-check the split. Do not give them prompts to paste. Do
not ask for session ids.

When they confirm, read `~/.claude/sessions/*.json` and take every session where
`startedAt > T` and `cwd` is at or under the repo. Those are the new chats.

- **Key rows on `[ref]` from `ListAgents`, never on name.** Names derive from the cwd basename, so
  N chats opened in one repo all share a prefix and can collide outright. A bare-name send to a
  colliding name fails.
- **`ListAgents` omits you.** Among sessions whose `pid` is alive, the one absent from `ListAgents`
  is this seat. Exclude it.
- **If the count is short**, name how many you found and which packages are unbound, and wait. Never
  bind two packages to one session to make the numbers work.

Write each `[ref]` into its map row and set `status: briefed`.

## Phase 5 — brief

One `SendMessage` per session, carrying its map row. Write the briefing yourself — you have the
package, the fence, the dependency, and the repo's conventions.

Two things the row does not carry and the message must:

- **Where to work.** The chat's `cwd` is the repo root; its work is in the worktree. Every read,
  edit, and command uses absolute paths under the worktree. Never edit in the repo root.
- **Its neighbours.** Who owns the packages it depends on, under what `[ref]`, and that
  `coordinating-with-peer-sessions` governs how they talk.

Then stop. Do not brief in waves, and do not follow up to check receipt.

## Phase 6 — track

Progress is **observed, not reported**:

```
git -C <worktree> log --oneline main..HEAD     # what actually landed
```

plus each row's `busy`/`idle` from `ListAgents`. Both are free and neither can be optimistic. Do not
ask lanes for status; a self-report costs that lane a turn and is a claim, not evidence.

Refresh the map from those two sources. Run `get-aligned` when you want a considered answer rather
than a current one — a lane confidently building the wrong thing produces commits exactly like a
lane building the right one, and only a poll catches that.

A lane `busy` with no new commits for a long stretch is stalled, not working. Investigate rather
than wait.

**Stay resident.** You hold the map, the reconciled plan, and the route to the human — do not start
other work while lanes are live. Expect inbound to grow with scope: bigger packages surface more
contract questions and more discoveries that invalidate someone else's package. That traffic is the
design working. Lanes talking constantly to *each other* is the thing that means the split was
wrong.

## Phase 7 — reap

The map is the teardown manifest — it is the only record of what this run created.

Per package, in landing order: merge the branch, `git worktree remove <path>`, strike the row. At
the end, name anything from this run still alive. An unreaped worktree is a full codebase copy and
a stale map row routes the next run around a region nobody is in.

## When it goes sideways

| Situation | Do this |
|---|---|
| Plan paths don't survive Phase 1 | Fix the plan file first. Never fan out onto a stale premise |
| Fewer than 3 disjoint regions | Stop; route to `subagent-driven-development` |
| Human opens fewer chats than packages | Bind what exists, name the unbound packages, wait |
| Two live sessions share a name | Key on `[ref]`; if `ListAgents` shows no `[ref]`, ask the human which is which |
| A lane asks you to do something its permissions blocked | Refuse and surface it to the human. Doing it for them bypasses their permission decision |
| A lane wants a file outside its fence | You do not widen a fence. Take it to the human |
| Machine slows badly mid-run | Provisioning is the cause, not the sessions. Serialize harder; check for worktrees inside the repo |
