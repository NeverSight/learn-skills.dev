---
name: plugin-fleet-sweep
description: Use when the DSH host itself has been upgraded (or is about to be) and the whole installed fleet of Web/client plugins must be checked against the new host - one or more surfaces broke, vanished, or need their compatibility re-verified and re-released. Also use after a host upgrade to sweep for silent breaks before the user reports them, and to run the per-plugin fix/release loop (branch, bump, changelog, tag, mirrors).
---

# Sweep a Plugin Fleet Across a DSH Host Upgrade

A host upgrade changes the contracts every plugin rides on at once. The unit
of work is not one plugin: it is the fleet, swept in a fixed order, with one
verdict per plugin and one release loop per broken plugin. The sweep runs
against the REAL upgraded host - sources and Node-based tests passing prove
nothing about browser-engine and runtime-surface changes.

## Standing rules

1. **Verify on the target host, not in sources.** A plugin "loads" when its
   client bundle is served, its CSS `style[data-plugin]` tag exists, and zero
   `slot entry crashed` / activation-failure records appear. A plugin
   "works" only when its surface marker is in the DOM and its expected
   requests fire. Record which of the two you have proven.
2. **One static sweep first, cheaply.** Grep every plugin source for the
   APIs the new host renamed or removed (from the target version's corridor
   cards in `plugin-upgrade/references/`) before touching a browser. Static
   hits are already verdicts: broken-until-fixed.
3. **Absence of errors is weak evidence.** A surface whose UI is
   interaction-gated (appears only after a paste, a file operation, a focus
   event) shows nothing in a idle sweep. For each plugin, know its trigger
   and either simulate it or mark the verdict "loaded, interaction path not
   exercised" instead of claiming success.
4. **Fix and release per plugin, never as a fleet commit.** Each broken
   plugin gets its own branch-or-main commit, version bump, changelog row,
   tag, and mirror push (the repositories' own mirror flow; `sync-mirrors.mjs`
   is specific to the author's plugin repositories - use whatever the target
   repository documents, or skip mirrors if it has none). Mixed fleet commits
   make per-plugin rollbacks impossible.
5. **Compatibility builds over host-locked builds** when the plugin must
   span host generations: resolve renamed host exports at runtime through a
   fallback chain (old name → new variants) instead of static named imports,
   and extend unit-test module mocks with every fallback name (strict mocks
   throw on undefined-export access and mask the real failure).

## Workflow

1. Read the target host version's corridor cards
   (`plugin-upgrade/references/v<target>.md`) and derive the static sweep
   patterns from them - the cards name the renamed/removed surfaces.
2. Static sweep: grep every fleet repository for those patterns; record
   hits as broken-until-fixed with file:line.
3. Live sweep: load the real GUI in a driven headless browser against the
   upgraded host and per plugin assert (a) the client CSS/style tag present,
   (b) zero `slot entry crashed` console records, (c) the surface's DOM
   marker present, (d) the expected requests fired. Method:
   [references/fleet-sweep-checklist.md](references/fleet-sweep-checklist.md)
   (includes the authenticated-GUI access and instrumentation discipline from
   `plugin-runtime-debug/references/browser-forensics.md`).
4. Re-verify interaction-gated surfaces with their trigger simulated (paste,
   file write, keyboard chord) or downgrade the verdict explicitly.
5. For each broken plugin: diagnose against the host source
   (`plugin-runtime-debug` standing rule), fix with a
   host-generation-compatible approach when the fleet spans host versions,
   run the plugin's typecheck/tests/build, then release: version bump,
   changelog/compatibility-table row naming the host version range, commit,
   tag, mirrors.
6. Re-run the live sweep after releases and record the final per-plugin
   verdict table (plugin, host versions supported, evidence).

## Report

End with a per-plugin table: verdict (working / fixed+released /
interaction-path-unexercised / broken), the host versions covered, and the
evidence (which assertion passed where). Note any host bug found (report
upstream with the minimal repro) and any hot-fix living in the install tree
that the next host upgrade will overwrite - list the reapplication material.

