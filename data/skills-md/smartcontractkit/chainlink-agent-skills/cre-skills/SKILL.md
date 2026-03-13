---
name: cre-skills
description: Enable developers to learn and use Chainlink Runtime Environment (CRE) quickly by referencing filtered CRE docs. Trigger when user wants onboarding, CRE workflow generation (in TypeScript or Golang or other supported languages), workflow guidance, CRE CLI and/or SDK help, runtime operations advice, or capability selection
license: MIT
compatibility: Designed for Claude Code, Cursor Composer, and AI agents that implement https://agentskills.io/specification. Cursor Composer (1.5) is particularly recommended — its WebFetch returns full page content including code snippets.
allowed-tools: Read WebFetch Write Edit Bash
metadata:
  purpose: CRE developer onboarding, assistance and reference
  version: "0.2"
---

# CRE Skills

Assist developers working with the Chainlink Runtime Environment (CRE) by looking up the latest documentation at runtime.

## Runtime Pattern

> **⚠️ IMPORTANT — AGENTS MUST READ BEFORE FETCHING ANYTHING:**
> WebFetch may return an empty shell (nav/metadata only, no prose or code) for some URLs. After every WebFetch call, assess quality before using the content.
>
> **After every WebFetch, ask:** Does the response contain actual prose and/or code blocks with more than ~1000 chars of useful content?
>
> **Full fetch cascade — follow in order:**
> 1. **WebFetch** → assess content quality → proceed if substantial
> 2. **Bash curl** (if WebFetch returned a shell) — works on Windows 10+, Linux, and Mac →
>    ```bash
>    curl -s -L -A "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" "<url>"
>    ```
> 3. **Tell the user** → if both fail, report the URL and suggest they open it directly
>
> Apply this cascade to ALL fetches — doc pages, GitHub URLs, and text dumps.

When a user asks a CRE-related question:

1. **Match user intent to a reference file** — Identify which topic best fits the query from the reference files listed below.
2. **Read the matching reference file** — Each entry includes a summary and key technical details. Use these to orient yourself. Do not fetch yet.
3. **Act immediately** — Write the answer or scaffold from your knowledge and the reference file descriptions. Do not fetch as preparation.
4. **Iterate** — Present your response. Ask the user to test or run it. Then loop:
   - Error or gap blocks progress → fetch exactly what the error names → fix → repeat
   - Cannot write a specific part → mark it inline (e.g. `// NEED: exact consensus tag for uint256`) → fetch that one thing → fill it in → continue
   - No error → done

> **⚠️ Do not fetch as preparation. Fetch as resolution.** Only fetch when you can state the exact piece of information you need. If you can't name it precisely, don't fetch.

CRE has runtime-specific constraints (e.g. WASM environment, encoding requirements) that differ from standard assumptions. When a specific gap involves CRE behaviour you are uncertain about, fetch to resolve it — do not guess.

### Code Example Priority

When looking for code examples or implementation details, use the most targeted source first. Apply the fetch cascade above to any URL you fetch:

1. **Individual doc pages first** — Most targeted. Fetch the specific page for the topic using the fetch cascade. Full content is accessible via curl if WebFetch returns a shell.
2. **Repo references second** (`repo-*.md`) — Use when the doc page lacks sufficient code, or the user explicitly wants a working implementation (templates, SDK examples, demo apps).
3. **Full-text doc dumps last** (`llms-full-ts.txt` / `llms-full-go.txt`) — 35,000-word plain-text dumps linked from `general.md`. Use only when you can't identify a specific doc page or need broad coverage.

**How to work through this list:**
- Fetch the single most relevant URL from the highest-priority source first. Read it fully.
- Stop as soon as you have enough to answer the question. Do not fetch more to verify or feel confident.
- Only move to the next priority source if the current one was genuinely insufficient.
- Never follow links found in fetched content — only fetch URLs explicitly listed in reference files.
- When fetching from repo reference files, fetch only the specific file you need. Do not browse directories or read adjacent files.
- 3-5 URLs is a ceiling, not a target. Most questions need 1-2 fetches.

### CLI Command Priority

When looking up CRE CLI commands, flags, or usage:

1. **Run `cre <command> --help` locally** — Most authoritative and version-accurate. Use this first if the CLI is installed.
2. **Individual CLI doc pages** — Fetch the specific command page via the fetch cascade. Targeted and accessible.
3. **`repo-cre-cli.md`** — Auto-generated markdown for every command. Use if the above don't cover the query.
4. **Full-text doc dumps / other** — Last resort.

**How to work through this list:**
- Fetch the single most relevant URL from the highest-priority source first. Read it fully.
- Stop as soon as you have enough to answer the question. Do not fetch more to verify or feel confident.
- Only move to the next priority source if the current one was genuinely insufficient.
- Never follow links found in fetched content — only fetch URLs explicitly listed in reference files.
- When fetching from repo reference files, fetch only the specific file you need. Do not browse directories or read adjacent files.
- 3-5 URLs is a ceiling, not a target. Most questions need 1-2 fetches.

## Reference Files

| File | Topic | When to use |
|------|-------|-------------|
| [account-setup.md](references/account-setup.md) | Account setup | Creating accounts, CLI login, managing authentication |
| [getting-started.md](references/getting-started.md) | Getting started | CLI installation, project setup, tutorial walkthrough (Go & TypeScript) |
| [capabilities.md](references/capabilities.md) | Capabilities | EVM read/write, HTTP capability, triggers overview |
| [workflow-building.md](references/workflow-building.md) | Workflow building | Secrets, time, randomness, triggers (cron/HTTP/EVM log), HTTP client, EVM client, onchain read/write, report generation |
| [cli-reference.md](references/cli-reference.md) | CLI reference | CLI commands for accounts, auth, project setup, secrets, workflows, utilities |
| [sdk-reference.md](references/sdk-reference.md) | SDK reference | SDK core, consensus/aggregation, EVM client, HTTP client, trigger APIs (Go & TypeScript) |
| [operations.md](references/operations.md) | Operations | Deploying, simulating, monitoring, activating, pausing, updating, deleting workflows, multi-sig wallets |
| [concepts.md](references/concepts.md) | Concepts | Consensus computing, finality, non-determinism, TypeScript WASM runtime |
| [organization.md](references/organization.md) | Organization | Org management, inviting members, linking wallet keys |
| [general.md](references/general.md) | General | CRE overview, key terms, demos, Gelato migration, project configuration, supported networks, release notes, service quotas, support |
| [templates.md](references/templates.md) | Templates | CRE workflow templates overview and usage |

## Workflow Generation Checklist

Follow these additional steps when **generating or scaffolding a new workflow** (not just answering questions):

1. **Determine language** — Before generating any code, confirm whether the user wants Go or TypeScript. Ask directly if not already clear from context.
2. **Choose HTTP capability** — If the workflow involves HTTP requests, ask the user whether they want **regular HTTP** or **Confidential HTTP**. Explain the difference: regular HTTP is the default for standard API calls; Confidential HTTP is an optional capability that provides privacy-preserving requests via enclave execution, secret injection, and optional response encryption. Do not assume one or the other — let the user decide.
3. **Write the scaffold immediately** — Generate the complete workflow structure from your knowledge. Do not fetch first. Mark specific uncertainties inline (e.g. `// NEED: exact consensus tag for uint256`, `// NEED: verify project.yaml structure`).
4. **Present and iterate** — Give the user the scaffold with simulation commands. Ask them to run `cre workflow simulate`. Then loop:
   - Simulation error → fetch exactly what the error names → fix → ask user to re-run
   - Inline gap → fetch that one specific thing → fill it in → continue
   - No error → done
   - One fetch per gap. Never fetch speculatively to prevent hypothetical errors.
5. **Default to simulation** — Always include simulation commands. Only provide deployment steps if the user explicitly requests it. Remind them deployment requires Early Access approval, a funded wallet, and a linked key.

## Repo Reference Files

Repo reference files are a **reliable source** for working code implementations. Use them when individual doc pages lack sufficient code examples, or when the user explicitly wants a template or runnable implementation.

| File | Repo | When to use |
|------|------|-------------|
| [repo-cre-templates.md](references/repo-cre-templates.md) | cre-templates | Starter templates, building blocks, example workflow patterns |
| [repo-cre-sdk-typescript.md](references/repo-cre-sdk-typescript.md) | cre-sdk-typescript | TypeScript SDK source, HTTP trigger package, SDK examples |
| [repo-cre-sdk-go.md](references/repo-cre-sdk-go.md) | cre-sdk-go | Go SDK source, capability implementations, consensus code |
| [repo-cre-prediction-market-demo.md](references/repo-cre-prediction-market-demo.md) | cre-gcp-prediction-market-demo | Prediction market demo app, end-to-end workflow example |
| [repo-cre-cli.md](references/repo-cre-cli.md) | cre-cli | CRE CLI source code and auto-generated command reference docs |

## Debugging Checklist

Follow these steps when **diagnosing errors or fixing broken CRE code**:

1. **Identify the capability involved** — Determine which CRE capability (HTTP client, EVM client, triggers, secrets, consensus, etc.) is related to the error.
2. **Fetch the relevant doc page** — Find the specific doc page for the capability via the matching reference file. Use the fetch cascade to retrieve it.
3. **Check repo examples** — If the doc page lacks a working implementation, consult the matching `repo-*.md` reference file. If still insufficient, fetch the llms-full text dump from `general.md`.
4. **Check known issues** — Review the Known Issues section below for any matching bug or workaround.
5. **Only then propose a fix** — Do not guess from type signatures, general programming knowledge, or first principles. CRE's WASM runtime and capability interfaces have specific requirements that may differ from standard assumptions.
6. **If a fix fails, re-consult docs** — Do not iterate by guessing alternatives. Go back to step 2 and re-read the docs more carefully, or fetch additional related pages.

## Known Issues

### Secret name/env var substring conflict (CRE CLI v1.1.0)

**Problem:** Secret resolution fails with "secret not found" if the env var name in `secrets.yaml` is a substring or prefix of the secret name (the YAML key). For example, secret name `GEMINI_API_KEY_SECRET` with env var `GEMINI_API_KEY` fails because `GEMINI_API_KEY` is a prefix of `GEMINI_API_KEY_SECRET`.

**Workaround:** Ensure the env var name is never a substring/prefix of the secret name. Use a suffix like `_VAR` on the env var (e.g., `GEMINI_API_KEY_VAR`).

**Observed in:** CRE CLI v1.1.0

**Verification test:** Create a `secrets.yaml` with a secret name that contains the env var as a prefix (e.g., key `MY_SECRET_NAME`, env var `MY_SECRET`). Run simulation. If it fails with "secret not found", the bug still exists. If it succeeds, the bug is fixed and this issue can be removed.

## Tips

- Many topics have separate Go and TypeScript pages. Ask the user which language they're using if unclear, or fetch both.
- For workflow generation tasks, follow the Workflow Generation Checklist above, start with `workflow-building.md`, and supplement with `sdk-reference.md` for API details.
- For onboarding, start with `getting-started.md` then `account-setup.md`.
- For code examples, fetch the specific doc page first (via fetch cascade), then repo reference files if more implementation detail is needed.
- Reference file entries contain enriched descriptions from the docs index. Read them carefully to narrow down which URLs to fetch — don't fetch blindly.
- The full docs index with structured JSON metadata is available at `assets/cre-docs-index.md` for deeper search if reference file descriptions aren't sufficient.
