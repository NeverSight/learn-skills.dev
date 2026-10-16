---
name: create-cli
description: >
  Build command-line interfaces for AI agents. Use when building a new CLI or refactoring an existing
  one for agent use.
---

# Create CLI

Build CLIs for AI agents. Assume 100% agent usage.

## Default Assumptions

- **Language**: Shell script (bash) by default. Use Python (uv + typer) or TypeScript (bun + commander) only when:
  - SDK works better in that language
  - Requires specific packages (e.g., data analysis → Python)
  - User explicitly requests it
- **Non-interactive**: Agents cannot respond to prompts—commands just hang
- **Parseable output**: JSON for machine consumption; human-readable as fallback

## Core Principles

### 1. Non-interactive first

Agents cannot answer prompts. Every input must be expressible as a flag.

```bash
# Bad: hangs the agent
mycli deploy
? Which environment? (use arrow keys)

# Good: works
mycli deploy --env staging
```

- Gate confirmations behind `--yes` or `--force` flags
- If required input is missing, fail immediately with an actionable error—don't prompt
- For optional human interactivity, gate behind `--interactive` flag

### 2. Layered discovery

Agents discover incrementally: `mycli` → `mycli deploy --help`. Don't dump all docs upfront.

- Each subcommand has its own `--help`
- Every `--help` includes **Examples** (agents pattern-match faster than reading prose)
- Suggest next commands in output when helpful

```text
Options:
  --env     Target environment (staging, production)
  --tag     Image tag (default: latest)
  --force   Skip confirmation

Examples:
  mycli deploy --env staging
  mycli deploy --env production --tag v1.2.3
  mycli deploy --env staging --force
```

### 3. JSON input for complex data

Prefer `--json` for structured input—agents generate it directly with zero translation loss.

```bash
# Accept full JSON payload
mycli create --json '{"title": "Doc", "locale": "en_US", "gridProperties": {"frozenRowCount": 1}}'

# Also accept JSON from stdin
cat config.json | mycli create --stdin
```

JSON maps directly to API schemas. No need to flatten nested structures into flags.

### 4. Parseable output

- Provide `--json` for structured output; human-readable text as default
- On success, return machine-useful data: IDs, URLs, durations, state changes

```text
deployed v1.2.3 to staging
url: https://staging.myapp.com
deploy_id: dep_abc123
duration: 34s
```

- Add `-q/--quiet` when useful; keep success output brief but informative

### 5. Input hardening against hallucinations

Agents don't typo like humans—they hallucinate. Validate defensively:

| Threat | Example | Defense |
|--------|---------|---------|
| Path traversal | `../../.ssh` | Canonicalize and sandbox to CWD |
| Control characters | Invisible chars below ASCII 0x20 | Reject them |
| Embedded query params | `fileId?fields=name` | Reject `?` and `#` in IDs |
| Pre-encoded URLs | `%2e%2e` for `..` | Reject `%` in resource IDs |

"The agent is not a trusted operator. Build like it."

### 6. Idempotency

Agents retry constantly. The same successful command run twice should be safe:

```bash
$ mycli deploy --env staging --tag v1.2.3
✓ Deployed v1.2.3 to staging

$ mycli deploy --env staging --tag v1.2.3
✓ Already deployed, no-op
```

No duplicate side effects. Design for crash-only recovery when feasible.

### 7. Predictable structure

Be consistent across subcommands:

- Reuse verbs: if you have `list` somewhere, use `list` everywhere (not `show` or `get`)
- Avoid ambiguous pairs (`update` vs `upgrade`, `remove` vs `delete`) unless sharply differentiated
- Share global flags/config/help across subcommands

For complex CLIs managing multiple resource types (like Docker, kubectl), see [references/multi-resource-clis.md](references/multi-resource-clis.md).

### 8. Destructive actions

Preview before committing. Require explicit confirmation flags.

```bash
# Preview what would happen
$ mycli delete --env production --dry-run
Would delete 3 instances in production
  - instance-a
  - instance-b
  - instance-c
No changes made.

# Execute with confirmation
$ mycli delete --env production --force
✓ Deleted 3 instances
```

- `--dry-run` validates without executing
- `--force` or `--yes` bypasses confirmation (required for destructive ops)

### 9. Schema introspection (for API-backed CLIs)

Let agents self-serve without static docs baked into prompts:

```bash
$ mycli schema drive.files.list
{
  "params": {"fields": "string", "pageSize": "integer"},
  "scopes": ["drive.readonly"],
  ...
}
```

The CLI becomes the canonical source of truth for what the API accepts right now.

### 10. Fail fast with actionable errors

On missing required flags, exit immediately with a clear message and correct invocation:

```text
Error: No image tag specified.
  mycli deploy --env staging --tag <image-tag>
  Available tags: mycli build list --output tags
```

Don't hang. Give agents something to self-correct with.

### 11. Solve, don't punt

Handle recoverable errors in the CLI rather than failing and forcing the agent to figure it out.

```bash
# Good: CLI handles the missing file
$ mycli process data.json
File data.json not found, creating with defaults...
✓ Created data.json

# Bad: CLI fails, agent must diagnose and retry
$ mycli process data.json
Error: No such file or directory: data.json
```

When errors are recoverable (missing files, missing directories, stale cache), fix them and continue. Only fail when there's no reasonable recovery path.

**Document magic numbers.** If a constant exists, explain why:

```bash
# Good: self-documenting
TIMEOUT=30  # HTTP requests typically complete within 30s
RETRIES=3   # Most intermittent failures resolve by second retry

# Bad: voodoo constants
TIMEOUT=47  # Why 47?
RETRIES=5   # Why 5?
```

If you don't know the right value, the agent won't either.

### 12. Stdin and pipelines

Agents think in pipelines. Accept stdin and support chaining.

```bash
# Pipe data between commands
cat config.json | mycli validate --stdin
mycli list --json | mycli process --stdin

# Chain with other tools
mycli export --json | jq '.items[]' | mycli import --stdin
```

- Accept `--stdin` or `-` for input where it makes sense
- Avoid odd positional ordering that breaks piping
- Output should be pipeable (clean stdout, errors to stderr)

## Interview (only if not already done)

If requirements aren't already clear from context, ask these questions using `AskUserQuestion`/`request_user_input`:

1. **Command name + purpose**: What's the CLI called and what does it do?
2. **Input sources**: Args only, or also stdin/files? Any secrets? (remind: never via flags—use stdin or `--password-file`)
3. **Output needs**: Does output need to be piped? (if yes, add `--json`)
4. **Subcommands**: Single command or multiple subcommands?
5. **Complexity check**: Does it need external SDKs/packages? (if yes, ask Python or TypeScript)

Proceed with sensible defaults for unanswered questions.

## Default Conventions

- `-h/--help` always shows help and ignores other args
- `--version` prints version to stdout
- Primary data to stdout; diagnostics/errors to stderr
- `--json` for machine output; consider `--plain` for stable line-based text
- Support `-` for stdin/stdout when input/output is a file
- Respect `NO_COLOR`, `TERM=dumb`; provide `--no-color`
- Handle Ctrl-C: exit fast, bounded cleanup, crash-only when possible

## Testing the CLI

After implementation, test the CLI before reporting done. Don't just check that it runs—verify it behaves correctly for agents.

**Required tests:**

1. **Primary use case works** - Run the main workflow the CLI was built for. Verify output matches expectations.

2. **Help is useful** - Check that `--help` shows usage, flags, and examples. Subcommands should have their own help.

3. **Non-interactive** - Pipe empty input or run without a TTY. The CLI must not hang waiting for prompts. Missing required args should fail fast with an actionable error.

4. **Exit codes are correct** - Success returns 0. Invalid usage returns non-zero. Check a few failure cases.

5. **JSON output parses** (if `--json` supported) - Pipe output through `jq` or equivalent to verify it's valid JSON with expected fields.

6. **Errors go to stderr** - Redirect stdout to `/dev/null` and trigger an error. The error message should still appear (via stderr).

**If applicable:**

7. **Input validation** - If the CLI accepts paths, IDs, or user-provided strings, test that malformed inputs (traversal paths, control chars, embedded params) are rejected.

8. **Idempotency** - For state-changing commands, run the same command twice. Second run should be safe (no-op or "already exists").

9. **Dry-run works** - If `--dry-run` is supported, verify it shows what would happen without making changes.

Fix any failures before considering the CLI complete.

## Language Notes

- **Shell script (bash)**: Default. Prefer long options (--env, --force) over short (-e, -f).
- **Python**: uv + typer. Choose when SDK is Python or needs data processing.
- **TypeScript**: bun + commander. Choose when SDK is JS/TS.

## References

- `references/cli-guidelines.md` - Extended philosophy, edge cases (man pages, distribution, analytics), full rationale behind the core principles
- `references/context-window-discipline.md` - Field masks, NDJSON streaming, output limiting for CLIs that return large results
- `references/auth-for-agents.md` - Env vars for tokens, service accounts, headless auth patterns
- `references/response-sanitization.md` - Protecting against prompt injection in API responses
- `references/multi-resource-clis.md` - Noun-verb pattern for complex CLIs managing multiple resource types (like Docker, kubectl)
