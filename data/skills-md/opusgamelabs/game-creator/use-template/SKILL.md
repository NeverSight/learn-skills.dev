---
name: use-template
description: Clone a game template from the gallery as a starting point. Use when the user says "use a template", "start from a template", "clone flappy-bird", "use the platformer template", or wants to quickly bootstrap a game from an existing example. Do NOT use for creating a game from scratch (use make-game).
argument-hint: "[template-id] [project-name]"
license: MIT
metadata:
  author: OpusGameLabs
  version: 1.3.0
  tags: [game, template, scaffold, clone, gallery]
---

# Use Template

Clone a game template from the gallery into a new project. This is a fast copy — working code in seconds, not an AI pipeline.

## Behavior

1. **Parse arguments**: `<template-id> [project-name]`
   - If no arguments provided, read `gallery/manifest.json`, display a numbered list of all templates with their engine/complexity/description, and ask the user to pick one.
   - `template-id` is required. `project-name` defaults to `template-id`.

2. **Look up template** in `gallery/manifest.json` by `id`. If not found, show available IDs and abort.

3. **Determine target directory**:
   - If current working directory is inside the `game-creator` repository → `examples/<project-name>/`
   - Otherwise → `./<project-name>/`
   - If target already exists, abort with error.

4. **Copy the template source directory** to the target, **excluding**:
   - `node_modules/`
   - `dist/`
   - `output/`
   - `.herenow/`
   - `progress.md`
   - `test-results/`
   - `playwright-report/`

5. **Update project metadata**:
   - In `package.json`: set `"name"` to the project name
   - In `index.html` (if exists): update `<title>` to a formatted version of the project name

6. **Install dependencies**: Run `npm install` in the target directory.

7. **Print next steps**:
   ```
   Template cloned successfully!

   cd <project-name>
   npm run dev
   ```

## Implementation

```javascript
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Find game-creator root (contains gallery/manifest.json)
function findRoot(dir) {
  let d = dir;
  while (d !== path.dirname(d)) {
    if (fs.existsSync(path.join(d, 'gallery', 'manifest.json'))) return d;
    d = path.dirname(d);
  }
  return null;
}

const root = findRoot(process.cwd());
const manifest = JSON.parse(fs.readFileSync(path.join(root, 'gallery', 'manifest.json'), 'utf-8'));

// Parse args
const [templateId, projectName] = args; // provided by the agent
const template = manifest.find(t => t.id === templateId);
const name = projectName || templateId;

// Determine target
const inGameCreator = process.cwd().startsWith(root);
const target = inGameCreator
  ? path.join(root, 'examples', name)
  : path.join(process.cwd(), name);

// Copy with exclusions
const EXCLUDE = ['node_modules', 'dist', 'output', '.herenow', 'progress.md', 'test-results', 'playwright-report'];

function copyDir(src, dst) {
  fs.mkdirSync(dst, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    if (EXCLUDE.includes(entry.name)) continue;
    const s = path.join(src, entry.name);
    const d = path.join(dst, entry.name);
    if (entry.isDirectory()) copyDir(s, d);
    else fs.copyFileSync(s, d);
  }
}

copyDir(path.join(root, template.source), target);

// Update package.json
const pkgPath = path.join(target, 'package.json');
if (fs.existsSync(pkgPath)) {
  const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf-8'));
  pkg.name = name;
  fs.writeFileSync(pkgPath, JSON.stringify(pkg, null, 2) + '\n');
}

// Update index.html title
const indexPath = path.join(target, 'index.html');
if (fs.existsSync(indexPath)) {
  let html = fs.readFileSync(indexPath, 'utf-8');
  const prettyName = name.replace(/[-_]/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
  html = html.replace(/<title>[^<]*<\/title>/, `<title>${prettyName}</title>`);
  fs.writeFileSync(indexPath, html);
}

// Install
execSync('npm install', { cwd: target, stdio: 'inherit' });

// Fire-and-forget telemetry (respects DO_NOT_TRACK / DISABLE_TELEMETRY)
if (!process.env.DO_NOT_TRACK && !process.env.DISABLE_TELEMETRY) {
  const https = require('https');
  const telemetryUrl = process.env.TELEMETRY_URL || 'https://gallery-telemetry.up.railway.app';
  https.get(`${telemetryUrl}/t?event=clone&template=${encodeURIComponent(templateId)}&source=skill&v=1`)
    .on('error', () => {});
}
```

## Example Usage

```
/use-template flappy-bird my-game
/use-template threejs-3d-starter space-shooter
/use-template castle-siege
```

## Key Difference from /make-game

`/use-template` is a **10-second copy**. You get working, runnable code instantly and customize it manually. `/make-game` is a **10-minute AI pipeline** that scaffolds, designs, adds audio, tests, deploys, and monetizes from a text prompt.
