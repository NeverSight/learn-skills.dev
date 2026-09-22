---
name: context-engine-builder
description: "Generate a context engine — seven structured blueprint files (UX, UI, content, accessibility, ethical, technical, business intelligence) that encode everything an AI agent needs to work with a design system. This produces YAML infrastructure in .ai/context-engine/, NOT a health score or quality assessment. Trigger when someone says: build a context engine, create a system brain, build the seven blueprints, context engine, blueprint stack, encode design system knowledge for AI, make our system AI-navigable, or anything about creating structured knowledge files that AI agents load to understand the system. Do NOT trigger for scoring or assessing system health — use system-health for that."
references:
  - ../../knowledge-notes/ai-readiness.md
  - ../../knowledge-notes/component-bestiary-reference.md
  - ../../knowledge-notes/agent-orchestration-guide.md
  - ../../knowledge-notes/mcp-setup-guide.md
  - ../../knowledge-notes/context-engine-blueprints.md
---

# Context engine builder

A skill for generating a context engine — a structured, multi-layered knowledge base that gives AI agents the complete picture of a design system. The engine encodes seven dimensions of system knowledge (UX, UI, content, accessibility, ethical, technical, and business intelligence) as machine-readable blueprints that agents load, reason over, and apply without requiring implicit knowledge or human interpretation.

## Context

A design system is more than a component library. It encodes decisions about user experience patterns, visual language, content voice, accessibility requirements, ethical guardrails, technical constraints, and business rules. These decisions live in different places — Figma files, code repos, wikis, Slack threads, the heads of senior team members — and most of them are invisible to AI agents.

When an AI agent interacts with a design system, it typically receives a narrow slice: component props, maybe a description, perhaps some token values. It does not receive the reasoning behind those components, the constraints that govern their use, or the relationships between design decisions and business outcomes. The result is output that is technically valid but contextually wrong — a login form that uses the right components but ignores the system's established authentication patterns, or a dashboard that follows the grid but violates the system's data visualisation principles.

A context engine front-loads this knowledge. Instead of letting agents discover context through trial and error (or not discover it at all), the engine encodes it as structured data that agents load at the start of a task. The seven blueprints are not arbitrary categories — they represent the seven dimensions of knowledge that, when missing, produce the most common classes of AI-generated design system errors.

The practical output is a set of structured files — one per blueprint — that live alongside the codebase and are consumed by AI agents, MCP servers, and developer tooling. Together they form the machine-readable brain of the design system.

## Boundaries

This skill builds context infrastructure — it does not assess system health or score quality (use `system-health` for that). If the system has no documented components, tokens, or patterns yet, the context engine has nothing to encode; help the team establish foundations first. If only one or two blueprints are needed (a common case — many teams start with the Technical and UI blueprints only), generate those specifically rather than forcing all seven. The engine is modular; partial generation is a feature, not a gap.

---

## Configuration

Before producing output, check for a `.ds-ops-config.yml` file in the project root. If present, load:
- `system.framework` — pre-selects framework for technical blueprint generation
- `system.component_paths` — directs blueprint scanning to correct directories
- `system.tokens` — identifies token files for UI blueprint extraction
- `integrations.*` — enables auto-pull for blueprint data
- `context_engine.blueprints` — overrides which blueprints to generate (default: all seven)
- `context_engine.output_format` — output format preference (JSON or YAML, default: YAML)

## Auto-pull integrations

If integrations are configured in `.ds-ops-config.yml`, pull data automatically:

**Figma MCP** (`integrations.figma.enabled: true`):
- Read the published library from `integrations.figma.file_key`
- Extract component descriptions, variant structures, and layer hierarchies for the UX and UI blueprints
- Pull design token definitions (colour, spacing, typography) for the UI blueprint
- Extract accessibility annotations if present for the accessibility blueprint

**Storybook** (`integrations.storybook.enabled: true`):
- Fetch the story index and component metadata
- Extract documented states, interactions, and composition patterns for the UX blueprint
- Pull accessibility addon results for the accessibility blueprint

**GitHub** (`integrations.github.enabled: true`):
- Scan component source files for prop types, default values, and TypeScript interfaces for the technical blueprint
- Pull PR templates and contribution guidelines for governance context
- Check for existing documentation files that inform blueprint content

If an integration fails, log it and proceed with manual scanning and user input.

---

## Step 1: Assess current context coverage

Before building blueprints, understand what context already exists. Scan for:

- **Existing documentation**: Component docs, pattern libraries, design principles pages, content guidelines, accessibility policies
- **Structured metadata**: JSON/YAML files with component definitions, token files, manifest files
- **Implicit context**: README files, contribution guides, code comments, Storybook stories that encode knowledge informally

Produce a brief context coverage assessment:

| Blueprint | Existing sources found | Coverage estimate | Primary gaps |
|---|---|---|---|
| UX | [list] | [none/partial/good] | [what's missing] |
| UI | [list] | [none/partial/good] | [what's missing] |
| Content | [list] | [none/partial/good] | [what's missing] |
| Accessibility | [list] | [none/partial/good] | [what's missing] |
| Ethical | [list] | [none/partial/good] | [what's missing] |
| Technical | [list] | [none/partial/good] | [what's missing] |
| Business intelligence | [list] | [none/partial/good] | [what's missing] |

Ask for or confirm (skip questions already answered by config or auto-pull):
- Which blueprints are highest priority? (Default: all, but teams may want to start with a subset)
- Are there existing documents that should be treated as source material for specific blueprints?
- Are there team members who hold institutional knowledge for specific dimensions that should be captured?

---

## Step 2: Generate the UX blueprint

The UX blueprint encodes behavioural rules — how components and patterns behave in context, the interaction patterns they follow, and the user experience principles that govern decisions.

### What to include

**Interaction patterns**: For each documented pattern in the system, capture the behavioural contract:
- Trigger conditions (what initiates the pattern)
- State transitions (what states exist and what causes transitions)
- Completion criteria (what defines a successful interaction)
- Error states (what happens when things go wrong)
- Edge cases (empty states, loading states, maximum data, minimum viewport)

**Pattern selection rules**: Decision logic for when to use which pattern:
- If the user needs to [intent], use [pattern] because [reasoning]
- If [context condition], prefer [pattern A] over [pattern B] because [trade-off]
- Never use [pattern] when [constraint] because [consequence]

**Flow definitions**: Multi-step user journeys that span multiple components:
- Authentication flows (sign-up, sign-in, password reset, session management)
- Data entry flows (form progression, validation timing, save patterns)
- Navigation patterns (wayfinding, breadcrumbs, deep linking)
- Feedback patterns (success, error, warning, informational)

### Output format

Follow the **UX blueprint template** in `references/context-engine-blueprints.md`. Key structures: `patterns` (with trigger, states, transitions, completion, errors, edge_cases) and `selection_rules` (with intent, use, not, reason).

---

## Step 3: Generate the UI blueprint

The UI blueprint encodes the visual system as structured, machine-readable data — not as a style guide for humans, but as a specification that AI agents and code generators consume directly.

### What to include

**Token architecture**: The complete token hierarchy with semantic intent:
- Primitive tokens (raw values: colours, spacing scale, type scale)
- Semantic tokens (intent-mapped: action-primary, surface-default, text-muted)
- Component tokens (scoped: button-background, input-border)
- Token relationships (which semantic tokens reference which primitives)

**Layout system**: Grid, spacing, and responsive rules:
- Grid definitions (columns, gutters, margins per breakpoint)
- Spacing scale with usage rules (when to use which step)
- Responsive behaviour rules (what changes at each breakpoint)
- Container constraints (max widths, content widths)

**Visual patterns**: Recurring visual treatments encoded as rules:
- Elevation system (shadow levels, when to use each)
- Border radius scale and usage rules
- Colour application rules (which semantic tokens apply to which element types)
- Typography application (heading hierarchy, body text rules, caption usage)

### Output format

Follow the **UI blueprint template** in `references/context-engine-blueprints.md`. Key structures: `tokens` (colour, spacing with semantic intent), `layout` (grid, breakpoints), and `visual_rules` (elevation, border radius, colour application).

---

## Step 4: Generate the content blueprint

The content blueprint encodes voice, tone, and language rules — the writing system that governs all text in the UI, from button labels to error messages to onboarding copy.

### What to include

**Voice definition**: The system's consistent personality:
- Voice attributes (e.g., confident but not arrogant, helpful but not patronising)
- Vocabulary rules (preferred terms, prohibited terms, domain-specific terminology)
- Sentence structure preferences (active voice, sentence length, complexity level)

**Tone modulation**: How voice adapts to context:
- Tone per context (success messages: warm and brief; error messages: clear and actionable; empty states: encouraging and guiding)
- Emotional range (what emotions the interface should and should not express)
- Formality spectrum (where different UI regions fall on casual-to-formal)

**Content patterns**: Reusable text structures:
- Button label conventions (verb + noun, character limits)
- Error message format (what went wrong + what to do next)
- Empty state format (what this area shows + how to populate it)
- Placeholder text conventions
- Tooltip and help text conventions
- Confirmation dialog copy patterns

**Terminology glossary**: Domain terms with definitions and usage rules:
- What to call things consistently across the system
- Terms that mean different things in different contexts (flag these)
- Abbreviations: which are acceptable, which should be spelled out

### Output format

Follow the **Content blueprint template** in `references/context-engine-blueprints.md`. Key structures: `voice` (attributes, vocabulary with preferred/prohibited), `tone` (per-context modulation), and `patterns` (button labels, error messages, empty states).

---

## Step 5: Generate the accessibility blueprint

The accessibility blueprint encodes accessibility as machine-readable constraints — not just WCAG compliance checkboxes, but the specific accessibility contracts that components and patterns must honour.

### What to include

**Component accessibility contracts**: Per-component requirements:
- ARIA role and required attributes
- Keyboard interaction pattern (tabs, arrow keys, Enter/Space, Escape)
- Focus management rules (where focus moves on open, close, navigation)
- Screen reader announcements (what is announced, when, in what order)
- Minimum touch target sizes

**System-level accessibility rules**: Cross-cutting requirements:
- Focus visible style (what it looks like, where it applies)
- Skip navigation implementation
- Heading hierarchy rules
- Colour contrast requirements beyond WCAG minimums (if the system exceeds AA)
- Motion and animation rules (reduced motion support, maximum animation duration)
- Dark mode contrast requirements (if applicable)

**Testing protocols**: What to verify and how:
- Automated checks per component (axe-core rules that must pass)
- Manual testing checklist (screen reader testing, keyboard-only testing)
- Assistive technology support matrix (which screen readers, which browsers)

### Output format

Follow the **Accessibility blueprint template** in `references/context-engine-blueprints.md`. Key structures: `component_contracts` (role, aria_required, keyboard, focus, announcements) and `system_rules` (focus_visible, colour_contrast, motion).

---

## Step 6: Generate the ethical blueprint

The ethical blueprint encodes guardrails for responsible design — constraints that prevent the system from being used in ways that manipulate, exclude, or harm users. These are not aspirational principles but concrete rules that agents must follow.

### What to include

**Dark pattern prohibitions**: Specific patterns the system forbids:
- Manipulative urgency (fake countdown timers, "only 2 left" without real scarcity)
- Forced continuity (making cancellation harder than sign-up)
- Confirmshaming (guilt-tripping language on decline options)
- Hidden costs (revealing charges after commitment)
- Misdirection (visual emphasis that steers users away from preferred choices)

**Inclusive design rules**: Requirements beyond accessibility compliance:
- Language inclusivity (gender-neutral defaults, cultural sensitivity)
- Representation rules for imagery and illustration
- Name and identity input requirements (no arbitrary character limits, support for non-Latin characters, no forced binary gender selection)
- Regional and cultural adaptation rules

**Data and privacy patterns**: How the system handles user data:
- Consent patterns (what requires opt-in, what requires opt-out)
- Data display rules (PII masking, sensitive data handling)
- Notification and communication frequency rules
- User control patterns (how users manage their data, preferences, and account)

**Bias detection signals**: Patterns that suggest potential bias:
- Personalisation that narrows rather than expands options
- Default selections that favour the business over the user
- Asymmetric effort (easy to add, hard to remove)

### Output format

Follow the **Ethical blueprint template** in `references/context-engine-blueprints.md`. Key structures: `prohibitions` (pattern, rule, bad/good examples), `inclusive_design` (name inputs, gender), and `data_privacy` (consent rules per data type).

---

## Step 7: Generate the technical blueprint

The technical blueprint encodes implementation constraints — the rules that govern how components are built, composed, and integrated at the code level.

### What to include

**Component API contracts**: The technical interface of each component:
- Prop types with TypeScript definitions
- Required vs optional props with defaults
- Event handlers and callback signatures
- Ref forwarding patterns
- Generic type parameters (for polymorphic components)

**Composition rules**: How components fit together technically:
- Valid parent-child relationships (what can contain what)
- Context dependencies (which components require which providers)
- Slot/children contracts (what content types are accepted)
- Controlled vs uncontrolled patterns per component

**Performance constraints**: Technical boundaries:
- Bundle size budgets per component
- Render performance expectations (acceptable re-render triggers)
- Lazy loading rules (which components should be code-split)
- SSR compatibility requirements

**Integration patterns**: How the system connects to consuming applications:
- Import patterns (tree-shakeable named exports, barrel files)
- Theme/token override patterns (how consumers customise without forking)
- Versioning contract (semver rules, what constitutes breaking)
- Framework-specific integration notes (if the system supports multiple frameworks)

### Output format

Follow the **Technical blueprint template** in `references/context-engine-blueprints.md`. Key structures: `component_contracts` (props with types/defaults, ref_forwarding, polymorphic), `composition` (valid/invalid parent-child rules), and `performance` (bundle budgets, SSR requirements).

---

## Step 8: Generate the business intelligence blueprint

The business intelligence blueprint connects design system decisions to business outcomes — encoding which components serve which business goals and how component usage maps to product metrics.

### What to include

**Component-to-outcome mapping**: Which components serve which business functions:
- Conversion components (CTAs, sign-up forms, checkout flows)
- Engagement components (content cards, interactive elements, personalisation surfaces)
- Retention components (onboarding flows, empty states, re-engagement patterns)
- Trust components (security indicators, social proof, transparency patterns)

**Metric associations**: Which metrics each component category influences:
- Primary metrics (the metric the component directly affects)
- Secondary metrics (metrics affected by the component's context)
- Anti-metrics (metrics that should not be optimised at the expense of user experience)

**A/B testing guidelines**: Rules for safe experimentation:
- Which component properties are safe to experiment with (colour, copy, size)
- Which properties must remain consistent (accessibility features, core interaction patterns)
- What constitutes a significant change (requires design review vs. can be tested freely)
- How experiments should be documented back into the system

**Usage analytics hooks**: What to measure:
- Component render frequency (which components are most/least used)
- Interaction rates (which interactive components are engaged with)
- Error rates per component (which components generate the most user errors)
- Performance impact per component (which components slow down pages)

### Output format

Follow the **Business intelligence blueprint template** in `references/context-engine-blueprints.md`. Key structures: `component_outcomes` (business function, primary/secondary/anti metrics), `experimentation` (safe/never/requires_review), and `analytics` (required events with data fields).

---

## Step 9: Assemble and output the context engine

### File structure

Generate the context engine as a set of files in `.ai/context-engine/`:

```
.ai/
  context-engine/
    ux-blueprint.yml
    ui-blueprint.yml
    content-blueprint.yml
    accessibility-blueprint.yml
    ethical-blueprint.yml
    technical-blueprint.yml
    business-intelligence-blueprint.yml
    engine-manifest.yml
    usage-guide.md
```

### Engine manifest

The manifest ties the blueprints together and provides metadata for tooling. Follow the **Engine manifest template** in `references/context-engine-blueprints.md`. The manifest lists each blueprint with its file path and coverage percentage, plus a total weighted coverage score.

### Usage guide

Generate a `usage-guide.md` that teaches AI agents how to consume the engine. Follow the **Usage guide template** in `references/context-engine-blueprints.md`. The guide covers engine loading, task-based blueprint selection, and query patterns for each blueprint dimension.

---

## Recommend to the user

- Commit the context engine files alongside the codebase
- Re-generate blueprints after significant system changes (new patterns, token restructuring, accessibility policy updates)
- Start with the blueprints that address the team's most common AI-generated errors
- Reference the usage guide in any AI agent system prompt that interacts with the design system
- Treat the context engine as living documentation — update it as the system evolves

---

## Quality checks

- Every blueprint addresses its specific dimension — no overlap or duplication between blueprints
- YAML output is valid and parseable by standard YAML parsers
- Component contracts in the accessibility and technical blueprints reference the same component names used in the codebase
- Content blueprint voice and tone rules are specific to this system, not generic writing advice
- Ethical blueprint prohibitions cite specific patterns, not abstract principles
- Business intelligence blueprint connects to measurable outcomes, not aspirational goals
- The usage guide provides task-specific blueprint loading recommendations, not a generic "load everything" instruction
- Coverage percentages in the manifest are accurate — not estimated, not aspirational
