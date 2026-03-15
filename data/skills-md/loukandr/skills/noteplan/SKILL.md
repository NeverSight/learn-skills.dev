---
name: noteplan
description: Comprehensive knowledge for NotePlan, the Markdown-based productivity app that combines note-taking, task management, and calendar integration. Use this skill whenever the user mentions NotePlan, asks about NotePlan markdown syntax, task scheduling, calendar notes, daily/weekly/monthly/quarterly/yearly notes, project notes, time blocking, templates, frontmatter, search filters, wiki-links, backlinks, tags, mentions, the NotePlan URL scheme (noteplan://), synced lines, Apple Calendar or Reminders integration within NotePlan, NotePlan themes, Kanban/folder views, or wants to build/modify/debug NotePlan plugins (plugin.json, script.js, JavaScript API with DataStore, Editor, CommandBar, HTMLView, Calendar, Clipboard objects).
---

# NotePlan

Markdown-based productivity app combining notes, tasks, and calendar. Available on macOS, iOS, iPadOS, and web. All data stored as plain text Markdown files (.txt default, configurable to .md). Syncs via CloudKit (recommended) or iCloud Drive.

## Note Types

### Calendar Notes (Periodic)
Tied to dates. File naming conventions:

| Period    | Filename       | Example        |
|-----------|----------------|----------------|
| Daily     | `YYYYMMDD.txt` | `20260220.txt` |
| Weekly    | `YYYY-Www.txt` | `2026-W08.txt` |
| Monthly   | `YYYY-MM.txt`  | `2026-02.txt`  |
| Quarterly | `YYYY-Qq.txt`  | `2026-Q1.txt`  |
| Yearly    | `YYYY.txt`     | `2026.txt`     |

Daily and weekly enabled by default. Monthly, quarterly, yearly toggled in Preferences > Calendar.

### Project Notes
Regular notes in sidebar folders. First line becomes the title (unless overridden by frontmatter `title` property). Stored in `Notes/` folder.

## Task Syntax

Three line-start markers (configurable in Preferences > Markdown):

| Marker                 | Default   | Visual          |
|------------------------|-----------|-----------------|
| `*` (asterisk + space) | Task      | Round checkbox  |
| `-` (dash + space)     | Bullet    | No checkbox     |
| `+` (plus + space)     | Checklist | Square checkbox |

### Task States

```
* task text          → Open
* [x] task text      → Done
* [-] task text      → Cancelled
* [>] task text      → Scheduled/Rescheduled
```

Same states apply with `+` for checklists and `-` when configured as task.

Checklists (`+`) differ from tasks: they do not appear in overdue filters, do not increment the overdue counter, and do not contribute to calendar heat maps.

### Scheduling

Append date tags to tasks to schedule them:

| Syntax        | Target                           |
|---------------|----------------------------------|
| `>YYYY-MM-DD` | Daily note (e.g., `>2026-02-20`) |
| `>YYYY-Www`   | Weekly note (e.g., `>2026-W08`)  |
| `>YYYY-MM`    | Monthly note                     |
| `>YYYY-Qq`    | Quarterly note                   |
| `>YYYY`       | Yearly note                      |
| `>today`      | Today                            |
| `>tomorrow`   | Tomorrow                         |
| `>nextweek`   | Next week                        |
| `>Friday`     | Next Friday (any weekday name)   |

Back-link `<YYYY-MM-DD` indicates the source date of a rescheduled task.

Completion timestamp: `@done(YYYY-MM-DD)` or `@done(YYYY-MM-DD HH:mm)` (controlled by Preferences > Todo > Append Completion Date).

### Priority Markers

Place at line beginning:

| Syntax | Level         |
|--------|---------------|
| `!`    | Important     |
| `!!`   | Urgent        |
| `!!!`  | Very urgent   |
| `>>`   | Current focus |

### Recurring Tasks

Built-in: `@repeat(occurrence/total)` (e.g., `@repeat(3/10)` means 3rd of 10).

With the Repeat Extensions plugin: `@repeat(Nx)` where N is a number and x is a unit (`d` days, `w` weeks, `m` months, `q` quarters, `y` years, `b` business days). Prefix with `+` to calculate from completion date instead of due date: `@repeat(+1w)`.

## Links

| Syntax                           | Purpose                                 |
|----------------------------------|-----------------------------------------|
| `[[Note Title]]`                 | Link to project note (creates backlink) |
| `[[YYYY-MM-DD]]`                 | Link to daily calendar note             |
| `[[Note Title#Heading]]`         | Link to heading in note                 |
| `[[Note Title^blockID]]`         | Link to synced line                     |
| `[display text]([[Note Title]])` | Link alias (custom display text)        |
| `[text](url)`                    | Standard markdown link                  |

Synced lines carry a unique ID (`^abc123`) and changes propagate to all copies. Create with CMD+drag (Mac/iPad) or context menu.

## Tags and Mentions

- Hashtags: `#tag`, nested with `/`: `#books/business`
- Mentions: `@person`, nested: `@team/jakob`
- Attributed tags (v3.17+): `#todo(state: backlog, assigned: Eduard)`

Click any tag or mention to surface all matching occurrences.

## Time Blocking

Add time to any bullet, task, checklist, or heading:

```
* 5:00pm Reply to emails
- 09:00 - 11:00 Communications
## 14:00 - 15:00 Deep work
```

Supports 12-hour (`5:00pm`) and 24-hour (`14:00`) formats. In project notes, include a date tag: `* 5:00pm Task >2026-02-20`. Can sync to external calendars via settings.

## Frontmatter

YAML block at the very start of a note between `---` markers:

```yaml
---
title: My Project
icon: folder
icon-color: Amber 500
---
```

Reserved keys: `title` (overrides note title), `icon`, `icon-color`, `icon-style` (`regular`/`solid`/`light`), `bg-color`, `bg-color-dark`, `bg-pattern` (`lined`/`squared`/`mini-squared`/`dotted`), `triggers` (plugin triggers).

Custom keys are supported for use in folder views (filtering, grouping, sorting).

## Extended Markdown

| Syntax                   | Effect                                           |
|--------------------------|--------------------------------------------------|
| `**bold**`               | Bold                                             |
| `*italic*`               | Italic                                           |
| `~~text~~`               | Strikethrough                                    |
| `==text==` or `::text::` | Highlighting                                     |
| `~text~`                 | Underline                                        |
| `%%comment%%`            | Hidden comment (invisible unless cursor on line) |

Tables, code blocks (with language specifier), blockquotes, and images are supported.

## Key Keyboard Shortcuts (macOS)

| Shortcut            | Action                                          |
|---------------------|-------------------------------------------------|
| `CMD+J`             | Open Command Bar                                |
| `CMD+D`             | Complete task                                   |
| `CMD+R`             | Cancel task                                     |
| `Shift+CMD+D`       | Open schedule menu                              |
| `CMD+0/1/2/3`       | Reschedule to today/tomorrow/+2 days/next week  |
| `CMD+E`             | Create event                                    |
| `Shift+CMD+E`       | Create reminder                                 |
| `CMD+K`             | Add link                                        |
| `CMD+/`             | Fold text                                       |
| `Ctrl+CMD+up/down`  | Move lines up/down                              |

Customize via macOS System Settings > Keyboard > Shortcuts > App Shortcuts.

## File Storage Paths

- **App Store:** `~/Library/Containers/co.noteplan.NotePlan3/Data/Library/Application Support/co.noteplan.NotePlan3`
- **Setapp:** `~/Library/Containers/co.noteplan.NotePlan-setapp/Data/Library/Application Support/co.noteplan.NotePlan-setapp`
- **iCloud Drive:** Files app > iCloud Drive > NotePlan

## Integration

- **Apple Calendar**: Syncs iCloud, Google, Outlook calendars. Events in timeline sidebar. Create with CMD+E.
- **Apple Reminders**: Bidirectional sync. Create with Shift+CMD+E.
- **Apple Shortcuts**: 7 actions (Add to Note, Open Note, Find Notes, Create Note, Open Filter, Open Tag, Run Plugin Command). Can trigger via Siri.
- **Folder Views**: List and Cards/Kanban layouts. Filter, group, sort by folder, tag, date, or frontmatter fields. Named views saveable per folder.

## Reference Files

Read these for detailed information on specific topics:

- **`references/markdown-and-tasks.md`** — Detailed markdown syntax, all paragraph types, checklist vs task differences, synced lines, attributed tags, custom markdown via themes
- **`references/url-scheme.md`** — Complete noteplan:// x-callback-url reference with all actions, parameters, and examples
- **`references/templates.md`** — Template system: types, all template tags (date, prompt, web service, meeting note), auto-insert templates, JavaScript in templates
- **`references/search-and-filters.md`** — Advanced search syntax, all operators (source, date, task status, location, sort), boolean logic, predefined and custom filters
- **`references/plugin-development.md`** — Complete plugin development guide: architecture, full JavaScript API reference (NotePlan, Editor, DataStore, CommandBar, Calendar, Clipboard, HTMLView), plugin.json schema, HTMLView patterns (communication, theming, auto-refresh), publishing workflow, and acceptance requirements
