---
name: agent-session-search
description: 'Coding Agent Session Search - unified CLI/TUI to index and search local coding agent history from Claude Code, Codex, Gemini, Cursor, Aider, ChatGPT, Cline, OpenCode, Amp, Pi-Agent, Factory, and more. Use when searching past agent conversations, indexing coding session history, finding previous solutions across agents, or querying session logs with CASS CLI robot mode.'
license: MIT
metadata:
  author: oakoss
  version: '1.0'
  source: https://github.com/pchaganti/gx-cass
---

# Agent Session Search

Unified CLI/TUI to index and search local coding agent history. Aggregates sessions from 13+ agents into a single searchable index with sub-60ms latency. Purpose-built for AI agent consumption with robot mode and forgiving syntax. Not a library -- CASS is an external Rust CLI that must be installed separately.

Do not use for real-time session monitoring. Do not use when the agent has no local session history stored on disk.

Install via `curl` one-liner, Homebrew, or Scoop (see Configuration reference). Requires Rust nightly toolchain for building from source.

**CRITICAL: NEVER run bare `cass` -- it launches an interactive TUI that blocks your session. Always use `--robot` or `--json` flags.**

## Essential Commands

| Command                                        | Purpose                                               |
| ---------------------------------------------- | ----------------------------------------------------- |
| `cass health --json`                           | Health check (exit 0 = healthy, non-zero = unhealthy) |
| `cass index --full`                            | Full rebuild of DB and search index                   |
| `cass index`                                   | Incremental update since last scan                    |
| `cass index --watch`                           | Watch mode: auto-reindex on file changes              |
| `cass search "query" --robot`                  | Search with JSON output                               |
| `cass search "query" --robot --fields minimal` | Minimal payload (path, line, agent)                   |
| `cass search "query" --robot --limit 5`        | Cap number of results                                 |
| `cass search "query" --robot --mode hybrid`    | Use hybrid (lexical + semantic) search                |
| `cass view /path -n 42 --json`                 | View source at specific line                          |
| `cass expand /path -n 42 -C 5 --json`          | Context around a search result                        |
| `cass export-html /path`                       | Export conversation as self-contained HTML            |
| `cass robot-docs guide`                        | LLM-optimized documentation                           |
| `cass robot-docs schemas`                      | Response JSON schemas                                 |
| `cass sources setup`                           | Configure multi-machine remote sources                |

## Supported Agents

| Agent           | Location                                        | Format                                 |
| --------------- | ----------------------------------------------- | -------------------------------------- |
| Claude Code     | `~/.claude/projects`                            | JSONL                                  |
| Codex           | `~/.codex/sessions`                             | Rollout JSONL                          |
| Gemini CLI      | `~/.gemini/tmp`                                 | JSON                                   |
| Cline           | VS Code global storage                          | Task directories                       |
| OpenCode        | `.opencode` directories                         | SQLite                                 |
| Amp             | `~/.local/share/amp` + VS Code                  | Mixed                                  |
| Cursor          | `~/Library/Application Support/Cursor/User/`    | SQLite state.vscdb                     |
| ChatGPT         | `~/Library/Application Support/com.openai.chat` | JSON (v1 unencrypted; v2/v3 encrypted) |
| Aider           | `~/.aider.chat.history.md` + per-project        | Markdown                               |
| Pi-Agent        | `~/.pi/agent/sessions`                          | JSONL                                  |
| Factory (Droid) | `~/.factory/sessions`                           | JSONL                                  |
| Clawdbot        | `~/.clawdbot/sessions`                          | JSONL                                  |
| Vibe (Mistral)  | `~/.vibe/logs/session/*/messages.jsonl`         | JSONL                                  |

## Search Modes

| Mode              | Algorithm                                | Best For                            |
| ----------------- | ---------------------------------------- | ----------------------------------- |
| lexical (default) | BM25 full-text via Tantivy               | Exact term matching, code searches  |
| semantic          | Vector similarity (MiniLM via FastEmbed) | Conceptual queries, finding similar |
| hybrid            | Reciprocal Rank Fusion (RRF)             | Balanced precision and recall       |

Semantic mode requires MiniLM model files. When unavailable, CASS falls back to a hash-based embedder for approximate similarity.

## Forgiving Syntax

CASS auto-corrects common agent mistakes and emits teaching notes to stderr:

| Input                             | Correction                               |
| --------------------------------- | ---------------------------------------- |
| Typos in commands                 | Levenshtein-matched to canonical command |
| Single-dash long flags (`-robot`) | Normalized to `--robot`                  |
| Wrong case (`--Robot`)            | Lowercased to `--robot`                  |

## Common Mistakes

| Mistake                    | Fix                                          |
| -------------------------- | -------------------------------------------- |
| Running bare `cass`        | Always use `--robot` or `--json`             |
| Missing `--robot` flag     | Add `--robot` for JSON output                |
| No index exists            | Run `cass index --full` first                |
| Token budget overflow      | Use `--fields minimal` and `--limit`         |
| Stale search results       | Run `cass index` to refresh                  |
| Parsing stderr as JSON     | stdout = JSON only, diagnostics go to stderr |
| Assuming CASS is installed | Check `cass health --json` first             |

## Delegation

Use this skill for indexing, searching, and analyzing coding agent session history via CASS CLI. Delegates to the external `cass` binary for all operations. Run `cass robot-docs guide` for the authoritative command reference directly from the installed version.

For multi-machine session search, see Remote Sources. For TUI usage by human operators, see TUI Reference.

## References

- [Command Reference](references/command-reference.md) -- indexing, search, session viewing, export, and diagnostics
- [Robot Mode](references/robot-mode.md) -- self-documenting API, forgiving syntax, output formats, token budget
- [Query Language](references/query-language.md) -- boolean operators, wildcards, match types, time formats, auto-fuzzy fallback
- [Search and Ranking](references/search-and-ranking.md) -- search modes, ranking, scoring formula
- [Remote Sources](references/remote-sources.md) -- multi-machine search via SSH/rsync, setup wizard, path mappings
- [TUI Reference](references/tui-reference.md) -- keyboard shortcuts, themes, saved views, density modes, bookmarks
- [Error Handling](references/error-handling.md) -- structured errors, exit codes, troubleshooting
- [Internals](references/internals.md) -- response shapes, deduplication, performance, watch mode, semantic search
- [Configuration](references/configuration.md) -- environment variables, shell completions, installation, integrations
