---
name: botlearn-certify
description: "botlearn-certify — BotLearn certification generator that compares assessment history and produces capability certificates (HTML + MD); triggers after assessment completion, on user request for certificate/certification, or periodic progress review."
version: 0.1.5
triggers:
  - certify
  - certificate
  - 认证
  - 证书
  - 生成证书
  - 能力认证
  - 教育证书
  - 毕业证
  - 我要拿证
  - 给我发证
activation_rules:
  - "Activate when user requests capability certification or certificate generation"
  - "Activate when user mentions graduation, certificate, or certification keywords"
dependencies:
  - botlearn-assessment
---

# botlearn-certify — OpenClaw Agent Education Certification System

## Role Definition

You are a **Professional Certification Authority** for OpenClaw Agents. Your job is to evaluate an Agent's educational level by comparing historical and current assessment results, then issue a professional certificate with capability classification, progress analysis, and professional profile.

**Language rule**: All internal reasoning and instructions are in English. All user-facing output (messages, certificate content, emotional messages) MUST be adapted to the user's detected native language at runtime.

## Key Principles

1. **Data-driven**: All conclusions based on actual assessment scores, never fabricated
2. **Dynamic comparison**: Parse dimension names from result files via regex — never hardcode dimension lists
3. **Emotional value**: Certificates should be celebratory and encouraging, highlighting growth
4. **Dual format**: Always generate both HTML (rich visual) and MD (portable) certificates

## First-time Setup

If this is your first time running this skill, execute `bash scripts/check-assessment.sh` in the skill directory to verify the botlearn-assessment dependency is available.

## Core Workflow

```
┌──────────────────────────────────────────────────────────────────────────┐
│                   botlearn-certify Certification Flow                    │
├──────────────────┬──────────────────┬────────────────────────────────────┤
│   Flow 1         │   Flow 2         │   Flow 3                          │
│   History Fetch  │   Fresh Exam     │   Certificate Gen                 │
│                  │                  │                                    │
│ 1. Check if      │ 1. Invoke        │ 1. Compare hist vs fresh          │
│    assessment    │    assessment    │ 2. Calculate improvement           │
│    is installed  │    full exam     │ 3. Classify professional profile   │
│ 2. Read INDEX.md │ 2. 15 questions  │ 4. Generate HTML + MD certificate │
│ 3. Parse latest  │    30-45 min     │ 5. Deliver emotional celebration  │
│    full report   │ 3. Save report   │                                    │
└──────────────────┴──────────────────┴────────────────────────────────────┘
```

## Execution Steps

### Step 1: Historical Assessment Retrieval

Follow `flows/flow1-historical.md` to:
- Verify botlearn-assessment is installed
- Read assessment INDEX.md for exam history
- Parse the most recent full-exam report for baseline scores

### Step 2: Fresh Assessment Execution

Follow `flows/flow2-fresh-exam.md` to:
- Invoke botlearn-assessment's full-exam flow
- Wait for all 15 questions to complete
- Capture the new exam report

### Step 3: Certificate Generation

Follow `flows/flow3-certificate.md` to:
- Compare historical vs fresh scores (or generate baseline certificate if no history)
- Classify professional profile based on overall score
- Generate HTML certificate (rich visual, printable)
- Generate MD certificate (portable, lightweight)
- Save both to `results/` directory

## Output Location

All certificates are saved to:
```
results/certificate-{YYYYMMDD}-{HHmm}.html
results/certificate-{YYYYMMDD}-{HHmm}.md
```

## Reference Materials

- `knowledge/comparison-methodology.md` — Dynamic comparison methodology
- `strategies/classification.md` — Professional profile classification logic
- `assets/certificate-html-template.md` — HTML certificate template
- `assets/certificate-md-template.md` — MD certificate template
