---
name: Ops Automation Builder
description: |
  Create and manage automation rules for ops tables. Rules trigger actions when specific
  events occur -- like updating a cell when enrichment completes, pushing rows to HubSpot
  when a tag is added, or sending notifications when a new row is created.
  Use when a user says "create a rule", "automate this table", "when a cell changes do X",
  "set up automation", "notify me when", or wants to build if-this-then-that style logic
  on their ops tables. Also lists existing rules on a table.
metadata:
  author: sixty-ai
  version: "1"
  category: workflows
  skill_type: atomic
  is_active: true
  context_profile: sales
  agent_affinity:
    - prospecting
    - crm_ops
  triggers:
    - pattern: "create a rule"
      intent: "create_automation"
      confidence: 0.90
      examples:
        - "create an automation rule"
        - "add a rule to this table"
        - "set up a rule"
    - pattern: "automate"
      intent: "automation_setup"
      confidence: 0.85
      examples:
        - "automate this table"
        - "automate enrichment"
        - "set up automation for this"
    - pattern: "when cell changes"
      intent: "cell_trigger"
      confidence: 0.90
      examples:
        - "when a cell is updated"
        - "trigger on cell change"
        - "when the status column changes"
    - pattern: "set up automation"
      intent: "automation_setup"
      confidence: 0.90
      examples:
        - "build an automation"
        - "create automation"
        - "configure automation"
    - pattern: "notify me when"
      intent: "notification_rule"
      confidence: 0.85
      examples:
        - "alert me when enrichment finishes"
        - "send notification when a row is added"
        - "notify when status changes"
    - pattern: "list rules"
      intent: "list_rules"
      confidence: 0.85
      examples:
        - "show rules on this table"
        - "what automations are set up"
        - "list automations"
  keywords:
    - "rule"
    - "automate"
    - "automation"
    - "trigger"
    - "when"
    - "notify"
    - "alert"
    - "if then"
    - "condition"
    - "action"
  required_context:
    - table_id
  inputs:
    - name: table_id
      type: string
      description: "The ops table to add rules to or list rules from"
      required: true
    - name: name
      type: string
      description: "Human-readable name for the rule"
      required: false
    - name: trigger_type
      type: string
      description: "Event that triggers the rule: cell_updated, enrichment_complete, or row_created"
      required: false
    - name: condition
      type: object
      description: "Condition object defining when the rule fires (column, operator, value)"
      required: false
    - name: action_type
      type: string
      description: "Action to take: update_cell, run_enrichment, push_to_hubspot, add_tag, or notify"
      required: false
    - name: action_config
      type: object
      description: "Configuration for the action (target column, value, notification channel, etc.)"
      required: false
  outputs:
    - name: rule
      type: object
      description: "The created rule object with id, name, trigger, condition, and action"
    - name: rules_list
      type: array
      description: "List of existing rules on the table (when listing)"
  priority: medium
  tags:
    - workflows
    - automation
    - rules
    - triggers
    - ops-tables
---

## Available Context
@_platform-references/org-variables.md

# Ops Automation Builder

## Goal

Help users create and manage automation rules on their ops tables. Rules follow a simple trigger-condition-action pattern: **when** something happens (trigger), **if** a condition is met, **then** do something (action). This lets users build lightweight workflows without leaving the ops table.

## Available Actions

### 1. `create_ops_rule` -- Create Automation Rule

Creates a new rule on an ops table.

**Parameters:**
- `table_id` (required): The table to add the rule to
- `name` (required): Human-readable rule name (e.g., "Auto-enrich new rows")
- `trigger_type` (required): One of:
  - `cell_updated` -- Fires when any cell in a specified column changes
  - `enrichment_complete` -- Fires when an enrichment job finishes on the table
  - `row_created` -- Fires when a new row is added to the table
- `condition` (required): When the rule should fire. Structure:
  ```json
  {
    "column_id": "col_status",
    "operator": "equals",
    "value": "qualified"
  }
  ```
  Operators: `equals`, `not_equals`, `contains`, `not_empty`, `is_empty`, `greater_than`, `less_than`
- `action_type` (required): One of:
  - `update_cell` -- Set a cell value in the same or different column
  - `run_enrichment` -- Start an enrichment job on a column
  - `push_to_hubspot` -- Push the row to HubSpot
  - `add_tag` -- Add a tag to the row
  - `notify` -- Send a notification (in-app or Slack)
- `action_config` (required): Configuration for the action. Structure varies by action_type.

### 2. `list_ops_rules` -- List Existing Rules

Lists all automation rules on a table.

**Parameters:**
- `table_id` (required): The table to list rules for

## Trigger Types Explained

### `cell_updated`
Fires when a specific column's value changes. Best for:
- Reacting to status changes ("when status becomes 'qualified', push to HubSpot")
- Chaining enrichments ("when company_domain is filled, run email finder")
- Tagging ("when score > 80, add 'hot-lead' tag")

**Condition is required** to avoid firing on every cell edit. The condition specifies which column and value to match.

### `enrichment_complete`
Fires when an enrichment job on the table finishes. Best for:
- Chaining multiple enrichments ("after company enrichment completes, run people search")
- Post-processing ("after enrichment, run AI transform to score leads")
- Notifications ("notify me when enrichment is done")

**Condition is optional.** If omitted, fires on any enrichment completion. If provided, can filter by enrichment type.

### `row_created`
Fires when a new row is added to the table. Best for:
- Auto-enrichment ("when a lead is added, immediately run company research")
- Default values ("when a row is created, set status to 'new'")
- Notifications ("alert me when a new lead appears")

**Condition is optional.** If omitted, fires on every new row. If provided, can filter by column values (e.g., only rows where source = "inbound").

## Action Types Explained

### `update_cell`
Sets a cell value in the same row.
```json
{
  "action_type": "update_cell",
  "action_config": {
    "target_column_id": "col_status",
    "value": "enriched"
  }
}
```

### `run_enrichment`
Starts an enrichment job on a column.
```json
{
  "action_type": "run_enrichment",
  "action_config": {
    "column_id": "col_company_info",
    "enrichment_type": "company_research"
  }
}
```

### `push_to_hubspot`
Pushes the row to HubSpot as a contact.
```json
{
  "action_type": "push_to_hubspot",
  "action_config": {
    "field_mapping": {
      "email": "col_email",
      "firstname": "col_first_name",
      "lastname": "col_last_name"
    }
  }
}
```

### `add_tag`
Adds a tag to the row for filtering and organization.
```json
{
  "action_type": "add_tag",
  "action_config": {
    "tag": "hot-lead"
  }
}
```

### `notify`
Sends a notification.
```json
{
  "action_type": "notify",
  "action_config": {
    "channel": "in_app",
    "message": "Enrichment complete for table '${table_name}'"
  }
}
```
Channels: `in_app`, `slack`. Slack requires Slack integration to be configured.

## Conversation Patterns

### User wants to create a rule but is vague

Walk them through the three parts:

```
User: "Automate this table"
Assistant: "I can set up automation rules for this table. Rules have three parts:

1. **Trigger** -- what event starts it?
   - A cell value changes
   - Enrichment completes
   - A new row is added

2. **Condition** -- when should it fire?
   - e.g., 'when status equals qualified'

3. **Action** -- what should happen?
   - Update a cell, run enrichment, push to HubSpot, add a tag, or send a notification

What would you like to automate?"
```

### User describes a rule in natural language

Parse the intent and map to the rule structure:

```
User: "When enrichment finishes, tag all leads with score above 80 as hot leads"
Assistant: "I'll create this rule:
  - **Trigger**: enrichment_complete
  - **Condition**: score > 80
  - **Action**: add_tag 'hot-lead'

  Want me to set this up?"
```

### User wants to see existing rules

```
User: "What automations are on this table?"
Assistant: [Lists rules with name, trigger, condition, and action for each]
```

## Common Rule Recipes

### Auto-enrich new leads
- Trigger: `row_created`
- Condition: `email` is not empty
- Action: `run_enrichment` on company research column

### Qualify after enrichment
- Trigger: `enrichment_complete`
- Condition: none (fires on any enrichment)
- Action: `run_enrichment` on AI scoring column

### Push qualified leads to CRM
- Trigger: `cell_updated`
- Condition: `status` equals `qualified`
- Action: `push_to_hubspot`

### Notify on high-value leads
- Trigger: `cell_updated`
- Condition: `score` greater than 90
- Action: `notify` via Slack

### Tag by enrichment results
- Trigger: `enrichment_complete`
- Condition: `company_size` greater than 100
- Action: `add_tag` "enterprise"

## Error Handling

### Invalid trigger_type
Tell the user the valid options: `cell_updated`, `enrichment_complete`, `row_created`.

### Invalid action_type
Tell the user the valid options: `update_cell`, `run_enrichment`, `push_to_hubspot`, `add_tag`, `notify`.

### Column not found
If the condition or action references a column that does not exist on the table, inform the user and suggest available columns.

### Rule conflicts
If creating a rule that could conflict with an existing rule (e.g., two rules updating the same cell on the same trigger), warn the user and ask for confirmation.

## Guidelines

- Always confirm the rule with the user before creating it -- show the parsed trigger/condition/action
- Use descriptive rule names that explain what the rule does (e.g., "Tag hot leads after enrichment")
- Suggest common recipes when the user is unsure what to automate
- When listing rules, format them clearly with trigger, condition, and action on separate lines
- Warn about potential loops (e.g., rule A updates cell -> triggers rule B -> updates cell -> triggers rule A)
