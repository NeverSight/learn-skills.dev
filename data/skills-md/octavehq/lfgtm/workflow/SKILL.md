---
name: workflow
description: Define, run, and manage multi-step GTM workflows with human-in-the-loop execution. Use when user says "run a workflow", "show workflows", "create a workflow", "automate this process", or references workflow-based tasks.
---

# /octave:workflow - GTM Workflow Engine

Define, run, and manage multi-step GTM workflows. Chain research, qualification, generation, and agent tools into reusable recipes. Ship with built-in templates or create your own.

## Usage

```
/octave:workflow [subcommand] [options]
```

## Subcommands

```
/octave:workflow                                          # List available workflows
/octave:workflow list                                     # List available workflows
/octave:workflow show "Full Outbound Pipeline"           # Show workflow details
/octave:workflow run "Full Outbound Pipeline" --company acme.com
/octave:workflow run "Full Outbound Pipeline" --company acme.com --auto
/octave:workflow create                                   # Build a new workflow interactively
```

## Examples

```
# List all workflows (templates + your custom ones)
/octave:workflow list

# See what a workflow does before running it
/octave:workflow show "Account-Based Research"

# Run a workflow with required inputs
/octave:workflow run "Full Outbound Pipeline" --company stripe.com

# Run with all options
/octave:workflow run "Competitive Deal Prep" --company acme.com --contact john@acme.com --competitor "Salesforce"

# Run without pausing between steps
/octave:workflow run "Full Outbound Pipeline" --company acme.com --auto

# Create a custom workflow
/octave:workflow create
```

## Instructions

When the user runs `/octave:workflow`:

### Subcommand: list (default)

Show all available workflows from both template and user directories.

**Discovery:**
1. Read `.workflow.md` files from the plugin's `workflows/` directory (templates)
2. Read `.workflow.md` files from `~/.octave/workflows/` (user-created)
3. Parse YAML front matter from each file

**Output Format:**
```
AVAILABLE WORKFLOWS
===================

TEMPLATES (4)
-------------

1. Full Outbound Pipeline
   Company research → qualify → find contacts → qualify → email outreach
   Inputs: company_domain (required), persona, num_contacts
   Run: /octave:workflow run "Full Outbound Pipeline" --company <domain>

2. Account-Based Research
   Deep research dossier on a target account with contact mapping
   Inputs: company_domain (required), num_contacts
   Run: /octave:workflow run "Account-Based Research" --company <domain>

3. Competitive Deal Prep
   Research + competitive positioning + tailored displacement outreach
   Inputs: company_domain (required), contact_email (required), competitor_name (required)
   Run: /octave:workflow run "Competitive Deal Prep" --company <domain> --contact <email> --competitor <name>

4. Persona-Targeted Outreach
   Find people matching a persona across companies and generate outreach
   Inputs: persona_name (required), industry, min_company_size
   Run: /octave:workflow run "Persona-Targeted Outreach" --persona "CTO"

---

MY WORKFLOWS (2)
-----------------

1. Security Team Outreach
   Find and reach security decision-makers at target companies
   Inputs: company_domain (required), num_contacts
   Run: /octave:workflow run "Security Team Outreach" --company <domain>

2. Partner Channel Mapping
   Research potential partners and their GTM teams
   Inputs: company_domain (required)
   Run: /octave:workflow run "Partner Channel Mapping" --company <domain>

---

Use /octave:workflow show <name> for details.
Use /octave:workflow create to build a new workflow.
```

If `~/.octave/workflows/` doesn't exist or is empty, show only templates and note:

```
MY WORKFLOWS (0)
-----------------
No custom workflows yet.
Use /octave:workflow create to build your first one.
```

### Subcommand: show <name>

Show detailed information about a specific workflow.

**Actions:**
1. Locate the workflow file (fuzzy match on name across both directories)
2. Parse front matter and step definitions
3. Present full details

**Output Format:**
```
Workflow: Full Outbound Pipeline
=================================
Source: Template
Author: octave
Tags: outbound, prospecting, email

Description:
Research a target company, qualify it against ICP, find decision-makers,
qualify them, and generate personalized outreach.

Inputs:
-------
- company_domain (string, REQUIRED) - Target company domain (e.g., acme.com)
- persona (string, optional) - Target persona name from library [default: auto-detect]
- num_contacts (number, optional) - Number of contacts to find [default: 5]

Steps (8):
----------
1. Research Company          → enrich_company
2. Qualify Company           → qualify_company
3. Review Company Fit        → decision (if score < 50, warn user)
4. Find Decision Makers      → find_person
5. Qualify Top Contact       → qualify_person
6. Select Contact            → decision (user picks contact)
7. Generate Email Sequence   → generate_email
8. Present Results           → output summary

---

Run this workflow:
/octave:workflow run "Full Outbound Pipeline" --company acme.com
/octave:workflow run "Full Outbound Pipeline" --company acme.com --persona "CTO" --num-contacts 10
/octave:workflow run "Full Outbound Pipeline" --company acme.com --auto
```

### Subcommand: run <name>

Execute a workflow step by step.

**Step 1: Locate and Parse**

1. Find the workflow file (fuzzy match on name)
2. Parse YAML front matter for inputs and metadata
3. Parse step definitions from markdown body

If not found:
```
Workflow "XYZ" not found.

Available workflows:
- Full Outbound Pipeline
- Account-Based Research
- Competitive Deal Prep
- Persona-Targeted Outreach

Use /octave:workflow list to see all workflows.
```

**Step 2: Collect Inputs**

Prompt the user for each required input. Apply defaults for optional inputs.

```
Running: Full Outbound Pipeline
================================

Required inputs:
  company_domain: [user provides or from --company flag]

Optional inputs (press Enter for defaults):
  persona [auto-detect]:
  num_contacts [5]:
```

If using command-line flags, map them: `--company` → `company_domain`, `--persona` → `persona`, `--contact` → `contact_email`, `--competitor` → `competitor_name`.

**Step 3: Execute Steps**

Process each step sequentially, maintaining a **context map** that stores all input values and `save_as` results from prior steps.

**For tool steps:**
```
STEP 1/8: Research Company
──────────────────────────
Get detailed intelligence on the target company.

Tool: enrich_company
Params: { companyDomain: "acme.com" }

Executing...

Result: Acme Corp
  Industry: B2B SaaS
  Employees: 450
  Stage: Series C
  Location: San Francisco, CA
  Recent: Raised $50M Series C in Q3 2025

[Enter to continue, or type feedback]
```

After execution:
- Save the result to the context map under the step's `save_as` name
- Show a brief summary of the result
- Wait for user acknowledgment (unless `--auto` mode)

**For decision steps:**
```
STEP 3/8: Review Company Fit
─────────────────────────────
Company qualification score: 42/100

This is below the recommended threshold of 50.

Options:
1. Continue anyway - proceed with outreach despite low score
2. Stop here - end the workflow
3. Find similar companies - pivot to better-fit alternatives

Your choice:
```

Wait for user selection and branch accordingly.

In `--auto` mode:
- If the condition is NOT met (e.g., score >= 50), auto-continue
- If the condition IS met (e.g., score < 50), auto-select the first option (continue) but flag it:
  ```
  [AUTO] Score 42/100 is below threshold. Continuing anyway (auto mode).
  ```

**For output steps:**
Render the output template with all values from the context map:
```
STEP 8/8: Results
──────────────────

OUTBOUND PIPELINE COMPLETE
===========================
Company: Acme Corp (acme.com)
ICP Score: 78/100 - GOOD FIT
Contact: Sarah Chen (CTO)
Persona Fit: 85/100

---

EMAIL 1: Initial Outreach
Subject: Reducing engineering overhead at Acme
[Full email content...]

EMAIL 2: Value Follow-Up (Day 3)
Subject: How TechCorp cut deployment time by 60%
[Full email content...]

[Continue for all emails...]

---

Personalization used:
- Company: Acme Corp (450 employees, Series C)
- Matched persona: CTO - Enterprise Tech
- Playbook: Enterprise DevOps Sale

---

Next steps:
1. Deliver to your tools (I'll check for MCP connectors first)
2. Research additional contacts (/octave:research)
3. Run this workflow for another company
4. Adjust and re-run for a different contact
```

**Step 4: Completion**

After all steps complete:
```
Workflow complete! (8/8 steps)

Summary:
- Company: Acme Corp - Score: 78/100
- Contact: Sarah Chen, CTO - Fit: 85/100
- Generated: 4-email sequence

Would you like to:
1. Deliver to your tools (sequencer, CRM, Drive, Gamma, etc.)
2. Run again for another company
3. Run for a different contact at Acme
4. Done
```

**Step 5: Deliver Results**

When the user selects "Deliver to your tools", follow this MCP-first approach:

**Phase 1: Detect likely destination from workflow output**

Map the workflow output type to a recommended destination:
- Email sequences → Email sequencer (Outreach, Apollo, Salesloft, Instantly)
- Account research / call prep → CRM (Salesforce, HubSpot, Pipedrive)
- Content / collateral → Documents (Google Docs, Notion, Confluence)
- Presentations → Slides (Gamma, Google Slides, PowerPoint)
- Reports / data → File export (CSV, markdown, HTML)

**Phase 2: Check for MCP connectors**

```
# Check what MCP servers the user has connected
ListMcpResourcesTool()

# Look for tool-specific MCP servers:
# - Google Drive MCP → can write docs directly
# - Salesforce/HubSpot MCP → can create CRM records
# - Slack MCP → can post to channels
# - Notion MCP → can create pages
# - Any other connected MCP server
```

**Phase 3: Branch based on what's available**

**If matching MCP server found:**
```
I can push these results directly to [Tool] via your connected MCP server.

Detected: [MCP Server Name] connected
Destination: [specific location — e.g., Drive folder, CRM object, Slack channel]

Ready to push? (yes / choose a different destination)
```

Use the MCP server's tools to write/push the output directly.

**If no matching MCP server found, ask for destination:**
```
Where should these results go?

OUTREACH & SEQUENCERS
1. Outreach / Apollo / Salesloft / Instantly

CRM
2. Salesforce / HubSpot / Pipedrive

DOCUMENTS
3. Google Docs / Notion / Confluence

PRESENTATIONS
4. Gamma / Google Slides / PowerPoint

COMMUNICATION
5. Slack / Email

MARKETING AUTOMATION
6. Marketo / Pardot / Mailchimp

FILE EXPORT
7. Local file (markdown, HTML, CSV, plain text)

8. Keep in conversation (already displayed)

Your choice (or name your tool):
```

After the user picks a destination, check for MCP:
```
Do you have an MCP server for [Tool] connected?

If yes → Connect it and I'll push directly.
If no → I'll format the output for easy import.
```

**Phase 4: Format for import (when no MCP connector)**

Recommend the best format based on destination, then generate:

| Destination | Recommended Format | Why |
|---|---|---|
| Outreach / Apollo / Salesloft / Instantly | CSV (Step, Subject, Body, Wait Days) | Direct sequence import |
| Salesforce / HubSpot / Pipedrive | Structured text (Account Summary, Stakeholders, Next Steps) | Paste into notes/activity fields |
| Google Docs | Clean markdown with headers | Import or paste preserves structure |
| Notion | Markdown with toggles/callouts | Native Notion markdown support |
| Confluence | Markdown or HTML | Paste into Confluence editor |
| Gamma | Numbered slide outline (Title + bullets per slide) | Paste into Gamma "Generate" |
| Google Slides / PowerPoint | Slide outline with speaker notes | Copy into slide builder |
| Slack | Formatted message blocks | Post as Slack message |
| Email (direct) | HTML email or plain text | Send or paste into email client |
| Marketo / Pardot | HTML email templates | Import as email template |
| Mailchimp | HTML email with merge tags | Import as campaign |
| Local file | User choice: `.md`, `.html`, `.csv`, `.txt` | Write to `./octave-output/<workflow>-<date>.<ext>` |

Present as:
```
For [Tool], I recommend: [Format]
[Brief reason why this format works best]

Other options:
- [Alternative format 1]
- [Alternative format 2]

Which format? (or press Enter for recommended):
```

Write the formatted output using Claude's Write tool (for files) or display inline (for paste targets).

---

**Variable Resolution:**

When executing steps, resolve `{{variable}}` references from the context map:
- `{{company_domain}}` → input value
- `{{company_profile}}` → full result from the step that saved as `company_profile`
- `{{company_profile.name}}` → specific field from a saved result
- `{{contacts[0]}}` → first item from an array result
- `{{persona_titles}}` → derived from persona lookup (Claude resolves intelligently)

Claude should resolve these references naturally from context. The `{{}}` syntax is a guide, not a rigid template engine — Claude understands what data to pass between steps.

### Subcommand: create

Build a new workflow interactively and save it to `~/.octave/workflows/`.

**Step 1: Understand the Goal**

```
Let's create a new workflow!

What should this workflow accomplish?
(Describe the end-to-end process in your own words)
```

Example user input:
> "I want to research a company, find their security team, check if they match our ICP, and then generate a security-focused email sequence."

**Step 2: Define Delivery Destination**

Ask where the workflow results should go:
```
Where do you want the results delivered?

1. Email sequencer (Outreach, Apollo, Salesloft, Instantly)
2. CRM (Salesforce, HubSpot, Pipedrive)
3. Documents (Google Docs, Notion, Confluence)
4. Presentations (Gamma, Google Slides, PowerPoint)
5. Communication (Slack, Email)
6. Marketing automation (Marketo, Pardot, Mailchimp)
7. Local file (markdown, HTML, CSV, plain text)
8. Conversation only — no delivery step needed
```

This gets saved in the workflow file so it knows where to deliver on repeat runs.

**Step 3: Suggest a Structure**

Based on the user's description, Claude proposes a workflow:

```
Great! Here's a suggested workflow:

Workflow: Security Team Outreach
Description: Research a company, find security decision-makers, qualify, and generate targeted outreach

Inputs:
- company_domain (string, required) - Target company domain
- num_contacts (number, optional, default 3) - Number of security contacts to find

Steps:
1. Research Company → enrich_company
   Get company intelligence, tech stack, and security posture signals

2. Qualify Company → qualify_company
   Score against ICP with security focus

3. Review Fit → decision
   If score < 50, warn and offer to stop

4. Find Security Team → find_person
   Search for CISO, VP Security, Head of Security, Security Director

5. Enrich Top Contact → enrich_person
   Deep research on the best-fit security contact

6. Qualify Contact → qualify_person
   Score against security-focused persona criteria

7. Generate Outreach → generate_email
   Security-focused email sequence with relevant proof points

8. Present Results → output
   Full summary with emails and next steps

Does this look right? (yes / adjust / add steps / remove steps)
```

**Step 4: Refine**

If user says "adjust":
```
What would you like to change?

1. Add a step
2. Remove a step
3. Reorder steps
4. Change an input
5. Modify a step's details

Your choice:
```

Iterate until user confirms.

**Step 5: Generate and Save**

1. Generate the `.workflow.md` file content
2. Create `~/.octave/workflows/` directory if it doesn't exist
3. Write to `~/.octave/workflows/<kebab-case-name>.workflow.md`
4. Confirm:

```
Saved workflow: Security Team Outreach
Location: ~/.octave/workflows/security-team-outreach.workflow.md

Run it now:
/octave:workflow run "Security Team Outreach" --company acme.com

Or list all workflows:
/octave:workflow list
```

### Workflow File Format Reference

Workflows are `.workflow.md` files with YAML front matter and markdown step definitions.

**Front Matter (YAML):**
```yaml
---
name: Workflow Display Name
description: One-line description of what the workflow does
author: username          # optional
tags: [tag1, tag2]        # optional
inputs:
  - name: variable_name
    type: string          # string, number, or boolean
    required: true        # or false
    description: Human-readable description
    default: value        # optional, for non-required inputs
delivery:                 # optional — where to deliver results
  destination: outreach | apollo | salesloft | instantly | salesforce | hubspot | pipedrive | google_docs | notion | confluence | gamma | google_slides | slack | email | marketo | mailchimp | local_file | conversation
  format: csv | markdown | html | plain_text | slide_outline | crm_notes
---
```

**Steps (Markdown):**

Each step is an `### Step N: Name` heading followed by key-value fields:

**Tool step:**
```markdown
### Step N: Step Name
tool: mcp_tool_name
params:
  paramName: "{{variable_or_literal}}"
  otherParam: "literal value"
save_as: result_name
description: What this step does and why.
```

**Decision step:**
```markdown
### Step N: Step Name
type: decision
condition: "result_name.field < threshold"
prompt: |
  Explanation of the decision.
  Options:
  1. First option
  2. Second option
  3. Third option
```

**Output step:**
```markdown
### Step N: Step Name
type: output
template: |
  WORKFLOW RESULTS
  ================
  Key result: {{saved_result.field}}
  Other data: {{another_result.field}}
```

**Available MCP Tools for Steps:**

Any MCP tool from the Octave server can be used in a workflow step:

| Phase | Tools |
|-------|-------|
| Research | `find_company`, `find_person`, `find_similar_companies`, `find_similar_people`, `enrich_company`, `enrich_person` |
| Qualify | `qualify_company`, `qualify_person` |
| Library | `list_all_entities`, `get_entity`, `get_playbook`, `search_knowledge_base`, `list_value_props` |
| Generate | `generate_email`, `generate_content`, `generate_call_prep` |
| Agents | `run_email_agent`, `run_content_agent`, `run_call_prep_agent`, `run_enrich_person_agent`, `run_enrich_company_agent`, `run_qualify_person_agent`, `run_qualify_company_agent` |
| Write | `create_entity`, `create_playbook`, `update_entity`, `update_playbook` |
| Deliver | `ListMcpResourcesTool` (discover connected MCP servers), any connected MCP server tools (Google Drive, Salesforce, Slack, etc.), Write tool (local files) |

## MCP Tools Used

This skill dynamically invokes MCP tools based on workflow step definitions. Any tool available through the Octave MCP server can be used within a workflow step.

**Core tools used by the skill itself:**
- File system tools (Read, Glob) to discover and parse workflow files
- Write tool to save user-created workflows

**Tools commonly used in workflow steps:**
- `enrich_company` / `enrich_person` - Research steps
- `qualify_company` / `qualify_person` - Qualification steps
- `find_person` / `find_company` - Discovery steps
- `generate_email` / `generate_content` - Generation steps
- `get_entity` / `get_playbook` - Library lookup steps
- `search_knowledge_base` - Context gathering steps
- `run_email_agent` / `run_content_agent` - Agent execution steps

## Error Handling

**Workflow Not Found:**
> Workflow "XYZ" not found.
>
> Available workflows:
> - Full Outbound Pipeline
> - Account-Based Research
> - Competitive Deal Prep
> - Persona-Targeted Outreach
>
> Use /octave:workflow list to see all workflows.

**Missing Required Input:**
> Workflow "Full Outbound Pipeline" requires the following input:
> - company_domain: Target company domain (e.g., acme.com)
>
> Usage: /octave:workflow run "Full Outbound Pipeline" --company <domain>

**Tool Call Failure During Execution:**
> Step 4 failed: find_person returned an error.
> Error: <error message>
>
> Options:
> 1. Retry this step
> 2. Skip and continue to next step
> 3. Stop the workflow
>
> Your choice:

**User Workflows Directory Missing:**
If `~/.octave/workflows/` doesn't exist when listing or creating:
- For `list`: Show only templates, note "No custom workflows yet"
- For `create`: Create the directory automatically before saving

**Invalid Workflow File:**
> Could not parse workflow file: <filename>
> Error: <parsing error>
>
> The workflow file may be malformed. Use /octave:workflow show <name> to check,
> or edit the file manually at: <file path>

## Related Skills

- `/octave:research` - Deep dive research (individual steps of a workflow)
- `/octave:generate` - Content generation (commonly used as workflow steps)
- `/octave:prospector` - Prospecting with ICP criteria (similar to outbound workflow)
- `/octave:explore-agents` - Run saved agents (can be used within workflow steps)
- `/octave:library` - Library management (workflows reference library entities)
- `/octave:brainstorm` - Ideation (brainstorm → create workflow → run workflow)
