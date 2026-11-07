---
name: website-visitor-follow-up
description: "Use this skill when you know which companies visited your website and want to follow up without being creepy: \"turn website visitors into meetings\", \"who should we contact from yesterday's visitors\", \"write outreach for high-intent visits\". Scores visits by page intent and recency, filters to ICP accounts, finds the right person, and writes helpful outreach that matches the topic of the visit without ever mentioning the visit. Includes privacy and consent guardrails."
license: MIT
metadata:
  title: Website visitor follow-up
  category: signals
  tags: "SDR, Marketing, Demand Gen, Sales"
  author: prosyo
  version: "1.0.0"
  keywords: "website visitor outreach, follow up website visitors b2b, reverse ip lookup outreach, claude website visitor skill, intent data follow up"
  inputs: "Company-level visit data, ICP and tiers, Page map of your site"
  outputs: "Ranked visitor accounts, Contact per account, Topic-matched outreach"
---

Use this when company-level website visit data is available. A visit tells you timing and topic; the message must use both without revealing either.

## Inputs

- Company-level visit data: company, pages, number of visits, dates.
- ICP and tiers.
- A map of your site pages to topics and intent level.

## The play

### 1. Map pages to intent
| Page type | Intent | Example |
| --- | --- | --- |
| Pricing, plans, demo, contact | High | /pricing, /demo |
| Comparisons and alternatives | High | /vs-competitor |
| Case studies, integrations, security | Medium-high | /customers, /security |
| Product and solution pages | Medium | /product/scheduling |
| Blog, free tools, careers | Low | /blog/*, /careers |

Careers-page visits are usually job seekers; exclude them. Repeat visits by your own customers are product usage, not intent.

### 2. Score and filter
Score = page intent + visit depth (3+ pages: +) + recency (last 48 hours: +) + repeat visits across days (+). Keep only ICP accounts with no open deal owned by someone else and no current customer status.

### 3. Find the likely person
Match the topic to a persona: pricing plus security pages suggests an evaluator in IT or operations; comparison pages suggest the champion. Pick 1-2 people, not the whole company.

### 4. Write about the topic, never the visit
The message offers something useful on the exact topic they looked at: the comparison, the security pack, a pricing explainer, a customer story in their industry. It should read as well-timed, not watched.

> Subject: scheduling for multi-site teams
>
> Hi Ana, teams running 10+ locations usually ask us the same three questions before switching: how shift swaps work, what it costs per location, and how long rollout takes. Here is a two-minute answer to all three. Happy to walk your team through it if useful.

### 5. Move fast, once
High-intent accounts get a touch within 24 hours. One signal-led touch per account per week, then let the normal sequence take over.

## What good looks like

- Zero mentions of the visit, the pages or tracking, in any message.
- The offered asset matches the pages viewed.
- Low-intent blog traffic is left to marketing, not sent to reps.
- The common mistake is "I noticed someone from your company was on our site", which turns a warm signal into a privacy complaint.

## Rules

- MUST work from company-level data and lawful sources only.
- MUST respect the site's consent settings and regional privacy rules.
- NEVER reference the visit, the pages or the tracking in outreach.
- NEVER treat a single blog visit as a reason for sales outreach.

## Example prompts

- "Here are yesterday's identified visitor companies with pages. Who should we contact and what should we send?"
- "Build an intent score for our site's pages."
- "Write follow-ups for accounts that viewed our comparison pages this week."
