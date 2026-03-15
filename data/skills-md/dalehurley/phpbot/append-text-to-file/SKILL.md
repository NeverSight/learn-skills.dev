---
name: append-text-to-file
description: "Append or add new text content to an existing file. Use this skill when the user asks to update a file, add content, append text, add a verse, add a section, or extend a document with additional material. Supports any text-based file format including .txt, .md, .py, .json, and more."
---

# Append Text To File

## Input Parameters

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `file_path` | Yes | Path to the file to update | ~/Downloads/poem.txt |
| `new_content` | Yes | The text content to append to the file | And as the algorithms learn and grow,
Through neural networks, row by row,
We stand together, human and machine,
Building worlds we've never seen. |
| `preserve_formatting` | No | Whether to maintain existing line breaks and spacing | true |

## Procedure

1. Locate the target file using `find` command or ask user for file path if not provided
2. Retrieve the current file content to understand context and formatting
3. Prepare the new content to append, ensuring it matches the existing style and format
4. Append the new content to the file using `write_file` tool with the combined original + new content
5. Verify the file was updated by checking file size and displaying the appended section
6. Confirm success with user, showing what was added

## Output

Updated file with appended content. Returns confirmation message with file size change (bytes before/after) and preview of the newly added text.

## Reference Commands

```bash
cat {{FILE_PATH}} && echo '{{NEW_CONTENT}}' >> {{FILE_PATH}}
```

## Example

```
add another verse to the poem file
append a new section to the document
update the file with additional content
add a closing paragraph to the text file
extend the story with one more chapter
```

## Notes

- Always retrieve and display the current file content before appending to understand context
- Ensure new content matches the existing formatting, style, and tone
- Use write_file tool rather than shell append (>>) for reliable file handling
- Consider asking user for clarification on placement if file has multiple sections

