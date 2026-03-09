---
name: invoice
description: "Generate professional PDF invoices from client billing data. Supports fixed-fee and hourly billing with auto-incrementing invoice IDs. Pass client name and line items as args, or invoke interactively."
---

<objective>
Generate a professional PDF invoice by combining client billing data with line item details, then output a ready-to-send PDF.
</objective>

<usage>
## Invocation

```
/invoice <client> [description] [amount] [options]
```

### Examples

```bash
# Full inline — generates immediately
/invoice validcodes "AI Training Pack" 7500 --net 15

# Just client — prompts for line items and terms
/invoice validcodes

# With notes
/invoice validcodes "Sprint Phase 1" 40000 --net 1 --notes "50% upfront per SOW"

# Hourly — interactive mode for multiple line items
/invoice acme --hourly

# Custom quantity
/invoice validcodes "Advisory Call" 300 --quantity 4 --net 15
```

### Arguments

| Arg | Required | Default | Description |
|-----|----------|---------|-------------|
| `client` | Yes | — | Client slug or alias (matched against client YAML files) |
| `description` | No | prompted | Line item description |
| `amount` | No | prompted | Total amount in USD |
| `--net N` | No | client default or 15 | Payment terms (NET-N days) |
| `--quantity N` | No | 1 | Line item quantity |
| `--notes "..."` | No | none | Notes to display below the total |
| `--hourly` | No | false | Interactive mode for multiple line items with rates |
</usage>

<configuration>
## Required Setup

### Paths

The skill needs these directories configured for your environment:

| Path | Purpose | Example |
|------|---------|---------|
| Clients dir | YAML files with billing info | `02_Areas/consulting/templates/invoicing/clients/` |
| Output dir | Where generated PDFs are saved | `02_Areas/consulting/invoices/` |
| Logo override | Optional custom logo | `02_Areas/consulting/templates/invoicing/logo.png` |

The generator script, HTML template, and default logo are bundled with this skill.

### Client YAML Schema

Create one YAML file per client in your clients directory:

```yaml
# clients/acme.yaml
name: "Acme Corporation"
address_1: "123 Innovation Blvd, Suite 400"
address_2: "San Francisco, CA 94105"
aliases: [acme, acme-corp]
default_net: 30
```

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Full legal name for invoice |
| `address_1` | Yes | Street address |
| `address_2` | Yes | City, state, zip |
| `aliases` | No | Alternative names for matching (case-insensitive) |
| `default_net` | No | Default payment terms for this client (fallback: 15) |

### Payee Info

The HTML template has a hardcoded "Pay to" address. Edit `invoice-template.html` in the skill directory to change your billing address.

### Dependencies

The generator requires Python packages installed via uv:
```bash
uv run --with weasyprint --with pyyaml --with jinja2 python3 generate-invoice.py <config.yaml>
```
</configuration>

<process>
## Step 1: Resolve Client

1. Read the first argument as the client identifier
2. Glob all YAML files in the clients directory
3. For each file, check:
   - Filename (without `.yaml`) matches the arg (case-insensitive)
   - The `aliases` array contains the arg (case-insensitive)
4. If no match found, list available clients and ask the user to choose
5. Load the matched client's billing info

## Step 2: Collect Invoice Details

For any fields not provided as arguments, prompt the user:

1. **Description** — What is the line item? (e.g., "AI Training Pack", "Sprint Phase 1")
2. **Amount** — Total amount in USD
3. **NET terms** — Use `--net` arg, or client's `default_net`, or fall back to 15
4. **Quantity** — Default 1 unless specified
5. **Notes** — Optional, use `--notes` arg or ask if user wants to add any

For `--hourly` mode, interactively collect multiple line items:
- Prompt for each: description, hours, rate
- Calculate amount as hours × rate
- Keep asking "Add another line item?" until done

## Step 3: Determine Invoice ID

1. Scan the output directory for existing PDF files matching `invoice-#*.pdf`
2. Extract the highest invoice number N
3. Use N+1 as the new invoice ID
4. If no existing invoices, start at 1

## Step 4: Generate Invoice

1. Compute invoice date (today) and due date (today + NET days)
2. Format dates as MM/DD/YYYY
3. Create a client slug from the YAML filename (used in PDF filename)
4. Write a temporary YAML config file combining client info + line items
5. Determine the skill directory (where generate-invoice.py lives)
6. Check for a logo override in the clients directory's parent — if it exists, use `--logo` flag; otherwise use the bundled default
7. Run the generator:

```bash
uv run --with weasyprint --with pyyaml --with jinja2 python3 \
  <skill-dir>/generate-invoice.py <temp-config.yaml> \
  --output-dir <output-dir> \
  [--logo <custom-logo>]
```

8. Delete the temporary YAML config

## Step 5: Review and Commit

1. Open/display the generated PDF for the user to review
2. Report: invoice number, client, amount, due date, file path
3. Ask: "Does this look right? Commit?"
4. If approved, stage and commit with message:
   ```
   feat: Generate <client> invoice #N ($X,XXX)
   ```
5. If changes needed, go back and adjust

</process>

<reference_files>
- `generate-invoice.py` — PDF generator script (bundled with this skill)
- `invoice-template.html` — Jinja2 HTML template (bundled with this skill)
- `logo.png` — Default logo (bundled with this skill)
- `INVOICE-TEMPLATE-SPEC.md` — Full design spec for the template layout
</reference_files>
