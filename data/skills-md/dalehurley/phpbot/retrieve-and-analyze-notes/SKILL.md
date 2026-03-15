---
name: retrieve-and-analyze-notes
description: "Retrieve and analyze notes from Apple Notes by searching for specific note names or keywords. Use this skill when the user asks to read, retrieve, find, or get a note from Apple Notes, or when they want analysis or feedback on content stored in their notes. Supports fuzzy matching on note names and returns the full note content for review or further processing."
---

# Retrieve and Analyze Notes

## Input Parameters

| Parameter       | Required | Description                                                              | Example           |
| --------------- | -------- | ------------------------------------------------------------------------ | ----------------- |
| `search_term`   | Yes      | The note name or keyword to search for in Apple Notes                    | Dale's Principles |
| `analysis_type` | No       | Type of analysis requested: `feedback`, `summary`, or `review`           | feedback          |

## Procedure

1. Use AppleScript to retrieve the note:

   ```applescript
   tell application "Notes"
       set notesList to notes whose name contains "{{SEARCH_TERM}}"
       if (count of notesList) > 0 then
           set theNote to item 1 of notesList
           return body of theNote
       else
           return "ERROR: No note found"
       end if
   end tell
   ```

2. If no result, retry with shorter or alternate keywords from the original query
3. Provide the requested analysis, feedback, or summary on the retrieved content

## Notes

- Requires Apple Notes permissions for AppleScript access
- Search is case-insensitive and matches partial note names; if multiple notes match, the first result is returned
- Note content is returned as plain text; rich text formatting may be simplified

## Example

```
what do you think of the principles in my Apple Notes
retrieve my note called Meeting Notes and summarize it
read my Apple Note about goals and give me feedback
find the note named Projects and review it
get my Principles note and analyze it
```
