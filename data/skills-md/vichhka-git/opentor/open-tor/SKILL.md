---
name: open-tor
description: Search and access the Tor dark web and .onion hidden services. Use when user asks to search dark web, investigate .onion sites, check for dark web data leaks, fetch onion URLs, hunt ransomware groups, look up leaked credentials, conduct Tor-based OSINT, or monitor dark web activity. Provides 12 search engines, batch scraping, entity extraction, relevance scoring, and export to CSV/JSON/STIX/MISP. Requires Tor running locally (socks://127.0.0.1:9050).
---

# OpenTor — Dark Web Access for OpenCode

OpenTor is an **orchestrator-conductor architecture**. You (the orchestrator) are the
intelligence. The Python modules in `scripts/` are mechanical tools — they route
traffic through Tor, query search engines, and scrape pages. Every strategic
decision flows through you.

## ⚠️ Permission Handling

**Before running any command that requires sudo, ask the user for their sudo password.**
Never assume you have it. If a command fails with "Permission denied", immediately
ask the user. Common cases:

- `sudo systemctl start tor` — starting Tor daemon
- `sudo apt install tor` — installing Tor
- `sudo chmod` — fixing cookie auth for renew_identity
- `pip install` may need `--user` flag or venv if PEP 668 is enforced

If the user hasn't provided a password and a command fails, say:
"I need sudo access to run this. What's your sudo password?"

## 🔍 Clearnet-First Search Strategy

**ALWAYS search the public internet first before going to the dark web.**

Dark web search engines have limited, noisy indexes. You will get far better results
by understanding the context from clearnet sources first, then using that intelligence
to craft precise dark web queries.

### The Pattern (follow this for every investigation):

```
STEP 1: CLEARNET (public internet — fast, high-quality)
  → Search Google/DuckDuckGo/Bing for the investigation topic
  → Find: threat actor names, .onion addresses, ransomware tracker IDs,
          victim details, published OSINT reports, IOCs
  → Use the webfetch and websearch tools for this
  → Goal: build context — who, what, when, how

STEP 2: REFINE (use clearnet intel to craft dark web queries)
  → From clearnet results: extract specific .onion addresses to target
  → Identify the exact threat actor/ransomware group name
  → Find known leak site patterns (e.g. "ransomgroupname" → ransomblog_____.onion) for the target actor
  → Craft 3-5 targeted dark web queries using this intelligence

STEP 3: DARK WEB (Tor/onion — slow, targeted)
  → Check Tor: python3 {baseDir}/scripts/opentor.py check
  → Search with precise queries derived from step 1-2
  → Fetch specific .onion addresses discovered in step 1
  → Extract entities, correlate with clearnet findings

STEP 4: SYNTHESIZE (you — the orchestrator)
  → Merge clearnet context + dark web findings
  → Produce structured OSINT report
```

**Example:** Investigating a company believed to have been breached:
1. Clearnet: search for "company name ransomware leak" → find group name, tracker entry, onion address
2. Refine: target the identified leak blog URL, search for victim-specific keywords
3. Dark web: crawl the leak directory → discover department folders, database backups, contracts
4. Synthesize: cross-reference dark web findings with public threat intel → produce IR report

**Never skip step 1.** Dark web search engines will not find specific victim names — but
Google and other public search engines will surface ransomware trackers, group names, and onion addresses.

## Architecture

```
ORCHESTRATOR (you)          ← All intelligence, analysis, decisions
    │
    ├─ opentor.py             ← CLI entry point (subcommands)
    │
    ├─ osint.py               ← High-level investigation tools
    │   search_darkweb()      → search + score + deduplicate
    │   batch_scrape()        → concurrent .onion fetch
      │   extract_entities()    → regex IOCs (emails, crypto, onions)
      │   score_results()       → BM25 relevance scoring
      │   format_output()       → CSV/JSON/STIX/MISP export
      │   content_fingerprint()  → MD5 dedup detection
    │
    ├─ engines.py             ← Search engine management
    │   search()              → query 12 engines in parallel
    │   check_engines()       → health/latency per engine
    │   mode_engines()        → recommend engines per mode
    │
    └─ torcore.py             ← Pure transport (no intelligence)
        tor_session()         → SOCKS5 session through Tor
        fetch()               → GET any URL via Tor
        check_tor()           → verify exit node
        renew_identity()      → rotate Tor circuit
```

## Setup (run once)

Install dependencies:
```bash
pip install -r {baseDir}/requirements.txt
# or: source {baseDir}/.venv/bin/activate
```

Run the setup wizard:
```bash
python3 {baseDir}/scripts/setup.py
```

Start Tor (required before any command):
```bash
# If you have sudo: (ask user for password if needed!)
sudo apt install tor && sudo systemctl start tor    # Linux
brew install tor && brew services start tor          # macOS
```

## CLI Commands

All commands use the unified CLI wrapper. Run via bash.

| Command | What it does |
|---------|-------------|
| `python3 {baseDir}/scripts/opentor.py check` | Verify Tor is running, show exit IP |
| `python3 {baseDir}/scripts/opentor.py engines` | Ping all 12 search engines, show status |
| `python3 {baseDir}/scripts/opentor.py search "query"` | Search dark web (all engines) |
| `python3 {baseDir}/scripts/opentor.py fetch "url"` | Fetch any URL through Tor |
| `python3 {baseDir}/scripts/opentor.py renew` | Rotate Tor circuit (new identity) |
| *(LLM composes its own flow: check → engines → search → fetch → entities)* | *(No fixed pipeline — you orchestrate)* |

### Common Options

```
--mode MODE        threat_intel (default) | ransomware | personal_identity | corporate
--engines NAME     Specific engines (e.g. Ahmia Tor66)
--max N            Max results (default 20)
--format FMT       json (default) | csv | stix | misp | text
--out FILE         Write output to file
--json             Machine-readable JSON output only
```

### Examples

```bash
# Verify Tor
python3 {baseDir}/scripts/opentor.py check

# Check which engines are alive
python3 {baseDir}/scripts/opentor.py engines

# Quick dark web search
python3 {baseDir}/scripts/opentor.py search "ransomware healthcare" --mode ransomware --max 15

# Fetch a specific .onion page
python3 {baseDir}/scripts/opentor.py fetch "http://example.onion/page" --json

# The LLM composes its own investigation flow from individual commands.
# Example: check → search → fetch → entities
python3 {baseDir}/scripts/opentor.py check && \
python3 {baseDir}/scripts/opentor.py search "acme.com data leak" --mode corporate --max 15 && \
python3 {baseDir}/scripts/opentor.py fetch "http://example.onion" && \
python3 {baseDir}/scripts/opentor.py entities --file results.json

# Rotate identity (use between sessions)
python3 {baseDir}/scripts/opentor.py renew

# Export to STIX
python3 {baseDir}/scripts/opentor.py search "ransomware" --format stix --out iocs.json
```

## Investigation Workflows

### "Search the dark web for X"

1. **Clearnet first:** Search Google/DuckDuckGo for "X" to understand context
2. **Refine:** From clearnet results, identify relevant .onion addresses, group names, keywords
3. **Check Tor:** `python3 {baseDir}/scripts/opentor.py check` — abort if not active
4. **Check engines:** `python3 {baseDir}/scripts/opentor.py engines` — note alive ones
5. **Search dark web:** `python3 {baseDir}/scripts/opentor.py search "refined keywords" --mode threat_intel`
6. **Fetch promising URLs:** `python3 {baseDir}/scripts/opentor.py fetch "URL"` on top results
7. **Synthesize:** Combine clearnet context + dark web findings. You produce the analysis.

### "Has company.com been leaked?"

1. **Clearnet:** Search for "company.com ransomware breach leaked" to find trackers
2. **Identify:** Which ransomware group? What .onion address? When did it happen?
3. **Check Tor** → **Search dark web:** `opentor.py search "company data" --mode corporate`
4. **Fetch specific leak site** if .onion address was found in step 1
5. **Synthesize** into a corporate OSINT report (see Analysis Prompts below)

### "Investigate ransomware group X"

1. **Clearnet:** Research group X — TTPs, known .onion addresses, victim count, IOCs
2. **Find leak site:** Look for the group's .onion blog address (ransomware.live tracks these)
3. **Check Tor** → **Fetch leak site:** `opentor.py fetch "http://group.onion"`
4. **Search for victims:** `opentor.py search "GROUP victim" --mode ransomware`
5. **Extract IOCs** and **synthesize** into a ransomware intelligence report

### "When you find a data leak directory"

If you discover a leaked data directory (Apache index, nginx autoindex, JSON API,
HTML file list, etc.), don't rely on fixed parsers. Use `fetch()` to get the raw
content, observe the format, and write a purpose-built parser for what you see.

1. **Fetch the listing:** `python3 {baseDir}/scripts/opentor.py fetch "URL" --json`
2. **Observe the format:** Is it an Apache index? nginx? JSON API? HTML table?
3. **Write a parser inline** that matches the observed format:
```bash
python3 -c "
import sys, json, re
sys.path.insert(0, '{baseDir}/scripts')
from torcore import fetch
r = fetch('URL')
text = r['text']

# Write your parser here based on what you observed.
# Examples:
#  - Apache two-line: name line → date+size line → pair them
#  - nginx: single line with date, size, name
#  - JSON: json.loads(text); iterate entries
#  - HTML table: BeautifulSoup table parsing

# Print results as JSON for further processing
"
```
4. **Verify at least 2 levels deep** before reporting contents as `✓ Observed`
5. **Label everything** with verification status per Rule 1

## 🧾 Professional Reporting Standards

OpenTor investigations are used by incident response teams, CISOs, and regulators.
Your reports must be trustworthy. These are not optional guidelines — they define
how you think about and present evidence.

### Rule 1: Everything Gets a Label

For every assertion in your report, classify it into one of these four categories:

| Label | Definition | When to use it |
|-------|-----------|----------------|
| `✓ Observed` | You saw it directly — raw data from a listing, page, or file | Use for: directory entries, file sizes from server, page titles, HTTP status codes, exact names and URLs you fetched |
| `⚡ Inferred` | You deduced it from naming patterns, context, or domain knowledge | Use for: interpreting what a folder or file likely contains based on its name, size, and surrounding context |
| `❓ Uncertain` | You genuinely cannot determine — ambiguous name, inaccessible, truncated | Use for: any item you haven't verified by crawling deeper, any directory beyond max_depth, any fetch that failed |
| `🤖 AI Analysis` | Your synthesis — connecting dots across multiple sources | Use for: conclusions drawn from combining clearnet intel + dark web findings + naming analysis + threat actor profiles |

The test: would a reviewer who was NOT present during the investigation be able
to tell which parts you saw directly vs which parts you reasoned about?

### Rule 2: Every Incomplete Observation Is a Hypothesis

Dark web investigations operate on layers of inference. You rarely see raw truth
directly — you see directory listings, file metadata, attacker claims, and search
engine snippets. Each is a hypothesis, not a fact.

**The universal test:** Did you directly observe the thing you're asserting, or did
you observe something else and then reason from it? If there is even one logical
step between observation and assertion, it is an inference that needs a label.

Here is what "verified" actually means for different data types you will encounter:

| What you see | What you might conclude | How to verify |
|---|---|---|
| Folder named `Finance/` | "Contains financial records" | Crawl inside — observe actual file names |
| File named `passwords.xlsx` | "Contains credentials" | Can only confirm by downloading and inspecting. Until then → `❓ Uncertain` |
| `.bak` file, 40 GB | "Full SQL Server database backup" | Extension and size are hints, not proof. Could be renamed .zip, VM snapshot, encrypted blob. → `⚡ Inferred` until forensic analysis |
| File size from server: `36557728256` | "36.6 GB" | Size in bytes → `✓ Observed`. Conversion to GB → automatic. Interpretation of what that size means → `⚡ Inferred` |
| Timestamp `22-Mar-2026` | "Data stolen on March 22" | This is the **upload date** to the leak server, not the theft date, not the encryption date. Timestamps are `✓ Observed`; their meaning is `⚡ Inferred` |
| Search result title: "100K customer records leaked" | "100K records were leaked" | Attacker claims in titles and snippets are self-serving and often exaggerated. → `❓ Uncertain` until you fetch the page. |
| Victim listed on group X's leak blog | "Group X attacked this company" | Attribution is an inference chain: blog post → group identity → attack responsibility. Cross-check at least 2 independent sources before labeling `⚡ Inferred`. |
| `confidence: 0.78` from BM25 scoring | "This result is highly relevant" | Statistical similarity ≠ relevance. BM25 measures keyword overlap, not truth. → `⚡ Inferred` — always review result content yourself. |
| 11/12 engines alive at 3pm | "Engines are working" | Engine status is a **snapshot**, not a guarantee. Re-check before every search session. |
| Naming pattern `HRMS` in a filename | "Human Resources Management System" | Standard abbreviation, but not guaranteed. Organization may use non-standard naming. → `⚡ Inferred` |

**The rule for every data type:** Report what you saw (the observation), state what
you think it means (the inference), and separate these with the correct label
(`✓` for the observation, `⚡` or `🤖` for the inference). Never collapse them
into a single statement.

For directories specifically, you must crawl at minimum 2 levels before labeling
contents `✓ Observed`. Until then → `❓ Uncertain`.

### Rule 3: Raw Data First, Summary Second

Structure every data finding as: raw → formatted → interpretation.

- **Raw**: the exact value as received (`36557728256`)
- **Formatted**: human-readable conversion (`34.0 GiB`)
- **Interpretation**: what it means (`This size and .bak extension suggest a full database backup`)

Always include the raw value. The formatted version is a convenience. The
interpretation must be clearly labeled as `⚡ Inferred` or `🤖 AI Analysis`.
Never collapse all three into a single summary sentence.

### Rule 4: Uncertainty Is Information — Report It

When you cannot determine something, that fact itself is valuable intelligence.
Report it explicitly:

- "Found 8 subdirectories. Crawled 3. Remaining 5 are `❓ Uncertain` — max_depth reached."
- "File listing suggests a 40 GB .bak file. Fetch timed out. `❓ Unconfirmed` — retry recommended."
- "Directory name is in a language I cannot interpret. `❓ Uncertain` — needs human analyst."

Never omit uncertain items to make a report look more complete. An honest gap
is more valuable than a confident guess.

### Rule 5: Every Finding Must Be Traceable

The reader must be able to independently verify every claim. For each finding,
include the trace:

- **Source URL**: the exact URL that was fetched
- **Method**: which tool was used (fetch, search_darkweb, extract_entities, purpose-built parser)
- **Timestamp**: when the data was observed (from server response or crawl time)
- **Confidence**: the `✓`/`⚡`/`❓`/`🤖` label

### Rule 6: Revise Publicly, Not Silently

If new evidence contradicts a previous finding:

1. State the original finding with its original label
2. State the new finding with its source
3. Explain what changed and why
4. Update downstream conclusions that depended on the original finding

Correcting yourself builds trust. The report is a living document, not a final
verdict. Stakeholders understand that OSINT evolves as more data is uncovered.

## OSINT Analysis — The Orchestrator's Role

You ARE the LLM. When you have scraped dark web content, analyze it yourself
using these prompts as guidance. Produce structured reports directly in your response.

### threat_intel mode

Output format: 1. Input Query → 2. Source Links → 3. Investigation Artifacts (names,
emails, crypto, domains, markets, threat actors, malware, TTPs) → 4. Key Insights
(3-5, data-driven) → 5. Recommended Next Steps

### ransomware mode

Output format: 1. Input Query → 2. Source Links → 3. Malware/Ransomware Indicators
(hashes, C2s, payload names, MITRE TTPs) → 4. Threat Actor Profile → 5. Key Insights
→ 6. Next Steps (hunting queries, detection rules)

### personal_identity mode

Output format: 1. Input Query → 2. Source Links → 3. Exposed PII Artifacts →
4. Breach/Marketplace Sources → 5. Exposure Risk Assessment → 6. Key Insights →
7. Next Steps (protective actions). Handle all personal data with discretion.

### corporate mode

Output format: 1. Input Query → 2. Source Links → 3. Leaked Corporate Artifacts
(credentials, docs, source code, databases) → 4. Threat Actor/Broker Activity →
5. Business Impact Assessment → 6. Key Insights → 7. Next Steps (IR, legal)

## Search Engines

12 engines queried in parallel through Tor:

| Engine | Type | Notes |
|--------|------|-------|
| Ahmia | .onion | Most reliable |
| OnionLand | .onion | Good coverage |
| Amnesia | .onion | Frequently down |
| Torland | .onion | |
| Excavator | .onion | Best for marketplace results |
| Onionway | .onion | |
| Tor66 | .onion | Fast, reliable |
| OSS | .onion | |
| Torgol | .onion | |
| TheDeepSearches | .onion | |
| DuckDuckGo-Tor | .onion | DDG on Tor |
| Ahmia-clearnet | clearnet | Only use with --include-clearnet |

## Mode → Engine Routing

| Mode | Preferred Engines |
|------|------------------|
| threat_intel | All alive engines |
| ransomware | Ahmia, Tor66, Excavator, Ahmia-clearnet (+ seed blogs) |
| personal_identity | Ahmia, OnionLand, Tor66, DuckDuckGo-Tor, Ahmia-clearnet |
| corporate | Ahmia, Excavator, Tor66, TheDeepSearches, Ahmia-clearnet |

## Key Principles

1. **Clearnet first, dark web second.** Always build context from public sources before
   hitting Tor. This is the single most important rule for productive investigations.
2. **You drive the investigation.** Python code queries and scrapes. You decide what
   to search, which results to pursue, how to interpret findings.
3. **Adapt to observed formats.** When you encounter a data leak directory listing,
   use `fetch()` to get the raw content, observe the format, and write a purpose-built
   parser for what you see. Folder names are hypotheses — only crawled contents are facts.
4. **Report facts, not guesses.** Every assertion must be labeled `✓ Observed`,
   `⚡ Inferred`, `❓ Uncertain`, or `🤖 AI Analysis`. If something is unclear, say
   so explicitly. Never fill gaps with assumptions.
5. **Efficiency.** Dark web queries are slow (30-60s per search). Be strategic and
   use short keyword queries (≤5 words).
6. **Ask for passwords.** If a command fails with "Permission denied" or needs sudo,
   ask the user before retrying. Never assume you have root.
7. **Content safety.** The engine has a built-in blacklist for illegal content.
   It cannot be disabled.
8. **Transparency.** Tell the user traffic routes through Tor. Note when .onion
   sites are offline (status 0).
9. **Clearnet noise filtering is your job.** Dark web search engines return
   noisy, low-relevance results — clearnet spam links often appear in Tor
   search results. You (the LLM) are responsible for filtering out clearnet
   noise, assessing relevance, and deciding which results to pursue. Do not
   pass raw engine output to the user without curation.

## Reference Files

- `README.md` — Project overview, install, quick-start
- `CORE_ENGINE.md` — Full API reference for all modules
- `EXAMPLES.md` — End-to-end usage examples
- `references/safety.md` — Content safety and responsible use
- `references/troubleshooting.md` — Common issues and fixes
