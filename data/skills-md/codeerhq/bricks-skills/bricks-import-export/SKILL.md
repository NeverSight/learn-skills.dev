---
name: bricks-import-export
description: "Transfer Bricks resources between sites with inspected packages, explicit item selection, conflict handling and recovery."
---

# Bricks: unified import / export via MCP

Use the unified transfer-package format for site-to-site migration.

Use these abilities:

- `bricks/list-transfer-items`: read the current site's export selector and exact item IDs.
- `bricks/export-transfer-package`: create a base64 ZIP package from explicit selected item IDs.
- `bricks/inspect-transfer-package`: inspect a ZIP before import; returns conflicts, warnings, and `zipHash`.
- `bricks/import-transfer-package`: import selected manifest items. Requires `expectedZipHash` from inspection.

Use `bricks/list-transfer-items` as the authority for available types and exact item IDs on the source site. Availability depends on the caller’s permissions. Typical transfer types include: `color-palettes`, `theme-styles`, `classes`, `variables`, `custom-fonts`, `breakpoints`, `global-queries`, `components`, `templates`, `settings`, `custom-capabilities`, and `icon-manager` when advertised.

## Normal site-to-site flow

1. On the source site, call `bricks/list-transfer-items`.
2. Choose explicit item IDs from the response.
3. Call `bricks/export-transfer-package` with:

```json
{
  "types": ["classes", "components", "templates"],
  "items": {
    "classes": ["abc123"],
    "components": ["hero-card"],
    "templates": ["100", "101"]
  }
}
```

4. On the target site, call `bricks/inspect-transfer-package` with the returned `zipBase64`.
5. Review `manifest.warnings` as well as `manifest.types.*.items`, especially each item’s `conflict` and `warning`.
6. Call `bricks/import-transfer-package` with the same `zipBase64`, the inspected `zipHash` as `expectedZipHash`, and explicit manifest item IDs:

```json
{
  "zipBase64": "UEsDBBQ...",
  "expectedZipHash": "sha256-from-inspect",
  "types": ["classes", "components"],
  "items": {
    "classes": ["abc123"],
    "components": ["hero-card"]
  },
  "conflictMode": "skip"
}
```

## Permission warnings on inspection

On Bricks 2.4.3+, inspection can omit a type from `manifest.types` and explain the omission in top-level `manifest.warnings`. A missing type does not prove that the source bundle lacks that data (`Unified_Global_Transfer::filter_manifest_by_permissions()` in `includes/unified-global-transfer.php`).

For `svg_upload_permission_required` with type `icon-manager`, the target caller has Icon Manager access and file-upload capability but lacks SVG-upload permission. Ask an administrator to check **Bricks > Settings > General > SVG uploads** and the **Upload SVG** override in the user profile, then inspect the bundle again. Import only types and item IDs available in that new inspection.

## Safety rules

- Always inspect before import. The import ability requires `expectedZipHash` so the imported ZIP matches the package you reviewed.
- `conflictMode` defaults to `skip`. Use `replace` only when overwriting is requested, and pass `allowOverwrite: true`.
- Per-item replacements live in `conflictDecisions`, keyed by type and item ID; any `replace` value also requires `allowOverwrite: true`.
- Sensitive settings tabs require explicit user intent and `allowSensitiveSettings: true`. The `custom-code` tab can be exported with that acknowledgement, but `import-transfer-package` rejects importing it even when acknowledged (`includes/abilities/import-export.php`).
- Template image import is off by default. Use `importImages: true` only when media migration is intended and the user can upload files.
- MCP ZIP payloads are capped for JSON transport. If a package is too large, split by type or item selection.
- Code-bearing templates, components, component properties, and global queries follow the caller’s code-authoring permissions. PHP imports need the complete PHP authorization contract in [bricks-custom-code](../bricks-custom-code/SKILL.md#code-authoring-through-abilities). Inspect redacted exports and rejected payloads; do not reconstruct hidden source or assume HTML-page partial omission applies to transfer packages.

## Notes

- `items` is required for each selected type. Do not omit it and assume "everything".
- For singleton `breakpoints`, use `items: { "breakpoints": ["all"] }`.
- For settings, pass tab IDs such as `builder`, `performance`, `api-keys`, or `custom-code`.
- Transfer packages include `manifest.json`; template-only legacy ZIPs without a manifest are not accepted by the unified import flow.

## Tool availability

If a `bricks/*` ability is not available as a direct tool, first check whether it is outside the fast path and call it through `mcp-adapter-execute-ability` with `ability_name: "bricks/<name>"`. If the dispatcher also rejects it, call `bricks-list-ability-status` to check whether a site admin disabled it under Bricks > AI.
