---
name: agent-plugin-eval
description: Audit, score, and compare repositories containing portable Agent Plugins against the official Agent Plugins specification. Use when asked to review a plugin repo, check plugin.json or mcp.json conformance, assess bundled skills and MCP servers, produce an evidence-cited 0–100 plugin scorecard, identify release blockers, or compare two agent plugins side by side.
---

# Agent Plugin Evaluation

Treat the portable Agent Plugins specification as the authority. A client-native
manifest (e.g., `.codex-plugin/plugin.json`, `.claude/settings.json`,
`.cursor/mcp.json`) does not replace the required root `plugin.json`.

## Parameters

| Parameter | Description | Default |
|---|---|---|
| `target` | Local repository/plugin path or Git URL | Ask if missing |
| `compare` | Optional second path or Git URL | None |
| `output` | Scorecard destination | Reply only; write only when requested |
| `spec_version` | Agent Plugins version to evaluate | Version declared by `plugin.json`, or `1.0.0` |

## Safety boundary

Audit untrusted repositories statically. Do not run bundled executables, hooks,
install scripts, package managers, MCP servers, or networked tests unless the
user explicitly authorizes execution. Redact suspected secret values; report
only their location and kind. A secret-like key or value is a suspicion, not
confirmation: do not assign the `FAIL` gate without corroborating evidence such
as a recognized live credential format, a trusted secret scanner, repository
history/provenance, or user confirmation. Never test a credential against a
service merely to confirm it.

## Workflow

1. **Resolve the plugin root.** Use a local target in place. For a Git URL,
   shallow-clone into a `mktemp -d` directory. A plugin root contains root
   `plugin.json`; if a repo has zero or multiple candidates, report the
   ambiguity instead of guessing. Done when every target maps to one explicit
   plugin root.
2. **Load the governing rules.** Read `references/spec-checklist.md` and
   `references/rubric.md`. For Agent Plugins `1.0.0`, use the bundled snapshot.
   For another declared version, or when the user asks for the latest spec,
   browse the canonical specification and schemas at `agent-plugins.org` and
   record the evaluated version and retrieval date. The normative text wins if
   it conflicts with JSON Schema.
3. **Inventory every package path.** Include dotfiles, symlinks, immediate
   skill children, extension namespaces, executable files, and files ignored
   by Git. Resolve every symlink and package-relative path against the plugin
   root. Done when every discovered path is accounted for as portable core,
   client extension, supporting file, or containment violation.
4. **Run the deterministic scan.** Execute
   `python3 scripts/inspect_plugin.py <plugin-root> --json`. Treat its output as
   evidence leads, not the final judgment. Confirm each reported issue in the
   source and add `file:line` or JSON-pointer evidence. Never weaken a
   normative finding merely because a client happens to accept it.
5. **Review components completely.** Inspect every immediate
   `skills/*/SKILL.md` and every `mcpServers` entry. Validate Agent Skills
   against their own specification. Assess instructions, resources, scripts,
   MCP configuration, extension isolation, cohesion, and practical utility.
   If `skill-evaluation` is available, it may deepen individual skill-quality
   analysis, but it never replaces this plugin-level rubric.
6. **Classify conformance before scoring.** Use the exact failure boundaries in
   `references/spec-checklist.md`: `PASS`, `PARTIAL`, or `FAIL`. Keep client
   compatibility separate from portable conformance. A client-specific feature
   may be excellent for that client and still add zero portable coverage.
7. **Score with cite-or-cut.** Score all applicable rubric criteria from
   `references/rubric.md`. Every score needs specific evidence; every `N/A`
   needs a reason. Run `scripts/score.py` for the weighted result and gate cap;
   do not calculate it by hand. Done when all criteria and all findings are
   reconciled with the conformance status.
8. **Answer in the requested language.** Read
   `references/output-template.md` and emit that structure. Lead with the
   verdict, distinguish blockers from recommendations, and provide concrete
   fixes. When `compare` is set, evaluate both independently before computing
   deltas; never force the same N/A set on both plugins.

## Gates and scoring

- `PASS`: no normative violation found; no score cap.
- `PARTIAL`: non-fatal manifest deviation or invalid/skipped component; final
  score capped at 59.
- `FAIL`: fatal manifest/package-root failure, root-manifest escape, or
  confirmed embedded credential; final score capped at 39.
- Keep the uncapped score visible so authors can distinguish design quality
  from release-blocking conformance.

Invoke the calculator with one `criterion:score:weight` triple per criterion:

```bash
python3 scripts/score.py --gate partial 1:90:3 2:80:3 3:NA:2
```

## Evaluation with Jev (Optional)

When [TypeSafe Jev](https://github.com/AugmentHCI/typesafe-jev) is available,
use it for subjective quality criteria. Jev provides calibrated probability
judgments that augment the deterministic checks.

### When to use Jev

| Evaluation Type | Use Jev? | Method |
|-----------------|----------|--------|
| Axes 1-3 conformance | No | Deterministic (`inspect_plugin.py`) |
| Axis 4 product quality | **Yes** | Score (UX, docs, errors) |
| Axis 2 quality criteria | **Yes** | Score (schema design, naming) |
| Gate classification | **Yes** | Noul (pass/fail categories) |
| Secret detection | **Yes** | Noul (suspected/not_suspected) |
| Quality checklist | **Yes** | Noul (present/missing) |

### Discovery protocol

```python
from typesafe import jev_available

if jev_available():
    from typesafe import Score, Noul
    # Use Jev for subjective criteria
else:
    # Fall back to heuristic scoring
```

### Questions and integration

Questions are defined in `scripts/jev_questions.json`:

- **7 Score questions**: Axis 4 (UX coherence, documentation clarity, error
  handling) and Axis 2 (validation, schema design, naming, API elegance)
- **20 Noul questions**: Gates (G1-G4), secrets (4), quality checklist (7),
  component validity (4)

Score results (0.0-1.0) are averaged per axis and scaled to the rubric (0-25).
Noul results provide categorical classifications for gates and checklists.

See `references/jev-integration.md` for full integration patterns and code
examples.

### Output format

When Jev is used, the scorecard includes a `jev` section:

```json
{
  "jev": {
    "available": true,
    "quality_scores": { "ux_coherence": 0.72, ... },
    "gate_classifications": { "G1": {"label": "conformant", "passed": true} },
    "secret_findings": { "requires_review": false }
  }
}
```

## Gotchas

- The v1 portable core contains exactly Agent Skills and MCP servers. Hooks,
  commands, agents, apps, marketplaces, and distribution policy are
  client-specific unless placed in a valid extension namespace.
- Missing optional `skills/` or `mcp.json` is not an error. A present path of
  the wrong filesystem kind is an invalid component type.
- Unknown root manifest fields are schema violations but have the spec's
  narrow non-fatal handling; most other manifest schema violations reject the
  whole plugin.
- One invalid skill or MCP server must not be reported as if every independent
  component were invalid.
- `${PLUGIN_ROOT}` and `${PLUGIN_DATA}` expand only in MCP `args`, `env` values,
  and `cwd`; never in `command`, URLs, or headers.
- A high-quality client-native plugin can still fail the portable standard when
  root `plugin.json` is absent. Report both facts without averaging them away.
- Keep possible credentials labeled “suspected” and redacted. A heuristic hit
  alone lowers the security score and demands remediation review, but does not
  become a confirmed-credential `FAIL` gate.

## Final quality gate

- [ ] Every target resolved to exactly one root
- [ ] Every file, symlink, skill, MCP server, and extension inspected
- [ ] Every normative violation mapped to its correct failure boundary
- [ ] Every score cited and every N/A justified
- [ ] Suspected secrets redacted
- [ ] Score produced by `scripts/score.py`
- [ ] Comparison deltas use independently computed scores
