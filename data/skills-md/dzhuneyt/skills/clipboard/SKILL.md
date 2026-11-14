---
name: clipboard
description: Copy the last meaningful output from the conversation to the macOS clipboard via pbcopy. Use when user wants to copy, grab, or export the last response.
argument-hint: 
allowed-tools: Bash
---

Copy your last substantive output to the macOS clipboard.

## Rules

- Strip any leading/trailing meta-commentary (e.g., "Here's what I found:", "Let me know if...", "Done.", "Copied to clipboard.")
- Keep only the core content the user would want to paste somewhere
- If the last output was a list, table, or code block — copy it as-is
- If the last output was prose with surrounding filler — extract the meaningful part

## Command

```bash
cat <<'EOF' | pbcopy
<paste the extracted content here>
EOF
```

After copying, confirm: "Copied to clipboard."
