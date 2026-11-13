---
name: start
description: Begin a new market research session. Thin launcher that delegates to the research-orchestrator agent for all phase management.
argument-hint: "[--quick] [--dimensions <dim,...> (competitive,sizing,trends,customer,tech,financial,regulatory,trend_modeling)] [<topic>]"
allowed-tools:
  - Agent
  - AskUserQuestion
  - Bash
  - Glob
  - Grep
  - Read
  - SendMessage
  - TaskCreate
  - TaskGet
  - TaskList
  - TaskUpdate
  - TeamCreate
  - TeamDelete
  - Write
---

# Sigint Start Skill (Launcher)

This skill initializes a research session and delegates to the `research-orchestrator` agent for all orchestration. The orchestrator owns team lifecycle, dimension-analyst spawning, codex review gates, finding merge, progress tracking, and cleanup.

## Arguments

Parse `$ARGUMENTS` before any other processing. **Input sanitization**: truncate `$ARGUMENTS` to 200 characters total, strip backticks and angle brackets.

- `--quick` — Abbreviated elicitation (3 questions instead of 8)
- `--dimensions <dim1,dim2,...>` — Optional: pre-select specific dimensions (comma-separated). Valid values: `competitive`, `sizing`, `trends`, `customer`, `tech`, `financial`, `regulatory`, `trend_modeling`. Passed to the orchestrator as `REQUESTED_DIMENSIONS` — Phase 1.5 skips interactive selection when this is set.
- Remaining text after flag extraction is the initial topic hint (may be empty)

---

## Phase 0.0: Preliminary Setup

### Step 0.0.1: Derive Preliminary Topic Slug

Parse `$ARGUMENTS` for a topic hint. Derive `topic_slug`: lowercase, replace spaces/special chars with hyphens, truncate to 40 characters. Use `"research"` if no topic hint. (Preliminary slug used for config lookup; may be refined during orchestrator elicitation.)

### Step 0.0.2: Apply Config Resolution Protocol

Execute the **Config Resolution Protocol**:
1. Read `protocols/CONFIG-RESOLUTION.md` and follow all steps.
2. Apply with `topic_slug` = {preliminary topic slug from Step 0.0.1}.
3. Result: `config`, `max_dimensions`, and `context_content` are now available.

**Config cascade clarification**: When loading config files, always apply the full cascade (project config values override global config values override hardcoded defaults) regardless of the config file's schema version. The version check in the protocol produces an advisory warning only — it does NOT cause config values to be discarded. If `sigint.config.json` sets `maxDimensions: 3`, then `max_dimensions = 3` even if the file's version field is not "2.0". Custom fields like `defaultPriorities` are preserved and passed through in the serialized config.

---

## Previous Research Detection

Before delegating, check if research already exists:
```
Glob("./reports/*/state.json")
```

If `./reports/{topic_slug}/state.json` exists:
- Load prior elicitation from state.json
- Ask: "Previous research found for '{topic}'. Use prior research context as starting point, or start completely fresh?"
- If "use prior": Pass `--resume-from={topic_slug}` context to orchestrator
- If "start fresh": Proceed normally (prior state.json will be overwritten after confirmation)

---

## Phase 0.1: Register Topic in Config

Register the research topic in `sigint.config.json` so that `/sigint:status`, `/sigint:resume`, and other commands can discover sessions from the config index.

Using jq (per Structured Data Protocol):
```bash
jq --arg slug "$TOPIC_SLUG" \
   --arg date "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
   --arg reports_dir "./reports/$TOPIC_SLUG" \
  '.topics[$slug] = (.topics[$slug] // {}) + {
     status: "in_progress",
     dimensions: [],
     created: ((.topics[$slug].created // null) // $date),
     updated: $date,
     reports_dir: $reports_dir,
     findings_count: 0
   }' \
  ./sigint.config.json > tmp.$$ && mv tmp.$$ ./sigint.config.json
jq -e -f schemas/sigint-config.jq ./sigint.config.json > /dev/null
```

This preserves any existing topic entry (merge mode) while setting the lifecycle fields. The `created` field is preserved if the topic was previously registered (e.g., from a prior session or `/sigint:migrate`).

---

## Phase 0.2: Delegate to Research Orchestrator

Spawn the research-orchestrator agent with full mode:

```
Agent(
  subagent_type="sigint:research-orchestrator",
  name="research-orchestrator",
  prompt="You are the research orchestrator for a new research session.

  MODE: full
  TOPIC: <user_input>{topic from $ARGUMENTS}</user_input>
  TOPIC_SLUG: {topic_slug}
  CONFIG: {serialized config}
  MAX_DIMENSIONS: {max_dimensions}
  CONTEXT_FILE_CONTENT: {context_content if non-null, else ""}
  QUICK_MODE: {true if --quick flag}
  REQUESTED_DIMENSIONS: {comma-separated dimension list from --dimensions flag, or "interactive" if omitted}
  {If resuming: PRIOR_ELICITATION: {prior elicitation JSON}}

  Execute the full research orchestration:
  1. Initialize team (Phase 0)
  2. Run elicitation (Phase 1) {quick mode note if applicable}
  3. Spawn dimension-analysts (Phase 2)
  4. Verify methodology plans (Phase 2.5)
  5. Run post-findings codex review gates (Phase 2.75)
  6. Merge findings (Phase 3)
  7. Run post-merge codex review gate (Phase 3.5)
  8. Render progress view (Phase 3.75)
  9. Cleanup (Phase 4)

  Follow all protocols defined in your agent definition."
)
```

Wait for the orchestrator to complete. The orchestrator handles all interaction with the user (elicitation questions, confirmations, progress updates).

---

## Error Handling

**If orchestrator doesn't complete within a reasonable time:**
1. Check for partial results: `Glob("./reports/{topic_slug}/findings_*.json")`
2. If findings files exist → orchestrator made progress. Check `research-progress.md` for last phase.
3. If no findings → inform user: "Research session did not complete. You can retry with `/sigint:start`."

**If state.json already exists:**
- Confirm before overwriting: "Previous session data exists. Overwrite?"

---

## Output

After orchestrator completes:
- Research session state saved to `./reports/{topic_slug}/state.json`
- Progress view at `./reports/{topic_slug}/research-progress.md`
- Quarantined findings (if any) at `./reports/{topic_slug}/quarantine.json`
- Next steps: `/sigint:report`, `/sigint:augment`, `/sigint:update`, `/sigint:issues`
