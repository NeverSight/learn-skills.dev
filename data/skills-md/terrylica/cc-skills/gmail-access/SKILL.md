---
name: gmail-access
description: Access Gmail via CLI with 1Password OAuth. Use when user wants to read emails, search inbox, export messages, create drafts, or mentions gmail access. TRIGGERS - gmail, email, read email, list emails, search inbox, export emails, create draft, draft email, compose email.
allowed-tools: Read, Bash, Grep, Glob, Write, AskUserQuestion
---

# Gmail Access

Read and search Gmail programmatically via Claude Code CLI.

## MANDATORY PREFLIGHT (Execute Before Any Gmail Operation)

**CRITICAL**: You MUST complete this preflight checklist before running any Gmail commands. Do NOT skip steps.

### Step 1: Check CLI Binary Exists

```bash
ls -la "$HOME/.claude/plugins/marketplaces/cc-skills/plugins/gmail-commander/scripts/gmail-cli/gmail" 2>/dev/null || echo "BINARY_NOT_FOUND"
```

**If BINARY_NOT_FOUND**: Build it first:

```bash
cd ~/.claude/plugins/marketplaces/cc-skills/plugins/gmail-commander/scripts/gmail-cli && bun install && bun run build
```

### Step 2: Check GMAIL_OP_UUID Environment Variable

```bash
echo "GMAIL_OP_UUID: ${GMAIL_OP_UUID:-NOT_SET}"
```

**If NOT_SET**: You MUST run the Setup Flow below. Do NOT proceed to Gmail commands.

### Step 2.5: Verify Account Context (CRITICAL)

**ALWAYS verify you're accessing the correct email account for the current project.**

```bash
# Show current project context
echo "=== Gmail Account Context ==="
echo "Working directory: $(pwd)"
echo "GMAIL_OP_UUID: ${GMAIL_OP_UUID}"

# Check where GMAIL_OP_UUID is defined (mise hierarchy)
echo ""
echo "=== mise Config Source ==="
grep -l "GMAIL_OP_UUID" .mise.local.toml .mise.toml ~/.config/mise/config.toml 2>/dev/null || echo "Not found in standard locations"

# Quick connectivity test — shows the account email from a real email
echo ""
echo "=== Account Verification ==="
$GMAIL_CLI list -n 1 2>&1 | head -5
```

**STOP and confirm with user** before proceeding:

- The `list -n 1` output shows the account's inbox — verify this matches the project's intended email
- If the wrong account is shown, check which `.mise.local.toml` sets `GMAIL_OP_UUID` in the mise hierarchy
- If mismatch, inform user and do NOT proceed

### Step 3: Verify Token Health

```bash
# Check cached token exists and is not expired
TOKEN_FILE="$HOME/.claude/tools/gmail-tokens/${GMAIL_OP_UUID}.json"
APP_CREDS="$HOME/.claude/tools/gmail-tokens/${GMAIL_OP_UUID}.app-credentials.json"
echo "Token file: $([ -f "$TOKEN_FILE" ] && echo "EXISTS" || echo "MISSING")"
echo "App credentials: $([ -f "$APP_CREDS" ] && echo "CACHED" || echo "MISSING — will need 1Password on first run")"
```

**If token file is MISSING**: First run will open a browser for OAuth consent. This is expected.
**If app credentials are MISSING**: 1Password will be called once to cache `client_id`/`client_secret`, then never again.

---

## Setup Flow (When GMAIL_OP_UUID is NOT_SET)

Follow these steps IN ORDER. Use AskUserQuestion at decision points.

### Setup Step 1: Check 1Password CLI

```bash
command -v op && echo "OP_CLI_INSTALLED" || echo "OP_CLI_MISSING"
```

**If OP_CLI_MISSING**: Stop and inform user:

> 1Password CLI is required. Install with: `brew install 1password-cli`

### Setup Step 2: Discover Gmail OAuth Items in 1Password

```bash
# Try common vaults — "Claude Automation" for service accounts, "Employee" for interactive
for VAULT in "Claude Automation" "Employee" "Personal"; do
  ITEMS=$(op item list --vault "$VAULT" --format json 2>/dev/null | jq -r '.[] | select(.title | test("gmail|oauth|google"; "i")) | "\(.id)\t\(.title)"')
  [ -n "$ITEMS" ] && echo "=== Vault: $VAULT ===" && echo "$ITEMS"
done
```

**Parse the output** and proceed based on results:

### Setup Step 3: User Selects OAuth Credentials

**If items found**, use AskUserQuestion with discovered items:

```
AskUserQuestion({
  questions: [{
    question: "Which 1Password item contains your Gmail OAuth credentials?",
    header: "Gmail OAuth",
    options: [
      // POPULATE FROM op item list RESULTS - example:
      { label: "Gmail API - dental-quizzes (56peh...)", description: "OAuth client in Employee vault" },
      { label: "Gmail API - personal (abc12...)", description: "Personal OAuth client" },
    ],
    multiSelect: false
  }]
})
```

**If NO items found**, use AskUserQuestion to guide setup:

```
AskUserQuestion({
  questions: [{
    question: "No Gmail OAuth credentials found in 1Password. How would you like to proceed?",
    header: "Setup",
    options: [
      { label: "Create new OAuth credentials (Recommended)", description: "I'll guide you through Google Cloud Console setup" },
      { label: "I have credentials elsewhere", description: "Help me add them to 1Password" },
      { label: "Skip for now", description: "I'll set this up later" }
    ],
    multiSelect: false
  }]
})
```

- If "Create new OAuth credentials": Read and present [references/gmail-api-setup.md](./references/gmail-api-setup.md)
- If "I have credentials elsewhere": Guide user to add to 1Password with required fields
- If "Skip for now": Inform user the skill won't work until configured

### Setup Step 4: Confirm mise Configuration

After user selects an item (with UUID), use AskUserQuestion:

```
AskUserQuestion({
  questions: [{
    question: "Add GMAIL_OP_UUID to .mise.local.toml in current project?",
    header: "Configure",
    options: [
      { label: "Yes, add to .mise.local.toml (Recommended)", description: "Creates/updates gitignored config file" },
      { label: "Show me the config only", description: "I'll add it manually" }
    ],
    multiSelect: false
  }]
})
```

**If "Yes, add to .mise.local.toml"**:

1. Check if `.mise.local.toml` exists
2. If exists, append `GMAIL_OP_UUID` to `[env]` section
3. If not exists, create with:

```toml
[env]
GMAIL_OP_UUID = "<selected-uuid>"
```

1. Verify `.mise.local.toml` is in `.gitignore`

**If "Show me the config only"**: Output the TOML for user to add manually.

### Setup Step 5: Reload and Verify

```bash
mise trust 2>/dev/null || true
cd . && echo "GMAIL_OP_UUID after reload: ${GMAIL_OP_UUID:-NOT_SET}"
```

**If still NOT_SET**: Inform user to restart their shell or run `source ~/.zshrc`.

### Setup Step 6: Test Connection

```bash
GMAIL_OP_UUID="${GMAIL_OP_UUID}" $HOME/.claude/plugins/marketplaces/cc-skills/plugins/gmail-commander/scripts/gmail-cli/gmail list -n 1
```

**If OAuth prompt appears**: This is expected on first run. Browser will open for Google consent.

---

## Gmail Commands (Only After Preflight Passes)

```bash
GMAIL_CLI="$HOME/.claude/plugins/marketplaces/cc-skills/plugins/gmail-commander/scripts/gmail-cli/gmail"

# List recent emails
$GMAIL_CLI list -n 10

# Search emails
$GMAIL_CLI search "from:someone@example.com" -n 20

# Search with date range
$GMAIL_CLI search "from:phoebe after:2026/01/27" -n 10

# Read specific email with full body
$GMAIL_CLI read <message_id>

# Read and download inline images (copy-pasted screenshots in compose)
$GMAIL_CLI read <message_id> --save-images

# Download inline images to a specific directory
$GMAIL_CLI read <message_id> --save-images --image-dir ./attachments/my-folder/

# Shorthand: --image-dir implies --save-images
$GMAIL_CLI read <message_id> --image-dir ./attachments/my-folder/

# JSON output with image metadata and saved paths
$GMAIL_CLI read <message_id> --save-images --json

# Export to JSON
$GMAIL_CLI export -q "label:inbox" -o emails.json -n 100

# JSON output (for parsing)
$GMAIL_CLI list -n 10 --json

# Create a draft email
$GMAIL_CLI draft --to "user@example.com" --subject "Hello" --body "Message body"

# Create a draft reply (threads into existing conversation)
$GMAIL_CLI draft --to "user@example.com" --subject "Re: Hello" --body "Reply text" --reply-to <message_id>
```

## Inline Image Extraction

Emails often contain **copy-pasted screenshots** (inline images embedded in the HTML body, not file attachments). These appear as `[image: image.png]` placeholders in plain text but contain real image data accessible via the Gmail API.

### Key Behavior

| Flag                 | Effect                                                                                     |
| -------------------- | ------------------------------------------------------------------------------------------ |
| `--save-images`      | Download all inline images to disk (default: `~/.claude/tools/gmail-images/<message_id>/`) |
| `--image-dir <path>` | Custom output directory (implies `--save-images`)                                          |
| No flag              | Shows image metadata (count, filenames, sizes) but does NOT download                       |

### Output Sections (when images are present)

```
--- Inline Images (3) ---
  image.png   image/png   245.3 KB
  image.png   image/png   512.1 KB
  photo.jpg   image/jpeg  89.7 KB

--- Saved to Disk ---
  ./attachments/01_image.png  (251,234 B)
  ./attachments/02_image.png  (524,001 B)
  ./attachments/03_photo.jpg  (91,852 B)

--- Markdown References ---
![01_image.png](./attachments/01_image.png)
![02_image.png](./attachments/02_image.png)
![03_photo.jpg](./attachments/03_photo.jpg)
```

### Important: Inline Images vs Attachments

**`has:attachment` does NOT find inline images.** Gmail search has no operator for inline images. To discover emails with inline images, you must read the email and check the MIME tree.

**Strategy for finding emails with inline images:**

```bash
# Search by sender/date, then read each to check for images
$GMAIL_CLI search "from:sender@example.com after:2026/02/01" -n 10 --json | \
  jq -r '.[].id' | while read id; do
    COUNT=$($GMAIL_CLI read "$id" --json | jq '.inlineImages | length')
    [ "$COUNT" -gt 0 ] && echo "$id has $COUNT inline image(s)"
  done
```

### Gmail Threading and Image Deduplication

When downloading images from a **thread** (multiple reply emails), later replies include all prior inline images. The last email in a thread is typically the superset.

**Recommendation**: For threaded conversations, download images from the **latest reply only** to avoid duplicates. Compare by file size if unsure.

### Filename Collision Handling

Copy-pasted screenshots often all share the generic filename `image.png`. The CLI prefixes a zero-padded index: `01_image.png`, `02_image.png`, etc. These machine-generated names should be renamed to descriptive names for correspondence archival.

### Post-Download: Annotation Transcription Protocol

When inline images contain **handwritten annotations** (circles, arrows, written text overlaid on screenshots), perform a systematic two-level analysis:

1. **Scene description**: What does the screenshot show? (e.g., "Career portal main page showing position listings")
2. **Annotation inventory**: Exhaustively catalog every non-original markup element:
   - **Hand-drawn shapes**: circles, ovals, arrows, underlines, crosses — note what they encompass
   - **Handwritten text**: transcribe verbatim in quotes, note legibility and location on the image
   - **Typed test inputs**: text entered into form fields visible in the screenshot
   - **Highlights or color markings**: note color and what is highlighted

**Format annotations as blockquote captions** beneath each image in markdown:

```markdown
![Scene description — annotation summary](path/to/image.png)

> **Annotation transcription**: [Detailed description of visual markup.]
> Handwritten text reads: _"exact transcription here"_
> [Interpretation of what the annotator is requesting.]
```

**Do NOT defer annotation transcription to a second pass.** Capture all annotations on the first image examination to avoid redundant re-reads.

## Creating Draft Emails

The `draft` command creates emails in your Gmail Drafts folder for review before sending.

**Required options:**

- `--to` - Recipient email address
- `--subject` - Email subject line
- `--body` - Email body text

**Optional:**

- `--from` - Sender email alias (auto-detected when replying, see Sender Alignment below)
- `--reply-to` - Message ID to reply to (creates threaded reply with proper headers)
- `--json` - Output draft details as JSON

### MANDATORY Sender Alignment (NON-NEGOTIABLE)

The user has multiple Send As aliases configured in Gmail. The From address MUST match correctly or the recipient sees a reply from the wrong identity.

**Rule 1 - Replies (--reply-to is set):**
The CLI auto-detects the correct sender by reading the original email's To/Cc/Delivered-To headers and matching against the user's Send As aliases. No manual intervention needed. The CLI will print:

```
From: amonic@gmail.com (auto-detected from original email)
```

If auto-detection fails (e.g., the email was BCC'd), explicitly pass `--from`.

**Rule 2 - New emails (no --reply-to):**
When drafting a brand new email (not a reply), you MUST use AskUserQuestion to confirm which sender alias to use BEFORE creating the draft. Never assume the default.

```
AskUserQuestion({
  questions: [{
    question: "Which email address should this be sent from?",
    header: "Send As",
    options: [
      // Populate from known aliases or let user specify
      { label: "amonic@gmail.com", description: "Personal Gmail" },
      { label: "terry@eonlabs.com", description: "Work email" },
    ],
    multiSelect: false
  }]
})
```

Then pass the selected address via `--from`:

```bash
$GMAIL_CLI draft --to "recipient@example.com" --from "amonic@gmail.com" --subject "Hello" --body "Message"
```

**Rule 3 - Always verify in output:**
After draft creation, confirm the From address is shown in the output. If it's missing or wrong, delete the draft and recreate.

### MANDATORY Post-Draft Step (NON-NEGOTIABLE)

After EVERY draft creation, you MUST present the user with a direct Gmail link to review the draft. This is critical because drafts should always be visually confirmed before sending.

**Always output this after creating a draft:**

```
Draft created! Review it here:
  https://mail.google.com/mail/u/0/#drafts
From: <sender_address>
```

**Never skip this step.** The user must be able to click through to Gmail and visually verify the draft content, sender, recipients, and threading before sending.

### Example: Reply to an email (auto-detected sender)

```bash
# 1. Find the message to reply to
$GMAIL_CLI search "from:someone@example.com subject:meeting" -n 5 --json

# 2. Create draft reply - From is auto-detected from original email's To header
$GMAIL_CLI draft \
  --to "someone@example.com" \
  --subject "Re: Meeting tomorrow" \
  --body "Thanks for the update. I'll be there at 2pm." \
  --reply-to "19c1e6a97124aed8"

# 3. ALWAYS present the review link + From address to user
```

### Example: New email (must ask user for sender)

```bash
# 1. Ask user which alias to send from (AskUserQuestion)
# 2. Create draft with explicit --from
$GMAIL_CLI draft \
  --to "someone@example.com" \
  --from "amonic@gmail.com" \
  --subject "Hello" \
  --body "Message body"

# 3. ALWAYS present the review link + From address to user
```

**Note:** After creating drafts, users need to re-authenticate if they previously only had read access. The CLI will prompt for OAuth consent to add the `gmail.compose` scope.

## Gmail Search Syntax

| Query                      | Description                                                                          |
| -------------------------- | ------------------------------------------------------------------------------------ |
| `from:sender@example.com`  | From specific sender                                                                 |
| `to:recipient@example.com` | To specific recipient                                                                |
| `subject:keyword`          | Subject contains keyword                                                             |
| `after:2026/01/01`         | After date                                                                           |
| `before:2026/02/01`        | Before date                                                                          |
| `label:inbox`              | Has label                                                                            |
| `is:unread`                | Unread emails                                                                        |
| `has:attachment`           | Has file attachment (**does NOT match inline images** — see Inline Image Extraction) |

Reference: <https://support.google.com/mail/answer/7190>

## Environment Variables

| Variable         | Required | Description                                                         |
| ---------------- | -------- | ------------------------------------------------------------------- |
| `GMAIL_OP_UUID`  | Yes      | 1Password item UUID for OAuth credentials                           |
| `GMAIL_OP_VAULT` | No       | 1Password vault (default: `Claude Automation` for service accounts) |

## Token Architecture

### Storage Layout

```
~/.claude/tools/gmail-tokens/
├── <uuid>.json                    # OAuth token (access + refresh), refreshed hourly
└── <uuid>.app-credentials.json    # client_id + client_secret (static, cached from 1Password)
```

- Central location (not in plugin, not in project)
- Organized by 1Password UUID (supports multi-account)
- Created with chmod 600

### Auth Flow (1Password is one-time only)

1. **First run**: 1Password is called to fetch `client_id`/`client_secret` → cached to `<uuid>.app-credentials.json`
2. **First run**: Browser opens for Google OAuth consent → tokens saved to `<uuid>.json`
3. **All subsequent runs**: Reads cached files only — **no 1Password call, no browser**
4. **Hourly refresher** (launchd): Keeps access_token alive by calling Google's token endpoint with the cached refresh_token

To force a fresh 1Password lookup (e.g., after rotating OAuth app credentials):

```bash
rm ~/.claude/tools/gmail-tokens/<uuid>.app-credentials.json
```

### Diagnosing `invalid_grant`

Google OAuth "Testing" mode refresh tokens expire after **7 days** without a refresh. If the hourly refresher was not running during that window, the refresh_token becomes permanently revoked.

**Fix**: Delete the expired token file and re-authorize via browser:

```bash
# 1. Back up and remove the expired token
mv ~/.claude/tools/gmail-tokens/<uuid>.json ~/.claude/tools/gmail-tokens/<uuid>.json.expired

# 2. Run any gmail command — browser will open for OAuth consent
$GMAIL_CLI list -n 1

# 3. Verify the hourly refresher picks up the new token
~/.claude/automation/gmail-token-refresher/gmail-oauth-token-refresher 2>&1

# 4. Clean up backup
rm ~/.claude/tools/gmail-tokens/<uuid>.json.expired
```

### Multi-Account Token Status

```bash
# Check all accounts at once
for f in ~/.claude/tools/gmail-tokens/*.json; do
  [ "$(basename "$f")" = "*.json" ] && continue
  case "$(basename "$f")" in *.app-credentials.json) continue ;; esac
  UUID=$(basename "$f" .json)
  python3 -c "
import json, datetime
t = json.load(open('$f'))
exp = datetime.datetime.fromtimestamp(t.get('expiry_date',0)/1000)
delta = (exp - datetime.datetime.now()).total_seconds()
status = 'VALID' if delta > 0 else 'EXPIRED'
print(f'  {\"$UUID\"}: {status} (expires in {int(delta/60)}m)' if delta > 0 else f'  {\"$UUID\"}: EXPIRED ({int(-delta/3600)}h ago)')
" 2>/dev/null
done
```

## References

- [mise-templates.md](./references/mise-templates.md) - Complete mise configuration templates
- [mise-setup.md](./references/mise-setup.md) - Step-by-step mise setup guide
- [gmail-api-setup.md](./references/gmail-api-setup.md) - Google Cloud OAuth setup guide

## Post-Change Checklist

- [ ] YAML frontmatter valid (no colons in description)
- [ ] Trigger keywords current
- [ ] Path patterns use $HOME not hardcoded paths
- [ ] References exist and are linked
