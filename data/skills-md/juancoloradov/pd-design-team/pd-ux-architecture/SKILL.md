---
name: pd-ux-architecture
description: >-
  Use when a product's content, objects, or navigation need explicit structure: content modeling,
  taxonomy, sitemaps, navigation systems, and findability. Defines the nodes and entities of a product;
  sits between research and flows. Part of the pd-* design team.
metadata:
  team: product-design
  role: ux-architecture
  version: "2.0.0"
---

# pd-ux-architecture — structure the space, before the path

## Overview

Define what a product is made of and how it is organized, before flows trace paths through it and before
design lays out screens. Weak information architecture shows up as duplicate content, contradictory
labels for the same thing, and users who cannot find what already exists.

## Before you start

1. Load `pd-foundations`: `principles.md`, `accessibility.md`, `handoff-protocol.md`.
2. Read `docs/design/PROJECT.md`. If it is missing, proceed with defaults and record them as assumptions,
   or ask `pd-design-lead` to set it up.
3. Read the upstream research artifact (`*-research-*.md`) and the requirement from the tracker named in
   `PROJECT.md` (see `integrations.md`). Research is replaceable by stated assumptions if the user
   accepts that; list them in your artifact.

## When to use

- A new product or module needs content, objects, or navigation structured from scratch.
- Users can't find something that exists, or one concept has several names across the product.
- Menus, navigation, or taxonomy need defining or fixing, independent of any single screen.
- Before `pd-ux-flows` or `pd-ux-design`, which both need firm structural ground.

**Not for:** the sequence of steps for a task (`pd-ux-flows`), one screen's layout (`pd-ux-design`),
final label wording (`pd-ux-writing`; this skill names things, writing polishes the words).

Three questions, three skills: architecture says what exists and how it is organized (space); flows say
what sequence completes a task (time); design says how one screen is laid out (surface). Architecture
defines the nodes, flows trace the paths between them, design shapes the inside of each node.

## Process

Artifact formats and method details are in `references/artifacts.md`.

1. **Inventory, then audit.** List every entity and content item that exists today, then judge each for
   accuracy, redundancy, and keep/merge/retire. Resolve duplicate names for one concept first.
2. **Model the content (OOUX).** Nouns before verbs: objects, attributes, relationships, then the actions
   each object supports.
3. **Build the taxonomy and, for search-driven products, the search model.** Use LATCH as a starting lens
   and a controlled vocabulary (preferred term, variants aliased to it). With no prior classification, run
   an open card sort first.
4. **Structure the sitemap.** Canonical hierarchy, breadth vs. depth balanced, public vs. authenticated
   zones marked.
5. **Define navigation and wayfinding.** Primary, secondary, contextual nav; breadcrumbs, active states,
   canonical paths, escape routes; deep-linking, since users arrive mid-tree via search and notifications.
6. **Validate when it matters.** Closed card sort to test an existing classification; tree test before
   freezing a sitemap deeper than about 3 levels. If you cannot run these, mark the structure unvalidated.
7. **Stress-test for growth.** If adding about 3 more entities or modules breaks primary navigation, the
   structure is fragile.

Hold to information scent (every label telegraphs what is behind it) and to the three orientation
questions answerable at any depth: where am I, what is here, where can I go.

## Output

`<artifacts_dir>/<date>-architecture-<topic>.md` with the artifact header from `handoff-protocol.md`
(`discipline: architecture`), then: content model (entities, attributes, relationships), taxonomy and
controlled vocabulary, sitemap table, navigation model table plus wayfinding rules, findability
validation results if run, open questions. `upstream:` research, if it was used (otherwise none, with assumptions stated). `downstream:` `flows`, `design`.

## Domain packs

If `PROJECT.md` lists domain packs, read each pack's section for architecture and apply it on top of this
skill.

## Common mistakes

- Mirroring the org chart: navigation built around internal departments instead of user goals.
- Junk-drawer labels ("Other", "General", "Misc", "Advanced Settings") for whatever went unclassified.
- Hiding key entities or actions 4-5 levels deep instead of flattening or adding contextual shortcuts.
- One entity under different names in different places ("Members", "Accounts", "Profiles").
- Designing only for the front door and ignoring deep links, bookmarks, notifications, and search landings.
- Vague intermediate labels ("Resources", "Tools") that force users to guess.
