---
name: verify
description: Verify harness changes end-to-end without docker — drive the real pinned CLI against a header-capturing stub server with the exact env resolve_auth_env() produces.
---

# Verifying harness changes on a docker-less host

The pipeline's real surface is the in-container `claude -p` process and its
outbound API requests. Without docker, drive the same pinned CLI binary
directly with the env dict the harness would inject via `docker -e`.

## Recipe

1. **Get the pinned CLI** (version from `harness/agent_image.py:CLAUDE_CODE_VERSION`):
   `npm install --no-save @anthropic-ai/claude-code@<pin>` in a temp dir →
   binary at `node_modules/@anthropic-ai/claude-code/bin/claude.exe` (the
   `.exe` name is the real native-binary entry on Linux too, filled in by the
   package's postinstall — not a Windows leftover).
2. **Stub API server**: a tiny HTTP server that appends each request's
   headers to a JSONL file and returns a 400 `invalid_request_error`
   (non-retryable, so the CLI exits fast; exit=1 is expected).
3. **Build the agent env exactly as the pipeline does**:
   `python3 -c "from harness.auth import resolve_auth_env; ..."` and dump to
   an `export`-lines file with `shlex.quote` (values contain newlines —
   NEVER pass via `env $(...)`, word-splitting mangles them; `source` the file).
4. **Emulate the container env**: `unset ANTHROPIC_CUSTOM_HEADERS` (and any
   other ambient var not in the resolved dict) before sourcing — a Claude
   Code session in this repo injects `.claude/settings.json` env into shells,
   which containers never see.
5. **Run**: `ANTHROPIC_BASE_URL=http://127.0.0.1:<port> CLAUDECODE= IS_SANDBOX=1
   timeout 30 <cli> -p hi --model claude-sonnet-4-5 --max-turns 1`, then read
   the captured JSONL.

## Gotchas

- Unit tests in `tests/test_patch.py` / `tests/test_patch_grade.py` need
  docker and fail on docker-less hosts — pre-existing, not your change.
- The docker `-e` injection leg itself can't be exercised without docker;
  it's the same mechanism that carries `ANTHROPIC_API_KEY` in production.
- For the interactive-skills surface, copy `.claude/settings.json` into a
  fresh temp dir and run the host `claude` from there (with ambient
  `ANTHROPIC_CUSTOM_HEADERS` unset so settings.json is the only source).
