---
name: people-search
description: >
  Find LinkedIn profiles of decision makers at target companies using Extruct's
  company_people_finder. Takes a company table, adds a people finder column,
  and produces a linked child people table with names, roles, and LinkedIn URLs.
  No external API credits — uses Extruct's index only.
  Triggers on: "find linkedin", "find people", "find contacts", "find decision makers",
  "people search", "linkedin search", "who to contact", "find profiles".
---

# LinkedIn Finder

Find the right people at target companies via Extruct. Produces a people table with LinkedIn profiles — no external API credits needed.

## Related Skills

```
list-segmentation → people-search → email-search → email-generation → email-response-simulation → campaign-sending
```

After you know WHICH companies to target, this skill finds WHO to contact. The next step (`email-search`) gets their verified emails and phones.

## Environment

| Variable | Service |
|----------|---------|
| `EXTRUCT_API_TOKEN` | Extruct API |

Before making API calls, check that `EXTRUCT_API_TOKEN` is set by running `test -n "$EXTRUCT_API_TOKEN" && echo "set" || echo "missing"`. If missing, ask the user to provide their Extruct API token and set it via `export EXTRUCT_API_TOKEN=<value>`. Do not proceed until confirmed.

Base URL: `https://api.extruct.ai/v1`

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Extruct table ID | Company table from `list-building` or `list-enrichment` | yes |
| Target roles | User input or context file ICP | yes |
| Max results per company | User preference (default: 5) | no |

## Workflow

### Step 0: Verify API reference

1. Read local reference: [references/api_reference.md](references/api_reference.md)
2. Fetch live docs: https://www.extruct.ai/docs
3. Compare endpoints, params, and response fields (especially `company_people_finder` column type and child table behavior)
4. If discrepancies found:
   - Update the local reference file
   - Flag changes to the user before proceeding
5. Proceed with the skill workflow

### Step 1: Confirm the table

Fetch table metadata via `GET /tables/{table_id}`. Show the user: table name, kind, row count.

### Step 2: Define roles

Ask the user: "Who are we trying to reach at these companies?"

Then expand into a role list. Use **broad role descriptions**, not exact titles — Extruct's people finder matches on role semantics, not exact title strings.

**Role list guidelines:**
- 3-7 roles is the sweet spot
- Use broad terms: "VP Sales" not "Vice President of Enterprise Sales"
- Cover the decision maker + influencer + champion if possible
- Include department variations

**Role expansion examples:**

```
User says: "Sales and ops leaders"
→ Roles: ["VP Sales", "Head of Sales", "Sales Operations", "RevOps", "Business Development", "CRO"]

User says: "People who buy data tools"
→ Roles: ["Revenue Operations", "Sales Operations", "Data Operations", "Business Intelligence", "CRM Admin"]

User says: "Innovation and strategy at corporates"
→ Roles: ["Head of Innovation", "VP Strategy", "Corporate Development", "Ventures", "Technology Scouting"]
```

**Read context file** for ICP role targets if available:
```
claude-code-gtm/context/{company}_context.md → ## ICP → Roles column
```

### Step 3: Add company_people_finder column

Create a `company_people_finder` column on the table via `POST /tables/{table_id}/columns`.

Column config shape:

```json
{
  "kind": "company_people_finder",
  "name": "Key Decision Makers",
  "key": "decision_makers",
  "value": {
    "roles": ["VP Sales", "Head of Sales", "Revenue Operations"],
    "provider": "research_pro",
    "max_results": 5
  }
}
```

| Param | Description | Recommended |
|-------|-------------|-------------|
| `roles` | Broad role descriptions to search for | 3-7 roles |
| `provider` | Search provider | `research_pro` (always) |
| `max_results` | Max people per company | 3-5 (more = slower + noisier) |

### Step 4: Trigger enrichment run

Run the new column via `POST /tables/{table_id}/run` scoped to the new column ID. Report: run ID and cells queued.

### Step 5: Monitor and discover child table

The `company_people_finder` column auto-creates a **child people table**. Fetch the parent table metadata and look at `child_relationships` for a relationship with `relationship_type: "company_people"`. That gives you the people table ID.

The child people table has auto-created columns:

| Column | Key | Kind | Description |
|--------|-----|------|-------------|
| Person Input | `input` | input | Raw person context string |
| Full Name | `full_name` | agent | Parsed full name |
| Role | `role` | agent | Current role/title |
| Profile URL | `profile_url` | agent (url) | LinkedIn URL |

### Step 6: Optionally add LinkedIn data column

For richer profile data (experience, education, skills), add a `linkedin` agent column to the people table. Config:

```json
{
  "kind": "agent",
  "key": "linkedin_data",
  "name": "LinkedIn Data",
  "value": {
    "agent_type": "linkedin",
    "prompt": "{profile_url}"
  }
}
```

This is optional — skip if you only need name + role + LinkedIn URL for the `email-search` step.

### Step 7: Fetch and review people data

Fetch data from the people table via `GET /tables/{people_table_id}/data`. Extract `full_name`, `role`, `profile_url`, and `parent_row_id` from each row.

Present summary:
- Total companies in table: N
- People found: N
- Avg people per company: N
- Companies with 0 people: N

Show a sample of 10 people for spot-checking:

| Name | Role | LinkedIn URL | Parent Company |
|------|------|-------------|----------------|
| ... | ... | ... | ... |

Ask:
- "Does the role mix look right?"
- "Any roles missing? Want to add more?"
- "Ready to proceed to `email-search` for verified emails?"

### Step 8: Export for email-search

Save the people list as CSV at `claude-code-gtm/csv/input/{campaign}/people_linkedin.csv` with columns: `full_name`, `role`, `profile_url`, `parent_row_id`.

The `email-search` skill takes this CSV (or reads the people table directly) and enriches with verified emails via contact enrichment providers (e.g. Prospeo, Fullenrich).

## Output

| Output | Format | Location |
|--------|--------|----------|
| People table | Extruct child table | Auto-created, linked to parent |
| People CSV | CSV with name, role, LinkedIn URL | `claude-code-gtm/csv/input/{campaign}/people_linkedin.csv` |

## Key Table IDs to Pass Forward

After this skill completes, pass these to `email-search`:
- **People table ID** — for direct API access to people data
- **Parent table ID** — for cross-referencing company data
- **Campaign slug** — for file paths

## API Reference

See [references/api_reference.md](references/api_reference.md) for the full `company_people_finder` column spec, child table behavior, and people table columns.
