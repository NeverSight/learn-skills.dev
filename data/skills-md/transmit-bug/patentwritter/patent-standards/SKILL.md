---
name: patent-standards
description: The standards catalog (专利标准/资料目录) for the patent-writing skill set — a thin index declaring which authoritative CN/US texts exist, where they live, and which per-type anchor file governs each patent type. Content is split by type under references/ (invention / utility model, design, US, CN professional practice, professional discipline, catalog); anchor article numbers were verified against the official CNIPA/USPTO full texts (2026-08-11 invention / utility model, 2026-08-12 design, 2026-08-13 CN professional practice). Consumed by the self-service skills (patent-intake, patent-drafting, patent-drawings, patent-compliance, patent-filing) and the professional CN group. Declares WHAT exists and where; retrieval belongs to environment tools and humans.
---

# Patent Standards (专利标准/资料目录)

The catalog of authoritative texts governing patent drafting and examination in CN and US, plus the citation discipline every writing skill follows. This skill is a **declaration**, not a retrieval tool: it says what exists and where; the environment's tools do the actual reading.

## Reference files (consume per type, load only the single per-type anchor file your branch needs)

| File | Content | Consumers |
|---|---|---|
| `references/cn-invention-utility.md` | Invention / utility-model anchors: 专利法 (第2/9/22/24/26/33/42条), 细则 (第17/20-26/43/46/47条), 指南 (第一部分第二章, 第二部分第二/三/四/五/九章) | patent-intake (invention / utility model), patent-drafting, patent-drawings (drawings part), patent-compliance (checks 1-7), patent-filing (invention / utility-model parts) |
| `references/cn-design.md` | Design anchors: 专利法 (第2条第4款 / 23 / 27 / 31条第2款 / 33条第2款 / 42条), 细则 (第30/31/32/40/43/44/53/57条第2款 / 58条第2款), 指南 (第一部分第三章 4.2-4.5) | patent-intake (design branch), patent-drawings (design drawings section), patent-compliance (check 8), patent-filing (design points) |
| `references/us.md` | US anchors: 35 U.S.C. (§100-112 / 251), 37 CFR Part 1 (§1.57-1.121), MPEP (§608 / 706 / 2106 / 2163 / 2164 / 2171-2176) | reserved US anchor table (no active consumers; CN group uses cn-professional) |
| `references/cn-professional.md` | CN professional-practice anchors for the prosecution pipeline (法37 / 41 / 45-47 / 66.2, 细则57.3 / 58 / 62-63 / 65-76, 指南II-4 3.2.1.1 / II-8 4.10.3 / 4.11.3.2 / IV / V-10), stage anchor map, 摘要300字 inconsistency note, agent-side honesty anchors | professional CN group (patent-prosecution entry + patent-oa-response, patent-re-exam, patent-invalidation, patent-evaluation-report, patent-claim-strategy) |
| `references/professional-discipline.md` | The shared professional discipline — declare / consume / cite / fail loud / never invent (jurisdiction-neutral single home; us.md and cn-professional.md reference it) | professional group, all jurisdictions |
| `references/catalog.md` | CN/US authoritative-text catalog (official location, edition, edition summary) + declared external source (CNIPA Publication & Announcement System) | when source info / external-source entries are needed |

Anchor verification: invention / utility model 2026-08-11, design 2026-08-12, both tested against the official CNIPA full texts; US 2026-08-10 verified against official sources; CN professional practice 2026-08-13. **Skills must cite the per-type anchors — not chapter-level approximations — and cite the verified per-type anchor numbers as recorded.**

## How writing skills invoke this skill

Two consumption modes:

- **Self-service direction**: use the corresponding reference file as an on-demand standards pointer. Keep the drafting and interview content clean; do not paste article numbers, statutory explanations, or `Rule basis` tables into the user-facing draft. Only surface a standards detail when the user asks for a legal explanation or a compliance blocker requires it.
- **Professional direction**: read `references/professional-discipline.md` (the shared discipline — declare / consume / cite / fail loud / never invent, single jurisdiction-neutral home) and the per-jurisdiction anchor file — `references/us.md` (US skills, reserved, hidden) or `references/cn-professional.md` (CN prosecution skills). Follow the discipline; cite the per-jurisdiction anchors.

## The discipline — four clauses, one prohibition (professional full version)

> The professional discipline (declare / consume / cite / fail loud / never invent) lives in `references/professional-discipline.md`, jurisdiction-neutral and shared by the professional group; `references/us.md` and `references/cn-professional.md` reference it and carry the per-jurisdiction anchors.

## Self-service discipline (simplified version)

Self-service skills referencing this catalog follow:

1. **Standards pointer**: read `references/cn-invention-utility.md` / `references/cn-design.md` only when a standards question or check requires it; the normal drafting output carries the file index, not a legal citation dump.
2. **Honesty red line**: prior art only from the three kinds of material — known prior solutions / objective common problems / real search-tool results. Write only from declared sources and delegated-search results patent numbers, references, or experimental data.
3. **Fail loud**: when input is missing (e.g. incomplete four elements) or a tool is missing (e.g. no dot), state exactly what is missing — don't force output.
4. **Out of scope**: professional work such as OA responses is not in this package.

## Scope guard

- CN + US only. EP / PCT, other jurisdictions: out of scope of this skill set.
- This skill declares what exists; it is not a search tool, not a corpus, not a knowledge base.
