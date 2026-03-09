---
name: miles
description: Design websites with Miles AI. Use when building websites, generating site layouts, creating web content, or when the user mentions Miles. Manages the full design conversation from brief through design direction selection to final build.
hooks:
  SessionStart:
    - hooks:
        - type: command
          command: "chmod +x ${CLAUDE_SKILL_DIR}/scripts/miles-cli.mjs && : > ~/.miles/last-response && ${CLAUDE_SKILL_DIR}/scripts/miles-cli.mjs check-auth 2>/dev/null || true"
          once: true
  PostToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "${CLAUDE_SKILL_DIR}/scripts/miles-cli.mjs hook"
---

# Miles AI Website Designer

Miles is an AI website designer you interact with through conversation via a CLI. You send messages, Miles responds — progressing through discovery, brief creation, design directions, and full site building.

## Available Commands

This is the complete set of commands. Do not invent others.

| Command | Purpose |
|---------|---------|
| `miles whoami` | Check authentication status |
| `miles login` | Authenticate (production) |
| `miles create-site "<description>" [--brief file]` | Create site, start conversation, wait for response |
| `miles reply "<message>"` | Send a message to Miles, wait for response |
| `miles wait` | Recovery only — if a prior command was interrupted |
| `miles status` | Quick non-blocking status check |
| `miles design-directions` | Re-list design direction preview URLs |
| `miles select-design-direction <N>` | Pick a design, triggers site build, waits for completion |
| `miles screenshot <url>` | Screenshot a preview URL (saves JPEG, prints path) |
| `miles preview` | Open dashboard in browser |
| `miles sites` | List all sites |
| `miles balance` | Check credits |
| `miles messages` | Full conversation history |
| `miles export-site` | Get static HTML download URL |
| `miles build-theme` | Convert HTML site to WordPress theme |
| `miles export-theme` | Get WordPress theme download URL |

Run all miles commands as: `${CLAUDE_SKILL_DIR}/scripts/miles-cli.mjs <command>`

Set the Bash timeout to 10 minutes (600000ms) for all miles commands — site building and theme conversion can take several minutes.

## Step 1: Authenticate

```bash
${CLAUDE_SKILL_DIR}/scripts/miles-cli.mjs whoami
```

If not logged in:

```bash
${CLAUDE_SKILL_DIR}/scripts/miles-cli.mjs login
```

This opens a browser URL for approval. Tell the user to approve in their browser.

## Step 2: Create a Site

Pass the user's description directly to create-site — the richer the initial description, the fewer follow-up questions Miles will ask:

```bash
${CLAUDE_SKILL_DIR}/scripts/miles-cli.mjs create-site "<user's description>"
```

If the user provided a written brief, save it to a temp file and use `--brief`:

```bash
${CLAUDE_SKILL_DIR}/scripts/miles-cli.mjs create-site --brief /tmp/brief.md "<summary>"
```

## Step 3: Relay the Conversation

After every `create-site`, `reply`, or `wait` command, Miles' response is delivered to you as additional context via a hook. This context contains Miles' message, the current phase, and structured data like questions and options.

<relay_guidance>

### Your role: relay, not participant

Miles conducts a design interview where each question builds on previous answers to refine the user's intent. Even if you think you know the answer from the user's original prompt, Miles needs to hear it directly from the user — Miles uses the specific phrasing to calibrate tone, formality, and design direction. Skipping the conversation produces worse designs because Miles lacks the nuanced input it needs.

Your job is straightforward: take what Miles says and show it to the user, then take what the user says and send it to Miles.

A detailed initial prompt (e.g. "Build me a website for my yoga studio in Portland, we do hot yoga and vinyasa, modern style") is a description to pass to `create-site`, not permission to answer all of Miles' follow-up questions yourself. Only if the user explicitly says "just go ahead" or "you decide" can you answer Miles' questions using your judgment — and even then, still show the brief and design directions for user approval.

### How to relay

The hook context includes structured tags like `[question: ...]` with question text and numbered options. Use `AskUserQuestion` to present these to the user, copying the question text and options directly from the context. Then send the user's answer:

```bash
${CLAUDE_SKILL_DIR}/scripts/miles-cli.mjs reply "<user's exact answer>"
```

Pass the user's words through unchanged. If the user says "Modern and clean", send "Modern and clean" — Miles knows how to work with brief answers. Go straight to the next action after each reply; skip commentary like "Great choice!".

</relay_guidance>

<example>
User prompt: "Build a website for my yoga studio"

1. Run: `${CLAUDE_SKILL_DIR}/scripts/miles-cli.mjs create-site "Build a website for my yoga studio"`
2. Hook context arrives with: `[question: What's the name of your studio?]`
3. Use AskUserQuestion: "What's the name of your studio?"
4. User answers: "Breathe Portland Yoga"
5. Run: `${CLAUDE_SKILL_DIR}/scripts/miles-cli.mjs reply "Breathe Portland Yoga"`
6. Hook context arrives with next question → repeat relay
7. Miles presents brief (phase: brief_review) → show brief to user, ask approval
8. User approves → `${CLAUDE_SKILL_DIR}/scripts/miles-cli.mjs reply "Looks good, approved"`
9. Miles generates design directions → present to user for selection
10. User picks design 2 → `${CLAUDE_SKILL_DIR}/scripts/miles-cli.mjs select-design-direction 2`
11. Miles builds the site → `[site_ready: true]`
</example>

### Brief review

When Miles presents a design brief for approval (phase: `brief_review`), show the brief content to the user and ask them to approve or request changes. The brief is the blueprint for the entire site — the user needs to see it.

## Step 4: Choose a Design Direction

When Miles finishes generating design directions (phase: `design_directions_ready`), the context includes preview URLs for each design.

Visually inspect each design before presenting to the user. If a browser is available, open the preview URLs. Otherwise, use `miles screenshot` to capture them — it saves a JPEG and prints the path, then use `Read` to view the image:

```bash
${CLAUDE_SKILL_DIR}/scripts/miles-cli.mjs screenshot /preview/abc123/previews/hero-xyz/index.html
```

When evaluating designs, consider: visual hierarchy, tone match with the business, layout quality, image quality, overall polish.

If none fit, ask Miles for new directions with feedback:

```bash
${CLAUDE_SKILL_DIR}/scripts/miles-cli.mjs reply "None of these feel right. I want something more modern and minimal."
${CLAUDE_SKILL_DIR}/scripts/miles-cli.mjs wait
```

Use `AskUserQuestion` to ask the user which design they prefer. Then select it — this command triggers the full site build and waits for completion:

```bash
${CLAUDE_SKILL_DIR}/scripts/miles-cli.mjs select-design-direction <number>
```

The select command already waits for the build, so there's no need to run `miles wait` after it.

## Step 5: The Built HTML Site

When `select-design-direction` finishes (indicated by `[site_ready: true]`), Miles has built a complete static HTML website. This is the first deliverable.

```bash
${CLAUDE_SKILL_DIR}/scripts/miles-cli.mjs preview              # Open live preview in browser
${CLAUDE_SKILL_DIR}/scripts/miles-cli.mjs screenshot <url>     # Screenshot a preview URL
${CLAUDE_SKILL_DIR}/scripts/miles-cli.mjs export-site          # Get static HTML download URL and file info
```

## Step 6: WordPress Theme (Separate Step)

Converting the HTML site into a WordPress block theme is a separate operation from the site build.

```bash
${CLAUDE_SKILL_DIR}/scripts/miles-cli.mjs build-theme          # Triggers theme conversion
${CLAUDE_SKILL_DIR}/scripts/miles-cli.mjs export-theme         # Get WordPress theme download URL
```

## How the Hook Works

When you run `create-site`, `reply`, or `wait`, the CLI writes Miles' response to a file. After the Bash command completes, a PostToolUse hook reads that file and delivers it to you as additional context. This means:

- Miles' response appears as context after the tool result — look for it there, not in stdout
- `create-site`, `reply`, and `wait` already deliver Miles' full response, so calling `miles messages` or `miles status` afterward is redundant
- Go straight to the next action after receiving Miles' response (relay the question via AskUserQuestion, or tell the user what happened)

## Credits

Miles uses credits for operations. If the context includes a `[warning: ...]` about credits running low, inform the user. If there's an `[error: ...]` about no credits, stop and tell the user to top up at their dashboard billing page.

See [commands.md](commands.md) for detailed command reference and [examples.md](examples.md) for workflow examples.
