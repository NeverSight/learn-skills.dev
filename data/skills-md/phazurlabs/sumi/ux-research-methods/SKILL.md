---
name: ux-research-methods
description: "UX research methodology: usability testing protocols, user interviews, contextual inquiry, surveys, card sorting, and diary studies, plus synthesis frameworks including JTBD, journey mapping, and affinity diagramming. Use when planning a study, writing a discussion guide, or analyzing research data."
---

# UX Research Methods — Comprehensive Methodology Guide

## Research Philosophy

Great design is grounded in evidence, not assumption. UX research exists to reduce the risk of building the wrong thing and to illuminate the gap between designer intent and user reality. Every design decision should trace back to user evidence — whether from direct observation, behavioral data, or validated heuristics.

### The Research Hierarchy (adapted from NNG Group)

1. **Behavioral data** (what users do) > **Attitudinal data** (what users say)
2. **Qualitative research** (why) informs **quantitative research** (how much)
3. **Generative research** (discover opportunities) precedes **evaluative research** (validate solutions)
4. **Continuous discovery** (ongoing) outperforms **project-based research** (periodic)

## Research Method Selection Matrix

### Discovery / Generative Methods

**Contextual Inquiry**
- Observe users in their natural environment while they perform real tasks
- Combine observation with in-situ interviewing — the "master-apprentice" model
- Ideal for understanding workflows, workarounds, and unarticulated needs
- Sample size: 4-8 participants for pattern identification
- Duration: 1-2 hours per session

**User Interviews (Semi-Structured)**
- Prepare 8-12 open-ended questions organized by research theme
- Follow the "funnel" structure: broad context → specific behaviors → future needs
- Never ask "Would you use X?" — instead ask "Tell me about the last time you..."
- Use the Critical Incident Technique for rich behavioral data
- Sample size: 5-8 participants per segment (saturation typically at 5-6)
- Remote interviews are acceptable; enable video for nonverbal cues

**Diary Studies**
- Participants log experiences over 1-4 weeks using structured prompts
- Captures longitudinal patterns that single-session methods miss
- Excellent for understanding habit formation, pain points over time, and context switching
- Use mobile-friendly logging tools (photos, voice memos, short text)
- Sample size: 10-15 participants to account for dropout

**Card Sorting**
- Open sort: users create their own category structure — reveals mental models
- Closed sort: users organize items into predefined categories — validates IA
- Hybrid sort: predefined categories with option to create new ones
- Use tools like Optimal Workshop or Maze for remote card sorts
- Sample size: 15-30 participants for statistical reliability

**Stakeholder Interviews**
- Map business constraints, technical limitations, and success metrics before user research
- Ask: "What would need to be true for this project to succeed?"
- Identify conflicting stakeholder goals early to mediate through user evidence

### Evaluative Methods

**Usability Testing (Moderated)**
- The gold standard of evaluative UX research
- Think-aloud protocol: ask participants to verbalize thoughts while performing tasks
- Task-based structure: 5-8 realistic scenarios with measurable success criteria
- Metrics: task success rate, time on task, error rate, satisfaction (SUS/SEQ)
- Sample size: 5 participants identify ~85% of usability issues (NNG finding)
- Run iterative rounds (test → fix → retest) rather than one large study

**Unmoderated Remote Testing**
- Scale usability testing to larger samples without moderator presence
- Platform options: UserTesting, Maze, Lookback, PlaybookUX
- Best for validating specific flows rather than open exploration
- Include post-task and post-study questionnaires
- Sample size: 10-20 for quantitative confidence

**A/B Testing**
- Compare two design variants with random user assignment
- Requires sufficient traffic volume for statistical significance (use calculators)
- Test one variable at a time for clear causation
- Minimum detectable effect must be defined before test launch
- Run for full business cycles (at least 1-2 weeks) to avoid temporal bias

**Heuristic Evaluation**
- Expert review against established usability principles (see nng-ux-heuristics skill)
- Fast and cost-effective — complements but does not replace user testing
- 3-5 evaluators find ~75% of usability problems
- Use severity ratings to prioritize findings

**Cognitive Walkthrough**
- Step through tasks from a first-time user's perspective
- At each step ask: Will the user know what to do? Will they recognize the correct action? Will they understand the feedback?
- Effective for onboarding flow evaluation

### Quantitative Methods

**Surveys and Questionnaires**
- Use validated instruments: SUS (System Usability Scale), SUPR-Q, NPS, UMUX-Lite
- Custom surveys: limit to 10-15 questions, use Likert scales consistently
- Avoid leading questions and double-barreled questions
- Pilot test with 3-5 people before full deployment
- Sample size: 100+ for statistical reliability (400+ for segment comparison)

**Analytics and Behavioral Data**
- Define key behavioral metrics tied to user goals, not vanity metrics
- Funnel analysis: identify where users drop off in critical flows
- Session recordings and heatmaps for qualitative context on quantitative patterns
- Cohort analysis to understand behavior changes over time
- Set up event tracking before launch, not after

**Tree Testing**
- Evaluate information architecture findability without visual design influence
- Present text-only hierarchy, ask users to locate specific items
- Success metrics: directness (% choosing correct path first), completion rate
- Sample size: 50+ for reliable results

## Research Synthesis Frameworks

### Affinity Diagramming
1. Capture individual observations on sticky notes (physical or digital — Miro, FigJam)
2. Silently group related observations into clusters
3. Name each cluster with a descriptive theme
4. Identify patterns, contradictions, and surprises across clusters
5. Prioritize themes by frequency, severity, and strategic importance

### Jobs-to-Be-Done (JTBD) Framework
- "People don't want a quarter-inch drill — they want a quarter-inch hole" (Theodore Levitt)
- Structure: When [situation], I want to [motivation], so I can [expected outcome]
- Identify functional, emotional, and social jobs
- Map current solutions and satisfaction gaps

### Journey Mapping
1. Define the persona and scenario scope
2. Map phases from awareness through post-use
3. For each phase: actions, thoughts, emotions, touchpoints, pain points, opportunities
4. Identify moments of truth — high-emotion points where experience is won or lost
5. Prioritize opportunities by user impact × business value × feasibility

### Research Repository
- Maintain a living research repository (Dovetail, Notion, or similar)
- Tag findings by theme, product area, persona, and severity
- Enable cross-study pattern recognition
- Share insights proactively — research unseen is research wasted

## Research Operations

### Planning a Research Study
1. Define research questions (3-5 focused questions per study)
2. Select appropriate method(s) based on questions and constraints
3. Write a 1-page research plan: goals, method, participants, timeline, deliverables
4. Recruit representative participants — screen rigorously for target criteria
5. Prepare materials: discussion guide, task scenarios, consent forms
6. Pilot test the protocol with 1-2 internal participants

### Participant Recruitment
- Screen for behavioral criteria, not just demographics
- Include users with disabilities (minimum 1 per study for inclusive insights)
- Offer fair compensation respecting participants' time and expertise
- Maintain a participant panel for longitudinal research
- Avoid "professional testers" — seek real target users

### Ethical Research Practice
- Obtain informed consent with clear explanation of data usage
- Allow participants to withdraw at any time without consequence
- Protect participant privacy and anonymize data
- Never manipulate or deceive participants
- Share findings back with participants when possible

## AI-Augmented Research Methods

Generative AI is transforming UX research operations. Use AI as an accelerator for research synthesis while maintaining researcher judgment as the quality gate.

### AI-Assisted Synthesis and Analysis

- **Theme extraction:** Use LLMs to identify initial themes from interview transcripts and open-ended survey responses. Treat AI-generated themes as a starting point for researcher refinement, never as final output.
- **Interview coding:** AI can perform first-pass coding of qualitative data against an established codebook, reducing coding time by 40-60%. Researchers must validate every AI-assigned code — expect 70-85% accuracy on well-defined codes.
- **Survey analysis:** LLMs can summarize open-ended survey responses, identify sentiment patterns, and flag outlier responses for manual review.
- **Research hypothesis generation:** After providing AI with research findings, use it to generate hypotheses for future studies. This combats researcher tunnel vision by surfacing unexpected connections.

### Quality Validation

Never trust AI analysis without researcher review. Establish a mandatory validation workflow:

1. AI performs first-pass analysis (coding, theme extraction, summarization).
2. Researcher reviews 100% of AI-generated output for the first three studies.
3. After calibrating AI accuracy, researcher spot-checks 30-50% of output.
4. All AI-generated insights must be traceable to specific participant quotes or data points.
5. Final research reports must be authored by the researcher, not generated by AI.

### Prompt Engineering for Research

Use specific, structured prompts for research tasks:

- For coding: "Code each statement in this transcript using only these codes: [codebook]. For each code assignment, quote the exact text that justifies it."
- For theme extraction: "Identify recurring themes across these 8 interview transcripts. For each theme, provide 3+ supporting quotes from different participants."
- For survey analysis: "Summarize the key themes in these 200 open-ended responses. Group by theme, report frequency, and include representative quotes."

### Ethical Considerations

- Never upload identifiable participant data to AI services without explicit consent and data processing agreements.
- Anonymize transcripts before AI processing.
- Disclose AI-assisted analysis in research reports.
- AI cannot replace researcher empathy, contextual understanding, or ethical judgment.

## Routing

For **running a study** — moderator scripts, interview discussion guides,
contextual inquiry, diary studies, card sorting and tree testing, A/B protocols,
survey design, and a participant screener template: read
`references/research-protocols.md`.

For **making sense of what you collected** — affinity diagramming, thematic
coding, Jobs-to-Be-Done, journey-map construction, turning data into personas,
SUS scoring and significance testing, mixing qual and quant, and repository
management: read `references/analysis-frameworks.md`.

## Cross-Referencing

- For heuristic evaluation methodology, reference `nng-ux-heuristics`.
- For accessibility research requirements, reference `accessibility-inclusive-design`.
- For mobile-specific testing considerations, reference `mobile-ux-design`.
- For design system validation, reference `design-systems-architecture`.
- For UX metrics and measurement frameworks, reference `ux-metrics-measurement`.
- For AI-specific research methods, reference `agentic-ai-generative-ux`.

## v3.0 Cross-References

The v3.0 upgrade introduces skills and references that extend research methodology into structured critique, AI-augmented synthesis, and advanced feedback frameworks.

### Structured Critique Frameworks — `design-critique-case-studies`

The `design-critique-case-studies/references/critique-methodology.md` reference provides structured feedback frameworks that complement research findings. When research surfaces usability issues, critique methodology offers systematic approaches for translating raw findings into actionable design direction — including critique session structures, feedback taxonomy (functional, aesthetic, strategic), and stakeholder alignment techniques. Pair research readouts with structured critique sessions to accelerate the insight-to-action pipeline.

### AI-Augmented Research Synthesis — `agentic-ai-generative-ux`

The `agentic-ai-generative-ux` skill expands significantly on the AI-Augmented Research Methods section above with 2026 approaches to research synthesis. Key additions include: multi-agent research analysis pipelines where specialized AI agents handle transcription, coding, theme extraction, and cross-study pattern detection as coordinated stages; retrieval-augmented generation (RAG) patterns for querying research repositories with natural language; and generative participant recruiting using AI to screen and match participants to study criteria. The skill also covers emerging ethical frameworks for AI in research, including bias detection in AI-generated themes and participant data sovereignty considerations.

### Note on Existing AI Research Coverage

The AI-Augmented Research Methods section in this skill covers foundational practices (AI-assisted synthesis, quality validation, prompt engineering, ethics). The v3.0 `agentic-ai-generative-ux` skill extends these into production-scale research operations and the latest multi-agent orchestration patterns emerging in 2026.

## Key Sources

- NNG Group: "Which UX Research Methods" and research methodology articles
- Portigal, S. (2013). "Interviewing Users"
- Krug, S. (2014). "Rocket Surgery Made Easy"
- Sauro, J. & Lewis, J. (2016). "Quantifying the User Experience"
- Arxiv: GenAI for UX Research (Dec 2025)
- Arxiv: EvAlignUX — Evaluating AI Alignment in UX Research (Sep 2024)
