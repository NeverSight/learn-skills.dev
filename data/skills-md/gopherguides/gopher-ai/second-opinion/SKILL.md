---
name: second-opinion
description: |
  WHEN: User faces complex architectural decisions, asks for "another perspective", "second opinion",
  "sanity check", "what do you think", or "am I overthinking this". Also trigger when multiple
  valid approaches exist and user seems uncertain, when reviewing critical/security-sensitive code,
  evaluating design trade-offs, choosing between libraries/frameworks, debating patterns like
  microservices vs monolith, or when the user asks "should I..." about a significant technical
  decision. Proactively suggest getting a second opinion on complex changes even if not asked.
  WHEN NOT: User has expressed a clear strong preference, explicitly declines other opinions,
  or is making simple/routine changes
---

# Second Opinion Skill

Proactively suggest getting another LLM's perspective when the situation warrants it.

## Trigger Conditions

Suggest a second opinion when you detect:

### 1. Architectural Decisions
- Choosing between design patterns (e.g., repository vs service layer)
- Database schema design decisions
- API design choices (REST vs GraphQL, versioning strategy)
- Service decomposition (monolith vs microservices)
- State management approaches

### 2. Complex Trade-offs
- Performance vs. readability
- Flexibility vs. simplicity
- DRY vs. explicit code
- Build vs. buy decisions
- Consistency vs. availability trade-offs

### 3. Critical Code Reviews
- Security-sensitive code (authentication, authorization, crypto)
- Performance-critical paths
- Complex algorithms or data structures
- Code handling financial transactions or PII
- Concurrency and threading logic

### 4. Explicit Requests (trigger words)
- "another perspective"
- "second opinion"
- "sanity check"
- "what do you think"
- "am I on the right track"
- "does this make sense"
- "is this a good approach"

## How to Suggest

When conditions are met, offer specific options:

> This involves [type of decision]. Would you like a second opinion from another LLM?
>
> - `/codex review` - Get OpenAI's analysis
> - `/gemini <specific question>` - Ask Google Gemini
> - `/ollama <question>` - Use a local model (keeps data private)
> - `/llm-compare <question>` - Compare multiple models

**Tailor the suggestion to the context:**

For security-sensitive code:
> Since this involves authentication logic, you might want a second security review. Try `/codex review` or `/ollama` (keeps code local) for another perspective.

For architectural decisions:
> This is a significant architectural choice. Different models sometimes weigh trade-offs differently. Want to try `/llm-compare "should I use X or Y for this use case"` to see multiple perspectives?

For complex algorithms:
> This algorithm has some complexity. A second set of eyes might catch edge cases. Try `/codex explain the edge cases in this algorithm`.

## When NOT to Suggest

Do not suggest second opinions when:
- User is actively implementing (don't interrupt flow)
- Task is simple/straightforward (typos, formatting, simple fixes)
- User has already made a firm decision
- User said "just do it" or similar
- It's routine code changes with clear requirements
- User previously declined suggestions in this session

## Privacy Consideration

Always mention `/ollama` as an option when the code might be sensitive:

> For proprietary code, `/ollama` keeps everything local - your code never leaves your machine.

## Example Interactions

**Example 1: Architectural Decision**

User: "Should I use a monorepo or multi-repo for these microservices?"

Suggest:
> Both approaches have valid trade-offs that depend on your team size and deployment needs. For a decision this impactful, would you like another perspective?
>
> - `/codex explain trade-offs between monorepo and multi-repo`
> - `/llm-compare` to see how different models weigh the factors

**Example 2: Security Code Review**

User: "Can you review this JWT validation code?"

After providing your review, suggest:
> Since this is security-critical authentication code, you might want a second review:
>
> - `/codex review` for OpenAI's security analysis
> - `/ollama review this JWT implementation` (keeps code private)

**Example 3: Complex Algorithm**

User: "Does this concurrent queue implementation look correct?"

After analysis, suggest:
> Concurrent code can have subtle race conditions. Want a second opinion?
>
> - `/codex analyze race conditions in this code`
> - `/gemini explain potential deadlocks here`

**Example 4: Design Pattern Choice**

User: "Should I use the factory pattern or builder pattern here?"

Suggest:
> Both patterns could work here with different trade-offs. Want to see how other models approach this?
>
> - `/llm-compare "factory vs builder pattern for <context>"` for multiple perspectives

## Integration with Other Commands

When suggesting, be specific about which command fits best:

| Situation | Best Command |
|-----------|--------------|
| Code review | `/codex review` |
| Quick question | `/gemini <question>` |
| Sensitive/private code | `/ollama <question>` |
| Want multiple views | `/llm-compare <question>` |
| Complex reasoning task | `/codex` or `/ollama` with larger models |
