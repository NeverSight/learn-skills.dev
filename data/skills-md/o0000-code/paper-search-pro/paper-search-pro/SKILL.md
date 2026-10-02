---
name: paper-search-pro
description: "Find academic papers across up to 8 sources (OpenAlex / Semantic Scholar / CrossRef / PubMed / arXiv for English, OpenReview for AI venues, plus native-Chinese retrieval via NSSD 国家哲社文献中心 + yiigle 中华医学期刊) with adjustable depth — Quick scan (5 min) to Audit prep (3 hr). Use when the user wants to find papers, run a literature search, gather references, scope a research topic, search Chinese-language / 中文原生 literature (中文文献/中文核心/CSSCI/C刊/国内研究/国内文献/中华××期刊/心理学报/经济研究), or filter results by journal tier (中科院分区/一区/几区, Q1, JCR/SJR quartile, 影响因子/impact factor, 期刊分区, 顶刊/top journal, '按分区筛'), or export paste-ready professional search strategies / 检索式 for external databases (PubMed / WOS / Scopus / Embase / 知网 CNKI / 万方 / SinoMed — '写检索式', '导出检索式', 'WOS 检索式', '知网专业检索', 'search strategy', 'boolean search strategy'). Triggers on search verbs ('find papers', 'literature search', 'papers about X'), review types ('scoping review', 'systematic review', 'SR prep', 'literature review', 'lit review', 'help me write a lit review'), Chinese ('找文献', '找论文', '论文搜索', '学术检索', '文献检索', '文献综述', '综述前期', '求文献', '中文文献', '中文核心', 'CSSCI', 'C刊', '国内研究', '找中文的'). Outputs Shadcn HTML report + BibTeX/RIS/CSV + PRISMA-S log. Do NOT use for: concept explanations ('what is X' / 'X 是什么', e.g. '影响因子怎么算'), writing ('帮我写' / 'help me write a paragraph'), single-paper interpretation or PDF download with metadata (use paper-downloader-portable), or when the user already has a literature set (use literature-set-review)."
license: Apache-2.0
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Task
metadata:
  author: Bo
  version: 2.5.0
  vendored-from: futurehouse/paper-qa (Apache 2.0)
---

# paper-search-pro

Multi-source literature search with adjustable depth. Four tiers, five data sources orchestrated by you (the main agent). Python helpers handle deterministic work; LLM classification is delegated to parallel Inline SubAgents — no external API key required.

## When to use this skill

- User wants to find academic papers / 找文献 / 论文搜索
- User is preparing a literature review, systematic review (SR), scoping review, or meta-analysis
- User wants to scope research on a topic for a thesis / proposal / coursework / news story
- User asks "what research exists on X" / "find me papers about Y"
- User uploads a query that suggests literature gathering (PICO, SPIDER, MeSH, RCT, etc.)

## When NOT to use

- User wants to **read** a specific paper (use PDF reader / download tool)
- User wants to **summarize** a single known paper (use a summarizer)
- User wants to **download** PDFs given DOIs (use `paper-downloader-portable`)
- User already has a literature set and wants to write a review (use `literature-set-review` / `factor-outcome-review`)
- User wants concept explanation, not papers ("what is prospect theory" → just answer)

---

## 🤖 Called by another agent / headless mode

**If you are an agent driving this Skill for your own reasoning (not for a human
who wants an HTML report)**, do NOT hand-run the 14-STEP recipe below. There is a
single structured-data channel built for you:

```bash
PYTHONPATH=$PSP_HOME python3 -m scripts.agent_search "<query>" > result.json
```

One command runs the whole deterministic core — multi-strategy retrieve → dedup →
heuristic relevance score (computed for every paper) → saturation signal → quota
snapshot → per-paper journal metric — and prints **one JSON envelope** (no HTML,
no PRISMA, no LLM classification SubAgent). The human path below is unaffected.
That command gives you a deterministic **floor**, not the finished job — agent mode
is *not* meant to stop at the machine output; `references/agent_mode.md` is where you
layer your own semantic judgement on top to reach human-recipe quality (the command
guarantees the floor; you supply the quality).

📖 **Read `references/agent_mode.md`** for the full envelope schema, every flag
(`--verify`, `--min-relevance`, `--quartile`, `--min-impact`, …), the relevance
formula, error codes / exit codes, and source selection. This is the SSOT for
agent callers — everything else in this section is just the pointer to it.

Everything from here down is the **human-facing 14-STEP recipe** (HTML report +
exports). Use it when the consumer is a person.

---

## 🔥 Execution discipline (read before running anything)

Four invariants govern every step — ignoring them is the dominant failure mode in real sessions:

- **A — NEVER `cd` into the Skill directory.** `cd $PSP_HOME` rebinds `./` to the Skill asset folder, so `./paper-search-results/...` lands inside the Skill instead of the user's workspace (and a re-install wipes it). Run every helper from the user's PWD: `PYTHONPATH=$PSP_HOME python3 -m scripts.<name> … > "$SEARCH_DIR/..."`. `$PSP_HOME` (STEP 0) is the install dir; `$SEARCH_DIR` (STEP 0) is an absolute path under the user's PWD.
- **B — Dispatch classifier SubAgents in parallel.** STEP 6 puts up to 5 `Task` blocks in one assistant message; serial dispatch inflates Standard tier from ~10 to ~17 min. The worked example lives in STEP 6 — it is not repeated elsewhere.
- **C — Announce every skip.** If you skip a STEP (budget / empty data / user choice), say *what* you skipped, *why*, *what's lost*, and *how to recover* (e.g. "re-run at `--tier deep`"). Skipping is fine; surprising the user is not.
- **D — Read a step's cited reference when that step is non-trivial for this case.** Each STEP names a `references/<file>.md` carrying edge cases not duplicated here. You won't read all of them every run, nor should you — but skipping the reference for a step you are *actually about to run* is where boundary knowledge (dict-vs-list shapes, enrich-not-search, DOI casing) gets lost. Read the one in front of you.

---

## Architecture at a glance

```
You (main agent) drive the workflow per this SKILL.md.
Python helpers do deterministic work — NO LLM inside, NO external API key.

  L1 OpenAlex (primary)  → deep top-100 multi-strategy
  L2 PubMed (medical)    → MeSH enricher (mostly; Audit-tier can search independently)
  L2 arXiv (CS/AI)       → last-year recent layer (+ 4-day sentinel on freshness words)
  L2 OpenReview (AI)     → accepted-venue labels (ICLR / NeurIPS / ICML …)
  L3 Semantic Scholar    → influentialCitationCount + abstract fallback
  L3 CrossRef            → funder / license / clinical-trial-number

  Classification         → Inline SubAgents (parallel, file-IPC, 5 per message)
  Output                 → HTML (Shadcn) + MD + BibTeX/RIS/CSV + PRISMA-S log
```

---

## The 4 tiers — pick first

| Tier | Wall-clock | Papers | When to pick |
|------|------------|--------|--------------|
| Quick | ~5-8 min | 20-60 | "查一下" / "几篇" / "before tomorrow" / fast scope |
| **Standard** (default) | ~10-17 min | 60-180 | Scope a topic / write background / general lit search |
| Deep | ~30-45 min | 180-400 | "thorough" / writing a review article / 综述写作 |
| Audit | ~2-3 hr | 400-1000+ | "systematic review" / "PRISMA" / "Cochrane" / "meta-analysis" |

📖 **BEFORE picking, read `references/tier_decision.md`.** Tell the user your choice and why. For Audit, show limitations warning + get explicit confirmation before starting.

---

## The recipe

For every literature search, follow these steps in order. Each step references a `references/` file for details. Skip files only when the step is obviously trivial for the case at hand — and announce the skip per Rule C.

### STEP 0 — Setup ($PSP_HOME + working directory)

📖 BEFORE THIS STEP, read: `references/setup.md`.

**Resolve the Skill install path into `$PSP_HOME`** (every later step uses `PYTHONPATH=$PSP_HOME`). Prefer explicit injection / agent env var; otherwise scan the known cross-agent install locations. If your harness already exposes this SKILL.md's absolute path, just `export PSP_HOME="<that dir>"` and skip the scan. 📖 Full rationale, why this can't be a script, and the complete path list: `references/runtime_bootstrap.md`.

```bash
PSP_HOME="${PSP_HOME:-${CLAUDE_SKILL_DIR:-${CODEBUDDY_SKILL_DIR:-}}}"   # explicit / agent-injected
if [ -z "$PSP_HOME" ]; then                                            # else scan known installs
  for base in "$HOME/.claude" "$HOME/.codex" "$HOME/.agents" "$HOME/.config/opencode" \
              "$HOME/.codeium/windsurf" "$HOME/.config/goose" "$HOME/.cline" "$HOME/.roo" \
              "$HOME/.copilot" ./.claude ./.codex ./.agents ./.cursor ./.opencode ./.windsurf; do
    [ -f "$base/skills/paper-search-pro/SKILL.md" ] && PSP_HOME="$base/skills/paper-search-pro" && break
  done
fi
[ -z "$PSP_HOME" ] && { echo "ERROR: paper-search-pro install not found. Set PSP_HOME to the dir containing SKILL.md."; exit 1; }
export PSP_HOME; echo "Using Skill install: $PSP_HOME"
```

**Verify config keys** (executed from any cwd, never `cd` into the Skill dir):

```bash
PYTHONPATH=$PSP_HOME python3 -c \
  "from scripts.config import load_config; c = load_config(); print('OK' if c.openalex_api_key and c.ncbi_email else 'MISSING — see references/setup.md')"
```

If "MISSING", point the user to `references/setup.md` (5 keys, all free, ~15 min total) and halt.

**Set up the working directory variable** — every subsequent step uses `$SEARCH_DIR`:

```bash
SEARCH_ID="<topic_slug>_<tier>_$(date +%Y%m%d_%H%M%S)"   # e.g. clt_education_quick_20260522_103045
SEARCH_DIR="$(pwd)/paper-search-results/$SEARCH_ID"
mkdir -p "$SEARCH_DIR/raw" "$SEARCH_DIR/batches" "$SEARCH_DIR/classifications"
echo "Outputs will land in: $SEARCH_DIR"
```

`$SEARCH_DIR` is now an **absolute path under the user's PWD**. Use `"$SEARCH_DIR/..."` (quoted, with the variable) in every helper command below — not `./paper-search-results/...`.

### STEP 1 — Plan the query (MANDATORY for all tiers)

📖 BEFORE THIS STEP, read: `references/query_planner.md`.

**Detect the report UI language** — `UI_LANG` (`zh` for Chinese queries, `en` for everything else) selects which UI language the final HTML report renders in. Paper titles / abstracts / authors / venues are NEVER translated — only the report's UI chrome. Pass `--language $UI_LANG` to STEP 12b.

```bash
UI_LANG=$(PYTHONPATH=$PSP_HOME python3 -m scripts.detect_language "$USER_QUERY")
```

The detector routes Japanese / Korean / European queries to **English** (the bundle ships only EN + ZH dictionaries; English is the international academic default). 📖 The exact Unicode rule and why kana is checked before Han live in `references/runtime_bootstrap.md`.

**Determine the search language space** (`search_language`, axis 2 — *which literature ocean*, distinct from `UI_LANG` above which is only *report chrome*). 📖 The parsing SSOT is `references/source_routing.md` §"Language scope"; resolve the space here, before phrasing the query, because it changes how STEP 3's query is built. This is **additive and opt-in — a pure English query resolves to the `en` space with zero new prompts or behavior (R-19)**; everything below fires only for Chinese queries or explicit signals.

- Read the persisted default `config.search_language` (auto | en | zh | both) and apply the priority ladder **flags > in-query markers > config > auto**. CJK presence is the mechanical fact from `detect_language` above; markers (`CSSCI`, `中文文献`, `SSCI`, `知网`, …) and non-signals (`中科院一区`, topic-about-China) are your semantic judgment per the §"Language scope" tables.
- **`auto` + a Chinese (CJK) query + no language marker + no persisted value → ask ONE question before retrieving** (this is the human path's job; the CLI/agent path passes through instead). Two sentences, offer to persist, and don't re-ask later this session:

  > 你用中文提问——文献要英文、中文,还是都要?顺便可以说"以后都这样",我就记成默认、下次不再问。

  - "中文" / "都要" → enter that space (STEP 2 discipline routing takes over; report one line there).
  - "英文" → v2.2 behavior (Chinese topic planned as an English query), report one line.
  - "无所谓 / 都行" → **this run uses `both`** (Recall > Precision), not persisted; if the same user answers "无所谓" a second time, add one light offer to set `both` as default, then never ask again.
  - Only an explicit "以后都…" persists to `config.search_language` (single answers never auto-persist).
- **If a rank ambiguity (bare "Q1") also fired this run, merge both questions into ONE message** — ask language + platform together, never in two rounds (over-asking is a red line).
- Once the space is known, phrase the query per `references/query_planner.md` §"Cross-language query handling": **`zh` keeps Chinese search terms (no translation)**, `en` uses the English terms (v2.2 behavior), `both` builds two sets.

**Write each retrieval query as concept blocks, not a word list.** OpenAlex requires every bare word, so synonyms written as words exclude every paper that uses only one of them (a user's 11-word query matched one paper by title and abstract over five years). Synonyms go in OR groups, 2–3 blocks joined by AND, phrases in quotes — `("short video" OR TikTok OR Douyin) AND (attention OR concentration)` — and keep the population block out of at least one strategy. 📖 `references/query_planner.md` §"How OpenAlex reads a query".

Apply PICO / SPIDER / PEO depending on domain:
- Medical/clinical → PICO (Population/Intervention/Comparator/Outcome)
- Qualitative → SPIDER
- Scoping → PEO (Population/Exposure/Outcome)
- Open-ended → just extract 2-4 concept blocks + 2-5 synonyms each

**Journal-rank intent recognition (additive — only acts when the query mentions a partition).** Before you extract concept blocks, check whether the user's query carries a journal-rank/partition phrase — "中科院一区", "Q1", "JCR Q1", "SJR Q2", "顶刊 / top journal". If so, that phrase is a **filter condition, not a search term**, and it MUST be **stripped from the topic** before retrieval. This roots out the failure that motivated the whole feature: "中科院一区 情绪调节" used to send "中科院一区" to the search engine as a topic word, so it searched for papers *about* 中科院一区 instead of papers *on* 情绪调节 *filtered to* CAS tier 1. The deterministic parser does both jobs (extract + strip) for you:

```bash
PYTHONPATH=$PSP_HOME python3 -c "
from scripts.rank_intent import parse_rank_intent
i = parse_rank_intent('''<original user query>''')
import json; print(json.dumps({
  'platform': i.platform, 'tiers': i.tiers, 'quartiles': i.quartiles,
  'top': i.top, 'ambiguous': i.ambiguous, 'candidates': i.candidate_platforms,
  'cleaned_query': i.cleaned_query, 'stripped': i.matched}, ensure_ascii=False))
"
```

Then act on the parse:
- **`cleaned_query`** is the rank-stripped retrieval input — use it (NOT the raw query) when building STEP 3 queries and the query plan. It is not automatically `SEARCH_TOPIC` or the report title: the semantic planning step below still removes conversational and operational text. When the query had no rank phrasing, `cleaned_query == query` and retrieval behavior remains unchanged (R-19).
- **`platform` + `tiers`/`quartiles`/`top`** are the filter you will apply right after STEP 5 — remember them (and record them as `rank_filter` in `query_plan.json`); do not filter here.
- **`ambiguous == True`** (a tier or quartile with no platform word, e.g. a bare "Q1" or "SSCI 一区" — the recogniser never guesses a platform): **ask the user one short question inline** before going further, offering the platforms in `candidates` — *"按 JCR 还是 SJR 的 Q1 筛?"* / *"按中科院分区还是 JCR 分区?"*, plus *"顺便要不要设为以后的默认?"* The CLI/headless path cannot ask, so this inline question is specifically the human path's job.
- If the query mentions no partition at all, skip this entirely — STEP 1 proceeds exactly as before.

**Time scope — decide the year window before retrieving.** 📖 `references/query_planner.md` §"Year filter heuristics". Sort the request into one of four cases:

- **Explicit range** ("2020–2024", "近两年", "2023 年以后", "last 3 years", "只要 2026 年的") → set `year_min` / `year_max`; relative ranges count back from the current year ("近两年" = current year − 1 … current year). No question. One line: *"本次限定 2025–2026。"*
- **"New" without a number** ("最新", "最近", "近年", "前沿", "recent", "latest", "cutting-edge") → how recent is genuinely ambiguous and changes the result set. If `config.recent_years` is set, use it and say so in one line. Otherwise **ask one question** — in the same message as any language or rank question from above, never a second round:

  > 「最新」想要多近？近一年 / 近两年 / 近三年 / 近五年，或者直接给区间（如 2023–2026）。说「以后都这样」我就记成默认。

  Only an explicit "以后都…" persists (`recent_years: <N>` in `~/.paper-search-pro/config.yaml`, same mechanism as `search_language`).
- **Classics** ("经典", "奠基", "起源", "seminal", "classic") → no year window; add `seminal` in STEP 3.
- **Nothing said** (most requests) → no year window, and **do not ask**: STEP 3's recent leg still brings the most relevant papers of the last year and of the two years before. One line: *"没说时间范围：本次不限年份，并单独补一层近一年的新文献。只要近几年的，说「只要近两年」即可。"* If a language or rank question is being asked anyway, you may offer the time choices in that same message.
- **Audit tier**: date limits belong to the protocol (PRISMA-S reports them) — confirm the window as part of the Audit confirmation you already ask for.

Where the host has a structured-choice tool (Claude Code's AskUserQuestion; Codex's `request_user_input` when it is listed), ask with these options plus free input; otherwise ask in text. The agent/headless path never asks — it takes `--year-min` / `--year-max` as given.

Even Quick tier needs a lightweight version of this step — never skip silently. Output: 1-3 search strategies (concept blocks + year range + work type filter). Write to `"$SEARCH_DIR/query_plan.json"` as `{"strategies": [{"query": "..."}, ...], "year_min": …, "year_max": …, "rank_filter": {"platform": "cas", "tiers": [1, 2]}, "work_type_filter": …}` (other keys are fine; omit what does not apply). The report's audit tab and the PRISMA-S log (STEP 12a, 13) read the queries and filters from it.

**Define `SEARCH_TOPIC`, but do not freeze the report title yet.** Read `references/report_title.md` §"STEP 1". `SEARCH_TOPIC` is the normalized semantic retrieval scope derived from the concept blocks, not the user's prose with a few regex matches removed. Strip greetings, tool/output instructions, tier/language/date/database constraints, and other operating directions; retain population, exposure/intervention, outcome, mechanism, and setting only when they are scientific concepts. Keep the exact user message separately as `USER_QUERY` for PRISMA-S. The final visual title is authored in STEP 11 after the retained evidence is known.

### STEP 2 — Route supplemental sources within the STEP-1 language space

📖 BEFORE THIS STEP, read: `references/source_routing.md`.

**You make these routing calls by judging the query's domain — the reference's keyword tables are calibration examples, not a match list** (mechanical facts — CJK detection, explicit `--flags` — stay deterministic). Within the language space fixed in STEP 1, route the per-discipline boosters:

- **English space** (`en`, or the English half of `both`) — unchanged from v2.2:
  - Medical signals (RCT, PRISMA, MeSH, clinical, disease names) → enable PubMed
  - CS / AI topics (machine learning, LLM, transformer, NeurIPS, computer vision, …) → enable arXiv's recent layer **and OpenReview** (ICLR / NeurIPS / ICML / COLM / TMLR review platform — adds accepted-venue labels such as "ICLR 2026 Oral" and a few papers only it holds)
  - Freshness signals (preprint, "最新", "this week") → also the 4-day arXiv sentinel
  - Cross-domain (e.g. "AI in radiology") → enable both
  - Pure social science / humanities → OpenAlex only
  - *(Judgment call: a core AI/CS query may also raise the primary engine to Semantic Scholar — see `source_routing.md` §"AI / CS queries → consider Semantic Scholar as primary".)*
- **Chinese space** (`zh`, or the Chinese half of `both`) — route the Chinese boosters the same way, by discipline:
  - Social-science / humanities signal → add **NSSD** (国家哲社文献中心; carries the CSSCI 收录标识 OpenAlex has ≈0 coverage of)
  - Medical signal → add **yiigle** (中华医学期刊全文数据库); PubMed still covers MEDLINE-indexed 中华 journals, so the two are complementary
  - Pure sci-tech with neither → Chinese side runs on OpenAlex only (sci-tech Chinese core journals mostly register DOIs, so OpenAlex covers them well)

**Report one line** (axis-3 style — a statement, not a question; 22 §6.3). For an English-only run this is the PubMed/arXiv notice (*"I detected medical + AI signals — also searching PubMed, arXiv (last year) and OpenReview. Override with `--no-pubmed`."*). For a Chinese space, e.g.:

> 本次按「中英都要」检索;中文侧检测到社科主题,已加 NSSD(国家哲社文献中心)。想去掉说 `--no-nssd`,只查一边说"只要英文/中文"。

**Coverage honesty rides with the notice:** if the zh space has a social-science topic but the user declined NSSD, add that OpenAlex hits ≈0 on CSSCI flagship journals (经济研究 / 管理世界 …), so that layer is missing. User can override any of this with an explicit instruction (a per-query override wins over everything).

**On the `--flag` shorthands above (`--no-nssd`, `--no-pubmed`, `--source …`):** on this human path they are **natural-language override *notation*** — a compact way to write what the user can *say* ("去掉 NSSD" / "只查 OpenAlex"), which you (the LLM) interpret. They are **not executable CLI flags** — no script parses them here. The only real, script-parsed flags live on the agent/headless path (`agent_search`), and there the Chinese-source control is opt-**in**: `--with-nssd` / `--with-yiigle` (there is no `--no-nssd` / `--source` there). See `references/agent_mode.md`.

### STEP 3 — Retrieve from OpenAlex (deep)

📖 BEFORE THIS STEP, read: `references/openalex_helper_cheatsheet.md`.

Always run OpenAlex first. (OpenAlex is the default primary source; `primary_source` in `config.yaml` can change that — see *Primary source selection & quota fallback* in `references/source_routing.md`.)

**When OpenAlex cannot serve a call** (daily budget spent, persistent throttling, outage), `openalex_helper` serves that same call from Semantic Scholar and still prints the same JSON shape — no flag, no config. It says so in one stderr line starting `[paper-search-pro] OpenAlex unavailable`: tell the user in one sentence (Rule C) and carry on; do not stop to ask. If Semantic Scholar cannot serve it either, the call behaves as an OpenAlex error always did: exit status `3` (stdout is still valid JSON), and the stderr line says what happened and when OpenAlex resets — report it to the user as you would any OpenAlex error. `journal-list` is the exception: as before, it comes back empty with exit 0.

For Standard+ tiers, use multi-strategy deep crawl:

```bash
PYTHONPATH=$PSP_HOME \
  python3 -m scripts.openalex_helper double-sort "<query>" \
    --n 50 \
    > "$SEARCH_DIR/raw/openalex.json"
```

Three legs, one file: **cited** (the topic's most-cited work), **recent** (the most relevant work of the last 12 months, then of the two years before), **relevance** (the best matches overall). The recent leg is what finds this year's papers — relevance ranking leans on citations, so without it new work barely appears.

For Quick tier, relevance plus a smaller recent layer:

```bash
PYTHONPATH=$PSP_HOME \
  python3 -m scripts.openalex_helper search "<query>" \
    --limit 30 --recent 20 \
    > "$SEARCH_DIR/raw/openalex.json"
```

Then record how many works OpenAlex holds for the main query — one line under the report's year chart, so a thin recent bar is not read as a thin field (it counts title-and-abstract matches in the STEP 1 window, or the last two years when there is none):

```bash
PYTHONPATH=$PSP_HOME \
  python3 -m scripts.openalex_helper count "<query>" [--year-min YYYY] [--year-max YYYY] \
    > "$SEARCH_DIR/pool_count.json"
```

If `count` reports fewer than 30 works, or a helper warns about a long run of bare words, the query is too narrow (unless the topic is genuinely niche): regroup it as in STEP 1 and rerun retrieval before classifying.

Add the STEP 1 window to the retrieval commands too: `--year-min YYYY` / `--year-max YYYY` (inclusive). No window given → none is added (the helpers cap at the current year themselves). The recent leg stays inside the window: for a window ending in the past, it takes that window's last year.

**`raw/` holds retrieval output only — one file per search, as the helpers wrote it.** STEP 7 estimates coverage from how often these separate searches found the same papers. A subset, merge or screened copy you derive goes in `"$SEARCH_DIR/_working/"`, not `raw/`: in `raw/` it would look like another search that re-found everything.

The full subcommand + flag reference (`search` / `double-sort` / `seminal` / `reviews` / `journal-list` / `citation-network`, all verified against argparse) is in `references/openalex_helper_cheatsheet.md` — read it before reaching for anything beyond the two commands above. For Deep+Audit, also call topic-specific subcommands (e.g. `seminal`, `reviews`, `journal-list`), append outputs to `$SEARCH_DIR/raw/openalex_*.json`, and federate them all together in STEP 5.

### STEP 4 — Run L2 boosters (if enabled by STEP 2)

📖 BEFORE THIS STEP, read: `references/pubmed_helper_cheatsheet.md` and `references/arxiv_helper_cheatsheet.md`.

**PubMed — default mode is `enrich`, NOT `search`**:

- **Standard / Deep tier**: enrich OA-found papers with MeSH terms (mutates the openalex.json file in place):
  ```bash
  PYTHONPATH=$PSP_HOME \
    python3 -m scripts.pubmed_helper enrich \
      --input-file "$SEARCH_DIR/raw/openalex.json" \
      --output-file "$SEARCH_DIR/raw/openalex.json"
  ```
- **Audit tier with explicit MeSH query**: independent MeSH search (produces a new file to federate later):
  ```bash
  PYTHONPATH=$PSP_HOME \
    python3 -m scripts.pubmed_helper search-mesh "Diabetes Mellitus, Type 2" \
      --year-min 2020 --limit 30 --pub-type "Randomized Controlled Trial" \
      > "$SEARCH_DIR/raw/pubmed.json"
  ```
- Generic `pubmed_helper search` is a fallback when no MeSH term is known — prefer `enrich` or `search-mesh` whenever possible.

**arXiv — CS / AI topics: the recent layer.** The most relevant preprints of the last year (OpenAlex indexes arXiv late and incompletely: in one check, 7 of 20 recent on-topic papers from OpenReview were not in OpenAlex):

```bash
PYTHONPATH=$PSP_HOME \
  python3 -m scripts.arxiv_helper search "<query>" \
    --sort relevance --since-days 365 --limit 30 \
    > "$SEARCH_DIR/raw/arxiv.json"
```

**Freshness signals ("最新", preprint, "this week") — also the 4-day sentinel**, for preprints too new for any index:

```bash
PYTHONPATH=$PSP_HOME \
  python3 -m scripts.arxiv_helper freshness "<query>" \
    --days 4 --limit 30 \
    > "$SEARCH_DIR/raw/arxiv_fresh.json"
```

Plain words in the query are all required (arXiv would OR them). Both commands print `[]` and a stderr note when arXiv fails or times out — carry on without it (Rule C: say so in one line).

Subcommand reference:
- `arxiv_helper freshness <query> --days N --limit M [--all-cats]`
- `arxiv_helper search <query> --limit M --sort submitted|relevance|lastUpdated [--since-days N] [--all-cats]`
- `arxiv_helper get <arxiv_id>`

**OpenReview — CS / AI topics only.** 📖 `references/openreview_helper_cheatsheet.md`. The review platform of ICLR, NeurIPS, ICML, COLM and TMLR. The helper returns only accepted papers, labelled like "ICLR 2026 Oral" — the label OpenAlex and Semantic Scholar lack (they list these as arXiv preprints). STEP 5 merges each into the same paper's arXiv/OpenAlex record.

```bash
PYTHONPATH=$PSP_HOME \
  python3 -m scripts.openreview_helper --search "<query>" --n 30 \
    [--year-min YYYY] [--year-max YYYY] \
    --output-file "$SEARCH_DIR/raw/openreview.json"
```

Only its search endpoint is open to anonymous use; if OpenReview blocks it, the helper returns `[]` — say so in one line and carry on.

**NSSD / yiigle — Chinese boosters (ONLY when STEP 1-2 put this run in the `zh` space, and only the one(s) the discipline routing selected):**

Each is an independent primary source for the Chinese space (same role as `ss_helper --search`) and emits the **same `UnifiedPaperEntity` shape** as openalex.json, so STEP 5 federates them identically. Keep the query in **Chinese** (do NOT translate — query_planner §Cross-language) and write to `raw/nssd.json` / `raw/yiigle.json`:

```bash
# NSSD — Chinese social-sciences & humanities (adds the CSSCI-tier layer OpenAlex lacks)
PYTHONPATH=$PSP_HOME \
  python3 -m scripts.nssd_helper --search "<中文检索式>" \
    --n 50 [--year-min YYYY] \
    > "$SEARCH_DIR/raw/nssd.json"

# yiigle — Chinese medical (中华医学期刊全文数据库; native-Chinese titles + abstracts)
PYTHONPATH=$PSP_HOME \
  python3 -m scripts.yiigle_helper --search "<中文检索式>" \
    --n 50 [--year-min YYYY] \
    > "$SEARCH_DIR/raw/yiigle.json"
```

Both degrade gracefully to `[]` on any network / HTTP failure (they never raise) — an empty file just federates to nothing. Both take **only** 题录 + 摘要 (compliance: no full-text download, no caching) and print their source attribution to stderr. `--year-min` filters client-side; drop it to keep all years.

**config `search_language: en` but a Chinese query arrived (hard boundary 2):** do NOT enable Chinese boosters, but say one line — never a silent translation (22 §6.4):

> 按你的默认(只查英文),我把中文主题规划成英文检索式了。想要中文文献这次说一声即可,想改默认说"以后…"。

**User names 知网 / CNKI / 万方 / 维普 (marker hit + compliance):** these are closed subscription databases PSP does not scrape. Say one line, offer the substitute + the export, don't re-argue (22 §6.5):

> PSP 不抓知网/万方（合规，不做封闭库抓取）；中文侧用 OpenAlex 中文底座 + NSSD(社科,含 CSSCI 标识)/yiigle(医学)覆盖。但可以**把你的知网专业检索式写好**——按 CNKI 专业检索语法（`SU %=` 相关匹配、块内 OR/块间 AND、全英文半角、检索值单引号）生成可直接**粘贴进「专业检索」框**的检索式，粘贴即查。中文医学题另可给 SinoMed（CMeSH 受控词双轨）。要导出吗？

"要导出吗?" accepted = an explicit-ask trigger for STEP 11.5 — run the export at any tier.

### STEP 5 — Federate (dedup + merge)

📖 BEFORE THIS STEP, read: `references/source_routing.md` §"Field priority table".

Combine all retrieval results into a single deduped KG. **Default output is a dict keyed by canonical_key** — that's what `rcs_parser` expects later, so do NOT pass `--as-list`:

```bash
PYTHONPATH=$PSP_HOME \
  python3 -m scripts.federated_kg_resolver \
    --input-files "$SEARCH_DIR/raw/openalex.json" \
                  "$SEARCH_DIR/raw/pubmed.json" \
                  "$SEARCH_DIR/raw/arxiv.json" \
                  "$SEARCH_DIR/raw/openreview.json" \
    --output "$SEARCH_DIR/kg.json"
```

Pass only the input files you actually produced — skip ones that were not enabled by STEP 2 (and add `raw/arxiv_fresh.json` when the 4-day sentinel ran). OpenReview records carry no DOI; the resolver folds each into the same paper's arXiv/OpenAlex record by title and gives it the accepted venue label. **If STEP 4 ran the Chinese boosters, add `"$SEARCH_DIR/raw/nssd.json"` / `"$SEARCH_DIR/raw/yiigle.json"` to the same `--input-files` list** — they carry the identical entity shape and federate exactly like the others (CJK-safe dedup is handled by the Phase 0 canonical-key fix, so distinct Chinese titles don't collapse). For an English-only run those files don't exist, so the call is byte-identical to v2.2 (R-19). This handles DOI normalization (arXiv X→x case), version stripping, E5b guard (same title+year but different DOIs are kept separate), and field-priority merge.

`--as-list` exists but is only for consumers that want a sorted list (by citation_count); do not use it in this pipeline.

**Only when STEP 1 found a journal-tier request — filter before classifying.** A tier is a cheap deterministic filter; classifying papers it will drop is the expensive part. 📖 `references/journal_metrics.md`. Keep `kg.json` as the full pool and classify `kg_ranked.json`:

```bash
PYTHONPATH=$PSP_HOME \
  python3 -m scripts.rank_filter --kg "$SEARCH_DIR/kg.json" \
    --output "$SEARCH_DIR/kg_ranked.json" --platform cas --tiers 1,2
# JCR / SJR: --platform jcr --quartiles Q1,Q2 ; Top only: --top
```

It labels every paper with all three platforms, keeps the requested ones, and writes the rest to `kg_ranked_set_aside.json`. Tell the user the printed counts in one line (*"本次按中科院 1–2 区筛：留 N / 区外 M / 不在该表 K"*) with the attribution it prints. In STEP 6 batch and merge `kg_ranked.json` instead of `kg.json`. No tier requested → skip this entirely; nothing changes.

### STEP 6 — Classify in parallel batches (LLM happens here — main agent + SubAgents)

📖 BEFORE THIS STEP, read: `references/classifier_subagent_prompt.md` and `references/rcs_rubric.md`.

Split the KG into batches of 10 papers each. Write to `"$SEARCH_DIR/batches/batch_NNN.jsonl"`. If the pool is larger than the tier can classify, trim evenly across the raw files and never by citation count: new papers have almost none, so a citation cut removes exactly the recent layer.

**Before dispatch**, expand `$PSP_HOME/references/rcs_rubric.md` into the actual absolute path (e.g. `/Users/alice/.claude/skills/paper-search-pro/references/rcs_rubric.md`) and substitute it for `{rubric_path}` in the classifier prompt template. Each SubAgent runs in its own shell where `$PSP_HOME` is **not** exported — passing the literal `$PSP_HOME` token would leave the SubAgent unable to find the rubric, which silently degrades scoring quality. See `references/classifier_subagent_prompt.md` for the full placeholder table.

🔥 **PARALLELISM IS MANDATORY** (Rule B):

You MUST dispatch up to **5 classifier SubAgents in a single assistant message** using multiple `Task` tool_use blocks. Serial dispatch (one Task per message, waiting for each result) is the single biggest performance failure observed — it inflates Standard tier from ~10 min to ~17 min.

✅ **CORRECT — in ONE assistant message:**

```
Task tool_use #1  → subagent_type="general-purpose", prompt="<classifier prompt for batch_001.jsonl>"
Task tool_use #2  → subagent_type="general-purpose", prompt="<classifier prompt for batch_002.jsonl>"
Task tool_use #3  → subagent_type="general-purpose", prompt="<classifier prompt for batch_003.jsonl>"
Task tool_use #4  → subagent_type="general-purpose", prompt="<classifier prompt for batch_004.jsonl>"
Task tool_use #5  → subagent_type="general-purpose", prompt="<classifier prompt for batch_005.jsonl>"
```

All five tool_use blocks live in the same `<assistant>` message, so they run in parallel. Some harnesses hand the five results back together; others start the SubAgents in the background and report each one as it finishes. Either way, merge only once every `batch_NNN_result.json` of the round exists.

❌ **WRONG — five separate messages (this is what serial dispatch looks like):**

```
Message N:    Task tool_use #1 ─→ wait for result
Message N+1:  Task tool_use #2 ─→ wait for result   ← SERIAL, makes Standard run 70% slower
Message N+2:  Task tool_use #3 ─→ wait for result
...
```

If you have more than 5 batches, send 5-at-a-time across multiple messages — each message still contains 5 parallel Task blocks.

Each SubAgent reads its batch file, applies the RCS rubric, and writes `"$SEARCH_DIR/classifications/batch_NNN_result.json"`. Then merge classifications into the KG:

```bash
PYTHONPATH=$PSP_HOME \
  python3 -m scripts.rcs_parser \
    --input-dir "$SEARCH_DIR/classifications/" \
    --kg "$SEARCH_DIR/kg.json" \
    --output "$SEARCH_DIR/kg_classified.json"
```

### STEP 7 — Compute saturation curve (MANDATORY for all tiers)

📖 BEFORE THIS STEP, read: `references/stop_decision.md`.

This step is NOT optional, even for Quick: `curve.json` is what STEP 8 decides on, and STEP 12 renders the same estimate.

```bash
PYTHONPATH=$PSP_HOME \
  python3 -m scripts.discovery_curve \
    --kg "$SEARCH_DIR/kg_classified.json" \
    --output "$SEARCH_DIR/curve.json"
```

`curve.json` gives `coverage_estimate` (0-1) with `ci_lower` / `ci_upper`, and `method`: `sample_coverage` means it was estimated from how often this run's separate searches in `raw/` re-found the same highly relevant papers (`relevance_band` 7 = rcs ≥ 7; 6 = rcs ≥ 6, used when the rcs ≥ 7 papers are too few for the estimator to say anything); `prior` means there was nothing to measure — fewer than two searches, no relevant paper found, or too few in either band — so it is the Undermind median prior capped at 50%, not a measurement — say so if you quote it. `--raw-dir` overrides where the searches are read from (default: `raw/` next to `--kg`).

### STEP 8 — Decide next action (MANDATORY)

📖 BEFORE THIS STEP, read: `references/stop_decision.md`.

This step is NOT optional. Make the decision **explicitly** — based on curve.json + tier budget + intent — and state the reasoning to the user. Do not skip based on intuition.

Decision tree (on `coverage_estimate`):
- coverage < 0.6 AND budget remaining AND tier in {standard, deep, audit} → expand citations (STEP 9)
- coverage > 0.85 OR budget exhausted → stop, write report (STEP 10+)
- ambiguous → tell user the numbers and ask

### STEP 9 — Expand citations (if applicable)

📖 BEFORE THIS STEP, read: `references/citation_chasing.md`.

For top-rcs papers (rcs >= 7), get the citation network. Pass the seed's DOI when it has one: a DOI also works on the Semantic Scholar fallback, while a bare W-ID cannot be resolved outside OpenAlex.

```bash
PYTHONPATH=$PSP_HOME \
  python3 -m scripts.openalex_helper citation-network <doi_or_openalex_id> \
    --refs-limit 25 --cited-by-limit 25 \
    > "$SEARCH_DIR/raw/citations_01.json"      # one file per seed: citations_02.json, ...
```

Then loop back to STEP 5: add the `raw/citations_*.json` files to `--input-files` (the resolver reads their `references` / `cited_by` lists), re-classify only the new entries in STEP 6, and re-run STEP 7.

### STEP 10 — Enrich top-N papers (L3, optional but recommended)

📖 BEFORE THIS STEP, read: `references/ss_helper_cheatsheet.md` and `references/crossref_helper_cheatsheet.md`.

For papers with rcs >= 6, enrich with Semantic Scholar (influentialCitationCount + abstract fallback + tldr). Both helpers read the classified KG and write the new fields back into it, leaving every other field as it was; `--min-rcs 6` limits them to the top papers. Run this before STEP 11, so the summary can rank by `influential_citation_count`.

For Quick tier, skipping STEP 10 is acceptable — but **announce the skip** per Rule C ("Skipped L3 enrichment → no influentialCitationCount; re-run at `--tier standard` to include this").

```bash
# Semantic Scholar — adds influentialCitationCount + abstract fallback + tldr
PYTHONPATH=$PSP_HOME \
  python3 -m scripts.ss_helper \
    --input-file "$SEARCH_DIR/kg_classified.json" \
    --mode enrich --min-rcs 6 \
    --output-file "$SEARCH_DIR/kg_classified.json"
```

It prints one stderr line saying how many papers were enriched and, if Semantic Scholar refused (rejected key, rate limit), why. Relay that line when the count is short; the run continues either way.

**CrossRef (funder / license / clinical-trial number) only when those matter** — a clinical or funding question, or the user asks: the report does not display these fields.

```bash
PYTHONPATH=$PSP_HOME \
  python3 -m scripts.crossref_helper \
    --input-file "$SEARCH_DIR/kg_classified.json" \
    --mode all --min-rcs 6 \
    --output-file "$SEARCH_DIR/kg_classified.json"
```

**Optional (additive) — journal partitions (中科院 / JCR / SJR).**
The multi-platform partition layer labels every paper with **all three** platforms. It is **opt-in and off by default — skip it and the report is byte-for-byte unchanged** (R-19). 📖 Read `references/journal_metrics.md` first (it is the SSOT for sources, the ISSN join, attribution, and R-04 naming).

- **First use needs a one-time fetch** (init-once; data is pulled at runtime into
  `~/.paper-search-pro/ranks/` and **never bundled in the repo**). If you have not
  fetched before, run it once (and tell the user it is a one-time step):
  ```bash
  PYTHONPATH=$PSP_HOME python3 -m scripts.journal_rank fetch          # all three
  # or a single platform: ... journal_rank fetch --platform cas
  PYTHONPATH=$PSP_HOME python3 -m scripts.journal_rank info           # what's cached
  ```
- **A tier was requested** → the papers were already labelled and filtered right after STEP 5; nothing to do here.
- **No tier requested, the user wants to see partitions** → label only (no filter):
  ```bash
  PYTHONPATH=$PSP_HOME python3 -m scripts.rank_filter \
    --kg "$SEARCH_DIR/kg_classified.json" --output "$SEARCH_DIR/kg_classified.json"
  ```
  With nothing cached it prints a one-line hint and changes nothing; tell the user they can `journal_rank fetch` to enable partitions.
- **R-04 naming** is enforced for you in the serialised dict: only JCR exposes an
  `impact_factor` (the real IF); 中科院"区" and SJR quartile are **分区/quartile**.

### STEP 11 — Write the executive summary

📖 BEFORE THIS STEP, read: `references/summary_writer.md`.

📖 Also read: `references/report_title.md`, then author `DISPLAY_TITLE` alongside the summary. This is a **scholarly, evidence-bounded report title**, finalized from the retained corpus — never a copy of `USER_QUERY`, `SEARCH_TOPIC`, or the filter list. It carries the report's central narrative and visual identity. Language, date, database, journal-tier, export, and workflow requirements stay in Methods / PRISMA-S unless they are themselves scientifically meaningful. If the evidence cannot support a specific title, use the localized safe fallback (`文献检索报告` / `Literature Search Report`) rather than putting the raw request in the H1. Run the reference's pre-render acceptance check before STEP 12.

Write a ~300-word executive summary in your own words based on the classified papers:
- The field's main consensus
- Key methods / theoretical frameworks
- Notable disagreements or open questions
- Top 3-5 most influential papers (by `influential_citation_count` when available)
- *(Optional)* journal tier of the leading papers, **if** you attached SJR metrics in STEP 10 — phrase as "SJR分区 / 期刊影响力", never "影响因子 / JCR" (R-04). Skip this bullet entirely when no metrics were attached.

Save to `"$SEARCH_DIR/summary.md"`.

**Partition default / ask / filter / report / switch flow (additive — only when partitions are in play).** When journal partitions are in play (filtered after STEP 5, or labelled in STEP 10), follow this flow; it is entirely opt-in and changes nothing on the default no-partition path (R-19):

- **Factory default standard = JCR.** The persistent default lives in config `rank.default_platform` (out of the box: `jcr`; the user can set it to `cas`/`sjr`). The default platform only **labels** every paper — it does **not** filter unless the user actually asked for a tier.
- **No partition mentioned → do not filter.** Just show all three platforms' labels per paper (STEP 10 annotate already did this) and let the user read / refine. Never invent a tier filter the user didn't ask for.
- **A tier was requested (from STEP 1 intent or the user this round) → filter once, before classification** (right after STEP 5, with `rank_filter`). Use the STEP 1 parse: `platform` + `tiers`/`quartiles`/`top`. A per-request tier filter is **transient — never auto-persist it** to config. The persistent default is only ever changed when the user explicitly says "以后都用 X".
- **Ambiguous bare "Q1" with no platform and no persistent default → ask one short question** (you should already have asked in STEP 1; if not, ask now): *"按 JCR 还是 SJR?顺带设默认吗?"* Small confirmations are welcome, but do not over-ask.
- **Always report what this run did.** After filtering, tell the user in one line: *"本次按 {platform} 筛(留 N / 滤 M",* plus a light offer: *"可换中科院/JCR/SJR 或换档位、可设为以后的默认。"* Include the per-platform attribution (`journal_rank.ATTRIBUTION[platform]`).
- **Switching standard or tier = RE-FILTER the pool, NOT a re-search.** When the user then says "换成中科院二区" or "看看 SJR Q1", do **not** re-run the search: re-run `rank_filter` on the full pool `kg.json` with the new platform / tiers (seconds). Papers it newly admits have no score yet — classify only those (STEP 6), then re-run `rcs_parser` over all `classifications/` with `--kg kg_ranked.json`. **Only when the re-filter leaves too few survivors** do you go back to STEP 3 and deepen the search. This "切换=重筛不重搜" rule is what makes partition exploration cheap.
- **Persisting the default** (only on an explicit "以后都用 X"): set `rank.default_platform` in `~/.paper-search-pro/config.yaml`. Tier档位 is never persisted — only the platform default is.
- **R-04 naming in the summary bullet too:** 中科院"区" and SJR quartile are **分区 / quartile**; only JCR IF(2024) is an **影响因子 / Impact Factor**. The OpenAlex 2yr-mean-citedness figure is "期刊影响力" (open), never a JIF.

### STEP 11.5 — Export search strategies (opt-in — never on the default path)

**Trigger matrix — decide silently, before anything else:**

| Run | Export behavior |
|------|-----------------|
| Quick | **Does not run. Do not mention it, do not ask** — go straight to STEP 12. This silent skip is the one exception to Rule C: announcing it would itself disturb the untouched default path (R-19). |
| Standard | **Does not run during the search** — no question, go straight to STEP 12. **At STEP 14, offer it in one sentence only when this run has a gap the export fills:** the search space included Chinese (`zh` / `both`: 知网 / 万方 hold much of what PSP cannot reach), or `coverage_estimate` < 0.6 (other databases can fill in). No such gap → say nothing. Skip the offer if STEP 4 already made it this run. Accepted → run this step, then re-run 12a–12c so the report gains the export tab. |
| Deep | Offer once, one light sentence: *"要不要顺带导出各平台可粘贴的专业检索式?"* Accepted → run; declined or unanswered → skip without further mention. |
| Audit | **Runs by default** — it is the deliverable behind the Audit disclaimer's promise (Example 4). |
| Explicit ask, any tier | "给我 WOS 检索式" / "我要去知网查" / "导出检索式" / STEP 4's 知网 offer accepted → run immediately, whatever the tier. |

📖 BEFORE THIS STEP (when it triggers), read: `references/search_export/methodology.md` — the rulebook for every semantic judgment below. Add `references/search_export/chinese_methodology.md` whenever the zh/both space exports CNKI / 万方 / SinoMed (Chinese strategies are NOT word-for-word translations of Western boolean).

**Layer 1 — semantics. This is YOUR work (main agent); the script only assembles syntax:**

1. **Rebuild concept blocks** from `"$SEARCH_DIR/query_plan.json"` under methodology.md's block discipline — within-block OR = synonyms of ONE concept only; blocks joined by AND; default 2 blocks (P+I), C/O only when core and consistently reported in titles/abstracts; NOT banned. Do not copy query_plan blocks as-is: this rebuild is where mixed-concept blocks get fixed.
2. **Expand synonyms & entry terms** per block — spelling variants (tumour/tumor), abbreviation + full form (MBSR + "mindfulness-based stress reduction"), related terms. **On a zh / both run, also fill each block's `free_text_zh` with the Chinese synonyms** (简繁 / 别名 / 全称–缩略 variants — Chinese has no truncation, so enumerate explicitly): the CJK hosts (CNKI / 万方 / SinoMed) read **only** `free_text_zh`, and a block without it makes every Chinese strategy be honestly withheld — English words are never rendered into a Chinese database.
3. **Controlled-vocab candidates per platform** — judge MeSH / Emtree / CINAHL / APA / CMeSH independently per library; never symbol-translate one thesaurus into another. Prefer the MeSH already backfilled into the KG by STEP 4 (real descriptors from real hits).
4. **Trim the platform set by discipline** from the Audit full set (PubMed, WOS, Scopus, Embase, Cochrane CENTRAL, PsycINFO, CINAHL, ERIC, IEEE Xplore, ACM DL, EconLit, CNKI, 万方, SinoMed, ClinicalTrials.gov) — a medical topic doesn't need IEEE/ACM; a social-science topic doesn't need Cochrane/SinoMed. **zh / both runs always include CNKI + 万方 + SinoMed.**
5. **Register follows the tier** (audit = recall-leaning, controlled + free-text double-track). Need a study-design filter (e.g. RCT)? 📖 `references/search_export/filters_library.md` — use a canned validated filter verbatim; never write your own, and never add one on CENTRAL.
6. **PRESS six-domain self-review** of 1–5 before any syntax exists. 📖 `references/search_export/press_checklist.md`.

Write the outcome to `"$SEARCH_DIR/concept_model.json"` in the generator's wrapper shape: `{topic, framework, register, language_space, search_id, platforms, concept_model: {blocks (free_text + free_text_zh on zh/both + controlled_vocab_candidates), operator_logic, omitted_blocks + reasons, register_notes}}`. **Write `omitted_blocks.reason` and `register_notes` in the USER'S language** — they surface verbatim in the user-facing `search_strategies.md` (a Chinese-speaking user gets Chinese notes, not English pass-through).

**Layers 2+3 — mechanical assembly + verification (the script's job; never hand-assemble per-host syntax):**

```bash
PYTHONPATH=$PSP_HOME \
  python3 -m scripts.search_export.generate \
    --concept-model "$SEARCH_DIR/concept_model.json" \
    --out "$SEARCH_DIR"
```

Optional flags (verified against argparse): `--platforms pubmed,wos,cnki` (csv) overrides the wrapper's `platforms`; `--topic` / `--framework` / `--register` / `--language-space` / `--search-id` override the wrapper's run-level fields; `--no-verify-vocab` skips the MeSH/ERIC free-API check (terms stamped unverified); `--live-verify-links` live-GETs each A-tier link for a fresh `verified_http`/date.

Emits `search_strategies.md` (paste-ready, per platform) + `search_strategies.json`. Under the hood it reads the per-host syntax cards (`references/search_export/syntax_cards/<host>.md`) and the proximity conversion table (n-values are never hand-computed — not by you either), builds clickable deep links only for the free A-tier platforms (PubMed / ERIC / ClinicalTrials.gov; no link ever circumvents a login or captcha wall), API-verifies MeSH/ERIC terms, leaves Emtree/CINAHL/APA/CMeSH flagged 待人工核对, and lints every strategy — **a linter-rejected string is withheld, never emitted**. Downstream pickup: STEP 12a auto-discovers `search_strategies.json` beside `report_data.json` and folds it in (no extra flag); for STEP 13, append `--search-strategies "$SEARCH_DIR/search_strategies.json"` to the `prisma_s_logger` command so PRISMA-S items 8/1/9/10 are enriched from it.

**Check before handing over** (the honesty gate): the `.json` carries every platform's three-state verification label (🟩机械已验 / 🟨语法已验·词表待核 / 🟦结构参考) and review points — verify they are correct; the user-facing `.md` renders these as plain-language "使用前请核对" notes per platform (no internal jargon) — verify each note is clear and actionable; subscription-wall platforms are honestly marked "需机构登录，未在墙内实测"; CNKI / 万方 / SinoMed are delivered as paste-into-检索框 strategies, not URLs. Keep the quality claim at "专业初稿 + 标注复核点" — never "可署名直用 / 馆员级".

### STEP 12 — Render the report

📖 BEFORE THIS STEP, read: `references/output_files.md`.

```bash
# 12a. Materialize data for the renderer (also writes sibling chart_data / paper_list / metadata / prisma_log)
PYTHONPATH=$PSP_HOME \
  python3 -m scripts.data_materialization \
    --kg "$SEARCH_DIR/kg_classified.json" \
    --summary "$SEARCH_DIR/summary.md" \
    --query "<original query>" \
    --search-topic "$SEARCH_TOPIC" \
    --display-title "$DISPLAY_TITLE" \
    --language "$UI_LANG" \
    --tier "<quick|standard|deep|audit>" \
    --search-id "$SEARCH_ID" \
    --snapshots "$SEARCH_DIR/curve.json" \
    --output "$SEARCH_DIR/report_data.json"

# 12b. Render HTML (Shadcn webartifacts — only renderer; no size cap)
#      --language $UI_LANG selects EN vs ZH UI; the bundle ships with both
#      dictionaries inlined, $UI_LANG just picks which one mounts. Resolution
#      order inside the renderer is: explicit --language > metadata.language > en.
PYTHONPATH=$PSP_HOME \
  python3 -m scripts.html_renderer_webartifacts \
    --data "$SEARCH_DIR/report_data.json" \
    --output "$SEARCH_DIR/report.html" \
    --query "<original query>" \
    --search-topic "$SEARCH_TOPIC" \
    --display-title "$DISPLAY_TITLE" \
    --language "$UI_LANG"
#     add --rank-platform cas|jcr|sjr when this run filtered on a platform,
#     so the badges and zone filter show that platform (default: JCR)

# 12c. MD report (uses materialized-dir for speed)
PYTHONPATH=$PSP_HOME \
  python3 -m scripts.md_report \
    --materialized-dir "$SEARCH_DIR" \
    --summary "$SEARCH_DIR/summary.md" \
    --query "<original query>" \
    --search-topic "$SEARCH_TOPIC" \
    --display-title "$DISPLAY_TITLE" \
    --language "$UI_LANG" \
    --tier "<quick|standard|deep|audit>" \
    --output "$SEARCH_DIR/report.md"

# 12d. Exports (BibTeX / RIS / CSV / papers.json — only rcs >= 5 by default)
PYTHONPATH=$PSP_HOME \
  python3 -m scripts.generate_exports \
    --kg "$SEARCH_DIR/kg_classified.json" \
    --output-dir "$SEARCH_DIR/" \
    --min-rcs 5
```

If 12a–12c print `No scholarly display title was given`, `DISPLAY_TITLE` was empty: the report H1 is the generic fallback. Write the title (STEP 11, `references/report_title.md`) and re-run 12a–12c; nothing needs re-searching.

`data_materialization` accepts `--wall-clock-seconds` if you tracked elapsed time yourself; otherwise the helper computes it from session timestamps when available.

### STEP 13 — Write PRISMA-S log

📖 BEFORE THIS STEP, read: `references/prisma_s_checklist.md`.

```bash
PYTHONPATH=$PSP_HOME \
  python3 -m scripts.prisma_s_logger \
    --search-id "$SEARCH_ID" \
    --kg "$SEARCH_DIR/kg_classified.json" \
    --user-query "<original query>" \
    --tier "<quick|standard|deep|audit>" \
    --query-plan "$SEARCH_DIR/query_plan.json" \
    --snapshots "$SEARCH_DIR/curve.json" \
    --output "$SEARCH_DIR/execution_log.json"
```

This captures the 16 PRISMA-S items for transparency / audit.

### STEP 14 — Open the report + report to user

**First**, auto-open the HTML report in the user's default browser (do NOT wait for the user to ask). Platform-aware Bash:

```bash
# macOS — most common dev setup
open "$SEARCH_DIR/report.html"
# Linux fallback — xdg-open "$SEARCH_DIR/report.html"
# Windows fallback — start "" "$SEARCH_DIR/report.html"
```

Use `open` on macOS by default. If it fails (rare — only bare Linux containers), fall through to `xdg-open` then `start`. **Do NOT skip this step** — the user just waited 5-30 minutes for the report; they should see it the moment it's ready.

**Then** tell the user:
- "Opened report in your default browser." (1 line confirmation)
- Where the report is on disk (absolute path: `$SEARCH_DIR/report.html`) — so the user can find it later
- Top findings (3-5 sentences from your executive summary)
- Any caveats — including any steps you skipped per Rule C (e.g. "PubMed wasn't queried because no medical signals were detected", "Skipped STEP 10 L3 enrichment because Quick tier; re-run at standard to include funder/license fields")
- Standard tier, only when STEP 11.5's Standard row finds a gap: one sentence offering the strategy export, naming the gap and the cost — e.g. *"这次中文侧主要缺知网、万方的文献；需要的话我把这两个库的专业检索式写好（约 3–4 分钟），粘进检索框就能查。"* or *"估算覆盖率 45%，还有不少没找到；需要的话我把 WOS、Scopus、PubMed 的检索式写好（约 3–4 分钟），你拿去补检。"*

---

## Output convention

📖 See `references/output_files.md` for the full directory layout. All paths below are **relative to the user's working directory (PWD)** — never the Skill asset directory.

```
$(pwd)/paper-search-results/<search_id>/
├── report.html              # Main deliverable (Shadcn style)
├── report.md                # Markdown copy
├── papers.csv               # Spreadsheet export
├── papers.bib               # Citation manager import (BibTeX)
├── papers.ris               # Alternative citation format
├── papers.json              # Full structured data
├── kg_classified.json       # Internal KG with RCS scores
├── summary.md               # Your executive summary
├── metadata.json            # Includes original_user_query / search_topic / display_title
├── execution_log.json       # PRISMA-S 16-item log
├── report_data.json         # Renderer bundle
├── chart_data.json          # Sibling: chart series
├── paper_list.json          # Sibling: per-paper list
├── prisma_log.json          # Sibling: PRISMA log JSON view
├── curve.json               # Coverage snapshot (STEP 7)
├── query_plan.json          # STEP 1 output
├── raw/                     # Retrieval output only, one file per search (openalex.json, pubmed.json, citations_01.json, …)
├── batches/                 # batch_NNN.jsonl files
└── classifications/         # batch_NNN_result.json files
```

---

## Error handling

📖 See `references/error_handling.md`. Common cases:

| Error | What to do |
|-------|-----------|
| Config missing keys | Direct user to `references/setup.md`, halt |
| Rate limit (SS 429 / NCBI 429) | Helper auto-retries; if persistent, drop that enricher |
| SS enrichment prints "0/N papers enriched (…)" | Semantic Scholar refused (rejected key or rate limit) and the helper stopped early; relay the line, carry on without it |
| OpenAlex unavailable (budget spent / throttled / down) | `openalex_helper` switches the call to Semantic Scholar itself; relay its stderr line and continue. Exit `3` = Semantic Scholar could not serve it either: handle it like any OpenAlex error (tell the user what happened and when OpenAlex resets) |
| OpenAlex 404 on DOI | Use title search fallback (helper handles) |
| L2 booster returns 0 papers | Skip silently, note in PRISMA-S log via STEP 13 |
| SubAgent classifier returns invalid JSON | `rcs_parser.py` has 5-layer fallback (regex parse) |
| HTML output size | No size cap or fallback — `html_renderer_webartifacts` always produces the full Shadcn bundle. Typical 250-paper report is ~1.7 MB; pathological 1000+ paper Audit may reach 5-10 MB. All modern browsers handle 10+ MB HTML cleanly. |

---

## References (progressive disclosure — read the one for the step you're on)

You won't read all of these every run, and shouldn't. Read a step's reference when you reach that step and it's non-trivial for the case (Rule D). **core** = read for its step; **cond** = only when its trigger fires.

| File | Load | Read when |
|------|------|---------|
| `tier_decision.md` | core | choosing the tier (before STEP 0) |
| `setup.md` | core | STEP 0 — config + 5-key acquisition |
| `runtime_bootstrap.md` | cond | STEP 0/1 — only if `$PSP_HOME` env injection failed, or you need the full install-path list / language-routing rationale |
| `query_planner.md` | core | STEP 1 — PICO / SPIDER / PEO frameworks |
| `source_routing.md` | core | STEP 1 language scope (§"Language scope" SSOT) + STEP 2 routing + STEP 5 field-priority merge |
| `openalex_helper_cheatsheet.md` | core | STEP 3 + STEP 9 — subcommands, params, gotchas |
| `pubmed_helper_cheatsheet.md` | cond | STEP 4 — only if PubMed enabled |
| `arxiv_helper_cheatsheet.md` | cond | STEP 4 — only if arXiv enabled |
| `classifier_subagent_prompt.md`, `rcs_rubric.md` | core | STEP 6 — SubAgent prompt + RCS 0-10 rubric |
| `stop_decision.md` | core | STEP 7 + STEP 8 |
| `citation_chasing.md` | cond | STEP 9 — only if expanding citations |
| `ss_helper_cheatsheet.md`, `crossref_helper_cheatsheet.md` | cond | STEP 10 — only if enriching top-N |
| `summary_writer.md` | core | STEP 11 |
| `report_title.md` | core | STEP 1 normalized topic + STEP 11 evidence-bounded display title; prevents raw-query H1 |
| `search_export/methodology.md` | cond | STEP 11.5 — only when strategy export triggers (Audit default / explicit ask / accepted Deep offer); the layer-1 semantic rulebook |
| `search_export/chinese_methodology.md` | cond | STEP 11.5 — zh/both track only (CNKI / 万方 / SinoMed strategies; not a translation of Western boolean) |
| `search_export/press_checklist.md` | cond | STEP 11.5 — PRESS six-domain self-review of the concept model |
| `search_export/filters_library.md` | cond | STEP 11.5 — only when a study-design filter is wanted (canned validated filters; never self-written) |
| `search_export/syntax_cards/<host>.md` | cond | STEP 11.5 — per-host syntax facts, machine-read by the generator/linter; open one yourself only when hand-tuning a single platform's strategy |
| `journal_metrics.md` (SSOT) | cond | STEP 1 / STEP 10-11 — only if the user wants journal partitions (中科院 / JCR / SJR) or SJR metrics; ISSN join, attribution, R-04 naming |
| `output_files.md` | core | STEP 12 — output dir layout (PWD-relative) |
| `prisma_s_checklist.md` | core | STEP 13 |
| `agent_mode.md` (SSOT) | cond | only when another agent / headless calls this Skill — `agent_search` envelope + flags |
| `error_handling.md` | cond | any unexpected error |

---

## Examples

### Example 1: Quick scan (5-8 min)

User: "find 5-6 high-impact papers on prospect theory in decision making, classics + a couple recent ones"

You: Pick Quick tier (signals: "5-6", "high-impact", short query). Run STEP 0-2 lightweight. In STEP 3 use `openalex_helper seminal` for classics + `openalex_helper search` for recent (year >= 2020). No L2 boosters in STEP 4 (pure social science). In STEP 6 classify 20-30 papers via 2 parallel SubAgents in one message. STEP 7 + 8 still run (curve renders in the report). Announce skip of STEP 9 + STEP 10 per Rule C. Render report.

### Example 2: Standard ZH (10-17 min)

User: "用 paper-search-pro 帮我找一些关于工作记忆训练干预的文献 老板让我看 我对这块完全不懂 要给老年人群体的最好 谢谢🙏"

You: Pick Standard tier (default; signals: "找一些", "老板让我看"). Detect medical signal ("干预" + "老年") in STEP 2 → enable PubMed enricher. Query plan: PICO (P=elderly, I=working memory training, O=cognitive outcomes). OpenAlex `double-sort` top-100 in STEP 3. PubMed `enrich` of openalex.json in STEP 4. Federate in STEP 5 (dict output). Classify 60-180 papers via 4 batches × 5 SubAgents — **all 5 Tasks in one message** (Rule B). STEP 7 curve, STEP 8 expand if saturation < 0.6. Render report.

### Example 3: Deep × Lit review writing (30-45 min)

User: "I'm writing a proper literature review article on attachment and human-robot interaction in elderly care contexts. Need real depth..."

You: Pick Deep tier ("proper literature review article" + "real depth"). Cross-domain (psychology + CS) in STEP 2 → enable arXiv's recent layer and OpenReview. SPIDER plan in STEP 1. OpenAlex `double-sort` top-200 + `reviews` subcommand in STEP 3. Classify 200+ papers via 8 batches in STEP 6 — dispatch 5 parallel Tasks per message, two waves. STEP 9 expand citations 2 hops. STEP 10 enrich top-50 with SS + CrossRef. Render report with PRISMA-S log.

### Example 4: Audit × SR-prep (2-3 hr)

User: "Need help — preparing a systematic review on dietary interventions for IBS in adults. Inclusion criteria: RCTs, adult populations (≥18), low-FODMAP or fiber-based interventions, English-language, published 2010-present."

You: Pick Audit tier ("systematic review" + PICO + IC). **Show limitations warning first and get user confirmation** — the Audit disclaimer is a deliver-on-it promise, fulfilled by STEP 11.5 (which Audit runs by default). At delivery it reads:

> 这是 SR 前期助手，不是 PRISMA 替代。我已为你写好各平台**可粘贴的专业检索式初稿**——每个平台附「使用前请核对」清单（已对官方词表核实的 MeSH 主题词、与需要你在库内人工确认的 Emtree 等主题词，都分别写明了）；注册制 SR 仍需你在订阅库亲自执行，并补 **ClinicalTrials.gov（注册库检索是方法学硬要求，已给检索式+直达链接）与 ICTRP/灰色文献**。

(Up front, before the run, phrase the same promise in future tense — "我会为你写好…".) STEP 4 use `pubmed_helper search-mesh "Irritable Bowel Syndrome" --pub-type "Randomized Controlled Trial"` for independent MeSH search. STEP 3 also call `openalex_helper journal-list --preset Cochrane`. STEP 10 add CrossRef enrichment for funder + clinical-trial-number. STEP 11.5 exports the per-platform strategies (Audit default). Render with PRISMA flow chart in STEP 12.
