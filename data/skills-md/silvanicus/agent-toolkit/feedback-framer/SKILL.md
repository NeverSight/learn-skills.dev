---
name: feedback-framer
description: Structures written performance or peer feedback for colleagues and direct reports using the SBI model (Situation → Behavior → Impact). Use when writing review comments in tools like Lattice or Workday, or drafting feedback in email or Slack.
---

# Overview
Turns your observations and notes into structured, competency-anchored written feedback — so every review is consistent, fair, and grounded in what's actually expected at that role and level. Rather than generic comments, this skill anchors your feedback in your organization's competency framework or role expectations, then structures it using the SBI model (Situation → Behavior → Impact). The result is feedback that reflects your standards and reads as credible and actionable.

# When to use this Skill
Use this skill when:
- Structuring written feedback for a colleague or a direct report.
- Writing performance review comments (e.g., in Lattice, Workday, 15Five).
- Drafting peer feedback in an email or Slack message.
- Delivering difficult feedback in a way that is fair and actionable.

# When NOT to use this Skill
- For purely positive praise with no critique needed.
- For informal, casual compliments.
- For disciplinary or HR-sensitive conversations (consult HR/talent directly).

# Workflow

Follow these steps in order every time this skill is invoked:

## Step 1 — Identify the role
Extract the role from the user's prompt. Normalize it to a filename-friendly slug
(e.g., "Senior UI Engineering" → `senior-ui-engineer`).

## Step 2 — Load the competency table
Look for a matching file in `shared/competencies/`.

- **If found**: Read the file and keep the competencies in mind for the rest of the session.
  They define what is expected at that level and should anchor your analysis and questions.
- **If not found**: Tell the user no competency table exists for that role yet, then ask:
  > "Could you briefly describe what is expected at this level, or should I proceed with
  > general engineering/role expectations?"
  Wait for their answer before continuing.

## Step 3 — Analyze the provided information
Review what the user wrote in their prompt. Identify:
- Strengths mentioned (explicit or implied).
- Areas for improvement mentioned (explicit or implied).
- Gaps: competencies from Step 2 that the user did not address at all.

## Step 4 — Deep-dive clarifying questions *(most critical step)*

This is the most important step. Your goal is to surface concrete, credible, specific
evidence that transforms vague impressions into feedback that is fair, actionable, and
defensible. Do not rush it.

**Structure your questions in labeled groups** so the user can see exactly what you are
probing. Use the categories below, adapting the questions to what was actually provided.

---

### A. Specific Examples & Evidence
For every strength or improvement area mentioned, ask for at least one concrete example.
If the user already gave one, push for a second to check if it's a pattern.

- "Can you describe a specific situation where [behavior] happened? (Project name, meeting, PR, incident — any concrete reference helps.)"
- "Is this the most recent or the clearest example you have? Is there an earlier one that shows the same pattern?"
- "Do you have any artifacts that capture this — a peer comment, a Slack thread, a post-mortem — even if just paraphrased?"

### B. Frequency & Pattern
Single events don't define a person. Help the user distinguish consistent patterns from
isolated moments.

- "How often does this happen — would you say it's occasional, recurring, or consistent throughout the review period?"
- "Has this changed over time? Getting better, getting worse, or staying the same?"
- "Are there specific conditions where this behavior is more or less likely — certain types of work, team dynamics, pressure levels?"

### C. Impact & Stakeholder Effect
The SBI model lives or dies on impact. Push until the impact is specific.

- "How did this affect the team, the project timeline, or the quality of output? Can you quantify it even roughly?"
- "Who else noticed or was affected? (QA, PM, stakeholders, other engineers?)"
- "If this behavior changed, what would be different — what would you see more or less of?"

### D. Prior Conversations & Context
Context shapes how feedback lands. If this is a repeated issue, the review should
reflect that.

- "Have you discussed this with [name] before? What was their response — did they seem aware of it?"
- "Is there any context (personal, workload, team changes) that might help explain this pattern?"
- "Is this something you expect at this level, or would it only matter for the next level up?"

### E. Competency Gaps (from Step 3)
For each competency not addressed in the original notes, ask directly:

- "The competency table includes [gap]. Do you have any observations about [name] in this area — even if minor?"
- "Should this be flagged as 'not enough data' or is it intentionally not relevant this cycle?"

---

**Select the most relevant 4–7 questions** based on what is missing or underdeveloped
in the user's input. Do not ask all questions if many are already answered — use judgment.

**Always close with:**
> "Or, if you prefer, just say **'generate'** and I'll create the feedback with what I have so far."

Wait for the user's answers before moving to the next step. If the user says "generate"
at any point, skip directly to Step 5.

## Step 5 — Ask for output format
Before generating, ask the user how they'd like to receive the feedback:

> "How would you like this feedback delivered?
> - **Plain text** — ready to copy and paste into Lattice, Workday, email, or Slack
> - **Markdown** — structured with headers, ideal for Notion, GitHub, or similar tools
> - **Word / Google Doc format** — clean prose paragraphs, easy to drop into a document
> - **PDF-ready** — formatted for export via the `/pdf` skill"

Wait for the user's answer. If the user says "generate" at any point, default to plain text.

## Step 6 — Generate the feedback
Using all collected information, produce the written feedback in the chosen format, following the
Feedback Framework and Output Format sections below.

---

# Feedback Framework
This skill structures feedback using the **SBI model** (Situation → Behavior → Impact):
- **Situation**: Describe the specific context or event.
- **Behavior**: Describe the observable behavior (not assumptions or character judgments).
- **Impact**: Describe the effect that behavior had on you, the team, or the outcome.

# Writing Style Guide
- **Stay close to the user's words.** Preserve the language, phrasing, and specific observations from the original notes as much as possible. Do not paraphrase or sanitize unless necessary for clarity or professionalism.
- **Don't invent examples.** Only use situations, behaviors, and impacts that come from what the user provided or answered in the clarifying questions.
- **Elevate, don't replace.** Your job is to structure and sharpen the user's input, not rewrite it. The voice should still sound like the person giving the feedback.
- **Avoid generic filler.** Phrases like "demonstrates a strong commitment to excellence" or "is a valuable team member" add no signal. Cut them unless they are directly supported by the user's notes.
- **Match the register.** If the user writes casually, keep the tone warm and direct. If they write formally, match that. Do not default to corporate-speak.

# Output Format
Generated feedback will include:
- An opening that acknowledges the person's effort or intent.
- 2–4 specific feedback points following the SBI structure.
- A closing with a forward-looking, encouraging statement.

# Example Prompt
> "Name: Jamie.
> "Role: Senior UI engineering.
> "Context: Lattice perfomance review
> "I think she is accountable and based on the feedback I have had from QA, her deliverables are usually fast, in really good quality. Technically she is senior and shows a really good understanding and skills around quality engineering, accesibility and design systems.
> The only aspect I will improve is that she is too quite and she is not involved in a lot of conversations around solutions, blockers, etc.
> Althogh this is not a requirement for his role, usually senior engineers try to participate more in the solutioning of the different tickets and during daily, participate in different conversations around best practices, requirements, etc.
>With her knowledge, she could be more impactful in a project and a team."
