---
name: interview-guide-generator
description: Generates structured, role-calibrated interview guides for hiring across engineering levels. Use when preparing to interview a candidate for a specific role and context.
---

# Overview
This skill generates a tailored, structured interview guide for a specific technical role and hiring context.

It anchors every question to the competency framework for that level, incorporates project-specific technical requirements when provided, and produces a guide that any interviewer on the team can pick up and run with consistently.

The goal is to remove subjectivity from the interview process, ensure signal collection is calibrated to what actually matters at that level, and make the hiring bar consistent across directors and leads.

---

# When to Use This Skill
- Opening a new position and preparing the interview loop.
- Hiring for a project with specific technical, domain, or client requirements.
- Calibrating a hiring panel that includes people who don't interview frequently.
- Creating a repeatable guide for a role you hire for often (e.g., Senior UI Engineer).
- Refreshing an outdated interview process for an existing role.

# When NOT to Use This Skill
- For contractor or vendor evaluation (use a scoping/fit conversation instead).
- For internal transfers or promotions (use a growth roadmap or a calibration conversation).
- For roles outside the Technology/ software engineering craft without adapting the competency anchor.

---

# Company Context

Look for the company information in the files `shared/company.md`

---

# Workflow

Follow these steps in order every time this skill is invoked.

## Step 1 — Extract Role and Level
Identify the role and level from the user's prompt. Normalize to a standard label:
- Examples: `Senior frontend engineer`, `junior QA analyst`
- **If no role is provided**: Do not assume. Ask the user to specify the role before continuing.
- **If no level is provided**: Do not assume. Ask the user to specify the level (e.g., Junior, Mid, Senior, Staff) before continuing.
- **If the level is ambiguous** (e.g., user says "developer"): Ask for clarification before continuing.

> Role and level are required inputs. Never proceed to Step 2 without both confirmed.

## Step 2 — Load Role Competencies
Look for a competency file for the confirmed role. Use the following lookup order:

1. **`shared/competencies/<role-slug>.md`** — default location, Markdown format.
2. **Any file the user has already provided or referenced** in their prompt (e.g., a path, a pasted document, or an attached file such as a PDF or CSV).
3. **Any file in the current working context** that matches the role name or slug, regardless of format or location.

Accepted formats: `.md`, `.pdf`, `.csv`, plain text paste.

- **If found**: Load the competency data. This defines the expected behaviors and skills at that level and anchors every section of the interview guide.
- **If not found**: Do not assume or invent competencies. Ask the user:
  > "I couldn't find a competency framework for this role. You can:
  > - Point me to a file (any format — Markdown, PDF, CSV)
  > - Paste the competencies directly
  > - Say **'proceed'** and I'll use general expectations for this level and seniority"

  Wait for their response before continuing.

## Step 3 — Review Candidate Background (Optional)
Check whether the user has provided any candidate context. This step is optional — if nothing is provided, skip it and continue.

Accepted inputs:
- **CV or résumé** — any format (PDF, Word, plain text paste)
- **LinkedIn profile URL** — fetch and extract publicly available information
- **A brief summary** — written by the hiring manager or recruiter

If candidate context is available, extract and note:
- **Relevant experience** — years in similar roles, industries, company types (agency, startup, enterprise). Note if their background matches or diverges from the hiring context.
- **Technical signals** — technologies, tools, and domains they've worked in. Flag gaps relative to what the role requires.
- **Career trajectory** — progression pattern, lateral moves, tenure. Note anything that warrants probing (e.g., short stints, significant level jumps, career pivots).
- **Potential strengths to validate** — experience claims that are impressive but vague, and worth making concrete in the interview.
- **Potential gaps to probe** — areas the role requires that are absent or thin in their background.

Use this to personalize questions in Step 5 — reference specific experiences from the candidate's background, probe gaps directly, and avoid asking about things they've clearly done extensively.

> If no candidate context is provided, the guide will be generalized for the role and level. That's fine — the guide is still useful for the full interview loop.

## Step 4 — Analyze the Prompt
Review everything the user provided. Extract and categorize:

**Role signals**
- Confirmed level and track (IC vs. lead vs. director).
- Any seniority nuances mentioned (e.g., "leaning toward the senior end of M3").

**Project or context signals**
- Specific client industry or domain (e.g., financial services, healthcare, e-commerce).
- Required technologies, frameworks, languages, platforms, or certifications.
- Team composition context (e.g., "this person will be the only FE on the project").
- Timeline pressure or delivery complexity.

**People and culture signals**
- Any team dynamics mentioned (e.g., "we need someone who can mentor a junior").
- Client-facing expectations.
- Any red flags or must-avoids mentioned.

**Gaps**
- Note which competency areas the prompt does not address. These will inform clarifying questions.

## Step 5 — Ask Clarifying Questions
Ask **2–3 targeted questions** to fill the most important gaps from Step 4.
Prioritize questions that would meaningfully change the questions generated.

**Always include this option at the end:**
> "Or, if you prefer, just say **'generate'** and I'll build the guide with what I have."

Good questions to consider (adapt to the situation):
- Who else will be in the interview loop, and what will they cover? (Avoids duplication.)
- Is this a net-new role or a backfill? (Backfills may signal a specific gap to probe.)
- Will this person be client-facing, and if so, how much? (Shapes consulting/influence questions.)
- Are there any non-negotiables — skills or behaviors that would immediately disqualify a candidate?
- What does the onboarding timeline look like? (A person joining a live project in two weeks needs a different profile than someone ramping over three months.)

Wait for the user's answers before proceeding. If the user says "generate" at any point,
skip directly to Step 6.

## Step 6 — Generate the Interview Guide
Using all collected information, produce the interview guide following the
Framework and Output Format sections below.

Once the guide is complete, export it as a **PDF file** and share it with the user.
Name the file using the pattern: `interview-guide-[role-slug]-[YYYY-MM-DD].pdf`
(e.g., `interview-guide-senior-ui-engineer-2025-03-15.pdf`).

---

# Interview Question Framework

Questions must collect signal across four dimensions. Every generated guide should
balance coverage across all four, weighted by what matters most for the specific role and level.

## Dimension 1 — Technical Knowledge
Questions that assess depth and quality of technical knowledge. Anchored to the
"Technical Skills" section of the competency table. Include any project-specific technologies from the prompt.

Signal to collect:
- Depth of expertise in core technical areas for this role.
- Approach to code quality, testing, and performance.
- Ability to make and articulate architecture decisions.
- Awareness of trade-offs, not just solutions.
- Fluency with AI-assisted development — how they use tools like GitHub Copilot, Cursor, or Claude in their workflow, and critically, how they validate, review, and take ownership of AI-generated output. At senior levels, look for judgment about when AI assistance helps vs. when it introduces risk.

## Dimension 2 — Delivery & Process
Questions that assess how the candidate manages work, ambiguity, and complexity.
Anchored to the "Delivery" competency. Especially important in an agency context.

Signal to collect:
- How they scope, estimate, and manage risk.
- How they handle competing priorities or unclear requirements.
- Their relationship with process (Agile, CI/CD, documentation).
- How they communicate progress and problems to the team and stakeholders.

## Dimension 3 — Collaboration & Communication
Questions that assess how the candidate works with others — teammates, cross-functional partners, and clients. Anchored to "Builds Together" and "Influence" competencies.

Calibrate questions to the role's track and level:

**Individual contributors**
Signal to collect:
- How they navigate disagreement or misalignment within a team.
- Whether they elevate others or work in isolation.
- How they communicate technical concepts to non-technical audiences.
- Their approach to feedback — giving and receiving.

**Leads and Staff engineers**
Signal to collect:
- How they drive alignment across teams or workstreams without formal authority.
- How they sponsor or unblock others' work, not just their own.
- Their approach to technical decision-making in group settings (e.g., RFCs, design reviews).
- How they handle conflict between technical quality and business pressure.

**Directors and people managers**
Signal to collect:
- How they build, develop, and retain a team — not just manage output.
- How they give difficult feedback and handle underperformance.
- How they represent their team's needs upward and advocate for resources.
- Their approach to hiring and what they look for in candidates.
- How they balance hands-on involvement with delegation.

## Dimension 4 — Growth Mindset & Ownership
Questions that assess accountability, curiosity, and initiative. This dimension is a strong predictor of long-term fit and cultural alignment — weight it accordingly, especially when the environment is fast-moving or ambiguous.

Signal to collect:

**Accountability**
- Can they describe a specific failure — what happened, what they did, and what changed as a result? Watch for deflection, blame-shifting, or overly polished answers with no real consequence.
- Do they distinguish between effort and outcome? Ownership means caring about the result, not just the work.

**Curiosity and learning**
- How do they actively keep up with a fast-moving field — not just "I read blogs" but specific examples of how learning has changed how they work.
- Have they taught themselves something outside their job description? Proactively adopted a new tool, method, or practice without being asked?
- How are they adapting to AI-augmented development — are they experimenting, ignoring it, or thoughtfully integrating it?

**Initiative and proactiveness**
- Can they give an example of improving something that wasn't their responsibility? Raising a problem, proposing a solution, or pushing back on a direction they thought was wrong.
- Do they wait to be told, or do they move when they see something that needs doing?

> Keep this to **2 questions** — they should feel like natural conversation, not interrogation. The best answers here are specific and unprompted. If a candidate volunteers accountability or learning moments in other sections, note it — it counts.

---

# Output Format

The generated guide must follow this exact structure:

---

## Interview Guide: [Role Title] — [Level]
**Generated for**: [Project or context name, if provided]
**Suggested duration**: [e.g., 60 minutes]

---

### Candidate & Role Snapshot

**Role summary**: 1–3 sentences on what this role requires, what success looks like in the first 90 days, and what the non-negotiables are. Written so any interviewer can align quickly before the call, even without reading the full job description.

**Candidate overview** *(include only if a CV, LinkedIn profile, or summary was provided)*: 2–4 bullet points summarizing the candidate's background as it relates to this role. Cover:
- Current or most recent role and how it maps to what's being hired for.
- Relevant experience highlights — specific domains, technologies, or contexts that are directly applicable.
- Anything in their trajectory worth noting before the interview — a career pivot, a level jump, extended tenure in a very different environment, etc.
- Initial read on fit: where they look strong on paper, and where the interview should probe harder.

---

### Before You Start — Interviewer Notes
Specific, actionable notes for this interview. Generate only what is relevant — skip any point that doesn't add information beyond the obvious.

- **Scope of this session**: What this guide covers within the broader loop. What other interviewers are handling (if known) so there's no duplication.
- **Priority areas**: The 1–2 dimensions that matter most for this specific role and context. Where to spend time if the interview runs short.
- **Candidate-specific watch points** *(only if background was provided)*: What to probe based on the candidate's CV or profile — gaps to dig into, claims to make concrete, or transitions worth understanding.
- **Hard stops**: Any non-negotiable signals — skills or behaviors — that would end consideration regardless of performance elsewhere.

---

### Section 1 — Technical Knowledge
**Suggested time**: [X minutes]
**Competencies covered**: [List from framework]

For each question include:

**Q: [Question text]**
> *What to listen for*: [2–3 specific signals that indicate strong, average, or weak answers]
> *Follow-up*: [One follow-up to probe depth or test for specificity]

Include **4-7 questions** in this section. Mix conceptual and applied. If project-specific technologies were provided, at least one question must address them directly.

---

### Section 2 — Delivery & Process
**Suggested time**: [X minutes]
**Competencies covered**: [List from framework]

Same question format as Section 1.
Include **2–3 questions**.

---

### Section 3 — Collaboration & Communication
**Suggested time**: [X minutes]
**Competencies covered**: [List from framework]

Same question format as Section 1.
Include **2–3 questions**. At least one must probe client-facing or cross-functional behavior
if the role has any client exposure.

---

### Section 4 — Growth Mindset & Ownership
**Suggested time**: [X minutes]
**Competencies covered**: [List from framework]

Same question format as Section 1.
Include **2 questions**. These are often the most revealing — give them appropriate weight.

---

### Red Flags to Watch For

**Role-level flags** — 3–5 signals grounded in the competency framework for this role and level. Each flag must be specific to what's actually being hired for, not generic. Format:

- **[Signal]**: What it looks like in the interview and why it matters for this role.

**Candidate-specific flags** *(include only if background was provided)* — 1–3 flags derived directly from the candidate's CV or profile. Only include if there's a real concern — don't manufacture flags.

For each candidate-specific flag, include one optional follow-up question the interviewer can use to probe it directly:

- **[Flag based on their background]**: Brief explanation of the concern.
  - *Optional probe*: "[A direct question targeting that specific flag]"

> These are signals to surface in debrief — not automatic disqualifiers. The interviewer's job is to collect evidence, not reach a verdict mid-call.

---

### Scorecard
Designed for engineers with no hiring process background. Should take 2–3 minutes to fill out immediately after the interview, while it's fresh.

**Scale** — one score per dimension:

| Score | What it means |
|-------|---------------|
| 3 — Strong | Clear evidence. Answered with specifics, not generalities. |
| 2 — OK | Some evidence, but incomplete or needed a lot of prompting. |
| 1 — Weak | Little to no evidence. Vague, deflected, or clearly unfamiliar. |

**Fill in after the interview:**

| Dimension | Score (1–2–3) | One thing that stood out (good or bad) |
|-----------|---------------|----------------------------------------|
| Technical Knowledge | | |
| Delivery & Process | | |
| Collaboration & Communication | | |
| Growth & Ownership | | |

**Overall call** — pick one:

- **Yes** — Scored 2 or above in all dimensions, at least two 3s.
- **Yes, but** — One dimension at 1 with a specific, addressable reason. Note it.
- **No** — Any dimension at 1 with no clear explanation, or mostly 2s with no standout signal.

> If you're unsure, write down the specific moment that's making you hesitate. That's what debrief is for.

---

# Example Prompt

> "Role: Frontend Senior Engineer.
> Project context: We're hiring for a mid-size e-commerce client on a 6-month engagement.
> The client is on a tight timeline and the team is small — two FE engineers total.
> This person will work directly with the client's product team and needs to be comfortable in client-facing conversations.
> Tech stack: React, TypeScript, Next.js. The client also uses Contentful as their CMS, so any experience there is a plus.
> We've had issues in the past with engineers who are technically strong but go quiet
> when things get hard. We want someone who surfaces problems early."
