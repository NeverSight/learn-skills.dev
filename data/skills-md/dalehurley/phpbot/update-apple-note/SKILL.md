---
name: update-apple-note
description: "Update notes in Apple Notes with new content, suggestions, or enhancements. Use this skill when the user asks to update, edit, modify, or add content to an existing note in Apple Notes. Supports appending suggestions, replacing content, or enhancing existing notes with structured information."
---

# Update Apple Note

## Input Parameters

| Parameter        | Required | Description                                                                                        | Example                                          |
| ---------------- | -------- | -------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| `note_name`      | Yes      | The name of the note in Apple Notes to update                                                      | Dale's Principles                                |
| `content_to_add` | Yes      | The new content, suggestions, or enhancements to add                                               | Add measurability and action items to each point |
| `update_mode`    | No       | `append` (add to existing content) or `replace` (overwrite entire body); defaults to `append`      | append                                           |

## Procedure

1. Ask for the note name if not provided
2. Retrieve the current note content:

   ```applescript
   tell application "Notes"
       get body of note "{{NOTE_NAME}}"
   end tell
   ```

3. Prepare the new content, formatted with HTML for Notes rich text if needed
4. Update the note body:

   ```applescript
   tell application "Notes"
       set body of note "{{NOTE_NAME}}" to "{{NEW_CONTENT}}"
   end tell
   ```

   For longer or complex updates, write the AppleScript to a temp file and run with `osascript {{SCRIPT_FILE}}`

5. Verify the update by retrieving and displaying the updated content
6. Report a summary of changes made

## Notes

- Note names must match exactly as stored in Apple Notes (case-sensitive)
- Content can use HTML tags for rich text; plain text is also accepted
- Requires Apple Notes permissions for AppleScript access

## Example

```
update the note with suggestions for improvement
add these action items to my Principles note in Apple Notes
append a summary section to my Meeting Notes note
replace the content of my Goals note with this updated version
edit my Projects note to include the new deadline
```
