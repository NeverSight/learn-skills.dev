---
name: kami
description: |
  Document typesetting skill: resumes, one-pagers, white papers, letters, portfolios, and slide decks laid out on warm paper-like pages with serif type and ink-blue accents. Template and layout rules that produce print-ready output.
triggers:
  - "Kami document typesetting"
  - "Kami templates"
  - "typeset a resume"
  - "typeset a one-pager"
  - "white paper layout"
  - "paper-style slide deck"
das:
  type: skill
  category: presentations
  upstream: "https://github.com/tw93/Kami"
  version: latest
---

# kami

> Catalogue stub — full skill: [tw93/Kami](https://github.com/tw93/Kami)

<!-- das:install:start — generated from stub.yaml by `npm run generate`; edit stub.yaml, not this block -->
## Decision tree

1. **Is the full skill already installed?**
   - Global: `f=~/.agents/skills/kami/CHEATSHEET.md; [ -e "$f" ] && ! grep -qs "^das:" "$f" && echo "installed" || echo "pointer"`
   - Project: `f=.agents/skills/kami/CHEATSHEET.md; [ -e "$f" ] && ! grep -qs "^das:" "$f" && echo "installed" || echo "pointer"`
   - `installed` → invoke it and proceed
   - `pointer` → go to step 2

2. **Install** (the skills CLI cannot install this one):

   The repo is ~180 MB (fonts, site assets) and a plain `npx skills add tw93/Kami` clone takes minutes and can hit the CLI's 300 s clone timeout. Cloning only `skills/kami` (about 3 MB) takes seconds, then the skills CLI installs it from that local path.

   If an earlier attempt left `/tmp/kami-skill` behind, delete it first (`rm -rf /tmp/kami-skill`): `git clone` refuses a non-empty directory.

   ```bash
   [ -e ~/.agents/skills/kami ] && echo "global" || echo "project"
   ```

   **Global:**
   ```bash
   git clone --depth=1 --filter=blob:none --sparse https://github.com/tw93/Kami.git /tmp/kami-skill
   git -C /tmp/kami-skill sparse-checkout set skills/kami
   npx skills add /tmp/kami-skill/skills/kami -g -y
   ```

   **Project:**
   ```bash
   git clone --depth=1 --filter=blob:none --sparse https://github.com/tw93/Kami.git /tmp/kami-skill
   git -C /tmp/kami-skill sparse-checkout set skills/kami
   npx skills add /tmp/kami-skill/skills/kami -y
   ```

**Claude Code plugin route:**

```
/plugin marketplace add tw93/kami
/plugin install kami@kami
```

**Heads-up**

- **Requires:** Python 3 with WeasyPrint to build PDFs (python-pptx for editable PPTX); the commercial TsangerJinKai02 CJK font is not bundled
- **License:** MIT
<!-- das:install:end -->

## Invoke after install

- Skill name: `kami` (also available as the /kami command; the Claude Code plugin route namespaces it as /kami:kami)
- Trigger phrases: "Kami document typesetting", "Kami templates", "typeset a resume", "white paper layout"

## What it does

"Good content deserves good paper." Kami ships a set of templates and layout rules for documents that should look designed rather than generated: resumes, one-pagers, white papers, letters, portfolios, slide decks, and a landing-page template. Output is PDF, PNG, or editable PowerPoint. The workflow starts by locking a contract (language, template, output formats, page or length target, visual acceptance, verification command), then builds through scripts and verifies the output. English and Chinese have the most complete support; Japanese and Korean use language-specific font fallbacks. An optional brand profile can override defaults.

## When NOT to use

- Auditing or restyling an existing product site or app UI → use `hallmark` or `impeccable`
- Interactive, animated HTML slide decks → use `frontend-slides` or `html-ppt`
- Markdown-driven developer decks → use `slidev-skill` or `marp-slides`
- AI-generated slide imagery from a document → use `nanobanan-ppt`
