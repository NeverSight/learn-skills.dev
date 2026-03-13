---
name: research-prospect
description: Research a prospect company and contact before outreach or a meeting. Use when the user needs to understand a company, look up a contact on LinkedIn, or find personalization hooks before reaching out. Produces a structured research brief.
license: MIT
compatibility: Requires internet access for website and LinkedIn research.
metadata:
  author: toughtongueai
  version: "1.0"
---

# Prospect Research

Research a prospect company and contact to produce a structured intelligence brief. This skill gathers information from the company's website and the contact's LinkedIn profile, then cross-references with your `company-profile.md` to find personalization hooks.

## When to Use

- Before writing any outreach (cold email, LinkedIn message)
- Before a demo or meeting (this skill is called automatically by `demo-prep`)
- When the user says "research [name] at [company]"
- When you need to understand a prospect before generating any output

## Required Inputs

Ask the user for:

```
Company: [Name or website URL]
Contact: [Name and title — optional for company-only research]
```

If they only provide a name and company, that's enough. Research the rest.

## Process

### 1. Load Company Profile

Read `company-profile.md` from the workspace root. You need this to:
- Identify shared connections between the user and the prospect
- Match the prospect's pain points to the user's product
- Determine if this company fits the user's ICP

If `company-profile.md` doesn't exist, tell the user: "Run the `setup-company` skill first to set up your profile. This makes research much more useful."

### 2. Research the Company

Navigate to the company's website and gather:

| What to Find | Where to Look |
|-------------|---------------|
| **What they do** | Homepage hero section, About page |
| **Who they sell to** | Pricing page, case studies, customer logos |
| **Company size** | About page, LinkedIn company page, job postings |
| **Sales model** | Pricing page structure, "Book a Demo" vs "Start Free Trial" |
| **Recent news** | Blog, press page, recent funding announcements |
| **Tech stack signals** | Job postings, integrations page |
| **Demo / trial motion** | CTA buttons, pricing page, "how it works" |

Also check for (see [research checklist](references/research-checklist.md)):
- Whether they have a "Book a Demo" button (relevant for demo automation)
- Whether they're hiring for roles related to the user's product
- Recent product launches or pivots
- Customer testimonials that reveal their value prop

### 3. Research the Contact

Look up the contact on LinkedIn (use browser tools) and gather:

| What to Find | Why It Matters |
|-------------|---------------|
| **Current role and tenure** | How long they've been there — new hires are more open to change |
| **Department** | Maps to which angle to use in outreach |
| **Previous companies** | Shared connection opportunities |
| **Education** | Shared school connections |
| **Recent posts or activity** | Conversation hooks, what they care about publicly |
| **Responsibilities** | What they likely own and what metrics they're measured on |

### 4. Find Personalization Hooks

Cross-reference the contact's background with the user's `company-profile.md`:

| If You Find... | Hook to Use |
|----------------|-------------|
| Same school (any level) | "Fellow [school] alum" |
| Same previous company | "Ex-[company] here too" / "My co-founder is ex-[company]" |
| Same city or region | Geographic connection |
| Mutual LinkedIn connections | "We both know [name]" |
| They posted about a relevant topic | Reference the post directly |
| They recently changed roles | "Congrats on the new role" |
| Their company just raised funding | "Congrats on the raise" |

**Priority order:** Shared school > shared company > shared connection > recent event > geographic.

### 5. Assess ICP Fit

Based on research, assess how well this prospect matches the user's ICP from `company-profile.md`:

| Signal | What It Means |
|--------|--------------|
| Role matches target roles | Strong fit |
| Company size matches ICP | Strong fit |
| Industry matches ICP | Strong fit |
| They have signals from ICP (e.g., "hiring SDRs") | Strong fit |
| None of the above | Weak fit — note this in the output |

## Output Format

```markdown
# Prospect Research: [Contact Name] @ [Company Name]
**Researched:** [Date]

## Company Intel
| Field | Details |
|-------|---------|
| **Company** | [Name] |
| **Website** | [URL] |
| **Industry** | [Industry] |
| **Size** | [Estimate — employees, stage, funding] |
| **What They Do** | [2-3 sentences] |
| **Who They Sell To** | [Their customers] |
| **Sales Model** | [Inbound / outbound / PLG / enterprise] |
| **Recent News** | [Funding, launches, hires — if any] |

## Contact Intel
| Field | Details |
|-------|---------|
| **Name** | [Full name] |
| **Title** | [Job title] |
| **Department** | [Sales, Engineering, L&D, Product, etc.] |
| **Tenure** | [How long in current role] |
| **Background** | [Previous companies, education] |
| **Recent Activity** | [Posts, articles, comments — if any] |
| **Likely Priorities** | [What they probably care about based on role] |

## Personalization Hooks
- **Strongest hook:** [The best connection point]
- **Additional hooks:** [Other connection points]

## ICP Fit
[Strong / Medium / Weak] — [1 sentence explaining why]

## Relevant Pain Points
Based on their business and role, they likely care about:
1. [Pain point 1 — mapped to user's product]
2. [Pain point 2 — mapped to user's product]
3. [Pain point 3 — mapped to user's product]
```

## Instructions

1. **Always research before generating.** Never fabricate company details or contact background. If you can't find something, say so.
2. **Use browser tools for LinkedIn.** Navigate to LinkedIn and search for the person. Don't guess at their background.
3. **Be specific about hooks.** "Fellow IIT Delhi alum" is useful. "You both work in tech" is not.
4. **Flag weak ICP fit.** If the prospect doesn't match the user's ICP, say so clearly. Don't force a fit.
5. **Keep it scannable.** Tables and bullet points, not paragraphs. The user will skim this in 30 seconds.
