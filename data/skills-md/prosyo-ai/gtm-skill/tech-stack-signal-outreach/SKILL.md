---
name: tech-stack-signal-outreach
description: "Use this skill when a company's technology choices are a buying signal for you: \"target companies using X\", \"they just added a tool we integrate with\", \"technographic outreach\", \"companies switching away from a competitor\". Reads technology signals (tools added, removed or listed in job posts), decides what each change means for your offer (integration fit, replacement window, gap you fill), and writes outreach that leads with the buyer's situation, not the stack lookup. Produces a prioritised account list with the angle for each signal."
license: MIT
metadata:
  title: Tech stack signal outreach
  category: signals
  tags: "SDR, Sales, Founders, Marketing"
  author: prosyo
  version: "1.0.0"
  keywords: "technographic targeting, tech stack signals outreach, companies using a competitor, claude technographic skill, integration based prospecting"
  inputs: "Technology signals per account, Your integrations and competitors, ICP"
  outputs: "Signal verdicts, Prioritised accounts, Angle and message per signal"
---

Use this when the tools a company runs (or stops running) change how relevant you are. The signal gives timing and a hook; the message must still be about the buyer's problem.

## Inputs

- Technology signals per account: tools detected on the site, tools named in job listings, recent additions and removals.
- Your integrations, your competitors, and the tools you complement or replace.
- ICP and tiers.

## The play

### 1. Classify each signal
| Signal | Meaning | Strength |
| --- | --- | --- |
| Uses a tool you integrate with deeply | Lower switching effort, clear workflow story | Medium |
| Just added a complementary tool | Building out the function now | Strong |
| Uses a competitor, contract age unknown | Possible replacement later | Weak alone |
| Job listing asks for experience with a competitor | Committed to it for now, or replacing it soon (read the listing) | Depends |
| Removed a competitor or a related tool | Active change, gap may exist | Strong |
| Uses a legacy tool you replace | Pain likely; replacement window matters | Medium |

### 2. Stack with other signals
A stack signal alone rarely justifies a message. Combine it with fit and a timing signal: a new leader, hiring, funding, or a high-intent visit.

### 3. Pick the angle
- **Integration angle**: what becomes possible when the two tools work together, with a peer example.
- **Gap angle**: what the newly added tool does not cover that you do.
- **Replacement angle**: only near a likely renewal or after a visible problem, and never by attacking the incumbent.

### 4. Write about their world
Lead with the situation the signal implies, not the lookup itself.

> Hi Dev, teams that run their outbound from the CRM usually hit the same wall: reps still research every account by hand before writing. Northwind connected their CRM and now each rep gets a researched list every morning. Is research time an issue for your team?

### 5. Verify before sending
Detection tools are wrong often enough to matter. For Tier 1 accounts, confirm the signal (careers page, docs, public case study) before naming a tool.

## What good looks like

- Every message works even if the tool detection was wrong.
- Replacement plays are timed and respectful of the incumbent.
- Stack signals are combined with fit and timing, not used alone.
- The common mistake is "I see you use <tool>!" as an opener, which reads as surveillance and says nothing about the buyer's problem.

## Rules

- MUST combine stack signals with ICP fit before outreach.
- MUST verify a detected tool before naming it to a Tier 1 prospect.
- NEVER disparage a tool the prospect uses.
- NEVER claim an integration or capability that does not exist.

## Example prompts

- "Here are 300 accounts that added a sales engagement tool this quarter. Who should we contact and how?"
- "Write outreach for companies whose job listings mention our competitor."
- "Build a technographic targeting plan for our integrations."
