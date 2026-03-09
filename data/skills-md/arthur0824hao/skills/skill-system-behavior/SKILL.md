---
name: skill-system-behavior
description: "BDD-style behavior specification engine for the skill system. Use when: (1) defining a new skill's behavior before implementation, (2) validating a spec against the schema, (3) generating a behavior contract (Mermaid DAG) from a spec, (4) running structural acceptance tests against a built skill. Workflow: Spec → Test → Develop → Contract."
license: MIT
metadata:
  os: linux, macos, windows
---

# Skill System Behavior — Spec Engine

Define **what** a skill does before writing **how**. This skill enforces a BDD-style workflow:

```
SKILL.spec.yaml  →  Acceptance Tests  →  Implementation  →  SKILL.behavior.yaml (generated)
     (WHAT)           (VERIFY)              (HOW)              (DOCUMENT)
```

## Spec Format

Every skill's behavior is defined in `SKILL.spec.yaml`:

```yaml
schema_version: 1
skill_name: my-skill
description: "What this skill does"

operations:
  - name: do-something
    intent: "Why this operation exists"
    inputs: [...]
    outputs: [...]
    constraints: ["Must not...", "Must always..."]
    expected_effects: [...]

acceptance_tests:
  structural:
    - id: manifest-valid
      assert: "manifest exposes all operations"
  behavioral:
    - id: happy-path
      given: "Valid input"
      when: "do-something is called"
      then: "Returns expected output"
```

Full schema: `schema/spec-v1.yaml`

## Operations

### create-spec

Scaffold a new `SKILL.spec.yaml` from the schema template.

1. Read `schema/spec-v1.yaml` for the format
2. Ask user for: skill name, description, operations (name + intent + inputs/outputs)
3. Generate `SKILL.spec.yaml` in the target skill directory
4. Include placeholder acceptance tests (structural defaults + behavioral stubs)

### validate-spec

Validate a `SKILL.spec.yaml` against the v1 schema.

1. Read the target `SKILL.spec.yaml`
2. Check required fields: `schema_version`, `skill_name`, `description`, `operations`
3. For each operation: verify `name`, `intent`, at least one input or output, constraints present
4. For acceptance_tests: verify structural tests include `manifest-valid` and `scripts-exist`
5. Report: PASS with summary, or FAIL with specific violations

Run via: `python3 scripts/validate_spec.py <path-to-SKILL.spec.yaml>`

### verify-structural

Run structural acceptance tests against a built skill.

1. Read the skill's `SKILL.spec.yaml` for declared operations
2. Read the skill's `SKILL.md` for the `skill-manifest` block
3. Verify:
   - Every operation in spec has a matching operation in manifest
   - Every entrypoint script referenced in manifest exists on disk
   - `skills-index.json` includes this skill's capabilities
4. Report: checklist with PASS/FAIL per test

### generate-contract

Generate a `SKILL.behavior.yaml` (Mermaid DAG) from a completed spec + implementation.

1. Read `SKILL.spec.yaml` for operations, inputs, outputs, constraints
2. Map operations → stages in a flowchart
3. Map inputs → input nodes, outputs → output nodes
4. Map constraints → error paths
5. Write `SKILL.behavior.yaml` with embedded Mermaid diagram

This is the **last step** — only run after implementation is complete and tests pass.

## Workflow Integration

### For skill-system-creator (updated flow)

```
1. Understand the skill (examples, triggers)
2. Create spec         → skill-system-behavior:create-spec
3. Validate spec       → skill-system-behavior:validate-spec
4. Write tests         → define acceptance criteria from spec
5. Initialize skill    → skill-system-creator:init
6. Implement skill     → edit SKILL.md, scripts, references
7. Verify structural   → skill-system-behavior:verify-structural
8. Generate contract   → skill-system-behavior:generate-contract
9. Package             → skill-system-creator:package
```

### Spec as Single Source of Truth

- `SKILL.spec.yaml` — the authoritative definition (human-written, reviewed)
- `SKILL.md` + manifest — implementation (must conform to spec)
- `SKILL.behavior.yaml` — generated documentation (derived from spec)

## Guidelines

- Write specs in the language your team uses (English, Chinese, mixed — consistency within a spec)
- Constraints are **invariants**: if violated, the skill has a bug
- `intent` describes WHY, not HOW — implementation details go in SKILL.md
- Acceptance tests use Given/When/Then for behavioral, assert-statements for structural
- Generate contracts only after all tests pass — contracts are docs, not specs

```skill-manifest
{
  "schema_version": "2.0",
  "id": "skill-system-behavior",
  "version": "2.0.0",
  "capabilities": ["spec-create", "spec-validate", "spec-verify", "contract-generate", "skill-graph-build"],
  "effects": ["fs.read", "fs.write", "proc.exec"],
  "operations": {
    "create-spec": {
      "description": "Scaffold a new SKILL.spec.yaml from the schema template.",
      "input": {
        "skill_name": { "type": "string", "required": true, "description": "Name of the skill to spec" },
        "skill_dir": { "type": "string", "required": false, "description": "Target directory (default: skills/<skill_name>)" }
      },
      "output": {
        "description": "Path to created SKILL.spec.yaml",
        "fields": { "path": "string" }
      },
      "entrypoints": {
        "agent": "Read schema/spec-v1.yaml, then scaffold SKILL.spec.yaml in skill_dir"
      }
    },
    "validate-spec": {
      "description": "Validate a SKILL.spec.yaml against the v1 schema.",
      "input": {
        "spec_path": { "type": "string", "required": true, "description": "Path to SKILL.spec.yaml" }
      },
      "output": {
        "description": "Validation result with pass/fail and violations list",
        "fields": { "status": "string", "violations": "array" }
      },
      "entrypoints": {
        "unix": ["python3", "scripts/validate_spec.py", "{spec_path}"],
        "windows": ["python", "scripts/validate_spec.py", "{spec_path}"]
      }
    },
    "verify-structural": {
      "description": "Run structural acceptance tests against a built skill.",
      "input": {
        "skill_dir": { "type": "string", "required": true, "description": "Path to skill directory" }
      },
      "output": {
        "description": "Test results checklist",
        "fields": { "status": "string", "results": "array" }
      },
      "entrypoints": {
        "unix": ["python3", "scripts/verify_structural.py", "{skill_dir}"],
        "windows": ["python", "scripts/verify_structural.py", "{skill_dir}"]
      }
    },
    "generate-contract": {
      "description": "Generate SKILL.behavior.yaml (Mermaid DAG) from a completed spec.",
      "input": {
        "skill_dir": { "type": "string", "required": true, "description": "Path to skill directory with SKILL.spec.yaml" }
      },
      "output": {
        "description": "Path to generated SKILL.behavior.yaml",
        "fields": { "path": "string" }
      },
      "entrypoints": {
        "unix": ["python3", "scripts/generate_contract.py", "{skill_dir}"],
        "windows": ["python", "scripts/generate_contract.py", "{skill_dir}"]
      }
    },
    "build-graph": {
      "description": "Build a cross-skill dependency graph from SKILL.spec.yaml files.",
      "input": {
        "skills_dir": { "type": "string", "required": false, "description": "Root directory to scan (default: ./skills)" },
        "output_format": { "type": "string", "required": false, "description": "mermaid, json, or sql" }
      },
      "output": {
        "description": "Graph output in the requested format",
        "fields": { "graph": "string|json" }
      },
      "entrypoints": {
        "unix": ["python3", "scripts/build_graph.py", "--skills-dir", "{skills_dir}", "--format", "{output_format}"]
      }
    }
  },
  "stdout_contract": {
    "last_line_json": true
  }
}
```
