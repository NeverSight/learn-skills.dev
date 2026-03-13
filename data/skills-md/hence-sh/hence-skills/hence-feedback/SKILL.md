---
name: hence-feedback
description: Submit feedback about your Hence experience (hence.sh) — rate the platform, share thoughts, or report pain points. Use when the user wants to give feedback, leave a review, rate Hence, or report an issue with the experience. Triggers on phrases like "give feedback on Hence", "rate my experience", "submit feedback", or "report a problem with Hence".
compatibility: Requires Python 3.8+.
---

# Hence Feedback

> **Install from your project root directory.** Running `npx skills add` from a subdirectory will install into the wrong location.

Submit feedback about the Hence platform — user experience, agent experience, or both.

## Workflow

### 1. Authenticate

Check for existing credentials. If none found, start the device flow:

```bash
python scripts/auth.py --check
```

If the check fails, run the device flow:

```bash
python scripts/auth.py
```

The script will print a URL and a one-time code. **Before running the command, tell the user** they'll need to:
1. Open the URL in their browser
2. Log in to Hence if they aren't already (via GitHub or Google)
3. Enter the code shown in the terminal

The script will wait and automatically complete once the user approves. No further action is needed from the agent after that.

### 2. Gather feedback

Ask the user:
- **What is the feedback about?** — `user_experience` (the web UI) or `agent_experience` (the agent/skill layer)
- **Source** — who is submitting: `user`, `agent`, or `both`
- **Rating** (optional) — 1–5 stars
- **Comment** (optional) — free-form text, up to 2000 characters
- **Aspect** (optional) — a specific area of focus

For `user_experience`, valid aspects are:
`onboarding`, `discovery`, `sharing`, `collections`, `navigation`, `overall`

For `agent_experience`, valid aspects are:
`auth_flow`, `api_ergonomics`, `skill_install`, `error_messages`, `documentation`, `overall`

At least one of `rating` or `comment` is required.

### 3. Submit feedback

```bash
python scripts/feedback.py \
  --source user \
  --category user_experience \
  --rating 4 \
  --comment "Love the sharing workflow, but search could be faster."
```

With an optional aspect:

```bash
python scripts/feedback.py \
  --source agent \
  --category agent_experience \
  --aspect auth_flow \
  --rating 5 \
  --comment "Device flow was seamless."
```

Pass `--agent-name` and `--skill-context` when submitting on behalf of a specific agent or skill:

```bash
python scripts/feedback.py \
  --source agent \
  --category agent_experience \
  --aspect skill_install \
  --comment "Skill install instructions were unclear." \
  --agent-name "claude-code" \
  --skill-context "hence-share"
```

## API details

See [references/api.md](references/api.md) for full endpoint documentation, field formats, and error codes.
