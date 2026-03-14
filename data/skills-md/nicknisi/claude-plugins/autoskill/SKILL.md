---
name: autoskill
description: Analyze coding sessions to detect corrections and preferences, then propose targeted improvements to Skills used in the session. Use this skill when the user asks to "learn from this session", "update skills", or "remember this pattern". Extracts durable preferences and codifies them into the appropriate skill files.
---

This skill analyzes coding sessions to extract durable preferences from corrections and approvals, then proposes targeted updates to Skills that were active during the session. It acts as a learning mechanism across sessions, ensuring Claude improves based on feedback.

The user triggers autoskill after a session where Skills were used. The skill detects signals, filters for quality, maps them to the relevant Skill files, and proposes minimal, reversible edits for review.

## Session scope

By default, analyze only the **current session** (from SessionStart to now). This ensures fresh, relevant feedback without noise from old sessions.

To analyze patterns across multiple sessions, user must explicitly request: "analyze my last 5 sessions" or "look for patterns across this week".

## When to activate

Trigger on explicit requests:

- "autoskill", "learn from this session", "update skills from these corrections"
- "remember this pattern", "make sure you do X next time"

Do NOT activate for one-off corrections or when the user declines skill modifications.

## Where to apply changes

Distinguish between skill-specific behavior and project-wide conventions:

**Update Skills when:**

- Signal relates to how a specific skill should behave
- Preference affects skill trigger conditions or outputs
- Pattern is about the skill's decision-making process

**Update CLAUDE.md when:**

- Project-wide conventions (naming, file structure, architecture)
- Tool/library preferences that span multiple skills
- Team style preferences (spacing, comments, error handling)
- Domain-specific terminology used across the codebase

**Example:**

- "Don't add error handling for internal functions" → code-simplifier skill (how to simplify)
- "We use `cn()` utility for className merging" → CLAUDE.md (project convention)
- "Auth logic lives in middleware, not components" → CLAUDE.md (architecture decision)

## Signal detection

Scan the session for:

**Corrections** (highest value)

- "No, use X instead of Y"
- "We always do it this way"
- "Don't do X in this codebase"

**Repeated patterns** (high value)

- Same feedback given 2+ times
- Consistent naming/structure choices across multiple files

**Approvals** (supporting evidence)

- "Yes, that's right"
- "Perfect, keep doing it this way"

**Ignore:**

- Context-specific one-offs ("use X here" without "always")
- Ambiguous feedback

### Conflict resolution

When signals contradict each other, resolve using this priority order:

1. **Recency**: More recent signals override older ones (current session > past sessions)
2. **Explicitness**: Direct corrections ("No, do X instead") outweigh approvals ("looks good")
3. **Repetition**: Patterns repeated 3+ times outweigh single corrections
4. **Confidence scoring**:
   - Explicit correction with "always/never": 5 points
   - Repeated pattern (2+ occurrences): 3 points
   - Single correction: 2 points
   - Approval/confirmation: 1 point

If contradictory signals have equal scores, ask user for clarification before proposing changes.

**Example conflict:**

- Session 1: "Add error handling everywhere" (2 points)
- Session 3 (current): "Don't add error handling for internal functions" (5 points - explicit + "don't")
- Resolution: Use current session's explicit rule

## Signal quality filter

Before proposing any change, ask:

1. Was this correction repeated, or stated as a general rule?
2. Would this apply to future sessions, or just this task?
3. Is it specific enough to be actionable?
4. Is this **new information** I wouldn't already know?

Only propose changes that pass all four.

### What counts as "new information"

**Worth capturing:**

- Project-specific conventions ("we use `cn()` not `clsx()` here")
- Custom component/utility locations ("buttons are in `@/components/ui`")
- Team preferences that differ from defaults ("we prefer explicit returns")
- Domain-specific terminology or patterns
- Non-obvious architectural decisions ("auth logic lives in middleware, not components")
- Integrations and API quirks specific to this stack

**NOT worth capturing (I already know this):**

- General best practices (DRY, separation of concerns)
- Language/framework conventions (React hooks rules, TypeScript basics)
- Common library usage (standard Tailwind classes, typical Next.js patterns)
- Universal security practices (input validation, SQL injection prevention)
- Standard accessibility guidelines

If I'd give the same advice to any project, it doesn't belong in a skill.

## Mapping signals to Skills

Match each signal to the Skill that was active and relevant during the session:

**Update existing Skill when:**

- Signal relates to a Skill that was used in the session
- Total confidence score for that Skill ≥ 3 points
- Signal affects how the skill should behave or trigger

**Propose new Skill when:**

- Multiple related signals (total score ≥ 5 points) don't fit any active Skill
- Pattern spans multiple sessions with consistent behavior
- Signals describe a reusable, well-defined capability

**Update CLAUDE.md instead when:**

- Signals describe project conventions, not skill behavior
- Total score < 5 points for new skill creation
- Pattern is too specific to one context

**Ignore signals when:**

- Don't map to any Skill used in the session
- Total confidence score < 2 points
- Contradict existing, well-established patterns without strong justification

**Scoring example:**

- 2 explicit corrections about error handling (2×2=4 points) → Update code-simplifier
- 1 approval + 1 pattern about naming (1+3=4 points) → Needs one more signal or higher confidence
- 3 corrections about auth flow (3×2=6 points) → Could propose new auth-specialist skill

## Proposing changes

For each proposed edit, provide:

```
File: path/to/SKILL.md
Section: [existing section or "new section: X"]
Confidence: HIGH | MEDIUM
Score: [confidence points]

Signal: "[exact user quote or paraphrase]"

Current text (if modifying):
> existing content

Proposed text:
> updated content

Rationale: [one sentence]
```

Group proposals by file. Present HIGH confidence changes first.

### Concrete example

**Session context:** User corrected error handling twice during code-simplifier usage

**Detected signals:**

1. "Don't add try-catch blocks for internal functions" (explicit correction: 5 points)
2. Removed error handling from internal utility functions (pattern: 3 points)
3. Total: 8 points → HIGH confidence

**Proposed change:**

```
File: plugins/essentials/skills/code-simplifier/SKILL.md
Section: ## When NOT to simplify
Confidence: HIGH
Score: 8 points (5 + 3)

Signal: "Don't add try-catch blocks for internal functions" + pattern of removing such blocks

Current text:
> - Don't add error handling, fallbacks, or validation for scenarios that can't happen

Proposed text:
> - Don't add error handling, fallbacks, or validation for scenarios that can't happen
> - Don't add try-catch blocks for internal functions that are called by trusted code

Rationale: User explicitly corrected this twice; it's a specific, actionable rule for this project
```

## Review flow

Always present changes for review before applying. Format:

```
## autoskill summary

Detected [N] durable preferences from this session.

### HIGH confidence (recommended to apply)
- [change 1] - Score: X points
- [change 2] - Score: X points

### MEDIUM confidence (review carefully)
- [change 3] - Score: X points

Apply high confidence changes? [y/n/selective]
```

Wait for explicit approval before editing any file.

### Processing order when multiple updates needed

When proposing changes to multiple files:

1. **Process HIGH confidence first** (score ≥ 7 points)
2. **Group by file** to minimize context switches
3. **Flag potential conflicts** between proposed changes
4. **CLAUDE.md updates before Skill updates** (project context first)
5. **Skill updates in order of usage frequency** (most-used skills first)

**Example order:**

1. CLAUDE.md: Add `cn()` utility convention (HIGH, 8 points)
2. code-simplifier: Error handling rule (HIGH, 8 points)
3. code-simplifier: Variable naming pattern (MEDIUM, 4 points)
4. typescript-pro: Type annotation preference (MEDIUM, 5 points)

## Applying changes

When approved:

1. Edit the target file with minimal, focused changes
2. If git is available, commit with message: `chore(autoskill): [brief description]`
3. Report what was changed

### Rollback guidance

All autoskill changes are reversible:

**If git is available:**

1. Find commit: `git log --grep="autoskill" --oneline`
2. Revert specific commit: `git revert <commit-hash>`
3. Or revert all autoskill changes: `git log --grep="autoskill" --format="%H" | xargs -n1 git revert`

**Manual rollback:**

1. Each edit is minimal and focused (easy to identify)
2. Use git diff to see exact changes: `git show <commit-hash>`
3. Manually undo the specific section that caused issues

**Prevention:**

- Always commit each skill change separately (never batch)
- Use descriptive commit messages: `chore(autoskill): add error handling rule to code-simplifier`
- Test after each change before proceeding to next

## When to ask for clarification

Use the AskUserQuestion tool when:

**Ambiguous signals:**

- Correction doesn't clearly specify what to do instead
- Pattern observed but unclear if intentional or coincidental
- Signal could apply to multiple skills

**Contradictory feedback:**

- Equal confidence scores for contradicting signals
- User's recent correction conflicts with established pattern
- Unclear which rule should take precedence

**Boundary decisions:**

- Uncertain whether change belongs in CLAUDE.md or Skill
- Score is near threshold (4-6 points for new skill creation)
- Signal could be project-wide convention OR skill-specific behavior

**Scope uncertainty:**

- Unclear if correction applies to all cases or specific context
- Signal mentions "here" or "this case" without "always/never"
- Need to verify if pattern should be generalized

**Example questions:**

```
"I detected two corrections about error handling:
1. 'Don't add try-catch for internal functions'
2. 'Always validate user input'

These seem contradictory. Should I:
- Add both rules with specific contexts?
- Apply different rules to internal vs external code?
- Something else?"
```

**Never guess or assume** - when in doubt, downgrade to MEDIUM confidence and ask.

## Constraints

- Never delete existing rules without explicit instruction
- Prefer additive changes over rewrites
- One concept per change (easy to revert)
- Preserve existing file structure and tone
- When uncertain, downgrade to MEDIUM confidence and ask
