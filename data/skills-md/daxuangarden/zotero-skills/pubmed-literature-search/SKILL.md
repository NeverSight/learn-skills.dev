---
name: pubmed-literature-search
description: Search PubMed through PubMed MCP, inspect PMID metadata, expand related/review literature, and export a Markdown review plus EndNote-compatible RIS references by default unless chat-only/no-export is explicit.
license: MIT
compatibility: codex,opencode,zcode
metadata:
  workflow: biomedical-literature-search
  requires: pubmed-mcp
  optional: zotero-mcp
  version: 1.0.0
---

# PubMed Literature Search Skill

## Overview

Use PubMed MCP tools as the primary biomedical literature-search layer. This skill is for direct PubMed / NCBI searches, PMID metadata inspection, related-article and review discovery, OA full-text triage, and automatic Markdown + RIS export unless the user explicitly chooses chat-only/no-export mode. It can be used independently from `zotero-evidence-review`; when Zotero tools are visible, use Zotero only as an optional local-library cross-check and import-suggestion layer, never as a PubMed search client.

Default output is Chinese-first when the user writes in Chinese, while official bibliographic metadata, article titles, journal names, DOI, PMID, and RIS field tags remain in their original/official format.

---

## 0. Intent Detection

Route the request before choosing tools. Do not ask the user to choose a mode when the intent is clear.

| Intent | User input features | Route to |
|---|---|---|
| `search` | Biomedical topic, keywords, natural-language question, disease/exposure/outcome, MeSH terms, or requests such as "search PubMed", "find papers", `检索 PubMed`, `找 PubMed 文献` | **Module 1: PubMed Search Workflow** |
| `pmid` | Specific PMID list, PubMed URL, DOI/title plus request for details, abstract, citation, or RIS | **Module 2: PMID Metadata Inspection** |
| `related` | A key PMID/article plus words such as related, similar, reviews, citation chain, `相关文献`, `综述`, `相似文献` | **Module 3: Related and Review Expansion** |
| `fulltext` | Request to check OA/full text/PDF availability for PMID(s) | **Module 4: OA Full-text Triage** |
| `package` | Request for saved report, EndNote/RIS, reusable literature review, `生成报告`, `导出参考文献`, `保存结果` | **Module 5: PubMed Review Package Export** |
| `health` | MCP status, PubMed server status, cache status, `状态检查`, `health check`, `preflight` | **Module 0.5: PubMed MCP Health Check** |

### Routing Rules

1. `/pubmed-literature-search` is the recommended user-facing entry point. Treat it as a request to run this skill and auto-route from the user's topic or PMID input.
2. If the user says `只在聊天输出`, `不要生成文件`, `不导出`, or `chat only`, keep the response in chat and do not write package files.
3. For topic searches, PMID inspection requests, related/review expansion, EndNote/RIS requests, saved reports, reusable literature reviews, or `完整工作流`, run the relevant search/inspection workflow first, then Module 5 by default unless chat-only/no-export is explicit.
4. If the request includes both a broad topic and a key PMID, run topic search first and then use the key PMID for related/review expansion.
5. If PubMed MCP tools are unavailable, do not claim that a PubMed search ran. Provide the planned query and report status as `⚠️ Tool unavailable; search not executed`.
6. If intent is ambiguous, ask the user to choose:

```markdown
我可以按以下哪种方式处理？
1. PubMed 主题检索（关键词/MeSH/自然语言问题）
2. PMID 元数据检查（摘要、作者、DOI、期刊、引用信息）
3. 相关/综述扩展（similar articles / reviews）
4. OA 全文可用性检查
5. 生成 Markdown 报告 + EndNote RIS
```

### Default Export and Zotero Cross-Check

Use these defaults for PubMed-first work:

1. **PubMed default export**: PubMed topic search default output is a Markdown PubMed review report plus EndNote-compatible RIS. PMID inspection and related/review expansion also continue to Module 5 when they produce reusable selected records, unless the prompt explicitly says chat-only/no-export.
2. **Chat-only opt-out**: only explicit `只在聊天输出`, `不要生成文件`, `不导出`, or `chat only` suppresses package writing.
3. **Zotero optional cross-check**: when Zotero MCP tools are visible, perform a read-only local-library cross-check for selected/exported PMIDs by PMID, DOI, and normalized title after PubMed metadata inspection. Record `In Zotero?`, the Zotero match route, and `recommend citing / consider importing / already in library`.
4. **No Zotero mutation**: do not import PubMed records into Zotero, attach PDFs, batch tag, or move collections unless the user explicitly confirms that separate action.
5. **PubMed-only RIS boundary**: only PMIDs with completed PubMed metadata inspection can enter RIS. Zotero cross-check status does not make an uninspected PubMed hit citation-ready.

---

## 0.25 PubMed MCP Readiness and Runtime Availability

Use this readiness gate before any PubMed-dependent workflow. Static validation of this skill only checks the Markdown specification; it does not connect to PubMed, does not run NCBI queries, and does not prove runtime MCP tools are visible in the active Agent IDE session.

### Dependency Model

| Layer | Requirement | Runtime availability rule |
|---|---|---|
| PubMed MCP | Required (`metadata.requires: pubmed-mcp`) | The active session must expose callable PubMed / NCBI tools before searches, PMID inspection, related/review expansion, or PubMed-only RIS generation. |
| Zotero MCP | Optional (`metadata.optional: zotero-mcp`) | Zotero tools may be used only for read-only local-library cross-checks or later import suggestions; Zotero is not a PubMed search client. |
| Static validation | Repository-side guardrail only | `scripts/validate-skill.py --skill pubmed-literature-search` checks structure and guardrail text; it does not run live MCP smoke tests. |

Expected PubMed MCP tools for PancrePal-style servers include `pubmed_search`, `pubmed_get_details`, `pubmed_extract_info`, `pubmed_find_related`, `pubmed_detect_fulltext`, `pubmed_download_fulltext`, `pubmed_system_status`, and `pubmed_manage_cache`. Actual availability depends on the active session.

### PubMed Status Decision Tree

| Condition | Required report status | RIS consequence |
|---|---|---|
| No PubMed-capable tool is visible | `⚠️ Tool unavailable; search not executed` | Do not create PubMed-only RIS records; provide a copyable query. |
| Tool is visible, but workflow is explicit chat-only/no-export | `Completed` only if the search/details actually ran; otherwise `Not executed` with reason | Do not create package files for that run. |
| PubMed search call failed | `Failed; query reported` | Do not create PubMed-only RIS records from failed queries. |
| PubMed search ran and selected PMID metadata was inspected | `Completed` | PubMed-only RIS records are allowed for inspected records with sufficient metadata. |

Only actual PubMed execution plus inspected metadata can justify `Completed` or PubMed-only RIS inclusion. Tool visibility alone is not enough.

### Sequential Execution Guardrail

PubMed workflows are dependency chains, not batch jobs. Do not schedule `pubmed_search` in the same tool-call batch as downstream tools that require its returned PMIDs, including `pubmed_get_details`, `pubmed_extract_info`, `pubmed_find_related`, `pubmed_detect_fulltext`, or `pubmed_download_fulltext`.

Run one PubMed step, inspect its result, and only then decide whether the next PubMed step has valid inputs. If `pubmed_system_status`, `pubmed_search`, or any required upstream PubMed call fails, stop the PubMed chain immediately, report `Failed; query reported` with the attempted query/error, and do not schedule dependent details, related, full-text, export, or PubMed-only RIS steps.

If a search returns zero usable PMIDs, revise and retry the query at most once when broadening is appropriate. The retry must be a separate MCP call after inspecting the failed or empty result, not a downstream call pre-scheduled in the same tool-call batch. If no usable PMIDs are returned after that, report zero hits and do not fabricate PMIDs or continue to metadata inspection.

### Scheduled Tool Failure Handling

When an MCP result says `Tool skipped because a previous tool call in the scheduled sequence failed`, treat the skipped tool as **not executed**. Do not interpret it as a PubMed zero-hit result, unavailable PMID, or metadata failure. Identify and report the first failed tool in that scheduled sequence as the root cause; then, if the skipped search or inspection is still needed, rerun that specific upstream PubMed tool as a separate MCP call after the failure has been inspected.

Never chain additional PubMed dependent calls after a scheduled-sequence failure. First stabilize the upstream status/search call, then continue with one inspected step at a time.

---

## 0.5 PubMed MCP Health Check

Use when the user asks whether PubMed MCP is ready. Keep this read-only.

### Checks

| Check | Tool | What to report |
|---|---|---|
| Server status | `pubmed_system_status` | Whether the server is reachable, transport mode, abstract/full-text mode, and API key/anonymous mode if reported. |
| Cache status | `pubmed_manage_cache` with stats only | Cache counts and storage status. |
| Smoke search | `pubmed_search` with a small safe query if the user requests a live smoke test | Query, hit count, and whether metadata details can be retrieved. |

Never clear PubMed caches, download full text, edit Zotero, or import records during a health check unless the user explicitly confirms the action.

---

## Tool Selection

Choose the smallest PubMed MCP call that satisfies the task:

- **Topic discovery** → `pubmed_search` with Boolean terms, MeSH terms, filters, `sort_by`, `days_back`, and `format`.
- **Scanning many hits** → `pubmed_search` with `format="compact"`.
- **Evidence-level review** → `pubmed_search` with `format="standard"` or `format="detailed"` for selected result sets.
- **Canonical PMID metadata** → `pubmed_get_details` before citing, deduplicating, exporting, or recommending selected PMIDs.
- **Targeted fields** → `pubmed_extract_info` for `basic_info`, `authors`, `abstract_summary`, `keywords`, or `doi_link`.
- **Related papers** → `pubmed_find_related` with `type="similar"`.
- **Reviews** → `pubmed_find_related` with `type="reviews"`.
- **OA full-text availability** → `pubmed_detect_fulltext`.
- **OA download** → `pubmed_download_fulltext` only when OA is available, useful for the workflow, and the user confirms or explicitly requested download.
- **Diagnostics** → `pubmed_system_status` and `pubmed_manage_cache`; cache cleaning requires explicit confirmation.

---

## Safety Rules

- Never fabricate PMIDs, DOI, titles, authors, journals, years, abstracts, statistics, or RIS records.
- Do not report PubMed status as `Completed` unless the relevant PubMed tool call actually ran and selected metadata was inspected.
- Do not create PubMed-only RIS records from uninspected search snippets.
- Maintain a PMID Inspection Ledger for every PMID that is recommended, exported, excluded for metadata reasons, or considered for RIS.
- Do not treat Zotero MCP as PubMed MCP.
- Ask before `pubmed_download_fulltext` unless the user explicitly requested OA PDF/full-text download in the current task.
- Ask before `pubmed_manage_cache` clean/clear actions.
- Ask before importing PubMed results into Zotero, batch tagging, moving collections, or changing local library data.
- When a query fails or tools are unavailable, report the attempted/planned query and failure status rather than inventing results.

---

## 1. PubMed Search Workflow

Use for topic-level biomedical literature searches.

### Process

1. Parse the request into PICO/PECO-style components when possible: population, exposure/intervention, comparator, outcome, study type, date range, and required filters.
2. Build one primary PubMed query using explicit Boolean grouping. Use MeSH terms when obvious, but do not overconstrain if the user's topic is exploratory.
3. Choose result size and sort:
   - broad scan: `max_results=20`, `sort_by="relevance"`, `format="standard"`;
   - recent scan: `sort_by="date"` and `days_back` when the user asks for recent literature;
   - systematic-style scan: use a larger result count only when the user requests breadth.
4. Execute `pubmed_search` only if PubMed MCP is visible.
5. Inspect selected candidate PMIDs with `pubmed_get_details` or `pubmed_extract_info` before making citation recommendations.
6. When Zotero MCP is visible, run a read-only Zotero local-library cross-check for selected/exported PMIDs by PMID, DOI, and title after PubMed metadata inspection; record `In Zotero?`, match route, and import/citation recommendation.
7. Record every selected, recommended, excluded-for-metadata, or RIS-candidate PMID in the PMID Inspection Ledger with inspection status, route/tool, inspected fields, DOI, abstract status, metadata/retraction warning, evidence use, and RIS action.
8. Classify results by relevance, study type, evidence role, and citation readiness.
9. If no results are found, revise the query once by broadening synonyms, removing overly narrow filters, or switching from MeSH-heavy to keyword-heavy terms.
10. Unless the prompt explicitly says chat-only/no-export, continue to Module 5 and write the PubMed review Markdown report plus RIS.

### Chat Output

```markdown
## PubMed Search Summary

- Status: `{Completed|Failed; query reported|Not executed|⚠️ Tool unavailable; search not executed}`
- Query: `{actual or planned PubMed query}`
- Scope: `{population/exposure/outcome/date/study type}`
- Hits reviewed: `{n}`
- Selected PMIDs inspected: `{PMID list or none}`

| Priority | Citation | PMID | DOI | Study type | Main relevance | Caveat |
|---:|---|---|---|---|---|---|
| `1` | `{Author et al., year}` | `{PMID}` | `{DOI or —}` | `{type}` | `{why it matters}` | `{limitation}` |

### Recommended next step
- `{refine query / inspect full text / export package / search related reviews / no action}`
```

---

## 2. PMID Metadata Inspection

Use when the user provides PMID(s), PubMed URLs, or asks for citation-ready metadata.

### Process

1. Normalize input to PMID strings.
2. Retrieve details with `pubmed_get_details` for up to 20 PMIDs at a time.
3. Use `pubmed_extract_info` only when targeted fields are enough.
4. Report missing DOI, missing abstract, retraction concern if surfaced, publication type, and whether the record is citation-ready.
5. Add every inspected PMID to the PMID Inspection Ledger; mark PMIDs that came only from search snippets as `not inspected` and exclude them from RIS by default.
6. Do not infer missing metadata from memory.

### Output Table

```markdown
| PMID | Short citation | Title | Journal | Year | DOI | Abstract status | Citation-ready? | Notes |
|---|---|---|---|---:|---|---|---|---|
| `{pmid}` | `{Author et al.}` | `{title}` | `{journal}` | `{year}` | `{doi or —}` | `{available/missing}` | `{yes/no/verify}` | `{notes}` |
```

---

## 3. Related and Review Expansion

Use after one or more key PMIDs have been identified.

### Process

1. Confirm each seed PMID has inspected metadata.
2. Use `pubmed_find_related` with `type="similar"` for mechanistic, adjacent, or comparable empirical studies.
3. Use `pubmed_find_related` with `type="reviews"` for review background, narrative framing, or broad coverage.
4. Inspect selected related/review PMIDs before recommending them.
5. Deduplicate by PMID first, then DOI, normalized title, and first-author/year.

### Output Focus

- Separate `Similar articles` from `Reviews`.
- Explain why each related paper expands the evidence base.
- Mark low-relevance or uninspected hits as excluded, not recommended.

---

## 4. OA Full-text Triage

Use when the user asks whether PubMed results have accessible full text.

### Process

1. Run `pubmed_detect_fulltext` for target PMID(s).
2. Report OA/full-text availability and source if returned by the tool.
3. Download only with `pubmed_download_fulltext` when the user explicitly asks for download or confirms it after availability is known.
4. Treat downloaded files as PubMed MCP cache artifacts, not Zotero attachments.

### Output Table

```markdown
| PMID | OA/full-text status | Source/link | Download action | Notes |
|---|---|---|---|---|
| `{pmid}` | `{available/not available/unknown}` | `{source or —}` | `{not downloaded/downloaded/needs confirmation}` | `{notes}` |
```

---

## 5. PubMed Review Package Export

Use when the user asks for saved outputs, EndNote/RIS, or a reusable PubMed literature review. Also use this module automatically after PubMed topic search, selected PMID inspection, or related/review expansion unless the user explicitly says chat-only/no-export.

### Default Deliverables

Write exactly two files unless the user explicitly requests additional outputs:

```text
pubmed-literature-output/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}_pubmed_review.md
pubmed-literature-output/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}_references.ris
```

Do not write package files for explicit chat-only/no-export requests. Do not overwrite existing files or folders unless the user explicitly confirms replacement; append `_v2`, `_v3`, etc. if needed.

### Export Requirements

1. Run the relevant search, PMID inspection, and optional related/review expansion first.
2. Include only selected PMIDs whose metadata was inspected with `pubmed_get_details`, `pubmed_extract_info`, or equivalent visible PubMed metadata tooling.
3. Exclude uninspected hits, failed-query hits, metadata-conflict records, and low-relevance records from RIS by default.
4. Record the PubMed query, tool status, selected PMIDs, excluded PMIDs, PMID Inspection Ledger, Zotero optional cross-check status when available, and metadata warnings in the Markdown report.
5. Generate EndNote-compatible RIS records using inspected metadata only.
6. Only PMIDs with `Inspection status = completed` through `pubmed_get_details`, `pubmed_extract_info`, or equivalent visible PubMed metadata tooling may use `RIS action = include`; search snippets alone are insufficient for recommended citations or RIS export.
7. Zotero cross-check results may mark `already in library` or `consider importing`, but they do not override PubMed metadata inspection requirements and must not trigger Zotero imports without explicit confirmation.

### Final Chat Output

```markdown
Generated PubMed Literature Package:
- Status: `{Ready / Caution / Partial / Unknown}`
- Markdown report: `pubmed-literature-output/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}_pubmed_review.md`
- EndNote RIS: `pubmed-literature-output/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}/{brief_topic_slug}_{YYYY-MM-DD_HHMMSS}_references.ris`

Critical Warnings:
- `{warning or No critical warnings}`
```

---

## Appendix: Output Templates

### PUBMED_REVIEW_REPORT

```markdown
# PubMed Literature Review: {topic}

## 1. Metadata and Use Status

- Input topic: `{original user topic}`
- Generated: `{YYYY-MM-DD HH:MM}`
- Status: `{Ready|Caution|Partial|Unknown}`
- PubMed status: `{Completed|Failed; query reported|Not executed|⚠️ Tool unavailable; search not executed}`
- Query: `{actual or planned PubMed query}`
- Markdown report: `{relative/path}`
- EndNote RIS: `{relative/path}`

## 2. Critical Warnings

| Risk | Affected record/query | Required action |
|---|---|---|
| `{No critical warnings / PubMed unavailable / failed query / uninspected PMID / missing DOI / metadata conflict}` | `{record or query}` | `{action}` |

## 3. Search Reproducibility

| Source | Query | Sort | Max results | Status | Hits reviewed | Selected PMIDs |
|---|---|---|---:|---|---:|---|
| `PubMed` | `{query}` | `{relevance/date}` | `{n}` | `{status}` | `{n}` | `{pmids}` |

## 4. Included Studies

| Priority | Citation | PMID | DOI | Study type | Main finding/use | Caveat |
|---:|---|---|---|---|---|---|
| `{n}` | `{Author et al., year}` | `{PMID}` | `{DOI or —}` | `{type}` | `{use}` | `{caveat}` |

### Zotero Local Library Cross-Check

| PMID | DOI | Title | In Zotero? | Zotero match route | Recommendation |
|---|---|---|---|---|---|
| `{PMID}` | `{DOI or —}` | `{title}` | `{yes/no/not checked/tool unavailable}` | `{PMID / DOI / title / not checked}` | `{already in library / recommend citing / consider importing / no action}` |

## 5. Related and Review Expansion

| Seed PMID | Expansion type | Included PMIDs | Notes |
|---|---|---|---|
| `{PMID}` | `{similar|reviews|not run}` | `{PMIDs}` | `{notes}` |

## 6. Metadata Quality Control

### PMID Inspection Ledger

| PMID | Citation | Inspection status | Inspection tool / route | Inspected fields | DOI | Abstract status | Retraction / metadata warning | Evidence use | RIS action |
|---|---|---|---|---|---|---|---|---|---|
| `{PMID}` | `{Author et al., year}` | `{completed|partial|not inspected|failed}` | `{pubmed_get_details|pubmed_extract_info|equivalent PubMed metadata tool|search snippet only}` | `{title; authors; journal; year; DOI; abstract; publication type}` | `{doi or —}` | `{available|missing|not inspected}` | `{none / retraction concern / metadata conflict / missing required field}` | `{recommended citation|background|excluded|low relevance|metadata only}` | `{include|exclude|verify|optional}` |

Ledger rules:

- Every PMID that is recommended, considered for RIS, excluded for metadata reasons, or reported as an inspected candidate must appear in the PMID Inspection Ledger.
- `Inspection status = completed` requires inspected metadata from `pubmed_get_details`, `pubmed_extract_info`, or equivalent visible PubMed metadata tooling.
- `search snippet only` is not sufficient for recommended citations or RIS export.
- Only PMIDs with `Inspection status = completed` and no unresolved metadata/retraction warning may use `RIS action = include`.
- PMIDs with `Inspection status = not inspected`, `partial`, `failed`, or unresolved metadata conflict must use `RIS action = exclude` or `verify` by default.

| PMID | DOI | Title check | Authors check | Year check | Metadata warning | RIS action |
|---|---|---|---|---|---|---|
| `{PMID}` | `{doi or —}` | `{matched/verify}` | `{matched/verify}` | `{matched/verify}` | `{warning or none}` | `{include/exclude/verify}` |

## 7. Export Files

- Markdown report: `{relative/path}`
- EndNote RIS: `{relative/path}`
- RIS inclusion rule: completed PMID Inspection Ledger rows only; inspected selected PMIDs only.
- Metadata source of truth: PubMed metadata inspected in this run.
```

### RIS_REFERENCE_FILE

Rules:

- RIS records only; no Markdown headings, prose, comments, or code fences.
- Use one `TY  - JOUR` record per journal article unless inspected metadata indicates a different type.
- Include `AU  -`, `TI  -`, `JO  -`, `PY  -`, `DO  -`, `UR  - https://pubmed.ncbi.nlm.nih.gov/{PMID}/`, `N1  - PMID: {PMID}`, and `ER  -` when fields are available.
- Do not include records without inspected PMID metadata.

```ris
TY  - JOUR
AU  - {Family Name}, {Given Names}
TI  - {Title}
JO  - {Journal}
PY  - {Year}
DO  - {DOI}
UR  - https://pubmed.ncbi.nlm.nih.gov/{PMID}/
N1  - PMID: {PMID}
ER  -
```
