---
name: jaan-issue-report
description: Report bugs, feature requests, or skill issues to the jaan-to GitHub repo or save locally. Use when reporting plugin issues.
allowed-tools: Read, Glob, Grep, Bash(gh auth status *), Bash(gh issue create *), Bash(gh label create *), Bash(uname *), Bash(awk *), Bash(rm -f /tmp/jaan-issue-body-*), Bash(mkdir -p $JAAN_OUTPUTS_DIR/jaan-issues/*), Write($JAAN_OUTPUTS_DIR/jaan-issues/**), Edit($JAAN_LEARN_DIR/**), Edit(jaan-to/config/settings.yaml)
argument-hint: "<issue-description> [--type bug|feature|skill|docs] [--submit | --no-submit]"
disable-model-invocation: true
license: MIT
compatibility: Designed for Claude Code with jaan-to plugin. Requires jaan-init setup.
---

# jaan-issue-report

> Report issues to the jaan-to GitHub repo or save locally for manual submission.

## Context Files

Read these before execution:
- `${CLAUDE_PLUGIN_ROOT}/skills/jaan-issue-report/LEARN.md` - Plugin-side seed lessons
- `$JAAN_LEARN_DIR/jaan-to-jaan-issue-report.learn.md` - Project-side learned lessons
- `${CLAUDE_PLUGIN_ROOT}/skills/jaan-issue-report/template.md` - Issue body templates per type
- `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json` - Plugin version
- `${CLAUDE_PLUGIN_ROOT}/docs/extending/language-protocol.md` - Language resolution

## Input

**Arguments**: $ARGUMENTS

Parse from arguments:
1. **Issue description** — Free text describing the issue
2. **--type** — Issue type: `bug`, `feature`, `skill`, `docs`. Default: auto-detect from description or session context.
3. **--submit** — Force submit to GitHub (overrides saved preference)
4. **--no-submit** — Force local-only mode (overrides saved preference)

If neither `--submit` nor `--no-submit` is provided, submit mode is resolved in Step 1 via saved preference or smart detection.

If no arguments provided, proceed to session context scan (Step 0) or ask: "What issue would you like to report?"

---

# PHASE 1: Analysis (Read-Only)

## Pre-Execution Protocol

**MANDATORY** — Read and execute ALL steps in: `${CLAUDE_PLUGIN_ROOT}/docs/extending/pre-execution-protocol.md`
Skill name: `jaan-issue-report`
Execute: Step 0 (Init Guard) → A (Load Lessons) → B (Resolve Template) → C (Offer Template Seeding)

**MANDATORY FIRST ACTION** — Before any other step, use the Read tool to read:
`$JAAN_LEARN_DIR/jaan-to-jaan-issue-report.learn.md`

If the file exists, apply its lessons throughout this execution:
- Add questions from "Better Questions" to Step 3
- Note edge cases to check from "Edge Cases"
- Follow workflow improvements from "Workflow"
- Avoid mistakes listed in "Common Mistakes"

If the file does not exist, continue without it.

Also read the plugin-side seed lessons:
`${CLAUDE_PLUGIN_ROOT}/skills/jaan-issue-report/LEARN.md`

### Language Settings

Read and apply language protocol: `${CLAUDE_PLUGIN_ROOT}/docs/extending/language-protocol.md`
Override field for this skill: `language_jaan-issue-report`

**CRITICAL LANGUAGE RULE:**
- **Conversation** (questions, confirmations, status messages, HARD STOP prompts): Use the resolved language preference
- **Issue output** (title + body): **ALWAYS in English** regardless of conversation language. GitHub issues target English-speaking maintainers.

**Keep in English always**: technical terms, file paths, variable names, skill names, code snippets, error messages.

---

## Tone and Framing Guidance

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/jaan-issue-report-reference.md` section "Tone and Framing Guidance" for problem-focused, suggestive tone principles (gathering, drafting, reviewing).

---

## Step 0: Session Context Scan (Smart Pre-Draft)

**This step runs ONLY when the skill is invoked mid-session** (not as the first command). If no useful session context is found, skip to Step 1.

Scan the current conversation history silently:

### 0.1 Detect Active Skills

Look for `/jaan-to:*` invocations in the conversation. Identify which skill(s) were used this session and what they produced.

### 0.2 Detect Errors and Frustrations

Search for patterns:
- Error messages, failed tool calls, unexpected output
- User expressions: "doesn't work", "wrong output", "expected X got Y", "broken", "bug", "missing"
- Repeated retries of the same action
- Skill output that didn't match expectations

### 0.3 Extract Key Signals

From the conversation, extract:
- **Skill name + command** used when the issue occurred
- **What the user was trying to accomplish**
- **What went wrong** (error, wrong output, missing feature, unexpected behavior)
- **Any workarounds** the user tried

### 0.4 Generate Suggested Draft

If signals were found:
- Auto-classify type: `bug` if errors found, `feature` if user expressed a wish, `skill` if skill-specific
- Draft a title (English, under 80 chars, `[Type] description`)
- Draft a 2-3 sentence description based on session signals
- Pre-fill template fields where possible (related skill, steps to reproduce)

**Present to user** using AskUserQuestion (in their conversation language):

Show the draft context first:
> "Based on this session, it looks like you experienced an issue with `/jaan-to:{skill-name}`:
>
> **Observed issue:** {draft title}
> {draft description — 2-3 sentences describing what went wrong}"

Then ask:
```
AskUserQuestion:
  question: "Is this what you'd like to report?"
  header: "Draft"
  options:
    - label: "Yes, report this"
      description: "Continue with this draft. Only deepening questions will be asked."
    - label: "No, something else"
      description: "Discard this draft and start fresh."
    - label: "Close, let me adjust"
      description: "Edit the draft before continuing."
```

- **Yes, report this**: Continue to Step 1 with draft pre-filled. Step 3 will ask only deepening questions.
- **No, something else**: Discard draft, proceed to Step 1 with standard flow.
- **Close, let me adjust**: User modifies the draft, then continue to Step 1 with the adjusted version.

---

## Step 1: Resolve Submit Mode

Determine submit mode using this priority order:

### 1.1 Check for explicit flags (highest priority)

- If `--submit` flag is present: set submit mode = **submit**. Proceed to 1.4.
- If `--no-submit` flag is present: set submit mode = **local-only**. Skip to Step 2.

### 1.2 Check saved preference

Read `jaan-to/config/settings.yaml` and look for the `issue_report_submit` key.

- If `issue_report_submit: true`: set submit mode = **submit**. Proceed to 1.4.
- If `issue_report_submit: false`: set submit mode = **local-only**. Skip to Step 2.
- If key is missing or `"ask"`: proceed to 1.3.

### 1.3 Smart detection (default: submit)

1. Run `gh auth status` silently.
2. If `gh` is **not available or not authenticated**:
   > "GitHub CLI is not installed or not authenticated. Issues will be saved locally. You can submit them manually later."
   Set submit mode = **local-only**. Skip to Step 2. Do NOT save this as a preference (user may install gh later).
3. If `gh` **is authenticated**: Set submit mode = **submit**. Proceed to 1.4.
   No question asked — submit is the default. Users can opt out with `--no-submit` or by setting `issue_report_submit: false` in `jaan-to/config/settings.yaml`.

### 1.4 Verify gh availability (for submit mode)

If submit mode is **submit** (from any source):

1. Run `gh auth status` to verify GitHub CLI is still installed and authenticated.
2. If **available**: Confirm submit mode is active.
3. If **not available**: Inform user in their conversation language:
   > "GitHub CLI is not installed or not authenticated. Your issue will be saved locally instead. You can submit it manually later."
   Override to local-only mode.

---

## Step 2: Classify Issue Type

Determine issue type using this priority order:

1. **From `--type` flag** (if provided): use directly
2. **From session draft** (if accepted in Step 0): use the auto-classified type
3. **From keyword detection** in the description:

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/jaan-issue-report-reference.md` section "Keyword Detection Table (Step 2)" for keyword-to-type mapping and type-to-label mapping.

4. **If uncertain**, ask using AskUserQuestion with options: Bug, Feature, Skill, Docs.

---

### Tone Guidance for Questions

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/jaan-issue-report-reference.md` section "Tone and Framing Guidance" for problem-focused question framing and smart auto-conversion.

## Step 3: Gather Details

Ask targeted clarifying questions to build a complete, detailed issue. **If a session draft was accepted in Step 0, only ask deepening questions** — don't re-ask what's already captured from the conversation.

### For `bug` type:
1. "Which skill or feature were you using?" (skip if known from session)
2. "What were you trying to accomplish?"
3. "What outcome did you expect?"
4. "What actually happened instead?"
5. "Can you share any error messages or unexpected output?" (skip if captured from session)
6. "What are the steps to reproduce this issue?"
7. "Does this occur consistently or intermittently?"

**Smart synthesis:** Focus bug description on the problem (broken functionality, unexpected behavior) and impact (workflow blocked, wrong results) rather than just error text.

### For `feature` type:
1. "What problem are you experiencing or trying to address?"
2. "What outcome would you like to achieve?"
3. "Can you describe a concrete situation where this problem occurs?"
4. "How does this problem impact your workflow or results?"
5. "Are there related existing skills or features you've tried?"

**Smart auto-conversion:** If user describes a solution ("Add support for X"), extract the problem:
- Ask: "That's a helpful idea. What problem would that solve?"
- Ask: "What outcome are you trying to achieve?"
- Synthesize: User wants to achieve [outcome] but currently experiences [problem]

### For `skill` type:
1. "Which skill is affected? Or describe the new skill you need?" (skip if known from session)
2. "What challenge or limitation are you facing?"
3. "What is the current behavior or what's missing?"
4. "What outcome would address this challenge?"
5. "How does this impact your workflow or productivity?"
6. "Can you share an example scenario showing the problem?"

**Smart synthesis:** Frame skill issues around the gap (missing capability, unexpected behavior) and its impact, not the solution (new skill, modified output).

### For `docs` type:
1. "Which documentation page or section?"
2. "What's incorrect, missing, or confusing?"
3. "What were you trying to accomplish when you encountered this issue?"
4. "What information or clarity would have helped you?"

**Smart synthesis:** Focus on the knowledge gap (what was unclear, what was missing) and the user's goal, not the specific documentation fix.

**Always ask** (for all types): "Is there anything else that would help understand this issue?"

**Skip questions the user already answered** in their initial description or session context.

---

## Step 4: Collect Environment Info

Auto-collect without user interaction:

1. Read `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json` — extract `version` field
2. Run `uname -s -r -m` — extract OS type and architecture (do NOT include hostname)
3. Note the related skill name from Step 0/Step 3 (if identified)

Store as environment data for the issue body.

## Step 4.5: Input Threat Scan

Scan accumulated issue content (title draft + gathered details) for threat patterns. Strip hidden characters.
> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/threat-scan-reference.md` for pattern tables and verdict actions.

---

## Step 5: Generate Issue Title

Craft a clear, descriptive title. **Always in English.** Pattern: `[{Type}] {concise description}` (under 80 chars).

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/jaan-issue-report-reference.md` section "Issue Title Format (Step 5)" for full rules and examples.

---

## Step 6: Generate Issue Body

Read the template from `${CLAUDE_PLUGIN_ROOT}/skills/jaan-issue-report/template.md`.

Select the matching type template (bug / feature / skill / docs) and fill all `{{field}}` variables using:
- User's answers from Step 3
- Session context signals from Step 0 (if available)
- Environment info from Step 4

Merge all sources into a coherent, well-structured issue body. **All issue body content must be in English.**

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/jaan-issue-report-reference.md` section "Variable Mapping (Tone-Aware)" for complete field mapping per issue type (bug, feature, skill, docs), smart auto-conversion rules, and tone reminders.

---

## Step 7: Privacy Sanitization

**MANDATORY before HARD STOP preview.** Scan the generated issue body for private information:

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/jaan-issue-report-reference.md` section "Privacy Sanitization Rules" for path, credential, and personal info sanitization rules, safe-to-keep list, and counting requirements.

Apply all sanitization rules. Track the number of sanitized items for HARD STOP display.

---

# HARD STOP — Issue Review

Present the complete issue preview:

```
ISSUE PREVIEW
──────────────────────────────────────────
Repo:    parhumm/jaan-to
Type:    {type}
Label:   {label}
Title:   {title}
Mode:    {Submit to GitHub / Save locally}

BODY:
──────────────────────────────────────────
{full issue body — every line}
──────────────────────────────────────────
```

If items were sanitized in Step 7, flag:
> "For privacy, {N} path(s)/value(s) have been sanitized with placeholders. Please review the preview carefully to ensure the issue description remains clear and complete."

Ask using AskUserQuestion (in the user's conversation language):
```
AskUserQuestion:
  question: "Does this look correct?"
  header: "Approve"
  options:
    - label: "Yes, looks good"
      description: "Proceed to save and/or submit the issue"
    - label: "No, abort"
      description: "Cancel — nothing will be saved or submitted"
    - label: "Edit"
      description: "Make changes to the issue before proceeding"
```

- **Yes**: Proceed to Phase 2
- **No**: Abort, nothing saved
- **Edit**: User provides changes → revise body, re-run sanitization, show preview again

**Do NOT proceed to Phase 2 without explicit approval.**

---

# PHASE 2: Generation (Write Phase)

## Step 8: Generate Output Path

Generate `NEXT_ID`, `SLUG`, `OUTPUT_FOLDER`, and `MAIN_FILE` for potential local save.

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/jaan-issue-report-reference.md` section "Output Path Generation (Step 8)" for the full bash script and variable definitions.

## Step 9: Submit to GitHub (if submit mode is active)

If submit mode is **local-only** (as resolved in Step 1), skip this step entirely and proceed to Step 10.

If submit mode is **submit**:

### 9.1 Prepare Issue Body

Write the sanitized issue body (without YAML frontmatter) directly to a temp file:

```bash
cat > /tmp/jaan-issue-body-clean.md <<'EOF'
{full issue body content — generated in Step 6, sanitized in Step 7}
EOF
```

### 9.2 Create Label (best effort)

```bash
gh label create "{label}" --repo parhumm/jaan-to --description "{description}" 2>/dev/null || true
```

### 9.3 Create Issue

```bash
gh issue create --repo parhumm/jaan-to \
  --title "{title}" \
  --label "{label}" \
  --body-file /tmp/jaan-issue-body-clean.md
```

### 9.4 Clean Up Temp File

```bash
rm -f /tmp/jaan-issue-body-clean.md
```

### 9.5 Handle Result

**If successful:**
1. Capture the returned issue URL (e.g., `https://github.com/parhumm/jaan-to/issues/123`)
2. Extract issue number from URL
3. Store both for Step 11 confirmation
4. **Skip Step 10 entirely** — proceed directly to Step 11 (do NOT create local file)

**If failed** (authentication error, network issue, API error):
1. Capture error message
2. Continue to Step 10 to handle local copy options

---

## Step 10: Handle Local Copy (conditional)

**This step is reached in two scenarios:**
1. Submit mode is **local-only** (GitHub was never attempted)
2. Submit mode was **submit** but GitHub submission failed in Step 9

**This step is SKIPPED if:**
- GitHub submission succeeded in Step 9 (proceed directly to Step 11)

### 10.1 Show Copy-Paste Ready Version

Present the issue title and body in a copy-paste ready format with contextual message (different for GitHub failure vs. local-only mode).

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/jaan-issue-report-reference.md` section "Copy-Paste Ready Template (Step 10.1)" for the exact format and contextual messages.

### 10.2 Ask About Local File

Use AskUserQuestion (in the user's conversation language):

```
AskUserQuestion:
  question: "Would you like to save a local copy of this issue as a file?"
  header: "Save file"
  options:
    - label: "Yes, save local copy"
      description: "Save the issue as a .md file with metadata for future reference"
    - label: "No, skip"
      description: "Don't create a file — use the copy-paste version above instead"
```

### 10.3 Save Local File (if user chooses "Yes")

If user selected **"Yes, save local copy"**:

#### 10.3.1 Create Folder Structure

```bash
mkdir -p "$OUTPUT_FOLDER"
```

#### 10.3.2 Write Issue File

Write to `$MAIN_FILE` (the path generated in Step 8) with YAML frontmatter (metadata) followed by the full issue body.

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/jaan-issue-report-reference.md` section "Local Issue File Template (Step 10.3.2)" for the complete file format and frontmatter fields.

#### 10.3.3 Update Index

```bash
source "${CLAUDE_PLUGIN_ROOT}/scripts/lib/index-updater.sh"
add_to_index \
  "$SUBDOMAIN_DIR/README.md" \
  "$NEXT_ID" \
  "${NEXT_ID}-${SLUG}" \
  "{title}" \
  "{one-line summary}"
```

Confirm:
> "Local copy saved to: `$JAAN_OUTPUTS_DIR/jaan-issues/{NEXT_ID}-{SLUG}/{NEXT_ID}-{SLUG}.md`"

### 10.4 Skip Local File (if user chooses "No")

If user selected **"No, skip"**:
- Do NOT create any folders or files
- Do NOT update the index
- Proceed directly to Step 11

---

## Step 11: Confirm Result

Show the appropriate result message in the user's conversation language.

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/jaan-issue-report-reference.md` section "Result Scenario Templates (Step 11)" for all 5 scenarios (A: GitHub success, B: Local+file, C: Local+no file, D: GitHub fail+file, E: GitHub fail+no file).

## Step 12: Capture Feedback

```
AskUserQuestion:
  question: "Any feedback on this issue reporting experience?"
  header: "Feedback"
  options:
    - label: "No feedback"
      description: "All good, skip feedback"
    - label: "Yes, I have feedback"
      description: "Share feedback to improve this skill"
```

If **Yes, I have feedback**: ask for details, then run `/jaan-to:learn-add jaan-issue-report "{feedback}"`

---

## Skill Alignment

- Two-phase workflow with HARD STOP for human approval
- Single source of truth (no duplication)
- Plugin-internal automation
- Maintains human control over changes

## Definition of Done

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/jaan-issue-report-reference.md` section "Definition of Done" for the full checklist.
