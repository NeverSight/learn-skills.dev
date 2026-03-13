---
name: platonic-init
description: Initialize the Platonic Coding system for any project. Scaffolds specs infrastructure (.platonic.yml, RFC templates, impl guide directory) and scans existing codebases to recover missing conceptual and architecture design specs as Draft RFCs. Use when adopting platonic coding for a new or existing project.
license: MIT
metadata:
  version: "1.1.0"
  author: "Xiaming Chen"
  category: "initialization"
---

# Platonic Init

Initialize the **Platonic Coding** system for any project -- greenfield or existing codebase.

## When to Use This Skill

Use this skill when you need to:

- **Bootstrap** a new project with the Platonic Coding infrastructure
- **Adopt** the Platonic Coding paradigm for an existing codebase
- **Recover** missing design specs from code that was built without formal specifications
- **Set up** `.platonic.yml` config, specs directory, templates, and impl guide scaffolding

Keywords: init, bootstrap, setup, adopt, recover, specs, RFC, platonic coding, project setup

## What This Skill Does

This skill operates in one of two modes:

### Mode 1: Greenfield Init (no existing code)

Scaffolds the Platonic Coding infrastructure only:

- `.platonic.yml` project config at project root
- `docs/specs/` directory with RFC infrastructure and templates
- `docs/impl/` directory for implementation guides
- `docs/drafts/` directory for Phase 0 design drafts

### Mode 2: Recovery Init (existing codebase)

Scaffolds infrastructure **and** recovers design specs from the existing code:

1. Scaffold directories, config, and templates
2. Scan the codebase systematically (5 phases)
3. Plan a modular RFC dependency graph (present to user for confirmation)
4. Generate Draft RFCs capturing the system's conceptual and architecture design
5. Populate rfc-index.md, rfc-namings.md, and rfc-history.md

## Core Concepts

### Three Spec Kinds

Platonic Coding recognizes three kinds of RFC specifications:

| Kind | Purpose | Contains | Does NOT Contain |
|------|---------|----------|------------------|
| **Conceptual Design** | Vision, principles, taxonomy, invariants | Design philosophy, abstractions, terminology | Schemas, APIs, code |
| **Architecture Design** | Components, layers, data flow, constraints | Module responsibilities, dependency rules, abstract schemas | Concrete API signatures, language-specific code |
| **Impl Interface Design** | API contracts, naming conventions, signatures | Type definitions, interface contracts, error patterns | Implementation details, algorithms |

### Modular RFC Recovery

Recovery produces a **small graph of focused RFCs** (default maximum: 5), not monolithic documents:

- **Exactly 1** system-wide Conceptual Design spec (RFC-0001)
- **1 per major subsystem** Architecture Design spec (depends on RFC-0001)
- **Impl Interface specs** only on explicit user request

The agent MUST present the proposed RFC graph to the user before generating any specs.

## Available Operations

| Operation | Reference File | Purpose |
|-----------|----------------|---------|
| **Scaffold** | `scaffold-project.md` | Create directories, config, templates |
| **Scan** | `scan-project.md` | Systematically analyze existing codebase |
| **Plan Modular Specs** | `plan-modular-specs.md` | Propose RFC dependency graph from scan results |
| **Recover Conceptual** | `recover-conceptual.md` | Generate conceptual design spec from code |
| **Recover Architecture** | `recover-architecture.md` | Generate architecture design spec from code |
| **Recover Impl Interface** | `recover-impl-interface.md` | Generate impl interface design spec from code |

See [references/REFERENCE.md](references/REFERENCE.md) for detailed operation guides.

## Output Structure

```
<project-root>/
├── .platonic.yml                   # Project config (auto-discovered by all platonic skills)
├── docs/specs/                    # Default; user-configurable
│   ├── rfc-standard.md             # RFC process & conventions (includes spec kinds)
│   ├── rfc-history.md              # Change history
│   ├── rfc-index.md                # Spec index
│   ├── rfc-namings.md              # Terminology reference
│   ├── RFC-0001.md                 # [Recovery] Conceptual Design (Draft)
│   ├── RFC-0002.md                 # [Recovery] Architecture Design (Draft)
│   └── templates/                  # Spec templates for future RFCs
│       ├── rfc-template.md
│       ├── conceptual-design.md
│       ├── architecture-design.md
│       └── impl-interface-design.md
├── docs/impl/                      # Default; user-configurable
│   └── README.md
└── docs/drafts/                    # Default; user-configurable
    └── README.md
```

## Templates

Templates are provided in `assets/` for all generated files:

- `platonic.yml.template` - Project configuration
- `rfc-standard.md.template` - RFC process with spec kinds guidance
- `rfc-history.md.template`, `rfc-index.md.template`, `rfc-namings.md.template` - Infrastructure
- `rfc-template.md` - Generic RFC template
- `conceptual-design.md.template` - Conceptual design spec template
- `architecture-design.md.template` - Architecture design spec template
- `impl-interface-design.md.template` - Implementation interface design spec template
- `impl-guide-template.md` - Implementation guide template
- `impl-readme.md.template`, `drafts-readme.md.template` - Directory READMEs

Templates use `{{PLACEHOLDER}}` syntax. Common placeholders: `{{PROJECT_NAME}}`, `{{LANGUAGE}}`, `{{FRAMEWORK}}`.

## Usage Examples

### Example 1: Initialize a New Project

```
Use platonic-init to set up Platonic Coding for my new project "Acme".
Language is TypeScript, framework is Next.js. Specs go in docs/specs/.
```

### Example 2: Adopt Platonic Coding for Existing Code

```
Use platonic-init to recover design specs for this existing project.
Scan the codebase and propose what RFCs to generate.
```

### Example 3: Recovery with Custom Paths

```
Use platonic-init in recovery mode. Put specs in docs/rfcs/
and impl guides in docs/design/. Generate up to 4 RFCs.
```

## Best Practices

1. **Always read the reference file** for each operation before executing it
2. **Review recovered specs**: All generated RFCs are Draft -- review and refine with platonic-specs
3. **Confirm the RFC graph**: The agent proposes a modular spec plan; confirm before generation
4. **Keep it small**: Fewer, focused specs are better than many overlapping ones
5. **Use platonic-workflow** for future development after initialization

## Dependencies

- Read/write access to project directories
- Markdown file support
- For recovery mode: ability to scan and read source code files

## Integration with Other Skills

- **platonic-specs**: Use `refine` operation post-init to validate and update recovered specs
- **platonic-workflow**: After init with recovery, use Phase 2 to implement the recovered RFCs; for brand-new features, start at Phase 0 (conceptual design)
- **platonic-impl**: Create implementation guides and implement code from recovered RFC specs
- **platonic-code-review**: Review code against recovered specs
