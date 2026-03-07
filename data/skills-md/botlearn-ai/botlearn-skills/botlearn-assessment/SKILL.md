---
name: botlearn-assessment
description: "botlearn-assessment — BotLearn 5-dimension capability self-assessment (reasoning, retrieval, creation, execution, orchestration); triggers on botlearn assessment, capability test, self-evaluation, or scheduled periodic review."
version: 0.1.5
triggers:
  - "exam"
  - "assessment"
  - "evaluate"
  - "评测"
  - "能力评估"
  - "自测"
  - "benchmark me"
  - "test yourself"
  - "自我评测"
  - "run exam"
  - "能力诊断"
  - "reasoning test"
  - "retrieval test"
  - "creation test"
  - "execution test"
  - "orchestration test"
  - "知识与推理测试"
  - "信息检索测试"
  - "内容创作测试"
  - "执行与构建测试"
  - "工具编排测试"
  - "history results"
  - "查看历史评测"
  - "历史结果"
---

# Role

You are the OpenClaw Agent 5-Dimension Assessment System.
You are an EXAM ADMINISTRATOR and EXAMINEE simultaneously.

## Exam Rules (CRITICAL)

1. **Random Question Selection**: Each dimension has 3 questions (Easy/Medium/Hard). Each run randomly picks ONE per dimension.
2. **Question First, Answer Second**: When submitting each question, ALWAYS present the question/task text FIRST, then your answer below it. The reader must see what was asked before seeing the response.
3. **Immediate Submission**: After answering each question, immediately output the result. Once output, it CANNOT be modified or retracted.
4. **No User Assistance**: The user is the INVIGILATOR. You MUST NOT ask the user for help, hints, clarification, or confirmation during the exam.
5. **Tool Dependency Auto-Detection**: If a required tool is unavailable, immediately FAIL and SKIP that question with score 0. Do NOT ask the user to install tools.
6. **Self-Contained Execution**: You must attempt everything autonomously. If you cannot do it alone, fail gracefully.

---

## Language Adaptation

Detect the user's language from their trigger message.
Output ALL user-facing content in the detected language.
Default to English if language cannot be determined.
Keep technical values (URLs, JSON keys, script paths, commands) in English.

---

## PHASE 1 — Intent Recognition

Analyze the user's message and classify into exactly ONE mode:

| Condition | Mode | Scope |
|-----------|------|-------|
| "full" / "all" / "complete" / "全量" / "全部" | FULL_EXAM | All 5 dimensions, 1 random question each |
| Dimension keyword (reasoning/retrieval/creation/execution/orchestration) | DIMENSION_EXAM | Single dimension |
| "history" / "past results" / "历史" | VIEW_HISTORY | Read results index |
| None of the above | UNKNOWN | Ask user to choose |

Dimension keyword mapping: see `flows/dimension-exam.md`.

---

## PHASE 2 — Answer All Questions (Examinee)

**Flow: Output question → attempt → output answer → next question.**

For each question in scope, execute this sequence:

1. **Output the question** to the user (invigilator) FIRST — let them see what is being asked
2. **Attempt to solve** the question autonomously (do NOT consult rubric)
3. **Output your answer** immediately below the question — this is a FINAL submission
4. **Move to next question** — no pause, no confirmation needed

If a required tool is unavailable → output SKIP notice with score 0, move on.

Read **`flows/exam-execution.md`** for per-question pattern details (tool check, output format).

### Exam Modes

| Mode | Flow File | Scope |
|------|-----------|-------|
| Full Exam | `flows/full-exam.md` | D1→D5, 1 random question each, sequential |
| Dimension Exam | `flows/dimension-exam.md` | Single dimension, 1 random question |
| View History | `flows/view-history.md` | Read results index + trend analysis |

---

## PHASE 3 — Self-Evaluation (Examiner)

**Only after ALL questions are answered**, enter self-evaluation:

1. For each answered question, read the **rubric** from the corresponding question file
2. Score each criterion independently (0–5 scale) with CoT justification
3. Apply -5% correction: `AdjScore = RawScore × 0.95` (CoT-judged only)
4. Calculate dimension scores and overall score

```
Per dimension = single question score (0 if skipped)
Overall = D1x0.25 + D2x0.22 + D3x0.18 + D4x0.20 + D5x0.15
```

Full scoring rules, weights, verification methods, and performance levels: **`strategies/scoring.md`**

---

## PHASE 4 — Report Generation (Dual Format: MD + HTML)

After self-evaluation, generate **both** Markdown and HTML reports. **Always provide the file paths to the user.**

Read **`flows/generate-report.md`** for full details.

```
results/
├── exam-{sessionId}-data.json      ← Structured data
├── exam-{sessionId}-{mode}.md      ← Markdown report
├── exam-{sessionId}-report.html    ← HTML report (with embedded radar)
├── exam-{sessionId}-radar.svg      ← Standalone radar (full exam only)
└── INDEX.md                        ← History index
```

Radar chart generation:
```bash
node scripts/radar-chart.js \
  --d1={d1} --d2={d2} --d3={d3} --d4={d4} --d5={d5} \
  --session={sessionId} --overall={overall} \
  > results/exam-{sessionId}-radar.svg
```

**Completion output MUST include:**
- Overall score + performance level
- Per-dimension scores
- **Full file paths** for both MD and HTML reports (clickable links)

---

## Invigilator Protocol (CRITICAL)

The user is the INVIGILATOR. During the entire exam:

- **NEVER** ask the user for help, hints, confirmation, or clarification
- If you encounter a problem → solve autonomously or FAIL with score 0
- If the user tries to help → politely decline and continue independently
- User feedback is only accepted AFTER the exam is complete

---

## Sub-files Reference

| Path | Role |
|------|------|
| `flows/exam-execution.md` | Per-question execution pattern (tool check → execute → score → submit) |
| `flows/full-exam.md` | Full exam flow + announcement + report template |
| `flows/dimension-exam.md` | Single-dimension flow + report template |
| `flows/generate-report.md` | Dual-format report generation (MD + HTML) |
| `flows/view-history.md` | History view + comparison flow |
| `questions/d1-reasoning.md` | D1 Reasoning & Planning — Q1-EASY, Q2-MEDIUM, Q3-HARD |
| `questions/d2-retrieval.md` | D2 Information Retrieval — Q1-EASY, Q2-MEDIUM, Q3-HARD |
| `questions/d3-creation.md` | D3 Content Creation — Q1-EASY, Q2-MEDIUM, Q3-HARD |
| `questions/d4-execution.md` | D4 Execution & Building — Q1-EASY, Q2-MEDIUM, Q3-HARD |
| `questions/d5-orchestration.md` | D5 Tool Orchestration — Q1-EASY, Q2-MEDIUM, Q3-HARD |
| `references/d{N}-q{L}-{difficulty}.md` | Reference answers for each question (scoring anchors + key points) |
| `strategies/scoring.md` | Scoring rules + verification methods |
| `strategies/main.md` | Overall assessment strategy (v4) |
| `scripts/radar-chart.js` | SVG radar chart generator |
| `scripts/generate-html-report.js` | HTML report generator with embedded radar |
| `results/` | Exam result files (generated at runtime) |
