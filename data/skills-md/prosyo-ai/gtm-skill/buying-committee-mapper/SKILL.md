---
name: buying-committee-mapper
description: "Use this skill when a B2B deal or target account needs more than one contact: \"who else should I talk to\", \"map the buying committee\", \"multi-thread this deal\", or a single-threaded deal is at risk. Maps the economic buyer, champion, influencers, users, technical evaluator and blockers, names the likely people and titles, scores coverage and sentiment, and produces a multi-threading plan with what each person needs to hear and who should reach them."
license: MIT
metadata:
  title: Buying committee mapper
  category: prospecting
  tags: "Sales, Sales Leaders, SDR"
  author: prosyo
  version: "1.0.0"
  keywords: "buying committee map, stakeholder mapping sales, multithreading deals, claude stakeholder map skill, decision makers b2b"
  inputs: "Account or deal, Known contacts, Deal size and product"
  outputs: "Committee map, Coverage score, Multi-threading plan"
---

Use this whenever a deal depends on one person. Single-threaded deals close far less often than deals with three or more engaged contacts, and they die quietly when the one contact changes jobs or goes quiet.

## Inputs

- The account or deal, its size and stage.
- Contacts already engaged and what each has said.
- The product and the departments it touches.

## The play

### 1. List the roles the deal needs
| Role | Question they answer | Typical titles |
| --- | --- | --- |
| Economic buyer | Is it worth the money? | VP, C-level, budget owner |
| Champion | Will this make my life and my team better? | Manager or director who feels the pain |
| Technical evaluator | Will it work with what we have? | IT, engineering, operations, RevOps |
| Users | Will I actually use it? | Individual contributors |
| Blockers | Is it safe and compliant? | Security, legal, procurement, finance |
| Influencers | What do I recommend? | Peers, advisors, adjacent team leads |

Deal size sets how many roles show up: under $10k often 1-2 people; $10-50k usually 3-5; above $100k usually 6-10.

### 2. Name the people
For each role, find the most likely person at the account. Mark each as confirmed (they told you or you met them) or inferred (from the org chart or titles).

### 3. Score each contact
Engagement (none, aware, engaged, active) and sentiment (supporter, neutral, sceptic, unknown). An unknown blocker is the most dangerous cell on the map.

### 4. Plan the threads
For each gap, decide who reaches out (rep, manager, executive sponsor, solutions engineer), through which route (champion introduction is best, then direct), and what that person needs to hear in their own language.

### 5. Arm the champion
Give the champion the material they need to sell internally: a one-paragraph business case, the security pack, a short answer to the most likely objection from each other role.

## Output format

```
Deal: <account> - <size> - <stage>
Committee:
  role | name | title | confirmed/inferred | engagement | sentiment | what they need
Coverage: <roles engaged / roles needed>  Risk: <single-threaded? unknown blocker?>
Plan: <next 3 actions with owner and date>
Champion kit: <items to send>
```

## What good looks like

- At least three engaged contacts before a deal is called "commit".
- The blocker is identified before the proposal, not after.
- Outreach to new contacts goes through the champion when possible, so it reads as collaboration rather than going around them.
- The common mistake is mapping titles without talking to anyone: a map full of inferred names gives false comfort.

## Rules

- MUST mark each person as confirmed or inferred.
- MUST flag any deal with a single engaged contact as at risk.
- NEVER contact a new stakeholder in a way that undermines the champion without discussing it with them first.

## Example prompts

- "Map the buying committee for our $80k deal with Contoso. I only talk to the IT manager."
- "Who else should I bring into this deal, and how?"
- "Build a multi-threading plan for my top 5 deals."
