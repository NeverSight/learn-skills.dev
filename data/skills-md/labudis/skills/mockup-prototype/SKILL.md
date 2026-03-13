---
name: mockup-prototype
description: 'Generate interactive HTML mockups from a description, iterate on them, and deploy to GitHub Pages or Vercel for sharing. Use this skill when the user wants to create a mockup, prototype, UI exploration, or design comparison, or when they want to deploy or share one.'
---

# Mockup Prototype

End-to-end workflow for creating, iterating, and sharing interactive HTML mockups using Copilot CLI.

## When to Use This Skill

- User asks to "create a mockup" or "prototype a UI"
- User wants to compare design alternatives side by side
- User asks to "deploy" or "share" a mockup with colleagues
- User wants a quick visual exploration of a feature idea

## Phase 1: Generate

### Ask where this mockup belongs

Before creating the file, ask the user which repo to work in. The mockup file lives in the repo's local clone from the start - no copying later.

1. Ask: "Which repo should this mockup live in?" (e.g., `github/triage-agent`, `labudis/ideas`)
2. Find the local clone (check `~/GitHub/<org>/<repo>` or `~/GitHub/<repo>`)
3. Look for existing folder conventions: `docs/mockups/`, `considerations/`, `designs/`, `proposals/`. If none exist, use `docs/mockups/`.
4. Create the mockup at `<repo>/docs/mockups/<feature-name>/mockup.html`

### Create the mockup

Create a **single self-contained HTML file** with all CSS inline. No external dependencies, no build steps.

### Style guide

Match the visual style of the product being mocked up. If the user specifies a product or brand, replicate its look (colors, spacing, typography). If no specific product is mentioned, use a clean dark theme as a sensible default:

| Token | Value |
|-------|-------|
| Background (page) | `#0d1117` |
| Background (surface) | `#161b22` |
| Background (overlay) | `#21262d` |
| Text (primary) | `#e6edf3` |
| Text (secondary) | `#9198a1` |
| Text (muted) | `#7d8590` |
| Border | `#30363d` |
| Blue | `#4493f8` |
| Green | `#3fb950` |
| Red | `#f85149` |
| Yellow | `#d29922` |
| Purple | `#a371f7` |
| Font stack | `-apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif` |

Use inline SVGs for icons. Do not reference external icon libraries or CDNs.

### Comparing multiple options

When showing alternatives, use a tabbed layout:

```html
<!-- Sticky nav -->
<div class="option-nav">
  <button class="option-btn active" onclick="show('a')">A. Option name</button>
  <button class="option-btn" onclick="show('b')">B. Option name</button>
</div>

<!-- Each option in its own section -->
<div class="mockup-section active" id="section-a">
  <!-- mockup content -->
  <!-- pros/cons narrative INSIDE this div -->
</div>
<div class="mockup-section" id="section-b">
  <!-- mockup content -->
  <!-- pros/cons narrative INSIDE this div -->
</div>

<script>
function show(id) {
  document.querySelectorAll('.mockup-section').forEach(s => s.classList.remove('active'));
  document.querySelectorAll('.option-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('section-' + id).classList.add('active');
  event.target.classList.add('active');
}
</script>
```

Key rules:
- Narrative blocks (pros/cons) go **inside** each `.mockup-section`, not outside
- Only one section visible at a time via CSS (`display:none` / `display:block`)
- Use realistic data, not placeholder text

### Preview locally

After creating the file, always open it in the browser automatically:

```bash
open <repo-path>/docs/mockups/<feature-name>/mockup.html   # macOS
xdg-open <repo-path>/docs/mockups/<feature-name>/mockup.html  # Linux
```

## Phase 2: Iterate

All changes stay local. Do not push to the remote until the user explicitly asks to deploy or push.

1. Edit the HTML file based on user feedback
2. **Always re-open in browser after each change** so the user can see updates immediately
3. Common iteration patterns:
   - Adding/removing/reordering options
   - Adding pros/cons narrative below each option
   - Tweaking layout, spacing, colors
   - Fixing visual bugs reported via screenshots

**Important:** Do not `git commit`, `git push`, or create PRs during this phase. The user will tell you when they are ready.

## Phase 3: Deploy for sharing

Only start this phase when the user explicitly asks to deploy, push, or share.

### Confirm public visibility

Before deploying, remind the user:

> This will deploy the mockup to a **public URL**. Confirm the content is safe to share externally (see the Security section above).

If the user has not acknowledged this, ask for confirmation before proceeding.

### Choose a deployment target

Ask the user where to deploy:

- **GitHub Pages** (default): deploys via the repo's Pages site. Requires merging to main.
- **Vercel**: deploys instantly via `vercel deploy --prod`. No PR or merge required.

If the user has already stated a preference (e.g., "deploy to Vercel"), skip the prompt.

### Option A: GitHub Pages

1. **Ensure GitHub Pages is enabled** on the target repo:
   ```bash
   gh api repos/<owner>/<repo>/pages --jq '.html_url'
   # If not enabled:
   gh api repos/<owner>/<repo>/pages -X POST -f source='{"branch":"main","path":"/"}'
   ```

2. **Add a README.md** in the mockup directory with a summary of the states/options.

3. **Create branch, commit, push, PR, and merge** in one flow:
   ```bash
   git checkout -b <user>/mockup-<feature-name>
   git add docs/mockups/<feature-name>/
   git commit -m "Add <feature-name> mockup"
   git push origin <user>/mockup-<feature-name>
   gh pr create --title "<Feature> mockup" --body "..."
   # Wait for checks, then merge
   gh pr merge <number> --squash --delete-branch
   ```

   The merge to main is required for Pages to deploy. Do not leave the PR open.

4. **Open the live URL** in the browser after merge:
   ```bash
   PAGES_URL=$(gh api repos/<owner>/<repo>/pages --jq '.html_url')
   open "${PAGES_URL}docs/mockups/<feature-name>/mockup.html"
   ```

### Option B: Vercel

1. **Ensure the Vercel CLI is installed and authenticated:**
   ```bash
   vercel --version || npm install -g vercel
   vercel whoami  # confirm logged in
   ```

2. **Prepare the deploy directory.** Vercel serves `index.html` by default. Copy the mockup file so it works at the root URL:
   ```bash
   cp <repo-path>/docs/mockups/<feature-name>/mockup.html \
      <repo-path>/docs/mockups/<feature-name>/index.html
   ```

3. **Deploy from the mockup directory:**
   ```bash
   cd <repo-path>/docs/mockups/<feature-name>
   vercel deploy --prod --yes
   ```

4. **Clean up the temporary index.html** (keep `mockup.html` as the source of truth):
   ```bash
   rm <repo-path>/docs/mockups/<feature-name>/index.html
   ```

5. **Open the live URL** in the browser. Vercel prints the production URL and alias on deploy. Open the alias URL (e.g., `https://<project>.vercel.app`).

6. **Optionally commit and push** the mockup to the repo for project history. This is separate from the Vercel deploy and follows the same branch/PR/merge flow as GitHub Pages. Only do this if the user asks.

## Security

### Public visibility

Both GitHub Pages and Vercel deploy content to **publicly accessible URLs** by default. Before deploying, confirm the mockup does not contain:

- Real user data, PII, or production database content
- API keys, tokens, secrets, or credentials
- Internal-only URLs, hostnames, or infrastructure details
- Proprietary business logic or unreleased feature specifics that should stay confidential

### Content guidelines

- Use **synthetic, fictional data** in all mockups (fake usernames, placeholder repos, made-up org names)
- Do not embed real screenshots of internal tools unless cleared for public sharing
- Do not reference external CDNs, scripts, or stylesheets. All assets must be inline. This prevents supply-chain risks and ensures the file works offline.

### Credential hygiene

- The skill uses `gh` CLI and `vercel` CLI, which rely on locally stored auth tokens. These tokens are never written into mockup files.
- Do not hardcode tokens, passwords, or auth headers in any HTML, CSS, or JS within the mockup.

## Guidelines

- Single self-contained HTML file. No build tools, no npm, no frameworks.
- Save the mockup directly in the target repo's local clone from the start.
- Do not maintain two copies of the mockup (e.g., Desktop + repo). One file, one location.
- Do not push changes during iteration. Local only until the user says to deploy.
- Always auto-open the local file in browser during iteration.
- Always auto-open the live Pages URL after deploy.
- Use descriptive file and folder names (e.g., `sessions-sidebar`, not `mockup-1`).
