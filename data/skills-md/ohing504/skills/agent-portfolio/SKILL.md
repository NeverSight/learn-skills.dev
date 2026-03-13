---
name: agent-portfolio
description: Generate a personalized portfolio site from agent-reference reports and deploy it to GitHub Pages. The site reflects the user's working style as observed by their AI collaborators — AI analyzes the reports, proposes a design concept, scaffolds an Astro site with concept-based theming, and deploys to {username}.github.io. Use this skill whenever the user asks to "build my portfolio", "create portfolio site", "make a site from my reports", "deploy to github pages", "github.io site", or says things like "포트폴리오 사이트 만들어줘", "사이트 배포해줘", or wants to turn agent-reference reports into a live website. Also triggers when the user has agent-reference reports ready and wants to publish them as a site, wants a personal site generated from AI collaboration data, or asks to update/redeploy an existing agent portfolio. Do NOT use for general Astro development, generic website building, agent-reference analysis without site generation, or resume writing that does not involve deploying a site.
---

# Agent Portfolio — Introduced by My Agents

You are generating a personalized portfolio site from agent-reference reports. The site reflects the user's working style as observed by their AI collaborators — not a generic developer template, but a site shaped by real collaboration data. Each portfolio is different because each person's reports are different.

The result is an Astro site deployed to GitHub Pages at `{username}.github.io`, with sections for agent reviews, project highlights, work style visualization, and GitHub activity.

## How This Skill Works

| Step | What happens |
|------|-------------|
| 1. Collect Inputs | Gather agent-reference reports, resume, GitHub data |
| 2. Analyze & Propose Concept | Read reports, identify traits, propose design concept |
| 3. Scaffold Site | Create Astro project with concept-based theme |
| 4. Customize & Review | User reviews, agent adjusts |
| 5. Deploy | Push to GitHub, enable Pages, go live |

Most users will have already run the `agent-reference` skill to generate reports. If not, suggest running that skill first.

---

## Step 1: Collect Inputs

This step gathers all data needed to generate the portfolio. Guide the user through each input:

**1. Agent-reference reports (required)**
- Ask the user where their report files are
- Expected structure: markdown files from agent-reference Phase 1 and optionally Phase 2
- If no reports exist, suggest running the `agent-reference` skill first and stop here

**2. Resume / self-introduction (optional)**
- Ask if they have a resume, CV, or self-intro to include
- This populates the "About" and "Career" sections
- Any format (markdown, PDF text, plain text)
- **PDF handling:** Read PDF files directly using your file reading tool (e.g., Claude Code's Read tool supports PDF natively) — do NOT use external conversion tools like `pdftoppm` or `pdftotext`, which lose structure and ordering. Even with direct reading, multi-column layouts, tables, and Korean text can be misinterpreted. Always verify the extracted content with the user — career order, company-project mapping, and tech stacks are commonly garbled. Markdown format is most reliable.
- **PII warning:** Resumes often contain phone numbers, email addresses, and home addresses. These must NOT appear on the public site. Extract only career/education/skills content. If the user wants a contact method on the site, suggest a contact form or LinkedIn link instead of raw PII.

**3. GitHub data (optional)**
- Check `gh auth status` to see if gh CLI is available
- If available, offer to pull: contribution calendar, repo list, language stats
- Reference: `gh api graphql` for contribution data, `gh repo list` for repos

**4. Existing portfolio materials (optional)**
- Any existing site content, project descriptions, or images to incorporate

### Set Up the Repository

After collecting inputs, help the user create the portfolio repo:

**1. Private source + public deploy (Recommended)**
```bash
gh repo create {username}/portfolio --private --clone
cd portfolio
gh repo create {username}/{username}.github.io --public
```
- The `{username}.github.io` name is a GitHub Pages convention and **must not be changed**. The private source repo name (e.g., `portfolio`) can be anything.
- Two repos: `portfolio` (private) for source/reports, `{username}.github.io` (public) for deployed site
- Reports stay private, clean URL: `https://{username}.github.io`
- GitHub Actions builds in `portfolio` and pushes to `{username}.github.io`
- User controls which reports appear on the Raw Data page

**2. Single public repo (Simple)**
```bash
gh repo create {username}/{username}.github.io --public --clone
cd {username}.github.io
```
- One repo for everything — simplest setup
- All reports visible in git history
- Fine if user has no private content

### Organize Reports

Copy reports into the repo:
```
reports/
├── {date}-{agent-name}/
│   ├── user-profile.md
│   ├── project-{name}.md
│   └── ...
└── aggregated/          (if Phase 2 was run)
    ├── aggregated-profile.md
    ├── references-multi-perspective.md
    ├── introduced-by-agents.md
    ├── faq.md
    └── blog-topics.md
```

If the user provides a resume, profile photo, or screenshots, save them to `materials/`. Any filename and format works (`resume.pdf`, `이력서.pdf`, `cv.md`, etc.).

### Portfolio Repo Structure

After setup, your repo should look like this:

```
portfolio/
├── reports/                    # Agent-reference reports (required)
│   ├── 2026-03-claude-code/
│   │   ├── user-profile.md
│   │   └── project-*.md
│   └── aggregated/             # Phase 2 outputs (if available)
│       ├── aggregated-profile.md
│       ├── references-multi-perspective.md
│       ├── faq.md
│       └── blog-topics.md
├── materials/                  # User-provided materials (optional)
│   ├── resume.pdf              # Resume/CV (any format and filename)
│   └── profile.jpg             # Profile photo, screenshots
└── README.md                   # Will be auto-generated
```

The skill will generate the `src/`, `public/`, and config files in the next steps. You only need to provide the data above.

---

## Step 2: Analyze & Propose Concept

Read `references/concept-generation-guide.md` for the full concept generation workflow.

### What You Do

1. **Read all reports** in the `reports/` directory — user profiles, project reports, aggregated outputs
2. **Identify dominant traits** — work style signals, communication patterns, technical identity
3. **Map to a design concept** — each concept has a color palette, typography, and layout direction
4. **Present the concept** to the user for approval

### Available Concepts

| Concept | Best for | Visual direction |
|---------|----------|-----------------|
| Blueprint | Methodical architects | Cool blues, monospace headers, structured grid |
| Launchpad | Fast iterators, many projects | Vibrant warm colors, bold sans, project gallery |
| Chronicle | Deep domain experts | Earth tones, serif, editorial case studies |
| Spectrum | Full-stack generalists | Gradient accents, balanced sections |
| Terminal | CLI/infra builders | Dark theme, green accents, monospace |
| Canvas | Creative/design-aware | Soft pastels, asymmetric layout |

The concept affects visual styling only — all sections are available regardless of concept.

**Always get user approval before proceeding.** Show the proposed color palette, fonts, and section order. Offer to adjust or try a different concept.

---

## Step 3: Scaffold Site

Read `references/site-structure-guide.md` for complete component specifications.

### Initialize Astro

```bash
npm create astro@latest -- --template minimal --no-install
npm install
npm install tailwindcss @tailwindcss/vite
```

> **Warning:** Do NOT use `npx astro add tailwind` — it installs `@astrojs/tailwind` (Tailwind 3 integration) which conflicts with Tailwind 4. Install `@tailwindcss/vite` directly instead.

### Optional: Enhanced Design Quality

If the `frontend-design` skill is available in the current environment, invoke it during component implementation for production-grade styling and modern design patterns. This produces more polished, distinctive results — avoiding generic AI aesthetics.

- **Available:** Invoke `frontend-design` after concept approval, before generating components. Let it guide component styling, layout composition, and interaction design alongside the concept theme.
- **Not available:** The built-in concept themes and site-structure-guide provide a complete design system. The site will still look good.

This is an optional enhancement, not a dependency. The skill is never required to run agent-portfolio.

### Generate Components

Based on the approved concept and available data, generate these components:

| Component | Data source | Required |
|-----------|------------|----------|
| Hero.astro | aggregated profile or first user-profile report | Yes |
| About.astro | materials/resume (any format) | Only if resume provided. Two-column: main content (left) + Career preview & Education sidebar (right) |
| AgentReviews.astro | user-profile reports (persona sections) | Yes |
| Projects.astro | project-*.md reports | Yes |
| WorkStyle.astro | analysis dimensions from profiles | Yes |
| GitHub link | Hero or Footer | No — just a profile link, not a stats component. GitHub stats are already on the user's profile. |
| FAQ.astro | faq.md from aggregated outputs | Only if available |
| BlogTopics.astro | blog-topics.md from aggregated outputs | Only if available |
| RawData.astro | report files user chose to make public | Optional |
| Footer.astro | auto-generated | Yes |

### Apply Concept Theme

Configure concept-specific design tokens. Tailwind 4 supports both CSS-based configuration (using `@theme` in your CSS) and the traditional `tailwind.config.mjs`. Either approach works — see `site-structure-guide.md` for details. Import Google Fonts in `Layout.astro`.

### Process Report Data

Create `src/lib/parse-reports.ts` to transform raw markdown reports into structured data for components. See site-structure-guide.md for the parsing functions specification.

---

## Step 4: Customize & Review

### Preview Locally

```bash
npm run dev
```

Open `http://localhost:4321` and walk through the site with the user.

### Review Checklist

Go through each section with the user:

- [ ] **Hero** — Does the summary line capture who they are?
- [ ] **Agent Reviews** — Are the persona voices distinct and accurate?
- [ ] **Projects** — Are the right projects highlighted? Any to add/remove?
- [ ] **Work Style** — Does the visualization feel accurate?
- [ ] **Overall feel** — Does the concept match their identity?

### Pre-deployment Privacy Check

**Before deploying, review the site content for sensitive information.** The reports were written for the user's reference — not all content is safe to publish. Walk through this checklist with the user:

- [ ] **PII** — No phone numbers, email addresses, or home addresses on the site (check resume-derived content especially)
- [ ] **Private repo details** — Reports for private/employer projects should match their assigned privacy level (Full/Private/Stats-only). Check that private projects don't leak identifying details (specific domain names, internal URLs, unique tech combinations)
- [ ] **Business metrics** — No exact user counts, MAU, revenue, or cost figures from private projects (use qualitative descriptions)
- [ ] **Security details** — No RLS function names, auth implementation patterns, SECURITY DEFINER details, or error filtering rules from production services
- [ ] **Employer internal systems** — No internal tool names, infrastructure architecture, or vendor integrations that could violate NDA or expose attack surface
- [ ] **Materials** — Resume PDF is NOT served as a static file (extract content only, don't copy the file to `public/`)

### Adjust

Based on feedback:
- **Content changes** — update report excerpts, rewrite summaries
- **Design changes** — adjust colors, fonts, section order in Tailwind config
- **Section changes** — add/remove optional sections
- **Concept change** — if the whole direction feels wrong, go back to Step 2

Iterate until the user approves the site.

---

## Step 5: Deploy

Read the deployment guide matching the user's chosen option:
- Option 1 (private source + public deploy): `references/deployment-private.md`
- Option 2 (single public repo): `references/deployment-public.md`

### Quick Deploy

For Option 1 (private source + public deploy), set up the deploy key first (see `references/deployment-private.md`), then:

```bash
git add -A
git commit -m "Initial portfolio site — Introduced by My Agents"
git push -u origin main
```

GitHub Actions builds in `portfolio` and pushes to `{username}.github.io`. The site will be live at `https://{username}.github.io`.

### Verify

- Check the Actions tab in the source repo for build status
- Visit `https://{username}.github.io` once deployment completes
- Test on mobile (responsive check)

### GitHub Profile README (Optional)

If the user wants, generate a minimal GitHub Profile README that links to the portfolio. See the deployment guides for the template.

---

## Updating the Site

When you have new reports (new projects, new machine, new agent):

1. Run `agent-reference` skill again → new report files
2. Copy new reports to `reports/` in the portfolio repo
3. Run this skill again or just `npm run build` to regenerate
4. Push → GitHub Actions rebuilds automatically

The site's footer shows "Last updated: {date}" so visitors know how current the data is.

---

## Important Principles

**The site tells the user's story through agent eyes.** Every section should trace back to real observations from agent-reference reports. Don't pad with generic content.

**Concept serves content.** The design concept amplifies what the reports reveal — it doesn't impose a personality that isn't there.

**User controls everything.** Which reports to include, which sections to show, what to make public. The agent proposes; the user decides.
