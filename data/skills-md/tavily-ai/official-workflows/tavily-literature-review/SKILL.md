---
name: tavily-literature-review
description: |
  Write a sourced literature review from research papers, preprints, working papers and technical reports, using Tavily. Finds both the recent work and the foundational papers across arXiv, PubMed, NBER, SSRN and publisher journals, and reads each paper's own page before citing it. Use when the user wants a literature review, a survey of studies, related work for a paper, the state of the art on a method, a summary of RCTs or meta-analyses, or what papers say on a topic. Prefer this over tavily-research when the evidence should be published papers rather than web pages.
license: MIT
metadata:
  author: tavily
  version: "0.1.0"
  homepage: https://tavily.com
  source: https://github.com/tavily-ai/official-workflows
allowed-tools: Bash(tvly *)
---

# Tavily literature review

Produce a literature review in which every paper listed was found with Tavily
and opened before it was cited.

Search and extract as `tavily-search` describes. If it isn't installed, run
`npx skills add tavily-ai/skills --skill tavily-search` and read its SKILL.md
before continuing. When the user wants web sources weighed alongside papers
(market data, policy, news), hand that part to `tavily-research`.

## Intake

Infer the topic, field, date window and paper count. Default to 15 papers and
the last 5 years. Origin papers and the papers the field treats as canonical go
in at any date, marked Foundational whether or not they predate the window. Ask
at most 2 questions, only when the answer changes which papers qualify: an
acronym with two meanings, a method versus an application area, or a
study-type constraint. State the defaults in the review. For one named paper,
search its title in quotes and skip Collect. For every paper that does X, such
as all papers on a benchmark, search the benchmark name, then each strong
method's name with `outperforms`.

## Sources

| Field | Search domains |
|---|---|
| CS, ML, NLP | arxiv.org |
| Physics, math | arxiv.org, journals.aps.org, iopscience.iop.org |
| Clinical, biomedical | pubmed.ncbi.nlm.nih.gov, pmc.ncbi.nlm.nih.gov, the field's journals, medrxiv.org (clinical) or biorxiv.org (lab biology) |
| Psychology, education | psycnet.apa.org, journals.sagepub.com, tandfonline.com, sciencedirect.com, eric.ed.gov, osf.io, pubmed.ncbi.nlm.nih.gov |
| Economics, social science | nber.org, iza.org, aeaweb.org, academic.oup.com, papers.ssrn.com |
| Chemistry, materials, energy | nature.com, science.org, pubs.acs.org, pubs.rsc.org, onlinelibrary.wiley.com, sciencedirect.com |
| Environmental science | sciencedirect.com, pubs.acs.org, nature.com, pubmed.ncbi.nlm.nih.gov; ipbes.net, eea.europa.eu, fao.org for assessments |
| Law | the journals' own sites (yalelawjournal.org, harvardlawreview.org, californialawreview.org), papers.ssrn.com, dl.acm.org |
| Any other field | search `<topic> review` with no domain filter, then search the sites of the venues the top results come from |

A topic spanning two rows uses both rows.

- **CS and ML.** Search `arxiv.org` alone; adding conference sites returns
  duplicates. Dedupe by arXiv ID, then by title, as a paper can hold two IDs.
- **Clinical.** For a drug, name it or the trial in the query and search
  nejm.org, thelancet.com and jamanetwork.com, then read the paper from its
  PubMed page. For a behavioural intervention, add `randomized controlled
  trial` or `meta-analysis` to the query. On medRxiv and bioRxiv keep only
  `/content/` URLs.
- **Economics.** Search nber.org first. Policy reports are on gov.uk, cbo.gov
  and oecd.org.
- **Law.** A recent article's footnotes map the field. Replies run in each
  journal's online section.

### Reading papers

Get the title, authors, date, venue and abstract from the paper's own page,
never from a search snippet, a search-result title, or memory. Extract several
papers in one call.

- **arXiv.** Extract `arxiv.org/pdf/<id>`; its first page gives the title,
  authors and abstract. The ID gives the first version's year and month
  (`2211.` is November 2022). Cite `arxiv.org/abs/<id>`.
- **PubMed.** Extract `pubmed.ncbi.nlm.nih.gov/<pmid>/`, which gives journal,
  date, DOI, authors, abstract, and the comments and errata linked to the
  paper. Cite that URL.
- **Journals.** Extract the publisher page with `--extract-depth advanced` and
  no `--query`. On ScienceDirect use the `/science/article/pii/<pii>` URL. When
  the page holds no abstract, search the title in quotes and read a PubMed,
  PMC, repository or author-hosted copy. Cite `doi.org/<doi>`.
- **Venue check.** For a preprint or working paper whose page names no venue,
  search its title in quotes on the venue sites: proceedings.mlr.press,
  proceedings.neurips.cc, proceedings.iclr.cc, aclanthology.org and
  openaccess.thecvf.com for ML; the field's journal domains otherwise. When
  nothing confirms the venue, type it preprint and write "venue unverified".
- **Numbers.** For a number from the body, extract the PDF or
  `pmc.ncbi.nlm.nih.gov/articles/PMC<id>/` with `--query` naming the result and
  `--chunks-per-source 3`.

## Collect

1. **Anchor.** Run 3 to 5 searches on the search domains with `--depth
   advanced --max-results 10 --start-date <window start>`: the problem in the
   field's own terms, the method's name, and the benchmark or dataset name.
   Run one more with no start date for replications and null results.
2. **Foundational.** Run searches with no start date on the search domains
   for every name and spelling of the topic, with word-order variants and the
   measured quantity (`<topic>`, `<topic reworded>`, `<measured quantity>`).
   Then search the mechanism, method or assay names the field uses, whose
   papers often never name the topic. Add one search for `<topic> review` and
   one for `<topic> meta-analysis` or `survey`, with no date.
3. **Expand.** Take the newest survey, meta-analysis or Cochrane review and
   one older, highly visible review. Extract each once without `--query`, from
   `arxiv.org/pdf/<id>` for an arXiv review and from the PMC page when the
   PubMed page links one. If neither the body nor the reference list came
   back, pick another review. List the papers each review names as the origin
   of the topic or as the main evidence for a category, then search each title
   in quotes to reach its page. A paper named by two reviews, or in the
   introductions of several anchor results, is foundational. Use
   `--query '<category> methods'` only when the body was cut off. Never take a
   venue from a review's reference list.
4. **Contest.** For each Key paper a later paper disputes, find the challenge.
   Search the paper's title with `comment`, `reply`, `Matters Arising`,
   `failure to replicate` or `reanalysis`, and follow the comment links on its
   PubMed page. Keep both sides and the authors' reply.
5. **Read** the page of every paper you keep, and full text only for a
   number, dataset size, baseline or limitation you will cite.
6. **Select.** Every foundational paper from step 3 goes into Key papers if
   its abstract reports a measured result on the topic, even when its headline
   is another outcome, or if it is a review naming the topic as its focus. Drop
   one only by listing it under Out of scope with the reason. Fill the next
   slots from step 2 results whose titles name the topic, then from the window.
   Foundational papers count toward the target; comments and replies sit under
   the paper they answer and don't. Aim for about a third from the last 12
   months when that many exist. Go over the target rather than drop a
   foundational paper or one side of a dispute, and say by how much in Scope.
   **Stop** at the target, or when two expansion rounds add no relevant
   papers. Say which.

Check `failed_results` and the body of every extract. List a paper no page
could be read for under Inaccessible.

## Parallel work

With subagents, split by subtopic or by step (anchor, foundational, reviews).
Run at most three agents on one API key; when a call returns an
excessive-requests error, wait 60 seconds and run calls one at a time. Have
one agent check that every claim cites a Key paper.

## Deliverable

Show the review in the reply and save it to `reviews/{title}.md`, with a 3 to
6 word title in sentence case.

```markdown
# Literature review: {topic}

Scope: {field, date window, target count, and any defaults assumed}
As of: {YYYY-MM-DD}
Papers: {count kept} ({peer-reviewed}, {preprints and working papers}, {reports}; {reviews and meta-analyses among them}; {foundational} from before the window)

## Summary
{2 to 3 paragraphs on what the literature shows}

## Key papers
### {Title} ({year, or both years as the Quality bar describes})
- Authors: {first author et al.}
- Venue: {journal or conference, or the preprint server or working-paper series}
- Type: {peer-reviewed | law review | preprint | working paper | report}, {design: RCT, meta-analysis, cohort, theory, method, review}
- Link: {abs, PubMed, DOI or venue page URL}
- Finding: {one or two sentences, from the abstract or the read passage}
- Result: {headline number with its comparison, the main theorem for theory papers, or "not reported in abstract"}
- Method: {data, model or study design, with population or sample for empirical work}
- Relevance: {why it belongs, and "Foundational" for an origin or canonical paper}

## Themes and consensus
{what several papers agree on, citing them by title}

## Open questions and disagreements
{where results conflict or a question is unanswered, citing both sides and any reply}

## Recent work
{papers from the last 12 months and what they change}

## Not included
- Inaccessible: {titles and URLs that failed to extract}
- Out of scope: {near-misses a search returned, and why}

## Coverage
Searches: {the queries and domain filters used, and the reviews expanded}
Stop: {hit the target | two rounds added nothing}
Likely gaps: {venues or subfields these searches did not reach}

## Rerun inputs
workflow: tavily-literature-review
topic: {topic}
field: {field}
since: {YYYY-MM-DD}
target_count: {N}
```

## Quality bar

- Every claim in Themes, Open questions and Recent work cites a Key paper.
- Authors, Finding, Result and Method come only from text you extracted,
  including first names and initials. A design, sample or number the abstract
  doesn't state is "not reported in abstract", never filled in from memory.
- A preprint or working paper is never described as published. Call it
  peer-reviewed only when the venue check or the paper's PubMed or journal
  page shows the venue.
- The year is the first version's year for a preprint and the issue year from
  the journal page's volume and issue line for a journal article. When they
  differ, give both (`arXiv 2022; ICML 2023`, `online 2018; issue 2019`).
  Decide the window by the version you cite, not an earlier working-paper
  draft.
- Design comes from the title and abstract, whatever the page labels it.
- The abstract describes the paper cited, not an editor's summary of another
  paper in the same Science or Nature issue.
- Effect sizes keep each paper's sign convention, stated once per theme, from
  the corrected version when an erratum exists.
