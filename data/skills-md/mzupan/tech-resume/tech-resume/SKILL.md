---
name: tech-resume
description: Write tailored tech resumes and cover letters aimed at engineering hiring managers, built to parse cleanly in ATS and AI screeners (Greenhouse, Lever, Ashby, Workday) and to read as written by a person, not AI. Interviews the user to build a reusable career profile, asks targeted gap questions per job description, then produces DOCX + PDF. Use when the user wants a resume or cover letter for a job, wants to tailor to a JD, improve or review a resume, build a career/brag profile, or change their target level.
metadata:
  version: "1.0.0"
---

# Tech resume and cover letter

Produce resumes and cover letters for tech roles that (1) parse cleanly for ATS and LLM screeners, (2) persuade an engineering hiring manager in a 7-second skim and a 2-minute read, and (3) do not read as AI-written.

Three rules override everything else in this skill:

1. **Never invent facts.** Every number, scope, title, date, tool, and outcome must come from the user or their documents. If a bullet needs a number you don't have, ask. If the user doesn't know, use an honest range they confirm ("~40%", "8-10 teams") or a non-numeric result. Do not add a JD skill the user hasn't confirmed they have.
2. **No hidden or deceptive content.** No white text, tiny fonts, off-page text, zero-width characters, or prompt-injection text. Screeners now detect these and recruiters treat them as fraud.
3. **Write like the person.** Run the human-voice pass ([references/human-voice.md](references/human-voice.md)) on every resume and letter before building files. This is where the humanizer and unslop skills are applied.

## Agent compatibility

Use this same skill with Claude Code, Codex, IBM Bob, GitHub Copilot, Gemini CLI, or OpenCode. Installation locations and invocation examples are in [README.md](README.md).

Resolve `SKILL_DIR` to the absolute directory containing this loaded `SKILL.md`; set it in the shell before running the commands below. Scripts, references, and templates are relative to that directory. Keep the current directory set to the user's career workspace so generated files go there. Do not assume the skill is installed under `~/.claude`.

Use the agent's available question tool or a plain-text question for the choices below. For image-only PDFs, use an available PDF or image viewer; if none is available, ask for a text export. Optional humanizer and unslop skills improve the writing pass but are not required.

## Workspace

Data lives in the user's working directory, not in this skill:

```
<workspace>/
  profile/career-profile.md     # master profile: every role, fact, metric, story (from templates/career-profile.md)
  profile/sources/              # old resumes, LinkedIn PDF export, brag docs, perf reviews the user drops in
  profile/voice/                # writing samples the user actually wrote (emails, posts, docs) for cover-letter voice
  profile/bases/bases.md        # index of base resumes (name, source file, current role, history notes)
  profile/bases/<name>/resume.md  # cleaned, ATS-formatted generic resume; one per base
  applications/YYYY-MM-DD-company-role/
    jd.md  keywords.txt  gaps.md  resume.md  cover-letter.md  report.md
    First-Last-Resume-Company.docx/.pdf  First-Last-Cover-Letter-Company.docx/.pdf
```

Workspace = current directory if `profile/career-profile.md` exists there; otherwise ask the user where it lives or offer to create it in the current directory.

## Routing

| Invocation | Do |
|---|---|
| `tech-resume` (no args; agent-specific invocation) | If no profile: explain the flow, ask whether they have an existing resume or LinkedIn PDF to start from (`init`), otherwise start `profile`. If profile exists: show target level, profile completeness (roles with < 2 quantified facts), recent applications; ask what's next. |
| `init <file...>` | Seed a new profile from existing resumes (PDF, DOCX, TXT, MD) and/or a LinkedIn PDF export. See "init" below. |
| `profile` | Build or extend the master profile. Read [references/interview.md](references/interview.md). |
| `base` | List base resumes from `profile/bases/bases.md`. `base new <file>` seeds another base from a resume file (see "Base resumes"). `base show <name>` builds and shows that base's PDF. `base tune <name>` runs `scripts/keyword_trends.py` over the saved applications, shows the recurring JD terms that base doesn't prove in a bullet, asks which ones the user can back up (and with what fact), adds those facts to the profile, and updates the base. Never add a term the user can't back up. |
| `target` | Show the current target. `target <level...>` changes it. Read [references/levels.md](references/levels.md). |
| `apply <JD>` | Gap questions, then resume and cover letter. Default when the user just pastes a JD or URL. |
| `resume <JD>` | Gap questions, then resume only. |
| `cover <JD>` | Cover letter only (uses this JD's resume if it exists). Read [references/cover-letter.md](references/cover-letter.md). |
| `review <file> [JD]` | Critique an existing resume/letter: run `scripts/lint.py`, `scripts/verify.py` (if PDF/DOCX), check against the rules, and list fixes ranked by impact. Then offer to ask the questions that would fix the weak bullets. |

A JD can be pasted text, a file, or a URL (fetch it; if the page is JS-rendered and fetch returns nothing, ask the user to paste it).

## Writing rules

The profile frontmatter can hold `writing_rules`: standing instructions from the user that override this skill's defaults in every resume, letter, and base (e.g. `no-years-of-experience`: never state experience as a span of years). Read them before drafting. `scripts/lint.py` enforces the ones it knows as HARD hits. When the user gives a new standing instruction ("never…", "always…"), add it to `writing_rules` and apply it to every existing base and open application.

## Target level

The target level is stored in the profile frontmatter (`target_levels`, `target_roles`). If it's empty when any writing command runs, ask before writing (allow multiple selections): Entry level / new grad / intern, Senior IC, Staff/Principal IC, Engineering Manager, Director, VP/Head of Engineering/CTO, Architect/Platform/DevOps/SRE, plus "other". Also ask the target role titles they want to be seen as. A JD that clearly sits at a different level than the target: point it out and ask which level to write for this application (don't silently change the stored target).

## `init` workflow

Also runs when the user hands over a resume file with no other instruction, or when `profile` starts and `profile/sources/` has files not yet harvested.

1. Create `profile/` and `profile/sources/` in the workspace if missing; copy each given file into `profile/sources/` (keep the original name).
2. Extract text: `python3 "$SKILL_DIR/scripts/extract.py" "profile/sources/<file>" --out "profile/sources/<file>.txt"`. It flattens DOCX tables, recovers Word header/footer and text-box content, fixes ligatures, and warns on image-only or multi-column PDFs. For an image-only PDF, read it visually with an available viewer. For `.doc`, ask for DOCX/PDF.
3. Tell the user what the parse report says about their old file (header contact info, tables, columns, ligatures, missing text layer). Those same problems are likely costing them in ATS today, so this is useful feedback.
4. Fill `profile/career-profile.md` from `templates/career-profile.md`: contact, every role with title/dates/company/location, each bullet split into facts tagged `(source: old resume; confidence: as written)`, education, certifications, skills (depth unknown until asked). Several sources (resume + LinkedIn) get merged; list conflicts in dates or titles under "Gaps or things to explain" and ask about them.
5. Ask for target level and roles if they're unset (see "Target level").
6. Run the profile completeness check from [references/interview.md](references/interview.md), show the weakest roles, and offer to start the interview there. Existing bullets are raw material: ask for the scale, baseline, and ownership behind them rather than reusing their wording.

## Base resumes

A base is a cleaned, generic resume the user can start applications from. Users may keep several (different emphasis, or different ways of presenting a complicated history). Each base's employers, titles, and dates are authoritative for that base: tailoring changes wording, order, and selection, never the history, and never pulls a role from one base into another.

- **Creating a base.** `init` with a second resume file, or `base new <file>`: extract it, add any new roles and facts to the profile (tag which base each role appears in), then write `profile/bases/<name>/resume.md` from `templates/resume.md`. Apply every correction already recorded in the profile (corrected or retracted claims, updated contact info, excluded projects, newer facts for shared roles) so the new base starts at the same quality as the others. Run the human-voice pass, build, verify, and add a row to `bases.md`. Ask the user for a short name if the file name doesn't suggest one.
- **Timeline differences.** If bases disagree on employers or dates, tell the user once that recruiters and background checks compare versions. If the user says to keep them, record that decision in `bases.md` and don't raise it again.
- **Corrections propagate.** When the user corrects or adds a fact for a role that appears in several bases, update every base that contains the role and rebuild them.

## `apply` / `resume` workflow

0. **Pick a base.** If `profile/bases/bases.md` lists more than one base, ask which to use (one option per base, with its current role and source in the description). Record the choice in `report.md`.
1. **Load.** Read the chosen base, the profile, and [references/resume-rules.md](references/resume-rules.md) and [references/levels.md](references/levels.md) (current level only). Create the application folder; save the JD to `jd.md`.
2. **Analyze the JD.** Extract: exact role title; level signals; must-haves vs nice-to-haves; the 3-5 problems this hire is meant to solve (read between the lines: team stage, scale, what's broken); exact keyword spellings including acronym forms. Write `keywords.txt` in the format `scripts/verify.py` documents (`must:` / `nice:`, alternates after `|`). Use the JD's spelling as the first term.
3. **Map evidence.** For each must-have, find profile facts that prove it. Classify: strong (quantified, recent), weak (mentioned, no scale/result), missing.
4. **Gap questions.** Ask only about weak and missing items plus anything the cover letter needs (why this company, referral, a concrete detail about their product). 3-8 questions, batched in one or two question-tool rounds or one plain-text list, never one long interrogation. Use the JD-gap bank in [references/interview.md](references/interview.md). Always include: "Anything in this JD you can't honestly claim, so we leave it out?" Save Q&A to `gaps.md` and fold new facts back into the profile (ask once per session whether to do that automatically).
5. **Draft `resume.md`** starting from the chosen base, following the rules: summary of 3-4 sentences at the top tuned to the JD, reverse-chronological experience, education, skills at the bottom matched to the JD. Select and reorder facts for this JD; don't paste the whole profile. Stay inside the length budget in [references/resume-rules.md](references/resume-rules.md): 475-750 words, 3-5 bullets for each of the two most recent roles and 1-3 for older ones, strongest bullet first, result or metric in the first 5-8 words. Add the one-line company context for lesser-known employers and an optional `- Stack:` line for the two most recent roles.
6. **Human-voice pass.** Follow [references/human-voice.md](references/human-voice.md): `scripts/lint.py`, then the humanizer and unslop passes, then lint again until 0 HARD.
7. **Build and verify.**
   ```bash
   python3 "$SKILL_DIR/scripts/build.py" resume.md --out-dir . --basename First-Last-Resume-Company
   python3 "$SKILL_DIR/scripts/verify.py" --source resume.md --pdf First-Last-Resume-Company.pdf --docx First-Last-Resume-Company.docx --keywords keywords.txt --max-pages 2
   ```
   Fix every FAIL. For WARNs: missing must-haves either get evidence (ask the user) or are left out deliberately and noted; "only in Skills" terms get a supporting bullet or go on the role's `Stack:` line if the user has the experience. Page count or word count over budget: cut the oldest and weakest bullets first. `build.py` also prints a WARN for each widow line (a bullet whose last line holds only one or two words): trim a few words or add a detail until it's gone. Render page 1 to PNG (`pdftoppm -png -r 70 -f 1 -l 1`) and look at it once.
8. **Report.** Write `report.md` and tell the user: files made, must-have coverage, what was left out on purpose and why, remaining WARNs, and the 2-3 facts that would most improve this resume if they can find them.

## `cover` workflow

Read [references/cover-letter.md](references/cover-letter.md). Uses the same JD analysis, `gaps.md`, and the user's voice samples. Draft `cover-letter.md` from `templates/cover-letter.md`, run the human-voice pass with `--type cover`, then:

```bash
python3 "$SKILL_DIR/scripts/build.py" cover-letter.md --type cover --out-dir . --basename First-Last-Cover-Letter-Company
python3 "$SKILL_DIR/scripts/verify.py" --type cover --source cover-letter.md --pdf First-Last-Cover-Letter-Company.pdf --docx First-Last-Cover-Letter-Company.docx
```

Also give the letter as plain text in the reply, since many portals take it in a text box and direct-to-hiring-manager emails go in the email body.

## Scripts

| Script | Purpose |
|---|---|
| `scripts/extract.py` | Existing resume (PDF/DOCX/TXT/MD) to plain text plus a parse report (contact found, dates, header/table/column/ligature/image-only warnings). |
| `scripts/build.py` | Markdown source to DOCX + PDF. Single column, embedded Arial, no ligatures, contact info in body, dates right-aligned by tab stop, company names bold. Warns on widow lines in bullets. `--font Arial\|Georgia\|Calibri`, `--size 10-11.5`. |
| `scripts/verify.py` | Parse test: text layer, name first, email/phone, header/footer, hidden text, odd unicode, headings, date format, fonts, size, page count, word budget, keyword coverage by section. Exit 1 on FAIL. |
| `scripts/keyword_trends.py` | Ranks JD keywords that recur across `applications/*/keywords.txt` and shows whether a base resume proves each one in a bullet, only in Skills, or not at all. Used by `base tune`. |
| `scripts/lint.py` | AI-tell and generic-writing scanner for resumes and letters, plus resume shape: bullets per role, word budget, pronouns in bullets, context-clause, bystander ("Assisted", "Helped"), and -ing activity openers, overused team words. Merges unslop's scanner hits. Exit 1 on any HARD. |

Requires `python-docx`, `reportlab`, `pypdf`; `pdftotext`/`pdftoppm` (poppler) recommended. If a dependency is missing, tell the user the install command (`pip install python-docx reportlab pypdf`, `brew install poppler`) rather than switching to a different generator.

## References

| File | Read when |
|---|---|
| [references/interview.md](references/interview.md) | `profile`, and gap questions in `apply`/`resume`/`cover` |
| [references/resume-rules.md](references/resume-rules.md) | Writing or reviewing any resume |
| [references/levels.md](references/levels.md) | `target`, and the section for the current level when writing |
| [references/cover-letter.md](references/cover-letter.md) | Writing or reviewing a cover letter |
| [references/human-voice.md](references/human-voice.md) | Every draft, before building files |
| [references/research.md](references/research.md) | When the user asks why a rule exists; evidence and sources |
