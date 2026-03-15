---
name: clipboard
description: "Read from and write to the system clipboard. Use this skill when the user asks to copy text to clipboard, paste clipboard contents, get clipboard contents, read what's on the clipboard, or set the clipboard to a value."
tags: [clipboard, copy, paste, pbcopy, pbpaste, utility]
version: 0.1.0
---

# Skill: clipboard

## When to Use

Use this skill when the user asks to:

- Copy text to the clipboard
- Read/get/paste clipboard contents
- Set the clipboard to a specific value
- Check what's currently on the clipboard
- Transfer text via clipboard

## Input Parameters

| Parameter | Required  | Description                   | Example     |
| --------- | --------- | ----------------------------- | ----------- |
| `action`  | Yes       | Either `read` or `write`      | read        |
| `text`    | For write | The text to copy to clipboard | Hello World |

## Procedure

1. Determine whether the user wants to read or write the clipboard
2. Run the bundled script:

   ```bash
   # Read clipboard contents
   bash skills/clipboard/scripts/clip.sh read

   # Write text to clipboard
   bash skills/clipboard/scripts/clip.sh write "text to copy"
   ```

3. Report the result to the user

## Bundled Scripts

| Script            | Type | Description                            |
| ----------------- | ---- | -------------------------------------- |
| `scripts/clip.sh` | SH   | Read from or write to system clipboard |

### Script Usage

```bash
# Read clipboard
bash scripts/clip.sh read

# Write text to clipboard
bash scripts/clip.sh write "Hello World"

# Pipe content to clipboard
echo "piped content" | bash scripts/clip.sh write
```

## Example

```
copy "hello world" to the clipboard
what's on my clipboard?
paste the clipboard contents
set clipboard to the current date
read the clipboard
```
