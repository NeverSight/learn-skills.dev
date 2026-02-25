---
name: person-intelligence-osint
description: Conduct a full-spectrum public intelligence (OSINT) investigation on any individual given their name, job title, and company. Produces a structured intelligence dossier. Use when asked to research a person, build a profile, investigate a contact, create a dossier, or gather publicly available intelligence on an individual.
---

# Person Intelligence OSINT

Conduct a comprehensive, LinkedIn-friendly, open-source intelligence investigation on any individual. The process starts with professional network reconnaissance, expands to broad-spectrum public sources, and produces a structured intelligence dossier.

## Inputs

Three inputs are required. If any are missing, ask the user before proceeding.

| Input            | Description                                      | Example                  |
| ---------------- | ------------------------------------------------ | ------------------------ |
| **Person Name**  | Full name of the subject                         | Jane Smith               |
| **Job Title**    | Current or most recent known role                | Chief Technology Officer |
| **Company Name** | Primary company the subject is associated with   | Acme Corp                |

## Workflow

Execute sequentially. Do not skip steps.

### Step 1: Acknowledge and Scope

Confirm the target details with the user. Create a working directory:

```
mkdir -p /home/ubuntu/osint/{{person_name_slug}}
```

Create `osint_notes.md` inside this directory to accumulate raw findings throughout the process.

### Step 2: LinkedIn Reconnaissance

This is the foundational data source. The goal is to locate and extract the subject's canonical professional profile.

1. Use `search` tool (type: `info`) with these query patterns:
   - `"{{person_name}}" "{{company_name}}" site:linkedin.com`
   - `"{{person_name}}" "{{job_title}}" LinkedIn`
   - `"{{person_name}}" "{{company_name}}" LinkedIn profile`

2. Use `browser_navigate` to visit the identified LinkedIn URL. Extract:
   - Full name, headline, location
   - Career history (all roles, companies, dates)
   - Education
   - Skills, endorsements, recommendations count
   - Connection count and notable mutual connections
   - Any posts or articles authored

3. Save all extracted data to `osint_notes.md` immediately.

### Step 3: Corporate Intelligence

Investigate the subject's company and any other associated entities.

1. Use `search` tool with:
   - `"{{company_name}}" Companies House` (UK) or `"{{company_name}}" SEC filing` (US)
   - `"{{company_name}}" corporate registration`
   - `"{{person_name}}" director OR officer "{{company_name}}"`

2. For UK companies, navigate to `https://find-and-update.company-information.service.gov.uk/` and search for the company. Extract:
   - Company number, status, incorporation date
   - Registered address
   - Directors and officers (confirm subject's role)
   - Filing history (recent accounts, confirmation statements)

3. Append findings to `osint_notes.md`.

### Step 4: Media & Public Presence

Expand to news, social media, and other public mentions.

1. Use `search` tool (type: `news`) with:
   - `"{{person_name}}" "{{company_name}}"`
   - `"{{person_name}}" interview OR announcement OR appointed`

2. Use `search` tool (type: `info`) with:
   - `"{{person_name}}" site:twitter.com OR site:x.com`
   - `"{{person_name}}" site:facebook.com`
   - `"{{person_name}}" site:github.com` (if technical role)
   - `"{{person_name}}" "{{company_name}}" conference OR speaker OR panel`

3. For each significant result, use `browser_navigate` to read the full content. Save key excerpts and URLs to `osint_notes.md`.

### Step 5: Domain & Technical Intelligence (Conditional)

Execute this step only if the subject has a technical or digital role (CTO, developer, engineer, etc.).

1. Search for personal websites, blogs, or portfolios.
2. Search for GitHub profiles, open-source contributions, or academic papers.
3. Search for domain registrations (WHOIS) if a personal domain is found.
4. Append findings to `osint_notes.md`.

### Step 6: Connected Systems Check (Conditional)

If the user has Gmail or Slack MCP integrations enabled, search those systems for any prior correspondence or mentions of the subject.

1. **Gmail**: Use `gmail_search_messages` with queries for the person's name and company.
2. **Slack**: Use `slack_search_public_and_private` with the person's name.
3. Append any findings to `osint_notes.md`.

### Step 7: Synthesize and Generate Dossier

1. Read the dossier template: `/home/ubuntu/skills/person-intelligence-osint/templates/dossier_template.md`
2. Create the final report file: `Dossier_{{person_name_slug}}.md`
3. Populate the template with synthesized intelligence from `osint_notes.md`.
4. Ensure all sections are written in complete paragraphs, not bullet lists.
5. Include a References section with numbered citations and source URLs.
6. Include a table for career history and a table for the identity profile.

### Step 8: Deliver

1. Review the dossier for completeness.
2. Use `message` tool (type: `result`) to deliver the Markdown dossier as an attachment.
3. Provide a concise summary of key findings in the message text.
4. Optionally, sync to Google Drive if the user has integration enabled.

## Output Format

The final dossier MUST use the template at `templates/dossier_template.md`. Key requirements:

- Professional Markdown formatting
- Identity table at the top
- Career history table
- Complete paragraphs (not bullet-point lists) for analysis sections
- Numbered inline citations with a References section
- All source URLs documented

## Example Usage

**User says:** "Research John Smith, VP Engineering at TechCorp"

**Skill triggers with:**
- Person Name: John Smith
- Job Title: VP Engineering
- Company Name: TechCorp

**Output:** A structured Markdown dossier covering LinkedIn profile, corporate filings, news mentions, social media presence, and any connected system references.
