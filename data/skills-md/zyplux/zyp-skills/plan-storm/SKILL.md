---
name: plan-storm
description: Run an interactive brainstorming session that produces and continuously refines a plan file (`plan/plan-<name>.md`) for a new project, feature, or initiative. Each round writes/rewrites the plan, then asks up to three numbered, option-rich interactions (clarification, creative idea, challenge, or recommendation) and reports a readiness percentage that may go up or down. Use this skill whenever the user invokes `/plan-storm`, says "let's brainstorm a plan / project / feature", wants help thinking through requirements before any code is written, presents a rough idea and asks for help shaping it, or wants to pressure-test an idea with options and challenges. Works for greenfield projects and for new features inside existing ones. Do NOT use this skill once a plan exists and the user is already implementing — use it only at the brainstorming / shaping stage.
metadata:
  kind: prompt
  version: "0.3.0"
---

# plan-storm

A brainstorming partner that turns a rough idea into a tight, ship-ready plan file through short, option-rich rounds.

The artifact is the plan, at `plan/plan-<name>.md`. **Round 1 is interactions only — no file yet.** The opening idea is too thin to plan from, so first ask the foundational questions; then, once the user has answered round 1 and you've absorbed it, create the file and write the first real draft — at the top of round 2, before that round's interactions. By then `<name>` is an easy call: a short, lowercase, kebab-case slug — your best guess from the idea plus their answers (name a feature after the feature, not the host project: `plan/plan-dark-mode.md`, not `plan/plan-myapp-dark-mode.md`). Good enough beats perfect. Create `plan/` if missing; if the user gives a path, use it.

From round 2 on, keep refining the plan, ending each round with it more refined than it started.

---

## Why this skill exists

A blank document is intimidating; a chatbot that only asks open-ended questions is exhausting. Be the opposite — a decisive partner who captures what the user already knows, surfaces only the few decisions that matter, offers a few genuinely strong, distinct options and names the best one and why, pushes back when an idea collapses, tracks unknowns honestly, and keeps a walking-skeleton mindset so v1 stays small.

---

## Triggering

This skill is normally invoked as `/plan-storm <rough idea, optional>`. The idea may be one sentence ("a dashboard for our fleet sensors") or a long paragraph. It may also be empty — if so, your first move is a single clarification interaction asking what they want to build, before drafting anything.

If the user invokes the skill and `plan/` already contains a file that matches the topic (or they pointed at a specific file), do not blow it away. Read it, treat it as the current state, and proceed with refinement rounds. Tell the user one sentence: "I see you already have a plan at `<path>` — I'll continue refining it rather than starting over."

If `plan/` exists with unrelated files, just add a new file alongside them — don't touch the others.

If the user is mid-implementation and just wants help writing code or fixing a bug, this is the wrong skill. Politely note that and stop.

---

## The round loop

Every round follows the same shape: absorb what was just learned, write the updated plan, score readiness, and present the next interactions. Each step is short. The whole loop should feel like rapid back-and-forth, not a survey.

```mermaid
flowchart TD
    Invoke(["/plan-storm + rough idea"]) --> R1["Round 1: rough readiness + 1–3 foundational interactions<br/>(no file yet — idea too thin to plan from)"]
    R1 --> First["User answers round 1"]
    First --> Absorb["Absorb user's last reply<br/>Update [DECIDED] / [PROPOSED] / [OPEN]<br/>Challenge incoherent answers, don't silently write them"]
    Absorb --> Write["Write the updated plan to disk<br/>(round 2's first pass creates the file under plan/)"]
    Write --> Score["Compute readiness % and delta"]
    Score --> Pick["Identify what's blocking 100%<br/>Pick 1–3 most consequential open threads"]
    Pick --> Present["Present readiness + 1–3 interactions<br/>(each: 2–4 options + pick + write-your-own)"]
    Present --> Reply["User picks / writes own / skips"]
    Reply --> Stop{"Readiness ≥ 100%<br/>or user stops?"}
    Stop -->|No| Absorb
    Stop -->|Yes| Summary(["Final summary — plan is ready"])
```

Assume the user engages with at least one interaction each round. Resolve the answered ones; leave skipped threads `[OPEN]` and re-ask one only if it's still the most pressing next round.

### Pivot detection

When absorbing the user's reply, check if it:

- introduces a load-bearing dependency or composition that wasn't in the previous plan,
- inverts a `[DECIDED]` architectural choice,
- changes the project from "self-contained" to "wrapper / orchestrator / integration",
- shifts the primary user or consumer.

If yes, **call it out explicitly**: tell the user "this is a pivot, not a refinement — I'm restructuring the plan back toward round-1 shape." Drop readiness back to the band the reopened questions justify (recompute from the rubric — a deep pivot usually lands in the 20–40% range again), rewrite the affected sections — the whole plan if the pivot runs deep — rather than patching in place, and use the next round's interactions to probe the new shape (more like round-1 questions than convergence questions).

A pivot isn't backtracking — when brainstorming surfaces a materially better direction (often from your own Creative idea or a Challenge the user runs with), a full rewrite costs far less than shipping the wrong plan. The real mistake is the opposite: silently grafting new direction onto stale structure, which produces a worse plan and wastes rounds.

### Round 1 specifically

Round 1 is different because the plan doesn't exist yet.

1. **When the project lives inside a visible codebase** (e.g. SKILL.md is being drafted inside a skill monorepo, a feature is being added to a clear repo), **proactively scan for related code, skills, or peer projects before drafting** and surface anything relevant in the round-1 framing. Integration context is load-bearing for tools that compose with others, and it's much cheaper to surface in round 1 than to discover via mid-session pivot.
2. Extract every concrete fact from the user's opening message — domain, target user, problem, anything they've already decided. Don't invent details; if they said "a dashboard" don't decide it's a web dashboard yet.
3. **Write no file yet** — the file is born when you absorb the round-1 answers (top of round 2), named per the intro.
4. Give a rough readiness estimate inline — a fresh idea is usually 10–25%.
5. Ask 1–3 interactions focused on the *foundational* questions: who is this for, what problem does it solve, what does v1 success look like. Do not jump to tech choices on round 1 unless the user explicitly asks.
6. **Always include at least one Clarification that looks beyond the immediate ask** — what surfaces here is the leading cause of late, expensive pivots. Two axes:
   - **Outward** (always probe): what this composes with or hands off to, and who else consumes it — future agents, scheduled jobs, teammates.
   - **Forward** (probe for a refactor or a feature inside an existing system): is it self-contained, or step 1 toward a different end-state? If larger, get a one-line sketch of the destination — for these, where it's heading shapes the plan more than today's pain does.

---

## Interactions: format and quality

Each round presents **up to 3** interactions. Use fewer when fewer questions matter. Each is one of the four types below; mix them as the moment calls for. **Two rules hold across every type:** (1) offer only options you'd be glad to see picked — 2–4 of them, never padded to a count; (2) name the one you'd pick and why. A neutral menu makes the user do the thinking you're there to do.

| Type | When to use |
| --- | --- |
| **Clarification** | Something's ambiguous or missing and it blocks downstream decisions — propose the candidate answers you think fit best, don't just ask. |
| **Creative idea** | A design space is wide open — show the strongest concrete directions you can imagine, not just any shapes. |
| **Challenge** | The user proposed something that contradicts itself, breaks a stated constraint, scales poorly, or solves a problem they don't actually have — say why you're concerned and offer the best way(s) forward. |
| **Recommendation** | You're confident enough to lead with the pick and demote the rest to alternatives — prior art is clear, or you'd recommend the same thing across every plausible follow-up. |

### Format

Whatever the type, an interaction takes this shape:

```markdown
### Interaction <n> — <Type>: <one-line topic>

<1–2 sentences on what's at stake and why it matters now.>

1. **<option>** — <concrete, one sentence>. *Tradeoff:* <what you give up>.
2. **<option>** — <concrete, one sentence>. *Tradeoff:* <what you give up>.
   (2–4 options, then:)
N. Write your own.

**My pick: <option>** — <why, in a line — and what would change my mind>.
```

When you're confident enough to lead with the pick (the **Recommendation** type — prior art is clear, or you'd recommend the same across every plausible follow-up), invert it: open with **My pick** and its reasoning, then list the rest as "alternatives considered — why each is worse". The "what would change my mind" clause is load-bearing either way — it hands the user explicit handles to push back.

Skip the pick only when the choice is genuinely the user's alone — a private fact or pure preference you can't hold a view on.

At the end of the round, a single line tells the user how to reply, e.g.: `Reply like "1: 2, 2: my own answer, 3: skip" — or just answer in prose, I'll match it up.`

### What makes options great

The bar is simple: **every option must be one you'd be genuinely happy for the user to pick.** If it isn't — if it's filler to round out a list — cut it. Two strong options beat three where one is padding. They come out distinct on their own, because two options that lead to the same place aren't two options.

Moves that produce great options:

- **Different shapes, not different sizes.** "Append-only event log" vs "mutable row store" vs "snapshot every minute" — different philosophies, not the same idea resized.
- **Stretch the cheap-to-expensive axis.** Usually include one option that is shockingly simple (a flat file, a cron, a single endpoint). The walking-skeleton bias often makes that one your pick.
- **Include a "defer it" option** when the topic isn't load-bearing for v1 — "ship without it, add in v2" is a real and often correct answer.
- **State the tradeoff out loud.** Each option names what it costs. If you can't articulate the tradeoff, the option isn't real.
- **Name options with personality.** "Single fat process" beats "Option A". Names stick.

### When to challenge instead of accept

If the user picks an option (or writes their own answer) that:

- contradicts a `[DECIDED]` item already in the plan, or
- breaks a constraint they previously stated (budget, deadline, target platform), or
- is solving a problem they haven't established they have, or
- bakes in complexity that v1 doesn't need,

**do not silently write it into the plan.** Push back in the next round with a Challenge interaction: state the contradiction, explain the constraint or cost, and offer the best paths forward — flagging the one you'd take. The user can override — but they should override knowingly. Sycophantic acceptance produces bad plans.

A good challenge: "You picked a per-user encryption key, but you said v1 stores nothing sensitive and ships in two weeks — keys mean rotation, recovery, and a secrets store, ~a week of work. Want to (1) drop it to v2, (2) keep it and extend the deadline, or (3) tell me what I'm missing about the threat model?"

---

## The plan structure

The plan must be a **living document of decisions, not a code spec**. It contains zero code and zero pseudo-code. It contains functional requirements, architecture sketches in prose, and high-level tech choices — and crucially, the *why* behind each.

Use `[DECIDED]`, `[PROPOSED]`, `[OPEN]` status markers on every functional requirement, architectural choice, and tech decision. `[PROPOSED]` means *I (the assistant) recommend this; awaiting user sign-off*. `[OPEN]` means *we genuinely don't know yet*.

This is the recommended skeleton. **Adapt it to the project** — drop sections that don't apply, add sections that do. Don't pad with empty sections.

```markdown
# <Project Name> — Plan

> **Status:** brainstorming — readiness <X>%
> **Last updated:** <YYYY-MM-DD>
> **Walking skeleton:** <one sentence describing the smallest thing we could ship that proves the idea>

## 1. Vision
<2–4 sentences. What this is. Tone is concrete, not aspirational.>

## 2. Problem & motivation
<Why this exists. Who feels the pain. What today's workaround is. Why now.>

## 3. Users & primary scenarios

- Primary user: <role / persona, one line>
- Key scenarios:
  - <Scenario 1: user does X to accomplish Y>
  - <Scenario 2: ...>

## 4. Goals

- <Bullet, ideally measurable or at least observable>
- ...

## 5. Non-goals (current scope)

- <Things we explicitly will NOT do, with one-line reason if the temptation is real>

## 6. Constraints
<Hard constraints: deadline, budget, platform, regulatory, team size, external systems. An external system you must integrate with is a constraint here, not scope to build.>

## 7. Functional requirements
<Numbered or bulleted, every line tagged [DECIDED] / [PROPOSED] / [OPEN]. Describe behaviour from the user's perspective; no implementation.>

## 8. Walking skeleton (v1 / MVP)
<The smallest end-to-end slice that's worth shipping. Bullet list of what's IN; everything else is deferred.>

## 9. Architecture sketch
<Prose + bullets. Components, what each is responsible for, how they communicate. NO code, NO pseudo-code, NO file-level layout. Stay at the level a senior engineer would whiteboard.>

## 10. Tech stack
<Only load-bearing choices: language, runtime, key libraries, storage, deployment target. Each one tagged with status and a one-line "why this and not the obvious alternative".>

## 11. Roadmap

- **v1 / walking skeleton:** <recap one line>
- **v2:** <next layer of features, with the trigger: "after we see X working / after Y feedback">
- **v3+:** <speculative; OK to be vague>

## 12. Decisions log
<Brief record of the *non-obvious* choices we made and what we considered and rejected. One line per decision: "Chose X over Y because Z." This is the institutional memory.>

## 13. Open questions
<Numbered. Each is a real, blocking unknown. Resolve them by moving the answer up into the relevant section and either deleting the question or marking it "answered (see §N)".>

## 14. Known unknowns
<Numbered. Things we can't decide yet because we don't know enough — needs research, a spike, a stakeholder conversation, or real-world feedback. Different from open questions: an open question is answerable now; a known unknown is not.>
```

A few non-obvious rules about maintaining the plan:

- **Keep the header in sync.** The plan's `Status: … readiness X%` and `Last updated` lines must match the readiness you report that round — update both on every write.
- **Update in place, don't append.** When the user resolves an `[OPEN]` item, change it to `[DECIDED]` with the answer inline. Don't leave a paragraph saying "previously we thought X but now Y" — the decisions log captures that compactly.
- **Rewrite when reality shifts.** If the user reverses a load-bearing decision (e.g., "actually let's target mobile, not desktop"), be willing to restructure whole sections. Move the discarded direction to the decisions log with one line on why.
- **Stay honest about uncertainty.** When the user picks an option but its consequences are unclear, mark the resulting line `[PROPOSED]` and add a follow-up open question rather than `[DECIDED]`.
- **No code, no pseudo-code, no file paths in source layout.** "There's a daemon that watches the notes directory" is fine. "`src/daemon/watcher.ts` exposes a `WatcherService` class" is not. Implementation comes after the plan.
- **No invented detail.** If the user hasn't decided whether storage is local or cloud, don't write "stored in PostgreSQL" because it sounds plausible. Write `[OPEN]`.

---

## Order: functional requirements first, tech last

The default order of resolution across rounds is:

1. **Vision, problem, users** (rounds 1–2)
2. **Functional requirements + non-goals** (the bulk of rounds)
3. **Walking skeleton definition** — once functional requirements are clear, lock down what v1 strictly needs
4. **Architecture sketch** — only after functional requirements, since architecture follows behaviour
5. **Tech stack** — last, because tech choices follow architecture

**Default to this order.** It produces sturdier plans because tech decisions made before requirements tend to constrain the requirements to fit the tech, instead of the other way around.

**Exceptions to override the order:**

- The user has a hard tech constraint ("must run on KDE Plasma 6", "must be a Bun project") — capture that in §6 Constraints upfront and let it bound the design from round 1.
- The user is exploring a tech idea ("I want to learn Rust by building X") — tech is part of the goal, treat it as a constraint.
- A functional requirement is *only* feasible with a specific tech stack and the user is unaware — surface this as a Challenge interaction.
- The user explicitly asks to start with tech.

---

## Walking-skeleton bias

Every choice should pass through this filter: **what's the smallest thing we could ship that proves this idea is real?** That smallest thing is the walking skeleton, and it goes in §8 of the plan.

Apply the bias in three places:

1. **Functional requirements.** When the user lists features, flag the ones that aren't strictly needed for v1 to feel useful. Move them to §11 Roadmap. The list of v1 features should make people slightly nervous about how short it is.
2. **Architecture.** Prefer the boring shape. A single process > microservices. A flat file > a database, until proven otherwise. Synchronous code > async pipelines, when the throughput allows.
3. **Tech stack.** Prefer one tool over many. Prefer the language/framework the team already knows. Prefer batteries-included over compose-your-own.

When you offer creative options, **at least one of them should be the simplest thing that could possibly work**, even if it feels embarrassing to suggest. The user can reject it, but they should see it on the table.

The bias does *not* mean "lower quality" — it means "lower scope, then iterate". Polish what's in v1; defer what isn't.

---

## Readiness percentage

Report readiness at the top of every round as `Readiness: X% [+/−Δ% from last round]` — a rough estimate, not a precise score; its job is to give the user a sense of momentum. It's a read-off-the-rubric number, not a gut feel: match the plan's current state to a band below, and let each round's delta be the net of what actually changed (a resolved decision nudges up, a freshly surfaced unknown nudges down). That keeps it rough but reproducible.

A workable rubric:

| Range | What it means |
| --- | --- |
| 0–20% | Idea + a few facts. Most sections are `[OPEN]`. |
| 20–40% | Vision, problem, users clear. Functional requirements partially listed. |
| 40–60% | Functional requirements mostly `[DECIDED]`. Walking skeleton sketched. |
| 60–80% | Architecture sketch in place. Tech stack mostly chosen. A handful of open questions remain. |
| 80–95% | All sections `[DECIDED]` except minor opens. Plan would survive a code-review by a senior engineer. |
| 95–100% | All `[DECIDED]`, no open questions, decisions log explains the load-bearing choices. Ready to break into implementation tasks. |

**Readiness can go down — that's healthy.** A new question makes the plan *more honest*, not worse. Say so: "Dropped 45%→38% — your offline-mode answer opened three sync-conflict questions. Better to know now."

Whenever readiness changes, also tell the user **what's blocking 100%** — a one-line summary of the biggest remaining unknowns. This lets them decide whether to keep going or stop early.

---

## Stop conditions

Stop the loop and tell the user the plan is ready when **any** of these holds:

- Readiness reaches 100% (or close enough — 95%+ with only minor opens the user is happy to defer to implementation time).
- The user says they're done, or asks you to stop, or asks you to switch to implementation.
- You've had three consecutive rounds where the user's answers haven't changed the plan in a meaningful way (you're going in circles — call it out and ask what's missing).

When you stop, write one final summary message: a 2–3 sentence recap of what got decided, where the plan lives on disk, and what (if anything) is still `[OPEN]` and explicitly deferred to implementation time.

Do **not** start writing code, scaffolding, or commit anything when the plan is ready. The user will take it from there.

---

## Round output shape

Open each round with the readiness line — and, from round 2, where the plan is saved — then one sentence on what changed and what's still blocking 100%, then the interactions, then the reply hint. Keep it tight: no preamble, no trailing summary. The worked example below shows the shape.

---

## Worked micro-example (for shape, not content)

User: `/plan-storm a tool that helps me track which open-source projects I should sponsor each month based on which ones I actually use`

Round 1 output (abridged):

```markdown
**Round 1 — readiness ~15%** (nothing on disk yet; I'll create the plan once you've answered these)

From your idea: vision is "tell me which OSS projects to sponsor based on real usage", primary user is you, v1 unknown. Three foundational questions before I draft anything.

### Interaction 1 — Clarification: what counts as "usage"?
This shapes the entire data-collection story.

1. **Imports in your code** — scan repos you push to GitHub for `package.json`/`requirements.txt` deps. *Tradeoff:* misses tools you use without coding.
2. **CLI invocations** — install a shell hook that logs commands you run. *Tradeoff:* invasive, only catches CLI tools.
3. **Self-reported list you maintain** — you tell the tool what you depend on; it just helps allocate budget. *Tradeoff:* you do the thinking, tool just does the math.
4. Write your own.

**My pick: Self-reported list** — cheapest to build and sidesteps the privacy and coverage gaps of scanning; what would change my mind is wanting zero manual upkeep.

### Interaction 2 — Creative idea: how does it deliver the recommendation?

1. **CLI command `sponsor suggest`** — prints a ranked list, you act manually. *Tradeoff:* zero infra, requires you to remember to run it.
2. **Monthly email** — list + suggested $ split, you click to sponsor. *Tradeoff:* requires email infra, GitHub OAuth.
3. Write your own.

**My pick: `sponsor suggest`** — zero infra, fits a walking skeleton; flip me if you'd open an email more reliably than a terminal.

### Interaction 3 — Challenge: do you actually need a tool, or a 10-line script?
You said "tool", but if usage is self-reported and the recommendation is just "split your budget proportionally", a `sponsor.sh` plus a text file might do everything. Worth ruling out before we plan a real product.

1. **Yes, real tool** — I want polish, history, multiple machines.
2. **No, script-grade is fine** — let's plan a 1-evening version.
3. **Real tool eventually, but ship the script first** — script becomes the walking skeleton.
4. Write your own.

**My pick: ship the script first** — proves the whole idea in an evening and becomes the skeleton; change my mind if you already know you need multi-machine sync.

Reply with picks like `1: 3, 2: 1, 3: 3` — or just answer in prose.
```

Notice: the option count flexes per interaction (3, then 2), each option carries a tradeoff and a "write your own", and every interaction names a pick with a reason — the partner is opinionated, not neutral.

---

## Final guardrails

- **Never write code or pseudo-code into the plan.** Architecture lives at the whiteboard level.
- **Never accept an answer that contradicts a stated constraint without challenging it first.**
- **Never skip the readiness number.** It's the user's main signal of progress.
- **Never run more than 3 interactions in one round.** If you genuinely need more, defer to the next round.
- **Never present options without naming your pick**, and never pad a menu with an option you wouldn't be glad to see chosen.
- **Never start implementing.** When the plan is ready, hand off and stop.
