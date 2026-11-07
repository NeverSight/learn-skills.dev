---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.
metadata:
  credits:
    - skill: grilling
      author: Matt Pocock
      url: "https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md"
---

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Put the whole frontier in one round, in the [round format](#round-format). Then wait for the user's answers before the next round.

The first round always includes the **premise**: should this exist at all, and do the inputs it inherits (a research recommendation, an earlier assumption, the ticket's own wording) still hold? A research recommendation is an input to a decision, never the decision.

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

## Who decides

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), dispatch a sub-agent to find it; don't ask the user for anything you could look up yourself. Don't block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait for the sub-agent to report; ask the rest of the frontier now.

Sort every frontier item into one of three kinds:

- **Derived**: a source already answers it: a prototype, a closed ticket, a doc, or what the code does today. Read the primary artifact (the prototype's source and seed data, the code), not a summary of it. Today's behaviour stands unless the task asks to change it. Deviating from a source is a decision for the user, with the reason.
- **Defaulted**: internal, reversible, consistent with existing patterns, cheap to change, and free of product, data, security, cost, or compatibility consequences. Pick the default yourself.
- **Decision for the user**: anything that changes product behaviour or visible UX (copy included), a domain term, data meaning or schema, permissions, security, cost, or compatibility; anything destructive or expensive to reverse; anything that needs authority, credentials, or information only the user has. When unsure, it is a decision for the user.

Derived and defaulted items still go in front of the user, under 🤖, so they can overturn any of them.

## Round format

Every round uses exactly these sections, in this order, under these headers. Leave out an empty section. Every question in the round is a 🧭 item; the rest of the message states facts and defaults.

```markdown
### 🧭 Decisions for you

🧭 **D1** - **<decision title>**: <question, worded so "yes" accepts the default>

- **a)** <option>
- **b)** <option>

✅ **Default** - <your recommended answer>

🔐 **Why you** - <the boundary it crosses: product, UX, domain term, data, permissions, security, cost, compatibility, irreversibility, authority, or knowledge only the user has>

---

🧭 **D2** - ...

### 🤖 Decided without you

<show-me view>

### ⏳ Still looking up

- <running lookup> → gates <what it unblocks>
```

Keep the blank lines exactly as shown: Markdown joins lines separated by a single line break into one paragraph, so without them ✅ and 🔐 run on after the question. ✅ and 🔐 each start their own line. When a decision has several options, list each as its own `a)`, `b)`, … bullet and name the letter in ✅; leave the list out for a plain yes/no question.

Send the round as the last message of your turn, with nothing after it. Anything you post later (a follow-up, a reply to a hook) pushes the round into the collapsed work log, where the user won't see it. Ask in the message text, not in a question dialog that covers the rest of the round.

Number 🧭 items `D1`, `D2`, … across the whole session, never restarting per round, so an answer like "D4: no" is unambiguous.

For 🤖, call the Skill tool with "show-me" and render every derived and defaulted item in the smallest view that fits. Usually that is a table of `A1`, `A2`, … with the decision and its source (a file, a ticket, a prototype screen, or `default: <reason>`); a tree or diff fits better when the items shape a structure. The user overturns an item by its id, and an overturned item becomes a 🧭 item next round.

## Done

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Close with one message:

```markdown
### ✅ Shared understanding

<show-me view of every settled decision and who settled it: the user, a source, or your default>
```

Do not act on it until the user confirms you have reached a shared understanding.
