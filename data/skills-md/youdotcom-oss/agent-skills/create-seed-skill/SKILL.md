---
name: create-seed-skill
description: |
  Scaffold a new integration-type "seed skill" — a SKILL.md with reference assets and prompts.jsonl entries that teach an agent to generate working, testable integration code from scratch.
  - Use when: developer wants to create a new skill for an SDK or framework integration that agents should be able to implement and test
  - Ask first: Is this an integration skill (code generation + tests) or a tool skill (CLI wrapper with no tests)? Only proceed with this skill for integration-type skills.
license: MIT
compatibility: Requires Bun 1.3+ or Node.js 18+
allowed-tools: Read Write Edit Bash(bun:add) Bash(mkdir) Bash(touch) Bash(ln) Bash(bunx)
assets:
  - example-SKILL.md
  - example-path-a.ts
  - example-test.spec.ts
  - example-pyproject.toml
  - example-test_integration.py
metadata:
  author: youdotcom-oss
  version: "1.0.0"
  category: scaffolding
  keywords: seed-skill,integration,scaffold,sdk,framework,eval,prompts
---

# Create a Seed Skill

Scaffold an integration-type skill from scratch. A seed skill is SKILL.md + reference assets + `prompts.jsonl` entries that together teach an agent to sprout a working, testable integration.

## When to Use This

**Integration skills** (use this skill):
- Wrapping an SDK or framework with code generation + real API tests
- The eval question is: "Did the agent write code that calls real APIs and passes tests?"
- Examples: `ydc-ai-sdk-integration`, `teams-anthropic-integration`

**Tool skills** (do NOT use this skill):
- CLI wrappers where the agent runs a command, not writes code
- No test directory, no generated files
- Examples: `youdotcom-cli`

## Decision Point

**Ask the developer first:**

> Is this an integration skill (the agent generates code + tests) or a tool skill (the agent runs a CLI command)?

- **Integration** → Continue with this workflow
- **Tool** → Stop. This skill is not needed for tool skills.

---

## Workflow

### Step 1 — Gather Information

Ask these questions **all at once** (do not ask one by one):

1. **Skill name**: What should it be called? (lowercase, hyphens, e.g. `my-sdk-integration`)
2. **Package(s)**: What npm/pip package(s) does it wrap? Include exact package names.
3. **Language(s)**: TypeScript, Python, or **both**?
   - **Both** means: separate asset files for each language, **two** `prompts.jsonl` entries (one `-typescript`, one `-python`), and **two** `tests/` directories (`tests/<skill-name>-typescript/` and `tests/<skill-name>-python/`), each with a `.gitkeep` file.
   - **One language** means: one set of assets, one `prompts.jsonl` entry, one `tests/<skill-name>/` directory with a `.gitkeep` file.
4. **Path A** (basic): What is the simplest working integration — one function, one API call?
5. **Path B** (extended): What is the natural extension — MCP, streaming, tool filtering, etc.?
6. **Required env vars**: Which API keys are required? (e.g. `MY_API_KEY`, `OPENAI_API_KEY`)
7. **Test query**: What is a factual question with a deterministic, multi-keyword answer that the integration should be able to answer? (See [Choosing a Test Query](#choosing-a-test-query))

### Step 2 — Read Reference Assets

Before writing any code, read the reference assets to understand the required structure:

- [assets/example-SKILL.md](assets/example-SKILL.md) — complete SKILL.md template
- [assets/example-path-a.ts](assets/example-path-a.ts) — TypeScript Path A asset structure
- [assets/example-test.spec.ts](assets/example-test.spec.ts) — TypeScript test asset structure
- [assets/example-pyproject.toml](assets/example-pyproject.toml) — Python project config asset
- [assets/example-test_integration.py](assets/example-test_integration.py) — Python test asset structure

### Step 3 — Create Files

Create all files in one pass. The skill lives in `skills/<skill-name>/`.

**Directory layout:**

```
skills/<skill-name>/
├── SKILL.md
└── assets/
    # TypeScript:
    ├── path-a-<variant>.ts       # Path A integration
    ├── path-b-<variant>.ts       # Path B integration (if applicable)
    ├── integration.spec.ts       # Bun test file
    # Python:
    ├── path_a_<variant>.py       # Path A integration
    ├── path_b_<variant>.py       # Path B integration (if applicable)
    ├── test_integration.py       # pytest file
    └── pyproject.toml            # Python project config (required for uv run pytest)

# Also create (see below):
tests/<skill-name>/               # single language
└── .gitkeep
# — or for both languages —
tests/<skill-name>-typescript/
└── .gitkeep
tests/<skill-name>-python/
└── .gitkeep
```

**Also create the `tests/` eval target directory (or directories) with a `.gitkeep` file** so the directory exists in git before agents write to it:

- Single language: `tests/<skill-name>/.gitkeep`
- Both languages: `tests/<skill-name>-typescript/.gitkeep` **and** `tests/<skill-name>-python/.gitkeep`

```bash
# Single language (adjust path as needed):
mkdir -p tests/<skill-name> && touch tests/<skill-name>/.gitkeep

# Both languages:
mkdir -p tests/<skill-name>-typescript tests/<skill-name>-python
touch tests/<skill-name>-typescript/.gitkeep tests/<skill-name>-python/.gitkeep
```

### Step 4 — Add prompts.jsonl Entry

Append one entry per language to `data/prompts/prompts.jsonl`.

**Single language template** (pick one concrete example — do NOT leave `TypeScript` or `Python` as a placeholder):

TypeScript:
```jsonl
{"id":"<skill-name>","input":["Using the <skill-name> skill, create a working TypeScript <description of Path A> integration. Write flat minimal code with no comments or TSDoc. Write integration tests that call real APIs and assert on meaningful response content. Save everything to the tests/<skill-name> directory.","Extend the integration with <description of Path B>. Write flat minimal code with no comments or TSDoc. Update the integration tests to verify the extended integration also works with a live query."],"metadata":{"cwd":"tests/<skill-name>","language":"typescript"}}
```

Python:
```jsonl
{"id":"<skill-name>","input":["Using the <skill-name> skill, create a working Python <description of Path A> integration. Write flat minimal code with no comments or docstrings. Write integration tests that call real APIs and assert on meaningful response content. Save everything to the tests/<skill-name> directory.","Extend the integration with <description of Path B>. Write flat minimal code with no comments or docstrings. Update the integration tests to verify the extended integration also works with a live query."],"metadata":{"cwd":"tests/<skill-name>","language":"python"}}
```

**Both languages — append TWO entries:**
```jsonl
{"id":"<skill-name>-typescript","input":["Using the <skill-name> skill, create a working TypeScript <description of Path A> integration. Write flat minimal code with no comments or TSDoc. Write integration tests that call real APIs and assert on meaningful response content. Save everything to the tests/<skill-name>-typescript directory.","Extend the integration with <description of Path B>. Write flat minimal code with no comments or TSDoc. Update the integration tests to verify the extended integration also works with a live query."],"metadata":{"cwd":"tests/<skill-name>-typescript","language":"typescript"}}
{"id":"<skill-name>-python","input":["Using the <skill-name> skill, create a working Python <description of Path A> integration. Write flat minimal code with no comments or docstrings. Write integration tests that call real APIs and assert on meaningful response content. Save everything to the tests/<skill-name>-python directory.","Extend the integration with <description of Path B>. Write flat minimal code with no comments or docstrings. Update the integration tests to verify the extended integration also works with a live query."],"metadata":{"cwd":"tests/<skill-name>-python","language":"python"}}
```

**Rules for prompts:**
- Exactly 2 turns per entry
- **Name the language explicitly in Turn 1** ("TypeScript" or "Python") so the agent doesn't guess
- Describe outcomes only — never mention class names, method names, or config keys
- Turn 1: basic integration + tests
- Turn 2: extension + update tests
- `metadata.cwd` must match the `tests/` directory created in Step 3 (the grader reads files from here)
- `metadata.language` must be `typescript` or `python`

### Step 5 — Create Symlink

```bash
ln -s ../../skills/<skill-name> .claude/skills/<skill-name>
```

### Step 6 — Validate

```bash
bunx @plaited/development-skills validate-skill skills/<skill-name>
```

---

## What Makes a Good Seed Skill

### SKILL.md Must Contain

1. **Correct frontmatter** — `name`, `description`, `license`, `compatibility`, `allowed-tools`, `assets` list, `metadata`
2. **Decision point** — brief Path A vs Path B description, one clear question
3. **Install instructions** — exact package name and install command
4. **Complete code templates** — full working examples, not pseudo-code
5. **Security section** — if the integration fetches untrusted web content, include prompt injection warning (W011)
6. **Generate Integration Tests section** — markdown links to all asset files, explicit rules

### Generate Integration Tests Rules (include all of these)

```markdown
**Rules:**
- No mocks — call real APIs
- Assert on keywords from a deterministic query, not just `length > 0`
- Validate required env vars at test start (inside the test function, not at module scope)
- TypeScript: use `bun:test`, dynamic imports inside tests, `timeout: 60_000`
- Python: use `pytest`, import inside test function; always include `pyproject.toml` with `pytest` in `[dependency-groups] dev`
- Run TypeScript tests: `bun test` | Run Python tests: `uv run pytest`
```

### Reference Assets Must

- **Compile and run** — no pseudo-code, no placeholders
- **Include security instructions** in agent `instructions`/`system_prompt`
- **Use the test query** from Step 1 in both the integration files (as the `__main__` example) and the test assertions
- **Assert on keywords** — not just `length > 0`
- **TypeScript**: export a callable function, use dynamic `import()` in tests
- **Python**: define a `main(query: str) -> str` function, use deferred imports inside test functions

---

## Choosing a Test Query

**The real goal**: verify the integration code ran, not that the LLM knows the answer.

Most LLMs can answer factual questions from memory without calling any tool. A query the model can answer without searching doesn't prove the MCP server or SDK tool was invoked — the integration may silently skip the tool and still pass.

**What actually matters:** the test passes only if the *code path* worked — the SDK was initialized, the MCP server was reached, and a response was returned. A keyword assertion that matches typical tool output is better than no assertion, but it doesn't prove the tool fired.

**Practical guidance:**

- **Prefix the query with an explicit instruction to use the tool** — this forces invocation rather than relying on the model's judgment
- Use a query with a stable, multi-keyword answer so you can assert on content, not just `length > 0`
- The LLM-as-judge grader (`scripts/grader.ts`) also evaluates the generated code structure, not just whether keywords appear

**Good examples** (explicit tool instruction + stable keywords):
- `"Search the web for the three branches of the US government"` → assert `legislative`, `executive`, `judicial`
- `"Use web search to find what programming language TypeScript compiles to"` → assert `javascript`
- `"Search the web for the four classical elements"` → assert `earth`, `water`, `fire`, `air`

The `"Search the web for..."` or `"Use [tool name] to find..."` prefix makes tool use an explicit instruction, not an inference — the model must call the tool to follow the prompt.

**Avoid:**
- Plain factual queries ("What are the three branches...") — model may answer from memory, skipping the tool entirely
- "What is the latest news in AI?" — changes daily, no predictable keywords
- "Say hello in one sentence." — no meaningful content assertion possible

---

## Eval Grader Notes

The grader (`scripts/grader.ts`) runs from `metadata.cwd`:

- **TypeScript**: runs `bun test`, scans `**/*.{ts,js}` for generated files
- **Python**: runs `uv run pytest` (requires `pyproject.toml` in the test dir)
- Sends test output + generated file contents to Haiku for LLM-as-judge scoring (0.0–1.0)
- Pass threshold is ~0.65; target is 0.95

Common failure modes to prevent in your SKILL.md:
- **pytest missing**: Always include `pyproject.toml` asset with pytest in dev deps
- **Module-scope env checks**: Python imports should be inside test functions to avoid collection errors
- **Prescriptive prompts**: prompts.jsonl should describe outcomes, not implementation steps
- **Tool introspection**: Never instruct agents to assert on SDK event streams or tool call objects
- **open-ended test queries**: "latest AI news" produces unpredictable content — use factual queries with deterministic keywords

---

## Example: Adding a New Python Integration Skill

Given: wrapping the `httpx` library with You.com search, Python only.

**Files to create:**
```
skills/ydc-httpx-integration/
├── SKILL.md
└── assets/
    ├── path_a_basic.py
    ├── test_integration.py
    └── pyproject.toml

tests/ydc-httpx-integration/
└── .gitkeep
```

**Create the tests directory:**
```bash
mkdir -p tests/ydc-httpx-integration && touch tests/ydc-httpx-integration/.gitkeep
```

**prompts.jsonl entry:**
```jsonl
{"id":"ydc-httpx-integration","input":["Using the ydc-httpx-integration skill, create a working Python application that calls the You.com search API directly with httpx and returns search results. Write integration tests that call the real API and verify the response contains expected keywords. Save everything to the tests/ydc-httpx-integration directory.","Extend the integration to also support content extraction from URLs. Update the integration tests to verify both search and content extraction work with live queries."],"metadata":{"cwd":"tests/ydc-httpx-integration","language":"python"}}
```
