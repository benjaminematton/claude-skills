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

## Corrections that arrive outside the rounds

Peers send corrections you did not ask for — retractions, self-corrections, a fix for a bug another
session surfaced — and they arrive mid-phase, including after you have closed round two. Expect it.

**They are evidence, not a third round.** Fold them into the path before you present it. If the path
is already with the human, re-present the changed part rather than letting a stale path go out. Never
broadcast a reply to one: that is what starts the lap the two-round bound exists to prevent.

The bound governs laps, not arrivals — a round where sessions overturn their own earlier claims is
the round working. But volume is a separate failure from lap count: one measured run solicited 6
sessions and received 16 messages.

**Read every arrival. Reply to none.** A reply turns one arrival into two. If one genuinely needs an
answer before you can present the path, that is a finding for the human — it goes in the doc.

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
- **Append the `[ref]` where two live sessions share a name.** Derived names collide, and a bare-name
  send to either of two `fund-8b`s fails.
- **A peer's other repos are invisible to you.** The roster is this repo's worktrees, so a peer's
  "nothing is mine" covers this repo only.

**Re-check `ListAgents` immediately before you broadcast.** The roster is a snapshot and fleets grow:
one measured run built a roster of 3 and found 11 live sessions nineteen minutes later, 8 of which
did not exist when it was built. State coverage when you show the roster — "polled 3 of 11". A go
issued off a stale roster is the failure this skill exists to prevent.

**Do not trim by recency.** `/morning-standup` filters to sessions active since yesterday, because a
quiet session has nothing to report. A huddle is the opposite: the session that has not spoken all
day may be the one holding the region you are about to hand to someone else. Poll everyone live on
the repo, and let the roster gate — not your own guess at who matters — be where it gets narrowed.

**Then broadcast in batches of about six.** This is a machine bound, not a roster bound: the whole
roster still gets polled. But every peer you wake runs `git` and reads files, so a broadcast to N is
N Claude Code processes doing disk I/O at once, on top of the N already holding their context in
RAM. A laptop running a dozen sessions can be swapping before the huddle starts — check `ps aux |
grep -c '[c]laude'` and the free-memory line from `memory_pressure` while building the roster, and
say the number out loud when you show it. If the roster is larger than the machine, that is the
human's call to make before round one, not something to discover when the box starts paging.

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
> Your reply is exactly four lines, one per field, each under 200 characters. Evidence is a SHA, a
> path, or a branch name — the pointer, not the output.
>
> - **doing** — what you are on
> - **owns** — regions, not filenames (`parse_config` and its callers; the retry block in `send()`).
>   Releasing a region counts, and so does "nothing" — a stale claim is worse than a blank, because it
>   makes everyone route around a region you already left
> - **blocked** — what is stopping you and who owns that. "nothing" is valid and important here
> - **path** — the right next move for the group, not just for you
>
> Reply to me only. If something here concerns another session, name them in your reply — I will put
> the two of you in touch if you overlap.

Peers never read this skill; they only see the broadcast. The hub topology holds only if the
broadcast says so — unstated, one measured run leaked ten peer-to-peer messages during the rounds,
each one waking a session nobody was waiting on.

Keep the shape stated. Without those two sentences "one line" is decorative — the same prompt drew
3.5k–5.2k-character replies; with them, 750–890. Do not soften it to "be brief": asking for brevity
while also asking peers to check facts is what produced the essays.

End the turn, say who you are waiting on, and start the deadline:

```
Bash(run_in_background: true): sleep 300
```

## Phase 3 — round two, respond

**Write the round-one board to the huddle doc before you broadcast anything** — same path Phase 4
uses, `~/.claude/align/<repo-basename>/huddles/YYYY-MM-DD-HHMM.md`, each session's four lines
attributed by name. Then send every peer a **pointer to it, never a copy of it**:

> Round two, the last one. Every session's round one is at `<path>` — read it there.
>
> Reply **only** if one of these is true:
> - You can unblock someone in it. Say what you will do and by when.
> - You disagree with a stated path, and you have a fact that settles it — a path, a value, a commit.
> - Something in it contradicts what you know.
>
> Nothing to add is a fine answer — say "nothing from me" so I know you are not silent.

Same deadline. Silence here is cheap; that is the point of naming the exit condition.

Inlining the board is quadratic — N sessions each receiving N states, and every peer pays to read its
copy. At eight peers that measured 19,561 characters outbound against about 3,200 for a pointer.

## Phase 4 — the path, and the go

Synthesize one **path forward**: ordered steps, one owner per step, and the dependency that fixes the
order. Where a refactor and an addition collide, the refactor lands first and the addition conforms —
replaying a refactor over new code is where the errors come from.

**Then name the pairs.** Two sessions whose regions overlap need a direct line to each other, and
discovering that is what the rounds were for — it is a deliverable, not a side effect. List each
overlapping pair in the doc with the region they share.

Pairs, never groups. Three sessions in one region is a finding for the human, not a group chat — that
is the unbounded lap the two-round bound exists to prevent, arriving by a different door. And pairing
happens here, after the rounds close, never during them: two sessions talking is two processes awake,
where the same conversation mid-round means everyone is awake at once.

Append it to the huddle doc under the round-one board — Phase 3 created that file; if you skipped
round two, create it here. It sits outside every repo so no working tree is dirtied.

**Present it to the human and wait for a yes.** Nothing is sent before that. Lead with the steps and
their owners, then anything round two left genuinely contested.

On the yes, send go — **only to unblocked sessions, individually**:

> Path agreed. Your step: <step>. Go.
>
> <peer> is in your region — you both touch <region>. Talk to them directly from here; you do not
> need me in the middle. Anyone else, route through me.
>
> This is a go on work you already own, not new scope. If the step as written needs something you do
> not own, reply instead of starting.

Send the pair line only to sessions that actually have a counterpart, and name only the one region
they share. A session told it overlaps with everyone talks to everyone.

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
