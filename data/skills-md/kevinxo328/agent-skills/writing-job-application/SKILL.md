---
name: writing-job-application
description: Write evidence-grounded cover letters, job-application answers, interview self-introductions, and recruiter responses from a user's resume. Use when the user asks to draft or revise these application materials for senior, lead, or management roles.
metadata:
  version: "1.4.0"
allowed-tools:
  - Read
  - Glob
  - Bash
---

# Job Application Writing

Write focused application materials for senior, lead, and management roles. Preserve the source of every factual claim while adapting the emphasis to the target role.

## Workflow

### 1. Establish the assignment

Identify the document type, target role, company, output language, job description, and any word, character, or speaking-time limit. Ask only for information that is missing and relevant to the selected document type. Accept that the user may have no personal connection to the company; use a direct, evidence-led opening in that case.

Read [references/formats.md](references/formats.md) after identifying the document type. The assignment is established when the applicable inputs in that reference are known or explicitly unavailable.

### 2. Select and read evidence

Use a resume or facts supplied in the current conversation first. A purely logistical recruiter response does not require a resume.

When factual candidate background is required and no resume is available, resolve the directory containing this `SKILL.md` as `SKILL_DIR` and keep the current working directory at the project root. If the environment gates access outside the working directory, obtain read access to the expanded absolute path of `$HOME/.agents/resumes` before running:

```bash
bash "$SKILL_DIR/scripts/scan-resumes.sh" "$PWD/resumes" "$HOME/.agents/resumes"
```

Check the exit status before handling `RESUME_COUNT`. On a permission error, obtain read access through the environment's permission flow and rerun the scan once. If access remains blocked, ask for an attached resume or another readable path. Only treat `RESUME_COUNT=0` as an empty result after a successful scan.

Handle the `RESUME_COUNT` result as follows:

- For one result, select and read it.
- For multiple results, show the paths and metadata, then ask which version to use.
- For zero results, ask the user to provide a path or attach a resume.

Ask for permission before copying a supplied resume into `~/.agents/resumes/`. After consent, preserve the filename, quote every path, and avoid overwriting an existing file.

For PDF resumes, run `python3 "$SKILL_DIR/scripts/read-pdf.py" RESUME_PATH`. The script tries `pypdf` first and `pdftotext` second. Treat a nonzero exit as a blocked read and ask for another readable format. Read Markdown resumes directly.

Build an internal evidence map for each candidate claim: what happened, where it happened, when it happened, and which supplied source supports it. This step is complete when every planned factual claim maps to the resume or an explicit user statement.

### 3. Draft the selected format

Follow the selected branch in [references/formats.md](references/formats.md). A user-provided length limit overrides every default in the reference.

Before drafting, privately generate three candidate voice hooks from the evidence map: an unusual concrete detail, a meaningful trade-off, and a defensible point of view about how the candidate works. Rank them by specificity, consequence, and evidence. Select the strongest hook. Generic themes such as passion, collaboration, or leadership earn space only when a particular event makes them distinctive.

Build the draft around a **voice hook**: one concrete detail, judgment, or earned point of view that makes this candidate memorable. Derive it from the evidence map rather than inventing a slogan. Pair the hook with a **tension**: the constraint, disagreement, failure, or trade-off that made the work difficult. Then show the candidate's choice and its verified result. The hook must reveal the candidate through a specific piece of work.

Choose an opening mode that puts information first: result-first, problem-first, or point-of-view-first. In the first two sentences, name the role or company only where it gives the hook useful context. Give the opening a concrete signal about the candidate's work.

Prefer one or two recent, role-relevant examples. Show decisions, constraints, trade-offs, team enablement, and business impact when the evidence supports them. Use verified metrics when available; otherwise describe verified scope or outcomes without manufacturing numbers. Let the prose sound like a capable person explaining how they work, with specific nouns and active verbs, rather than a summary of competencies.

Use **embedded fit**. Show the relationship to the company or role through the work being discussed: a product constraint, customer problem, operating choice, or business trade-off that the candidate has actually handled. Mention the company when it gives the example context. Make the reader infer why this candidate belongs in the conversation from the evidence.

Translate company research into one concrete implication for the job. Include a company fact when it explains why the example matters or identifies a problem the candidate can help handle. Use the job description's language when the evidence supports it, then prove the requirement through an action and result.

Do a voice pass before validation. Replace generic enthusiasm with a concrete observation, remove smooth transitions that merely announce a connection, and keep one slightly personal but defensible phrase if the evidence supports it. Give each paragraph a distinct job and use three-part lists only when the content genuinely calls for them.

Write in the language requested by the user. If none is requested, match the language of the application prompt or job description.

Drafting is complete when the selected format is fully written, every planned claim is evidence-backed, the opening has a concrete signal, and the draft contains one voice hook plus one tension-choice-result chain.

### 4. Validate and deliver

Verify all of the following:

- Every skill, metric, project, employer, and timeline maps to its actual source.
- The draft answers the selected prompt and respects its word, character, or speaking-time limit.
- The draft uses connected plain-text paragraphs, with normal sentence punctuation rather than Markdown, lists, tables, or em dashes.
- The opening is specific and evidence-led; interest appears through relevant choices and outcomes.
- The first two sentences contain a concrete result, problem, observation, or point of view.
- The draft has one identifiable voice hook and one clear tension, choice, and result, with paragraphs that serve the evidence rather than a competency inventory.
- Role or company relevance is embedded in the example and is legible from the evidence.
- Any company research or job-description language changes the context of the example and is supported by candidate evidence.
- The draft uses no more than two core examples and gives every tool or keyword business context.

Pass the exact candidate output to `python3 "$SKILL_DIR/scripts/check-format.py"` through standard input. Revise until it exits successfully.

Return only the finished application content by default so it can be pasted directly into the target field. Add rationale or revision notes only when the user asks for them. The work is complete when every validation item passes and the output contains only the requested artifact.

## Script contracts

- `scripts/scan-resumes.sh [local-directory] [global-directory]` prints a stable result count and resumes sorted by modification time, or exits nonzero when an existing directory cannot be scanned.
- `scripts/read-pdf.py PDF_PATH` prints extracted text to standard output and reports failures through a nonzero exit.
- `scripts/check-format.py [TEXT_FILE]` reads a UTF-8 file, or standard input when no file is provided, and rejects non-pasteable formatting.
