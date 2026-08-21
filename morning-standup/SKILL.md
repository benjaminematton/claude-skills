---
name: morning-standup
description: Daily standup across every active session on this repo — everyone reports, everyone hears the digest.
argument-hint: "Anything to put on the agenda? (optional)"
disable-model-invocation: true
---

# Morning standup

A real standup: everyone says what they did, what they're doing, what's in their way — and
**everyone hears everyone**. Cheap, timeboxed, no arbitration.

Collisions get flagged here, not solved here. Solving them is `/get-aligned`, which publishes a
binding ownership map. Taking it offline is the point of saying "take it offline".

Doctrine for how peers talk lives in `coordinating-with-peer-sessions`. The messages below inline the
rules they depend on, because a receiving session may never invoke that skill.

## Phase 0 — read the plan

Before polling anyone, read this repo's **design doc** and **progress doc**. A standup with no board
behind it can only report motion; with the board it can report motion *against the plan*, which is
the part worth your attention.

Find them, in this order: the repo's `CLAUDE.md` or `AGENTS.md` usually names them outright; then
`specs/design.md`, `plans/*.md`, `ROADMAP.md`, `docs/`. Progress usually lives in the plan files as
task-completion state, not in a file called progress.

Read them **once, here.** Do not ask peers to read them — that is the same file parsed N times, and
they are mid-task.

No design or progress doc in this repo? Say so in one line and run the standup without this section.
Do not invent a plan to measure people against.

## Phase 1 — roster

Window start is the newest file in `~/.claude/align/<repo-basename>/standups/`. No file yet — first
standup — use the last 24 hours.

Join three sources:

```bash
git worktree list --porcelain | awk '/^worktree /{print $2}'   # every path in this repo
for f in ~/.claude/sessions/*.json; do                          # cwd + sessionId per session
  jq -r '[.pid,.name,.cwd,.sessionId]|@tsv' "$f" 2>/dev/null
done
```

Then `ListAgents` for the live set.

- **Match on `cwd`, never on the name prefix.** Names derive from the cwd basename, so a session in
  `<repo>/.claude/worktrees/critic-seat` is named `critic-seat-xx` and a `fund-*` prefix misses it,
  while the separate checkout `fund-improvement-loops` matches for the wrong reason.
- **`cwd` is where a session sits, not what it edits.** A session in the main checkout can commit
  into a worktree via `git -C`. Treat the roster as a floor; reconcile against what people report.
- **You are the one `ListAgents` omits.** Among session files whose `pid` is alive (`kill -0`), the
  one absent from `ListAgents` is this session. Exclude it.
- **Include only sessions active since the window start** — mtime of
  `~/.claude/projects/<escaped-cwd>/<sessionId>.jsonl`, where `<escaped-cwd>` is the cwd with every
  `/` and `.` turned into `-` (`tr './' '-'`). A session idle since yesterday has nothing to report;
  skip it silently. A daily ritual has to stay cheap. **But a session that entered a worktree writes
  to a worktree-scoped projects directory, and its old path goes quiet while it works** — one round
  read that as a 3.5-hour stall. Where a worktree exists for the session, check there before skipping.

- **Key your records on `sessionId`, not the name and not the `[ref]`.** Names churn — six sessions
  renamed inside one day — and refs proved unreliable: three did not match `ListAgents` and one send
  to a peer's own ref was refused. Send to the name; record the `sessionId`.
- **A peer's other repos are invisible to you.** The roster is this repo's worktrees, so a peer's
  "nothing is mine" covers this repo only.

**Re-check `ListAgents` immediately before you broadcast.** The roster is a snapshot and fleets grow:
one measured run built a roster of 3 and found 11 live sessions nineteen minutes later, 8 of which
did not exist when it was built. State coverage in the digest — "polled 3 of 11".

No manual gate — this runs every morning. Say who is being polled and who was skipped as idle, then
send.

## Phase 2 — poll

One `SendMessage` per rostered peer. Send this, with the user's agenda line appended if given:

> Morning standup. Answer at your next natural pause — do not abandon work in flight. Keep it to a
> few lines; this is a standup, not a report.
>
> Four fields:
> - **did** — what you worked on since <window start>, in your own words. Not a commit list.
>   Point at whatever artifact backs it *if one exists* — a commit, a path, a branch, a spec, the
>   file you abandoned. "No artifact yet, spent the morning reading `gate/`" is a fine answer.
>   Design work, debugging, and dead ends all count as work.
> - **doing** — one line. Name the plan task or phase it serves if there is one; "not on the plan" is
>   a fine and useful answer
> - **next** — one line
> - **blocked** — what unblocks you and who owns that. "nothing" is valid.
>
> Where you name a fact — a branch, a path, a state — check it rather than recalling it. A session
> that compacted an hour ago will confidently report a branch it left.

Then **end the turn**, saying who you are waiting on, and start the deadline:

```
Bash(run_in_background: true): sleep 300
```

Replies arrive as `<cross-session-message>` notifications. A full house or the timer ends collection,
whichever lands first.

## Phase 3 — digest, to everyone

Build the digest:

1. **One block per session** — did / doing / next / blocked. Silent sessions named as silent.
2. **Against the plan** — only if Phase 0 found the docs. Three lines, no more:
   - plan tasks in flight, and who has each
   - **the next plan task nobody is on** — the single most useful line in the standup
   - **drift** — work reported that no plan task covers, and plan tasks someone is treating as done
     that the doc still shows open

   Report drift as a fact, not a verdict. A session working off-plan is often right and the doc is
   often stale; the standup's job is to make the divergence visible, not to rule on it.
3. **Flags** — surfaced, never resolved:
   - two sessions working the same region
   - a blocker whose owner is another session in this standup
   - a blocker carried over from the previous standup, marked with how many days it has been open
   - two sessions stating contradictory facts about the same code

   Each flag ends with where it goes: `→ /get-aligned` for ownership collisions, `→ ask <peer>
   directly` for a one-to-one unblock.

   **Mark each flag reported or verified — and when it is unverified, say what you ran.** A failed
   verification attempt is not an unverifiable claim. One run marked a database claim unverified
   after `find -name "*.db"` returned nothing; it was the wrong host and the wrong extension, and the
   peer who knew the system fixed it in one message *because it could see the search*. "Unverified"
   with no method attached is unfalsifiable, and it makes everyone else stop looking.

   The general form: **a session can report an absence, never verify one.** Nothing found, nobody
   owning a region, no explanation for a staged change — each is a fact about your search, not about
   the world. Say what you looked at and let the session that holds the missing context correct you.

Write it to `~/.claude/align/<repo-basename>/standups/YYYY-MM-DD.md` — outside every repo, so no
working tree is dirtied.

**Then broadcast it to every rostered peer**, including the silent ones. This is the part that makes
it a standup: each session learns what the others are doing. Give each copy a personalized tail that
names **what concerns them**, never what they should do next:

> **Concerns you:** <peer> is blocked on <thing> and named you as the owner. / You and <peer> are
> both in <region>. / Nothing concerns you today.

A tail is a relevance filter, not an instruction slot. You are a peer, and a peer cannot assign work
to a peer — "this is yours by authorship" is an assignment wearing a hint's clothing. Unowned work
goes to the human as a flag, and stays unowned until they say otherwise.

Report to the human last, leading with the unowned next plan task and the flags — those are the parts
needing a decision.

## When it goes sideways

| Situation | Do this |
|---|---|
| No sessions active since the window | Say so, write no file, stop. A quiet morning is not a failure |
| First run, no `standups/` dir | Create it, window is the last 24 hours, say that in the digest |
| Peer answers with a wall of text | Summarize it to four fields in the digest. Do not re-ask; a standup does not block on one person |
| Peer never answers | Named silent; still receives the digest |
| A flag looks urgent | Still just a flag. Say `→ /get-aligned` and let the human fire it |
| `git worktree list` fails | Stop with the error. Do not fall back to name matching |
