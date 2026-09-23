---
name: ext-scaffold
description: Generates a working Manifest V3 browser extension skeleton — manifest.json, background service worker, content script, and popup — valid on first load in Chrome/Edge/Firefox with no npm and no bundler. Refuses to overwrite an existing directory. Use when starting any browser extension instead of writing boilerplate.
when_to_use: Beginning a new browser extension, prototyping an extension idea quickly, or giving an agent a correct MV3 baseline to modify. NOT a build system or a publishing tool; it's the correct-by-construction starting point.
version: 1.0.0
license: MIT
metadata:
  agentskills:
    tags: [browser-extension, manifest-v3, chrome, scaffold]
---

# Ext Scaffold

A working Manifest V3 extension in one command — no npm, no bundler, no
"why doesn't my service worker register".

## Commands

```bash
python3 scripts/ext_scaffold.py my-extension
python3 scripts/ext_scaffold.py my-extension --dir ~/projects --permissions storage,tabs
```

## Generated

```
my-extension/
├── manifest.json    # MV3, kebab-case name validated, permissions you asked for
├── background.js    # service worker: install hook + message ping/pong
├── content.js       # content script: runs on all pages, pings background
├── popup.html       # action popup with a working button
└── popup.js         # popup logic: queries the active tab
```

Load it: `chrome://extensions` -> Developer mode -> Load unpacked.
It works before you touch a line — message passing, content injection, and
popup all wired.

## Pairs with

`webapp-testing` (drive the browser with your extension loaded),
`code-review` (review what you build on the scaffold).
