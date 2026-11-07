---
name: grilling
description: Grill the user about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.
---

Interview the user until you reach a shared understanding. Map the plan as a
**design tree**: every decision branches into the decisions that hang off it. Show
the tree first, each branch with your recommended answer, so the user can prune
before you ask anything.

## Work the tree in rounds

The **frontier** is every decision whose prerequisites are settled: the questions
you can ask now without guessing at answers you haven't heard. A question that
depends on another question still open belongs to a later round.

Sort the frontier by stakes:

- **Load-bearing**: hard to reverse, branches the tree, a real trade-off. Each one
  is its own numbered question with your recommended answer.
- **Low-stakes**: an obvious default, cheap to change later. One list at the end of
  the round, recommended answer each; the user accepts them in a word or overrides
  the few they care about.

Format a round like so, wording each question so "yes" accepts your recommended
answer:

```
❓ **Q1** - **<question title>**: <question body, may include choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body>

➡️ <your recommended answer>

**Defaults** (say "ok" to accept all):
- <decision>: <recommended answer>
- <decision>: <recommended answer>
```

Wait for the answers. Each round reshapes the tree: settled decisions push the
frontier outward and unblock what depended on them. Recompute the frontier and ask
the next round.

When the tree is still widening after a few rounds, or whole branches wait on
research, prototypes, or other people, the plan is bigger than one session. Say so
and suggest `/wayfinder`, which charts a map from what is settled so far. Inside a
wayfinder ticket, a new branch goes to the map as a ticket or fog instead.

## Facts are yours, decisions are the user's, some are someone else's

Finding facts (filesystem, tools, code, docs) is your job, never the user's. When a
frontier question needs a fact, dispatch a sub-agent to find it. The decisions are
the user's: put each to them and wait.

A decision the user hands to a third person ("that's my boss's call", "the
integrations team would know") is **deferred**. Record the owner and keep your
recommended answer beside it. A deferred question stays out of the Defaults list
and stays open until its owner answers it.

A fact still being looked up and a deferred decision block the same way: only the
questions downstream of them wait. Ask the rest of the frontier now.

## Stop when the stakes run out

The session is done when the frontier is empty, or when only low-stakes decisions
remain: list those with their defaults and ask for one confirmation. Ask only
questions whose answer changes what gets built. Do not act on any of it until the
user confirms you have reached a shared understanding.

If deferred decisions remain when the frontier runs dry, the session pauses
instead of ending: write the questionnaire and stop.

## Deferred decisions pause the session on a questionnaire

File one issue on the project issue tracker, labelled `needs-grilling`, with the
body from [QUESTIONNAIRE.md](QUESTIONNAIRE.md): every decision settled so far, then
the deferred questions grouped by owner. If no tracker has been provided, write the
same body to `.scratch/questionnaire-<slug>.md`. Report the link or path. Done when
every deferred question is in the document with its owner and your recommended
answer.

Resume when the user says the answers are in, whether this session is still open
or a fresh one picked the issue up. Take the settled list and `GLOSSARY.md` as
decided and ask none of it again. The answers are a round: recompute the frontier
and ask the next one. An answer that contradicts a settled decision reopens that
branch: name the conflict and put it to the user. Then stop as above.
