---
name: huddle
description: Get every live session on this repo talking to each other, agree one path forward, then start the unblocked ones working.
argument-hint: "What are we huddling about? e.g. 'live run tomorrow' — optional"
disable-model-invocation: true
---

# Huddle

A working round, not a status round. Every session hears every other session, they respond to each
other, one path forward gets agreed, and then the sessions that aren't blocked **start work**.

Sibling skills, so you fire the right one:

| | |
|---|---|
| `/morning-standup` | Daily, scheduled. Everyone hears everyone. Nothing happens afterwards |
| `/get-aligned` | Branches are colliding. Ends in an ownership map |
| `/huddle` | Work is stuck. Ends in sessions actually working |

Doctrine for how peers talk lives in `coordinating-with-peer-sessions`. The messages below inline the
rules they depend on, because a receiving session may never invoke that skill.

## The two-round bound

**Exactly two rounds. Never a third.** Peers reply only to you, never to each other — you are the
only sender of broadcasts.

Three sessions replying to each other's replies is unbounded, costs every session a turn per lap, and
converges on nothing. The hub topology is what makes this skill terminate. If round two leaves a
genuine disagreement, that is a finding for the human, not a reason to run round three.

## Phase 1 — roster

Same join as `/get-aligned`: `git worktree list --porcelain` for repo paths, `~/.claude/sessions/*.json`
for each session's `cwd` and `sessionId`, `ListAgents` for the live set.

- **Match on `cwd`, never the name prefix.** A session in `<repo>/.claude/worktrees/critic-seat` is
  named `critic-seat-xx`; a `fund-*` prefix misses it and catches the unrelated checkout
  `fund-improvement-loops`.
- **`cwd` is where a session sits, not what it edits.** A session can commit into a worktree via
  `git -C`. The roster is a floor; reconcile against what peers report.
- **You are the one `ListAgents` omits.** Among session files whose `pid` is alive (`kill -0`), the
  one absent from `ListAgents` is this session.

Show the roster and **wait for a yes.** This round ends in code being written; the roster is who gets
told to write it.

## Phase 2 — round one, state

One `SendMessage` per peer, with the user's focus line appended if given:

> Huddle from the overseer seat. Two rounds, then work starts — this is round one. Answer at your
> next natural pause; do not abandon work in flight.
>
> Check facts rather than recalling them (`git status --short`, `git branch --show-current`). A
> session that compacted an hour ago will confidently report a branch it left.
>
> - **doing** — what you are on, one line
> - **owns** — regions, not filenames (`parse_config` and its callers; the retry block in `send()`)
> - **blocked** — what is stopping you and who owns that. "nothing" is valid and important here
> - **path** — what you think the right next move is for the group, not just for you. Say it even if
>   it means someone else's work should land before yours

End the turn, say who you are waiting on, and start the deadline:

```
Bash(run_in_background: true): sleep 300
```

## Phase 3 — round two, respond

Publish round one to **every** peer: each session's four fields, attributed by name, verbatim enough
to be checkable. Then ask for exactly one thing:

> Round two, the last one. Reply **only** if one of these is true:
> - You can unblock someone above. Say what you will do and by when.
> - You disagree with a stated path, and you have a fact that settles it — a path, a value, a commit.
> - Something above contradicts what you know.
>
> Nothing to add is a fine answer — say "nothing from me" so I know you are not silent.

Same deadline. Silence here is cheap; that is the point of naming the exit condition.

## Phase 4 — the path, and the go

Synthesize one **path forward**: ordered steps, one owner per step, and the dependency that fixes the
order. Where a refactor and an addition collide, the refactor lands first and the addition conforms —
replaying a refactor over new code is where the errors come from.

Write it to `~/.claude/align/<repo-basename>/huddles/YYYY-MM-DD-HHMM.md`, outside every repo so no
working tree is dirtied.

**Present it to the human and wait for a yes.** Nothing is sent before that. Lead with the steps and
their owners, then anything round two left genuinely contested.

On the yes, send go — **only to unblocked sessions, individually**:

> Path agreed. Your step: <step>. Go.
>
> This is a go on work you already own, not new scope. If the step as written needs something you do
> not own, reply instead of starting.

And to each blocked session:

> Path agreed. You are waiting on <thing>, owned by <peer>, who has it. Do not start <step> yet.

A session that never replied gets **no go** — you do not know its state, and a go to a session
already mid-task is how two sessions end up in one region.

## When it goes sideways

| Situation | Do this |
|---|---|
| Nobody is blocked | Skip round two. Publish the path, get the yes, go |
| Everyone is blocked on someone in the round | That is a deadlock, and it is the finding. Present it to the human. Send no go |
| Round two reopens round one | Do not run a third round. Publish the disagreement as contested and let the human call it |
| A peer disputes the path after go was sent | Surface it to the human. Do not rescind a go on your own — a session told to stop and then restarted has lost more than it gained |
| Peer never replied | No go. Named as unknown state in the huddle doc |
| `git worktree list` fails | Stop with the error. Do not fall back to name matching |
