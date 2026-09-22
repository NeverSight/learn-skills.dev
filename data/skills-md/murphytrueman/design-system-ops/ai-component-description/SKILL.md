---
name: ai-component-description
description: "Generate AI-optimised text descriptions for components, formatted for Figma's MCP server and LLM consumption. This produces prose descriptions in a six-section format (purpose, props, anti-patterns, composition, accessibility, examples), NOT JSON schemas or structured data files. Trigger when someone says: write component description for AI, Figma MCP description, write the description for Claude to read, six-section description, describe this component for AI, or anything about writing text that makes components legible to LLMs. Do NOT trigger for JSON metadata schemas, structured constraint files, or programmatic tooling data — use metadata-schema-generator for those."
references:
  - ../../knowledge-notes/ai-readiness.md
  - ../../knowledge-notes/component-bestiary-reference.md
  - ../../knowledge-notes/mcp-setup-guide.md
---

# AI component description

A skill for generating structured component descriptions optimised for consumption by LLMs via Figma's MCP server. Output is a six-section description that gives an AI agent the information it needs to understand, compose, and generate from a component accurately — without relying on implicit knowledge, visual inference, or team context.

## Context

This is the differentiating skill in Design System Ops. It encodes a methodology built through production use on a real AI-assisted design system and informed by the AI-readiness patterns in the knowledge notes.

The problem it solves: most component descriptions are written for human designers discovering the component for the first time. They use phrases like "use this to show important information" or "works great in cards". These descriptions are not useless — but they are not structured for LLM consumption. An LLM reading a component description needs to know what the component IS, what it takes, what it prohibits, how it relates to other components, and what failure modes look like. Human-readable descriptions skip most of this.

The six-section format is the product of watching AI agents misuse components that had perfectly fine human documentation. The sections are not arbitrary — each one addresses a specific class of LLM error.

---

## Configuration

Before producing output, check for a `.ds-ops-config.yml` file in the project root. If present, load:
- `integrations.figma` — if enabled, auto-pull component data from Figma (see below)
- `integrations.storybook` — if enabled, pull prop definitions and story context
- `integrations.documentation` — if enabled, cross-reference existing documentation for accuracy

## Auto-pull integrations

**Figma MCP** (`integrations.figma.enabled: true`):
- Read the component node, its variants, layer structure, and existing description text from `integrations.figma.file_key`
- Extract: component name, variant names and values, layer hierarchy (for composition rules), and any existing description
- Use this as the primary source for Step 1 — skip the manual "ask for component information" step if Figma data is comprehensive
- Do not assume existing description text is accurate — it is a starting point, not a source of truth

**Storybook** (`integrations.storybook.enabled: true`):
- Fetch the component's story from `integrations.storybook.url`
- Extract: prop types, default values, and arg types from the story metadata
- Use this to validate and complete the Props section — Storybook's auto-generated prop tables are usually accurate for types and defaults

**GitHub** (`integrations.github.enabled: true`):
- Pull the component source file to read prop definitions directly from TypeScript interfaces or PropTypes
- Cross-reference with the Figma and Storybook data to ensure all three sources agree on the component's API

If an integration fails, log it and proceed with manual input.

## Step 0: Check data sources and existing description

This skill works best with a Figma MCP connection but does not require one. Before proceeding, check what data sources are available:

1. **Figma MCP available:** Read the component directly from Figma (preferred path — skip most manual questions in Step 1)
2. **Storybook / GitHub available:** Read prop definitions and source code (good alternative for the Props and Accessibility sections)
3. **Neither available:** Ask the user for component information manually — the skill still produces a complete description from user-provided input

If Figma tools are configured but fail (connection error, invalid node, nothing selected), note the error and fall back to manual input. Do not retry in a loop.

**Check for an existing description first.** When reading from Figma, always check whether the component already has a description. If it does:
- **Show it to the user** before doing anything else: "This component already has a description: [quote the existing text]. Want me to rewrite it in the six-section format, improve what's there, or start fresh?"
- Do not claim "there is no description" unless the description field is genuinely empty (null, empty string, or whitespace only)
- Do not silently discard an existing description and offer to "add" one — the user wrote that text and deserves to see it acknowledged

If the existing description already follows the six-section format, say so: "This component already has a structured description. Want me to review it for completeness, or is there a specific section you want improved?"

---

## Step 1: Gather component information

Ask for or confirm the following (skip if auto-pulled via integrations above). If the component is in a connected Figma file, use the MCP server to read it directly:

- Component name
- Component category (e.g. navigation, feedback, form, layout, data display)
- Available props/variants and their accepted values
- Default state
- Any composition relationships (what it contains, what it can be placed inside)
- Accessibility requirements already defined for the component
- Known misuse patterns observed in production (if any)

If pulling directly from Figma via MCP: read the component node, its variants, layer structure, and any existing description text. If description text exists, show it to the user (see Step 0). Do not assume existing description text is accurate — it is a starting point, not a source of truth. But do not ignore it either — existing descriptions often contain institutional knowledge that should be preserved in the rewrite.

## Step 2: Write the six-section description

Write each section in plain prose. No bullet lists inside the description itself — AI agents parse prose better than nested lists in this context. Each section should be dense but not padded.

---

### Section 1: Purpose

One to two sentences. What does this component do, and when should it be used? Write this as a contract statement, not a marketing line.

Bad: "A flexible card component for displaying content in a visually appealing way."
Good: "A surface container for grouping related content that belongs together but does not require its own page. Use when content needs visual separation from surrounding context without implying navigational hierarchy."

### Section 2: Props

Document every configurable prop. For each:
- Prop name (exact, as it appears in the component API)
- Accepted values (enumerated where finite, typed where variable)
- Default value
- One-sentence description of what the prop controls

Format: prop-name | type | default | description

Do not skip props because they seem obvious. LLMs cannot infer defaults.

Example:
```
variant | "primary" | "secondary" | "ghost" | "destructive" | "primary" | Controls visual weight and colour treatment
size | "sm" | "md" | "lg" | "md" | Adjusts padding, font size, and min-touch-target
disabled | boolean | false | Prevents interaction and applies reduced-opacity treatment
loading | boolean | false | Replaces label with loading indicator and prevents further clicks
```

### Section 3: Anti-patterns

What should an AI agent NOT do with this component? List the three to five most common misuse patterns, each as a one-sentence prohibition with a brief reason.

These anti-patterns should be specific to this component, not generic design system guidance. Write them based on actual misuse patterns if known, or inferred from the component's structure and common analogues.

Example (Button):
- Do not use the destructive variant for actions that are reversible. Destructive implies permanent data loss or deletion.
- Do not use ghost variant as the primary action in a flow. Ghost is for secondary or tertiary actions where a button is needed but should not compete with a primary.
- Do not place more than one primary variant button in the same visual context.
- Do not use size lg in dense form layouts. It creates disproportionate vertical rhythm.

#### Anti-pattern inference guide

If observed misuse patterns are not available from production data, infer likely anti-patterns from the component's API structure:

- **Components with a `variant` prop that includes "destructive" or "danger":** Likely misuse — using the destructive variant for reversible actions, or using it as a visual emphasis tool rather than a semantic signal.
- **Components with a `size` prop:** Likely misuse — using large sizes in dense layouts, or mixing sizes inconsistently within the same context.
- **Components with a boolean `disabled` prop:** Likely misuse — using disabled state to hide functionality rather than communicating why it is unavailable (missing `aria-disabled` with explanation).
- **Container components (Card, Modal, Drawer):** Likely misuse — nesting containers inside other containers without semantic justification, or using a container for visual grouping when a simpler layout element would suffice.
- **Components with an `icon` or `iconOnly` prop:** Likely misuse — using icon-only variants without providing an accessible label, or choosing icons based on aesthetics rather than meaning.
- **Components with `onClick` or action props:** Likely misuse — using a button-like component for navigation (should be a link), or attaching actions to non-interactive elements.

Use these inferences as starting points. Mark inferred anti-patterns as "anticipated" in the description — they should be validated against real usage and upgraded to "observed" once confirmed.

### Section 4: Composition rules

How does this component relate to others? Document:
- What this component can contain (if it is a container)
- What this component can be placed inside
- What other components are typically used alongside it
- Any hard constraints on nesting or ordering

Be specific. "Can be used in cards" is not useful. "Can be placed inside Card as an action — always as the last child of Card.Footer, never inside Card.Body" is useful.

### Section 5: Accessibility

Document the accessibility contract for this component:
- ARIA role(s) applied
- Keyboard interaction pattern (Tab, Enter, Space, Arrow keys, Escape — state which apply)
- Focus management behaviour (where does focus go on open/close/activate)
- Required aria attributes and their expected values
- Screen reader announcement pattern

This is not a WCAG checklist. It is the specific accessibility behaviour of this specific component.

**Why this section requires extra rigour.** Accessibility is where AI-generated components fail most often. LLMs understand accessibility theory but routinely produce code that fails basic testing — missing keyboard handlers, incomplete ARIA attributes, focus management that traps or loses focus. The description must be prescriptive enough that an AI agent generating from it produces accessible output without additional guidance.

Specific requirements:
- Specify semantic HTML elements, not just ARIA roles. If the component should render as a `<button>`, say so — an LLM may default to a `<div>` with role="button" which loses native keyboard behaviour.
- For interactive components: document both `disabled` attribute and `aria-disabled` behaviour, and state which one the component uses and why.
- For icon-only actions: require `aria-label` with a description of the action, not the icon name.
- For focus indicators: specify that focus must be visually apparent (not just functionally present). Custom focus styles must meet 3:1 contrast ratio against adjacent colours.

### Section 6: Usage examples

Two to three examples of correct usage. Each example must include three parts: the intent, the configuration, and the expected DOM output. The expected DOM output is what makes this section uniquely valuable for AI agents — it gives them a validation target, not just a generation prompt.

**Example format:**

```
Intent: [What the user is trying to accomplish]
Configuration: [Exact props/values needed]
Expected DOM output:
  [The rendered HTML structure an AI agent should produce and can validate against]
```

**Example (Button):**

```
Intent: Primary action in a confirmation dialog. Confirms the destructive action.
Configuration: variant="primary", size="md", label="Delete account"
Expected DOM output:
  <button
    type="button"
    class="btn btn-primary btn-md"
    aria-label="Delete account"
  >
    Delete account
  </button>
```

```
Intent: Secondary cancel action paired with the primary action above.
Configuration: variant="secondary", size="md", label="Cancel"
Expected DOM output:
  <button
    type="button"
    class="btn btn-secondary btn-md"
  >
    Cancel
  </button>
```

```
Intent: Icon-only close button in a modal header.
Configuration: variant="ghost", size="sm", iconOnly=true, icon="close", ariaLabel="Close dialog"
Expected DOM output:
  <button
    type="button"
    class="btn btn-ghost btn-sm btn-icon"
    aria-label="Close dialog"
  >
    <svg aria-hidden="true" class="icon icon-close">...</svg>
  </button>
```

The expected DOM output does not need to be exhaustive — it should include the elements, attributes, and structure an AI agent would need to validate correctness. Include: semantic HTML elements, ARIA attributes, class names (if predictable), and any accessibility-critical attributes. Omit: internal implementation details, event handlers, and styling properties.

**Deduplication rule:** If information in the examples section repeats what was already stated in the Props or Accessibility sections, reference it rather than restating it. The examples section adds contextual usage — it should not be a third place where prop defaults or ARIA roles are listed. If an example uses `variant="primary"`, do not re-explain what the primary variant does — the Props section already covered that.

---

## Step 2b: Prose tightness review

Before formatting, review each section for redundancy. The six sections should be complementary, not overlapping. Apply these rules:

- **Props section** is the single source of truth for what the component accepts. No other section should redefine prop types or defaults.
- **Anti-patterns section** should reference props by name without re-explaining them. "Do not use variant='destructive' for reversible actions" is sufficient — the Props section already explains what the destructive variant does.
- **Accessibility section** should reference the keyboard pattern once, not repeat interaction details from the Props section.
- **Examples section** should add contextual usage, not summarise what other sections already said.
- **Composition section** should focus on relationships, not re-describe the component's purpose.

If any section exceeds 100 words and contains information duplicated elsewhere, trim it. The target is dense precision, not comprehensive coverage through repetition.

## Step 3: Format for Figma MCP

The final description should be written as a single continuous text block suitable for pasting into Figma's component description field. Structure it with clear section headers in plain text (e.g. PURPOSE, PROPS, ANTI-PATTERNS) so an LLM scanning the description via MCP can locate sections without parsing markdown.

Total length: 300 to 600 words. Long enough to be comprehensive, short enough that the full description fits within a reasonable token budget when loaded alongside other components.

## Step 4: Generate structured JSON metadata (staff-level)

In addition to the six-section text description, produce a structured JSON metadata object for machine consumption. This metadata serves MCP servers, linters, code generators, and testing frameworks that need to parse component information programmatically.

```json
{
  "component": "[exact component name]",
  "category": "[navigation|form|feedback|layout|display|overlay]",
  "version": "[component version if available]",
  "status": "[alpha|beta|stable|deprecated]",
  "challengeRating": [CR number or null],
  "purpose": "[one-sentence purpose from Section 1]",
  "props": [
    {
      "name": "[prop name]",
      "type": "[type — e.g. 'enum', 'boolean', 'string', 'number', 'ReactNode']",
      "values": ["[accepted values if enum]"],
      "default": "[default value]",
      "required": true|false,
      "description": "[one-sentence description]"
    }
  ],
  "antiPatterns": [
    {
      "rule": "[short prohibition statement]",
      "reason": "[why this is harmful]"
    }
  ],
  "composition": {
    "canContain": ["[component names this can contain]"],
    "canBeContainedIn": ["[component names this can be placed inside]"],
    "typicallyUsedWith": ["[components commonly used alongside]"],
    "constraints": ["[hard nesting or ordering constraints]"]
  },
  "accessibility": {
    "role": "[primary ARIA role]",
    "keyboardPattern": "[named pattern — e.g. 'button', 'dialog', 'combobox', 'tabs']",
    "keyboardInteractions": {
      "Tab": "[behaviour]",
      "Enter": "[behaviour]",
      "Space": "[behaviour]",
      "Escape": "[behaviour]",
      "ArrowKeys": "[behaviour or 'N/A']"
    },
    "focusManagement": "[description]",
    "requiredAria": ["[required aria attributes]"],
    "screenReaderAnnouncement": "[what is announced]"
  },
  "tokens": ["[token names this component binds to]"],
  "composedOf": ["[system components rendered internally]"],
  "examples": [
    {
      "intent": "[what the example demonstrates]",
      "configuration": {
        "[propName]": "[value]"
      }
    }
  ]
}
```

**When to produce both formats:**
- Always produce the six-section text description (for Figma MCP and human consumption)
- Produce the JSON metadata when: the team maintains a component manifest, the system has an MCP server beyond Figma, or the team is building toward an optimised maturity stage
- If the team's maturity stage is unclear, produce both — the JSON metadata is immediately useful for tooling even if the team doesn't have an MCP server yet

**Keeping text and JSON in sync:**
- The JSON `purpose` field should be the same text as the Purpose section's first sentence
- The JSON `props` array should exactly match the Props section
- Anti-patterns and composition rules should be consistent across both formats
- If the team edits one format, flag the other as needing a sync update

## Step 5: Self-test

Before delivering the description, run a mental test: if an LLM received only this description and nothing else, could it:

1. Identify the correct component to use for a given UI requirement?
2. Configure it with the right props for a given context?
3. Avoid the three most common misuse patterns?
4. Understand where it can and cannot be placed?
5. Apply it accessibly without additional guidance?
6. Distinguish this component from the two or three most similar components in the system?
7. Generate a correct usage example that matches real-world application?

If the answer to any of these is no, revise the relevant section before delivering.

**Staff-level validation:** If structured JSON metadata was produced, additionally verify:
- Every prop in the text description appears in the JSON `props` array (and vice versa)
- The `composition.canContain` and `composition.canBeContainedIn` arrays are complete and accurate
- The `accessibility.keyboardPattern` matches a recognised pattern name
- The `tokens` array lists actual token names from the system, not generic placeholders

## Step 6: Write back to Figma (when Figma Console MCP is available)

If the Figma Console MCP from Southleft is connected (check for `figma_set_description` tool availability), write the completed description directly into the Figma component's description field. This closes the loop — the description goes from generation to Figma in a single session, visible in Dev Mode immediately.

**How to write back:**
1. Use `figma_set_description` with the component's node ID and the full six-section text description
2. For rich formatting in Dev Mode, use the `descriptionMarkdown` parameter with the markdown-formatted version
3. After writing, confirm success by reading the component description back to verify it was saved correctly

**When NOT to write back:**
- If the user asked only for a draft or preview
- If the component is in a published library and the user does not have edit access
- If the user explicitly asked for output in chat only

**When the standard Figma MCP is connected (read-only):** The description cannot be written back automatically. Present the description in chat and note that the user will need to paste it into Figma's component description field manually. If the user asks "can you write this to Figma?", explain that the standard Figma MCP is read-only and recommend the Figma Console MCP from Southleft for write-back capability.

## Quality checks

- Purpose section reads as a contract statement, not a product description
- Every prop is documented with name, type, default, and description — no props are omitted
- Anti-patterns are specific to this component, not generic advice
- Composition rules give placement constraints, not just adjacency suggestions
- Accessibility section documents the specific ARIA and keyboard behaviour, not generic WCAG reference
- Final output is a single text block formatted for Figma's description field
- Description passes the five-question self-test
- If written back to Figma, the description was verified by reading it back from the component
