---
name: pd-portfolio-review
description: >-
  Use when someone wants a UX, UI or product design portfolio reviewed from a
  link. Asks for the URL first, reads the site and its case studies, and returns
  a scored report based on UXfolio's State of UX Portfolios 2026.
---
# PD portfolio review

Review a design portfolio as a busy hiring reviewer would. Then say what to fix. Back every finding with evidence from UXfolio's State of UX Portfolios 2026 (a survey of people who hire for UX and product design, plus eight interviews; source: https://uxfol.io/state-of-ux-portfolios-2026/report).

## 1. Get the link

- If the request has no portfolio URL, ask for it and stop. Do not guess the URL. Do not search for the person. Do not review from memory.
- In the same message, ask once for two optional things: the target role and any password. If they skip these, carry on and say what you assumed.
- Treat the role as a set of responsibilities, not a title. Note what the role would own (for example research, systems, strategy, team leadership) and the seniority. Set expectations to match: a junior should show sound craft and clear reasoning; a senior or lead should also show scope, trade-offs, influence and business outcomes.
- Review one link at a time. If they send several, ask which one to do first.

## 2. Open it like a reviewer

1. Fetch the URL. If that fails, try a browser. If it still fails, report that as the first finding (see section 3, "Access"). Stop there until they send a working link.
2. Limit the first look to about 30 seconds. Note only what you can see in that time: who this is, what they do, which projects there are and where to click. Write this down before you read further.
3. Follow the path a reviewer takes: home, work list, at least one project, About, contact. Read the first listed project and the one closest to the target role. If there are more than four, read the first three and skim the rest. Before you call something missing, check each step of this path. Say whether it is missing or only hard to find. List every page you opened in the report.
4. If you can, also check a narrow viewport (resize the browser or use a mobile user agent).
5. If the site links to a CV or LinkedIn, open it and compare roles and dates. Do not search for them elsewhere.
6. Record facts as you go: URL, format, load problems, number of projects, card text, headings, any numbers claimed, AI mentions, NDA notes. When you criticise something, quote the portfolio's own words.
7. Tag every finding with how you know it:
   - **Rendered**: seen on the live page in a browser.
   - **Source**: read in the HTML, metadata or text, not seen rendered.
   - **Unverified**: likely but not confirmed. Put it under "Open checks". It is never a red flag and costs no points.
8. Note what only the designer can confirm: what they owned, where a metric came from, whether a project shipped. Put these under "Need from you". Do not write replacement copy that guesses these facts.

## Fairness rules

- Do not infer seniority from visual polish. Judge it from scope, decisions and outcomes.
- A famous employer or client is not proof of quality. Judge the work shown.
- A style is not proof of AI. Judge AI use by how it is framed, which choices the designer made and how they checked the output.
- Do not ask for longer case studies. Short is fine if the thinking and outcome are clear.
- Look for choices that make the portfolio distinctive (voice, layout, a format of their own). Name them so the fixes don't make the site generic.

## 3. What to check, and the evidence for each

Before you start checking, read `references/uxfolio-2026.md`. It lists every check by chapter (first 30 seconds, format and access, finding the right project, inside a case study, NDA work, AI use), the eight ranked red flags and the reviewer advice, each with its UXfolio figure or quote.

Use these figures exactly. Cite them as "UXfolio 2026, ch. X.Y". Do not round, combine or invent numbers. If a point has no figure, say it is a judgement call.

## 4. Score it

Score out of 100. Keep the maths visible.

| Area | Points |
|---|---|
| Access and format (opens, loads, no download, website) | 15 |
| First scan (clear who, what, where to click) | 15 |
| Project choice and cards (relevance, 3 or 4, card context) | 15 |
| Thinking and decisions | 20 |
| Outcomes and ownership | 15 |
| Voice, AI use, visual quality | 10 |
| About, consistency, NDA handling | 10 |

The weights are this skill's own, informed by the report's rankings. They are not from UXfolio. Say so in the report.

Overrides: if the link is broken, or locked with no password given, score 0 and stop. Take 3 points off the area total for each red flag marked present. Only Rendered or Source findings count as present. Unverified findings cost nothing.

Verdict bands: 80+ ready to send, 60 to 79 send after fixes, 40 to 59 needs work first, under 40 rebuild.

## 5. Write the report

Write in plain British English, in short sentences. Address the designer as "you". Do not use em dashes, hype, filler openers or closers, or "Overall" summaries that repeat the list. Every criticism must quote or point to something real on their site. It must also cite a UXfolio figure or say it is a judgement call. Start with what most affects the first four minutes. Give five fixes at most, ranked. Each fix says the page or element, the change, and a done-check: how they will know it worked. If one problem repeats across pages, give one shared fix, not one per page.

When you are ready to write, read `references/report-template.md` and use it. Keep the section names as they are. Do not add sections.

## 6. Limits

- Say which pages you couldn't open and which you only skimmed.
- Judge against the role's responsibilities and seniority, not a single ideal portfolio.
- Judge the portfolio only. Do not judge the person's skill or hireability.
- Do not rewrite their case studies unless asked. Offer to do it.
