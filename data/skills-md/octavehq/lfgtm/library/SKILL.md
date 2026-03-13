---
name: library
description: Browse, search, create, and update Octave library entities (personas, products, playbooks, segments, competitors, proof points, references). Use when user says "show my personas", "list products", "create a competitor", "update this segment", "search the library", or references any entity type by name.
---

# /octave:library - Library Management

Browse, search, create, and update Octave library entities.

## Trigger

User runs `/octave:library` with subcommands:
- `/octave:library list <type>` - List entities of a type
- `/octave:library search <query>` - Semantic search across library
- `/octave:library show <oId>` - Show full entity details
- `/octave:library create <type> "<name>"` - Create new entity
- `/octave:library update <oId>` - Update existing entity

Or natural language like:
- "Show me all personas"
- "What playbooks do we have?"
- "Create a new persona for CTOs"
- "Update the enterprise segment"

## Instructions

**Entity Type Mapping:**

```yaml
# Library entities
personas:       { prefix: pe_ }
products:       { prefix: px_ }
services:       { prefix: px_ }  # Services share the product prefix
playbooks:      { prefix: pb_ }
segments:       { prefix: sg_ }
use-cases:      { prefix: uu_ }
competitors:    { prefix: cp_ }
proof-points:   { prefix: pp_ }
references:     { prefix: re_ }
brand-voices:   { prefix: bv_ }
writing-styles: { prefix: ws_ }

# Other common oId prefixes
agents:         { prefix: ca_ }  # ContentAgent - all agent types
value-props:    { prefix: hy_ }
workspaces:     { prefix: wa_ }  # Workspace
organizations:  { prefix: og_ }  # Organization
```

### Subcommand: list

List entities of a specific type.

**Usage:**
```
/octave:library list personas
/octave:library list products
/octave:library list playbooks --detailed
```

**Actions:**
- Use `list_all_entities` for quick overview (default)
- Use `list_entities` with pagination for detailed view (--detailed flag)

**Entity Types:**
- `personas` / `persona`
- `products` / `product`
- `playbooks` / `playbook`
- `segments` / `segment`
- `use-cases` / `use_case`
- `competitors` / `competitor`
- `proof-points` / `proof_point`
- `references` / `reference`
- `services` / `service`
- `brand-voices` / `brand-voice`
- `writing-styles` / `writing-style`

**Output Format:**
```
Personas (5 total)
==================

1. CTO - Enterprise Tech
   oId: pe_abc123
   Updated: 2026-01-15

2. VP of Engineering
   oId: pe_def456
   Updated: 2026-01-20

3. Director of Platform
   oId: pe_ghi789
   Updated: 2026-01-22

...

Use /octave:library show <oId> for full details.
```

### Subcommand: search

Semantic search across the library.

**Usage:**
```
/octave:library search "pain points for engineering leaders"
/octave:library search "security compliance" --type persona
```

**Actions:**
- Use MCP tool: `search_knowledge_base`
- Optionally filter by entity type using the `entityTypes` parameter

**Output Format:**
```
Search Results: "pain points for engineering leaders"
=====================================================

1. [Persona] VP of Engineering (pe_def456)
   Relevance: High
   Snippet: "Key pain points include developer velocity,
   technical debt management, and platform reliability..."

2. [Playbook] Enterprise Technical Sale (pb_xyz789)
   Relevance: High
   Snippet: "Engineering leaders prioritize reducing
   operational overhead and improving team productivity..."

3. [Use Case] Developer Productivity Platform (uu_abc123)
   Relevance: Medium
   Snippet: "Addresses the challenge of tool sprawl and
   context switching that impacts engineering teams..."

Use /octave:library show <oId> for full details.
```

### Subcommand: show

Display full details for an entity.

**Usage:**
```
/octave:library show pe_abc123
/octave:library show pb_xyz789
```

**Actions:**
- Use MCP tools: `get_entity` or `get_playbook` (for playbooks with full value props and personas)

**Output Format:**
```
Persona: CTO - Enterprise Tech
==============================
oId: pe_abc123
Created: 2026-01-10
Updated: 2026-01-15
Status: Active

## Description
Senior technology executive responsible for technical strategy
and engineering organization at enterprise companies...

## Pain Points
- Managing technical debt while delivering new features
- Balancing innovation with operational stability
- Attracting and retaining top engineering talent
- Security and compliance requirements

## Key Objectives
- Modernize technology stack
- Improve developer productivity
- Reduce operational costs
- Accelerate time to market

## Primary Responsibilities
- Technical strategy and roadmap
- Engineering team leadership
- Vendor and technology selection
- Budget management

---
Use /octave:library update pe_abc123 to modify this persona.
```

### Subcommand: create

Create a new library entity.

**Usage:**
```
/octave:library create persona "VP of Product"
/octave:library create playbook "SMB Quick Sale" --sources "https://..."
```

**Interactive Flow for Playbooks:**

Playbooks require a dedicated creation flow with offering selection.

1. **List available offerings:**
   ```
   list_all_entities({ entityType: "product" })
   ```

2. **Ask user to select an offering:**
   ```
   Which product or service is this playbook for?

   1. [Product A] (px_abc123)
   2. [Product B] (px_def456)
   3. [Service C] (px_ghi789)

   Your choice:
   ```

3. **Gather playbook details:**
   ```
   Creating new playbook: "SMB Quick Sale"
   For: [Selected Product/Service]

   Please provide details to generate this playbook:

   1. What's the strategic angle or approach?
   2. Which personas does this playbook target?
   3. Any specific use cases or segments to focus on?
   4. Any source materials? (URLs or text to inform generation)
   ```

4. **Call `create_playbook`:**
   ```
   create_playbook({
     name: "SMB Quick Sale",
     description: "Sales playbook for SMB quick-close opportunities",
     instructions: "<detailed instructions from user input>",
     productOId: "px_abc123",
     keyContext: "<any additional context>",
     sources: [{ type: "url", content: "https://..." }]
   })
   ```

5. **Report success:**
   ```
   Created playbook: SMB Quick Sale
   oId: pb_new123

   The playbook has been generated and saved to your library.
   Use /octave:library show pb_new123 to view the full details.
   ```

**Interactive Flow for Other Entities:**

1. **Gather basic info:**
   ```
   Creating new persona: "VP of Product"

   Please provide details to generate this persona:

   1. What industry or company type? (e.g., B2B SaaS, Enterprise Tech)
   2. What are their main responsibilities?
   3. Any specific pain points or priorities to focus on?
   4. Any source materials? (URLs or text to inform generation)
   ```

2. **Confirm and create:**
   ```
   I'll create a VP of Product persona with:
   - Focus: B2B SaaS companies
   - Key responsibilities: Product strategy, roadmap, GTM alignment
   - Pain points: Prioritization, cross-functional alignment, metrics

   Proceed? (yes/no)
   ```

3. **Call `create_entity`:**
   ```
   create_entity({
     entityType: "persona",
     name: "VP of Product",
     instructions: "<detailed instructions from user input>",
     keyContext: "<any additional context>",
     sources: [{ type: "url", content: "https://..." }]
   })
   ```

4. **Report success:**
   ```
   Created persona: VP of Product
   oId: pe_new123

   The persona has been generated and saved to your library.
   Use /octave:library show pe_new123 to view the full details.
   ```

### Subcommand: update

Update an existing entity.

**Usage:**
```
/octave:library update pe_abc123
/octave:library update pe_abc123 --instructions "Add focus on AI/ML adoption"
```

**Interactive Flow:**

1. **Fetch current entity:**
   ```
   Fetching: CTO - Enterprise Tech (pe_abc123)
   ```

2. **Show current state and ask for changes:**
   ```
   Current Persona: CTO - Enterprise Tech

   Key sections:
   - Pain Points: [list current]
   - Objectives: [list current]
   - Responsibilities: [list current]

   What would you like to update?
   (Describe the changes in natural language)
   ```

3. **Confirm changes:**
   ```
   I'll update the CTO persona with:
   - Add AI/ML adoption as a key objective
   - Include "evaluating AI tools" in responsibilities
   - Add "AI readiness" to pain points

   Proceed? (yes/no)
   ```

4. **Apply the update:**

   **For playbooks** (oId starts with `pb_`), use `update_playbook`:
   ```
   update_playbook({
     oId: "pb_xyz789",
     instructions: "Update the objection handling to address security concerns...",
     keyContext: "<any additional context>"
   })
   ```

   **For other entities**, use `update_entity`:
   ```
   update_entity({
     entityType: "persona",
     oId: "pe_abc123",
     instructions: "Add AI/ML adoption as a key objective...",
     keyContext: "<any additional context>"
   })
   ```

5. **Report success:**
   ```
   Updated persona: CTO - Enterprise Tech

   Changes applied:
   - Added AI/ML adoption objective
   - Updated responsibilities
   - Added AI readiness pain point

   Use /octave:library show pe_abc123 to see the updated version.
   ```

### Playbook Updates (Special Handling)

Playbooks have a nested structure requiring different tools for different parts:

**Playbook Structure:**
- **Core attributes** - Key insights, approach angle, strategic narrative, associated personas, qualifying questions
- **Value props** - Persona-specific value propositions (nested within the playbook)

**Decision Logic:**

| User Request | Tools to Use |
|--------------|--------------|
| "Update the playbook's approach angle" | `update_playbook` |
| "Change the strategic narrative" | `update_playbook` |
| "Add a qualifying question to the XYZ playbook about company size being more than 50 employees" | `update_playbook` |
| "Update the value prop for CTOs" | `update_value_props` |
| "Add a new value prop for the CFO persona" | `add_value_props` |
| "Rework the whole playbook including value props" | Both `update_playbook` and value prop tools |

**Updating Value Props Flow:**

1. **Fetch playbook with `get_playbook`** - This returns the full playbook including all value props with their oIds. If you only need the list of value props and their oIds (and not the rest of the playbook), you can instead call `list_value_props` as a lighter-weight alternative.

2. **Identify what needs to change:**
   - Core attributes (insights, narrative, approach) → use `update_playbook`
   - Existing value props → use `update_value_props`
   - New value props → use `add_value_props`

3. **Apply changes with appropriate MCP tool(s)**

**Example - Updating a Value Prop:**
```
User: "Make the CTO value prop focus more on cost savings"

1. Fetch playbook: get_playbook({ oId: "pb_xyz789" })
2. Find CTO value prop oId from response (e.g., "hy_abc123")
3. Update using update_value_props:
   - playbookOId: the playbook containing the value prop
   - updates: array of changes, each with:
     - oId: the value prop oId (hy_ prefix)
     - name: new title (optional)
     - details: new description (optional)
     - archive: true to archive (optional)
     - delete: true to delete (optional)
   - reasoning: why these changes are being made
```

**Example - Updating Qualifying Questions:**
```
User: "Change the qualifying question about budget to focus on timeline instead"

1. Fetch playbook: get_playbook({ oId: "pb_xyz789" })
2. Review current qualifying questions
3. Update: update_playbook({
     oId: "pb_xyz789",
     instructions: "Replace the qualifying question about budget with one that focuses on project timeline and urgency. Keep all other qualifying questions unchanged."
   })
```

**Example - Adding New Value Props:**
```
User: "Add value props for the CFO persona"

1. Fetch playbook to confirm CFO persona is associated
2. Use add_value_props:
   - playbookOId: the playbook to add to
   - personaOIds: array of persona oIds to generate for (optional, defaults to all)
   - numValuesPerPersona: how many to generate (default: 4)
   - instructions: guidance for generation (optional)
   - replaceExisting: true to archive existing first (default: false)
```

## MCP Tools Used

**Important:** Call MCP tools by name (e.g. `get_entity`, `update_entity`, `list_all_entities`).

### Read Operations
- `list_all_entities` - Quick list with basic fields (default for list)
- `list_entities` - Detailed list with pagination (for --detailed flag)
- `get_entity` - Full entity details
- `get_playbook` - Rich playbook with related personas
- `search_knowledge_base` - Semantic search
- `list_value_props` - List value props for a playbook (with oIds)

### Write Operations
- `create_entity` - Create new entity except playbooks (calls generate endpoints)
- `update_entity` - Update existing entity except playbooks (calls refine endpoints)
- `delete_entity` - Delete any entity type (soft delete)
- `create_playbook` - Create new playbook with offering association
- `update_playbook` - Update existing playbook
- `update_value_props` - Update an existing value prop
- `add_value_props` - Add a new value prop to a playbook

### Resource Operations
- `list_resources` - List global resources (documents, websites) with filtering
- `get_resource` - Get detailed resource information by oId
- `create_resource` - Create a new resource (text, file, URL, or Google Drive)
- `delete_resource` - Delete one or more resources
- `search_resources` - Semantic search across global resources

## Error Handling

**Entity Not Found:**
> Entity "[oId]" not found in your library.
>
> This usually means the oId is wrong or the entity was deleted.
> 1. Run `/octave:library list [type]` to see available entities and their oIds
> 2. Check for typos in the oId
> 3. Search by name instead: `/octave:library search [name]`

**Invalid Entity Type:**
> Unknown entity type "[input]".
>
> Valid types: personas, products, playbooks, segments, use-cases,
> competitors, proof-points, references, services, brand-voices, writing-styles
>
> Check spelling and try again.

**Create/Update Failed:**
> Failed to [create/update] [type]: [error message]
>
> Options:
> 1. Check that all required fields are provided
> 2. Try again with simpler instructions
> 3. Run `/octave:workspace` to verify your connection
