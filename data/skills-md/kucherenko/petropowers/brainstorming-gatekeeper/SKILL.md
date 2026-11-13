---
name: brainstorming-gatekeeper
description: Pre-flight check that determines if brainstorming is required before any action. Invoke this FIRST for any request involving creative or generative work.
---

# Skill: Brainstorming Gatekeeper

Pre-flight check that analyzes user requests and determines if brainstorming is required before any action.

## When to Invoke

Invoke this skill when the user request contains ANY of:
- Creative keywords (generate, create, build, implement, add, develop, make, set up, write, design)
- Oil & gas domain terms (reservoir, well, seismic, production, drilling, LAS, SEG-Y, WITSML, pipeline)
- Missing critical details (no size, format, location, constraints specified)

## Skill Type: Rigid

This is a gatekeeper skill. Follow the decision logic exactly. Do not rationalize around it.

## Trigger Detection

### Keywords Table

| Category | Triggers |
|----------|----------|
| **Creative** | generate, create, build, implement, add, develop, make, set up, write, design, construct, establish |
| **Oil & Gas** | reservoir, well, seismic, production, drilling, LAS, SEG-Y, WITSML, PRODML, pipeline, formation, porosity, permeability, logs, survey |
| **Ambiguity** | Missing: size, format, location, constraints, data type, time range, count, structure |

### Decision Logic

```
IF (has_creative_keyword AND has_domain_context) 
   OR (has_creative_keyword AND has_ambiguity)
   OR (has_domain_context AND has_ambiguity)
THEN → brainstorming required
ELSE → proceed directly
```

## Your Task

Analyze the user's request against the triggers above. Then output ONE of:

### Output A: Brainstorming Required

```markdown
## Gatekeeper Decision: Brainstorming Required

**Triggers detected:**
- Keyword: [list detected creative keywords]
- Domain: [list detected domain terms]
- Ambiguity: [list missing details]

**Action:** Invoke brainstorming skill before proceeding.
Do NOT execute any implementation actions.
```

Then immediately invoke the `brainstorming` skill.

### Output B: Proceed Directly

```markdown
## Gatekeeper Decision: Proceed

**Analysis:** [Brief explanation why this is not creative work]
**Action:** Continue with appropriate skill or direct response.
```

Then continue with the appropriate action.

## Exceptions (Skip Brainstorming)

These requests do NOT require brainstorming:
- Pure information queries ("What is porosity?", "Explain SEG-Y format")
- Analysis of existing data ("Analyze this LAS file", "Read this SEG-Y")
- Simple file operations ("Read this file", "List directory contents")
- Status checks ("What's in this folder?", "Show git status")
- Follow-up to existing brainstorming session (design already approved)
- Bug fixes with clear reproduction steps
- Code review responses

## Red Flags - You're Rationalizing

| Thought | Reality |
|---------|---------|
| "This is too simple to brainstorm" | Simple requests often hide complexity. Run the check. |
| "I already know what they want" | That's an assumption. Run the check. |
| "I'll save time by skipping this" | Brainstorming catches scope issues early. Run the check. |
| "The user said it's urgent" | Urgency doesn't change the need for clarity. Run the check. |

## Examples

**Request:** "I work on ppr-1 reservoir and need to generate data for the reservoir"

**Analysis:**
- Keyword: "generate" ✓
- Domain: "reservoir" ✓
- Ambiguity: missing data type, format, size ✓

**Decision:** Brainstorming Required

---

**Request:** "What does the GR curve in a well log represent?"

**Analysis:**
- Keyword: none
- Domain: "well log", "GR curve" (but informational)
- Ambiguity: N/A (question, not task)

**Decision:** Proceed (informational query)

---

**Request:** "Read the LAS file in data/well-1.las and show the curves"

**Analysis:**
- Keyword: "read", "show" (not creative)
- Domain: "LAS file" (but analysis, not creation)
- Ambiguity: file path specified

**Decision:** Proceed (analysis of existing data)
