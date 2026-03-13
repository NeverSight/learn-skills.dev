---
name: hashline
description: "A safer, less error-prone alternative to patch/diff editing (e.g. apply_patch): reads files as LINE:HASH anchors and applies fail-fast, line-addressed edits."
allowed-tools: Bash(cargo rustc)
---

# Hashline Rust Tools

This skill provides a small CLI (`hashline`) that implements:

- `read`: prints file contents with hashline prefixes `LINE:HASH|content`
- `edit`: applies a list of hash-verified edits (`set_line`, `replace_lines`, `insert_after`, optional `replace`)

The goal is fail-fast edits: if the file changed since the agent last read it, anchors won’t match and the edit will be rejected.

## Build

If `hashline` is already on your `PATH` (for example installed via Nix/Home Manager), skip this section.

Otherwise, from the skill directory:

```bash
cd ~/.codex/skills/hashline
cargo build
```

Binary path:

```bash
~/.codex/skills/hashline/target/debug/hashline
```

## Read

```bash
hashline read path/to/file.txt
```

Optional:

```bash
hashline read path/to/file.txt --offset 10 --limit 50
```

Output format:

```
12:1a2b|some line content
13:9f00|next line
```

Use the `LINE:HASH` part (example `13:9f00`) as anchors in edits.

## Edit

Edits JSON can be either an array of edit objects, or an object with `{ "edits": [...] }`.

### 1) Set (replace) a single line

```bash
hashline edit path/to/file.txt --edits-json '
[
  {"set_line": {"anchor": "3:abcd", "new_text": "replaced content"}}
]
'
```

- `new_text` may contain `\n` to replace the single line with multiple lines.
- `new_text: ""` deletes that line.

### 2) Replace a range of lines

```bash
hashline edit path/to/file.txt --edits-json '
[
  {"replace_lines": {"start_anchor": "5:aaaa", "end_anchor": "8:bbbb", "new_text": "new block\nsecond line"}}
]
'
```

- `new_text: ""` deletes the whole range.

### 3) Insert after a line

```bash
hashline edit path/to/file.txt --edits-json '
[
  {"insert_after": {"anchor": "10:ccdd", "text": "inserted line"}}
]
'
```

### 4) Content replace (no anchors)

This is optional and runs after anchor-based edits.

```bash
hashline edit path/to/file.txt --edits-json '
[
  {"replace": {"old_text": "foo", "new_text": "bar", "all": true}}
]
'
```

## Preview

```bash
hashline edit path/to/file.txt --edits-file edits.json --preview
```

## Agent usage pattern

1. `hashline read <file>`
2. Select the exact line anchors you will target.
3. Call `hashline edit <file> --edits-json ...` with those anchors.
4. If you get a “changed since last read” error, re-read and retry with updated anchors.
