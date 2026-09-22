---
name: bazi-skill
description: Specialized workflow for BaZi 八字, Four Pillars 四柱, optional Zi Wei Dou Shu 紫微斗数 evidence, optional Western astrology / zodiac / 星座 evidence, optional NaYin 纳音, branch-relation 刑冲合害, Qi Men Dun Jia 奇门遁甲, Liu Yao 六爻 evidence, K-line style fortune JSON, true solar time 真太阳时, compatibility/synastry 合盘合婚, auspicious date/hour selection 择日择时, professional report writing, structured reports, 命理研报, and multi-school master/orchestrator workflows 多流派大师/主理规划师/主理官综合. Use when the user asks to build, debug, validate, or improve a host project that computes chart facts with code and asks AI only to interpret confirmed facts.
---

# bazi-skill

Use this skill for project-aware BaZi, optional Zi Wei Dou Shu evidence, optional Western astrology evidence, optional common-school evidence, and K-line style fortune workflows. Preserve the source-of-truth split: local libraries calculate charts; AI writes structured interpretation against a confirmed chart.

## Workflow

1. Classify the task:
   - Code change in a host project: read the repository docs and the touched modules before editing. Start with `CLAUDE.md` if present, then the relevant `components/CLAUDE.md`, `services/CLAUDE.md`, `types/CLAUDE.md`, or `constants/CLAUDE.md` if present.
   - Skill or workflow architecture change, including requests to reference `ai-berkshire`, a multi-agent research/team pattern, multi-school masters, 大师会诊, 主理规划师, or 主理官综合: update this skill or related skill docs first; do not change frontend/backend application code unless the user explicitly asks for implementation.
   - Analysis JSON generation, repair, or validation: read `references/project-contracts.md`, then run `scripts/validate_analysis_result.py` on any candidate JSON.
   - BaZi rules, prompt wording, scoring logic, or domain explanation: read `references/bazi-domain-reference.md`, then `references/analysis-methods.md` when the task needs interpretation or ranking.
   - 盲派象法, 象法体系, concrete imagery, 宫位象, 十神象, or requests to make 象法 more complete/source-bounded: read `references/xiangfa-system/source-map.md`, then `references/xiangfa-system/coverage-map.md`, then only the required slice files.
   - True solar time, strict apparent solar time, timezone, longitude correction, equation of time, or boundary-hour issues: read `references/true-solar-time.md`; if implementing, also read `references/project-contracts.md`.
   - Zi Wei chart logic, palace display, or pattern wording: read `references/ziwei-reference.md`.
   - Western astrology, zodiac signs, star signs, 星座, 西洋占星, natal chart, ascendant, moon sign, aspects, transits, or astrology synastry: read `references/western-astrology.md`.
   - NaYin 纳音, branch relations 刑冲合害, Qi Men 奇门遁甲, Liu Yao 六爻, Mei Hua 梅花易数, Da Liu Ren 大六壬, modern astrology, traditional astrology, or other school extensions: read `references/common-schools.md`; then load only the matching prompt/reference files.
   - Compatibility or synastry analysis, 合盘, 合婚, 伴侣匹配, relationship fit, or partnership matching: read `references/compatibility-analysis.md`, plus `references/analysis-methods.md`; if the task is also app implementation, read `references/project-contracts.md`.
   - Auspicious date/hour selection, 吉日吉时, 择日, or 择时: read `references/auspicious-timing.md` and `references/analysis-methods.md`; if the task is also app implementation, read `references/project-contracts.md`.
   - Professional report, 命理研报, structured report, Markdown report, or HTML report workflow: read `references/report-generation.md` and `references/project-contracts.md`; if using an `AnalysisResult`, validate the JSON before composing the report.
   - 古籍条文、典籍引用、条文出处、引用核对，或需要为判断补依据: read
     `references/classics/index.md`, then only the topic card files your school needs;
     verify with `scripts/validate_citations.py`; locate raw source text with
     `scripts/search_classics.py --corpus`. Never read `references/classics/corpus/`
     end to end.

2. Apply an information-completeness gate before analysis, JSON generation, report rendering, or multi-agent work:
   - If required user information is missing, ask follow-up questions before proceeding. Do not guess birth facts, chart facts, event constraints, relationship counterpart data, or report scope.
   - Ask only the missing essentials, preferably 1-3 concise questions at a time.
   - For normal BaZi calculation, required essentials are: gender, birth date, birth time, calendar type (solar/lunar if ambiguous), birthplace plus longitude/timezone basis, and whether true solar time should use the current legacy method or strict apparent solar time when that distinction matters. City-level birthplace is acceptable by default only when it resolves to a longitude; for boundary-hour or professional requests, prefer district/township, map point, hospital, or manual longitude. For Zi Wei, first verify that the current repo actually contains a tracked implementation and contract; otherwise treat Zi Wei as unavailable or planned. For Western astrology, first verify a tracked ephemeris/service or require a user-confirmed astrology chart; otherwise treat it as unavailable or planned.
   - For professional-mode chart input, required essentials are: four pillars and gender. Birth year, startAge, direction, and daYun can use documented defaults only when the user accepts approximate/professional-mode behavior.
   - For compatibility/synastry, require both people’s chart inputs or confirmed charts plus the relationship goal/context.
   - For auspicious timing, require event type, candidate date range, location/timezone, and any hard constraints before ranking dates/hours.
   - For Qi Men or Liu Yao, require a computed/user-confirmed plate or hexagram plus the exact event/question; do not cast or derive the plate/hexagram in AI text.
   - For professional reports, require the source `BaZiResult`, `AnalysisResult`, or report-spec JSON and the desired output format/scope before rendering.
   - Optional missing details may be handled with explicit assumptions only when the final output remains contract-valid and the user request is not asking for precision.

## Multi-School Masters + Orchestrator Pattern

Use this pattern when the user asks for an `ai-berkshire`-style team workflow, multi-agent analysis, 多流派大师, 大师会诊, 主理规划师, 主理官综合, deep review, report generation, or a complex task where different mainstream schools should be compared. For role details, read `references/agent-roles.md`; for executable school prompts, read `references/school-prompts/index.md` and only the selected role prompt files.

### Four-layer design

1. **Skill layer**: The skill is the scenario entry point. It decides the workflow, required references, output contract, and validation gates.
2. **Orchestrator-planner layer**: The planner decides which facts are missing, which roles are useful, which roles must be skipped, and which validation steps are required.
3. **School-master layer**: Parallel master personas represent different mainstream schools. They perform school-specific interpretation from the same evidence packet. They do not own source-of-truth calculations and do not emit final app contracts directly.
4. **Tool/validator layer**: Local deterministic libraries and scripts are the authority for chart facts, schema checks, JSON validation, and report composition.

### Orchestrator workflow

For complex BaZi/Zi Wei/Western astrology/common-school/K-line work, the main agent acts as **orchestrator / 主理官**:

1. Build an evidence-availability packet from code-computed facts, validated JSON, user constraints, and relevant references.
2. Load `references/school-prompts/orchestrator-planner.md` and produce a dispatch plan with task type, missing facts, selected references, selected masters, parallel groups, and validation steps.
3. If the planner identifies blocking missing facts, ask the user or compute them with deterministic code before dispatching masters.
4. Load `references/school-prompts/index.md`, then load only the selected masters from the planner output.
5. Require each selected master to return school-specific thesis, evidence, risks, confidence, and recommended wording. Masters may not recalculate chart facts.
6. Compare school disagreements explicitly; resolve by source hierarchy: code facts > project contract > 典籍条文（`核心论断`/`操作规则`）> task-specific method fit > 典籍条文（`例证`）> cross-school consensus > narrative preference — classics are deliberately split into two tiers around method fit, not collapsed into one (full hierarchy and rationale: `references/agent-roles.md`, `references/school-prompts/orchestrator.md`).
7. The orchestrator synthesizes the final answer, JSON, or report. Do not average school scores mechanically.
8. Validate final artifacts with deterministic scripts before treating them as ready.

### Execution rules

- Start school masters in parallel only when the task is large enough to benefit from independent views. For small edits, use a single-agent workflow.
- Do not start parallel masters until the information-completeness gate has passed or the user has explicitly accepted the stated assumptions.
- Run the orchestrator-planner before master dispatch for complex/report-grade tasks. The planner is allowed to select a single role or no school-master role when that is sufficient.
- The planner must explain skipped roles when a role seems relevant but lacks computed evidence.
- Every master prompt must include: "CONFIRMED BY USER - DO NOT RECALCULATE, USE AS TRUTH" and the relevant confirmed facts.
- Give each master the same source-of-truth evidence packet plus only the references required for its school.
- If a selected prompt file says the current project lacks a complete knowledge base for that sub-school, preserve that limitation in the master output as `evidence_gap` instead of inventing rules.
- Master outputs should be concise findings, risks, evidence, scores, or section edits. The orchestrator must synthesize; do not paste master reports together.
- The orchestrator owns final decisions, contract shape, JSON repair, and user-facing wording.
- Validate every final `AnalysisResult` with `scripts/validate_analysis_result.py` before treating it as ready.
- For professional reports, run the report-generation workflow after JSON validation; masters may review sections, but final prose consumes computed/validated data only.
- Do not implement runtime multi-agent behavior in the frontend/backend unless the user explicitly asks for an app code change.

3. Keep calculation authority local:
   - Normal birth input uses `services/baziService.ts` with `lunar-javascript`.
   - `birthLocation` is provenance/display text; `longitude` is the actual calculation input for current solar-time correction.
   - Convert lunar input to solar before true-solar-time adjustment.
   - Current project true-solar-time behavior is a legacy longitude correction: `clock time + (longitude - 120) * 4 minutes`.
   - For strict apparent solar time, add timezone-standard-meridian handling and equation-of-time correction; see `references/true-solar-time.md`.
   - Da Yun from `lunar.getEightChar().getYun(genderCode)` is authoritative when normal birth data is available.
   - Professional mode accepts user-entered pillars as truth and only fills defaults for missing `startAge`, `direction`, and `daYun`.
   - Do not assume the repo contains a Zi Wei service. Verify tracked/present files before referencing any path such as `services/ziweiService.ts` or `components/ZiWeiChartPanel.tsx`.
   - If Zi Wei is implemented, its palaces, stars, Si Hua, Da Xian, and pattern evidence must still come from deterministic code or a vetted library; do not hand-roll these facts in AI text.
   - Do not assume the repo contains a Western astrology service, ephemeris, or chart UI. Verify tracked/present files before referencing implementation paths.
   - If Western astrology is implemented, sun sign, moon sign, ascendant, houses, planetary placements, aspects, transits, synastry, and composite facts must come from deterministic code or user-confirmed charts.
   - Do not assume the repo contains Qi Men, Liu Yao, NaYin, or Da Liu Ren services. Verify tracked/present files before referencing implementation paths.
   - If Qi Men or Liu Yao is used, the plate or hexagram must come from deterministic code or a user-confirmed cast. AI must not cast, randomize, or derive it.
   - Never ask an AI model to calculate or recalculate BaZi, Da Yun, Liu Nian GanZhi, Zi Wei palaces/stars, Western astrology placements/houses/aspects/transits, NaYin labels, branch/stem relation matrices, Qi Men plates, Liu Yao hexagrams, compatibility matrices, or auspicious timing pillars. Code must compute these facts first; AI may only interpret, summarize, explain, rank from supplied features, or polish wording.

4. Treat confirmed chart data as truth:
   - Prompts must tell the AI: "CONFIRMED BY USER - DO NOT RECALCULATE, USE AS TRUTH".
   - Do not let model text contradict `BaZiResult.bazi`, `startAge`, `direction`, `daYun`, `birthYear`, or `gender`.
   - If a user edits pillars in the confirmation screen, downstream analysis must use the edited pillars.
   - When sending data to AI, include computed facts and feature labels, not raw birth details as an invitation to recalculate.

5. After a chart run, advance the conversation with a current-life question:
   - When the user asks to "run", "排盘", or provides birth data without a specific analysis question, first return the computed facts and a concise reading.
   - After the concise reading, ask the user what has been troubling them recently or what domain they want to focus on next, such as career, money, relationship, study, family, health, relocation, timing, or decision pressure.
   - Phrase the follow-up as a natural next step, for example: "如果要继续细看，我需要知道你最近最困扰的是什么；我会结合当前日期、当前大运、流年/流月与这张命盘来推。"
   - For deeper current-period analysis, use the current date, current Da Yun, current Liu Nian, and Liu Yue/Liu Ri when relevant, but keep the confirmed birth chart and Da Yun as source of truth.
   - Do not invent the user's current problem. If the user has not supplied a focus area, ask before giving a detailed current-life judgment.

6. Preserve the K-line `AnalysisResult` contract:
   - Output must be valid JSON, no markdown.
   - Include all top-level `AnalysisResult` fields documented in `references/project-contracts.md`.
   - `timeline` must contain exactly 100 entries, birth year through birth year + 99, ages 1 through 100.
   - Keep OHLC values integers or finite numbers from 0 to 100.
   - Include both rising and falling candles.
   - Mark exactly one `isPeak: true`; backend provider services currently normalize the peak to the highest `high`, tie-breaking by `close`.

7. Produce report artifacts from computed data only:
   - A professional report must consume confirmed `BaZiResult`, `AnalysisResult`, optional Zi Wei facts, optional Western astrology facts, optional common-school facts, compatibility results, or auspicious-timing feature tables.
   - Do not let the report-generation stage recalculate pillars, true solar time, Zi Wei stars, Western astrology placements/aspects/transits, NaYin labels, Qi Men plates, Liu Yao hexagrams, compatibility relations, or timing candidates.
   - Include computation metadata, method notes, caveats, and source-validation status.
   - Do not offer PDF export or offline PDF rendering; this skill currently supports structured, Markdown, or HTML-style report content only.

8. Edit prompts and schemas together:
   - Frontend manual prompt lives in `utils/promptGenerator.ts`.
   - Backend Gemini prompt/schema lives in `backend/src/services/gemini.ts`.
   - Backend Claude prompt lives in `backend/src/services/claude.ts`.
   - When adding, renaming, or making a field required, update `types.ts`, frontend rendering, backend prompt/schema, demo data, and validation logic together.

9. Use culturally careful output:
   - Frame BaZi/Zi Wei/Western astrology/Qi Men/Liu Yao as cultural analysis and reflective guidance, not deterministic medical, legal, or financial advice.
   - Avoid frightening, absolute, or diagnosis-like claims.
   - For investment language, describe temperament, risk style, and timing tendencies; do not recommend specific securities or guaranteed returns.
   - For compatibility language, describe interaction dynamics and risk points; do not frame a relationship as doomed or guaranteed.
   - For auspicious timing, rank candidate windows and explain tradeoffs; do not present a time as guaranteed to cause an outcome.

## Resources

- `references/project-contracts.md`: repository map, TypeScript data contracts, AI provider contract, and output checklist.
- `references/bazi-domain-reference.md`: concise BaZi tables and rule reminders adapted for this app's current implementation.
- `references/analysis-methods.md`: distilled project methods from AlgorithmGuide, llms docs, and module docs for K-line scoring, eight-dimension analysis, and day/hour ranking.
- `references/true-solar-time.md`: current vs strict true solar time, equation-of-time handling, timezone design, and boundary-hour policy.
- `references/compatibility-analysis.md`: two-chart comparison method for 合盘, 合婚, relationship fit, and partnership matching.
- `references/ziwei-reference.md`: optional Zi Wei workflow rules, repo-verification policy, and no-assumption boundaries.
- `references/western-astrology.md`: optional Western astrology / zodiac workflow rules, evidence gate, and BaZi cross-check policy.
- `references/common-schools.md`: optional common-school extensions for NaYin, branch relations, Qi Men, Liu Yao, and modern/traditional astrology split.
- `references/auspicious-timing.md`: workflow for day/hour granularity, event-type inputs, scoring, and output format for 吉日吉时.
- `references/report-generation.md`: professional structured/Markdown/HTML report workflow, section structure, and QA checklist.
- `references/agent-roles.md`: multi-school master + orchestrator workflow, school roster, evidence packet, and synthesis rules.
- `references/xiangfa-system/`: source map, coverage map, and local rule slices for source-bounded 盲派象法 / 象法 scene language.
- `references/school-prompts/`: executable prompt templates and source-bounded knowledge slices for the orchestrator and each school master.
- `scripts/validate_analysis_result.py`: deterministic validator for candidate K-line `AnalysisResult` JSON.
- `references/classics/index.md`: 古籍知识层入口，三向路由、卡片契约、层级定义与引用规范。
- `scripts/validate_citations.py`: 卡片库自检（`--cards`）与答案/报告引用校验（`--answer`）。
- `scripts/search_classics.py`: 零依赖检索，卡片优先、原文回落。

## Useful Commands

These commands assume the current working directory is an arbitrary host
project, not the skill's own directory: script paths and the skill's own
`references/` paths always use the full install path
`${CODEX_HOME:-$HOME/.codex}/skills/bazi-skill/...`; user-supplied data files
(`result.json`, `answer.md`) resolve relative to that host-project working
directory.

Validate a JSON file:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/bazi-skill/scripts/validate_analysis_result.py" result.json
```

Validate stdin with an explicit birth year:

```bash
cat result.json | python3 "${CODEX_HOME:-$HOME/.codex}/skills/bazi-skill/scripts/validate_analysis_result.py" --birth-year 1990 -
```

校验卡片库：

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/bazi-skill/scripts/validate_citations.py" --cards "${CODEX_HOME:-$HOME/.codex}/skills/bazi-skill/references/classics"
```

校验一份 master 输出或报告的引用使用：

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/bazi-skill/scripts/validate_citations.py" --answer answer.md --classics-root "${CODEX_HOME:-$HOME/.codex}/skills/bazi-skill/references/classics"
```

检索条文：

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/bazi-skill/scripts/search_classics.py" "衰旺真机" --school 旺衰扶抑 --classics-root "${CODEX_HOME:-$HOME/.codex}/skills/bazi-skill/references/classics"
python3 "${CODEX_HOME:-$HOME/.codex}/skills/bazi-skill/scripts/search_classics.py" "余寒犹存" --corpus --classics-root "${CODEX_HOME:-$HOME/.codex}/skills/bazi-skill/references/classics"
```
