---
name: bricks-agent-repository
description: "Handle complex existing-site Bricks edits through advertised repository/workspace workflows when focused abilities cannot express the change."
---

# Bricks agent repository

Treat Bricks as a typed repository while WordPress remains authoritative.

## Explicit host-owned file workspace

Use this route only when the task environment explicitly announces
`bricks.workspace/v1`. Treat the projected files as a temporary authorized checkout:

1. Inspect and edit only the supplied resource files with ordinary file tools.
2. Preserve opaque fields, IDs, baselines, and files outside the requested scope.
3. Do not edit host metadata, credentials, session files, or baseline digests.
4. Do not call write abilities in parallel. The host validates and saves the changed
   files after the agent finishes.
5. Report the edited files, then wait for the host result before claiming the changes
   were saved to WordPress.

Never infer `bricks.workspace/v1` from filenames, a `.bricks` directory, an
installed skill, or prior tasks. If the host does not announce it, use the ability
routes below.

## Choose the smallest route

- **Exact supported edit:** use `commit-exact-site-edits`.
- **Exact edit that needs target discovery:** use `checkout-site-edit-map`, then
  `commit-site-edit-plan` when the returned `editableOps` supports the change.
- **Known target needing structural editing:** use `resolve-agent-file`, then
  `commit-agent-file`.
- **Two to 25 coordinated resources:** use one site changeset.
- **Unknown or ambiguous targets, dependency analysis, or recovery:** use
  `checkout-site-repository` with narrow filters.

Never fetch every full document merely to locate one target.

## Exact edits

Use `commit-exact-site-edits` when the live schema supports the requested operation
and the target is an exact ID, unique full name, current text, or label. Supply
`expectedValue`. Use `allowBlindWrite: true` only when the user intentionally supplied
the exact target and requested replacement regardless of its current value.

Use only operations advertised by the live schema. Component attribute edits on this
route are limited to `role` and `aria-*`; use the canonical file route for broader
custom attributes. Never change a component instance boundary or overwrite content
controlled by a component property.

## Edits that need discovery

Call `checkout-site-edit-map` with the smallest target list that can locate the edit:

```json
{
  "targets": [
    { "scope": "page", "postId": 13 },
    { "scope": "design", "resource": "globalVariable", "id": "accent" }
  ],
  "elementIds": ["bbbbbb"]
}
```

Omit `elementIds` when they are unknown. Do not substitute unsupported ID arrays or
parameters. Copy each returned `selectionRef` into one advertised operation and call
`commit-site-edit-plan` once with a stable idempotency key. Repeat that exact call to
resume safely. Request `responseFormat: "summary"` unless another edit needs the full
document.

Use `preview-site-edit-plan` with `resourcePath` and `selectionDigest` only when the
user asks for a dry run. Fall back to canonical files when the map is truncated or
does not support the required element, property, link, attribute, or structural edit.

## Repository discovery

When the target is not exact, call `checkout-site-repository` with the narrowest
useful `query`, `postTypes`, `designKinds`, `includeDocuments`, `includeDesign`,
`includeDependencies`, and `perPage`. Follow cursors only while later results may
matter. After selecting a target, continue with the smallest edit route above.

## Two-call known-target path

Call `bricks/resolve-agent-file` with an exact `scope`, `query`, and optional
`resourceKinds`. Proceed only when it returns one target and a canonical document.
Follow its `editingContract` for canonical keys, native style shapes, responsive
suffixes, flat-tree ordering, and preservation rules. Commit the target and requested
edit through `bricks/commit-agent-file` with one stable idempotency key. Prefer compact
readback; request the full document only when another edit needs it.

Preserve every unrelated element in a replacement file. If the live commit schema
advertises `removeElementIds`, name each element you intentionally remove; its
descendants are implied. An omission error means restore the missing content
unless the user asked for its removal.

For custom attributes, preserve ordered `_attributes` records shaped as `{ "id"?: string, "name": string, "value": string }`. The returned editing contract is authoritative.

## Changesets

There is no atomic whole-site transaction across WordPress hooks, assets, caches, and plugins. Keep each step safe if later work fails:

- Keep every intermediate pages-first state valid.
- Preview the complete bounded changeset once.
- Apply/resume with the same token and outer idempotency key until terminal.
- Continue only from `in_progress`; success is `committed` with authoritative readback for every changed step.
- Stop on `failed_before_commit`, `partial_commit`, or `manual_recovery`. Re-read and re-plan; never assume rollback.
- Clear a recovery record through the destructive resolution ability only after explicit human approval; clearing it does not undo saved changes.

Split work above 25 resources into independently valid batches. For renames or reference migrations, use dependency hints to narrow authoritative consumer reads; hints are not proof that a resource is unused.

## Boundaries

- Rendered HTML is verification evidence, not editable source.
- Page files may reference but cannot mutate shared design resources.
- Workspaces update existing resources. Use focused create/delete abilities and their required preconditions for lifecycle changes.
- Never replace focused ownership/version/digest requirements with a repository baseline.
- Do not reconstruct redacted component or code-sensitive data from frontend markup.
- Prefer a fresh targeted checkout over retaining a large snapshot across unrelated tasks.
