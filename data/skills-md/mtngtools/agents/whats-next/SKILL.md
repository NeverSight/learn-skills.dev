---
name: whats-next
description: Work out the next move on the current wayfinder map and hand back a short, copy-pasteable prompt for the session that does it.
argument-hint: "Optional: the map (number or URL), if the session doesn't make it obvious"
metadata:
  type: command
  invocation: skill-callable
  applies-to: [planning, wayfinder, sessions, prompts]
---

# What's Next

Ends a session by handing over the start of the next one: a prompt short enough to read at a glance and copy without editing.

**Stay on the map.** Unless the current map is finished, the next move is on that same map. Do not offer a different effort, a tempting side quest, or a cleanup that occurred to you along the way — one map at a time is the whole discipline of `/wayfinder`, and this skill is where it gets broken if anywhere.

**The output is a prompt, not advice.** Everything the human needs to act is inside a copyable block. Reasoning that doesn't fit in the block goes in the one-line label above it, or nowhere.

## Process

### 1. Fix the map and the repo

From the argument, the session, or the tracker — in that order, and ask rather than search if none of them settles it. Ask the human which map rather than surveying the repo for one; this skill is for the map you were just on.

**Done when:** you have one map number and one `owner/name`.

### 2. Refresh the map, then read it for its state

Call `/read-the-map` fresh — nearly always, even on a map this session already read. Skip the re-read only when nothing could have changed the tracker since that last read: no claim, close, or comment landed in between. Stale state is exactly what hands back a prompt for dead work, so when in doubt, refresh.

It owns the checklist, the verdicts, and the verdict → next-move mapping; this skill turns its answer into something pasteable and adds nothing to the judgment.

If it comes back **Done** — everything closed, sliced, and merged — that is the one case where the next move leaves this map. Say so, and let the human pick the next effort.

**If the door it names is stale** — the ticket the map calls next is actually closed on the tracker — stop before building a prompt for it. Name the ticket, its closed state, and what the map still claims, then ask the human how to clean it up rather than guessing: drop it and recompute the frontier, treat the close as the map's own progress and move on, or flag it as closed in error.

**Done when:** you have its verdict, the one or two doors it names, and every child ticket's status — none of it more than one read old.

### 3. Cut the choices down

**Two, three at the very most.** A move earns its place by being **blocking** — the most other work waits on it — or **quick** — done in one short session and off the board. Everything else is not next; leave it out entirely rather than listing it as a third-best option.

**Done when:** every move left standing is there for one of those two reasons.

### 4. Hand over the prompt

One block per move, in the [shape below](#prompt-shape) — and if the move is a build ticket, [that rule](#a-build-ticket-is-implement-in-a-worktree-always) rather than your own judgment. Nothing after the blocks except a single line if something genuinely can't be said inside one.

**Done when:** the human can copy a block and paste it into a fresh session unchanged — and every build ticket among them says `/implement` and carries its worktree line.

### 5. Lay out the whole board

Below the what's-next block, the rest of the map: a heading that names the map, every ticket in one table, and a paste-ready prompt for everything else that's takeable right now. Format for all three lives in [The board](#the-board).

**Done when:** the heading carries the map's number as a link to its issue plus its title, every child and backlog ticket from step 2 appears in the table once, and every ready one outside the what's-next picks has its own block — or you've said the frontier holds nothing else.

## Prompt shape

The door `/read-the-map` named decides the shape. **If that door is a build ticket, skip to [the rule below](#a-build-ticket-is-implement-in-a-worktree-always) — it is the whole answer for those.** For everything else there are two shapes.

**A decision ticket on the map.** A `wayfinder:<type>` child. No skill of its own, so it rides in on `/wayfinder`:

```
/wayfinder <map#> take #<n> — <title> in repo <owner/name>
```

**A human-invoked skill.** The skill comes first and `/wayfinder` doesn't appear — the skill takes the map or the ticket itself:

```
/decisions-to-specs <map#> in repo <owner/name>
/specs-to-tickets <map#> in repo <owner/name>
/prototype #<n> in repo <owner/name>
/implement #<n> in repo <owner/name>
```

Keep the whole prompt to a line where it can be — the next session reads the map for itself, so a prompt that explains the work is padding.

**If the move writes to the repo** — `/decisions-to-specs`, `/implement`, `/prototype` — end the prompt with the worktree reminder, so it travels with the paste:

```
/decisions-to-specs 157 in repo mtngtools/mtng-dotnet-mono
Work in a worktree.
```

A move that only touches the tracker (`take`, `/specs-to-tickets`) gets no reminder — there's nothing to isolate.

### A build ticket is `/implement`, in a worktree, always

**A build ticket is any open issue on the map that isn't a `wayfinder:<type>` child** — the backlog `/specs-to-tickets` sliced out of the settled specs, whatever other labels it carries. `/read-the-map` gathers exactly that set at checklist item 3. If a ticket came from there, this section decides its prompt and the two shapes above do not.

Every build ticket hands back these two lines, both of them, whether it appears in the step 4 picks or in the board's ready-now blocks:

```
/implement #<n> in repo <owner/name>
Work in a worktree.
```

**Never `/wayfinder <map#> take #<n>` for a build ticket.** `take` is the door for decisions — grilling, research, charting — and aiming it at a build ticket sends the next session off to re-decide work whose decisions are already settled and specced. Build backlog means the verb is `/implement`, and there is no second option.

**Never drop the worktree line.** It is one line and it survives a paste into a session that never loads the skill.

**Which base that worktree branches from is `/implement`'s to settle, not this prompt's.** It fetches, looks for overlapping worktrees and open PRs, and asks the human before it cuts anything — including whether the work should stack on an unmerged PR. Naming a base in the prompt second-guesses a check that hasn't run yet, so the line stays exactly as short as it is above.

## Labels

One block, no label needed. More than one, each gets a **one-line label above its block** saying why it's on the list:

**Unblocks the other three tickets**
```
/wayfinder 157 take #163 — presentation timing base unit in repo mtngtools/mtng-dotnet-mono
```

**Quick — clears the last decision**
```
/decisions-to-specs 157 in repo mtngtools/mtng-dotnet-mono
Work in a worktree.
```

Labels are for choosing between blocks. They never carry instructions the pasted prompt needs — anything the next session must know goes inside the block.

## The board

The heading, the table, and the ready-now prompts, built from the tickets and backlog `/read-the-map` already gathered in step 2 — no second tracker pass.

**The heading carries the map's number as a link to its issue, then its title.** Never the bare word "Board", never the title on its own, and never a bare `#157` — several sessions run at once, each ending in one of these, and a board you can't place, or can't open, is dead text once it scrolls:

```markdown
## Board: [#157](https://github.com/mtngtools/mtng-dotnet-mono/issues/157) — presentation timing
```

**The number is the part that identifies the map**, and it is the part that gets dropped. A title alone reads fine and still costs the human a search to act on: titles get reworded on the tracker, near-duplicates run side by side across maps, and every prompt in the blocks below takes the number, not the title. `## Board: presentation timing` is the same failure as `## Board` — write the number first, every time.

**Link it.** `/read-the-map` already fetched the map, so its URL costs nothing here, and the heading is the one place the human goes to open the map itself — the ticket table below links its rows for the same reason. A number they have to paste into a search is a link you didn't write.

Both parts come from the tracker exactly as it has them. If the title is long, the whole title still goes in — a truncated name is the same problem as no name.

**The ticket table.** Every child ticket, open and closed, plus the build backlog — not just the frontier, so the human sees the whole map without opening the tracker.

```markdown
| # | Ticket | Type | Status | Blocked by |
|---|---|---|---|---|
| [163](url) | presentation timing base unit | wayfinder:task | open, unclaimed | — |
| [164](url) | grill: base unit for timing | wayfinder:grilling | closed | — |
| [165](url) | grill: frame boundary rule | wayfinder:grilling | open, unclaimed | — |
```

**Ready-now prompts.** One [prompt-shape](#prompt-shape) block for every ticket that's open, unblocked, unclaimed, and either `wayfinder:grilling` or from the build backlog — the takeable work outside the curated picks in step 4. A grilling ticket rides in on `/wayfinder <map#> take #<n>`; a build ticket takes the two-line `/implement` block from [the rule above](#a-build-ticket-is-implement-in-a-worktree-always), worktree line included — the rule is the same here as in step 4.

Each block gets a one-line bold label naming the ticket — not a reason, just enough to tell blocks apart once stacked:

**#165 — grill: frame boundary rule**
```
/wayfinder 157 take #165 — grill: frame boundary rule in repo mtngtools/mtng-dotnet-mono
```

**#171 — frame clock adapter**
```
/implement #171 in repo mtngtools/mtng-dotnet-mono
Work in a worktree.
```

Skip a ticket already pasted in step 4 — one block per ticket across the whole reply, never two. No ready ticket outside the what's-next picks means no blocks here; say so in a line rather than leaving the section silently empty.

## Where this sits in the flow

At the seam between sessions. `/read-the-map` says where this map stands; **`/whats-next`** says what to type to act on it. `/check-wayfinder-maps` is the one to reach for only when the question is *which map at all* — a different question from this one. `/check-wayfinder-maps` tables one row per map across the whole repo; this skill's [board](#the-board) tables one row per ticket on the single map in hand — the plural survey versus the one-map deep-dive.

Pairs with `/are-decisions-from-this-session-saved`: that one makes sure this session left nothing behind, this one makes sure the next one starts without re-deciding where it is.
