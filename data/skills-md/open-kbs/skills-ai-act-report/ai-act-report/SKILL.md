---
name: ai-act-report
description: Generate an EU AI Act (Regulation 2024/1689) compliance report for the project. Collects AI usage data, scans for compliance artifacts, classifies risk per Annex III, and produces a structured Markdown report.
allowed-tools: Bash(node *report.mjs*)
---

# AI Act Compliance Report

Generate a compliance report for Regulation (EU) 2024/1689 (the EU AI Act). The report covers AI model inventory, risk classification, compliance checklist, and actionable recommendations.

## When to use

Use this skill when the user asks to:
- Generate an AI Act compliance report
- Audit AI usage in the project
- Check AI Act compliance status
- Prepare documentation for regulators or auditors
- Classify AI systems by risk level
- Review AI literacy or transparency obligations

## Step 1: Collect data

Run the data collection script:

```bash
node .claude/skills/ai-act-report/report.mjs --days 90 --output ai-act-report-data.json
```

This queries the OpenKBS Project API for AI usage statistics and scans the project for compliance artifacts. It outputs a JSON file with:
- AI model usage (vendor, model, request count, tokens, cost)
- Daily usage breakdown
- Available model catalog
- Compliance artifact scan results (skills, policies, disclosure components)
- List of project functions

## Step 2: Analyze the project

Read the JSON output, then analyze the project code to determine:

1. **What is AI used for?** — Read the functions in `functions/` and `site/` to understand each AI use case. Examples: customer chatbot, content generation, data analysis, employee evaluation, recruitment screening, credit scoring.

2. **Risk classification per Annex III** — For each AI use case, determine if it falls into a high-risk category:
   - Biometrics (remote identification, emotion recognition)
   - Critical infrastructure (energy, transport, water management)
   - Education (admission, grading, learning assessment)
   - **Employment** (recruitment, CV screening, performance evaluation, promotion/termination decisions)
   - Essential services (credit scoring, insurance pricing, social benefits)
   - Law enforcement (evidence evaluation, risk assessment)
   - Migration (visa assessment, border surveillance)
   - Justice (legal research, sentencing tools)

   If a use case does NOT fall into any Annex III category, classify it as **minimal risk** or **limited risk** (transparency only).

3. **Compliance gap analysis** — Check for each Article 21 requirement.

## Step 3: Generate the report

Produce a Markdown document with this exact structure:

```markdown
# AI Act Compliance Report
## Project: {project name or ID}
## Period: {start date} — {end date}
## Generated: {date}

---

### 1. AI System Inventory

| Vendor | Model | Requests | Input Tokens | Output Tokens | Cost (credits) |
|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... |

**Total AI requests:** {N}
**Total cost:** {N} credits ({N} EUR)
**Models used:** {N} distinct models from {N} vendors

---

### 2. Risk Classification

| AI Use Case | Description | Risk Category | Annex III Reference | Justification |
|---|---|---|---|---|
| {function name} | {what it does} | Minimal / Limited / High-risk | {e.g., Annex III, pt. 4} | {why this classification} |

---

### 3. Compliance Checklist

| Requirement | Article | Status | Evidence |
|---|---|---|---|
| AI Literacy measures | Art. 4 | {status} | {what was found or missing} |
| No prohibited practices | Art. 5 | {status} | {AI Act Compliance Skill active / not found} |
| Activity logging / traceability | Art. 12 | {status} | {proxy logs available for N days} |
| Human oversight mechanisms | Art. 14, 26 | {status} | {approval workflow detected / not found} |
| Transparency / AI Disclosure | Art. 50 | {status} | {disclosure component found / not found} |
| Log retention >= 6 months | Art. 26(6) | {status} | {retention period} |
| Worker notification (if HR AI) | Art. 26(7) | {status or N/A} | {evidence} |
| AI Acceptable Use Policy | Best practice | {status} | {document found / not found} |
| AI Literacy Policy | Best practice | {status} | {document found / not found} |

Status values: Compliant / Partial / Non-compliant / N/A

---

### 4. Recommendations

Produce a prioritized checklist of actions:
- Critical: things that must be fixed before Aug 2, 2026
- Important: things that should be in place for full compliance
- Recommended: best practices that strengthen the compliance posture

---

### 5. Report Metadata

- **Tool:** ai-act-report v1.0.0
- **Data source:** OpenKBS AI Proxy usage logs
- **Classification method:** Automated data collection + AI-assisted code analysis
- **Regulation:** Regulation (EU) 2024/1689
- **Disclaimer:** This report is generated automatically and does not constitute legal advice. For binding compliance assessments, consult a qualified legal professional.
```

Save the report as `AI-ACT-COMPLIANCE-REPORT.md` in the project root (or a path the user specifies).

## Step 4: Present to the user

After generating the report:
1. Summarize the key findings (how many models, what risk level, what's missing)
2. Highlight the most critical gaps
3. Ask if they want to address any of the recommendations now

## Important notes

- The report uses data from the OpenKBS AI Proxy. If the project uses AI models outside the proxy (e.g., direct API calls), those will NOT appear in the report. Mention this limitation.
- Risk classification is based on code analysis and may require human validation for edge cases.
- The cost conversion is: 100,000 credits = 1 EUR.
- The report should be regenerated periodically (recommended: quarterly) to maintain a documented compliance history.
- Do NOT generate fake or placeholder data. If data is unavailable, say so explicitly.
