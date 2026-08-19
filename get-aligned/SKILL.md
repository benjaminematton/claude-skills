---
name: get-aligned
description: Poll every live session on this repo for status, then publish one ownership map back.
argument-hint: "What is this alignment round about? (optional)"
disable-model-invocation: true
---

# Get aligned

One round of cross-session alignment, run from this seat. Poll the live sessions working this repo,
find the overlaps and mutual blockers, publish one ownership map back.

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
- **You are the one `ListAgents` omits.** It lists every peer except the caller. Among session files
  whose `pid` is alive (`kill -0`), the one absent from `ListAgents` is this session. Exclude it.
- **Rank by last activity.** `started X ago` is start time and says nothing about activity. Use the
  mtime of `~/.claude/projects/<escaped-cwd>/<sessionId>.jsonl`, where `<escaped-cwd>` is the cwd
  with every `/` and `.` turned into `-` (`tr './' '-'`).

Render the roster — name, worktree, last activity — and **wait for a yes before sending anything.**
Each peer spends a turn on this. Append the `[ref]` from `ListAgents` where two live sessions share a
name.

## Phase 2 — poll

One `SendMessage` per rostered peer. Send this, with the user's focus line appended if given:

> Alignment round from the overseer seat. Answer at your next natural pause — do not abandon work in
> flight.
>
> Get the factual half from commands, not memory: `git branch --show-current`, `git worktree list`,
> `git status --short`, `git log --oneline -5`. A session that compacted an hour ago will confidently
> report a branch it left.
>
> Reply with exactly these fields:
> - **branch / worktree** — verified
> - **dirty** — paths from `git status --short`
> - **recent** — last commits, plus one line on what they were for
> - **owns** — regions, not filenames (`parse_config` and its callers; the retry block in `send()`).
>   One file routinely has three owners; filenames produce false conflicts and hide real ones.
> - **doing** — one line
> - **next** — one line
> - **blocked** — what unblocks you and who owns it. "nothing" is a valid answer.

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
2. **Findings** — the point of the round. Two sessions claiming one region; a `dirty` path nobody
   owns; a blocker whose unblocker is another polled session and does not know it; a `recent` commit
   that contradicts another session's stated assumption.
3. **Ownership map** — region → owner, plus **landing order** wherever a refactor and an addition
   collide. The refactor lands first and the addition conforms to the new shape; replaying a refactor
   over new code is where the errors come from.

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
