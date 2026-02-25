---
name: perplexity
description: "AI-powered search and chat with Perplexity. Use when you need to: (1) get AI responses with real-time web search, or (2) answer questions with up-to-date information."
version: 1.0.0
skillId: skp-rkmnjbtpxxpidhck89q60yvt
workflowId: c-xz42o3itzw4bdnnhoovb16dv
installationId: skpi-sww12wxvy9zbfr1wwx35gybm
category: text-data
---

# Perplexity

AI-powered search and chat with Perplexity. Use when you need to: (1) get AI responses with real-time web search, or (2) answer questions with up-to-date information.

## Input

Provide input as JSON:

```json
{
  "query": "Your search query or question"
}
```

## Execution

### Step 1: Run the Skill

```bash
refly skill run --id skpi-sww12wxvy9zbfr1wwx35gybm --input '{
  "query": "Your question here"
}'
```

### Step 2: Wait for Completion

```bash
refly workflow status c-xz42o3itzw4bdnnhoovb16dv --watch --interval 10000
```

### Step 3: Get the Run ID

```bash
refly workflow runs c-xz42o3itzw4bdnnhoovb16dv --limit 1
```

Look for `runId` in the output (format: `we-xxx`).

### Step 4: Get the Result ID

```bash
refly workflow detail <RUN_ID>
```

Look for `resultId` in the `skillResponse` node (format: `ar-xxx`).

### Step 5: Extract the Content

```bash
refly workflow result <RESULT_ID> --include-messages --raw
```

The AI response is in `.payload.messages[]` where `type` is `"ai"`. Extract with:

```bash
refly workflow result <RESULT_ID> --include-messages --raw | jq -r '.payload.messages[] | select(.type=="ai") | .content'
```

### Alternative: One-liner (after Step 2)

```bash
RUN_ID=$(refly workflow runs c-xz42o3itzw4bdnnhoovb16dv --limit 1 | jq -r '.payload.runs[0].runId') && \
RESULT_ID=$(refly workflow detail "$RUN_ID" | jq -r '.payload.nodes[] | select(.nodeType=="skillResponse") | .resultId') && \
refly workflow result "$RESULT_ID" --include-messages --raw | jq -r '.payload.messages[] | select(.type=="ai") | .content'
```

## Key Concepts

| ID Type | Format | How to Get | Used For |
|---------|--------|------------|----------|
| workflowId | `c-xxx` | In SKILL.md frontmatter | `workflow status`, `workflow runs` |
| runId | `we-xxx` | From `workflow runs` or `workflow status` output | `workflow detail`, `workflow toolcalls` |
| resultId | `ar-xxx` | From `workflow detail` → nodes[].resultId | `workflow result` |

## Common Mistakes to Avoid

### Do NOT use `toolcalls` with `.output.preview`

```bash
# WRONG - This will fail!
refly workflow toolcalls <RUN_ID> --latest | jq -r '.payload.toolCalls[-1].output.preview | fromjson | .data.response'
```

**Why it fails:**
- `.output.preview` may be `null` → jq error: `null (null) only strings can be parsed`
- `.output.preview` may be truncated → jq error: `Unfinished string at EOF`
- The preview field is not guaranteed to exist

**Always use this instead:**
```bash
refly workflow result <RESULT_ID> --include-messages --raw | jq -r '.payload.messages[] | select(.type=="ai") | .content'
```

## Expected Output

- **Type**: Text content with citations
- **Format**: AI-generated response from Perplexity with web search results
- **Action**: Display content to user
