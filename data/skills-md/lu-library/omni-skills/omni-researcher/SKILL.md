---
name: omni-researcher
description: Full research workflow orchestrator for OCUL Omni. Use this when the user wants to conduct a complete literature search session — from finding papers to summarizing, evaluating, and saving results. Chains omni-search, omni-detail, omni-summarize, omni-reading-list, and omni-export together into a guided workflow.
---

# Omni Researcher

Orchestrate a complete research session on OCUL Omni by chaining skills in sequence. Guide the user from initial query to a saved reading list and exported citations.

## Workflow Stages

```
[1. Clarify] → [2. Search] → [3. Browse & Filter] → [4. Deep Dive] → [5. Save & Export]
```

---

### Stage 1: Clarify Research Goal

Before searching, ask the user:
- What is the research topic or question?
- What type of resources are most useful? (journal articles, books, theses, all)
- How many results to review? (suggest 10–30 for a literature review)
- Any filters? (year range, specific authors, local collection only)

Keep these preferences for the entire session.

---

### Stage 2: Search — load omni-search

Run omni-search with the user's keywords. Present the results table.

If results look off-topic or too few, suggest:
- Broadening or narrowing the search terms
- Switching scope (local vs. OCUL network)
- Trying related terms

If the user wants more results, load omni-navigate to page through results and collect additional records.

---

### Stage 3: Browse and Filter

Present the full results list and ask the user to:
- Identify items that look relevant (by number)
- Or say "summarize all" to auto-evaluate every item

For each selected item, load **omni-summarize** to generate a quick relevance assessment. Present summaries one by one and let the user mark each as:
- ✅ Keep — add to reading list
- ❌ Skip
- 🔍 Inspect — load omni-detail for full metadata

---

### Stage 4: Deep Dive — load omni-detail

For items marked 🔍, load omni-detail to show:
- Full abstract
- Subjects and keywords
- Publisher / journal
- Full-text access links

Ask the user if they want to open the full text in the browser.

---

### Stage 5: Save and Export

Once the user has finished reviewing:

**Option A — Reading List:**
Load omni-reading-list on all ✅ kept items.
Generate and save a Markdown reading list file.

**Option B — Export Citations:**
Load omni-export on each kept item.
Compile RIS entries and present them as a combined `.ris` file for import into Zotero or Mendeley.

**Option C — Both.**

---

## Session Memory

Track the following across the session in your context:

```
topic: {user's research topic}
search_keywords: {keywords used}
all_results: [{idx, title, authors, recordId, link}]
kept: [{recordId, title, summary}]
skipped: [recordId, ...]
```

---

## Example Session

```
User: "I need papers on climate change adaptation in urban areas"

Researcher: Clarifies scope → searches → presents 10 results →
            summarizes top 5 → user keeps 3, skips 2 →
            runs detail on 1 flagged item →
            generates reading list Markdown + RIS export
```

---

## Rules

- Never jump ahead — confirm with the user at each stage transition
- If Chrome loses the Omni session (gets logged out), pause and ask the user to log back in
- Always inform the user before navigating away from a page they may want to read
- If a search returns 0 results, immediately suggest alternative keywords rather than stopping

