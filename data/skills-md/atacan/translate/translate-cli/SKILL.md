---
name: translate-cli
description: End-user guide for running and configuring the `translate` CLI across text/stdin/file/glob inputs, provider selection, presets, custom prompt templates, and TOML settings. Use when users ask for command construction, config updates (`translate config`/`translate presets`), provider setup, dry-run validation, or troubleshooting translation behavior.
---

# translate-cli

Use this skill to help end users run and configure the `translate` CLI.

`translate` is a command-line translator for text, stdin, files, globs, and `.xcstrings` catalogs. It supports multiple providers (OpenAI, Anthropic, Ollama, OpenAI-compatible endpoints, Apple providers, DeepL), prompt presets and template overrides, and persistent TOML configuration.

## Capabilities

- Build correct `translate` commands for inline text, stdin, single-file, and multi-file workflows.
- Keep options before positional input(s) when constructing commands (for example, `translate --to de README.md`).
- Explain provider selection, credentials, model/base URL requirements, and provider-specific constraints.
- Configure defaults, provider endpoints, network settings, and presets with `translate config` and `config.toml`.
- Customize prompts with presets, inline templates, `@file` templates, and placeholders.
- Explain output behavior (`stdout`, `--output`, `--in-place`, suffix naming), parallel jobs, dry-run, and validation errors.
- Streaming output: `--stream` forces on, `--no-stream` forces off, otherwise `defaults.stream` applies.

## Starter commands

```bash
translate --text --to fr "Hello world"
translate --to de README.md
translate --provider ollama --text --to en --dry-run "Merhaba dunya"
translate config set defaults.provider anthropic
```

Note: prefer option-before-input ordering in all examples and generated commands.

## References

- Quick examples: `references/quickstart.md`
- Full flag and subcommand reference: `references/flags-and-subcommands.md`
- TOML schema and precedence: `references/config-toml.md`
- Provider rules and environment variables: `references/providers-and-env.md`
- Presets, prompt templates, placeholders: `references/presets-and-prompts.md`
- Runtime behavior, warnings, and exit codes: `references/behavior-and-errors.md`
