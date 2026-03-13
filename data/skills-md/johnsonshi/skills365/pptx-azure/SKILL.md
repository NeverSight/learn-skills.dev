---
name: pptx-azure
description: "Azure-specific PowerPoint guidance and assets for creating/editing .pptx presentations; use with the base pptx skill when users need Azure-branded slide design, architecture visuals, icons, color palettes, storytelling structure, and speaker-note-driven slide workflows."
---

# pptx-azure

Azure-specific assets for PowerPoint presentations.

**Prerequisite:** Use in conjunction with the [pptx skill](https://github.com/anthropics/skills/blob/main/skills/pptx/SKILL.md) for core PowerPoint workflows (reading, editing, creating presentations).

## Recommended Workflow

**Start here:** Before creating a PowerPoint, use the `/doc-coauthoring` skill to create a markdown spec first.

```
Phase 1: Context Gathering    →  /doc-coauthoring skill
         (Back-and-forth to gather requirements, create markdown spec)
                              ↓
Phase 2: Validation           →  Review against slides/ guides
         (Ensure each slide follows best practices)
                              ↓
Phase 3: Slide-by-Slide       →  Build PPTX incrementally
         (Create one slide at a time, user reviews each)
```

See [workflow.md](workflow.md) for the complete process.

**Key principle:** Create the markdown spec FIRST, validate it, THEN build the PPTX slide-by-slide with user collaboration.

### Template

Use [templates/presentation-spec.md](templates/presentation-spec.md) for the markdown spec:

```markdown
## Slide N: [Action Title]

**Type:** [Title | Section header | Content | Architecture | Data/Chart | Comparison | Summary]

**Key Message:** [One sentence takeaway]

**Content:**
- [Verbose content - will be trimmed later]

**Visuals:**

Description: [What the visual shows]

```mermaid
[Mermaid diagram representing the visual]
```

**Speaker Notes:** [Detailed notes on what presenter will say]
```

### Agent Responsibilities During Co-authoring

When using `/doc-coauthoring` to create the markdown spec, the agent should:

1. **Ask clarifying questions** - Understand audience, goals, key messages
2. **Proactively draft speaker notes** - Don't wait for the user to write these; propose them based on context
3. **Create Mermaid diagrams** - For any visual (architecture, flowchart, sequence), create a Mermaid representation
4. **Iterate collaboratively** - Refine content, visuals, and speaker notes with the user

The agent generates the speaker notes and Mermaid diagrams based on user requirements - the user provides the ideas, the agent drafts the details.

### Slide-by-Slide Creation

When building the PPTX:

1. **Always re-read the PPTX before editing** - user may have manually edited
2. Create/update one slide at a time
3. Present to user for review
4. Iterate until approved, then move to next slide
5. Handle additions, removals, and reordering as needed

### Per-Slide Checklist

For each slide, ensure:

- [ ] **Title** matches the action title from the markdown spec
- [ ] **Key message** is clear and matches the spec
- [ ] **Content** is trimmed down from verbose spec to concise slide
- [ ] **Visuals** are included and aligned (icons, diagrams, charts)
- [ ] **Speaker notes** are added to the slide (from the spec's Speaker Notes field)
- [ ] **Layout** follows visual hierarchy principles
- [ ] **Colors** use Azure palette consistently
- [ ] **Icons** are from the official Azure icon set

**Speaker notes are critical** - they contain what the presenter will say verbally. Always transfer speaker notes from the markdown spec to the actual PPTX slide.

## Structure

```
pptx-azure/
├── SKILL.md                    # This file
├── workflow.md                 # Full workflow documentation
├── architecture/
│   └── diagrams.md             # Azure architecture diagram guidelines
├── icons/
│   └── Azure_Public_Service_Icons/
│       └── Icons/              # SVG icons by category
├── palettes/
│   └── azure-colors.md         # Full color palette reference
├── slides/                     # Slide design best practices
│   ├── one-idea-per-slide.md
│   ├── action-titles.md
│   ├── visual-hierarchy.md
│   ├── less-is-more.md
│   ├── storytelling-structure.md
│   └── executive-communication.md
└── templates/
    └── presentation-spec.md    # Markdown template for presentation spec
```

## Which Guide to Use

| You're doing... | Read this |
|-----------------|-----------|
| Starting a new presentation | [workflow.md](workflow.md) + `/doc-coauthoring` |
| Creating an Azure architecture diagram | [architecture/diagrams.md](architecture/diagrams.md) |
| Presenting to executives or leadership | [slides/executive-communication.md](slides/executive-communication.md) |
| Building a pitch deck or persuasive presentation | [slides/storytelling-structure.md](slides/storytelling-structure.md) |
| Reviewing slides that feel cluttered or wordy | [slides/less-is-more.md](slides/less-is-more.md) |
| Writing slide titles | [slides/action-titles.md](slides/action-titles.md) |
| Laying out content on a slide | [slides/visual-hierarchy.md](slides/visual-hierarchy.md) |
| Splitting a complex slide | [slides/one-idea-per-slide.md](slides/one-idea-per-slide.md) |
| Adding Azure icons or branding | See Icons and Colors below |

## Quick Reference

### Icons

**Path:** `icons/Azure_Public_Service_Icons/Icons/<category>/<icon>.svg`

| Category | Examples |
|----------|----------|
| ai + machine learning | Azure OpenAI, Cognitive Services, Machine Learning |
| analytics | Synapse, Data Factory, Event Hubs |
| compute | Virtual Machines, App Service, Functions |
| containers | AKS, Container Instances, Container Registry |
| databases | SQL Database, Cosmos DB, Redis Cache |
| networking | Virtual Network, Load Balancer, Application Gateway |
| security | Key Vault, Defender, Sentinel |
| storage | Blob Storage, Data Lake, File Storage |

Full categories: ai + machine learning, analytics, app services, azure ecosystem, azure stack, blockchain, compute, containers, databases, devops, general, hybrid + multicloud, identity, integration, intune, iot, management + governance, menu, migrate, migration, mixed reality, mobile, monitor, networking, new icons, other, security, storage, web

**Using SVG icons in PowerPoint:**
- PowerPoint 2019+ supports SVG directly: Insert > Pictures > select SVG file
- For older versions, convert SVG to PNG or EMF first
- Recommended size: 64x64 px for inline icons, larger for featured elements
- Do not stretch, distort, or recolor official Azure icons

### Colors

| Name | Hex | Usage |
|------|-----|-------|
| Azure Blue | `#0078D4` | Primary brand color |
| Azure Dark | `#002050` | Headers, dark backgrounds |
| Azure Light | `#50E6FF` | Accents, highlights |
| Success | `#107C10` | Positive states |
| Warning | `#FFB900` | Caution |
| Error | `#D13438` | Critical |

See [palettes/azure-colors.md](palettes/azure-colors.md) for full palette including neutrals, extended product colors, and dark theme.

## Slide Design Guides

Based on established frameworks: McKinsey/BCG consulting style, Barbara Minto's Pyramid Principle, Garr Reynolds' Presentation Zen, Nancy Duarte's Slide:ology and Resonate.

| Guide | When to Use | Key Principle |
|-------|-------------|---------------|
| [one-idea-per-slide.md](slides/one-idea-per-slide.md) | Slide feels overloaded or confusing | Each slide conveys exactly one message |
| [action-titles.md](slides/action-titles.md) | Writing or reviewing slide titles | Titles state the takeaway, not just the topic |
| [visual-hierarchy.md](slides/visual-hierarchy.md) | Laying out slide content | Guide the eye with size, contrast, white space |
| [less-is-more.md](slides/less-is-more.md) | Slides have too much text | Cut ruthlessly; apply 10/20/30 rule |
| [storytelling-structure.md](slides/storytelling-structure.md) | Building a persuasive narrative | Create story arc, not information dump |
| [executive-communication.md](slides/executive-communication.md) | Presenting to leadership | Lead with conclusion (Pyramid Principle) |

## Architecture Diagrams

When creating Azure architecture diagrams, read [architecture/diagrams.md](architecture/diagrams.md). Key points:

- **Always use directional arrows** - lines without arrows are ambiguous
- **Label everything** - icons, containers, relationships
- **Be accurate** - don't show PaaS in a subnet if it uses private endpoint
- **Layer, don't overload** - use multiple diagrams at different detail levels
- **Include metadata** - title, date, author, version

## See Also

- [workflow.md](workflow.md) - Complete presentation creation workflow
- [pptx skill](https://github.com/anthropics/skills/blob/main/skills/pptx/SKILL.md) - Core PowerPoint workflows
- [Azure Architecture Icons](https://learn.microsoft.com/en-us/azure/architecture/icons/) - Official icon source
- [Azure Well-Architected Framework - Design Diagrams](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/design-diagrams) - Microsoft's diagramming guidance
