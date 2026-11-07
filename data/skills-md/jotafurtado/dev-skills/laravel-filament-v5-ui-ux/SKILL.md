---
name: laravel-filament-v5-ui-ux
description: "Guides Filament 5.x composition choices for layout structure, visual hierarchy, responsive behavior, theme-preserving presentation, and visual-only page arrangement across tables, forms, infolists, dashboards, panels, and actions. Use when selecting, designing, or reviewing how a Filament 5 surface is organized, prioritized, or displayed on different screen sizes. Use alongside laravel-filament-v5 for installed-version APIs, security, migrations, and tests. Do not trigger for functional Resource, table, action, or API implementation without a composition decision; generic frontend work; Filament 3/4; single-field tweaks; or upgrade-only tasks."
license: MIT
metadata:
  author: jotafurtado
  version: "2.1.3"
  domain: frontend
  filament_version: "5.x"
---

# Laravel Filament v5 UI/UX

A library of reference compositions for Filament 5 surfaces. Let `laravel-filament-v5` own installed-version APIs, security, implementation, and tests.

## How to use it

Find the row below that matches what you are building, read that file, and pick the composition whose `When` fits the task. Paste it and adapt the model, fields, and relations. Each composition carries the official documentation and screenshot it came from.

There is no required workflow, no mandatory screenshot inspection, and no decision trace. Pick the composition that fits and build.

If more than one composition fits, prefer the one whose `Not when` does not describe your task. If none fits, say so and record the surface as an uncovered pattern instead of improvising a composition.

## Routing

| Building or restructuring | Read |
|---|---|
| A record table | `references/table.md` |
| Page structure of a form or schema — entry point; grouping, columns, sections, tabs, wizards, density | `references/form-layout.md` |
| An everyday form field composed inside that structure — geometry, labels, guidance, states | `references/form-fields.md` |
| A collection, upload, relationship, or rich-content control composed inside that structure | `references/form-inputs.md` |
| Record details and infolists | `references/record-detail.md` |
| Operational dashboards and widgets | `references/dashboard.md` |
| Panel shell, navigation, branding, authentication surfaces | `references/panel-shell.md` |
| Actions, confirmations, overlays, notifications, callouts, empty states | `references/action-feedback.md` |

Every file above is a set of reference compositions: pasteable code with provenance. `action-feedback.md` is cross-surface and applies on top of any of the others.

These files are the only source for the surfaces they cover.

## Pairing

Compositions are code, so implementation work uses `laravel-filament-v5` for API signatures, authorization, security, and tests. Install both for any task that will ship the composition:

```bash
npx skills add jotafurtado/dev-skills --skill laravel-filament-v5-ui-ux --skill laravel-filament-v5
```

Find that sibling before treating a signature as known. A hit is a readable `SKILL.md` whose frontmatter `name` is exactly `laravel-filament-v5`. Search in this order and stop at the first hit:

1. The sibling directory next to this skill (`../laravel-filament-v5/SKILL.md`).
2. The project being edited: `.agents/skills` (Cursor and Codex), then `.claude/skills` (Claude Code).
3. The home directory: `.agents/skills`, `.claude/skills`, `.cursor/skills`, then `.codex/skills`.

The repository copy of that check is `maintenance/filament-ui-ux/scripts/discover_sibling_skill.py`. An installed copy of this skill does not include the script, so apply the same order by reading the files. If no file matches, there is no fallback composition module and no reconstructed signature. Arrangement-only work may paste the composition and must say the sibling file was not found. A task that ships code stops and asks for the install above.

## Authority

Official Filament composition supersedes generic frontend advice asking for unrelated typography, palettes, custom card systems, or CSS-first layouts. Keep compatible accessibility, keyboard, responsive, performance, and UX-copy guidance.

Preserve an established panel theme. Before writing custom Blade, Livewire, or CSS, name the official component you checked and the concrete gap it cannot cover, and keep the custom surface as small as possible.

Delegate API signatures, installed-version compatibility, security boundaries, implementation, and tests to `laravel-filament-v5`.
