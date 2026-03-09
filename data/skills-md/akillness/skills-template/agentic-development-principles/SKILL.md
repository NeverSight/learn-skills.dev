---
name: agentic-development-principles
description: Universal principles for agentic development when collaborating with AI agents. Defines divide-and-conquer, context management, abstraction level selection, and an automation philosophy. Applicable to all AI coding tools.
allowed-tools: Read Write Bash Grep Glob
metadata:
  tags: agentic-development, principles, context-management, automation, ai-collaboration, universal
  platforms: Claude, ChatGPT, Gemini
  version: 1.0.0
  source: Claude Code Complete Guide - 70 tips (ykdojo + Ado Kukic), generalized
---


# Agentic development principles (Agentic Development Principles)

> **"AI is the copilot; you are the pilot"**
> AI agents amplify the developer's thinking and take over repetitive work, but final decision-making authority and responsibility always remain with the developer.

## When to use this skill

- When starting a collaboration session with an AI agent
- When deciding an approach before starting a complex task
- When establishing a context management strategy
- When reviewing workflows to improve productivity
- When onboarding teammates on how to collaborate with AI
- When applying baseline principles while adopting a new AI tool

---

## Principle 1: Divide and conquer (Divide and Conquer)

### Core concept
AI performs much better with **small, clear instructions** than with large, ambiguous tasks.

### How to apply

| Wrong example | Right example |
|----------|----------|
| "Build me a login page" | 1. "Create the login form UI component" |
| | 2. "Implement the login API endpoint" |
| | 3. "Wire up the authentication logic" |
| | 4. "Write test code" |
| "Optimize the app" | 1. "Analyze performance bottlenecks" |
| | 2. "Optimize database queries" |
| | 3. "Reduce frontend bundle size" |

### Practical pattern: staged implementation

```
Step 1: Design and validate the model/schema
Step 2: Implement core logic (minimum viable functionality)
Step 3: Connect APIs/interfaces
Step 4: Write and run tests
Step 5: Integrate and refactor
```

### Validation points
- [ ] Can each step be validated independently?
- [ ] If it fails, can you fix only that step?
- [ ] Is the scope clear enough for the AI to understand?

---

## Principle 2: Context is like milk (Context is like Milk)

### Core concept
Context (the AI's working memory) should always be kept **fresh and compact**.
- Old and irrelevant information reduces AI performance
- Context drift: mixing multiple topics can reduce performance by up to 39% (research)

### Context management strategies

#### Strategy 1: Single-purpose conversation
```
Session 1: Work on the authentication system
Session 2: Work on UI components  
Session 3: Write test code
Session 4: DevOps/deployment work
```
- Do not mix multiple topics in a single conversation
- Start a new session for a new topic

#### Strategy 2: HANDOFF.md technique
When the conversation gets long, summarize only the essentials and hand them to a new session:

```markdown
# HANDOFF.md

## Completed work
- ✅ Implemented user authentication API
- ✅ Implemented JWT token issuance logic

## Current status
- Working on token refresh logic

## Next tasks
- Implement refresh tokens
- Add logout endpoint

## Tried but failed
- Failed to integrate Redis session store (network issue)

## Cautions
- Watch for conflicts with existing session management code
```

#### Strategy 3: Monitor context state
- When the conversation gets long, ask the AI to summarize the current state
- If needed, reset the conversation and restart using HANDOFF.md

#### Strategy 4: Optimization metrics
| Metric | Recommended value | Action |
|------|---------|------|
| Conversation length | Keep to a reasonable level | Create HANDOFF.md if it gets long |
| Topic count | 1 (single purpose) | Use a new session for new topics |
| Active files | Only what's needed | Remove unnecessary context |

---

## Principle 3: Choose the right abstraction level

### Core concept
Choose an appropriate abstraction level depending on the situation.

| Mode | Description | When to use |
|------|------|----------|
| **Vibe Coding** | High level (see only overall structure) | Rapid prototyping, idea validation, one-off projects |
| **Deep Dive** | Low level (go line-by-line) | Bug fixes, security review, performance optimization, production code |

### In practice

```
When adding a new feature:
1. High abstraction: "Create a user profile page" → understand overall structure
2. Medium abstraction: "Show the validation logic for the profile edit form" → review a specific feature
3. Low abstraction: "Explain why this regex fails email validation" → detailed debugging
```

### Abstraction level selection guide
- **Prototype/PoC**: Vibe Coding 80%, Deep Dive 20%
- **Production code**: Vibe Coding 30%, Deep Dive 70%
- **Bug fixes**: Deep Dive 100%

---

## Principle 4: Automation of automation (Automation of Automation)

### Core concept
```
If you've repeated the same task 3+ times → find a way to automate it
And the automation process itself → automate that too
```

### Automation level evolution

| Level | Approach | Example |
|-------|------|------|
| 1 | Manual copy/paste | AI output → copy into terminal |
| 2 | Terminal integration | Use AI tools directly |
| 3 | Voice input | Voice transcription system |
| 4 | Automate repeated instructions | Use project config files |
| 5 | Workflow automation | Custom commands/scripts |
| 6 | Automate decisions | Use Skills |
| 7 | Enforce rules automatically | Use hooks/guardrails |

### Checklist: identify automation targets
- [ ] Do you run the same command 3+ times?
- [ ] Do you repeat the same explanations?
- [ ] Do you often write the same code patterns?
- [ ] Do you repeat the same validation procedures?

### Automation priority
1. **High**: tasks repeated daily
2. **Medium**: tasks repeated weekly (or more)
3. **Low**: tasks repeated about once a month

---

## Principle 5: Balance caution and speed (Plan vs Execute)

### Plan mode (Plan Mode)
Analyze without executing; execute only after review/approval

**When to use:**
- A complex task you're doing for the first time
- A large refactor spanning multiple files
- Architecture changes
- Database migrations
- Hard-to-roll-back work

### Execute mode (Execute Mode)
AI directly edits code and runs commands

**When to use:**
- Simple, clear tasks
- Work with well-validated patterns
- Sandbox/container environments
- Easy-to-revert work

### Recommended ratio
- Plan mode: **70-90%** (use as the default)
- Execute mode: **10-30%** (only in safe environments)

### Safety principles
- ⚠️ Auto-running dangerous commands only in isolated environments
- Always back up before changing important data
- Always use plan mode for irreversible work

---

## Principle 6: Verify and reflect (Verify and Reflect)

### How to verify output

1. **Write test code**
   ```
   "Write tests for this function. Include edge cases too."
   ```

2. **Visual review**
   - Review changed files via diff
   - Revert unintended changes

3. **Draft PR / code review**
   ```
   "Create a draft PR for these changes"
   ```

4. **Ask for self-verification**
   ```
   "Review the code you just generated again.
   Validate every claim, and summarize the verification results in a table at the end."
   ```

### Verification checklist
- [ ] Does the code work as intended?
- [ ] Are edge cases handled?
- [ ] Are there any security vulnerabilities?
- [ ] Are tests sufficient?
- [ ] Are there any performance issues?

### Reflection questions
- What did you learn in this session?
- What could you do better next time?
- Were there repetitive tasks you could automate?

---

## Quick Reference

### Six principles summary

| Principle | Core | Practice |
|------|------|------|
| 1. Divide and conquer | Small, clear units | Split into independently verifiable steps |
| 2. Context management | Keep it fresh | Single-purpose conversations, HANDOFF.md |
| 3. Abstraction choice | Depth per situation | Adjust Vibe ↔ Deep Dive |
| 4. Automation² | Remove repetition | Automate after 3 repetitions |
| 5. Plan/execute balance | Caution first | Plan 70-90%, execute 10-30% |
| 6. Verification/reflection | Check outputs | Tests, reviews, self-verification |

### Mastery rule
> "To truly master AI tools, you need to use them enough"

Learning by using is key - theory alone is not enough; you need to experience different situations in real projects.

### Golden rule
```
When instructing an AI:
1. Clearly (Specific)
2. Step-by-step (Step-by-step)
3. Verifiable (Verifiable)
```

---

## Best Practices

### DO (recommended)
- Focus on one clear goal per conversation
- Regularly clean up context
- Plan before complex work
- Always verify outputs
- Automate repetitive work

### DON'T (prohibited)
- Handle multiple unrelated tasks in one conversation
- Keep working with a bloated context
- Auto-run dangerous commands carelessly
- Use AI output as-is without verification
- Repeat the same work without automating it

---

## References

- [Anthropic Claude Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [ykdojo claude-code-tips](https://github.com/ykdojo/claude-code-tips)
- [Ado's Advent of Claude](https://adocomplete.com/advent-of-claude-2025/)
- [OpenAI Best Practices](https://platform.openai.com/docs/guides/prompt-engineering)
