---
name: papers-research
description: Use when the user wants to search academic papers, read research literature, find citations, download arXiv PDFs, or perform any literature-review style task. Self-contained Python toolkit — no MCP server required.
---

# Papers Research

Skill-mode port of [papers-mcp](https://github.com/xwmxcz/papers-mcp).
Orchestrates a bundled Python CLI (`scripts/papers.py`) via Bash to search
papers, fetch metadata/citations, and download + read PDFs.

## One-time setup

Verify dependencies (only once per machine):

```bash
python -c "import httpx, arxiv, fitz" 2>&1 || pip install httpx arxiv PyMuPDF
```

If `python` isn't on PATH, use `py` (Windows) or the full interpreter path.

## Invocation

The script lives at `${CLAUDE_PLUGIN_ROOT}/skills/papers-research/scripts/papers.py`
— this variable is auto-substituted by Claude Code's plugin loader. Always
quote the path (it may contain spaces).

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/papers-research/scripts/papers.py" <subcommand> [args]
```

## Subcommands

| Subcommand | What it does | Example |
|---|---|---|
| `search <query> [--limit N]` | Semantic Scholar search (cap 20) | `search "diffusion models" --limit 5` |
| `detail <paper_id>` | Full metadata, TL;DR, top 10 references | `detail 10.48550/arXiv.2310.06825` |
| `citations <paper_id> [--limit N]` | Papers that cite this one (cap 20) | `citations <id> --limit 15` |
| `arxiv <query> [--max-results N]` | arXiv preprint search (cap 10) | `arxiv "RLHF" --max-results 5` |
| `download <arxiv_id> [--save-dir D]` | Save PDF locally | `download 2310.06825 --save-dir ./pdfs` |
| `read <pdf_path> [--max-pages N]` | Extract PDF text via PyMuPDF | `read ./pdfs/foo.pdf --max-pages 20` |

## Paper ID conventions

`detail` and `citations` auto-detect ID type:
- **DOI** (`10.xxxx/...`) → used as-is
- **arXiv** (`ARXIV:2310.06825`, or bare numeric ≥10 digits → auto-prefixed)
- **Semantic Scholar paperId** (long hex string) → used as-is

`download` requires a plain arXiv ID like `2310.06825` (no prefix).

## Standard workflows

### A — Literature scan
1. Run `search <topic>`.
2. Present results as a ranked table: **# | Title | Year | Citations | ID**.
3. Ask which paper(s) to dig into.

### B — Deep-read one paper
1. `detail <id>` → confirm match, show abstract + TL;DR.
2. If arXiv ID present: `download <arxiv_id> --save-dir ./pdfs`.
3. `read <pdf_path>` (default 10 pages = abstract + intro + conclusion;
   raise to 30+ for full read but warn about context usage).
4. Summarize: **problem · method · key result · limitations**.

### C — Impact analysis
1. `detail` the anchor paper.
2. `citations <id> --limit 20`.
3. Cluster citing papers by year/theme; highlight most-cited follow-ups.

### D — Build a reading list
1. Run Workflow A.
2. For each chosen paper, also run `citations` to find related work.
3. Deduplicate by paperId; annotate each entry with one-line rationale.

## Decision rules

**Which search first?**
- Generic topic, unknown venue → `search` (broader, has citation counts).
- User says "preprint" / "latest" / "arXiv" → `arxiv`.
- Ambiguous → run both, dedupe by title.

**Before downloading a PDF:**
1. Always `detail` first to confirm match.
2. If user request was vague, show abstract and confirm before downloading.
3. Then `download`.

**Reading PDFs:**
- `max_pages=10` default is fine for skim.
- Bump to 30+ only when user wants thorough analysis.
- If extraction returns `PDF无法提取文本（可能是扫描件）`, the PDF is a
  scanned image — offer to find an alternative version on the publisher
  site or use OCR (out of scope for this skill).

## Failure handling

- **HTTP 429** → script auto-retries 3× with exponential backoff. If it
  still fails, wait 10s and retry once before reporting.
- **Empty results** → broaden query (drop quoted phrases, try synonyms)
  before giving up.
- **Unknown paper_id format** → try as DOI first, then `ARXIV:<id>`, then raw.
- **Missing dependency** → script returns `需要安装 X: pip install X`;
  surface this and offer to install.

## Output conventions

- Always include the paper ID alongside titles so the user can re-query.
- Cite format: `[FirstAuthor et al., Year] *Title* (cites: N)`.
- For downloaded PDFs, always report the absolute save path.
- Default `save-dir` is the current working directory; ask if the user
  wants a specific location.
