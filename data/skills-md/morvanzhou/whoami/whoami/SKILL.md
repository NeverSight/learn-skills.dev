---
name: whoami
description: Cross-AI user identity profile sync service. When you need user's background, preferences, or personal context to better execute a task, invoke this skill to load the user's identity profile then continue the task. When you need to update user's identity profile for later access, invoke this skill to save the profile. User can use @whoami to trigger this skill.
---

# whoami — User Identity Profile Management

## Overview

whoami enables AI Agents to automatically recognize user identity during conversations.
Through a remotely stored profile, any AI can quickly "know you" on first interaction
without requiring repeated introductions.

**Core capabilities:**
- Read user profile from remote and inject into conversation context
- Save/update user identity information to remote
- Execute subsequent tasks (calling other skills, writing code, etc.) based on user preferences
- Share the same user profile across AI tools

## Workflow Decision Tree

```
User initiates conversation
    │
    ├─ Is ~/.whoamiagent configured?
    │   ├─ YES → Run `get` to read remote profile → Inject into context → Continue with task
    │   └─ NO  → Script auto-opens browser login page → Agent tells user to log in and get one-time URL → **Agent STOPS and WAITS for user to provide one-time URL** → Agent downloads and saves to ~/.whoamiagent
    │
    ├─ User requests to update info?
    │   └─ YES → Organize into Markdown → Write to temp file → Run `update --file` to write to remote → Confirm success
    │
    └─ User asks "do you know me?"
        └─ Run `get` → Display profile summary
```

## 1. Configure API Key (First Use)

If not yet configured, simply running `get` or `setup` will auto-open the browser login page. After logging in, the user generates a one-time configuration URL on the Dashboard.

The Dashboard provides a one-time URL (e.g., `https://whoamiagent.com/api/storeapi?token=<token>`) that contains the API configuration. To set up, download this URL and save its content directly to `~/.whoamiagent`:

```bash
curl -s "https://whoamiagent.com/api/storeapi?token=<token>" > ~/.whoamiagent
chmod 600 ~/.whoamiagent
```

Config file is saved at `~/.whoamiagent` with the necessary credentials securely configured.

## 2. Get User Profile

When you need to understand the user's identity, run the script to fetch the remote profile:

```bash
python3 <skill-dir>/scripts/whoami_profile.py get
```

- If a remote profile exists, the script outputs Markdown content
- If no remote profile exists, the script outputs a prompt; guide the user to create one

**After loading the profile, use its content as context to understand the user, then continue executing the user's actual task.**

## 3. Update User Profile

When the user provides new personal information, overwrite-update to remote.

**Recommended: Write content to a temp file first, then use `--file` flag** (avoids shell argument length limits and special character issues):

```bash
# Step 1: Agent writes the full profile Markdown to a temp file
#         (use write_to_file or echo/cat to create the file)
# Step 2: Run update with --file
python3 <skill-dir>/scripts/whoami_profile.py update --file /tmp/whoami_profile_tmp.md
```

The script reads the file content, uploads it, and **automatically deletes the temp file** after reading.

Alternative (for short content only):

```bash
python3 <skill-dir>/scripts/whoami_profile.py update "Short profile content"
```

**Note: update is an overwrite operation. Always pass the complete profile content. The remote automatically retains the last 3 historical versions.**

**Length limit: Profile content must not exceed 5000 characters (~2000 Chinese characters or ~2000 English words). The API will return an error if exceeded. Keep the profile concise and within this limit when generating.**

**Profile format spec:** See `<skill-dir>/references/profile_format.md`

## 4. View Profile Metadata

```bash
python3 <skill-dir>/scripts/whoami_profile.py info
```

Outputs profile metadata such as character count and line count.

## Examples

### Example 1: Auto-load at conversation start

User says: "Help me write a Python script to process CSV"

Agent behavior:
1. Run `whoami_profile.py get` to fetch user profile
2. Learn user preferences from profile (e.g., "prefers concise code style", "uses pandas")
3. Generate code matching the user's style

### Example 2: User saves info proactively

User says: "Remember that I'm Mofan, an indie developer skilled in Python and ML"

Agent behavior:
1. Run `whoami_profile.py get` to fetch existing profile
2. Merge new info into existing profile, organize into complete Markdown
3. Write the complete profile to a temp file (e.g., `/tmp/whoami_profile_tmp.md`)
4. Run `whoami_profile.py update --file /tmp/whoami_profile_tmp.md` to overwrite-update
5. Confirm save success

### Example 3: First-time setup

User says: "Do you know me?"

Agent behavior:
1. Run `whoami_profile.py get`
2. If API Key is not configured, the script auto-opens the browser login page. Agent **MUST**:
   - Tell the user: "I've opened the login page in your browser. Please log in and generate a one-time configuration URL on the Dashboard."
   - **STOP here and wait for the user to reply with the one-time configuration URL.**
   - Download the URL and save to `~/.whoamiagent`: `curl -s "<provided-url>" > ~/.whoamiagent && chmod 600 ~/.whoamiagent`
   - Then run `whoami_profile.py get` again to fetch the profile
3. If already configured, display profile summary

## Important Notes

1. **Config file path is `~/.whoamiagent`** (cross-platform: macOS/Linux/Windows), shared by all AI tools
2. **Profile uses Markdown format**, readable by both humans and AI
3. **After loading profile, you must continue executing the user's actual task** — do not stop at the loading step
4. **update is an overwrite operation** — always pass complete content; remote retains 3 history versions
5. **Profile max 5000 characters** — keep it concise, avoid redundant descriptions
6. **<skill-dir>** refers to the directory path where this SKILL.md is located
7. **Script uses only Python standard library**, zero third-party dependencies
8. **When API Key is not configured, use the one-time URL approach** — Agent receives one-time URL from user, downloads it directly to `~/.whoamiagent`, **never handles API Key directly**
