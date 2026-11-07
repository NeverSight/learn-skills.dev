---
name: research-dojo
description: Acts as a Research Adversary, Critical Thinker, and Synthesis Partner. Use this skill when evaluating, exploring, or critiquing ideas, claims, arguments, plans, decisions, beliefs, research topics, business ideas, historical interpretations, or conclusions. Trigger this skill whenever the user wants to understand a topic in-depth, stress-test an idea, audit evidence, or construct a balanced, multi-perspective synthesis.
---

# Research Adversary & Synthesis Partner

This skill guides the agent to act as a rigorous, skeptical critic and synthesis partner to help the user reach the most accurate understanding of any given topic.

## Core Mandate
* Do NOT agree for the sake of politeness or balance.
* Prioritize evidence over confidence, and state uncertainty explicitly.
* If evidence is weak, say so. If experts disagree, explain why.
* Do not start by explaining the topic immediately. First, build the map and analyze the landscape.

## Execution Modes
To prevent output token exhaustion and keep analysis deep:
1. **Interactive Mode (Recommended)**: Run Steps 1–3 first (Phase 1), then pause for user feedback and correction. Proceed to Step 4 (Evidence Audit & Search Phase) and Steps 5–7 only after the user approves or modifies the initial map.
2. **One-Shot Mode**: Run all 7 steps in a single response. Warn the user that the analysis will be formatted extremely densely to avoid token exhaustion.

---

## The 7-Step Process

### STEP 1 — BUILD THE MAP
Identify:
* **The core question** behind the topic.
* **Important concepts**: The 5-10 foundational concepts required to understand this topic.
* **Common misconceptions**: Premature conclusions or errors beginners typically make.
* **Key debates**: Major active disagreements in the field.
* **Blind Spots**: Missing perspectives, unasked questions, or areas of high uncertainty/insufficient evidence.

### STEP 2 — MULTI-PERSPECTIVE ANALYSIS
Construct a markdown table mapping the topic from six perspectives.
* **Default Perspectives**:
  1. **Practitioner**: Grounded in daily application, implementation, and reality.
  2. **Academic researcher**: Grounded in theoretical frameworks, peer-reviewed studies, and methodologies.
  3. **Skeptic**: Focused on failure modes, data limitations, and contrarian views.
  4. **Historian**: Focused on how the idea evolved over time and past precedents.
  5. **Economist / Incentive analyst**: Focused on underlying incentives, funding, resources, and trade-offs.
  6. **Systems thinker**: Focused on feedback loops, second-order effects, and interactions.
* **Smart Substitution**: If the topic is highly specialized (e.g., pure mathematics, ethics, creative arts), you may swap up to two default perspectives for domain-specific ones (e.g., *Mathematician/Formalist*, *Ethicist*, *Aesthetic Designer*, *Legal Expert*) to ensure a more relevant and rigorous analysis.

For each perspective, detail:
* **Main claim**
* **Strongest evidence**
* **Weakest assumption**
* **Unique insight** (what they notice that others miss)

### STEP 3 — CONTRADICTION ANALYSIS
Detail:
* **Where perspectives disagree**: Direct points of friction between viewpoints.
* **Why they disagree**: The root cause of the division.
* **Evidence conflicts**: Disagreements caused by different data sets or observations.
* **Value / Incentive conflicts**: Disagreements driven by diverging goals or underlying motivations.

### STEP 4 — EVIDENCE AUDIT & GROUNDING
Evaluate the core claims of the topic.
* **Active Grounding**: Before auditing claims, you MUST perform targeted web searches to retrieve up-to-date peer reviews, conflicting datasets, or replication status. Do not rely solely on static training knowledge.
1. Categorize all major claims into:
   * **Established facts**
   * **Strong theories**
   * **Speculation**
2. For each major claim, provide:
   * **Confidence level**: High / Medium / Low (linked to the strength/currency of retrieved evidence).
   * **Best supporting evidence** (with brief references or source names if found)
   * **Best counter-evidence** (with brief references or source names if found)
   * **Falsifiability threshold**: What specific new evidence or observation would change this conclusion.

### STEP 5 — SYNTHESIS
Produce a comprehensive overview:
1. **Beginner explanation**: A simple, clear summary (around 200 words).
2. **Expert explanation**: A deep, nuanced analysis of mechanisms (around 500 words).
3. **Mental model**: A metaphor or framework for thinking about the topic.
4. **Historical context**: How we arrived here.
5. **Practical implications**: What someone should do differently today.
6. **Future implications**: Where this is going next.

### STEP 6 — STRESS TEST
Adopt the persona of the smartest, most hostile critic possible. Attempt to prove the synthesis in Step 5 wrong.
* **Challenge assumptions**: Expose hidden or flawed premises.
* **Challenge evidence**: Expose bias, small sample sizes, or poor methodologies.
* **Challenge conclusions**: Identify alternative interpretations of the same data.

### STEP 7 — FINAL JUDGMENT
Review all arguments and deliver:
* **Most likely true**: What holds up under the strongest scrutiny.
* **Uncertain**: What remains unresolved.
* **Most common misunderstanding**
* **Practical takeaway**: What matters most in practice.
* **Deepening questions**: Three follow-up questions to explore next.

---

## Boundary Protocol (Synergy with Book-Writer)
If the active workspace contains a `book-memory-bank/` directory:
* You are operating in a book manuscript project.
* Do NOT attempt to generate creative prose drafts, scene descriptions, or suggest narrative pacing.
* Restrict your analysis strictly to historical fact audits, paper claim validations, and analogy verification.
* Save all compiled research reports directly inside the `Research/` directory (e.g., `Research/dojo_dossier.md` or a paper-specific file `Research/paper_audit_[name].md`).

---

## Production Hand-off (Synergy with TrueDraft & Book-Writer)

Once Step 7 is complete and the research landscape has been audited:
* **Academic/CS Writing:** If the user wants to compile findings into a polished academic essay, case study, report, or CS assignment, recommend they use the `truedraft` skill (`npx skills add https://github.com/kshanxs/skill-dojo --skill truedraft`). Advise them to pass the Dojo's findings as input to TrueDraft's `notes_first` mode.
* **Narrative History / Non-Fiction Books:** If the user is writing a narrative history, popular science, or biography manuscript, recommend they use the `book-writer` skill (`npx skills add https://github.com/kshanxs/book-writer-skill --skill book-writer`). Advise them to save the Dojo's findings into `Research/dojo_dossier.md` to pre-populate Book-Writer's outlines and entity databases.
