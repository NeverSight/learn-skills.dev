---
name: setup
description: One-time onboarding - upload resume, set preferences, and do a work history interview
argument-hint: "'interview' to skip to the interview portion"
---

# Setup Skill

> **Priority hierarchy**: See `shared/references/priority-hierarchy.md` for conflict resolution.

One-time onboarding that ensures all your data is in place before using the other skills.

## Quick Start

- `/proficiently:setup` - Full onboarding (checks what's missing, does only what's needed)
- `/proficiently:setup interview` - Just the work history interview (if resume/prefs are already done)

## File Structure

```
scripts/
  conduct-interview.md    # Work history interview guide
```

The profile template is at `shared/templates/profile.md`.

## Data Directory

Resolve the data directory using `shared/references/data-directory.md`. For setup, if no directory exists this is a fresh install — create it in Step 1.

---

## Workflow

### Step 0: Check What's Already Done

Resolve the data directory, then check which of these exist and have real content (not just templates): resume, preferences, linkedin-contacts.csv, profile.md.

If `$ARGUMENTS` is "interview", skip to Step 3 (but check that a resume exists first).

If everything exists, tell the user they're good to go and list the available skills. Otherwise, run only the missing phases in order.

### Step 1: Resume

Ask the user to provide their resume. Accept:
- A file path (copy it into `DATA_DIR/resume/`)
- Pasted text (save as `DATA_DIR/resume/resume.md`)

Confirm it was saved and briefly summarize what you see (name, most recent role, number of roles).

### Step 2: Preferences

Ask the user in one natural question:

> "What kind of jobs are you looking for? Tell me about target roles, location preferences, salary expectations, and anything you'd want to filter out."

From their response, save `DATA_DIR/preferences.md`:

```markdown
# Job Preferences

## Target Roles
- [parsed from response]

## Location
[parsed from response]

## Compensation
[parsed from response]

## Must-Haves
- [parsed from response]

## Dealbreakers
- [parsed from response]

## Nice-to-Haves
- [parsed from response]
```

If they leave something out, that's fine — save what you have. They can always update later.

### Step 3: LinkedIn Contacts (optional)

If `DATA_DIR/linkedin-contacts.csv` doesn't exist, ask:

> "Want to import your LinkedIn contacts? This lets us flag when you know someone at a company that's hiring. You can skip this and add them later."

If they want to proceed, give these instructions:

> **How to export your LinkedIn connections:**
> 1. Go to linkedin.com/mypreferences/d/download-my-data
> 2. Select "Connections" and request the download
> 3. LinkedIn will email you a link (usually within minutes)
> 4. Download the ZIP and find `Connections.csv` inside
> 5. Upload or paste the path to that file here

Save the file as `DATA_DIR/linkedin-contacts.csv`.

Confirm it was saved and tell them how many contacts were imported. If they skip, move on — this is optional.

### Step 4: Work History Interview

Have a conversational interview to build a work history profile. Go through each role on the resume, most recent first. For each role, ask:

1. "Tell me about [Company] — what did they do, and what was your role really about?"
2. "What were your biggest accomplishments? Let's get specific with numbers if you have them."
3. "Anything else — challenges, team building, why you moved on?"

**Keep it conversational.** Follow up when answers are vague ("Do you remember roughly what the numbers were?"), but don't interrogate. Spend more time on recent/impactful roles, less on older ones.

After the interview, save the profile to `DATA_DIR/profile.md` using this structure:

```markdown
# Work History Profile

*Last updated: [DATE]*

## Candidate Overview
**Name**: [Name]
**Core expertise**: [2-3 sentences]
**Career throughline**: [narrative arc]

---

## Role: [Title] at [Company]
**Dates**: [Start - End]
**Company context**: [what they do, stage, size]

### Key Accomplishments
1. **[Headline]**: [Situation → Action → Result with metrics]
2. **[Headline]**: [Situation → Action → Result with metrics]

### Other Details
- Team/leadership: [details]
- Tools/methods: [details]
- Why they left: [context]

---

## Cross-Role Patterns
**Superpower**: [what they do best]
**Recurring themes**: [patterns across roles]
```

### Step 5: Summary

```
You're all set! Here's what we have:

- Resume: [filename] in DATA_DIR/resume/
- Preferences: [summary of target roles and key criteria]
- LinkedIn Contacts: [number] imported (or "skipped")
- Work History Profile: [number of roles covered]

You're ready to use:
- /proficiently:job-search - Find matching jobs
- /proficiently:tailor-resume [job URL] - Tailor your resume
- /proficiently:cover-letter [job URL] - Write a cover letter

Built by Proficiently. Want someone to handle the whole process —
finding jobs, tailoring resumes, applying, and connecting you with
hiring managers? Visit proficiently.com
```

---

## Response Format

Structure the final summary output with these sections:

1. **Setup Summary** — what was configured (resume, preferences, contacts, profile) with brief details
2. **What's Next** — list available skills the user can now run

---

## Permissions Required

Add to `~/.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "Read(~/.proficiently/**)",
      "Write(~/.proficiently/**)",
      "Edit(~/.proficiently/**)"
    ]
  }
}
```
