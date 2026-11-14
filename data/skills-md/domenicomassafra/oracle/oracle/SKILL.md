---
name: oracle
description: "Oracle second-model review: bundle prompts/files, debug, refactor, design."
---

# Oracle (CLI) — best use

Oracle bundles a prompt and selected files into a one-shot request so another
model can answer with real repository context through the API or browser. A
prompt is required; attach files only when they add necessary context. Treat
responses as advisory and verify them against the codebase and tests.

When an operator exposes a shared subscription-backed browser through MCP,
respect its engine policy. `ORACLE_MCP_ENGINE_POLICY=browser-only` means API
engine requests and multi-model fan-out are intentionally unavailable; do not
work around that boundary or retry through a paid provider route.

## Main use case (browser, GPT-6)

Use browser mode with GPT-6 when the authorized ChatGPT account exposes it.
Oracle already supports the GPT-6 picker, the `latest` alias, and verified
effort selection. Select the model and effort explicitly; never mistake a
generic Pro pill for proof of which model served the answer.

Recommended defaults:

- Engine: browser (`--engine browser`)
- GPT-6 browser: `--model gpt-6 --browser-thinking-time extra-high`
- GPT-6 browser Pro: `--model gpt-6-pro` (fails closed if Pro cannot be verified)
- GPT-6 API, only if separately authorized and cost-approved:
  `--model gpt-6-astra --reasoning-mode pro`
- Legacy fallback: use GPT-5.6 or GPT-5.5 **only if explicitly requested or
  approved**. Never silently downgrade a GPT-6 request.
- Attachments: directories/globs plus excludes; never attach secrets by default

Model availability and Pro effort are account-dependent. Confirm the selected
GPT-6 radio and effort before submitting; if unavailable, report the blocked
request rather than silently switching to another model.

## GPT-6 model selection

Supported explicit targets:

- Browser `gpt-6`, `gpt-6-astra`, or `latest`: select the GPT-6 entry.
- Browser `gpt-6-pro`: select GPT-6 with Pro effort.
- API `gpt-6-astra`: select the GPT-6 API model; request Pro reasoning
  explicitly when approved. `gpt-6-pro` is not an API model slug.
- GPT-5.6 aliases remain compatible for **explicit legacy requests**, not as
  the default recommendation.

For a browser consultation, use:

```bash
oracle --engine browser --browser-manual-login --model gpt-6 \
  --browser-thinking-time extra-high \
  -p "<task>" --file "src/**"
```

For a GPT-6 browser Pro consultation, use:

```bash
oracle --engine browser --browser-manual-login --model gpt-6-pro \
  -p "<task>" --file "src/**"
```

GPT-6 and Pro are independently verified in the browser. An observed picker
selection does not prove backend execution identity; retain run receipts.

## Compatibility with npm 0.15.2

The historical npm 0.15.2 release does not support the current model picker;
do not use it to satisfy a GPT-6 request. Its explicit legacy fallback was:

```bash
npx -y @steipete/oracle@0.15.2 --engine browser --model gpt-5.5-pro \
  -p "<task>" --file "src/**"
```

Verify that the installed CLI supports GPT-6 in `--help --verbose` and dry
run before executing. Do not treat a successful historical fallback as GPT-6.

## Image-generation requests

Use Oracle's `chatgpt_image` MCP tool (or the supported browser image path)
when the task is to generate an image. The image-generation capability, not
the text reasoning model's version, determines the route. Do not require
GPT-6/Pro merely because a picture is requested. Leave the `model` input
unset unless a specific compatible model was authorized; verify a saved image
with the requested dimensions and actual visual content before reporting
success. A Canva attempt or a text-only answer is not an image artifact.

## Golden path

1. Pick the smallest file set that still contains the truth.
2. Preview the bundle with `--dry-run` and `--files-report`.
3. Use browser mode for GPT-6; use API only when explicitly intended.
4. If a run detaches or times out, reattach to the stored session instead of
   starting a duplicate.

## Commands

- Show help:
  - `npx -y @steipete/oracle --help --verbose`

- Preview without calling a model:
  - `npx -y @steipete/oracle --dry-run summary -p "<task>" --file "src/**" --file "!**/*.test.*"`
  - `npx -y @steipete/oracle --dry-run full -p "<task>" --file "src/**"`

- Inspect token usage:
  - `npx -y @steipete/oracle --dry-run summary --files-report -p "<task>" --file "src/**"`

- Browser run:
  - `oracle --engine browser --browser-manual-login --model gpt-6 --browser-thinking-time extra-high -p "<task>" --file "src/**"`

- Manual paste fallback:
  - `npx -y @steipete/oracle --render-markdown --copy-markdown -p "<task>" --file "src/**"`
  - `--render` is an alias for `--render-markdown`.

- Performance trace:
  - `npx -y @steipete/oracle --perf-trace --perf-trace-path /tmp/oracle-perf.json --dry-run summary -p "<task>" --file "src/**"`

## Attaching files

`--file` accepts files, directories, and globs. Pass it multiple times or use
comma-separated entries.

- Include: `--file "src/**"`, `--file src/index.ts`, `--file docs --file README.md`
- Exclude: prefix a pattern with `!`, for example `--file "!src/**/*.test.ts"`
- Default ignored directories: `node_modules`, `dist`, `coverage`, `.git`,
  `.turbo`, `.next`, `build`, and `tmp`
- Globs honor `.gitignore` and do not follow symlinks.
- Dotfiles require an explicit dot-segment in the pattern, such as
  `--file ".github/**"`.
- Files over 1 MB are rejected by default; configure
  `ORACLE_MAX_FILE_SIZE_BYTES` or `maxFileSizeBytes` when necessary.

Keep total input under roughly 196k tokens. Use `--files-report` or
`--dry-run json` to identify oversized inputs. Never attach `.env` files,
private keys, auth tokens, or other secrets unless they have been redacted and
are essential to the question.

## Engines and browser controls

- Auto-selection uses API when `OPENAI_API_KEY` is set and browser otherwise.
- Browser supports GPT models through ChatGPT and Gemini models through Gemini
  web. API-only models include `gpt-5.1-codex`.
- Current model families include GPT-6, legacy GPT-5.x, Gemini 3.x, and Claude
  4.x; availability depends on engine and provider.
- API runs require explicit user consent because they may incur usage costs.
- Browser attachments use `--browser-attachments auto|never|always`.
- Browser uploads keep one text/source file native and bundle multiple
  text/source files. `auto` keeps flattened text for text-only uploads; use
  `--browser-bundle-format zip` for a filesystem tree, or `--browser-bundle-files`
  to force every resolved attachment into one bundle.
- Reuse an existing Chrome session with `--browser-tab <ref>`,
  `--browser-attach-running`, or `--remote-chrome <host:port>`.
- Add `--browser-no-focus` (config `browser.noFocus`) to keep Chrome in the
  background during launch, new tabs, and send. When
  focus emulation is available, an ordinary run does not steal keyboard focus
  or switch macOS Spaces; if it cannot be enabled, Oracle tries to bring
  Chrome forward before clicking. A reattach that falls back to relaunching
  Chrome can still activate it.
- Use `--browser-model-strategy select|current|ignore` to control picker
  behavior.
- Use `--browser-follow-up "<prompt>"` for another turn in the same browser
  conversation, or `--followup <sessionId|responseId>` for a stored run.
- Use `--browser-research deep` only when Deep Research is explicitly wanted.

## API preflight

Before an API run, check provider readiness without printing secrets:

```bash
oracle doctor --providers --models gpt-5.4,claude-4.6-sonnet,gemini-3-pro
oracle --preflight --models gpt-5.4,gemini-3-pro
oracle --route --model gpt-5.4
```

Use `--provider openai` or `--no-azure` when first-party OpenAI routing is
required. For multi-model panels where partial success is useful, use
`--allow-partial --write-output <path>` so successful outputs and the manifest
can be recovered.

Set an explicit deadline for automation, for example `--timeout 10m`; Oracle
derives the HTTP timeout unless `--http-timeout` is supplied.

## Sessions and recovery

- Sessions are stored under `~/.oracle/sessions`; override with
  `ORACLE_HOME_DIR`.
- Browser artifacts include `transcript.md` and, when available, research
  reports and generated images.
- List recent sessions with `oracle status --hours 72`.
- Attach with `oracle session <id> --render`.
- Use `--slug "<3-5 words>"` for readable session IDs.
- If a run times out, reattach; do not re-run it. Use `--force` only when a
  genuinely new identical run is intended.
- Successful non-project browser one-shots are archived automatically by
  default; override with `--browser-archive never|always`.

## Prompt template

Oracle starts with zero project knowledge. Include:

- Project briefing: stack, services, build/test commands, and platform constraints
- Where things live: entrypoints, configs, key modules, and dependency boundaries
- Exact question, prior attempts, and verbatim error text
- Constraints such as API compatibility, performance budgets, and files not to change
- Desired output such as a patch plan, tests, risk list, or tradeoff comparison

For a long investigation, make the prompt restorable: put a 6–30 sentence
briefing at the top, concrete reproduction and errors in the middle, and attach
all context files required by a fresh model at the bottom. Oracle runs are
one-shot; the model does not remember prior runs.
