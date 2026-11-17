---
name: ems
description: Smart daily EMS / Timesheet task entry generator with first-time onboarding, customizable formatting templates, and automated end-of-day scheduling. Triggered via /ems or when the user asks for timesheet/EMS entries.
---

# EMS / Timesheet Entry Generator

Generates accurate, professional, and compliant daily EMS / timesheet entries from your Antigravity conversation history and code activity.

## When to Use
- When the user runs `/ems`
- When the user runs `/ems setup` or `/ems config`
- When the user provides conversation UUIDs or requests timesheet / task entries for today or any specific date.

---

## 1. First-Time Setup & Onboarding Check

Before generating entries, check whether the user has configured their preferences:

1. Run:
   ```bash
   python "scripts/setup_wizard.py" --check
   ```
2. If `NOT_CONFIGURED` (or if the user explicitly ran `/ems setup`):
   **Guide the user through the 3-step setup interview**:

   * **Step 1: Preferred Format & Samples**
     Ask the user how they would like their entries formatted:
     - **Option A (Tab-Separated EMS / Timesheet)**:
       `[Client]\t[Module]\t[Type]\t[Task Title]` followed by bullets and `\t[Est]\t[Actual]\t\t[Status]\t[Approval]`
     - **Option B (Ticket & Bullet List)**:
       `[Ticket Number]: [Title]` followed by concise accomplishment bullets.
     - **Option C (Markdown Table)**:
       `| Client | Ticket | Summary | Hours | Status |`
     - **Option D (Custom Format)**:
       Invite the user to paste 1-2 examples of their ideal task entry.

   * **Step 2: Constraints & Rules**
     - Character limit (e.g., *Under 700 characters* per entry, *Under 500 characters*, or *No limit*).
     - Default project / client name (e.g., `CE21`, `Internal`, or detect from workspace).
     - Default hours block (e.g., `04:00`, `08:00`, or based on task complexity).
     - Tone: Concise, professional, non-technical (focusing on business value and root cause).

   * **Step 3: End-of-Day Daily Automation**
     Ask whether they want an automated summary created at the end of every workday:
     - Preferred time (e.g., `6:30 PM` / `18:30`).
     - Timezone (e.g., `Asia/Kolkata`, `America/New_York`, `UTC`).
     - If yes, automatically configure the scheduled automation sidecar.

   Save their answers by writing `~/.gemini/config/ems-user-config.json` (or calling `python scripts/setup_wizard.py`).

---

## 2. Standard Generation Workflow (Configured)

Once preferences are saved, generating entries is seamless:

### Step 1: Detect Conversation Source
- **Explicit UUID(s)**: If user passed one or more conversation IDs in the prompt (e.g., `/ems daba5827-c3d3-431c-9680-e77c2a0159ff`), process those IDs.
- **Date / "Today"**: If user ran `/ems` or `/ems today`, run:
  ```bash
  python "scripts/extract_context.py" today
  ```
- **"Yesterday"**: If user ran `/ems yesterday`, run:
  ```bash
  python "scripts/extract_context.py" yesterday
  ```

### Step 2: Context Extraction & Synthesis
- Extract ticket IDs, problem statements, root cause findings, modified files, and solutions.
- Synthesize 4 to 5 concise, active-verb, non-technical bullet points describing the work.
- Apply the user's saved format, template, and client/module columns.
- Ensure the total character length strictly satisfies the configured character limit (e.g. `< 700 characters`).

### Step 3: Output
Output the generated entry in a clean markdown codeblock (` ```markdown ... ``` `) ready for one-click copying into EMS.
