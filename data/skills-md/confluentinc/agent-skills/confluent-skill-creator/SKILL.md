---
name: confluent-skill-creator
description: "Create Confluent-specific skills for external users. Use this skill when users want to create, build, or author a new skill related to Confluent Cloud, Confluent Platform, Apache Kafka, WarpStream, Flink, Connectors, Schema Registry, Tableflow, CDC pipelines, or any Confluent product. Skills can be use-case focused (like data enrichment, CDC to Tableflow, stream processing workflows) or component-specific (like a Flink skill, Schema Registry skill, or Connector skill). Do NOT use this skill when users want to directly use Confluent products (e.g., build a pipeline, write a producer, deploy Flink SQL) — use the appropriate product-specific skill instead. This skill is specifically for creating new skills, not for using existing ones."
compatibility: Requires Python 3.9+, confluent-kafka (with avro/json/protobuf extras), requests, jsonschema, python-dotenv. Needs access to a Confluent environment (Cloud, Platform, local Docker, or WarpStream) for E2E testing.
metadata:
  author: confluent
  version: "1.1.0"
  last_updated: "2026-07-09"
---

# Confluent Skill Creator

A specialized skill creator for building Confluent product skills that are tested against real Confluent environments (local, platform, cloud, or WarpStream).

This skill extends the base skill-creator workflow with Confluent-specific requirements:
- **Flexible scope**: Skills can be use-case focused (e.g., "CDC from PostgreSQL to Iceberg") or component-specific (e.g., "Flink SQL skill", "Schema Registry skill")
- **Platform targeting**: Skills either target a specific platform (named in the skill) or support all platforms with platform-specific reference files
- **Environment testing**: Real E2E tests against local Confluent, Confluent Platform, Confluent Cloud, or WarpStream
- **Safe CRUD operations**: Show full plan and get confirmation before creating/modifying Confluent resources
- **Credential management**: Proper .env file setup for all required credentials
- **Spec compliance**: Created skills validated against the [Agent Skills specification](https://agentskills.io/specification)
- **Smart defaults**: Schema Registry with JSON_SR (schema GUID in header) by default

## Prerequisites

- Python 3.9+
- `confluent-kafka[avro,json,protobuf]`, `requests`, `jsonschema`, `python-dotenv` Python packages (see `scripts/requirements.txt`)
- Access to a Confluent environment (Cloud, Platform, local Docker, or WarpStream) for E2E testing

## When to use this skill

Use this skill when a user wants to create a skill for external users that involves:
- Kafka topics, producers, consumers, or streaming applications
- Flink SQL or stream processing
- Connectors (Debezium CDC, sink connectors, etc.)
- Schema Registry (Avro, JSON Schema, Protobuf)
- Tableflow for data lake integration
- CDC pipelines from databases to data lakes
- Real-time data enrichment or transformation

## Core Workflow

1. **Understand scope and platform targeting** (Confluent-specific)
2. Capture intent and interview
3. Write the skill draft
4. **Validate spec compliance** (Confluent-specific)
5. Set up test environment and credentials (Confluent-specific)
6. Create test cases and run E2E tests (Confluent-specific)
7. Evaluate with viewer
8. Iterate until satisfied
9. Optimize description
10. Package and deliver

---

## Skill Anatomy and Progressive Disclosure

Apply these structural principles to **every skill you create**. They extend the base [skill-creator guidance](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md); the spec-compliance checks in [Step 4](#step-4-validate-spec-compliance) enforce the specifics, while this section is the mental model.

### Anatomy of a skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description required)
│   └── Markdown instructions
└── Bundled resources (optional)
    ├── scripts/     — executable code for deterministic/repetitive tasks
    ├── references/  — docs loaded into context as needed
    └── assets/      — files used in output (templates, icons, fonts)
```

### Progressive disclosure — a three-level loading system

Skills load context in three tiers, so the model only pays for what it needs:

1. **Metadata** (`name` + `description`) — always in context (~100 words). This is the trigger; invest here.
2. **SKILL.md body** — loaded whenever the skill triggers (<500 lines ideal).
3. **Bundled resources** — loaded only as needed (unlimited; scripts can execute without being read into context).

Word counts are approximate — go longer when a skill genuinely needs it.

**Key patterns:**
- Keep SKILL.md under 500 lines. Approaching the limit? Add a layer of hierarchy and point clearly to where the model should look next.
- Reference files explicitly from SKILL.md with guidance on *when* to read each one — never have SKILL.md pull them all in upfront (see [Step 4](#step-4-validate-spec-compliance)).
- For large reference files (>300 lines), include a table of contents at the top.

### Domain organization

When a skill spans multiple domains/frameworks, organize by variant and let the model read only the relevant file — the same pattern as cross-platform Confluent skills (`references/confluent-cloud.md`, `references/warpstream.md`, …):

```
cloud-deploy/
├── SKILL.md          # workflow + variant selection
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```

### Principle of lack of surprise

A skill's behavior must not surprise a user who has read its description. Skills must never contain malware, exploit code, or anything that could compromise system security, and must not facilitate unauthorized access, data exfiltration, or other malicious activity. Benign creative framing (e.g. "roleplay as X") is fine — misleading or malicious skills are not.

---

## Step 1: Understand Scope and Platform Targeting

### Skill scope

Understand what the user wants to build. Skills can be either **use-case focused** or **component-specific** — both are valid.

**Use-case focused** — solves a specific end-to-end problem:
- "Real-time customer order enrichment using Flink SQL"
- "CDC pipeline from PostgreSQL to Iceberg using Debezium and Tableflow"
- "Real-time anomaly detection with Kafka Streams"

**Component-specific** — covers a Confluent component's capabilities:
- "Flink SQL skill"
- "Kafka connector skill"
- "Schema Registry skill"
- "Tableflow skill"

If the user's request is ambiguous, ask:

> "What should this skill cover? It can be a specific use case (e.g., 'CDC pipeline from Postgres to Iceberg') or focused on a component (e.g., 'Flink SQL skill'). What's the scope you have in mind?"

### Platform targeting

After understanding scope, determine platform targeting:

> "Which platforms should this skill support?
> 1. **All supported platforms** (Confluent Cloud, Confluent Platform, Apache Kafka, WarpStream)
> 2. **Specific platform only** (e.g., Confluent Cloud only, WarpStream only)"

**If platform-specific:**
- The platform name MUST appear in the skill's `name` field (e.g., `confluent-cloud-cdc-tableflow`, `warpstream-producer-optimization`)
- The skill description should explicitly state the target platform
- Testing must run against that specific platform

**If cross-platform:**
- The skill name should NOT include a platform prefix
- The generated SKILL.md must include a platform-detection step that asks which platform the user is targeting
- Platform-specific nuances go in `references/<platform>.md` files:
  - `references/confluent-cloud.md` — Cloud-specific config, API keys, managed services
  - `references/confluent-platform.md` — Self-managed specifics, security config
  - `references/apache-kafka.md` — OSS defaults, no managed features
  - `references/warpstream.md` — Object-storage architecture, config overrides
- The SKILL.md points to these conditionally: "If user's target is WarpStream, read `references/warpstream.md` and apply overrides"
- See [PR #27 in agent-skills](https://github.com/confluentinc/agent-skills/pull/27) for the reference pattern

Once you understand scope and platform, proceed to the interview.

---

## Step 2-3: Capture Intent and Write Skill

Follow the base skill-creator process for capturing intent and writing the skill draft. Ask about:

1. **What should this skill enable users to do?**
2. **When should it trigger?** (phrases users would say)
3. **What components are involved?** (topics, schemas, Flink, connectors, etc.)
4. **How should the skill interact with Confluent?** Ask the user:
   > "How should this skill interact with Confluent?
   > 1. **MCP tools** (via Confluent MCP server — discover, manage, operate Confluent resources)
   > 2. **CLI** (Confluent CLI — `confluent kafka topic create`, `confluent flink statement create`, etc.)
   > 3. **REST APIs** (Confluent Cloud API, Schema Registry API, Kafka REST Proxy)
   > 4. **Client libraries** (confluent-kafka-python, Java clients, etc.)
   > 5. **Combination** (e.g., MCP for discovery + CLI for provisioning + client libs for data)"
   
   Based on the answer, the created skill must include:
   - The specific tool/CLI/API calls required, in execution order
   - Any prerequisite setup (MCP server config, CLI login, API key creation)
   - Error handling for each interaction method
5. **What's the expected output?** (working pipeline, sample data, SQL statements, etc.)

When writing the skill:
- Include links to relevant Confluent documentation (docs.confluent.io)
- Reference specific API endpoints, CLI commands, or MCP tool names
- Specify the execution order of tool/CLI/API calls clearly (step-by-step)
- Use bundled scripts for common operations (see `scripts/` directory)
- Explain the "why" behind Confluent best practices
- Link to external docs so the skill automatically stays current. Prefer the `.md` form of a docs.confluent.io page over `.html` when it exists (docs.confluent.io serves clean Markdown at the same path, which is easier for agents to consume), and verify every link resolves before shipping:
  ```markdown
  For Flink SQL syntax, see [Confluent Flink SQL Reference](https://docs.confluent.io/cloud/current/flink/reference/overview.md)
  ```

### Plan-before-execute requirement

The created skill MUST include a plan-before-execute step. Before the skill performs any operations (creating topics, registering schemas, deploying Flink statements, etc.), it must:
1. Present a numbered plan of all operations to the user
2. List which tools/CLI commands/API calls will be made and in what order
3. Wait for explicit user confirmation before proceeding
4. Never execute resource-modifying operations without approval

See [plan-template.md](references/plan-template.md) for the plan format with interaction method examples.

---

## Step 4: Validate Spec Compliance

Before proceeding to testing, validate the created skill against the [Agent Skills specification](https://agentskills.io/specification).

### Frontmatter validation

- `name`: required, max 64 chars, lowercase letters + numbers + hyphens only, no consecutive hyphens, must match parent directory name
- `description`: required, max 1024 chars, must describe both what the skill does AND when to use it
- If platform-specific: platform name must appear in `name` (e.g., `confluent-cloud-cdc-tableflow`)
- `metadata`: must include `author: confluent`, `version` (semver string), and `last_updated` (YYYY-MM-DD)
- `compatibility`: recommended if the skill requires specific packages, CLI tools, or environment access

### Trigger overlap check

Before finalizing the description, check for unintended overlap with existing skills in the repo:

1. Scan `skills/*/SKILL.md` in the target repo and extract each skill's `description:` field
2. Compare the new skill's description keywords against existing skills
3. If significant overlap exists (≥2 non-generic keywords shared), verify the boundary is clear — a user prompt should unambiguously trigger only one skill, not both
4. If the boundary is ambiguous, refine the new skill's description to make the scope distinction clear, or add explicit exclusions where needed

### Structure validation

- SKILL.md body under 500 lines — move detailed content to `references/`
- **Do NOT inline reference file contents into SKILL.md** — references must be lazy-loaded, read only when needed. Every activation pays the full context cost when references are inlined.
- Reference files one level deep from SKILL.md (no nested reference chains)
- Large reference files (>300 lines) include a table of contents at the top
- If SKILL.md exceeds ~200 lines and covers multiple workflows, include a mode-detection table near the top

### Required artifacts

- `evals/evals.json` — at least one test case per primary use case, following this format:
  ```json
  {
    "skill_name": "skill-name",
    "evals": [
      {
        "id": 1,
        "prompt": "realistic user prompt (≥40 chars, specific context, not abstract)",
        "expected_output": "description of success",
        "files": [],
        "assertions": [
          "Specific, verifiable check with a path, identifier, or NOT clause",
          "Another assertion encoding hard-won correctness"
        ]
      }
    ]
  }
  ```
  **Eval quality rules** (enforced by the `confluent-skill-reviewer`):
  - Use `assertions` (array of strings) — this is the repo standard. Do NOT use `expectations`, and do NOT use object-form entries (`[{id, type, description, …}]`); `check_eval_schema.py` flags both as blocking
  - Every eval must include a `files` field (empty array `[]` if no fixtures)
  - Prompts must be ≥40 chars and read like a real user message (specific data shapes, named environments, not just "Build me an X")
  - Assertions must be specific — include file paths, class names, config keys, `NOT` clauses, or quoted CLI flags. Vague assertions like "The code is well written" will be flagged
  - **Synthetic data only** — prompts, fixtures, and sample records must never contain real customer PII or secrets (SSNs, Luhn-valid card numbers, AWS keys, private keys, real emails/phone numbers). Use `example.com`/`.example` domains, `555-01xx` phone numbers, and obvious placeholders. See [PII and synthetic data](references/confluent-best-practices.md#pii-and-synthetic-data); the `confluent-skill-reviewer` blocks violations
- `.env.template` or `credentials.yaml.template` if the skill requires credentials
- `references/<platform>.md` files if cross-platform (one per supported platform)

### Run validation

```bash
# If skills-ref is available
skills-ref validate ./created-skill
```

**If validation fails:** fix issues and re-validate. Do not proceed to testing until the skill passes.

---

## Step 5: Set Up Test Environment and Credentials

### Choose test environment

Ask the user which environment to test against:

> "Which Confluent environment should we test against?
> 1. **Local Confluent** (Docker, for development)
> 2. **Confluent Platform** (self-managed on-prem)
> 3. **Confluent Cloud** (managed SaaS)
> 4. **WarpStream** (Kafka-compatible, object-storage-backed)
>
> Note: If this skill targets a specific platform, we must test against that platform."

**Important rule:** If the skill is designed for a specific platform, tests MUST run against that platform.

### Security: credential file handling

Credentials may live in a `.env` file or a YAML file (`credentials.yaml`) — the rules below apply to whichever format the skill uses.

**CRITICAL: Never read, display, or log credential files (`.env` or `credentials.yaml`) or their contents.** See [confluent-best-practices.md](references/confluent-best-practices.md) for the full security policy. Key rules:
- Never use `cat`, `Read`, `head`, `grep`, etc. on `.env` or `credentials.yaml`
- For `.env`: reference variables by name (e.g., `$BOOTSTRAP_SERVERS`), never read their values; verify with `test -n "$CLUSTER_API_KEY"`
- For `credentials.yaml`: load it inside the script/process that consumes it (e.g., a YAML parser at runtime), never echo parsed values to logs or stdout
- Add the credential file to `.gitignore` (`.env`, `credentials.yaml`)
- Generated skills **must** include this same guardrail

**CRITICAL: Use synthetic data only — never commit real customer PII or secrets.** Eval prompts, fixtures, sample records, and reference examples must use fabricated data (`example.com` emails, `555-01xx` phone numbers, obviously fake ids). Never embed real SSNs, Luhn-valid payment card numbers, AWS keys, or private key material. See [PII and synthetic data](references/confluent-best-practices.md#pii-and-synthetic-data). You can verify a skill directory with `python3 skills/confluent-skill-reviewer/scripts/scan_pii.py <skill-path>` before packaging.

### Set up credentials

See [credentials reference](references/credential-templates.md) for environment-specific credential templates — available in both `.env` and YAML (`credentials.yaml`) form — covering Kafka, Schema Registry, Flink, Tableflow, and Connectors. Pick whichever format fits the skill; YAML is convenient for nested/structured config, `.env` for flat shell-style variables.

---

## Step 6: Create Test Cases and Run E2E Tests

### Test case structure

Each test case should exercise the full use case end-to-end. See [plan-template.md](references/plan-template.md) for the CRUD operations plan format. Present the plan and **wait for user confirmation** before creating any resources.

### Schema Registry defaults

- **Default format**: JSON with Schema GUID in header (`JSON_SR`)
- **Alternative formats**: Avro, Protobuf
- Ask user if they want to change from JSON_SR: "This will use JSON serialization with Schema Registry (schema GUID in header) by default. Do you want to use Avro or Protobuf instead?"
- For Schema GUID in Header configuration details, see [schema-guid-header.md](references/schema-guid-header.md)

### Compute pool check (for Flink skills)

Before running Flink operations, verify a compute pool is available:
```python
python scripts/check_compute_pool.py --pool-id $FLINK_COMPUTE_POOL_ID
```
If no pool is available or capacity is full, notify the user and skip Flink tests.

### Running the tests

Use the base skill-creator workflow for running tests (spawn subagents with skill vs without skill), but adapt for Confluent:

**With-skill run:**
```
Execute this task:
- Skill path: <path-to-skill>
- Task: <eval prompt>
- Environment: .env file at <workspace>/.env
- Save outputs to: <workspace>/iteration-<N>/eval-<ID>/with_skill/outputs/
- Outputs to save:
  - Consumed data from output topic
  - SQL statements executed (if applicable)
  - Schema definitions
  - Verification logs
```

**Baseline run:** Same prompt, no skill, same environment.

### Bundled scripts

For common operations, use the bundled scripts in `scripts/`:

- `check_compute_pool.py` — Verify Flink compute pool availability
- `produce_data.py` — Produce JSON_SR-encoded data to topics
- `consume_and_verify.py` — Consume data and verify against expectations
- `register_schema.py` — Register schemas with Schema Registry
- `cleanup_resources.py` — Clean up topics, schemas, Flink statements (local only)

**If script execution is denied** (e.g., headless/non-interactive sessions have no approval mechanism) — fall back to the manual steps below rather than stalling silently:

- `check_compute_pool.py` → manually check pool status via the `confluent flink compute-pool` CLI or the Cloud Console
- `produce_data.py` → manually produce JSON_SR-encoded records via the `confluent kafka topic produce` CLI, or a one-off producer snippet described in prose
- `consume_and_verify.py` → manually consume via `confluent kafka topic consume` and compare the count/contents against expectations by hand
- `register_schema.py` → manually register the schema via `confluent schema-registry schema create` or the Schema Registry UI
- `cleanup_resources.py` → manually delete topics/schemas/statements via their respective `confluent` CLI delete commands (Cloud), or skip cleanup if the environment is ephemeral (local only)

Include relevant scripts in the created skill's `scripts/` directory when packaging — and require the created skill to document this same fallback if it ships its own scripts.

---

## Step 7-8: Evaluate and Iterate

Follow the base skill-creator evaluation workflow:

1. While tests run, draft assertions (if applicable)
2. Capture timing data when runs complete
3. Grade each run
4. Aggregate benchmark
5. Launch eval viewer
6. Review feedback with user
7. Improve skill based on feedback

**Confluent-specific assertions** — good assertions check:
- Correct number of messages produced/consumed
- Schema compatibility (e.g., forward/backward compatible)
- Flink statement syntax is valid
- Output data matches expected enrichment
- No data loss or duplication
- Topics created with correct configuration

---

## Step 9-10: Optimize Description and Package

### Description optimization

After the skill works well, optimize the triggering description. Focus on:
- Specific use case keywords (enrichment, CDC, Tableflow, etc.)
- Confluent product names (Flink, Kafka, Schema Registry, etc.)
- Common user phrases ("set up a pipeline", "stream changes from", etc.)
- If platform-specific: include platform name in triggers

### Packaging

Bundle the skill with:
- `SKILL.md` with external docs links (under 500 lines), including:
  - `metadata.author: confluent` for all Confluent-created skills
  - `metadata.version` (semver string, e.g., "1.0")
  - `metadata.last_updated` (YYYY-MM-DD)
  - `compatibility` field if the skill has environment or package requirements
- `evals/evals.json` — at least one test case per primary use case
- `references/` — platform-specific files (if cross-platform) and any Tier 3 reference content
- `scripts/` — relevant bundled scripts
- `.env.template` or `credentials.yaml.template` for credentials

**Validation gate:** Before delivering, run `skills-ref validate ./created-skill` one final time. Do not deliver a skill that fails validation.

### PR submission checklist

When the skill is being added to a Confluent skills repo (e.g., `confluentinc/agent-skills`), ensure:

1. **README updated** — add the new skill to the repo's skill table in README.md
2. **Evals pass at 90%+** — run evals and include the score in the PR description
3. **SME reviewer** — identify and assign a subject-matter expert for the skill's domain
4. **DTX/DevRel reviewer** — assign a reviewer from the DTX or Developer Advocates team

These are required gates in the PR template and will be checked by the `confluent-skill-reviewer`.

---

## Reference Files

- [credential-templates.md](references/credential-templates.md) — Environment-specific credential templates (`.env` and YAML)
- [schema-guid-header.md](references/schema-guid-header.md) — Schema GUID in Header configuration
- [plan-template.md](references/plan-template.md) — CRUD operations plan format
- [confluent-best-practices.md](references/confluent-best-practices.md) — Security, error handling, documentation, and testing guidelines
- [example-enrichment.md](references/example-enrichment.md) — Complete enrichment skill walkthrough
- Base skill-creator documentation for general patterns
