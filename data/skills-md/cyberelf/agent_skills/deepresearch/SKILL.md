---
name: deepresearch
description: Conduct structured deep research on any topic — security threat analysis, technology trend mapping, ecosystem analysis, market forecasts, or law/policy compliance research. Produces a multi-part report grounded in confirmed sources with no premature design assumptions. Use when asked to "deepresearch", "research deeply", or produce a comprehensive multi-part research report. Auto-detects whether the topic calls for security-focused, tech-trend-focused, or law/policy-focused structure.
allowed-tools: Agent, WebFetch, WebSearch, Read, Write, Edit, Glob, Grep, Bash
---

# Deep Research Skill

Conduct rigorous, multi-part research on a complex topic producing a report grounded entirely in confirmed sources. No design assumptions before research is complete. All claims backed by source links.

## Skill Files

This skill is split across files — read the relevant ones before proceeding:

| File | Purpose |
|------|---------|
| `security.md` | Full template and agent prompts for security research mode |
| `techtrend.md` | Full template and agent prompts for tech trend / ecosystem research mode |
| `law-policy.md` | Full template and agent prompts for law, policy, regulatory, and compliance research mode |
| `report-template.html` | HTML report template — use when user requests an HTML output |

---

## Step 1: Detect Mode

Determine research mode from the query **before reading any template**:

| Mode | Trigger keywords | Template to read |
|------|-----------------|-----------------|
| `security` | security, threat, CVE, attack, defense, vulnerability, exploit, risk, malware | Read `security.md` |
| `techtrend` | trend, forecast, ecosystem, landscape, technology, hardware, market, adoption | Read `techtrend.md` |
| `law-policy` | law, policy, regulation, compliance, legal requirement, statutory, retention, audit trail, recordkeeping, regulator, licensee, service provider, data residency, data protection, privacy, telecom law, cybersecurity law | Read `law-policy.md` |
| Ambiguous | None clearly applies, or multiple modes are plausible | Ask: "Is this a security analysis, technology trend/ecosystem research, or law/policy compliance research?" |

---

## Step 2: Read the Template

After detecting mode, **read the appropriate template file** in full before writing the research plan or launching agents. The template files contain:
- The 5-part structure for that mode
- Per-part research questions and source guidance
- Agent prompt scaffolding
- Lessons learned specific to that mode

---

## Step 3: Execute

Follow the execution steps in the template. The core workflow is the same for all modes:

1. Write `RESEARCH_PLAN.md` in a new `{topic}_{YYYYMM}/` folder
2. Launch 5 parallel background agents (one per part)
3. Acknowledge each agent as it completes with a key findings summary
4. After all 5 complete: read all raw files, compile `RESEARCH_REPORT.md`
5. If HTML output requested: use `report-template.html` as the base

---

## Universal Rules (apply to all modes)

### Source quality
- **Specs/products**: Official vendor docs, press releases, spec sheets
- **CVEs/security**: NVD, MITRE, vendor advisories, Black Hat/DEF CON/USENIX papers
- **Academic**: arXiv, NeurIPS/ICLR/CVPR/ACL proceedings, OpenReview
- **Market data**: Gartner, IDC, Forrester, MarketsandMarkets, Crunchbase
- **Regulatory**: EUR-Lex, NIST, CISA, Federal Register, national AI laws
- **Law/policy**: official gazettes, government legal portals, regulator websites, ministry publications, court/tribunal decisions, official consultation papers
- **Benchmarks**: MLCommons/MLPerf, HuggingFace leaderboards, official vendor disclosures
- **Do NOT cite**: Wikipedia, unattributed blogs, secondary summaries

### Agent instructions (every agent must)
1. Fetch and READ actual URLs — do not rely on training data alone
2. Note publication dates — distinguish confirmed vs. announced vs. speculative
3. Save raw output to `{folder}/raw_research/XX_topic.md`
4. Target 2,000+ words with real data, tables, and source URLs

### File structure
```
{topic}_{YYYYMM}/
├── RESEARCH_PLAN.md
├── RESEARCH_REPORT.md
├── report.html            # optional, if HTML requested
└── raw_research/
    ├── 01_*.md
    ├── 02_*.md
    ├── 03_*.md
    ├── 04_*.md
    └── 05_*.md
```

### Common errors to avoid
1. **Wrong platform ID**: Fetch the actual product website before writing the plan
2. **Shallow agents**: Anchor every agent with 3–5 specific URLs to fetch first
3. **Premature design** (security mode): Do not write Part 4 before Parts 1–3 are reviewed
4. **Fixed dimensions** (techtrend mode): Parts 2–4 are defined per-topic in the plan, not preset
5. **Legal status confusion** (law-policy mode): never mix binding law, proposed rules, regulator guidance, unofficial translations, and vendor summaries without labeling them
6. **Blocked sources**: Chinese sources behind auth walls — search for equivalent open-web sources
7. **Context length**: Raw research files can be 5,000–7,000 words each — read them carefully

---

## Example Invocations

```
# Security (auto-detected)
/deepresearch security for personal AI endpoint agents including OpenClaw and Claude Code
/deepresearch supply chain attacks on npm packages
/deepresearch quantum-safe cryptography for financial services

# Tech trend (auto-detected)
/deepresearch endpoint LLM ecosystem — hardware, models, runtimes, applications
/deepresearch autonomous vehicle software stack trends and 2030 forecast
/deepresearch edge AI chip market landscape

# Law/policy (auto-detected)
/deepresearch data residency laws for financial SaaS in Singapore, Indonesia, and Malaysia
/deepresearch firewall log retention compliance requirements in Thailand and Turkiye
/deepresearch EU AI Act obligations for enterprise AI coding assistants

# With HTML output
/deepresearch endpoint LLM ecosystem output: html
```
