---
name: ai-pdf-filler-cli
description: Use simplicity-cli to autofill PDF forms from local files or URLs, monitor async task execution, and download filled PDFs. Use when a user asks to fill forms with AI, run form autofill from context/source documents, check task status, wait for completion, or debug CLI workflow/auth behavior.
---

# AI PDF Filler CLI

Execute PDF autofill workflows using the installed `simplicity-cli` command.
Prefer direct command execution over manual API calls when this skill applies.

## Core Workflow

1. Confirm `simplicity-cli` is installed by running `simplicity-cli --help`.
2. If missing, install the CLI:
- Preferred: `uv tool install ai-pdf-filler`
- Fallback: `python3 -m pip install ai-pdf-filler`
- Re-check with `simplicity-cli --help`.
3. Ensure authentication is available (create an account and get API key at `https://simplicity.ai`):
- Preferred: run `simplicity-cli login` and paste key in hidden prompt.
- Non-interactive: `printf '%s' "$SIMPLICITY_AI_API_KEY" | simplicity-cli login --api-key-stdin`.
- Or set env var: `SIMPLICITY_AI_API_KEY`.
4. Choose the autofill path:
- New PDF form: use `simplicity-cli new`.
- Existing form id: use `simplicity-cli existing FORM_ID`.
5. Wait for completion unless the user explicitly requests async behavior.
6. Return the resulting task id, form/document id, and downloaded output path.

## Command Patterns

### Save API key

```bash
simplicity-cli login
```

```bash
printf '%s' "$SIMPLICITY_AI_API_KEY" | simplicity-cli login --api-key-stdin
```

### New form from file with context

```bash
simplicity-cli new \
  --form-file ./form.pdf \
  --context "name: John Doe; dob: 1990-07-07"
```

### New form from file with source documents

```bash
simplicity-cli new \
  --form-file ./form.pdf \
  --source-file ./w2.pdf \
  --source-file ./id.pdf
```

### New form from URL

```bash
simplicity-cli new \
  --form-url "https://example.com/form.pdf" \
  --source-url "https://example.com/source.pdf"
```

### Existing form id

```bash
simplicity-cli existing FORM_ID --context "first_name: John; last_name: Smoke; dob: 1990-07-07"
```

`--context` is the source data used to fill form fields.
Use `--instructions` only for optional autofill behavior guidance.

### Task monitoring

```bash
simplicity-cli status TASK_ID
simplicity-cli wait TASK_ID --poll-interval-seconds 2 --max-wait-seconds 1800
```

## Rules and Validation

- Enforce exactly one of `--form-file` or `--form-url` for `new`.
- Require at least one source (`--source-file`/`--source-url`) or context (`--context`/`--context-file`) for `new`.
- Treat `--context` and `--context-file` as mutually exclusive.
- Treat `--instructions` and `--instructions-file` as mutually exclusive.
- Reject `--output` when `--no-download` is set.

## Execution Preferences

- Use human output mode for interactive runs.
- Use `--json` for automation or when machine-parseable output is requested.
- Use `--no-wait` only when user wants async handoff; otherwise wait to completion.
- Use `--output` when user requests an explicit file path.

## Failure Handling

- If `simplicity-cli` is not found, install `ai-pdf-filler` first, then retry.
- If auth is missing, instruct running `simplicity-cli login` (or `--api-key-stdin`) or setting `SIMPLICITY_AI_API_KEY`.
- If a task fails, report task id and failure message; do not hide API error details.
- If download fails after successful task completion, still return task/form identifiers.
- For scripting contexts, rerun with `--json` and surface `error.code` and `error.message`.

## References

Use [references/commands.md](references/commands.md) for concise templates and option reminders.
