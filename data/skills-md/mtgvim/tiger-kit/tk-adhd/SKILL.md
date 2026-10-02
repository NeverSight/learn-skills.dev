---
name: tk-adhd
description: "[user/auto] 세션을 오가다 현재 작업의 맥락을 놓쳤거나 지금 어디까지 했는지 짧게 확인하고 턴을 끝낼 때 사용합니다. 코드 동작 설명, 원격 PR 현황 조사, 스킬 자체 수정, 인수인계 파일 작성에는 사용하지 않습니다."
disable-model-invocation: false
argument-hint: "[현재 작업 | 제공한 세션 요약]"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: adapted
---

# Session Orientation

Restore the reader's place in the current task, using only this conversation and evidence already available. If repository or branch identity is needed and not established, use one cheap read of current Git state. Do not investigate implementation details, enumerate other sessions/worktrees/repositories, or query remote PRs for a status recap. A requested comparison may use summaries the user supplied, with unknown or stale state labeled explicitly; never merge their goals or approvals.

Give one compact card in the user's language; for a requested comparison, give one labeled card per supplied session. Translate the field labels to that language. Prefer these five short lines, omitting an empty field rather than filling a quota:

```text
📍 <repository / branch when known> · <task goal>
완료: <latest verified outcome, or no verified completion yet>
지금: <paused task position or exact blocker>
다음: <one suggested action after the user resumes, not an action started now; or completed>
내가 할 일: <only required user action, or 없음>
```

Distinguish executed work from a plan, capture success from final verification, and local commits from confirmed publication. If context is missing, say what is unknown; ask only for the minimal task identifier needed for a useful answer. Do not invent percentages, timings, completed tests, or access to other sessions. Never infer medical status from this request.

A status request pauses task execution for orientation. Present the card as the final response and end the turn, even when an earlier task approval includes implementation, verification, commits or publication. Do not resume that work, dispatch workers, start checks, or schedule background continuation after the card. The next-action line is a suggestion for later, not execution authority. Wait for a subsequent user instruction to resume; do not add a routine approval question. This explicit reporting boundary takes precedence over an owner's ordinary phase-continuation rule. It does not revoke earlier scope approval: a later resume instruction can reuse it when the task still matches. This format does not persist to every future reply or truncate a requested detailed explanation.

Create no status ledger or handoff file, mutate no repository/remote state for the recap, and grant no additional authority. Durable handoff creation/resume belongs to `tk-handoff`; this skill only restores conversational orientation.

<!-- tigerkit:artifact-paths -->
## Artifact Paths

This skill creates no artifacts. Do not create temporary files, write reports, or edit ignore rules for this invocation; return the result in the conversation.

<!-- tigerkit:output-notation -->
## Output Notation

Use ASCII numbering such as `(1) Item` or `1. Item`, with a space after the marker, in generated headings, lists, choices, tables, diagrams, and summaries. Use `- Item` for unordered items. Do not generate Unicode circled/enclosed numbers, single-character parenthesized numbers, or keycap emoji as item markers; they can overlap adjacent text in terminal renderers. Preserve exact code, commands, URLs, quotations, identifiers, and verified UI labels unless explicitly authorized to edit them; apply this rule to the surrounding explanation instead.

For an authorized user-editable temporary input file, consistently provide a plain JSON object template with the needed keys and empty strings for missing text values, rather than an empty or raw-text file. The initial template's non-zero size is not an input-completion signal. Apply the owning package's Artifact Paths input branch before creation and consumption; this notation rule grants no artifact-writing authority.
<!-- /tigerkit:output-notation -->

<!-- tigerkit:questions -->
## User Questions

Before sending any user-owned clarification, choice, or approval, read [question rounds](references/questions.md) in this turn. Ask the whole answerable frontier in one plain-chat round; resolve facts first, preserve existing authorization, and skip question ceremony when no decision remains. Do not use question tools for ordinary TigerKit questions.

Minimum shape, even when already familiar:

```text
❓ **Q1 · <short title>**: <question and relevant choices>

➡️ <recommendation and reason, when supported>
```

Separate questions with `---`. Put context before the question block and make it the final substantive block: no plan, promise, or “answer and I will proceed” line afterward, except one short reply-format hint. An approval request is its own numbered `Q`, never buried in the proposal. Defer approval whose scope still depends on an unresolved answer.
<!-- /tigerkit:questions -->
