---
name: get-aligned
description: Align every live session on this repo — against a focus line if given, otherwise on who owns what.
argument-hint: "What are we aligning on? e.g. 'live paper run tomorrow' — optional"
disable-model-invocation: true
---

# Get aligned

One round of cross-session alignment, run from this seat. Poll the live sessions working this repo
and publish an ownership map back.

**The focus line decides the round.**

| Focus line | Round |
|---|---|
| Given — "live run tomorrow" | Peers answer against it; the digest is a readiness call, and the map assigns the gaps |
| Absent | Peers report their own state; the digest is overlaps and mutual blockers, and the map assigns contested regions |

Both share the roster, the poll mechanics, and the map. Only two things change, marked below: two
extra fields in the poll, and the shape of the findings.

For a cheap daily "where is everyone", use `/morning-standup` instead: active sessions only, no map,
digest goes to everyone.

Doctrine for how peers talk lives in `coordinating-with-peer-sessions`. This skill is one scheduled
round of it. The messages below inline the rules they depend on, because a receiving session may
never invoke that skill and a bare pointer leaves it with nothing.

## Phase 1 — roster

Join three sources. Each alone is wrong.

```bash
git worktree list --porcelain | awk '/^worktree /{print $2}'   # every path in this repo
for f in ~/.claude/sessions/*.json; do                          # cwd + sessionId per session
  jq -r '[.pid,.name,.cwd,.sessionId]|@tsv' "$f" 2>/dev/null
done
```

Then `ListAgents` for the live set.

- **Match on `cwd`, never on the name prefix.** Names derive from the cwd basename, so a session in
  `<repo>/.claude/worktrees/critic-seat` is named `critic-seat-xx` and a `fund-*` prefix misses it,
  while the separate checkout `fund-improvement-loops` matches for the wrong reason. Keep a session
  whose `cwd` is at or under any worktree path.
- **`cwd` is where a session sits, not what it edits.** A session in the main checkout can commit
  into a worktree via `git -C`, and the join will not see it — an active worktree with no session
  matching its path means someone is driving it from elsewhere. Treat the roster as a floor, not a
  complete list, and reconcile it against what peers report owning.
- **You are the one `ListAgents` omits.** It lists every peer except the caller. Among session files
  whose `pid` is alive (`kill -0`), the one absent from `ListAgents` is this session. Exclude it.
- **Rank by last activity.** `started X ago` is start time and says nothing about activity. Use the
  mtime of `~/.claude/projects/<escaped-cwd>/<sessionId>.jsonl`, where `<escaped-cwd>` is the cwd
  with every `/` and `.` turned into `-` (`tr './' '-'`). **This stops being an activity signal the
  moment a session enters a worktree** — its transcript moves to a worktree-scoped projects directory
  and the old path goes quiet. One round read that as a 3.5-hour stall on a session that was working.
  Ask before concluding anyone is idle.
- **Re-check `ListAgents` immediately before you broadcast.** The roster is a snapshot and fleets
  grow: one measured run built a roster of 3 and found 11 live sessions nineteen minutes later, 8 of
  which did not exist when the roster was built. State coverage in the digest — "polled 3 of 11" — so
  a partial round is never read as a complete one.
- **A peer's other repos are invisible to you.** The roster is this repo's worktrees, so a peer's
  "nothing is mine here" never means "nothing is mine anywhere". Do not let a clean map imply a clean
  machine.

Render the roster — name, worktree, last activity — and **wait for a yes before sending anything.**
Each peer spends a turn on this. **Key your records on `sessionId`, not on the name and not on the
`[ref]`.** Measured across a 13-session round: six sessions had renamed that day, three reported refs
that did not match `ListAgents`, and one send to a peer's own ref was refused. `sessionId` is stable
for the life of the session and is the string on the editor tab. Send to the name — that is the
address `SendMessage` takes — but record the `sessionId`.

## Phase 2 — poll

One `SendMessage` per rostered peer. Send this, with the user's focus line appended if given:

> Alignment round from the overseer seat. Answer at your next natural pause — do not abandon work in
> flight.
>
> Get the factual half from commands, not memory: `git branch --show-current`, `git worktree list`,
> `git status --short`. A session that compacted an hour ago will confidently report a branch it
> left.
>
> Reply with exactly these fields:
> - **branch / worktree** — verified
> - **dirty** — paths from `git status --short`
> - **recent** — commits **you** made, each checked with `git show --stat <sha>`, plus one line on
>   what they were for. Not `git log -5`: in a shared checkout that returns the *branch's* history,
>   which is mostly other sessions' work. "None" is a normal answer
> - **owns** — regions, not filenames (`parse_config` and its callers; the retry block in `send()`).
>   One file routinely has three owners; filenames produce false conflicts and hide real ones. Give
>   each region a status: **live** (working it now), **parked** (yours, not being worked, resumable),
>   **held** (complete but unshipped), **prospective** (intend to start, nothing begun). "nothing" is
>   a complete answer.
> - **doing** — one line
> - **next** — one line
> - **blocked** — what unblocks you and who owns it. "nothing" is a valid answer.

**If a focus line was given, add two fields** — and they are the ones that matter. The first six
describe the session; these two describe the thing you are aligning on:

> - **bearing** — what you hold that it touches or needs. "nothing of mine bears on it"
>   is a valid and useful answer.
> - **risk** — what you know that could stop it, including anything you were planning to land before
>   it. Say it even if you think someone else has it covered.

Then **end the turn**, saying who you are waiting on, and start the deadline:

```
Bash(run_in_background: true): sleep 300
```

Replies drain at each peer's next tool round and arrive as `<cross-session-message>` notifications.
Whichever lands first — a full house or the timer — ends collection.

## Phase 3 — digest and map

Produce three parts, in this order:

1. **Digest** — one block per session: doing / next / blocked. Name silent sessions as silent,
   carrying last-known state from the previous map if one exists.
2. **Findings** — the point of the round, and the part the focus line changes.

   *No focus line:* two sessions claiming one region; a `dirty` path nobody owns; a blocker whose
   unblocker is another polled session and does not know it; a `recent` commit that contradicts
   another session's stated assumption.

   *With a focus line:* a **readiness call on it**, in this order — what is ready and who
   verified it; what is missing, and for each gap the owner or **"unowned"**; what could stop it,
   from the `risk` field; and one line saying whether it holds, naming the single thing most likely
   to break it. An unowned gap is the most important output of the round: it is the work nobody
   thinks is theirs. Never soften a readiness call to be encouraging — if the answer is that it does
   not hold, say that first.
3. **Ownership map** — region → owner, plus **landing order** wherever a refactor and an addition
   collide. The refactor lands first and the addition conforms to the new shape; replaying a refactor
   over new code is where the errors come from.

   **Key it on `sessionId`.** Names collide and churn — two live sessions answering to `fund-8b`
   merge into one row in a name-keyed table — and refs proved unreliable in practice. State the
   deviation at the top of the map so readers know what the rows are keyed on.

   **Releases are first-class entries.** A session handing a region back belongs on the map as
   plainly as one claiming it. A stale claim is worse than a blank: it makes the next session route
   around a region nobody is in.

   **Carry the status through to the map** — live / parked / held / prospective, per region. "I own
   this and am not working it" and "I might work this later" are different facts, and a reader
   deciding whether to touch a region needs to know which one they are looking at. A map full of
   prospective entries read as claims teaches everyone to ignore the next one.

Write all three to `~/.claude/align/<repo-basename>/map.md` — outside every repo, so no working tree
is dirtied. Then broadcast the map to the rostered peers with its authority stated inline:

> Binding at your next task boundary, never mid-task. Do not abandon work in flight. Before your next
> edit, conform to this map. If you disagree, reply with the conflicting fact.

Regions the evidence does not settle go to the human. You report contested ownership; you do not
decide it.

## When it goes sideways

| Situation | Do this |
|---|---|
| No live sessions on this repo | Print the last map if one exists, say nothing was polled, stop |
| Peer answers in prose, not the fields | One re-ask, then treat as silent |
| Peer never answers | Named silent in the digest; still gets the map |
| Peer disputes the map | Surface it to the human. Do not rebroadcast a revised map — peers receiving contradictory maps in sequence is worse than one stale map |
| `git worktree list` fails | Stop with the error. Do not fall back to name matching |
