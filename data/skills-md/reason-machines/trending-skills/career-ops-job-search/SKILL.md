---
name: career-ops-job-search
description: AI-powered job search pipeline built on Claude Code with 14 skill modes, Go dashboard, PDF generation, batch processing, and portal scanning.
triggers:
  - "set up career-ops job search system"
  - "evaluate job offers with AI"
  - "generate tailored CV or resume PDF"
  - "scan job portals automatically"
  - "batch process multiple job listings"
  - "track job applications in terminal dashboard"
  - "configure career-ops pipeline"
  - "use claude code for job hunting"
---

# Career-Ops Job Search Pipeline

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Career-Ops turns Claude Code into a full job search command center. It evaluates offers with A-F scoring, generates ATS-optimized PDFs, scans 45+ company portals, and tracks everything in a single source of truth — all powered by Claude AI agents.

---

## Installation

```bash
# 1. Clone the repo
git clone https://github.com/santifer/career-ops.git
cd career-ops

# 2. Install Node dependencies (for PDF generation via Playwright)
npm install
npx playwright install chromium

# 3. Configure your profile
cp config/profile.example.yml config/profile.yml
# Edit config/profile.yml with your name, target roles, location, comp range, etc.

# 4. Configure portal scanner
cp templates/portals.example.yml portals.yml
# Add/remove companies you want to track

# 5. Add your CV in Markdown
# Create cv.md in project root — this is what the AI reads to evaluate fit
cat > cv.md << 'EOF'
# Your Name

## Experience
...your CV content in markdown...
EOF

# 6. Build the Go dashboard (optional but recommended)
cd dashboard
go build -o career-dashboard .
cd ..
```

### Prerequisites

- Node.js 18+ (for Playwright/PDF)
- Go 1.21+ (for dashboard TUI)
- Claude Code (`claude` CLI) with an active Anthropic API key

```bash
# Verify Claude Code is installed
claude --version

# Open career-ops in Claude Code
claude   # run from the career-ops directory
```

---

## Core Commands

All commands run inside Claude Code as slash commands. Paste into the Claude Code session:

```
/career-ops                     → Show all available modes
/career-ops {job URL or JD}     → Full auto-pipeline: evaluate + PDF + tracker entry
/career-ops scan                → Scan pre-configured portals for new offers
/career-ops pdf                 → Generate ATS-optimized CV for last evaluated offer
/career-ops batch               → Batch evaluate multiple offers in parallel
/career-ops tracker             → View application pipeline status
/career-ops apply               → AI-assisted application form filling
/career-ops pipeline            → Process all pending URLs in queue
/career-ops contacto            → Generate LinkedIn outreach message
/career-ops deep                → Deep company research report
/career-ops training            → Evaluate a course or certification
/career-ops project             → Evaluate a portfolio project fit
```

### Auto-detection shortcut

Just paste a raw job URL or job description text — career-ops detects it and runs the full pipeline automatically:

```
https://boards.greenhouse.io/anthropic/jobs/12345

# Or paste the full JD text — Claude auto-routes it
```

---

## Configuration Files

### `config/profile.yml`

This is your candidate profile. Claude reads this for every evaluation.

```yaml
# config/profile.yml
name: "Your Name"
title: "Head of Applied AI"
location: "Madrid, Spain"
timezone: "CET"
remote_preference: "remote-first"

target_roles:
  - "Head of AI"
  - "AI Engineer"
  - "LLMOps Engineer"
  - "Solutions Architect (AI)"

compensation:
  currency: "EUR"
  minimum: 120000
  target: 150000
  equity: true

languages:
  - "English (C2)"
  - "Spanish (Native)"

archetypes:
  - "LLMOps"
  - "Agentic"
  - "PM-AI"
  - "Solutions Architect"
```

### `portals.yml`

Configure which company job boards to scan:

```yaml
# portals.yml (copied from templates/portals.example.yml)
companies:
  - name: "Anthropic"
    url: "https://www.anthropic.com/careers"
    board: "greenhouse"
    
  - name: "ElevenLabs"
    url: "https://elevenlabs.io/careers"
    board: "ashby"
    
  - name: "n8n"
    url: "https://n8n.io/careers"
    board: "custom"

job_boards:
  ashby:
    base_url: "https://jobs.ashbyhq.com"
  greenhouse:
    base_url: "https://boards.greenhouse.io"
  lever:
    base_url: "https://jobs.lever.co"

search_queries:
  - "AI engineer remote"
  - "LLMOps"
  - "Head of AI Europe"
```

### `templates/states.yml`

Canonical pipeline statuses (edit to match your workflow):

```yaml
# templates/states.yml
statuses:
  - id: "pending"
    label: "Pending Review"
  - id: "evaluating"
    label: "Under Evaluation"
  - id: "applied"
    label: "Applied"
  - id: "screening"
    label: "HR Screening"
  - id: "interview"
    label: "Interviewing"
  - id: "offer"
    label: "Offer Received"
  - id: "rejected"
    label: "Rejected"
  - id: "withdrawn"
    label: "Withdrawn"
```

---

## Modes Directory

Each file in `modes/` is a Claude skill that defines behavior for one command:

```
modes/
├── _shared.md      # Shared context injected into every mode — customize this first
├── oferta.md       # /career-ops {JD} — full evaluation pipeline
├── pdf.md          # /career-ops pdf — PDF CV generation
├── scan.md         # /career-ops scan — portal scanner
├── batch.md        # /career-ops batch — parallel evaluation
├── tracker.md      # /career-ops tracker — pipeline viewer
├── apply.md        # /career-ops apply — form filling
├── pipeline.md     # /career-ops pipeline — process queue
├── contacto.md     # /career-ops contacto — LinkedIn outreach
├── deep.md         # /career-ops deep — company research
├── training.md     # /career-ops training — cert evaluation
└── project.md      # /career-ops project — portfolio project fit
```

### Customizing modes via Claude

Ask Claude to modify the system from within Claude Code:

```
# In your Claude Code session:
"Change the archetypes in _shared.md to focus on backend engineering roles"
"Translate all modes to English"
"Add Mistral and Cohere to portals.yml"
"Update the scoring weights in oferta.md to weight compensation at 20%"
"Add a new mode called 'referral' for tracking employee referrals"
```

---

## Go Dashboard TUI

The terminal dashboard provides a visual pipeline browser with filtering and sorting.

### Building and running

```bash
cd dashboard
go build -o career-dashboard .
./career-dashboard
```

### Dashboard features

- **6 filter tabs**: All, Pending, Applied, Interviewing, Offer, Rejected
- **4 sort modes**: Date, Score, Company, Status
- **Grouped/flat view**: Toggle between company groups and flat list
- **Lazy-loaded previews**: Press Enter to read the full evaluation report
- **Inline status changes**: Update status without leaving the TUI

### Go module structure

```go
// dashboard/main.go — entry point
package main

import (
    tea "github.com/charmbracelet/bubbletea"
    "github.com/charmbracelet/lipgloss"
)

func main() {
    p := tea.NewProgram(initialModel(), tea.WithAltScreen())
    if _, err := p.Run(); err != nil {
        log.Fatal(err)
    }
}
```

```go
// dashboard/model.go — core data model
package main

import "time"

type Application struct {
    ID          string    `json:"id"`
    Company     string    `json:"company"`
    Role        string    `json:"role"`
    Score       string    `json:"score"` // A, B+, B, C, D, F
    Status      string    `json:"status"`
    URL         string    `json:"url"`
    ReportPath  string    `json:"report_path"`
    PDFPath     string    `json:"pdf_path"`
    CreatedAt   time.Time `json:"created_at"`
    UpdatedAt   time.Time `json:"updated_at"`
    Archetype   string    `json:"archetype"` // LLMOps, Agentic, PM, SA...
    CompRange   string    `json:"comp_range"`
    Notes       string    `json:"notes"`
}

type Model struct {
    applications []Application
    filtered     []Application
    cursor       int
    activeTab    int
    sortMode     int
    grouped      bool
    preview      string
    showPreview  bool
    width        int
    height       int
}
```

### Reading pipeline data from TSV

```go
// dashboard/data.go
package main

import (
    "encoding/csv"
    "os"
    "path/filepath"
)

func loadApplications(dataDir string) ([]Application, error) {
    tsvPath := filepath.Join(dataDir, "pipeline.tsv")
    f, err := os.Open(tsvPath)
    if err != nil {
        return nil, err
    }
    defer f.Close()

    r := csv.NewReader(f)
    r.Comma = '\t'
    r.LazyQuotes = true

    records, err := r.ReadAll()
    if err != nil {
        return nil, err
    }

    var apps []Application
    for _, record := range records[1:] { // skip header
        if len(record) < 8 {
            continue
        }
        apps = append(apps, Application{
            ID:      record[0],
            Company: record[1],
            Role:    record[2],
            Score:   record[3],
            Status:  record[4],
            URL:     record[5],
        })
    }
    return apps, nil
}
```

---

## Batch Processing

Batch mode evaluates multiple offers in parallel using `claude -p` sub-agents.

### Setup batch queue

```bash
# Create a batch input file — one URL per line
cat > batch/queue.txt << 'EOF'
https://boards.greenhouse.io/company/jobs/123
https://jobs.lever.co/company/456
https://jobs.ashbyhq.com/company/789
EOF
```

### Run batch evaluation

```bash
# From Claude Code session:
/career-ops batch

# Or directly from terminal using the runner script:
cd batch
./batch-runner.sh queue.txt
```

### `batch/batch-runner.sh`

```bash
#!/usr/bin/env bash
# batch-runner.sh — orchestrates parallel claude -p workers

QUEUE_FILE="${1:-queue.txt}"
MAX_PARALLEL=4
PROMPT_FILE="batch-prompt.md"

while IFS= read -r url; do
    [[ -z "$url" || "$url" == \#* ]] && continue
    
    # Launch sub-agent for each URL
    claude -p "$(cat $PROMPT_FILE)\n\nEvaluate this offer: $url" \
        --output-format json \
        >> ../data/batch-results.jsonl &
    
    # Throttle parallelism
    while [[ $(jobs -r | wc -l) -ge $MAX_PARALLEL ]]; do
        sleep 2
    done
done < "$QUEUE_FILE"

wait
echo "Batch complete. Results in data/batch-results.jsonl"
```

---

## PDF Generation

PDFs are generated via Playwright rendering an HTML template with injected keywords.

### Triggering PDF generation

```
# In Claude Code — after an evaluation:
/career-ops pdf

# Claude will:
# 1. Read the last evaluation report
# 2. Extract keywords from the job description
# 3. Inject them into templates/cv-template.html
# 4. Render with Playwright to output/{company}-{role}.pdf
```

### Manual Playwright PDF render (Node.js)

```javascript
// scripts/generate-pdf.js
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function generatePDF(htmlContent, outputPath) {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  await page.setContent(htmlContent, { waitUntil: 'networkidle' });
  
  await page.pdf({
    path: outputPath,
    format: 'A4',
    margin: { top: '20mm', bottom: '20mm', left: '15mm', right: '15mm' },
    printBackground: true,
  });
  
  await browser.close();
  console.log(`PDF generated: ${outputPath}`);
}

// Usage
const template = fs.readFileSync('templates/cv-template.html', 'utf8');
const company = process.argv[2] || 'company';
const role = process.argv[3] || 'role';
const outputPath = path.join('output', `${company}-${role}.pdf`);

generatePDF(template, outputPath);
```

---

## Pipeline Data Structure

Career-ops stores data in `data/` (gitignored):

```
data/
├── pipeline.tsv          # Main tracker — all applications
├── batch-results.jsonl   # Batch evaluation outputs
└── urls-pending.txt      # Queue for /career-ops pipeline

reports/
└── {company}-{role}-{date}.md   # Full evaluation reports

output/
└── {company}-{role}.pdf         # Generated CVs
```

### Pipeline TSV format

```tsv
id	company	role	score	status	url	archetype	comp_range	created_at	updated_at	report_path	pdf_path
abc123	Anthropic	AI Engineer	A	applied	https://...	LLMOps	$150k-$200k	2026-04-05	2026-04-05	reports/anthropic-ai-engineer.md	output/anthropic-ai-engineer.pdf
```

---

## Evaluation Scoring System

Career-ops scores offers on 10 weighted dimensions producing an A-F grade:

| Dimension | Weight | What it measures |
|-----------|--------|-----------------|
| Role fit | 20% | Match between JD requirements and your CV |
| Level alignment | 15% | Seniority match |
| Compensation | 15% | Comp vs your target range |
| Tech stack | 15% | Stack overlap with your skills |
| Company stage | 10% | Startup/scale-up/enterprise fit |
| Remote policy | 10% | Location/remote match |
| Growth potential | 5% | Career trajectory opportunity |
| Mission alignment | 5% | Personal interest in the domain |
| Interview signals | 3% | Glassdoor/process quality signals |
| Recruiter quality | 2% | JD quality, clarity, red flags |

**Grade thresholds**: A ≥ 85, B+ ≥ 75, B ≥ 65, C ≥ 50, D ≥ 35, F < 35

---

## Common Patterns

### Evaluate a single offer end-to-end

```
# In Claude Code session (claude command in project root):
/career-ops https://boards.greenhouse.io/anthropic/jobs/4567890

# Claude will:
# 1. Scrape the job description
# 2. Detect archetype (LLMOps, Agentic, PM-AI, etc.)
# 3. Score against your cv.md and profile.yml
# 4. Generate 6-block evaluation report → reports/
# 5. Create ATS-optimized PDF → output/
# 6. Add entry to data/pipeline.tsv
```

### Add a company to the scanner

```yaml
# In portals.yml, add under companies:
  - name: "Langfuse"
    url: "https://langfuse.com/careers"
    board: "ashby"
    filter_keywords:
      - "AI"
      - "engineer"
      - "remote"
```

```
# Then run:
/career-ops scan
```

### Build interview story bank

The STAR+R system accumulates stories across evaluations:

```
# After several evaluations, run:
/career-ops tracker

# Claude surfaces your strongest STAR stories and maps them
# to common behavioral questions. Stories accumulate in:
# reports/_story-bank.md
```

### Salary negotiation script generation

```
# After receiving an offer:
/career-ops {paste the offer details}

# Claude generates:
# - Counter-offer script with specific numbers
# - Geographic discount pushback if applicable  
# - Competing offer leverage language
# - Email templates for each scenario
```

---

## Troubleshooting

### Playwright/PDF issues

```bash
# Chromium not found
npx playwright install chromium

# PDF generation fails silently
node scripts/generate-pdf.js 2>&1 | head -50

# Font not loading in PDF (Space Grotesk / DM Sans)
# Ensure fonts/ directory has the .woff2 files
ls fonts/
# SpaceGrotesk-*.woff2  DMSans-*.woff2
```

### Go dashboard won't build

```bash
cd dashboard
go mod tidy
go build -o career-dashboard .

# Missing Bubble Tea dependency
go get github.com/charmbracelet/bubbletea
go get github.com/charmbracelet/lipgloss
go get github.com/charmbracelet/bubbles
```

### TSV parsing errors

```bash
# Check pipeline.tsv for malformed rows
awk -F'\t' 'NF != 12 {print NR": "NF" fields: "$0}' data/pipeline.tsv

# Re-run integrity check via Claude:
# "Run pipeline integrity check and fix any malformed rows in pipeline.tsv"
```

### Claude Code not finding modes

```bash
# Verify CLAUDE.md is in project root
ls CLAUDE.md  # Must exist

# Verify modes directory
ls modes/     # Should show *.md files

# If Claude doesn't recognize /career-ops, re-open from project root:
cd /path/to/career-ops
claude
```

### Scanner blocked by bot detection

```yaml
# In portals.yml, add delays for rate-limited sites:
  - name: "CompanyName"
    url: "https://company.com/careers"
    board: "greenhouse"
    scrape_delay_ms: 3000
    user_agent: "Mozilla/5.0 (compatible)"
```

---

## Project Structure Reference

```
career-ops/
├── CLAUDE.md                    # Agent instructions (read by Claude Code)
├── cv.md                        # YOUR CV in markdown — create this
├── article-digest.md            # Your proof points / portfolio (optional)
├── config/
│   └── profile.example.yml      # Copy to profile.yml and fill out
├── modes/                       # 14 Claude skill definitions
│   ├── _shared.md               # Shared context — customize first
│   └── *.md                     # One file per /career-ops command
├── templates/
│   ├── cv-template.html         # ATS CV template (Space Grotesk + DM Sans)
│   ├── portals.example.yml      # Copy to portals.yml
│   └── states.yml               # Pipeline status definitions
├── batch/
│   ├── batch-prompt.md          # Self-contained worker prompt for sub-agents
│   └── batch-runner.sh          # Parallel orchestrator
├── dashboard/                   # Go TUI (Bubble Tea + Lipgloss)
│   ├── main.go
│   ├── model.go
│   ├── data.go
│   └── go.mod
├── fonts/                       # Space Grotesk + DM Sans woff2 files
├── data/                        # Runtime data — gitignored
├── reports/                     # Evaluation reports — gitignored
├── output/                      # Generated PDFs — gitignored
├── docs/
│   ├── SETUP.md
│   ├── CUSTOMIZATION.md
│   └── ARCHITECTURE.md
└── examples/                    # Sample CV, report, proof points
```

---

## Key Design Principles

1. **Quality over quantity** — the scoring system is designed to filter *out* weak fits, not to maximize application volume
2. **Claude customizes Claude** — ask Claude to edit the modes, weights, and archetypes; it knows the file structure
3. **Single source of truth** — `data/pipeline.tsv` is the canonical record; all commands read/write it consistently
4. **Gitignore your data** — `data/`, `reports/`, `output/`, and `cv.md` are gitignored by default; your personal info stays local
