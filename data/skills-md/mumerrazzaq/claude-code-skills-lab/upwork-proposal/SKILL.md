---
name: upwork-proposal
description: |
  Write winning Upwork proposals that stand out from AI-generated spam.
  This skill should be used when the user pastes an Upwork job description and wants to bid, or says "write proposal", "apply for this job", "bid on this".
---

# Upwork Proposal Skill

Generate proposals that beat the AI flood and actually get responses.

## The Problem We're Solving

Clients receive 50+ proposals that all sound the same: robotic, vague, and stuffed with "Dear Hiring Manager." They can smell generic AI instantly. This skill creates proposals that feel human, specific, and worth responding to.

## Key Stats (2025-2026)

| Metric | Value |
|--------|-------|
| Average proposals per job | 20-50 |
| Reply rate | 8-30% |
| Win rate | ~5% (1 in 20) |
| AI+Human hybrid win rate | **48% higher** than pure AI or pure manual |
| Optimal proposal length | **150-250 words** |
| First-hour applications | 48% higher response rate |

## Workflow

```
User pastes job → Extract requirements → Match to user skills → Generate proposal + shorter version
```

## Required Input

| Input | Description |
|-------|-------------|
| **job_description** | The Upwork job posting (user pastes it) |

## Optional Inputs (Ask if relevant)

| Input | When to Ask |
|-------|-------------|
| **relevant_experience** | If job matches a specific past project |
| **rate/pricing** | If user wants to include specific pricing |
| **availability** | If job mentions urgency or timeline |
| **special_angle** | If user has unique insight into the problem |

## The 7-Part Formula (24%+ Response Rate)

See `references/proposal-structure.md` for details. Quick reference:

| Part | Length | Purpose |
|------|--------|---------|
| **Hook** | 25 words | Client name + their specific problem |
| **Relevance** | 50-75 words | Similar experience with results |
| **Solution** | 50-75 words | Bullet-point deliverables |
| **Proof** | 30-50 words | 1-2 past projects with metrics |
| **Timeline** | 15-25 words | Specific dates, not vague |
| **Investment** | 10-15 words | Clear pricing if appropriate |
| **CTA** | 15-20 words | One specific next step |

**Total: 195-285 words** (under 300 is ideal)

## Anti-AI-Slop Rules

See `references/standout-strategies.md` for full guide. Critical rules:

| DO | DON'T |
|----|-------|
| Start with "Hey there" or use client's name | "Dear Hiring Manager" or "I hope this finds you well" |
| Mention 2 specifics from their job post | Generic "I'm the perfect fit for this role" |
| Use numbers: "23 similar projects", "$12K/month results" | Vague claims: "extensive experience" |
| Natural contractions: "I'll", "you're", "can't" | Robotic: "I would be delighted to" |
| One emoji max (👋 in greeting) | Multiple emojis or none at all |
| Specific timeline: "December 15th" | Vague: "as soon as possible" |
| Lead with solution approach | Lead with credentials |

## Testing Instruction Detection

Clients often add tests like "Write HOWDY at the top" to filter spam. **Always scan the job for:**
- Specific words to include
- Questions to answer
- Hidden instructions in the middle/end of posting

If found, follow them FIRST.

## Output Format

Always provide TWO versions (user frequently asks for shorter):

```markdown
## Proposal (Ready to Submit)

[Full proposal following 7-part formula]

## Shorter Version

[Condensed 100-150 word version]

## One-Liner (For quick reference)

[Single sentence pitch]

## Notes

- [Relevant past projects to mention]
- [Questions to ask client]
- [Red flags if any]
```

## User's Style Preferences

From 12 Upwork conversations analyzed:

1. **Greeting**: "Hey there 👋" or "Hi there 👋"
2. **Tone**: Natural, humanized, conversational
3. **Structure**: Solution-first, then experience
4. **Length**: Always asks for shorter - start concise
5. **Honesty**: Never oversells, mentions learning areas
6. **Tech mentions**: n8n, Python, AI agents, Google Workspace

## User's Skill Positioning

See `references/user-profile.md`. Quick reference:

**Highlight these:**
- n8n workflow automation
- AI agents / Agentic AI (PIAIC certified)
- Python, FastAPI
- API integrations
- Google Workspace automation
- WhatsApp Business API

**Be honest about:**
- React, Node.js (learning)
- Make/Zapier (concepts understood, not hands-on)

## Engineering Methodology (Trust Signal)

User follows **Spec-Driven Development (SDD)** and **Test-Driven Development (TDD)**.

**When to mention this:** Only for projects where quality/reliability matters:
- Complex automation with multiple integrations
- Long-term/ongoing projects
- Clients who mention "reliable", "production-ready", "maintainable"
- Higher-budget projects ($500+)
- Clients burned by previous freelancers

**DON'T mention for:** Simple one-off tasks, quick fixes, low-budget gigs.

**What you deliver (in repo):**
- `specs/` - Requirements & design specs (per phase)
- `tests/` - Pytest test suites (written BEFORE code)
- `docs/ADRs/` - Architecture Decision Records
- Self-documenting code with clear structure

**How to phrase it naturally:**
```
I follow spec-driven development — I'll document requirements first,
write tests, then implement. You'll get working code plus specs and
tests in the repo, not just "it works on my machine."
```

**Shorter version:**
```
I write specs and tests first, so you get reliable, documented code.
```

**One-liner (when relevant):**
```
All deliverables include specs, tests, and documentation in the repo.
```

See `references/engineering-methodology.md` for full details.

## Example Transformation

**Generic AI slop:**
```
Dear Hiring Manager,
I hope this message finds you well. I am writing to express my keen interest in your project. With my extensive experience in automation and workflow development, I am confident I can deliver exceptional results. I have worked on numerous similar projects and would be delighted to discuss further.
```

**Winning proposal:**
```
Hey there 👋

I can help you automate your Google Sheets → AI → PDF → Email workflow in n8n.

Here's the plan:
- Connect Google Sheets with scheduled triggers (twice weekly)
- Pass data to ChatGPT/DeepSeek for processing
- Generate formatted PDF (via API or Google Docs conversion)
- Auto-send via Gmail

I recently built a similar workflow connecting Sheets with ChatGPT for automated reporting — happy to share details.

When would you like to kick off?
```

## Checklist Before Output

- [ ] Read ENTIRE job post (including hidden test instructions)
- [ ] Extracted 2+ specific requirements to address
- [ ] Under 250 words
- [ ] Starts with personalized hook (not "Dear Hiring Manager")
- [ ] Includes specific approach/solution
- [ ] Has concrete proof (numbers, past projects)
- [ ] Clear CTA at the end
- [ ] Shorter version provided
- [ ] Natural tone, contractions used
- [ ] No overselling or vague claims
