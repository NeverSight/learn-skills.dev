---
name: study-quiz
description: >
  Quiz & assessment sub-skill (orchestrated by study-assistant; also usable standalone). Use when the learner uploads past papers/questions ("真题", 历年试卷, 样题), wants AI to search for school-style questions, asks to be tested ("出题" "考我" "测验" "模拟题" "来套模拟卷"), submits answers for grading, or asks to review mistakes. Maintains one course-level global question bank, prioritizes uploaded questions over web-sourced material, generates MathJax-capable interactive HTML quizzes, grades answers, updates mastery, and maintains the mistake book.
---

# Quizzing & Grading

**Output language: ALL learner-facing content MUST be Simplified Chinese.**

Never leak answers before the learner attempts. Durable quiz artifacts are files; conversation is for source-choice confirmation, grading, and next-step guidance.

## File and source standards

The question bank is course-level:

```bash
<study-dir>/question-bank/question-bank.json
```

Never create per-chapter banks. Legacy `<study-dir>/question-bank.json` is accepted only for old workspaces.

Generated files:

- quiz JSON: `<study-dir>/internal/quizzes/<date>-<topic>.json`
- learner HTML: `<study-dir>/open/quizzes/<date>-<topic>.html`, produced with `build_quiz.py --publish <study-dir>`
- exam profile: `<study-dir>/internal/state/exam-style.md`
- mistake book: `<study-dir>/internal/state/mistakes.md`
- reports: `<study-dir>/internal/reports/`

Quiz HTML supports LaTeX `$...$` / `$$...$$` through MathJax. Use LaTeX for real formulas; Unicode math is fine for short inline expressions.

## Source priority

1. User-uploaded real papers/questions are the gold standard.
2. If the user has not uploaded questions, ask whether they want to upload questions or let AI search the web.
3. If the user chooses web search, confirm school, subject/name/code, and year range first. Source priority: official syllabus/sample papers > prep-institution compilations > forum recollections.
4. Web-sourced material must carry URLs and confidence labels. If real papers arrive later, re-analyze and override web-sourced assumptions.

## Bank-first workflow

Before writing questions, inspect the bank:

```bash
python3 ~/.claude/skills/study-quiz/scripts/bank.py <study-dir> list --point 3.1.2 3.1.3
python3 ~/.claude/skills/study-quiz/scripts/bank.py <study-dir> stats --point 3.1.2 3.1.3
python3 ~/.claude/skills/study-quiz/scripts/bank.py <study-dir> get Q0003 Q0007
```

Prefer unused or least-used entries. For repeat practice, adapt numbers/scenarios instead of reusing verbatim. Write brand-new questions only for uncovered points or when uploaded/web sources add better exam-style material.

After building a quiz:

```bash
python3 ~/.claude/skills/study-quiz/scripts/bank.py <study-dir> add <quiz.json>
python3 ~/.claude/skills/study-quiz/scripts/bank.py <study-dir> use Q0003 Q0007
```

## Exam-style analysis

When uploaded or searched papers are available, write `internal/state/exam-style.md`:

```markdown
# 命题风格档案：<院校/科目>（来源：<真题年份 或 网络检索+URL+置信度>）
## 试卷结构
## 难度与风格特征
## 高频考点 → 教材章节映射
## 各题型出题模板与评分标准
## 典型真题摘录
```

Then update relevant `knowledge.json` point importance. Tell the learner the conclusions in one concise Chinese paragraph.

## Quiz generation

Default delivery is interactive HTML. Write quiz JSON using the schema in `build_quiz.py`, then render:

```bash
python3 ~/.claude/skills/study-quiz/scripts/build_quiz.py \
  <study-dir>/internal/quizzes/<quiz>.json --publish <study-dir>
```

Question types:

- `single`: options + integer answer index.
- `multi`: options + answer index list; default no partial credit unless `partial: true`.
- `judge`: true/false.
- `text`: subjective/calculation; requires `reference`.

Objective questions require `explanation`: why the right answer is right and why distractors are wrong. Text questions require point-by-point scoring criteria.

### Point or section reinforcement

Default 2-3 questions per point, easy -> hard. Use uploaded/source questions first, then bank entries, then new questions from lecture JSON. Without exam-style.md, use the subject's normal style.

### Chapter quiz

Cover at least 60% of the chapter's points and all high-importance points. Follow `exam-style.md` when present.

### Mistake-book review

Pick unresolved mistakes and re-ask them in disguise. Only a correct redo marks the mistake as `复盘通过`.

### Mock exam

When the learner asks for a full mock, follow the real structure, scoring, and time from `exam-style.md`. After grading, write `internal/reports/mock-<date>.md`.

## Delivery

Open or provide the path to the HTML in `open/quizzes/`. In conversation say one Chinese sentence: the quiz has opened, how many questions it has, and to export/paste the answer record after finishing. Do not repeat quiz questions in chat unless the learner explicitly asks for conversation-mode quizzing.

## Grading

Answers may arrive from exported HTML records, conversation, or handwritten photos. For handwritten work, invoke `study-img --mode answer`, transcribe verbatim, confirm uncertain `【?】`, then grade.

For each graded question, give verdict, score, correct answer, exact reasoning break, and mapped knowledge point.

After grading:

1. Update `internal/state/mistakes.md` for misses.
2. Update `knowledge.json`: status -> `已测验`, mastery 1-4 by performance, note = concrete weak spot.
3. Append `history.jsonl`, update `progress.json`, regenerate mind map, refresh dashboard.
4. If mastery <= 2, recommend re-teaching before advancing.
