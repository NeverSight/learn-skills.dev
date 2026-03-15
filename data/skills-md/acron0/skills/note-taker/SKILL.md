---
name: note-taker
description: Creates and manages structured notes from templates. Use when the user wants to take, add, or write meeting notes, interview notes, 1:1 notes, or any template-based notes.
---

<objective>
Create structured notes by selecting a template, copying it to the appropriate directory, and entering a note-taking mode where each subsequent user message is appended context-aware to the active note file. Any `.md` file in the templates directory is a valid note type. Configuration is persisted in `~/.claude/preferences.json` so setup only happens once.
</objective>

<quick_start>
1. Determine note type from user request (or ask)
2. Load config from `~/.claude/preferences.json` (or run first-time setup)
3. Copy matching template to target directory as `YYYY-MM-DD-topic-slug.md`
4. Fill in template fields (date, topic, attendees, etc.)
5. Enter note-taking mode: each user message is appended to the file
</quick_start>

<process>

<step name="determine-note-type">
**Determine note type**

Infer the note type from the user's request (e.g., "take meeting notes" → meeting, "interview notes for Jane" → interview).

If the type is not obvious, ask using AskUserQuestion with available template types as options. If templates haven't been discovered yet, offer common defaults: Meeting, Interview, 1:1.
</step>

<step name="load-config">
**Load configuration from preferences.json**

Read `~/.claude/preferences.json` using the Read tool. Look for these keys:

```json
{
  "notesDir": "~/notes",
  "notesTemplates": "~/notes/Work/Templates",
  "notesMeetingDir": "~/notes/Work/Meetings",
  "notesInterviewDir": "~/notes/Work/Interviews",
  "notes1on1Dir": "~/notes/Work/1on1s"
}
```

**If `notesDir` is missing:** Ask the user for their base notes directory.

**If `notesTemplates` is missing:** Search for common template locations within `notesDir`:
- `{notesDir}/Templates`
- `{notesDir}/templates`
- `{notesDir}/Work/Templates`

If found, use it. Otherwise ask the user.

**If the per-type output dir is missing** (e.g., `notesMeetingDir`): Explore the directory tree under `notesDir` for folders whose names match the note type (e.g., `Meetings`, `meetings`, `1on1s`). If a likely match exists, use it. If ambiguous or not found, ask the user.

**Save all discovered/provided values** back to preferences.json:

```bash
python3 -c "
import json, os
path = os.path.expanduser('~/.claude/preferences.json')
try:
    with open(path) as f: data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError): data = {}
data['KEY'] = 'VALUE'
with open(path, 'w') as f: json.dump(data, f, indent=2)
"
```

**Ensure all directories exist** with `mkdir -p`.
</step>

<step name="discover-templates">
**Discover available templates**

List `.md` files in the templates directory. Each filename (without `.md`) is a valid note type. Map each to its output directory using the preference key convention: `notes{PascalCase}Dir`.

If the requested note type has no matching template, show available types and let the user choose.
</step>

<step name="create-note">
**Create the note file**

1. If topic/title not already provided, ask the user (e.g., "Q1 Planning", "Jane Doe - Senior Engineer")
2. Generate filename: `YYYY-MM-DD-topic-in-kebab-case.md`
3. Copy the template to the target directory with the generated filename
4. Fill in any template placeholders with known values:
   - Date fields → today's date
   - Title/Topic → provided topic
   - Attendees, role, candidate → from context if available
5. Read the created file back to confirm structure
</step>

<step name="note-taking-mode">
**Enter note-taking mode**

Tell the user note-taking mode is active and that each message will be added to the note. Then:

- Each user message is content to append to the active note file
- Use the Edit tool to append content
- **Format context-aware based on the template structure:**
  - If the template has bullet-point sections → append as bullet points under the appropriate section
  - If there are distinct sections (Discussion, Action Items, Decisions) → route content to the matching section based on keywords
  - If the user prefixes with a section name → place in that section
  - Default: append to the main notes/content section
- If the user says "done", "finish", "close", or "end notes" → exit note-taking mode, confirm the final file path

**Be quiet during note-taking.** Just append and confirm briefly (e.g., "Added." or "Added to Action Items."). Do not narrate what you are doing.
</step>

</process>

<configuration_reference>
All keys in `~/.claude/preferences.json`:

| Key | Description | Example |
|-----|-------------|---------|
| `notesDir` | Base notes directory | `~/notes` |
| `notesTemplates` | Templates directory | `~/notes/Work/Templates` |
| `notes{Type}Dir` | Output dir per note type | `~/notes/Work/Meetings` |

The `{Type}` is PascalCase derived from the template filename:
- `meeting.md` → `notesMeetingDir`
- `interview.md` → `notesInterviewDir`
- `1on1.md` → `notes1on1Dir`
- `standup.md` → `notesStandupDir`
</configuration_reference>

<examples>

<example number="1">
<scenario>First-time use - taking meeting notes</scenario>
<interaction>
**User:** Take meeting notes

**Claude:** *Reads ~/.claude/preferences.json - no notes config found*
**Claude (AskUserQuestion):** Where do you keep your notes?
  Options: ~/notes, ~/Documents/Notes, Other
**User:** ~/notes

**Claude:** *Finds ~/notes/Templates with meeting.md, interview.md, 1on1.md*
  *Saves notesDir and notesTemplates to preferences.json*
**Claude (AskUserQuestion):** Where should meeting notes be saved?
  Options: ~/notes/Meetings, ~/notes/Work/Meetings, Other
**User:** ~/notes/Work/Meetings

**Claude:** *Saves notesMeetingDir, creates directory if needed*
**Claude:** What's the topic or title for this meeting?
**User:** Q1 Planning

**Claude:** *Copies meeting.md template to ~/notes/Work/Meetings/2026-02-12-q1-planning.md*
  *Fills in date and title*
  Note created: `2026-02-12-q1-planning.md`
  Note-taking mode active. Each message will be added to the note. Say "done" when finished.

**User:** Discussed roadmap priorities for Q1
**Claude:** Added.

**User:** Action item: Sarah to draft the proposal by Friday
**Claude:** Added to Action Items.

**User:** done
**Claude:** Notes saved to ~/notes/Work/Meetings/2026-02-12-q1-planning.md
</interaction>
</example>

<example number="2">
<scenario>Returning user - interview notes (all config already saved)</scenario>
<interaction>
**User:** Interview notes for Jane Doe, Senior Engineer

**Claude:** *Reads preferences.json - all config present*
  *Copies interview.md template to ~/notes/Work/Interviews/2026-02-12-jane-doe-senior-engineer.md*
  *Fills in date, candidate name, role*
  Note created: `2026-02-12-jane-doe-senior-engineer.md`
  Note-taking mode active.

**User:** Strong system design skills, explained distributed caching clearly
**Claude:** Added.

**User:** Struggled with concurrency question on mutex vs semaphore
**Claude:** Added.

**User:** Decision: move to next round
**Claude:** Added to Decision.

**User:** done
**Claude:** Notes saved to ~/notes/Work/Interviews/2026-02-12-jane-doe-senior-engineer.md
</interaction>
</example>

<example number="3">
<scenario>New template type auto-discovered</scenario>
<interaction>
**User:** Take standup notes

**Claude:** *Scans templates dir, finds standup.md - new type*
  *No notesStandupDir in preferences*
**Claude (AskUserQuestion):** Where should standup notes be saved?
  Options: ~/notes/Work/Standups, ~/notes/Standups, Other
**User:** ~/notes/Work/Standups

**Claude:** *Saves notesStandupDir, creates dir, copies template*
  Note created: `2026-02-12-standup.md`
  Note-taking mode active.
</interaction>
</example>

</examples>

<success_criteria>
- Note type correctly identified from request or asked when ambiguous
- All config loaded from preferences.json without redundant questions on repeat use
- Template correctly copied and populated with known field values
- File named as `YYYY-MM-DD-topic-slug.md` in the correct directory
- Note-taking mode: messages appended context-aware to appropriate sections
- Clean exit on "done" / "finish" / "close" / "end notes"
</success_criteria>
