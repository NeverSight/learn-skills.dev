---
name: mdzilla
description: >
  Browse, search, and export documentation from any source using the mdzilla CLI.
  Use when Claude needs to: (1) Read or browse documentation for a library, framework, or project,
  (2) Fetch docs from GitHub repos, npm packages, or websites,
  (3) Export documentation to flat markdown files,
  (4) Look up API references, guides, or usage examples from doc sites.
  Triggers: user asks to "read the docs", "check the documentation", "browse docs for X",
  "fetch docs from", "export docs", or references a docs site URL, npm package docs, or GitHub repo docs.
---

# mdzilla

Markdown documentation browser for terminal and agents. Fetches and renders docs from local dirs, GitHub, npm, HTTP, and `llms.txt`.

## CLI

```sh
npx mdzilla <source> [options]
```

### Sources

| Source    | Syntax                        | Notes                                                            |
| :-------- | :---------------------------- | :--------------------------------------------------------------- |
| Local dir | `mdzilla ./docs`              | Scan local docs directory                                        |
| File      | `mdzilla README.md`           | Render single markdown file                                      |
| GitHub    | `mdzilla gh:owner/repo`       | Looks for `docs/` in repo                                        |
| npm       | `mdzilla npm:package-name`    | Downloads package, reads docs                                    |
| HTTP      | `mdzilla https://example.com` | Tries `/llms.txt`, then markdown negotiation, then HTML→markdown |

### Options

- `--export <dir>` — Export docs to flat `.md` files
- `--page <path>` / `-p <path>` — Print a single page by path and exit
- `--plain` / `--headless` — Plain text output (no TUI); auto-enabled for AI agents or non-TTY stdout

### Agent usage

Always use `--plain` when calling from scripts or agents:

```sh
npx mdzilla gh:unjs/h3 --plain
npx mdzilla gh:unjs/h3 --plain --page /guide/basics
npx mdzilla https://h3.unjs.io --plain
npx mdzilla npm:consola --plain
```

Export docs for offline processing:

```sh
npx mdzilla <source> --export ./fetched-docs
```

Then read the exported `.md` files as needed.

## Programmatic API

```js
import { DocsManager, DocsSourceFS, DocsSourceGit, DocsSourceHTTP, DocsSourceNpm } from "mdzilla";

// Local filesystem
const docs = new DocsManager(new DocsSourceFS("./docs"));

// GitHub repo
const docs = new DocsManager(new DocsSourceGit("unjs/h3"));

// npm package
const docs = new DocsManager(new DocsSourceNpm("h3"));

// HTTP (llms.txt → markdown negotiation → HTML→md fallback)
const docs = new DocsManager(new DocsSourceHTTP("https://h3.unjs.io"));

await docs.load();
console.log(docs.tree); // NavEntry[] navigation tree
console.log(docs.flat); // FlatEntry[] flat list

const content = await docs.getContent(docs.flat[0]);
const results = docs.filter("query"); // fuzzy search
```

### Export API

```js
import { DocsExporterFS } from "mdzilla";

const exporter = new DocsExporterFS("./output");
await exporter.export(docs.flat, docs);
```
