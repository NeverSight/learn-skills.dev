---
name: figma
description: "Build Figma plugins, export selected frames, audit components, and map variables to design tokens using the Plugin and REST APIs."
category: design
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["figma", "plugin-api", "rest-api", "design-tokens", "variables", "rate-limits", "batch-export"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Figma Design Systems & Plugin AI Skill Guide (Claude)

## Overview & Engine Architecture

Figma models **Document → Pages → Nodes** with **Components**, **Variables**, and **Styles**. Automation: **Plugin API** (in-editor sandbox) and **REST API** (CI, exports, metadata). Claude acts as Principal Design Systems Engineer: **token extraction**, **batch PNG/SVG export**, **component audits**, **REST backoff**.

**Rate limits:** Per-user PAT limits depend on **seat** and **file's plan** ([Rate Limits docs](https://developers.figma.com/docs/rest-api/rate-limits/)). Tier 1 `GET /v1/files/:key` — e.g. Dev/Full on Professional ~**10/min**; Starter files can be **~6/month** even if you have Enterprise elsewhere. **429** → honor **Retry-After**, exponential backoff (~60s).

```
┌─────────────────────────────────────────────────────────────┐
│  Plugin: figma.* sandbox (mutate live file)                 │
│  REST: X-Figma-Token → files / images / variables           │
│  CI: cache file JSON; batch node IDs; respect tier limits     │
└─────────────────────────────────────────────────────────────┘
```

---

## When to use / when not to

**Use when:** design token sync, automated export of frames, design lint (detached instances), REST-driven previews in CI.

**Do not use when:** Pixel-perfect production video (use Remotion); heavy mutation at scale without Plugin (REST is read/export oriented); secrets in client-side plugin bundle.

---

## Operational Capabilities & Agent Directives

1. **Plugin vs REST:** Mutations → Plugin; scheduled export/metadata → REST `GET /v1/files/:key`, `GET /v1/images/:key?ids=&format=png&scale=2`.
2. **Token security:** PAT in env `FIGMA_TOKEN` only; Plugin uses `figma.clientStorage` for non-secret prefs; declare `networkAccess` in `manifest.json` for REST from UI iframe if needed.
3. **Batch export:** Chunk node IDs (REST image endpoint has payload limits); on **400** reduce batch size (large files timeout).
4. **Variables → tokens:** Use Variables REST where licensed; map `modeId` → platform theme; stable semantic names (`color.bg.default`), not raw node IDs in CSS.
5. **Deterministic export:** Fixed `scale`, `format`, `svg_outline` / `svg_include_id` flags; same file version (`version` field from file API) for golden diffs.
6. **Traversal:** `node.findAllWithCriteria` — avoid hard-coded `1:2` paths that break on reorder.

---

## Plugin: export selected frames (PNG @2x)

```typescript
async function exportSelectionPng2x() {
  const frames = figma.currentPage.selection.filter(
    (n): n is FrameNode => n.type === "FRAME"
  );
  if (!frames.length) {
    figma.notify("Select frames.");
    return;
  }
  for (const frame of frames) {
    const bytes = await frame.exportAsync({
      format: "PNG",
      constraint: { type: "SCALE", value: 2 },
    });
    figma.ui.postMessage({ type: "PNG", name: frame.name, bytes });
  }
}
```

## REST: image export with backoff

```bash
curl -s -H "X-Figma-Token: $FIGMA_TOKEN" \
  "https://api.figma.com/v1/images/${FILE_KEY}?ids=${NODE_IDS}&format=png&scale=2"
```

On 429, sleep `Retry-After` header or 60s; retry max 5.

---

## Failure taxonomy

| Symptom | Cause | Fix |
| :--- | :--- | :--- |
| 403 | Token scope / file access | Regenerate PAT with file_content read |
| 429 | Plan/seat/file tier | Backoff; move file to paid plan |
| 500 on images | Too many/large nodes | Smaller id batches |
| Detached instances | Local overrides | Audit plugin; re-instance |
| Plugin network blocked | manifest | `networkAccess.allowedDomains` |

---

## Agent Operational Directive

> **MANDATORY**: Never commit PATs. Chunk REST exports. Pin file `version` for deterministic asset CI. Prefer Variables for tokens over hard-coded fills.
