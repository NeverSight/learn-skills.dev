---
name: component-decision-tree
description: "Build queryable decision trees that help agents and teams choose between components — structured YAML files mapping user intents to the correct component through a sequence of narrowing questions. This produces selection logic for choosing BETWEEN components, NOT usage guidelines for a single component. Trigger when someone says: component decision tree, which component should I use, help me choose between, selection guide, decision framework, modal vs dialog, intent-to-component mapping, or anything about creating structured logic for picking the right component from alternatives. Do NOT trigger for usage guidance on a specific component — use usage-guidelines for that."
references:
  - ../../knowledge-notes/ai-readiness.md
  - ../../knowledge-notes/component-bestiary-reference.md
---

# Component decision tree

A skill for building structured decision trees that map user intents and requirements to specific component selections. The output is a queryable framework that AI agents traverse to select the right component for a given need — eliminating the guesswork that leads to component misuse, duplication, and inconsistency.

## Context

Component selection is the first decision in any design system interaction, and it is the one that AI agents get wrong most often. The failure mode is not random — it follows predictable patterns. An agent selects a Modal when a Dialog was appropriate. It uses a Card where a List Item fits better. It creates a custom component because it could not find the existing one that serves the need.

These errors have the same root cause: the agent does not have a decision framework. It has a list of components (if it has anything at all) and it pattern-matches the user's request against component names and descriptions. This works when the match is obvious ("I need a button" → Button) and fails when the match requires judgment ("I need to show a collection of items that users can filter and sort" → is that a Table, a DataGrid, a List with filters, or a custom composition?).

Decision trees encode the judgment. Instead of relying on an agent's ability to infer the right component from a description, the tree asks a structured sequence of questions that narrow the selection to the correct component. The questions are the same ones a senior designer or developer would ask when advising a junior team member.

The practical output is a structured file that agents load alongside component metadata. When an agent receives a request, it traverses the decision tree first to identify the component, then loads the component's metadata for configuration details.

## Boundaries

This skill produces decision trees for component selection — choosing between components. It does not document how to use a single component once selected (use `usage-guidelines` for that) or generate component metadata schemas (use `metadata-schema-generator`). If the system has fewer than 5 components, a decision tree adds overhead without value — a simple component index is sufficient. If no component inventory exists, run `component-audit` or `codebase-index` first to establish one.

---

## Configuration

Before producing output, check for a `.ds-ops-config.yml` file in the project root. If present, load:
- `system.component_paths` — directs scanning to component directories
- `system.category_model` — determines top-level decision tree branches (atomic, functional, custom)
- `integrations.*` — enables auto-pull for component data
- `decision_tree.output_format` — output format preference (JSON or YAML, default: YAML)

## Auto-pull integrations

If integrations are configured in `.ds-ops-config.yml`, pull data automatically:

**Figma MCP** (`integrations.figma.enabled: true`):
- Read the published component library from `integrations.figma.file_key`
- Extract component names, descriptions, and variant structures
- Use descriptions as input for decision node generation

**Storybook** (`integrations.storybook.enabled: true`):
- Fetch the story index for a complete component list
- Extract documented use cases from story titles and descriptions

**Codebase index** (`.ai/index/component-inventory.yml`):
- If a codebase index exists, load the component inventory and relationship graph
- Use category assignments and relationship data to inform tree structure

If an integration fails, log it and proceed with available sources.

---

## Step 1: Map the component landscape

Before building decision trees, understand what components exist and how they cluster.

**Component inventory**: List every component with its purpose and category. If a codebase index exists, use it. If not, scan the component directories.

**Functional clusters**: Group components by the user need they serve, not by their technical category. A single user need often spans multiple components:

| User need | Components that serve it |
|---|---|
| Show a notification | Toast, Banner, Alert, InlineMessage, Snackbar |
| Collect user input | Input, TextArea, Select, Combobox, DatePicker, Checkbox, Radio, Switch |
| Navigate between views | Tabs, Sidebar, Breadcrumb, Pagination, BottomNav |
| Display a collection | Table, DataGrid, List, CardGrid, Timeline |
| Confirm an action | Dialog, ConfirmationModal, AlertDialog |
| Show contextual info | Tooltip, Popover, HoverCard, Dropdown |

**Overlap analysis**: Identify components with overlapping use cases. These are the decision points where agents (and humans) get confused:

| Component A | Component B | Distinguishing factor |
|---|---|---|
| Modal | Dialog | Modal blocks the page; Dialog is for focused tasks with a specific outcome |
| Toast | Banner | Toast is transient and non-blocking; Banner persists until dismissed |
| Select | Combobox | Select has a fixed option list; Combobox allows search/filter |

Ask for or confirm:
- Are there components that teams frequently confuse or misuse? (These are high-priority decision points)
- Are there component selection decisions that are currently undocumented and rely on tribal knowledge?
- Are there recent cases where an AI agent or a new team member selected the wrong component?

---

## Step 2: Build the intent taxonomy

Define the intents that drive component selection. Intents are what the user or agent is trying to accomplish, expressed independently of any specific component.

### Intent categories

**Display intents** — showing information to the user:
- Display a single value
- Display a list of items
- Display a data table
- Display a status or state
- Display a notification or alert
- Display contextual help
- Display a media item
- Display a summary or overview

**Input intents** — collecting information from the user:
- Collect a text value
- Collect a selection from options
- Collect a date or time
- Collect a boolean choice
- Collect a file
- Collect a complex form
- Collect a search query

**Action intents** — enabling the user to do something:
- Trigger a primary action
- Trigger a secondary action
- Navigate to a destination
- Confirm a destructive action
- Open a menu of actions
- Toggle a state

**Layout intents** — organising content on a page:
- Group related content
- Separate content sections
- Create a navigable structure
- Establish visual hierarchy
- Contain an interactive flow

### Intent format

```yaml
intents:
  display_notification:
    description: "Show feedback about an action or system event"
    qualifiers:
      persistence: ["transient", "persistent", "dismissible"]
      severity: ["success", "warning", "error", "info"]
      position: ["inline", "overlay", "page-level"]
      blocking: ["blocks_interaction", "non_blocking"]
```

---

## Step 3: Build the decision trees

For each functional cluster, build a decision tree that maps intents and qualifiers to component selections.

### Tree structure

Each node in the tree is either a **question node** (asks a qualifying question) or a **leaf node** (resolves to a component).

```yaml
decision_trees:
  notification:
    description: "Select the right component for showing feedback or notifications"
    root:
      question: "Does the notification need to persist until the user dismisses it?"
      options:
        yes:
          question: "Is the notification related to the current page/section or the whole application?"
          options:
            current_section:
              question: "Is it inline with the content or separate from it?"
              options:
                inline:
                  resolve: "InlineMessage"
                  confidence: "high"
                  rationale: "Inline messages appear within the content flow for contextual feedback"
                separate:
                  resolve: "Alert"
                  confidence: "high"
                  rationale: "Alerts appear as distinct blocks for section-level notifications"
            whole_application:
              resolve: "Banner"
              confidence: "high"
              rationale: "Banners span the full width for application-level persistent messages"
        no:
          question: "Does the user need to take action based on the notification?"
          options:
            yes:
              resolve: "Toast"
              confidence: "medium"
              rationale: "Toasts with action buttons for transient but actionable feedback"
              notes: "If the action is critical, consider a persistent Alert instead"
            no:
              resolve: "Toast"
              confidence: "high"
              rationale: "Standard toast for transient, informational feedback"
```

### Decision node requirements

Every question node must:
- Ask a single, unambiguous question
- Have mutually exclusive answer options (no overlap between paths)
- Be answerable from the user's requirements (not require implementation knowledge)

Every leaf node must:
- Resolve to exactly one component
- Include a confidence level (high, medium, low)
- Include a rationale explaining why this component fits
- Include notes for edge cases or exceptions where the selection might change

### Confidence levels

- **High**: The decision tree path unambiguously leads to this component. No reasonable alternative exists.
- **Medium**: This is the best fit, but an alternative exists for specific edge cases. The notes field describes the alternative.
- **Low**: Multiple components could serve this need. The tree suggests one based on the most common use case, but the consumer should verify.

---

## Step 4: Add disambiguation nodes

For component pairs that are frequently confused, add explicit disambiguation:

```yaml
disambiguation:
  modal_vs_dialog:
    trigger: "Agent or user is uncertain between Modal and Dialog"
    question: "What is the user doing in this overlay?"
    options:
      completing_a_focused_task:
        description: "The user is filling a form, making a selection, or completing a workflow step"
        resolve: "Dialog"
        rationale: "Dialogs are task-oriented — they have a clear completion action"
      viewing_content:
        description: "The user is reading information, viewing details, or previewing content"
        resolve: "Modal"
        rationale: "Modals present content without a specific task completion flow"
      confirming_an_action:
        description: "The user is confirming or cancelling a specific action"
        resolve: "ConfirmationDialog"
        rationale: "Confirmation dialogs are specialised for binary confirm/cancel decisions"

  select_vs_combobox:
    trigger: "Agent or user is uncertain between Select and Combobox"
    question: "How many options are there, and does the user know what they're looking for?"
    options:
      few_options_user_browses:
        description: "Fewer than 15 options, user scans the list"
        resolve: "Select"
        rationale: "Select is simpler and appropriate when the option set is scannable"
      many_options_user_searches:
        description: "More than 15 options or user typically knows what they want"
        resolve: "Combobox"
        rationale: "Combobox adds search/filter capability for large or known-target option sets"
      options_are_dynamic:
        description: "Options are loaded from an API or depend on user input"
        resolve: "Combobox"
        rationale: "Combobox supports async loading and filtered results"
```

---

## Step 5: Generate the output

### File structure

```
.ai/decision-trees/
  trees/
    notification.yml
    input.yml
    navigation.yml
    layout.yml
    action.yml
    overlay.yml
  disambiguation/
    modal-vs-dialog.yml
    select-vs-combobox.yml
    ...
  intent-taxonomy.yml
  decision-tree-manifest.yml
  query-guide.md
```

### Manifest

```yaml
decision_tree_manifest:
  version: "1.0"
  generated: "[date]"
  system: "[design system name]"
  trees:
    - id: notification
      file: trees/notification.yml
      components_covered: ["Toast", "Banner", "Alert", "InlineMessage"]
      depth: 3
    - id: input
      file: trees/input.yml
      components_covered: ["Input", "TextArea", "Select", "Combobox", "DatePicker"]
      depth: 4
  disambiguation:
    - id: modal_vs_dialog
      file: disambiguation/modal-vs-dialog.yml
      components: ["Modal", "Dialog", "ConfirmationDialog"]
  coverage:
    components_in_trees: 45
    components_total: 55
    coverage_percentage: "82%"
    uncovered: ["Spacer", "Divider", "VisuallyHidden", "Portal"]
    uncovered_reason: "Utility components that do not require selection logic"
```

### Query guide

```markdown
# Decision tree query guide

## How agents should use these trees

1. Identify the user's intent from their request
2. Map the intent to a tree using intent-taxonomy.yml
3. Traverse the tree by answering each question from the user's requirements
4. If the resolution confidence is "medium" or "low", present the suggestion
   with the alternative noted in the leaf node
5. If the user's requirements do not clearly answer a tree question,
   ask for clarification rather than guessing

## Handling ambiguity

If two tree paths seem equally valid:
→ Check the disambiguation section for the specific component pair
→ If no disambiguation exists, present both options with rationale
→ Never silently pick one when the decision is genuinely ambiguous

## Components not in any tree

Some components do not need decision trees because their use case
is unambiguous (Button, Icon) or because they are utility components
(Spacer, Portal). For these, direct name matching is sufficient.

## Updating the trees

Decision trees should be updated when:
- A new component is added that serves an existing intent
- A component is deprecated and its alternatives need to be reflected
- Team feedback indicates a decision node is ambiguous or misleading
- A disambiguation case is identified from real-world confusion
```

---

## Recommend to the user

- Start with the functional clusters where component confusion is most common — these have the highest return
- Validate decision trees with real scenarios from the team's recent work
- Include disambiguation nodes for every component pair that has caused confusion in the past
- Review uncovered components — utility components genuinely do not need trees, but any component that a user might need to choose between should be covered
- Commit the decision trees alongside component metadata and update them when components are added, deprecated, or significantly changed

---

## Quality checks

- Every decision tree path terminates at a leaf node (no dead ends)
- Question options are mutually exclusive (no overlap between paths)
- Every component that could reasonably be confused with another is covered by either a tree or a disambiguation node
- Confidence levels are honest — "high" means there is genuinely no reasonable alternative, not that the tree author is confident
- Rationale in leaf nodes explains why this component fits, not just which component it is
- The query guide provides clear instructions for handling ambiguity
- Coverage percentage in the manifest is accurate and uncovered components have documented reasons for exclusion
- Decision trees are traversable from user requirements alone — no question requires implementation knowledge or system internals to answer
