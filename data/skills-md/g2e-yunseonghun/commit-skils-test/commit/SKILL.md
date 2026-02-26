---
name: commit
description: 'Automates git commits with WBS tracking and code review. Use when user wants to commit changes or needs commit message suggestions. Keywords: commit, 커밋, 커밋해줘, 커밋 메시지, git commit, WBS, 리뷰'
---

# Commit Automation with WBS & Review

## Purpose

Automate git commit workflow with:

- WBS (Work Breakdown Structure) number tracking
- Automated code review based on diff
- Structured commit message generation
- Interactive commit execution

**IMPORTANT: Always communicate with the user in Korean (한국어) throughout the entire workflow.**

## Trigger Conditions

### When to activate this skill:

- 커밋해줘 / 커밋 쳐줘 / 커밋 올려줘
- 커밋 메시지 만들어줘 / 커밋메시지 / 커밋 메세지
- git commit / commit message / 커밋 메시지 추천
- "WBS 1234로 커밋" (WBS + commit mention)
- "메시지만" (message generation only, no commit execution)

### When NOT to activate:

- Simple git concept questions (e.g., "커밋이 뭐야?")

---

## Workflow

**Performance Note:** Cache git command results throughout the workflow. Do not re-run `git status`, `git diff`, or `git log` if already executed in previous steps.

### Step 0: WBS Selection

**If user provided WBS number in the request:**

- Parse patterns:
  - Single: "WBS 123", "WBS-123", "123으로 커밋", "커밋 123", "/commit 123"
  - Multiple: "13, 14로 커밋", "커밋 13 14", "/commit 13, 14"
- Extract number(s) from the request:
  - Single number → format as `WBS-<number>` (e.g., 1234 → WBS-1234)
  - Multiple numbers → split by comma/space, format each, join with ", " (e.g., "13, 14" → WBS-13, WBS-14)
- **IMPORTANT:** Skip selection UI and proceed directly to Step 1 with the extracted WBS number(s)

**If NO WBS number provided:**

1. **Run** `git log -1 --pretty=%B` to get the most recent commit message
   - This is more reliable than reading `.git/COMMIT_EDITMSG` (works correctly during amend/rebase)
   - If this fails, fallback to reading `.git/COMMIT_EDITMSG`
2. Parse "Context:" section to extract WBS number from the most recent commit
3. Extract the commit subject (first line) as the task description
4. If WBS found (not "N/A"), prepare it as the previous WBS option with format: "WBS-XX (commit subject)"
5. Present selection UI:

```
========================================
WBS 작업 선택:
========================================
1. 직접입력
2. WBS 없음 (N/A)
[3: Previous WBS if found, e.g., "3. WBS-48 (이전 커밋 제목)"]
4. 취소
========================================
선택 (숫자 입력):
```

6. **MANDATORY:** Wait for user selection. Do NOT auto-select or assume any option based on previous commits.

**Handle user selection:**

- **Option 1 (직접입력):** Prompt for WBS number:

  ```
  WBS 작업 번호를 입력해주세요:
  - 단일: 1234
  - 여러 개: 13, 14 또는 13 14
  - 없음: '없음' 입력
  ```

  - If "없음" or empty → set WBS to "N/A"
  - Otherwise → parse input:
    - Split by comma or space (e.g., "13, 14" or "13 14")
    - Format each as `WBS-<number>`
    - Join with ", " → `WBS-13, WBS-14`

- **Option 2 (WBS 없음):** Set WBS to "N/A" and proceed

- **Option 3 (Previous WBS):** Use the previous WBS number extracted from git log

- **Option 4 (취소):** Exit workflow without proceeding

**Important:** Never invent or guess WBS numbers.

---

### Step 1: Inspect Changes

1. **MUST run** `git status -sb` to get branch and file status
2. **MUST run** diff commands:
   - First try: `git diff --staged`
   - If empty, try: `git diff`
3. Summarize changes in 3-5 lines (what files changed, what kind of changes)

**Commit Split Detection:**
If changes span multiple unrelated domains, suggest splitting:

- Backend vs Frontend
- Feature vs Refactor
- Logic vs Formatting
- Dependencies vs Business code

**If split is recommended:**

1. Explain split criteria and reasoning
2. List files for each commit unit
3. Wait for user approval
4. On approval:
   - Stage first unit → `git add <files>`
   - Continue with Step 2-6 for first unit
   - Repeat for remaining units
5. If user says "just do it all at once" → proceed as single commit

---

### Step 2: Code Review

**Diff Scope Rule (Mandatory):**

- Review ONLY lines added/removed in the current diff
- Inspect minimal surrounding context
- Do NOT audit unrelated existing code
- Ignore legacy technical debt not introduced by this change
- Do NOT suggest architectural refactors unrelated to this diff

**Review Checklist:**

1. **Potential bugs:**
   - Null/undefined handling
   - Edge cases
   - Error handling
   - Broken logic

2. **Debug leftovers:**
   - console.log / print / System.out.println
   - TODO / FIXME comments

3. **Security issues:**
   - Hard-coded secrets/tokens
   - Sensitive data in logs
   - SQL injection / XSS vulnerabilities

4. **Code quality:**
   - Code duplication
   - Poor naming
   - Overly large functions/files

5. **Unintended changes:**
   - Unrelated formatting changes
   - Stray files
   - Generated artifacts (build outputs, lock files if not intended)

---

### Step 3: Review Output

Present review results in Korean using this format:

```markdown
### 🔍 변경 요약

- [Brief summary of changes]

### ⚠️ 리스크 / 주의점

- [Identified risks or concerns, or "없음" if none]

### 🛠️ 개선 제안

- [Specific suggestions with file:line references, or "없음" if none]

### ✅ 결론

- [리뷰 통과 | 수정 필요 | 커밋 분리 권장]
```

---

### Step 4: Review Decision Branch

**If review result = "리뷰 통과":**

- Proceed to Step 5

**If review result = "수정 필요":**

- Do NOT generate commit message
- Show review output and instruct: "위 이슈를 수정한 뒤 다시 커밋을 요청해주세요."
- If user explicitly says "ignore and commit anyway" → proceed to Step 5

**If review result = "커밋 분리 권장":**

- Follow Commit Split Guide from Step 1
- Process each unit through Steps 2-6 separately

---

### Step 5: Generate Commit Message

**PRE-CHECK: Ensure WBS number has been set in Step 0 (including "N/A" for no WBS). If not set at all, return to Step 0 for user selection.**

1. **MUST read** `templates/commit-msg-template.md` from skill directory
   - This file contains the commit message format, emoji mapping, and all template rules
   - No user notification, silent check
   - Follow the template structure and emoji mapping exactly as defined in the file

2. Generate exactly **1 commit message** (best candidate only)

3. Do NOT run any git commands in this step

---

### Step 6: Commit Execution

**If trigger was "메시지만":**

- Display generated message and EXIT (skip commit execution)

**Otherwise, present commit UI:**

```
========================================
제안된 커밋 메시지:
========================================
[Display the generated commit message here]
========================================
1. 제안된 커밋 사용
2. 제안된 커밋 수정
3. 취소
========================================
선택 (1-3):
```

**Handle user selection:**

- **Option 1 (제안된 커밋 사용):**
  - Check if files are staged: `git diff --staged --name-only`
  - **IMPORTANT:** Escape double quotes and special characters in commit message before executing git commit
  - If staged files exist → **run** `git commit -m "..."`
  - If nothing staged → list unstaged files, ask user which to add, then **run** `git add <files>` → `git commit -m "..."`

- **Option 2 (제안된 커밋 수정):**
  - Prompt: "수정할 내용을 입력해주세요 (전체 커밋 메시지 또는 수정 지시):"
  - Wait for user input
  - Apply modifications to commit message
  - Commit with modified message

- **Option 3 (취소):**
  - Exit without committing

---

## Refinement Notes

**Why this design:**

1. **WBS tracking:** Company workflow requires linking commits to WBS tasks
2. **Automatic WBS suggestion:** Reduces friction by suggesting recent WBS numbers
3. **Mandatory review:** Prevents shipping debug code, secrets, or bugs
4. **Template flexibility:** Projects can override with custom templates
5. **Interactive selection:** Gives user control at each decision point
6. **"메시지만" mode:** Useful for learning or preparing messages before committing

**Tool usage patterns:**

- Silent execution for context gathering (git log)
- Explicit user prompts for decisions (WBS selection, commit execution)
- Structured output formats for consistency

**Error handling:**

- Never proceed if review fails (unless user overrides)
- Never invent WBS numbers
- Always confirm before staging/committing files
