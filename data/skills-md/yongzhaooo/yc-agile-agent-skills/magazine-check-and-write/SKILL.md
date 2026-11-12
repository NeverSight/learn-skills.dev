---
name: magazine-check-and-write
description: Fact-check a video, news story, or article against primary sources, then write it up as a correct, readable Chinese magazine-style feature, or return a claim-by-claim check report. Handles Bilibili links (BV id, URL, b23.tv) with a bundled transcript fetcher; other videos, news pages, and pasted text work from their supplied text. Use when asked to proofread or verify a news item, video, or article, or to turn it into a feature, guide, digest, or summary. Not for plain translation or prose polishing without fact-checking.
---

# Magazine Check and Write

Write the magazine piece the reader would want to read in spare time: they want to
understand the topic, not reread the source. Accuracy outranks fidelity to the author:
a piece that faithfully repeats errors leaves the reader with wrong impressions. The
deliverable is either a correct, relaxed Chinese feature with a technical appendix, or
a check report when the user only wants verification.

## 1. Get the source text

- **Bilibili video** (full URL with optional `?p=N`, `b23.tv` link, or BV id):

  ```bash
  python <skill-dir>/scripts/fetch_bilibili.py "<url_or_bvid>" --output <tmp>/<bvid>.json
  ```

  It tries official/AI subtitles, then BCut ASR, then local faster-whisper (optional
  dependency). Output has `metadata` and `transcript.segments`. For a multi-P video
  without `?p=`, ask whether the user wants one episode or the series.
- **Other video**: use subtitles or a transcript the user supplies, or one an available
  tool (such as `yt-dlp --write-subs`) can fetch.
- **News or article**: fetch the page text with the host's web tool, or use the pasted
  text. Record the outlet, author, publication date, and any later correction notice.

If no text can be obtained, report the exact failure and stop. **Never write from the
title alone**: guides generated that way invent content (a past batch described the
wrong framework and fabricated APIs and timestamps).

## 2. Clean the text internally

Fix ASR homophones and terms using the title, description, and domain knowledge
(e.g. "compare flow / chantel flow" → compileflow). Preserve numbers, negations,
conditions, quotes, and caveats. Mark guesses as guesses. This is working material,
not part of the deliverable.

## 3. Audit the claims

List the substantive claims and check each against primary sources: official
repositories, documentation, specifications, release notes; for news, the original
statement, filing, dataset, court record, or paper rather than other outlets repeating
it. Record what is correct, outdated, overstated, narrow (e.g. only one vendor's
ecosystem or region), misattributed, or wrong, and the mainstream alternatives or
counter-evidence.

- Verify every link, number, date, version, license, quote, and API signature that will
  appear in the output. Facts you could not verify stay out or are marked unverified.
- For GitHub facts, prefer authenticated `gh api repos/<owner>/<repo>` when available;
  anonymous API calls from shared egress IPs are often rate-limited.
- For news, separate what the source reports from what it infers, and note the date
  your check reflects; developing stories change.

## 4. Choose the output

- **Check**: the user wants proofreading or verification only. Give a table of claims
  with verdict, correction, and source link, then a short overall judgment.
- **Supplement**: the source is basically right. Retell the topic for a reader who has
  not seen it, writing corrections directly into the narrative (never "原作者说……其实……").
  Add a section "挑挑刺" that reviews the source's key judgments, then the appendix.
- **Rewrite**: the user values the topic rather than the narration, or the audit found
  errors or a narrow perspective that would mislead. Write an independent, correct guide
  with your own running example. Do not restate or rebut the source; the source line
  only credits the topic.

Use the mode the user names. Otherwise pick by the request and audit result, and state
the choice and reason when reporting.

## 5. Outline, write, then fact-check

1. Write an outline: section order, what each section must convey, one running example,
   and the verified fact list (names, numbers, dates, links, code facts) that must appear
   unchanged.
2. If the host offers a writing subagent and the article is long enough to justify it,
   hand it the outline, fact list, style rules, and
   [the reference article](references/example-rewrite.md) for tone. Otherwise write it
   yourself from the same inputs; no helper agent is required.
3. Read the whole result against the fact list and sources. Writers tend to add confident
   but unsupported specifics (performance claims, absolute statements, wrong mechanisms).
   Fix or remove each one.

Style:

- Like a senior colleague telling a story over tea: plain, relaxed, concrete, lightly
  humorous, varied sentence length. Assume the reader has not seen the source.
- Start from a scenario and the problem, then the idea, how it works, its costs, and
  how to choose. Explain each term with an everyday analogy on first use.
- Prefer paragraphs over bullet lists; little bold; no emoji, slogans, AI filler
  ("值得注意的是", "总而言之"), or transcript excerpts.

Structure:

```markdown
# <readable title containing the core terms; no clickbait>

> 来源/选题说明（原标题、链接、作者或媒体、日期；mode 声明；事实核对日期；阅读时长）
> 标签：#术语 ...

---

<story-driven body>

---

## 细节与延伸阅读
<table of tools, organizations, or sources: what it is, status, link>
<small verified code sample marked 示意, when it helps>
<further reading: primary sources, official docs, the original item>
```

## 6. Deliver

Save the result as Markdown where the user asks; otherwise in the working directory,
named after the source id or a short slug, and report the path. Do not commit it to an
unrelated project repository.

If the user keeps such guides in Bench (a `bench` CLI is configured), import with a
content-stable identity so any device updates the same record, then sync and read back:

```bash
bench --import-markdown <file>.md --project global --source-key <bilibili-BVid|news-slug> --author ai --tag <topic>
bench --sync
```

Check `bench --status <ID>` reports `indexed`.
Do not use `bench ob`: it keys records on the local file path and duplicates across devices.

## Lessons

- A knowledge-base title prioritizes retrievable terms over the source's
  click-oriented title.
- The audit belongs in the article as corrected content (supplement) or as a better
  independent explanation (rewrite), not as a list of the author's mistakes placed after
  a faithful retelling.
- An author's choice of example tool often reflects one ecosystem; check what is
  mainstream internationally before presenting it as the default.
