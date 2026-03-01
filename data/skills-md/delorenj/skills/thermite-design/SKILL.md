---
name: thermite-design
description: "Thermite game design process skill. Use when: running design sessions, generating design artifacts, updating decision logs, working on the thermite project, simulating creative team discussions, or when user mentions 'thermite', 'design session', 'creative team', 'retreat', or references the Bomberman/Tarkov extraction game concept. Provides structured artifact generation, decision tracking, and multi-persona design simulation."
---

# Thermite Design Process Skill

## Overview

This skill encodes the thermite game design methodology: structured creative sessions with domain expert personas, tracked decisions, and standardized artifact outputs.

## Core Documents

Load these at session start:
- `references/system_prompt.md` - Design pillars, constraints, scope
- `references/creative_team.md` - 8 expert personas with tensions
- `references/artifact_templates.md` - All output formats

## Design Session Protocol

### Session Types

**Boardroom Retreat** (multi-persona discussion)
1. State the topic clearly
2. Identify which personas are relevant (not all 8 every time)
3. Let each voice react from their expertise
4. Surface tensions explicitly
5. Drive toward synthesis
6. Capture decisions, open questions, action items

**Deep Dive** (single-domain exploration)
- Focus on one persona's domain
- Produce domain-specific artifact
- Flag cross-domain implications

**Decision Review** (validation check)
- Review pending decisions
- Run pillar check on each
- Promote to "Decided" or flag blockers

### Session Output Requirements

Every session MUST produce:
```markdown
# Session [N]: [Topic]
**Date:** YYYY-MM-DD
**Type:** Boardroom | Deep Dive | Decision Review
**Participants:** [List relevant personas]

## Decisions Made
[For each decision, append to decision_log.md]

## Open Questions
[Append to open_questions.md with tags]

## Artifacts Updated
[List which reference docs were modified]

## Action Items
- [ ] Owner: Task

## Next Session
[Recommended topic]
```

## Artifact Registry

| Artifact | File | Owner | Update Trigger |
|----------|------|-------|----------------|
| System Prompt | system_prompt.md | Moderator | Pillar changes |
| Decision Log | decision_log.md | Moderator | Every session |
| Open Questions | open_questions.md | Moderator | Every session |
| Core Loop Spec | core_loop.md | Viktor + Shinji | Loop changes |
| Gear Registry | gear_registry.md | Marcus | Item additions |
| Map Templates | map_templates.md | Elena | Map changes |
| Economy Model | economy_model.md | Sarah | Economy changes |
| Visual Language | visual_language.md | Jordan | UX changes |
| Tech Spec | tech_spec.md | Wei | Architecture changes |
| MVD Checklist | mvd_checklist.md | Moderator | Milestone tracking |

## Decision Log Format

```markdown
## Decision: [Short Title]
**ID:** DEC-[NNN]
**Date:** YYYY-MM-DD
**Session:** [N]
**Status:** Decided | Tentative | Revisit After Playtest
**Pillar(s):** [Which design pillars this serves]

### Context
Why this came up.

### Decision
What we chose.

### Alternatives Considered
What we didn't choose and why.

### Dissent
Who disagreed, their concern, how addressed.

### Validation Needed
What we need to test to confirm this works.
```

## MVD (Minimum Viable Design) Checklist

Before prototype development begins, these must be answered:

### Must Have (Blocks Development)
- [ ] Core loop minute-by-minute flow documented
- [ ] Grid contract defined (tile size, movement speed, bomb timing)
- [ ] Loadout system scoped (slots, starter kit, 2-3 tiers)
- [ ] Death rules codified (what's lost, what persists)
- [ ] One map template with zones annotated
- [ ] Extraction mechanic specified
- [ ] AI presence decided (in v1 or not)

### Should Have (Blocks Polish)
- [ ] 6-8 bomb types defined with counterplay
- [ ] Economy curves modeled (rebuild time, progression speed)
- [ ] Visual language guide started
- [ ] Audio design approach documented
- [ ] Netcode architecture specified

### Nice to Have (Can Iterate)
- [ ] Full gear registry
- [ ] All map templates
- [ ] Hideout system details
- [ ] Skill/progression system

## Persona Quick Reference

| Persona | Domain | Key Question | Tension With |
|---------|--------|--------------|--------------|
| **Shinji Tanaka** | Classic Arcade | "Is this readable in 2 seconds?" | Viktor, Maya |
| **Viktor Volkov** | Extraction/Economy | "Does risk feel real AND survivable?" | Shinji, Marcus, Maya |
| **Elena Vasquez** | Map Architecture | "Does space create decisions?" | Shinji, Wei |
| **Marcus Chen** | Combat Balance | "What beats this?" | Viktor, Wei |
| **Sarah Okonkwo** | Economy | "Where does currency leave?" | Viktor, Wei |
| **Dr. Maya Reyes** | Player Psychology | "What does first death teach?" | Viktor, Marcus |
| **Wei Zhang** | Technical | "What happens at 150ms latency?" | Everyone |
| **Jordan Ellis** | UX/Accessibility | "Can colorblind players distinguish this?" | Marcus, Elena |

## Pillar Check Protocol

Before finalizing any decision, run:

1. **Meaningful Risk** - Does this preserve stakes?
2. **Readable Chaos** - Is this instantly parseable?
3. **Compressed Tension** - Does this respect 5-8 min target?
4. **Earned Mastery** - Does skill beat gear?
5. **Sustainable Economy** - Is this exploitable? Patchable?

If ANY pillar is violated, flag and discuss.

## Red Flags

Stop and reconsider if you hear:
- "This would be cool but..." → Scope creep
- "Players won't do that..." → They will
- "We can balance it later..." → No you can't
- "Just like [AAA game] but..." → Resource mismatch
- "It's fine if it's a little unfair..." → Pillar violation

## Scripts

- `scripts/new_session.py` - Initialize session output template
- `scripts/add_decision.py` - Append formatted decision to log
- `scripts/check_mvd.py` - Report MVD checklist status
- `scripts/export_artifacts.py` - Bundle all artifacts for review

## Integration Notes

This skill works with:
- `ecosystem-patterns` - For project organization
- `software-change-management-using-git` - For versioning artifacts

When creating Thermite project files, follow iMi worktree patterns and maintain corresponding vault documentation.
