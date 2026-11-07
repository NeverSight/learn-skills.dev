---
name: thesis-workflow-cn
description: Main entry skill for Chinese undergraduate thesis workflows. Use first when the user asks for thesis topic selection, literature retrieval, literature review, proposal drafting, thesis outline and word budget, project material analysis, body chapter writing (正文), figures and tables (图表), thesis QC or mock blind review, Word conversion, "完整流程", "从选题到综述/开题/成稿", "写完整篇论文", or any task that may involve thesis-related modules. This is the single public workflow entrypoint; it routes internally to modules/undergraduate-thesis-topic, modules/cnki-cssci-search, modules/workbuddy-cnki-webbridge-search, modules/literature-review-cn, modules/thesis-proposal-cn, modules/thesis-outline-cn, modules/thesis-materials-cn, modules/thesis-body-cn, modules/thesis-figures-cn, modules/thesis-qc-cn, and modules/docx-editor-cn, asks whether to continue after each completed stage, and defaults to generating Word documents for literature reviews, proposal reports, and the full thesis.
---

# Thesis Workflow CN

## Overview

Use this skill as the single public entry point for Chinese undergraduate thesis work. Route all thesis-related requests through this workflow first, then delegate stage-specific work to internal modules under `modules/`.

Do not duplicate the long rules from internal modules. Read and follow the relevant module `SKILL.md` when a stage becomes active.

After each stage is completed, stop and ask the user whether to continue to the next stage. Do not silently proceed to the next major stage unless the user has already explicitly asked for an uninterrupted end-to-end run.

## Internal Modules

- Topic selection and scoping: `modules/undergraduate-thesis-topic/SKILL.md`
- Chinese CNKI/CSSCI/C-journal and English title-abstract retrieval: `modules/cnki-cssci-search/SKILL.md`
- WorkBuddy-only CNKI/知网 retrieval: `modules/workbuddy-cnki-webbridge-search/SKILL.md`
- Chinese literature review drafting or polishing: `modules/literature-review-cn/SKILL.md`
- Chinese undergraduate thesis proposal drafting or polishing: `modules/thesis-proposal-cn/SKILL.md`
- Thesis body outline and word budget: `modules/thesis-outline-cn/SKILL.md`
- Project materials, project understanding, and screenshot list: `modules/thesis-materials-cn/SKILL.md`
- Body chapter drafting in Markdown: `modules/thesis-body-cn/SKILL.md`
- Figures (Mermaid diagrams, matplotlib charts, screenshot lists) and tables: `modules/thesis-figures-cn/SKILL.md`
- Mechanical QC and role-based review: `modules/thesis-qc-cn/SKILL.md`
- Word document creation, template filling, `.docx` editing, and full-thesis Markdown → Word: `modules/docx-editor-cn/SKILL.md`

Thesis type templates shared by the body-stage modules, in `references/paper-types/`: `system-design.md` (系统设计与实现), `algorithm-improvement.md` (算法模型改进), `engineering-design.md` (工程设计), `empirical.md` (实证研究), `experimental.md` (实验研究), `case-study.md` (案例分析对策研究), `law.md` (法学研究), `humanities.md` (人文论述), `design-creative.md` (设计创作策划方案).

If a listed module is unavailable in the current environment, continue manually with the same stage boundaries and state the limitation. `$kimi-webbridge` remains an external browser-control skill and must still be read when the WorkBuddy CNKI module requires it.

## Workflow

1. Establish the current stage and existing materials:
   - Major, rough direction, or confirmed title.
   - Whether there is project code, a dataset, survey, experiment, or internship case to draw on.
   - School template, word count, and document format.
   - Existing literature records, abstracts, literature review, proposal draft, or Word template.
2. Route to the earliest missing stage. Do not ask the user to restate information that is already present in the thread.
3. Produce the stage output that can become the next stage input.
4. For literature review and proposal stages, create both the text deliverable and a Word `.docx` deliverable by default unless the user explicitly requests text only.
5. At each transition, summarize the handoff in a compact "阶段交接" block: confirmed title, scope, materials, output files, and next recommended action.
6. Ask a concrete next-step question after each completed stage, using the next stage in the default chain.
7. Preserve confirmed constraints across stages, especially implementation status, thesis type, word count, template requirements, and citation rules.

## Default Stage Chain

Use this chain unless the user asks to skip or start from a later stage:

1. 选题确认: read `modules/undergraduate-thesis-topic/SKILL.md`
2. 文献材料准备: read `modules/workbuddy-cnki-webbridge-search/SKILL.md` for WorkBuddy CNKI/知网 retrieval, `modules/cnki-cssci-search/SKILL.md` for ordinary real literature retrieval, or use user-provided literature records when already available
3. 文献综述写作并转 Word: read `modules/literature-review-cn/SKILL.md`, then `modules/docx-editor-cn/SKILL.md`
4. 开题报告写作并转 Word: read `modules/thesis-proposal-cn/SKILL.md`, then `modules/docx-editor-cn/SKILL.md`
5. 正文大纲与字数分配: read `modules/thesis-outline-cn/SKILL.md`
6. 素材整理与截图清单: read `modules/thesis-materials-cn/SKILL.md`
7. 分章写作: read `modules/thesis-body-cn/SKILL.md`
8. 图表制作: read `modules/thesis-figures-cn/SKILL.md`
9. 质检与审阅: read `modules/thesis-qc-cn/SKILL.md`
10. 整篇论文转 Word: read `modules/docx-editor-cn/SKILL.md` and run `scripts/md2docx_thesis.js`

Do not require a separate "Word document" final stage for 文献综述 or 开题报告. Word generation is part of those stages. For the thesis body, Word is built once from all chapter Markdown files in stage 10 and rebuilt after every later fix.

Stages 7 and 8 may interleave: figure sources can be produced right after the chapter that needs them. Stage 9 can run per chapter during drafting, but the full review runs after all chapters exist.

### Thesis Project Folder

From stage 5 on, keep all thesis-body artifacts in one project folder (ask the user where, default `./论文/`):

```text
<论文项目>/
├── plan/        大纲.md, 字数分配.json, 图表清单.md
├── materials/   项目清单.md, 项目理解.md, 截图清单.md
├── literature/  题录摘要.md and other literature records from stage 2
├── chapters/    00-摘要.md, 01-绪论.md, ..., 90-参考文献.md, 91-致谢.md
├── figures/     src/*.mmd, src/*.py, rendered *.png, user screenshots
├── qc/          质检报告.md, 审阅意见.md
└── output/      论文.docx
```

Copy the literature records from stage 2 into `literature/` so citation tracing works.

## Continuation Prompts

At the end of each completed stage, ask only one concise continuation question:

- After topic confirmation: "题目已确认。是否进入文献综述阶段？我会先确认/准备文献材料，然后写综述并自动转成 Word。"
- After literature retrieval or literature material confirmation: "文献材料已准备好。是否开始写文献综述并生成 Word 文档？"
- After literature review Word output: "文献综述和 Word 文档已完成。是否进入开题报告阶段？我会基于题目和综述写开题报告并自动转成 Word。"
- After proposal Word output: "开题报告和 Word 文档已完成。是否进入论文正文阶段？我会先做正文大纲和字数分配，确认后再写。"
- After outline confirmation: "大纲和字数分配已确认（建议先发给指导老师看）。是否开始整理项目素材？请告诉我项目代码、截图、数据所在的文件夹。"
- After materials confirmation: "项目理解和截图清单已完成。是否开始写正文？有两种写法：A. 每写完一章停下来给你看，确认或修改后再写下一章（推荐）；B. 按顺序一次写完全部章节，最后统一汇报。不选的话按 A 进行。"
- After each chapter in mode A: report that chapter and what to check in it, then ask "这一章有需要修改的吗？没有的话我接着写下一章。"
- After all chapters: "正文各章已完成（共 N 字，目标 M 字）。是否生成图表并渲染？"
- After figures: "图已渲染，截图清单已列出。是否进入质检和模拟盲审？"
- After QC: "质检完成，问题已修改。是否生成整篇 Word？"
- After full Word output: "整篇论文 Word 已生成。请在 Word 中更新目录并检查版式；是否还需要按学校模板调整格式？"

If the user says yes, continue with the next stage. If the user says no, stop and keep the handoff ready for later resumption.

## Stage Routing

### Stage 1: Topic

Read `modules/undergraduate-thesis-topic/SKILL.md` when the topic is broad, missing, too large, or needs feasibility comparison.

Exit only when there is a confirmed or recommended title plus a clear thesis type, research object, scope boundary, and evidence/material plan.

After exit, ask whether to enter the literature review path. If literature records are missing, the next action is literature material preparation before drafting the review.

### Stage 2: Literature Retrieval

Read `modules/workbuddy-cnki-webbridge-search/SKILL.md` when the request is for WorkBuddy/workbuddy and needs CNKI/知网, CSSCI, C-journal, C刊, Chinese journal records, bibliographic records, abstracts, or a literature database. In this route, do not use web search/search_query or search engines; the module must use Kimi WebBridge and CNKI's official website.

Read `modules/cnki-cssci-search/SKILL.md` for ordinary non-WorkBuddy Chinese or English literature records, abstracts, or literature database retrieval.

Before retrieval, confirm target counts for each language channel. Treat bibliographic records without abstracts as incomplete if abstracts were requested.

Exit only when the literature output paths or pasted records are available, the actual count is known, and missing abstracts or relevance compromises are clearly marked.

If the user already supplied usable records and abstracts, this stage can be marked complete without live retrieval. Then ask whether to write the literature review and generate Word.

### Stage 3: Literature Review

Read `modules/literature-review-cn/SKILL.md` when the user needs a 文献综述/研究综述 from provided abstracts or literature records.

Ask for the review template or formatting requirements before writing unless the user already said there is no template. Do not cite records outside the provided materials.

Exit with:

- A usable literature review draft.
- A reference list built only from supplied metadata.
- A generated Word `.docx` file created by following `modules/docx-editor-cn/SKILL.md`, using the user's template or default Chinese academic formatting.

If Word generation cannot be completed because a template, dependency, or render step is blocked, report the exact blocker and keep the text draft as the stage output.

### Stage 4: Proposal

Read `modules/thesis-proposal-cn/SKILL.md` after the title is confirmed and enough background or literature material exists.

When the literature review or records are not available, keep the research-status section general and mark that real literature support is still needed.

Exit with:

- Proposal sections that match the user's template when provided.
- A generated Word `.docx` file created by following `modules/docx-editor-cn/SKILL.md`, using the user's template or default Chinese academic formatting.

If Word generation cannot be completed because a template, dependency, or render step is blocked, report the exact blocker and keep the text draft as the stage output.

### Stage 5: Outline and Word Budget

Read `modules/thesis-outline-cn/SKILL.md` after the proposal (or when the user brings a confirmed title and wants to start the body).

Exit with `plan/大纲.md` and `plan/字数分配.json` confirmed by the user. Remind the user to send the outline to their supervisor before drafting.

### Stage 6: Materials and Screenshot List

Read `modules/thesis-materials-cn/SKILL.md` when the thesis depends on a real project, data, survey, or case.

Exit with `materials/项目理解.md` confirmed by the user and `materials/截图清单.md`.

For argument-based theses with no project, skip this stage.

### Stage 7: Chapter Drafting

Read `modules/thesis-body-cn/SKILL.md`. Draft the chapters in the module's drafting order into `chapters/*.md`, chapter by chapter with a stop for the user's review after each (default), or in one pass if the user chose that.

Exit when every outline chapter has a file, citations are renumbered by first appearance, and `90-参考文献.md` lists only cited records.

### Stage 8: Figures and Tables

Read `modules/thesis-figures-cn/SKILL.md`. Produce `plan/图表清单.md`, figure sources in `figures/src/`, rendered PNGs, and the screenshot list for the user.

Exit when all agent-made figures and data charts render and every screenshot the user still owes is in 截图清单.md.

### Stage 9: QC and Review

Read `modules/thesis-qc-cn/SKILL.md`. Run `thesis_qc.py`, then the four-role review, then fix with the user.

Exit when the findings are fixed in the chapter files.

### Stage 10: Full Thesis Word

Read `modules/docx-editor-cn/SKILL.md` and build:

```bash
node modules/docx-editor-cn/scripts/md2docx_thesis.js <论文项目>/chapters -o <论文项目>/output/论文.docx [--format format.json]
```

The output is the full thesis, named `论文.docx`. Report the script's counts (chapters, figures, tables, formulas, screenshots still to insert). Tell the user to open the file in Word, update the TOC field, and check layout by eye; the script cannot verify visual layout. Cover pages, declarations, and school-specific front matter come from the school template.

### Word Handling Inside Stages

Read `modules/docx-editor-cn/SKILL.md` whenever a stage says to generate Word, when the user provides a `.docx` template, or when the user asks for document formatting.

Identify source content and destination template before editing. For `.doc` templates, convert to `.docx` first. Do not claim visual layout correctness unless render or visual verification succeeds.

## Hard Rules

- References come only from retrieved or user-provided records. Institutional requirements and template contents come from the user or the school's files.
- The thesis body is written as the finished, submitted thesis: test results, experiment data, and performance figures are written in final form, consistent with the requirements, the design, and each other.
- When the user has no project code, the system is designed from the confirmed outline and requirements and written as a completed, tested system; code snippets are written to match that design.
- Prefer Chinese for Chinese thesis deliverables.
- Keep final answers stage-aware: say what stage was completed, what artifact was produced, and what remains.
- When the user asks for the full workflow, execute the current stage, then ask whether to proceed to the next stage.
- Do not bypass the continuation question between major stages unless the user explicitly requests a continuous full run.
- In the thesis body, `【待补充：…】` is used only for facts only the user knows (names, school details, missing bibliographic fields); screenshots stay as image references for the user to capture.
- Do not claim the thesis will pass plagiarism or AIGC detection. QC reduces obvious problems; the school's system decides.

## Reference

Read `references/stage-handoff.md` when managing a multi-turn workflow, resuming from existing artifacts, or deciding what information must be carried from one child skill to the next.
