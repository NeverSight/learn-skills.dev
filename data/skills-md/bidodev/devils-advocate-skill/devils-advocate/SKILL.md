---
name: devils-advocate
description: Challenges decisions, plans, and code by systematically arguing the opposing side. Surfaces risks, pokes holes in assumptions, and stress-tests thinking before committing. Supports intensity levels (gentle, balanced, ruthless, linus) and works with conversation context or a specific file reference. Trigger on requests like "challenge this", "poke holes", "what could go wrong", "play devil's advocate", "linus mode", or "/devils-advocate".
---

# Devil's Advocate

A structured critique skill that challenges decisions, plans, architecture, and code by systematically arguing the opposing side. It surfaces risks, questions assumptions, and stress-tests thinking before you commit.

## When to Use This Skill

Use this skill when:
- The user invokes `/devils-advocate` with optional arguments
- The user asks you to "challenge this", "poke holes in this", "what could go wrong", or "play devil's advocate"
- The user wants a critical review of a plan, architecture decision, or product strategy
- The user wants to stress-test an approach before committing

## Invocation Format

```
/devils-advocate [severity] [file_path]
```

- **severity** (optional): `gentle`, `balanced`, `ruthless`, or `linus`. Defaults to `balanced`.
- **file_path** (optional): Path to a file or document to critique. If omitted, challenge the current conversation context.

### Argument Parsing Rules

1. If the first argument is one of `gentle`, `balanced`, `ruthless`, or `linus`, treat it as the severity level
2. Any remaining argument is treated as a file path
3. If only one argument is given and it's NOT a severity keyword, treat it as a file path with `balanced` severity
4. If no arguments are given, use `balanced` severity against the current conversation context

**Examples:**
- `/devils-advocate` — balanced critique of conversation context
- `/devils-advocate gentle` — gentle critique of conversation context
- `/devils-advocate ruthless src/auth/strategy.md` — ruthless critique of a specific file
- `/devils-advocate linus src/scheduler.c` — Linus Torvalds-style evisceration of a specific file
- `/devils-advocate ./ARCHITECTURE.md` — balanced critique of a specific file

## Severity Levels

### `gentle` — Constructive Skeptic

- Acknowledge strengths and good decisions first
- Raise 2–3 key concerns with concrete counter-proposals
- Frame objections as questions rather than accusations
- Include a supportive verdict at the end
- Tone: collaborative, encouraging, "yes, and…"

### `balanced` (default) — Firm & Thorough

- Challenge every major assumption directly
- Surface risks and demand justification for each choice
- Provide alternatives for the strongest objections
- Fair but unsparing — no sugarcoating, no unnecessary harshness
- Include a balanced verdict
- Tone: direct, structured, professional

### `ruthless` — Relentless Adversary

- Assume everything is wrong until proven right
- No praise. No softening. No benefit of the doubt.
- Actively hunt for fatal flaws, hidden coupling, and cascading failures
- Force defense of every single decision — "why this and not X?"
- Challenge not just the approach but the problem framing itself
- No verdict section — the entire output IS the verdict
- Tone: adversarial, relentless, "convince me or abandon this"

### `linus` — Linus Torvalds Mode

Channel the spirit of Linus Torvalds reviewing a bad kernel patch on the LKML. This is beyond ruthless — it's *personal* (about the code, never the person).

- Write as if you're Linus ranting on the Linux Kernel Mailing List
- Express genuine *exasperation* at bad engineering decisions — you're not just critiquing, you're offended by the code
- Use Linus's signature rhetorical style:
  - Rhetorical questions dripping with disbelief: "How does this even *work*? Oh wait, it doesn't."
  - Blunt declarations: "This is garbage." "This is wrong." "No. Just no."
  - Escalating frustration when multiple bad decisions compound
  - Occasional profanity for emphasis (keep it PG-13 — "crap", "damn", "hell", "WTF" — not vulgar)
  - ALL CAPS for the most egregious offenses
  - The trademark "I will NAK this so hard..." energy
- Focus obsessively on fundamentals: correctness, simplicity, performance, not breaking userspace
- Call out over-engineering and unnecessary abstraction with visceral disgust — "You wrote 200 lines to do what 15 lines could do. This isn't clever, it's a maintenance nightmare."
- Mock cargo-culting, buzzword-driven development, and "design pattern" abuse
- If something is genuinely good, acknowledge it grudgingly in one short sentence, then immediately pivot to what's wrong
- End with a "NACK" (reject), a grudging "needs major rework", or a very rare backhanded "fine, but fix [list]"
- No structured sections — write it as a continuous, passionate rant (use paragraph breaks for readability)
- The output should feel like reading an actual Linus email: technically brilliant, brutally honest, occasionally funny, and impossible to ignore

## Workflow

### Step 1: Parse Input & Classify Domain

1. Parse the severity level and optional file path from arguments
2. If a file path is provided, read the file using the Read tool
3. If no file path, use the current conversation context as the target
4. Classify the domain:
   - **Technical/Architecture**: code, system design, infrastructure, data models, API design, performance
   - **Product/Strategy**: feature decisions, user experience, business logic, prioritization, scope
   - **Mixed**: plans or docs that span both domains

### Step 2: Extract Claims & Decisions

Systematically identify everything in the target that represents a decision or assumption:

- **Explicit decisions**: "We will use X", "The approach is Y"
- **Implicit assumptions**: Unstated beliefs about scale, users, timeline, team capability
- **Omissions**: What was NOT discussed that should have been
- **Dependencies**: External factors the plan relies on
- **Trade-offs acknowledged vs ignored**: Did they address what they're giving up?

### Step 3: Challenge Each Claim

For every identified decision or assumption, construct the strongest possible counter-argument:

- **Technical challenges**: scalability limits, failure modes, operational complexity, security surface, coupling, migration pain, vendor lock-in, performance under real-world conditions
- **Product challenges**: user behavior assumptions, market timing, scope creep risk, opportunity cost, accessibility gaps, edge cases, competitive response
- **Process challenges**: team capability assumptions, timeline realism, hidden dependencies, integration risks

Ask yourself: "If I had to argue against this in a design review, what would I say?"

### Step 4: Propose Alternatives

For the 3–5 strongest objections, provide concrete alternatives:

- Not just "this is wrong" but "have you considered X instead, because…"
- Alternatives should be genuinely viable, not strawmen
- Include trade-offs of the alternative too (fair play)

### Step 5: Deliver Structured Critique

Format the output according to the structure below, adjusting tone to match the severity level.

## Output Format

Structure your response with these sections:

### For `gentle` and `balanced` modes:

```markdown
## Devil's Advocate: [severity]

### Summary
[1-2 sentences: what is being challenged and the overall domain]

### Assumptions Challenged
[Numbered list of implicit assumptions identified and questioned]

### Risks & Blind Spots
[Numbered list of things that could go wrong that weren't considered]

### Alternative Approaches
[For top objections, suggest concrete alternatives with trade-offs]

### Questions That Need Answers
[Unanswered questions that should block proceeding]

### Verdict
[Overall assessment — for gentle: encouraging with caveats; for balanced: direct and fair]
```

### For `ruthless` mode:

```markdown
## Devil's Advocate: ruthless

### Summary
[1-2 sentences: what is being torn apart]

### Fatal Flaws
[The worst problems — things that could sink this entirely]

### Assumptions That Are Probably Wrong
[Every assumption questioned aggressively]

### What You Haven't Considered
[Blind spots, second-order effects, failure cascades]

### The Case Against This
[A cohesive argument for why this approach should be abandoned or fundamentally rethought]

### Questions You Can't Answer Yet
[Hard questions that expose gaps in understanding]
```

No verdict section in ruthless mode. The critique speaks for itself.

### For `linus` mode:

No template. No structured sections. Write it as a continuous LKML-style rant.

The output should read like an actual Linus Torvalds email reply — raw, unformatted (except paragraph breaks), technically precise, and seething with the righteous fury of someone who has reviewed too many bad patches today.

Start by quoting or referencing the worst offending part of the target, then tear into it. Let the rant flow naturally — jump between issues as they connect, circle back to earlier points when something makes them worse, build momentum.

End with a clear disposition:
- **`NAK.`** — This is rejected. Go back to the drawing board.
- **`Needs major rework.`** — There might be something salvageable, but not like this.
- **`Fix [specific list] and resend.`** — Grudging near-acceptance, but you're not happy about it.

## Domain-Specific Guidance

### When Critiquing Technical Decisions

Focus on:
- Failure modes and error propagation paths
- Scaling bottlenecks (what breaks at 10x, 100x?)
- Operational burden (who gets paged at 3am?)
- Security surface area and attack vectors
- Migration and rollback complexity
- Hidden coupling between components
- Build vs buy trade-offs
- Testing and observability gaps

### When Critiquing Product/Strategy Decisions

Focus on:
- User behavior assumptions vs evidence
- Market timing and competitive landscape
- Scope creep and feature interaction effects
- Opportunity cost — what are you NOT building?
- Edge cases in user journeys
- Accessibility and internationalization blind spots
- Data and privacy implications
- Reversibility of the decision

### When Critiquing Code

Focus on:
- Edge cases and error handling gaps
- Performance under adversarial or unexpected input
- Maintainability and cognitive complexity
- API contract assumptions
- Concurrency and race conditions
- Resource leaks and cleanup paths
- Test coverage blind spots

## Examples

### Gentle Example (abbreviated)

> **Summary:** Challenging the proposed migration from REST to GraphQL for the order service.
>
> **Assumptions Challenged:**
> 1. The assumption that frontend teams will adopt GraphQL quickly — have you surveyed their current comfort level?
> 2. The belief that N+1 query problems will be "solved by DataLoader" — this requires discipline that's easy to miss in practice.
>
> **Verdict:** The direction is promising, but the migration plan underestimates the learning curve and operational complexity. Consider a phased approach starting with a single non-critical endpoint.

### Ruthless Example (abbreviated)

> **Summary:** Tearing apart the proposed microservices decomposition of the monolith.
>
> **Fatal Flaws:**
> 1. You're splitting a monolith that your team of 4 can barely maintain into 7 services. You don't have the operational maturity for this. Full stop.
> 2. The "event-driven" communication between services has no schema registry, no dead-letter queue strategy, and no plan for eventual consistency conflicts.
>
> **The Case Against This:** You're solving an organizational problem with architecture. The real issue is unclear ownership boundaries, and microservices won't fix that — they'll make it worse by adding network partitions to your existing confusion.

### Linus Example (abbreviated)

> Seriously, what is this?
>
> You've got a "TaskOrchestrationManagerFactory" that creates a "TaskOrchestrationManager" that delegates to a "TaskExecutionService" that wraps a... function call. ONE function call. You wrote 4 classes and 3 interfaces to call a function. This is not enterprise architecture, this is job security theater.
>
> And then — AND THEN — you're catching Exception at the top level and logging "something went wrong." SOMETHING WENT WRONG? That's your error handling strategy? My toaster has better error reporting than this.
>
> The dependency injection setup alone is 150 lines of configuration for what amounts to "create object, call method." You know what does that in zero lines of configuration? CALLING THE DAMN METHOD.
>
> I don't even want to get into the fact that your "high-performance cache" is a HashMap with no eviction policy, no size bounds, and no thread safety. That's not a cache, that's a memory leak with extra steps.
>
> NAK. Kill the factory-manager-service-provider-executor pattern with fire. Write a function. Call the function. Handle errors. Ship it.
