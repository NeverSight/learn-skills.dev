---
name: flow-prune-agent-setup
description: "Audit and tidy a coding agent's configuration: instructions, memory, settings, hooks, MCP servers and plugins. Use when that setup has grown noisy, conflicting or stale. Feeds `flow-handoff`."
metadata:
  stage: operate
---

# Prune an agent setup

Find stale or conflicting instructions and configuration, then apply only the cleanup the user authorizes. Judge by ownership, active scope, and effective behavior, not age.

## Phase 1: Discover effective sources

Identify host and version, active project or profile, CLI overrides, and managed layers before attributing behavior to a file. Check the host's current official docs for locations and precedence; schemas differ between hosts and versions, and not every settings file is user-owned. Never print credentials.

- **Instructions:** every instruction file the host loads (for example AGENTS.md or a host-specific equivalent, rules directories) at user, project and local scope.
- **Configuration:** each settings layer (user, project, local, managed), including permissions, hooks, enabled plugins or extensions, and MCP server entries. Treat managed, system and CLI overrides as read-only context.
- **Capabilities:** skills, agents and plugins in user and project directories, plus any memory store.
- Locate skill ownership through its supported manager (plugin manager, `npx skills`, or the owning installer).

## Phase 2: Four audits

1. **Instructions:** stale paths, redundant or contradictory rules, procedures that belong in a focused skill, rules tooling already enforces. Verify references first.
2. **Memory:** outdated facts and duplicates, with source, age, and intended consumer. Unknown relevance is not evidence for deletion. Reconcile any memory index.
3. **Settings and integrations:** effective values, obsolete hooks or MCP servers, conflicting scopes. Distinguish allow, ask, and deny entries; removing a protective rule changes behavior even when the tool looks unused.
4. **Skills, agents, and plugins:** overlap, routing quality, inactive workflows, ownership, actual discovery. Inspect the host's enabled-plugins setting (for example `enabledPlugins` in settings.json) where it has one; do not assume that schema elsewhere. Separate installed links from source directories and host-owned bundles.

Run parallel read-only audits only when authorized and independent. Merge into one punch list: item, source and owner, reason, evidence, consequence, confidence, proposed action. Label uncertain candidates and false positives.

## Phase 3: Apply the requested scope

- Audit-only request: report the punch list and stop.
- Explicit cleanup: perform the authorized reversible edits without re-asking per item. Ask only about consequential uncertainty or unauthorized destructive actions. Never auto-delete unknown assets.
- Back up changed settings, preserve unrelated keys, and validate the resulting format and effective behavior.
- Use the owning installer or plugin manager. Unlinking an install is not deleting its source. Complete an explicitly requested user-owned skill removal through the supported mechanism instead of handing the user an unsafe shell command. Never edit managed or plugin-owned sources directly.

## Phase 4: Confirm behavior

Reinspect active values and discovery. Explain removed and retained items and remaining conflicts. Distinguish disk state from cached session or UI state; do not keep rewriting correct files because the current session has not refreshed.

## Anti-patterns

- Treating old or unused entries as proven obsolete.
- Auditing one settings file and claiming full effective coverage.
- Removing deny rules, plugin-owned assets, caches, or history under a vague cleanup request.
- Repeated approval questions after the user named the exact cleanup.

## Done when

- Findings rest on effective scope, provenance, and a concrete behavioral consequence.
- Authorized changes validate and preserve unrelated setup; uncertain items stay explicit.
- Actual discovery and effective state are checked, or the limits are reported.

Use `flow-handoff` only if unresolved decisions or a later session need a continuation record.
