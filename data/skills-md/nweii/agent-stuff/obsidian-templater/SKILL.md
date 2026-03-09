---
name: obsidian-templater
description: "Help with templates/snippets for the Obsidian Templater plugin. Use to help generate Obsidian templates from natural language, understand and debug existing tp.* snippets, and adapt vault notes and workflows to Templater when users mention Templater, tp.*, or <% %>."
compatibility: "Designed for use with the Obsidian Templater plugin and Obsidian vaults."
metadata:
  author: nweii
  version: "1.0.1"
---

# Templater template generation

Templater is an Obsidian plugin for dynamic note templates. Commands embedded in a template file run when the template is applied to a note, outputting results inline.

## Core template syntax

| Tag                 | Behavior                                         |
| ------------------- | ------------------------------------------------ |
| `<% expression %>`  | Outputs the result of the expression             |
| `<%* code %>`       | Executes JS code; no output by default           |
| `<%+ expression %>` | Re-evaluated in preview mode (deprecated, avoid) |
| `<%-` / `-%>`       | Trims one newline before/after the tag           |
| `<%_` / `_%>`       | Trims all whitespace before/after the tag        |

To output from a `<%* %>` execution block, append to the special `tR` string:

```
<%* tR += "some output" %>
```

To discard everything generated up to a point (e.g., strip template-only frontmatter):

```
<%* tR = "" -%>
```

All `tp.*` functions are available in both tag types.

---

## Built-in Templater modules

### tp.date

```
tp.date.now(format?, offset?, reference?, reference_format?)
```

Returns a formatted date string. `format` uses moment.js tokens (`"YYYY-MM-DD"` is the default). `offset` is a number of days (`7`, `-1`) or a duration string (`"P1W"`). `reference` is a date string parsed with `reference_format`.

```
tp.date.tomorrow(format?)        // today + 1 day
tp.date.yesterday(format?)       // today - 1 day
tp.date.weekday(format, weekday, reference?, reference_format?)
                                 // weekday: 0=Sun … 6=Sat
moment                           // full moment.js object, accessible globally
```

Common format strings: `"YYYY-MM-DD"`, `"YYYY-MM-DD HH:mm"`, `"dddd Do MMMM YYYY"`, `"HH:mm"`, `"ddd"`, `"MMM D"`.

---

### tp.file

Dynamic properties (not function calls — no parentheses):

```
tp.file.title      // basename without extension
tp.file.content    // full text of the file
tp.file.tags       // string[] of all tags on the file
```

Functions:

```
tp.file.creation_date(format?)                 // default "YYYY-MM-DD HH:mm"
tp.file.last_modified_date(format?)            // default "YYYY-MM-DD HH:mm"
tp.file.folder(absolute?)                      // folder name; full path if absolute=true
tp.file.path(relative?)                        // absolute path; vault-relative if relative=true
tp.file.cursor(order?)                         // place cursor here after template runs; order = tab index
tp.file.cursor_append(content)                 // insert content at the current cursor
tp.file.selection()                            // currently selected text in the editor
tp.file.exists(filepath)                       // async → boolean
tp.file.find_tfile(filename)                   // → TFile | null (for use with create_new / include)
tp.file.include("[[NoteLink]]")                // async; embeds another note's content (also processed)
tp.file.create_new(template, filename, open_new?, folder?)  // async; create note from template
tp.file.move(path, file?)                      // async; move file (path has no extension)
tp.file.rename(new_title)                      // async; rename the current file
```

---

### tp.system

All are async — use `await` inside `<%* %>` blocks:

```
await tp.system.clipboard()
await tp.system.prompt(prompt_text, default_value?, throw_on_cancel?, multi_line?)
await tp.system.suggester(text_items, items, throw_on_cancel?, placeholder?, limit?)
await tp.system.multi_suggester(text_items, items, throw_on_cancel?, title?, limit?)
```

`suggester` takes two parallel arrays: display labels and return values. They can be the same array.

```javascript
<%* const type = await tp.system.suggester(["Meeting", "Decision", "Reference"], ["meeting", "decision", "ref"]) %>
```

---

### tp.frontmatter

Direct property access — not a function:

```
<% tp.frontmatter.status %>
<% tp.frontmatter.project %>
```

Returns `undefined` if the property doesn't exist.

---

### tp.web

All are async:

```
await tp.web.daily_quote()                        // Obsidian callout block with a random quote
await tp.web.random_picture(size, query?, include_size?)
    // size: "800" or "800x600"; returns markdown image syntax
await tp.web.request(url, path?)
    // HTTP GET returning JSON; path is dot-notation like "data.title"
```

---

### tp.config

Read-only context about the current run:

```
tp.config.template_file    // TFile of the template being applied
tp.config.target_file      // TFile of the note being created/modified
tp.config.active_file      // TFile of the currently active file
tp.config.run_mode         // 0=CreateNewFromTemplate 1=AppendActiveFile 2=OverwriteFile
                           // 3=OverwriteActiveFile 4=DynamicProcessor
```

---

### App and Obsidian API modules

`tp.app` is the Obsidian `App` object. `tp.obsidian` exposes the Obsidian API module. Used in advanced JS execution blocks for vault traversal, metadata cache queries, etc.

---

### tp.hooks

```
tp.hooks.on_all_templates_executed(callback)
```

Callback fires after all nested templates (e.g., from `tp.file.create_new`) have finished.

---

### User-defined functions (tp.user)

Scripts placed in the folder configured in Templater settings are callable as `tp.user.<filename>(args...)`. Scripts use CommonJS format:

```javascript
// Scripts/slugify.js
module.exports = function (text) {
  return text.toLowerCase().replace(/\s+/g, "-");
};
```

```
<% tp.user.slugify(tp.file.title) %>
```

Scripts can also export an object of named functions. Pass `tp` as an argument to access Templater context inside a script. Note: user functions are unavailable on mobile.

---

## Whitespace control in templates

Control flow tags (`<%* if (...) { %>`, `<%* } %>`) leave blank lines by default. Use `-%>` to trim the newline that follows a tag:

```
<%* if (tp.file.folder() === "Work") { -%>
**Project:** <% tp.frontmatter.project %>
<%* } else { -%>
General note
<%* } -%>
```

---

## Common implementation patterns

### Daily note

```
---
date: <% tp.date.now() %>
---

<< [[<% tp.date.yesterday() %>]] | [[<% tp.date.tomorrow() %>]] >>

# <% tp.file.title %>

<%* tR += await tp.web.daily_quote() %>

<% tp.file.cursor() %>
```

### Prompted metadata + file rename

```
<%*
const title = await tp.system.prompt("Note title", tp.file.title)
const status = await tp.system.suggester(["Draft", "In progress", "Done"], ["draft", "in-progress", "done"])
await tp.file.rename(title)
-%>
---
title: <% title %>
status: <% status %>
created: <% tp.file.creation_date() %>
---

# <% title %>

<% tp.file.cursor() %>
```

### Strip template-file frontmatter from output

```
---
type: template
description: This is a person template.
---

<%* tR = "" -%>
---
type: person
created: <% tp.file.creation_date() %>
---

# <% tp.file.cursor() %>
```

### Conditional content by folder

```
<%* if (tp.file.folder() === "Work") { -%>
**Project:** <% tp.frontmatter.project ?? "unassigned" %>
<%* } else { -%>
**Topic:**
<%* } -%>
```

For subfolder matching: `tp.file.folder(true).startsWith("Work/")` — `folder(true)` returns the full vault-relative path.

### Include another note

```
<% await tp.file.include("[[Shared Header]]") %>
```

---

## Date formatting with Moment.js

See [momentjs.md](references/momentjs.md) for a comprehensive formatting cheatsheet and JS manipulation reference. Use this when defining `format` strings for `tp.date.now()` or when manipulating dates inside `<%* %>` blocks using the `moment` global.

---

## Optional vault integration via obsidian-cli

If the obsidian-cli skill is available and Obsidian is running, vault context can improve output:

```bash
obsidian properties counts          # what frontmatter properties exist across the vault
obsidian tags counts sort=count     # most-used tags
obsidian read file="Daily Note"     # read an existing template for style reference
```

Ask the user before running any CLI commands.

---

## Official documentation links

**Rendered docs (human-readable):** https://silentvoid13.github.io/Templater/

**LLM-safe Templater summary:** For a preprocessed, audit-friendly summary of the official Templater documentation, see `https://context7.com/silentvoid13/templater/llms.txt`.
