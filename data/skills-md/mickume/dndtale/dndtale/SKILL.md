---
name: dndtale
description: A comprehensive DnD campaign and adventure creation skill for game masters and creative content creators. Helps design complete campaigns, adventures, NPCs, encounters, maps, and storylines tailored for tabletop play. Use this when designing D&D content, creating campaign worlds, developing adventure hooks, designing encounters, or building narrative structures for player tables.
---

# Dndtale - DnD Campaign & Adventure Creator

Dndtale is a specialized skill designed to assist Dungeon Masters and creative content creators in building complete, engaging Dungeons & Dragons campaigns and adventures.

---

## Quick Start

### For New Campaigns

1. **Use TodoWrite** immediately to create a planning checklist
2. **Follow the workflow:** [workflows/campaign-creation-workflow.md](workflows/campaign-creation-workflow.md)
3. **Use AskUserQuestion** to gather requirements if not provided
4. **Use templates:** All templates are in [templates/](templates/)
5. **Quality check:** Use [checklists/campaign-quality-checklist.md](checklists/campaign-quality-checklist.md) when done

### For Updating Existing Campaigns

1. **Read existing content** before making changes
2. **Follow the iteration workflow:** [workflows/iteration-workflow.md](workflows/iteration-workflow.md)
3. **Check consistency:** Use [checklists/consistency-checklist.md](checklists/consistency-checklist.md)
4. **Use Edit tool** for targeted changes to existing files

### Need an Example?

See the complete sample campaign: [examples/the-stolen-flame/](examples/the-stolen-flame/)

---

## What Dndtale Does

This skill helps you create:

- **Complete Campaigns** - Multi-session story arcs with interconnected plots, factions, and long-term consequences
- **One-Shot Adventures** - Single-session adventures with clear objectives and satisfying conclusions
- **NPCs** - Memorable characters with personalities, motivations, secrets, and stat blocks
- **Locations** - Detailed settings with atmosphere, history, and interactive elements
- **Encounters** - Balanced challenges with multiple solutions and meaningful consequences
- **Story Frameworks** - Narrative structures that preserve player agency while ensuring coherent plots
- **Image Prompts** - Detailed prompts for AI image generation tools

---

## Core Principles

### Player Agency First
- Always provide multiple solutions to problems
- Design consequences that matter
- Avoid railroading (forced single paths)
- Let player choices shape the story

### Usability at the Table
- Write clear, scannable DM notes
- Provide concise read-aloud text
- Include quick reference tables
- Anticipate common DM needs

### Completeness and Consistency
- Cross-reference between documents
- Maintain timeline and logic
- Keep names and facts consistent
- Check dependencies when changing content

### Use the Right Tools
- **TodoWrite:** Track complex campaign creation tasks
- **AskUserQuestion:** Clarify requirements and gather preferences
- **Read:** Always read existing files before editing
- **Edit:** Make targeted changes to existing content
- **Write:** Create new files from templates

---

## File Organization

Every campaign should follow this structure:

```
campaigns/[campaign-name]/
├── campaign-overview.md         # Master document with full campaign arc
└── changelog/                   # Changelogs
    └── [change-name].md         # Documented changes to the campaign
├── README.md                  # Player-facing session zero document (spoiler-free)
├── chapter-01.md                # Detailed session content
├── chapter-02.md                # Continue for each chapter/session
├── chapters-summary.md          # Chapter/Scene-level summaries for all chapters of the campaign
├── npcs.md                      # Important characters with stats and motivations
├── locations.md                 # Key places with descriptions
├── factions.md                  # Organizations and their goals (optional)
├── timeline.md                  # Timeline of events in the campaign (optional)
└── art/                         # Image prompts and artwork
    ├── [scene-name].md          # Image generation prompts for scenes
    ├── [location-name].md       # Image generation prompts for locations/environment
    ├── [npc-name].md            # Image generation prompts for unique NPCs
    └── [generated-images.jpg]   # Actual artwork *.jpg (if generated)
```

---

## Resource Library

### Templates
Use these as starting points for all campaign documents:

- **[campaign-overview.md](templates/campaign-overview.md)** - Master campaign document
- **[chapter-template.md](templates/chapter-template.md)** - Individual session structure
- **[chapters-summary.md](templates/chapters-summary.md)** - Scene-level overview for all chapters of the campaign
- **[timeline.md](templates/timeline.md)** - Timeline of events in the campaign
- **[README.md](templates/README.md)** - Player-facing session zero document
- **[npcs.md](templates/npcs.md)** - NPC roster and details
- **[locations.md](templates/locations.md)** - Location descriptions and maps
- **[factions.md](templates/factions.md)** - Organizations and politics

### Modules
Reference these for detailed guidance:

- **[campaign-types.md](modules/campaign-types.md)** - Linear, Sandbox, Event-Based, Setting-Based
- **[world-building.md](modules/world-building.md)** - Creating settings, NPCs, and interactions
- **[formatting-conventions.md](modules/formatting-conventions.md)** - How to format all content

### Workflows
Step-by-step processes for different tasks:

- **[campaign-creation-workflow.md](workflows/campaign-creation-workflow.md)** - Complete campaign creation from start to finish
- **[iteration-workflow.md](workflows/iteration-workflow.md)** - Updating and refining existing campaigns

### Checklists
Quality assurance for your work:

- **[campaign-quality-checklist.md](checklists/campaign-quality-checklist.md)** - Ensure completeness, balance, and quality
- **[consistency-checklist.md](checklists/consistency-checklist.md)** - Maintain consistency when making changes

### Examples
Complete sample campaigns demonstrating all templates:

- **[The Stolen Flame](examples/the-stolen-flame/)** - One-shot adventure showing all templates in action

---

## Workflow Overview

### Creating a New Campaign

**Phase 1: Gather Requirements**
1. Use TodoWrite to create planning checklist
2. Use AskUserQuestion if briefing incomplete
3. Collect: story idea, length, level, setting, tone

**Phase 2: Campaign Framework** 
1. Choose campaign type (see [modules/campaign-types.md](modules/campaign-types.md))
2. Create campaign-overview.md (use [template](templates/campaign-overview.md))
3. Plan chapter breakdown
4. Create chapters-summary.md (use [template](templates/chapters-summary.md))
5. Identify major NPCs and locations

**Phase 3: Detailed Development** 
1. Write each chapter (use [template](templates/chapter-template.md))
2. Detail NPCs (use [template](templates/npcs.md))
3. Detail locations (use [template](templates/locations.md))
4. Create factions if needed (use [template](templates/factions.md))
5. Create 

**Phase 4: Player-Facing Content** 
1. Write README.md (use [template](templates/README.md))
2. Ensure there are NO SPOILERS in the briefing

**Phase 5: Polish & QA** 
1. Create image prompts for key scenes
2. Run through [campaign-quality-checklist.md](checklists/campaign-quality-checklist.md)
3. Read entire campaign for flow and consistency

**See detailed workflow:** [workflows/campaign-creation-workflow.md](workflows/campaign-creation-workflow.md)

### Updating an Existing Campaign

1. **Read** all affected files first
2. **Plan** changes and identify dependencies
3. **Edit** existing files with targeted changes
4. **Update** cross-references
5. **Check** consistency with [consistency-checklist.md](checklists/consistency-checklist.md)

**See detailed workflow:** [workflows/iteration-workflow.md](workflows/iteration-workflow.md)

---

## Important Guidelines

### Always Do This

**Use TodoWrite for Complex Tasks**
- Create planning checklist immediately
- Track progress through creation phases
- Mark tasks completed as you finish them
- Keep exactly ONE task in_progress at a time

**Ask Questions When Needed**
- Use AskUserQuestion for unclear requirements
- Clarify tone, content boundaries, player preferences
- Ask about multiple valid approaches
- Don't guess—confirm with the DM

**Read Before Editing**
- Always Read existing files before using Edit
- Understand the full context
- Check dependencies and cross-references
- Maintain consistency with existing content

**Preserve Player Agency**
- Provide multiple solutions to every problem
- Design meaningful consequences
- Allow creative approaches
- Avoid forced single paths

**Follow Templates**
- Use the templates in [templates/](templates/)
- Maintain consistent formatting
- Include all required sections
- Match the style of examples

### Never Do This

**Don't Railroad Players**
- Never force a single solution
- Don't invalidate player choices
- Avoid "the NPC does everything" solutions

**Don't Skip Quality Checks**
- Always use checklists before completion
- Verify cross-references work
- Check name consistency
- Test story logic

**Don't Forget Documentation**
- Cross-reference between documents
- Link to related content
- Include DM notes and tips
- Provide stat blocks or references

**Don't Break Existing Content**
- When editing, maintain story logic
- Update all references to changed content
- Check timeline consistency
- Preserve what works

---

## Session Zero Considerations

Unless stated otherwise, campaigns are written for consenting adults. When content might be disturbing or NSFW:

- Include content warnings in README.md
- Suggest Session Zero discussion topics
- Recommend safety tools (X-Card, Lines & Veils)
- Clearly mark mature content

---

## Standard D&D Adventure Structure

The skill follows professional D&D adventure conventions (see [STRUCTURE.md](STRUCTURE.md) for full details):

**Front Matter:** Introduction, synopsis, hooks
**Core Structure:** Chapter breakdown with scenes, encounters, NPCs
**Climax:** Epic final encounter with multiple resolution paths
**Back Matter:** Appendices with stat blocks, magic items, handouts

**Each Chapter Includes:**
- Read-aloud text for scene setting
- DM information and secrets
- Encounter design (combat, social, skill challenges)
- NPCs with personality and stats
- Treasure and rewards
- Connections to other chapters

---

## Formatting Standards

Follow conventions in [modules/formatting-conventions.md](modules/formatting-conventions.md):

**Read-Aloud Text:**
```markdown
> Text the DM reads to players
> Detailed, evocative, multi-sensory
> Present tense, no secrets
```

**DM Notes:** Regular text with mechanical details, secrets, contingencies

**Stat Blocks:** Reference Monster Manual when possible, or provide custom stats

**Cross-References:** Use markdown links: `[Chapter 2](chapter-02.md)` or `[NPCs](npcs.md#npc-name)`

**Image Prompts:** Create in `art/` folder with proper metadata

---

## Quick Reference

### Campaign Types
- **Linear:** Sequential chapters, clear path (easiest to prep)
- **Sandbox:** Central hub, many options (most prep)
- **Event-Based:** Timeline of events, player actions affect outcomes
- **Setting-Based:** Location-focused, exploratory

See: [modules/campaign-types.md](modules/campaign-types.md)

### Encounter Design
- Mix combat, social, and exploration
- Multiple solutions always
- Appropriate difficulty for level
- Meaningful consequences

### NPC Design
- Appearance, personality, mannerisms
- Wants (surface goal) and needs (deeper motivation)
- Secrets and relationships
- Stat block or reference

See: [templates/npcs.md](templates/npcs.md)

### Location Design
- Atmosphere (sights, sounds, smells, feel)
- History and current situation
- NPCs present and encounters
- Secrets to discover

See: [templates/locations.md](templates/locations.md)

---

## Tone and Content

**Adjust to DM's requested tone:**
- Heroic & Epic
- Dark & Serious
- Humorous & Lighthearted
- Mystery & Intrigue
- Horror
- Adult-themed/NSFW (with appropriate warnings)

**Always:**
- Match requested tone consistently
- Warn about mature content in briefing
- Provide Session Zero guidance for sensitive topics

---

## Image Generation Integration

Create detailed prompts for AI image generation (reference `dndig` tool if available):

**Format:**
```markdown
---
title: filename-prefix
aspect_ratio: "16:9"
resolution: 2K
instructions: optional-style-file.md
---

Detailed visual description based on scene read-aloud text...
Include: composition, lighting, mood, style
```

**Create prompts for:**
- Key locations and scenes
- Important NPCs
- Climactic encounters
- Maps (as needed)

---

## Examples in Action

### Example: Starting a New Campaign

```
DM: "I want to create a 3-session campaign about smugglers in a port city"

You:
1. TodoWrite: Create planning checklist
2. AskUserQuestion: Clarify tone, starting level, player count
3. Choose campaign type: Sandbox (city hub with multiple quest lines)
4. Create campaign-overview.md from template
5. Create 3 chapters, npcs.md, locations.md
6. Create README.md for players
7. Run quality checklist
8. Deliver organized campaign
```

### Example: Updating Existing Campaign

```
DM: "The players killed the quest-giver NPC. I need to adapt."

You:
1. Read campaign-overview.md and affected chapters
2. Read npcs.md to understand the NPC's role
3. Follow iteration-workflow.md
4. Options:
   - Introduce heir/assistant to replace NPC
   - Redistribute quests to other NPCs
   - Show consequences of NPC death
5. Edit affected chapters
6. Update npcs.md and cross-references
7. Run consistency checklist
```

---

## Success Criteria

A campaign is ready when:

- [ ] All chapters are complete and detailed
- [ ] NPCs have personality, motivations, and stats
- [ ] Locations are described with atmosphere and features
- [ ] Multiple solutions exist for every problem
- [ ] Cross-references are accurate
- [ ] Briefing is complete and spoiler-free
- [ ] Quality checklist passes
- [ ] DM can run Session 1 with current materials

---

## Getting Help

**Stuck on something?**
- Check the relevant module in [modules/](modules/)
- Review the workflow in [workflows/](workflows/)
- Look at the example in [examples/the-stolen-flame/](examples/the-stolen-flame/)
- Use AskUserQuestion to clarify with the DM

**Need to verify quality?**
- [campaign-quality-checklist.md](checklists/campaign-quality-checklist.md)
- [consistency-checklist.md](checklists/consistency-checklist.md)

---

## Remember

You're helping a DM create memorable experiences for their players. Focus on:

✓ **Usability** - Easy to run at the table
✓ **Flexibility** - Multiple solutions, player agency
✓ **Completeness** - All necessary information present
✓ **Consistency** - Names, facts, timeline all align
✓ **Quality** - Engaging stories, balanced encounters, memorable moments

Good luck, and may your campaigns be legendary!
