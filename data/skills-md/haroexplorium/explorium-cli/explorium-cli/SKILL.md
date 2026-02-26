---
name: explorium-cli
description: Use when needing to look up companies, find prospects, enrich contacts with emails and phone numbers, match businesses or people to Explorium IDs, get firmographics, technographics, funding data, or any B2B sales intelligence. Use when user mentions Explorium, prospect enrichment, company data, or lead research via CLI.
---

# Explorium CLI

B2B data enrichment CLI. Match companies/prospects to IDs, enrich with firmographics, contacts, profiles, tech stack, funding, and more.

## Setup (run once per session if needed)

**Step 1: Check if binary is installed**

```bash
which explorium 2>/dev/null || ls ~/.local/bin/explorium 2>/dev/null
```

If not found, install with the one-liner:

```bash
curl -fsSL https://raw.githubusercontent.com/haroExplorium/explorium-cli/main/install.sh | bash
export PATH="$HOME/.local/bin:$PATH"
```

This downloads the CLI binary to `~/.local/bin/explorium`, makes it executable, and adds it to PATH.

**Step 2: Check if API key is configured**

```bash
explorium config show
```

If output shows `api_key: Not set`, ask the user for their Explorium API key using AskUserQuestion, then:

```bash
explorium config init -k <API_KEY>
```

## Global Options

Place BEFORE the subcommand:

```
-o, --output {json|table|csv}   Output format (default: json)
--output-file PATH              Write to file (clean output, no formatting)
```

## Commands Reference

See `commands-reference.md` in this skill directory for the full command reference with all options.

### Businesses

| Command | Purpose | Key Options |
|---------|---------|-------------|
| `businesses match` | Match companies to IDs | `--name`, `--domain`, `--linkedin`, `-f FILE`, `--summary`, `--ids-only` |
| `businesses search` | Search/filter businesses | `--country`, `--size`, `--revenue`, `--industry`, `--tech`, `--total N` |
| `businesses enrich` | Firmographics (single) | `--id`, `--name`, `--domain` |
| `businesses enrich-tech` | Technology stack | Same ID resolution options |
| `businesses enrich-financial` | Financial indicators | Same ID resolution options |
| `businesses enrich-funding` | Funding & acquisitions | Same ID resolution options |
| `businesses enrich-workforce` | Workforce trends | Same ID resolution options |
| `businesses enrich-traffic` | Website traffic | Same ID resolution options |
| `businesses enrich-social` | LinkedIn posts | Same ID resolution options |
| `businesses enrich-ratings` | Employee ratings | Same ID resolution options |
| `businesses enrich-keywords` | Website keywords | Same ID resolution options + `--keyword` |
| `businesses enrich-challenges` | 10-K challenges | Same ID resolution options |
| `businesses enrich-competitive` | Competitive landscape | Same ID resolution options |
| `businesses enrich-strategic` | Strategic insights | Same ID resolution options |
| `businesses enrich-website-changes` | Website changes | Same ID resolution options |
| `businesses enrich-webstack` | Web technologies | Same ID resolution options |
| `businesses enrich-hierarchy` | Company hierarchy | Same ID resolution options |
| `businesses enrich-intent` | Bombora intent signals | Same ID resolution options |
| `businesses bulk-enrich` | Bulk firmographics | `--ids`, `-f FILE`, `--match-file`, `--summary` |
| `businesses enrich-file` | Match + enrich in one | `-f FILE`, `--types`, `--summary` |
| `businesses lookalike` | Similar companies | `--id`, `--name`, `--domain` |
| `businesses autocomplete` | Name/industry/tech suggestions | `--query`, `--field {name,industry,tech}` |
| `businesses events list` | List event types | `--ids` |
| `businesses events enroll` | Subscribe to events | `--ids`, `--events`, `--key` |
| `businesses events enrollments` | List subscriptions | |

### Prospects

| Command | Purpose | Key Options |
|---------|---------|-------------|
| `prospects match` | Match people to IDs | `--first-name`, `--last-name`, `--company-name`, `--email`, `--linkedin`, `-f FILE`, `--summary` |
| `prospects search` | Search prospects | `--business-id`, `--company-name`, `-f FILE`, `--job-level`, `--department`, `--has-email`, `--total N`, `--max-per-company N`, `--summary` |
| `prospects enrich contacts` | Emails & phones (single) | `--id`, `--first-name`, `--last-name`, `--company-name`, `--email`, `--linkedin` |
| `prospects enrich social` | LinkedIn posts | Same ID resolution options |
| `prospects enrich profile` | Professional profile | Same ID resolution options |
| `prospects bulk-enrich` | Bulk enrich (with `-f FILE`: preserves input columns with `input_` prefix; with `--ids`: enrichment fields only) | `--ids`, `-f FILE`, `--match-file`, `--types {contacts,profile,all}`, `--summary` |
| `prospects enrich-file` | Match + enrich in one | `-f FILE`, `--types {contacts,profile,all}`, `--summary` |
| `prospects autocomplete` | Name/title/dept suggestions | `--query`, `--field {name,job-title,department}` |
| `prospects statistics` | Aggregated insights | `--business-id`, `--group-by` |
| `prospects events list` | List event types | `--ids` |
| `prospects events enroll` | Subscribe to events | `--ids`, `--events`, `--key` |

### Config & Webhooks

| Command | Purpose |
|---------|---------|
| `config init -k KEY` | Set API key |
| `config show` | Display config |
| `config set KEY VALUE` | Set config value |
| `webhooks create --partner-id ID --url URL` | Create webhook |
| `webhooks get --partner-id ID` | Get webhook |
| `webhooks update --partner-id ID --url URL` | Update webhook |
| `webhooks delete --partner-id ID` | Delete webhook |

## CSV Column Mapping

The CLI auto-maps CSV columns (case-insensitive):

**Businesses:** `name`/`company_name`/`company`, `domain`/`website`/`url`, `linkedin_url`/`linkedin`
**Prospects:** `full_name`/`name`, `first_name`, `last_name`, `email`/`email_address`, `linkedin`/`linkedin_url`, `company_name`/`company`

LinkedIn URLs without `https://` are auto-fixed.

**Note:** All `-f`/`--file` options accept CSVs with any number of columns. The CLI reads only the columns it needs and ignores the rest. You can pass the output of one command directly as input to the next without stripping columns.

## Stdin Piping

All `-f`/`--file` options accept `-` to read from stdin, enabling command pipelines:

```bash
# Pipe match output into search, then into enrich
# bulk-enrich -f preserves input columns with input_ prefix
explorium businesses match -f companies.csv -o csv 2>/dev/null \
  | explorium prospects search -f - --job-level cxo --total 10 -o csv 2>/dev/null \
  | explorium prospects bulk-enrich -f - --types contacts -o csv \
  > final_results.csv
```

Format (CSV vs JSON) is auto-detected from content. `--summary` output goes to stderr and won't corrupt piped data.

## Workflows

### Search prospects by company name

```bash
# No need to resolve business_id manually — --company-name does it internally
explorium prospects search --company-name "Salesforce" --job-level cxo --country US --total 50 --summary -o csv --output-file results.csv
```

### Discover valid filter values

```bash
# Find valid industry categories for --industry
explorium businesses autocomplete --query "software" --field industry

# Find valid technologies for --tech
explorium businesses autocomplete --query "React" --field tech

# Find valid job titles
explorium prospects autocomplete --query "founder" --field job-title
```

### Event-Driven Marketing Leader Discovery

**Goal**: Find marketing leadership at companies actively posting about events (conferences, webinars)

**Input**: CSV file with messy prospect data (varying fields: name, company, email, LinkedIn URL)

**Output**: Marketing VPs+ at event-active companies with contact information

#### Step 1: Read and Validate Input File

```bash
# Read the input CSV to understand structure
head -20 /Users/omer.har/Downloads/prospects_enriched_redacted.csv

# Check what columns are available
head -1 /Users/omer.har/Downloads/prospects_enriched_redacted.csv
```

**Expected columns** (may vary per row):
- `first_name`, `last_name`, or `full_name`/`name`
- `company_name` or `company`
- `email` (some rows)
- `linkedin` or `linkedin_url` (some rows)

#### Step 2: Match and Enrich Prospects with Company Data

Use `enrich-file` to match prospects and get their company information in one step.

```bash
# Match and enrich prospects using the messy CSV
# Gets prospect_id, business_id, and basic prospect data
explorium prospects enrich-file \
  -f /Users/omer.har/Downloads/prospects_enriched_redacted.csv \
  --types firmographics \
  --summary \
  -o csv \
  --output-file matched_prospects.csv
```

**What happens**:
- Rows with email → matched by email (most accurate)
- Rows with LinkedIn URL → matched by LinkedIn
- Rows with only name + company → matched by name + company
- Output includes `prospect_id`, `business_id`, and all matched prospect data
- The `business_id` column is what we'll use in the next step

#### Step 3: Enrich Companies with Social Posts

```bash
# Enrich companies directly from matched prospects
# enrich-file reads the business_id column and ignores other columns
explorium businesses enrich-file \
  -f matched_prospects.csv \
  --types all \
  --summary \
  -o json \
  --output-file companies_with_social.json
```

**Note**: The CLI automatically uses the `business_id` column from `matched_prospects.csv` and ignores all other columns (like prospect names, emails, etc.). No need to create a separate file with only business IDs.

#### Step 4: Filter Companies with Event-Related Posts

```bash
# Use jq to filter companies that have social posts mentioning events
jq -r '
  select(.social_posts != null) |
  select(
    .social_posts | tostring |
    test("(?i)(conference|webinar|event|summit|meetup|workshop|seminar)"; "i")
  ) |
  .business_id
' companies_with_social.json > event_companies.txt

# Create CSV for next step
echo "business_id" > event_companies.csv
cat event_companies.txt >> event_companies.csv

# Count how many companies matched
echo "Companies with event posts: $(wc -l < event_companies.txt)"
```

**Event keywords checked**:
- conference, webinar, event, summit, meetup, workshop, seminar (case-insensitive)

#### Step 5: Find Marketing Leadership at Event-Active Companies

```bash
# Search for Marketing VPs+ at these companies
# Use --max-per-company to get balanced results (up to 3 per company)
explorium prospects search \
  -f event_companies.csv \
  --department "Marketing" \
  --job-level "cxo,vp" \
  --has-email \
  --max-per-company 3 \
  -o csv \
  --output-file marketing_leaders.csv \
  --summary
```

**Filters applied**:
- Department: Marketing only
- Seniority: C-level and VP level
- Must have email address
- Max 3 per company (balanced across all companies)

#### Step 6: Enrich with Full Contact Information

```bash
# Enrich marketing leaders with email + phone
explorium prospects enrich-file \
  -f marketing_leaders.csv \
  --types contacts \
  --summary \
  -o csv \
  --output-file final_marketing_leaders.csv
```

**Final output**: `final_marketing_leaders.csv` contains:
- Marketing VPs and C-level executives
- At companies actively posting about events
- With enriched email and phone numbers
- Up to 3 prospects per company

#### Complete Pipeline (All Steps)

```bash
# Full automated pipeline
# Step 1: Match and enrich prospects (gets business_id)
explorium prospects enrich-file \
  -f /Users/omer.har/Downloads/prospects_enriched_redacted.csv \
  --types firmographics \
  --summary \
  -o csv \
  --output-file matched_prospects.csv

# Step 2: Enrich companies with social posts
# Uses business_id column from matched_prospects.csv directly
explorium businesses enrich-file \
  -f matched_prospects.csv \
  --types all \
  --summary \
  -o json \
  --output-file companies_with_social.json

# Step 3: Filter for event posts
jq -r 'select(.social_posts != null) | select(.social_posts | tostring | test("(?i)(conference|webinar|event|summit|meetup|workshop|seminar)"; "i")) | .business_id' companies_with_social.json > event_companies.txt
echo "business_id" > event_companies.csv
cat event_companies.txt >> event_companies.csv

# Step 4: Find marketing leaders
explorium prospects search \
  -f event_companies.csv \
  --department "Marketing" \
  --job-level "cxo,vp" \
  --has-email \
  --max-per-company 3 \
  -o csv \
  --output-file marketing_leaders.csv \
  --summary

# Step 5: Enrich with contacts
explorium prospects enrich-file \
  -f marketing_leaders.csv \
  --types contacts \
  --summary \
  -o csv \
  --output-file final_marketing_leaders.csv

echo "✓ Pipeline complete! Results in: final_marketing_leaders.csv"
```

#### Error Handling and Validation

At each step, check the `--summary` output:
- **Step 2**: Prospect match rate (target: >70%)
- **Step 3**: Companies enriched with social data successfully
- **Step 4**: Number of companies with event posts
- **Step 5**: Marketing leaders found per company
- **Step 6**: Contact enrichment rate (emails/phones added)

#### Constraints

- ✅ **Use ONLY Explorium CLI** for all operations
- ❌ **DO NOT use Vibe Prospecting MCP**
- ✅ Use `jq` for JSON filtering (system tool, allowed)
- ✅ Use `cut`, `sort`, `echo` for CSV manipulation (system tools, allowed)

## Important Notes

- Match-based enrichment: All enrich commands accept `--name`/`--domain`/`--linkedin` instead of `--id` — the CLI resolves the ID automatically
- `enrich-file` is the fastest path for CSV workflows — combines match + enrich in one command
- CSV output flattens nested JSON automatically for spreadsheet use
- `--summary` shows matched/not-found/error counts on stderr
- `--company-name` on `prospects search`: resolves company names to business IDs automatically (accepts comma-separated names)
- `prospects search --summary`: prints aggregate stats (countries, job levels, companies, email/phone counts) to stderr
- `--field` on autocomplete: discover valid values for `--industry`, `--tech`, `--job-title`, `--department`
- `-f -` reads from stdin on all file-accepting commands (auto-detects CSV vs JSON)
- All batch operations retry on transient errors (422, 429, 500-504, ConnectionError, Timeout) with exponential backoff. Failed batches are skipped and partial results are returned.
