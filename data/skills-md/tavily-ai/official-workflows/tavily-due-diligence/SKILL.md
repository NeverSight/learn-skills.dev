---
name: tavily-due-diligence
description: |
  Write a due-diligence memo on one company before an investment, acquisition, partnership or vendor contract, using Tavily. Resolves the company, then covers product, leadership, funding and ownership, customers and traction, lawsuits, regulator actions, sanctions screening, data breaches, news sentiment over a window, and red flags. Searches federal and state court dockets, SEC Form D filings, US, UK, EU, Canadian and Australian privacy and consumer regulators, and OFAC sanctions lists, keeps allegations apart from findings, and lists what could not be checked. Use when the user asks for due diligence, a DD memo, vendor or supplier vetting, a background check on a company, a risk review, or red flags on a company. For a CRM record only use tavily-entity. For comparing several competitors use tavily-competitor-analysis. For a whole market use tavily-market-research.
license: MIT
metadata:
  author: tavily
  version: "0.1.0"
  homepage: https://tavily.com
  source: https://github.com/tavily-ai/official-workflows
allowed-tools: Bash(tvly *)
---

# Tavily due diligence

Produce a memo on one company in which every risk item is dated, sourced, and
labelled as an allegation or a finding.

Resolve the company and fill its record as `tavily-entity` describes. Search
and extract as `tavily-search` describes. If either isn't installed, run
`npx skills add tavily-ai/skills --skill <name>` and read its SKILL.md before
continuing.

## Intake

Infer the company, its domain, and the purpose from the request. Default to a
24-month news window and a 5-year legal window. Ask at most 2 questions: the
domain or country when the name is shared, and whether to screen named
executives as individuals. A vendor review weights security, breaches and
financial stability. An investment review weights team, traction and ownership.

## Sources

Quote the name in every query. `{legal name}` is the registered name
(`'"Acme Corp, Inc."'`) and `{name}` is the name the press uses.

| Check | Search | Then |
|---|---|---|
| UK registration | `'"{brand}"' --include-domains find-and-update.company-information.service.gov.uk` | Extract `/company/{number}` for status, incorporation date, SIC and accounts dates, and `/company/{number}/officers` |
| US registration, funding, officers | `'"{legal name}" Form D' --include-domains sec.gov` | Take the CIK from the hit and extract `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=D&owner=include&count=40` to list every Form D. Each Form D gives state of incorporation, address, directors, amount sold and investor count |
| Funding history | `'"{name}" raises funding round investors'` | Confirm each round on the company press room or a Form D |
| Leadership changes | `'"{name}" CEO steps down OR appointed'` | Compare with the directors on the latest Form D or Companies House officers page |
| Federal litigation | `'"{legal name}" lawsuit OR complaint' --include-domains courtlistener.com,pacermonitor.com` | Extract pacermonitor.com case pages in full: they open with the court, case number, filed and terminated dates and the latest entries. Extract courtlistener.com dockets with `--query 'Citation Date Filed Date Terminated Nature of Suit' --chunks-per-source 2` to get the header alone |
| Opinions, appeals, state courts | `'"{legal name}"' --include-domains law.justia.com,dockets.justia.com` | Use the opinion date and court for the matter's status |
| Current status | `'"{legal name}" settlement OR appeal OR ruling' --topic news --start-date {12 months ago}` | Run before you set any status. Terminated cases get appealed and reopened |
| State attorneys general | `'"{name}" attorney general lawsuit OR settlement'` | Open the AG's own press release |
| US consumer protection | `'"{name}"' --include-domains ftc.gov` | Add the sector regulator's domain |
| EU data protection | `'"{name}" fine GDPR decision' --include-domains edpb.europa.eu,cnil.fr,garanteprivacy.it,autoriteitpersoonsgegevens.nl,dpa.gr,dsb.gv.at` | edpb.europa.eu national-news pages summarise each national fine in English |
| UK, Canada, Australia privacy | `'"{name}" fine enforcement' --include-domains ico.org.uk,priv.gc.ca,oaic.gov.au` | Extract the penalty notice or report of findings |
| US sanctions | `'"{legal name}"' --include-domains ofac.treasury.gov,sanctionssearch.ofac.treas.gov` | Extract any `sanctionssearch.ofac.treas.gov/Details.aspx` or `recent-actions` hit with `--query '{legal name}'` to read aliases and program tags |
| Breaches | `'"{name}" data breach OR security incident OR hacked'` | Find the company's own statement or a regulator notice |
| Workforce | `'"{name}" layoffs OR "job cuts"' --topic news --start-date {window start}` | Keep only items about this company |
| Customers, traction | `'case study OR customer' --include-domains {domain}` and customer press releases | Label each figure as filed or self-reported |
| Sentiment | `'"{name}"' --topic news --start-date {quarter start} --end-date {quarter end} --max-results 20`, one search per quarter | Group the items by month |

Search the regulators in English. Garante and CNIL return their Italian and
French decisions for English queries.

Count a domain-filtered result only when its title or snippet names the
company. When every result scores under 0.2 and none names the company, record
"not found in the sources searched" with the domains and query. Check the UK
and EU sanctions lists on their official search pages, or record "could not
check".

## Collect

1. **Resolve.** Identify the company as `tavily-entity` does: legal name,
   domain, country of registration and former names. Search the registry with
   the brand and read the legal name from the registry page.
2. **Profile.** Fill product, leadership, funding and ownership from the
   company's pages, Form D filings and the registry. Search each founder's and
   executive's previous companies for lawsuits or enforcement that named them.
3. **Measure traction.** Collect named customers, headcount trend and any
   disclosed revenue. Label a figure from a press interview as self-reported.
4. **Screen.** Run each Sources row for the company, its former names and,
   when asked, each executive. Extract every hit before using it. For each
   legal matter, record the forum, case number, filing date, claim and status
   (filed, pending, dismissed, settled, judgment or consent order).
5. **Track sentiment.** Run the quarterly news searches. Mark each item
   positive, negative or neutral by the event it reports, ignoring the writer's
   tone, and name the events behind any spike.
6. **Stop** when every Risk checks row has an outcome and every profile field
   is filled or listed under Not checked.

## Allegations and findings

A complaint, a lawsuit filing, a news report of a claim, or a review is an
allegation. A court judgment, a regulator's final order, a consent decree, an
announced settlement, or the company's own disclosure is a finding. Never
describe an allegation as fact. A settlement without admission is a finding
that the settlement happened, and the claim stays an allegation. A fine under
appeal is a finding with the appeal noted.

## Parallel work

With subagents, split into profile, legal and regulatory, and news. Give each
the legal name, domain, former names, windows and its Sources rows. Have one
subagent check the Quality bar at the end.

## Deliverable

Show the memo in the reply and save it to `diligence/{company}-{YYYY-MM-DD}.md`.

```markdown
# Due diligence: {company}

Legal name: {name} ({country of registration})
Domain: {domain}
Purpose: {investment | vendor | partnership}
As of: {YYYY-MM-DD}
Windows: news {start} to {end}, legal since {YYYY}

## Summary
{2 paragraphs: what the company is, its stage, and the risks that matter most}

## Red flags
- {flag}: {allegation | finding}, {date} ({url})

## Company profile
| Field | Value | Source |
|---|---|---|

## Leadership
| Name | Role | Background | Issues found | Source |
|---|---|---|---|---|

## Funding and ownership
| Date | Round or event | Amount | Investors or holders | Source |
|---|---|---|---|---|

## Customers and traction
- {signal, dated, filed or self-reported} ({url})

## Legal and regulatory
| Date | Forum | Case or action | Claim | Status | Label | Source |
|---|---|---|---|---|---|---|

## Risk checks
| Check | Sources searched | Outcome |
|---|---|---|

## News sentiment
{monthly positive, negative and neutral counts, and the events behind spikes}

## Not checked
- {check}: {why}

This memo uses public web sources and is not a legal or financial opinion.

## Rerun inputs
workflow: tavily-due-diligence
company: {legal name}
domain: {domain}
former_names: {list}
people: {names screened}
purpose: {purpose}
news_window_months: {N}
legal_window_years: {N}
```

## Quality bar

- Every risk item carries a date, a source URL and its label.
- Every Risk checks row reads found, not found in the sources searched, or
  could not check. Never write "clean".
- A matter that shares only a name with the company stays out until a second
  identifier (address, domain, executive, registration number) ties it to the
  company.
- Do not give an investment recommendation. Report the facts and the gaps.
