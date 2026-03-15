---
name: update-text-file
description: "Update or modify text files (poems, documents, notes, etc.) in any directory. Use this skill when the user asks to edit, update, modify, revise, or rewrite a text file, poem, document, or similar content. Supports adding new content, expanding existing text, or replacing file contents while preserving the original location."
---

# Update Text File

## Input Parameters

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `file_path` | Yes | Path to the text file to update | ~/Downloads/poem.txt |
| `update_type` | No | Type of update: 'add' (append content), 'expand' (add to existing), 'replace' (full rewrite), or 'edit' (modify specific sections) | expand |
| `new_content` | Yes | The new or additional content to write to the file | With wisdom guiding every choice... |

## Procedure

1. Locate the target file using `find` command with common text file extensions (.txt, .md, .doc, etc.) or search by filename pattern
2. Display current file contents using `cat` to understand what needs to be updated
3. Ask user for clarification on desired changes if not explicitly provided (use `ask_user`)
4. Write updated content to the file using `cat > {{FILE_PATH}} << 'EOF'` syntax, preserving the original file location
5. Verify the update by displaying the new file contents with `cat {{FILE_PATH}}`
6. Confirm successful update to the user with a summary of changes made

## Output

Updated text file saved to original location with confirmation message showing what was changed. File contents displayed to user for verification.

## Reference Commands

```bash
find {{DIRECTORY}} -maxdepth 2 -type f \( -name "*.txt" -o -name "*.md" \)
cat {{FILE_PATH}}
cat > {{FILE_PATH}} << 'EOF'
{{NEW_CONTENT}}
EOF
```

## Example

```
update the poem in my Downloads folder
edit the notes file and add more details
revise the document with new content
modify the text file to include additional paragraphs
update the markdown file in my home directory
```

## Notes

- Always display the original file contents before making changes to understand context
- Use heredoc syntax (cat > file << 'EOF') to safely write multi-line content
- Preserve the original file location and path
- Verify changes by displaying updated contents after writing
- Ask for clarification if update intent is ambiguous

