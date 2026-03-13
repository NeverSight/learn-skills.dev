---
name: show-code
description: Open code files in a tmux pane at the relevant line using the user's preferred editor. Use when the user says "show me the code", "open this in an editor", "let me see that code", or wants to view discussed code in an editor.
---

<objective>
Open a file at a specific line in the user's preferred terminal editor inside a tmux pane. Infer the file path and line number from conversation context, manage tmux panes automatically, and persist editor preference.
</objective>

<execution_style>
**Be silent and fast.** Combine commands into as few Bash calls as possible. Do not narrate what you are doing — just do it. Only speak to the user if something goes wrong or you need information. No commentary between steps.
</execution_style>

<quick_start>
1. Infer file path and line number from conversation context
2. Resolve editor preference from `~/.claude/preferences.json`
3. Verify tmux session and ensure a second pane exists
4. Open the file in the editor via `tmux send-keys`
</quick_start>

<process>

<step name="identify-target">
**Identify target file and line**

From the conversation context, determine:
- The **absolute file path** being discussed
- The **line number** (exact or best approximation)

If either cannot be determined, ask the user. Use the Read tool or Grep tool to confirm the file exists and the line number is correct before proceeding.
</step>

<step name="resolve-editor">
**Resolve editor preference**

Read `~/.claude/preferences.json` using the Read tool and look for the `editor` key.

If the file doesn't exist or has no `editor` key, ask the user using AskUserQuestion:

- Question: "What terminal editor should I use to show code?"
- Options: "micro", "vim", "nano", "nvim"

Then save their choice. Use Bash:

```bash
python3 -c "
import json, os
path = os.path.expanduser('~/.claude/preferences.json')
try:
    with open(path) as f: data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError): data = {}
data['editor'] = 'CHOSEN_EDITOR'
with open(path, 'w') as f: json.dump(data, f, indent=2)
"
```

Replace `CHOSEN_EDITOR` with the user's selection.
</step>

<step name="verify-tmux">
**Verify tmux session**

Check if running inside tmux:

```bash
echo "$TMUX"
```

If `$TMUX` is empty, tell the user: "Sorry, this requires a tmux session. Please start tmux and try again." Then **stop** - do not proceed further.
</step>

<step name="manage-panes">
**Ensure a second pane exists**

Count panes in the current window:

```bash
tmux list-panes -F '#{pane_id} #{pane_active}'
```

- If only **1 pane** exists, create a second one:
  ```bash
  tmux split-window -h
  tmux last-pane
  ```
  The split creates a side-by-side pane. `last-pane` returns focus to the original pane (where Claude is running). **Remember that the pane was newly created** — this affects the command in the next step.

- If **2+ panes** exist, use the first inactive pane as the target. The pane is **pre-existing**.

Determine the target pane ID (the pane that is NOT active):

```bash
tmux list-panes -F '#{pane_id} #{pane_active}' | grep ' 0$' | head -1 | awk '{print $1}'
```
</step>

<step name="open-editor">
**Open editor in target pane**

Send the editor command to the target pane. Most terminal editors support `+LINE` syntax.

If the pane was **newly created** in the previous step, append `&& exit` so the pane closes automatically when the editor exits:

```bash
tmux send-keys -t TARGET_PANE 'EDITOR +LINE FILEPATH && exit' Enter
```

If the pane was **pre-existing**, do NOT append `&& exit`:

```bash
tmux send-keys -t TARGET_PANE 'EDITOR +LINE FILEPATH' Enter
```

Replace:
- `TARGET_PANE` with the pane ID from the previous step
- `EDITOR` with the user's preferred editor
- `LINE` with the line number
- `FILEPATH` with the absolute file path

**Examples:**
```bash
# Newly created pane — closes when editor exits
tmux send-keys -t %3 'micro +641 /home/user/project/main.ts && exit' Enter

# Pre-existing pane — stays open
tmux send-keys -t %3 'micro +641 /home/user/project/main.ts' Enter
```
</step>

</process>

<edge_cases>
- If the target pane has a running process (not a shell prompt), warn the user before sending keys
- If the editor is not installed, inform the user and suggest installing it
- If the line number exceeds the file length, open at the last line (most editors handle this gracefully)
- If multiple files are being discussed, ask which one to open
</edge_cases>

<success_criteria>
- File opens in the correct editor at the specified line
- Editor appears in a tmux pane (reusing existing or creating new)
- Editor preference is persisted in `~/.claude/preferences.json`
- Graceful exit with message when not in tmux
</success_criteria>
