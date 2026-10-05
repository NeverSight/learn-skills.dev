---
name: edit-prototype
description: "Edit one or more existing Phat prototype pages by prototype revision ID while preserving unrelated pages and confirmed requirements. Use when the user references an ID such as home-v1 or booking-v2 and wants targeted visual, layout, content, state, navigation, or interaction changes before specification."
---

# Edit Prototype

Apply targeted changes to an existing UI prototype using prototype revision IDs.

Edit only the requested prototype surface.

Do not redesign unrelated pages.

Do not turn prototype edits into production implementation.

## Contents

- [Input](#input)
- [Locate the target](#locate-the-target)
- [Read context](#read-context)
- [Preserve requirements](#preserve-requirements)
- [Targeted editing](#targeted-editing)
- [Revision IDs](#revision-ids)
- [Multiple targets](#multiple-targets)
- [Prototype proposals](#prototype-proposals)
- [Verification](#verification)
- [Finish](#finish)

## Input

Prefer requests such as:

```text
$edit-prototype home-v1

Make the hero shorter and add a search input.
```

or:

```text
$edit-prototype booking-v2

Show an unavailable time-slot state.
```

The prototype ID is the primary target.

## Locate the target

Inspect:

```text
docs/assets/prototype/
```

Find the HTML page whose metadata contains:

```html
data-prototype-id="<requested-id>"
```

Do not assume the filename from the page name.

For example:

```text
home-v1
```

may map to:

```text
index.html
```

If the requested ID does not exist, report available page IDs rather than editing a guessed page.

## Read context

Before editing, read:

* `AGENTS.md` if present;
* the target HTML;
* shared `style.css`;
* shared `script.js`;
* relevant requirement/context;
* applicable Agreed UI Design Requirements and confirmed Design Direction;
* relevant spec if one exists.

Read other prototype pages only when needed to preserve shared navigation or shared styling.

## Preserve requirements

A prototype edit may change visual representation without changing product behavior.

Examples:

```text
color
spacing
layout
typography
content hierarchy
component arrangement
```

These usually do not require requirement changes.

If the user asks for behavior that introduces a new:

* business rule;
* permission;
* workflow;
* user role;
* data requirement;
* integration;
* product scope;

treat that as a product change.

Do not silently encode it as agreed behavior.

Route material decisions to:

```text
$grill-workflow
```

before treating them as authoritative.

## Targeted editing

When the requested edit needs composition, hierarchy, responsive layout, or
visual treatment decisions, load `$ui-design` when available and apply it
inline to the requested pages. Pass the existing direction and shared-file
boundaries. Skip it for mechanical edits whose design is already determined.
Keep revision IDs, proposal labels, verification, and handoff under this skill;
check shared-style effects on other pages. If unavailable, preserve established
patterns and report the fallback without auto-installing it.

Preserve unrelated prototype behavior.

Do not:

* rewrite every page;
* globally restyle the prototype unnecessarily;
* replace the visual direction without request;
* rename pages unnecessarily;
* remove working interactions outside the requested change.

Shared CSS or JavaScript may be modified when required, but ensure other pages still work.

## Revision IDs

A meaningful requested edit creates a new revision ID.

For example:

```text
home-v1
→
home-v2
```

Update:

```html
data-prototype-id="home-v2"
```

Then update navigation references across the prototype from:

```html
data-prototype-target="home-v1"
```

to:

```html
data-prototype-target="home-v2"
```

Update the visible ID shown in prototype navigation/control UI as well.

Only increment pages that actually changed.

For example:

```text
Before

home-v1
about-v1
contact-v1

After editing Home

home-v2
about-v1
contact-v1
```

Do not bump every page version because a shared file changed unless the visible or interactive behavior of those pages meaningfully changed.

## Multiple targets

If the user explicitly requests several pages, modify each target and increment each changed page independently.

Example:

```text
home-v2 → home-v3
contact-v1 → contact-v2
```

Preserve unchanged IDs.

## Prototype proposals

If the user asks:

```text
"ลองเพิ่ม pricing comparison ดู"
```

and that behavior is not an agreed requirement, it may appear as an explicitly experimental prototype proposal.

Mark it visibly or in prototype comments as:

```text
Prototype proposal
```

Do not let `$spec-with-prototype` treat it as agreed automatically.

## Verification

After editing:

* open/check the target structure;
* verify requested changes are represented;
* verify page ID was incremented;
* verify navigation references use the new ID;
* verify internal links still resolve;
* verify shared CSS/JS did not break unrelated pages;
* verify responsive behavior remains reasonable;
* verify requested interactions still work.

## Finish

Report:

1. requested prototype ID;
2. file edited;
3. old ID;
4. new ID;
5. changes made;
6. shared files changed;
7. prototype proposals introduced;
8. unresolved decisions;
9. next skill.

Use:

```text
more visual iteration wanted
    → $edit-prototype

prototype accepted
    → $spec-with-prototype

product decision required
    → $grill-workflow
```

Do not update the feature spec automatically.

Do not create tasks.

Do not implement production code.
