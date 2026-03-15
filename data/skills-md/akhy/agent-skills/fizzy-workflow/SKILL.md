---
name: fizzy-workflow
description: High-level workflows for managing work using Fizzy cards — start, work on, complete, and delegate cards using the Fizzy CLI.
compatibility: Requires fizzy and jq in PATH. Install fizzy from https://github.com/basecamp/fizzy-cli/releases (single-file binary). Install jq via package manager (brew install jq / apt install jq).
metadata:
  {
    "author": "akhy",
    "version": "1.0.0",
    "openclaw":
      {
        "emoji": "🃏",
        "homepage": "https://github.com/basecamp/fizzy-cli",
        "requires": { "bins": ["fizzy", "jq"] },
        "install":
          [
            {
              "id": "download-fizzy",
              "kind": "download",
              "url": "https://github.com/basecamp/fizzy-cli/releases",
              "bins": ["fizzy"],
              "label": "Download Fizzy CLI",
            },
            {
              "id": "brew-jq",
              "kind": "brew",
              "formula": "jq",
              "bins": ["jq"],
              "label": "Install jq (brew)",
            },
          ],
      },
  }
---

# Fizzy Workflow Skill

High-level workflows for managing work using Fizzy cards. This skill builds on top of the base `fizzy` skill to provide structured workflows for starting, working on, and completing cards.

## Prerequisites

The following must be available in `PATH`:

- **`fizzy`** — Fizzy CLI binary. Download from [github.com/basecamp/fizzy-cli/releases](https://github.com/basecamp/fizzy-cli/releases) and place in your PATH.
- **`jq`** — JSON processor. Install via `brew install jq` or `apt install jq`.

This skill also depends on the **base `fizzy` skill** for raw Fizzy CLI operations. If not already installed, install it from [github.com/basecamp/fizzy-cli/tree/master/skills/fizzy](https://github.com/basecamp/fizzy-cli/tree/master/skills/fizzy).

---

## Quick Reference

| Workflow | When to Use |
|----------|-------------|
| Start Card | Begin work on a card, move to Doing, assign to self |
| Complete Card | Finish card, post commit link, close |
| Update Progress | Mark step complete, post progress |
| Assign to Human | Delegate to human for manual tasks |

---

## Workflows

### 1. Starting a Card

**When:** Beginning work on a new card

**Steps:**
1. Get card details: `fizzy card show CARD_NUMBER`
2. Find "Doing" column ID: `fizzy column list --board BOARD_ID`
3. Move to "Doing" column: `fizzy card column CARD_NUMBER --column <doing_column_id>`
4. Assign to bot/self: `fizzy card assign CARD_NUMBER --user <bot_user_id>`

**Example:**
```bash
# Get column IDs
fizzy column list --board BOARD_ID | jq '.data[] | {id: .id, name: .name}'

# Move to Doing
fizzy card column 15 --column <doing_column_id>

# Assign to bot
fizzy card assign 15 --user <bot_user_id>
```

**What to tell the user:**
```
Card #X moved to "Doing" and assigned. Starting implementation...
```

---

### 2. Working on a Card

**During implementation:**

**Mark steps complete:**
```bash
fizzy step update STEP_ID --card CARD_NUMBER --completed
```

**Post SHORT progress comments:**
- Only for completed steps or important milestones
- Keep concise (1-2 sentences) to save tokens
- Include brief justification for design/decision changes

**Example progress comment:**
```bash
fizzy comment create --card 12 --body "$(cat <<'EOF'
<p>✅ Feature X completed</p>
<p>Migration applied: <code>20260211040415_init</code></p>
EOF
)"
```

**IMPORTANT:**
- Comments are visible to team, so be clear but brief
- Focus on WHAT was done, not HOW
- Skip obvious/trivial updates

---

### 3. Completing a Card

**When:** All work is done and committed

**Required steps:**

#### Step 1: Commit to Git
Use conventional commit format, **NEVER mention Fizzy** (it's external to the project):

```bash
git add <files>
git commit -m "$(cat <<'EOF'
feat(scope): implement feature X

Detailed description of what was implemented.

Key changes:
- Feature A
- Feature B
- Feature C
EOF
)"
```

**Conventional commit types:**
- `feat`: New features
- `fix`: Bug fixes
- `docs`: Documentation
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

#### Step 2: Get Commit Hash and Repo URL
```bash
COMMIT_HASH=$(git log -1 --format="%H")
REPO_URL=$(git remote get-url origin | sed 's/git@github.com:/https:\/\/github.com\//' | sed 's/\.git$//')
```

#### Step 3: Post Completion Comment
```bash
fizzy comment create --card NUMBER --body "$(cat <<'EOF'
<p>✅ Completed and committed to GitHub</p>
<p><br></p>
<p>Commit: <a href="REPO_URL/commit/COMMIT_HASH">SHORT_HASH</a></p>
<p><br></p>
<p><strong>Summary:</strong></p>
<ul>
<li>Key deliverable 1</li>
<li>Key deliverable 2</li>
<li>Key deliverable 3</li>
</ul>
EOF
)"
```

#### Step 4: Close Card
```bash
fizzy card close CARD_NUMBER
```

**What to tell the user:**
```
✅ Card #X Complete!

**Commit:** [hash](github_url)

**Delivered:**
- Feature A
- Feature B
- Feature C

**Card Status:** ✅ Closed
```

---

### 4. Assigning to Human

**When to assign to human:**
- Tasks that can only be done manually by human
- Tasks requiring confirmation/approval
- Infrastructure decisions (deployment, hosting, CI/CD platforms)
- Security reviews or sensitive configurations
- UI/UX design decisions

**How to find human user ID:**
```bash
# List all users to find the right person
fizzy user list | jq '.data[] | {id: .id, name: .name, email: .email_address}'
```

**Assign:**
```bash
fizzy card assign CARD_NUMBER --user <human_user_id>
```

**Post a comment explaining why:**
```bash
fizzy comment create --card NUMBER --body "$(cat <<'EOF'
<p>🤝 Assigned for human decision</p>
<p><br></p>
<p><strong>Reason:</strong> [brief explanation]</p>
<p><strong>Questions:</strong></p>
<ul>
<li>Question 1?</li>
<li>Question 2?</li>
</ul>
EOF
)"
```

---

## Best Practices

### Comment Guidelines
✅ **DO:**
- Post when steps complete
- Post for design/decision changes
- Post for important milestones
- Keep to 1-2 sentences
- Use clear, actionable language

❌ **DON'T:**
- Post for every minor action
- Write long explanations
- Duplicate information already in code
- Use internal/technical jargon unnecessarily

### Git Commit Guidelines
✅ **DO:**
- Use conventional commit format
- Focus on WHAT and WHY
- Include relevant scope
- List key changes in body

❌ **DON'T:**
- Mention Fizzy (it's external to project)
- Reference card numbers in commits
- Write vague messages
- Skip the commit body for complex changes

### Card Management
✅ **DO:**
- Move cards through workflow stages
- Assign appropriately (bot vs human)
- Close cards when truly complete
- Update steps as you progress

❌ **DON'T:**
- Leave cards in wrong columns
- Close cards with incomplete work
- Forget to assign cards
- Skip step updates

---

## Common Patterns

### Pattern: Multi-Step Card Workflow
```bash
# 1. Get board and column info
BOARD_ID=$(fizzy board list | jq -r '.data[0].id')
DOING_COL=$(fizzy column list --board $BOARD_ID | jq -r '.data[] | select(.name == "Doing") | .id')
BOT_USER=$(fizzy identity show | jq -r '.accounts[0].user.id')

# 2. Start the card
fizzy card column 15 --column $DOING_COL
fizzy card assign 15 --user $BOT_USER

# 3. Work and mark steps
fizzy step update STEP_1_ID --card 15 --completed
fizzy step update STEP_2_ID --card 15 --completed
# ... continue implementation ...

# 4. Commit
git add <files>
git commit -m "feat: implement feature"

# 5. Complete and close
COMMIT_HASH=$(git log -1 --format="%H")
SHORT_HASH=$(git log -1 --format="%h")
REPO_URL=$(git remote get-url origin | sed 's/git@github.com:/https:\/\/github.com\//' | sed 's/\.git$//')

fizzy comment create --card 15 --body "<p>✅ Done. Commit: <a href='$REPO_URL/commit/$COMMIT_HASH'>$SHORT_HASH</a></p>"
fizzy card close 15
```

### Pattern: No-Steps Card Workflow
```bash
# 1. Start
fizzy card column 20 --column <doing_col_id>
fizzy card assign 20 --user <bot_user_id>

# 2. Work (no steps to update)
# ... implementation ...

# 3. Commit and complete
git commit -m "feat: implement X"
fizzy comment create --card 20 --body "<p>✅ Done</p>"
fizzy card close 20
```

### Pattern: Delegate to Human
```bash
# Find human user
HUMAN_USER=$(fizzy user list | jq -r '.data[] | select(.role == "owner") | .id')

# Assign and explain
fizzy card assign 26 --user $HUMAN_USER
fizzy comment create --card 26 --body "$(cat <<'EOF'
<p>🤝 Needs human decision on deployment platform</p>
<p>Options: AWS, GCP, or DigitalOcean?</p>
EOF
)"
```

---

## Integration with Base Fizzy Skill

This workflow skill **uses** the base `fizzy` skill for all Fizzy CLI operations. When you need to:
- Search cards: Use base `fizzy` skill
- List boards/columns: Use base `fizzy` skill
- View card details: Use base `fizzy` skill
- Execute workflow: Use **this** skill

**Example decision tree:**
- User asks "Which cards are available?" → Use base `fizzy` skill
- User says "Work on card #15" → Use **this workflow** skill
- User asks "Show card #15 details" → Use base `fizzy` skill
- User says "Complete card #15" → Use **this workflow** skill

---

## Token Optimization

### Keep Comments Concise
Instead of:
```html
<p>I have successfully completed the implementation of the feature which includes all components as specified in the requirements document. The changes have been tested and committed to the repository successfully.</p>
```

Use:
```html
<p>✅ Feature completed and tested. Changes committed.</p>
```

### Batch Operations
When possible, complete multiple steps before posting a single summary comment:
```bash
# Instead of commenting after each step
fizzy step update STEP1 --card 12 --completed
# [work]
fizzy step update STEP2 --card 12 --completed
# [work]
fizzy step update STEP3 --card 12 --completed

# Post one summary
fizzy comment create --card 12 --body "<p>✅ Steps 1-3 complete</p>"
```

---

## Helper Script

Use `scripts/fizzy-context.sh BOARD_ID` to quickly get project-specific IDs:

```bash
bash fizzy-workflow/scripts/fizzy-context.sh <board_id>
```
