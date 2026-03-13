---
name: web-artifacts-builder
description: Suite of tools for creating elaborate, multi-component claude.ai HTML artifacts using modern frontend web technologies. Supports React 18 + TypeScript + Tailwind CSS + shadcn/ui and Vue 3 + TypeScript + Tailwind CSS project initialization, then bundles apps into a single HTML artifact. Use for complex artifacts requiring state management, routing, or component systems - not for simple single-file HTML/JSX/Vue snippets.
license: Complete terms in LICENSE.txt
---

# Web Artifacts Builder

To build powerful frontend claude.ai artifacts, follow these steps:
1. Initialize the frontend repo with the unified initializer
2. Develop your artifact by editing the generated code
3. Bundle all code into a single HTML file using `scripts/bundle-artifact.sh`
4. Display artifact to user
5. (Optional) Test the artifact

**Stack**:
- React 18 + TypeScript + Vite + Parcel (bundling) + Tailwind CSS + shadcn/ui
- Vue 3 + TypeScript + Vite + Parcel (bundling) + Tailwind CSS

## Design & Style Guidelines

VERY IMPORTANT: To avoid what is often referred to as "AI slop", avoid using excessive centered layouts, purple gradients, uniform rounded corners, and Inter font.

## Quick Start

### Step 1: Initialize Project

Use the unified initializer (recommended):
```bash
# React (default)
bash scripts/init-artifact.sh <project-name>

# Explicit React
bash scripts/init-artifact.sh <project-name> --framework react

# Vue + TypeScript + Tailwind
bash scripts/init-artifact.sh <project-name> --framework vue

cd <project-name>
```

You can also call the framework-specific script directly:
```bash
bash scripts/init-artifact-vue.sh <project-name>
```

This creates a fully configured project with:
- ✅ React + TypeScript (with shadcn/ui) or Vue 3 + TypeScript
- ✅ Tailwind CSS 3.4.1 setup
- ✅ Path aliases (`@/`) configured
- ✅ React path includes 40+ shadcn/ui components and Radix dependencies
- ✅ Vue path keeps a lightweight, framework-native setup
- ✅ Parcel configured for bundling (via .parcelrc)
- ✅ Node 18+ compatibility (auto-detects and pins Vite version)

### Step 2: Develop Your Artifact

To build the artifact, edit the generated files.

### Step 3: Bundle to Single HTML File

To bundle the frontend app into a single HTML artifact:
```bash
bash scripts/bundle-artifact.sh
```

This creates `bundle.html` - a self-contained artifact with all JavaScript, CSS, and dependencies inlined. This file can be directly shared in Claude conversations as an artifact.

**Requirements**: Your project must have an `index.html` in the root directory.

**What the script does**:
- Installs bundling dependencies (parcel, @parcel/config-default, parcel-resolver-tspaths, html-inline)
- Creates `.parcelrc` config with path alias support
- Builds with Parcel (no source maps)
- Inlines all assets into single HTML using html-inline

### Step 4: Share Artifact with User

Finally, share the bundled HTML file in conversation with the user so they can view it as an artifact.

### Step 5: Testing/Visualizing the Artifact (Optional)

Note: This is a completely optional step. Only perform if necessary or requested.

To test/visualize the artifact, use available tools (including other Skills or built-in tools like Playwright or Puppeteer). In general, avoid testing the artifact upfront as it adds latency between the request and when the finished artifact can be seen. Test later, after presenting the artifact, if requested or if issues arise.

## Reference

- **React path details**: `references/react.md`
- **Vue path details**: `references/vue.md`
- **shadcn/ui components**: https://ui.shadcn.com/docs/components
- **Vue docs**: https://vuejs.org/guide/introduction.html
