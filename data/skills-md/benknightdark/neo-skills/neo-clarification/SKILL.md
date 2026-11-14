---
name: neo-clarification
description: >
  Use this skill when the user gives vague, emotional, fragmented, screenshot-based,
  or complaint-style requirements and wants them converted into structured specs,
  acceptance criteria, or clarifying questions.
---

# Requirement Clarification Specifications

Apply the Inversion & Generator Pattern. Follow this protocol strictly to translate raw, chaotic user complaints and screenshots into clean, structured system specifications.

---

## 1. Perceive Phase

1. **Information Extraction**:
   - Carefully read the user's text and inspect any attached screenshots or logs.
   - Filter out emotional noise, frustrations, and blame.
   - Separate objective facts (what is currently happening or visible) from user expectations (what they wanted to accomplish).

2. **Identify System Boundaries**:
   - Determine the scope, domain, and potential technical layers affected by the feedback (e.g., frontend rendering, network APIs, database states, permission groups).

---

## 2. Reason Phase

1. **Load Analysis Framework**:
   - **Always read** the external analysis guide before starting your deduction:
     [5w1h-framework.md](file:///Users/ben/Projects/neo-skills/skills/neo-clarification/references/5w1h-framework.md)
   
2. **Context Reconstruction (5W1H)**:
   - Map the extracted facts to the 5W1H framework (Who, Where, When, What, Why, How).
   - Formulate logical hypotheses on the root causes of UI anomalies or system behaviors.

3. **Identify Gaps**:
   - Pinpoint critical missing information (e.g., browser environment, specific action steps, parameters, error logs).
   - Prepare a list of clarifying questions to ask the user.

---

## 3. Act Phase

Generate a structured "Requirement Translation and Clarification Report" strictly in **Traditional Chinese (Taiwan)**. Follow these steps:

1. **Load Output Template**:
   - Read the standard markdown structure from:
     [clarification-template.md](file:///Users/ben/Projects/neo-skills/skills/neo-clarification/assets/clarification-template.md)

2. **Compile the Report**:
   - Fill in the template using Traditional Chinese.
   - **Context Restoration**: Present objective facts concisely without emotional adjectives.
   - **User Story**: Use the strict format: "身為... 我想要... 以便於..."
   - **System Requirements & Hypotheses**: Highlight key rendering, API, and validation checkpoints for the development team.
   - **Open Questions**: List between 2 and 10 polite, precise, and constructive clarifying questions.

3. **Self-Validation**:
   - Proactively validate your report using the non-interactive python script:
     ```bash
     uv run skills/neo-clarification/scripts/validate-requirements.py -i <path_to_saved_report>
     ```
     *(Or verify mentally that all sections exist and the number of questions is between 2 and 10 before final output).*

---

## 4. Communication Guidelines

- **Maintain Empathetic Neutrality**: Acknowledge the user's difficulty, but never agree that the system is "broken" or "a disaster" in the official report. Use neutral, objective descriptions.
- **Strictly No Guesswork**: Do NOT invent features that the user did not hint at. Ask clarifying questions instead.
