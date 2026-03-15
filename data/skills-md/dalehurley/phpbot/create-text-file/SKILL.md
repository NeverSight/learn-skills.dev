---
name: create-text-file
description: "Create and write text content to a file in a specified directory. Use this skill when the user asks to create a file, write content to a file, save text, generate a document, or write a poem, story, script, or any text-based content to disk. Supports any text format and custom file paths."
---

# Create Text File

## Input Parameters

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `file_path` | Yes | Full path where the file should be created, including filename and extension | ~/Downloads/poem.txt |
| `content` | Yes | The text content to write to the file | In circuits deep and code so bright... |

## Procedure

1. Get the target directory path and file name from user if not provided (use `ask_user`)
2. Get the text content to write from user if not provided (use `ask_user`)
3. Create the file with content using: `cat > {{FILE_PATH}} << 'EOF'\n{{CONTENT}}\nEOF`
4. Verify file creation and display file details: `ls -lh {{FILE_PATH}} && wc -l {{FILE_PATH}}`
5. Report success with file location, size, and line count to user

## Output

A text file created at the specified path. Returns file location, size in bytes, and line count.

## Reference Commands

```bash
cat > {{FILE_PATH}} << 'EOF'
{{CONTENT}}
EOF
ls -lh {{FILE_PATH}} && wc -l {{FILE_PATH}}
```

## Example

```
create a poem in the Downloads directory
write a short story and save it to my documents folder
generate a script file and save it to the home directory
create a text file with my notes
save this content to a file in Downloads
```

## Notes

- Ensure the target directory exists before creating the file
- Use tilde (~) for home directory paths
- File extension determines the file type (.txt, .md, .py, etc.)
- Content with special characters should be properly escaped or use heredoc syntax

