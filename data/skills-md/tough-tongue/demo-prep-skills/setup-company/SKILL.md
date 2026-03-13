---
name: setup-company
description: Set up your company profile and personal background for demo preparation. Use when setting up demo-prep-skills for the first time, or when the user wants to update their company context. Creates a company-profile.md that all other skills reference.
license: MIT
metadata:
  author: toughtongueai
  version: "1.0"
---

# Company Profile Setup

Create a `company-profile.md` file that all other demo-prep skills use as context. Run this once when you first install the skills, and update it whenever your product, positioning, or team changes.

## When to Use

- First time setting up demo-prep-skills
- User says "set up my demo prep profile" or "configure my company"
- The `company-profile.md` file doesn't exist yet
- User wants to update their company info or positioning

## Process

### Step 1: Check for Existing Profile

Look for `company-profile.md` in the workspace root. If it exists, ask: "You already have a company profile. Want to update it or start fresh?"

### Step 2: Gather Information

Ask the user for each section below. Ask questions conversationally — don't dump a form. If they provide a website URL or docs link, research it first and pre-fill what you can, then confirm with the user.

**Required:**

1. **Company name and website**
2. **What you sell** — 2-3 sentence description. What problem does it solve? Who is it for?
3. **Your name and role** — Name, title, LinkedIn URL (optional)
4. **Your ICP** — Ideal customer profile: role titles, company size, industries you sell to
5. **Key differentiators** — 2-3 things that make you different from alternatives
6. **Common objections** — Top 3 objections prospects raise, and how you typically respond

**Optional (but improves output quality):**

7. **Docs URL** — An `llm.txt` file, docs site, or knowledge base the agent can reference for deeper product knowledge
8. **Pricing** — Pricing model and ranges (this stays local, never shared)
9. **Proof points** — Customer logos, case study headlines, key metrics (e.g., "200+ customers", "30% conversion lift")
10. **Your background** — Education and previous companies (used to find shared connections with prospects)
11. **Co-founders / key team** — Names and backgrounds (for additional shared-connection matching)
12. **Sales motion** — How you sell: inbound-led, outbound, PLG, enterprise, channel
13. **Competitor list** — Top 3-5 competitors and your positioning against each

### Step 3: Generate the Profile

Write the `company-profile.md` file using the format below. Save it to the workspace root.

### Step 4: Confirm and Advise

After saving, tell the user:

> Your company profile is saved. All demo-prep skills will now use this context automatically.
>
> To update it later, just say "update my company profile."
>
> Tip: If you're using this repo for a team, you can commit `company-profile.md` so everyone shares the same context. If it's personal, it's already in `.gitignore`.

## Output Format

Save the following as `company-profile.md` in the workspace root:

```markdown
# Company Profile

## Company
- **Name:** [Company Name]
- **Website:** [URL]
- **Industry:** [Your industry / category]
- **Sales Motion:** [Inbound / Outbound / PLG / Enterprise / Mixed]

## Product
[2-3 sentence description of what you sell and the problem you solve]

## ICP (Ideal Customer Profile)
- **Target roles:** [VP Sales, Head of Engineering, etc.]
- **Company size:** [e.g., 50-500 employees, Series A-C]
- **Industries:** [e.g., B2B SaaS, fintech, healthcare]
- **Signals:** [What indicates a company is a good fit — e.g., "hiring SDRs", "has Book a Demo button"]

## Differentiators
1. [First differentiator]
2. [Second differentiator]
3. [Third differentiator]

## Common Objections
| Objection | Your Response |
|-----------|--------------|
| [Objection 1] | [How you typically respond] |
| [Objection 2] | [How you typically respond] |
| [Objection 3] | [How you typically respond] |

## Proof Points
- [Key metric, customer logo, or case study headline]
- [Key metric, customer logo, or case study headline]

## Pricing
- [Pricing model and ranges — keep this for internal prep only]

## Your Profile
- **Name:** [Your name]
- **Role:** [Your title]
- **LinkedIn:** [URL]
- **Background:** [Previous companies, education — used for finding shared connections]

## Team
- [Co-founder / key team member name] — [Background snippet]

## Competitors
| Competitor | Your Positioning Against Them |
|-----------|------------------------------|
| [Competitor 1] | [1-sentence positioning] |
| [Competitor 2] | [1-sentence positioning] |
| [Competitor 3] | [1-sentence positioning] |

## Docs / Knowledge Base
- [URL to llm.txt, docs site, or knowledge base — optional]
```

## Instructions

1. **Be conversational, not form-like.** Ask questions one section at a time, not all at once.
2. **Pre-fill from research.** If they give you a website URL, visit it and draft the product description, ICP, and differentiators. Then ask them to confirm or edit.
3. **Don't skip objections.** This is the highest-leverage section — objection handling across all other skills depends on it.
4. **Encourage specificity.** "We're better than competitors" is useless. "We deploy in 3 days vs. their 3 months" is actionable.
5. **The profile should be readable by a human and an agent.** Use simple markdown, no complex nesting.
