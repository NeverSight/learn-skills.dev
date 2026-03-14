---
name: starwave:requirements
description: 1. Requirement Gathering
---

### 1. Requirement Gathering

First, generate an initial set of requirements in EARS format based on the feature idea, then iterate with the user to refine them until they are complete and accurate.

Don't focus on code exploration in this phase. Instead, just focus on writing requirements which will later be turned into
a design.

**Constraints:**

- The model MUST first propose a {feature_name} based on: (1) user's explicit preference if stated, (2) current branch name if not a default branch like main or develop, (3) derived from the prompt content. The model MUST allow the user to override this proposal.
- The model MUST wait for the user's answer to the {feature_name} question.
- Once the {feature_name} is decided, the model MUST first ask general questions that are important to the requirements. This includes, but is not limited to, backwards compatibility.
- The model MUST create a 'specs/{feature_name}/requirements.md' file if it doesn't already exist
- Unless told differently by the user, the model MUST ask clarifying questions around the proposed solution.
- The model MUST keep asking questions, until everything is clear or the user indicates they want to stop answering.
- The model MUST generate an initial version of the requirements document based on the user's rough idea AND ask any potential clarifying questions.
- The model MUST format the initial requirements.md document with:
  - A clear introduction section that summarizes the feature
  - A hierarchical numbered list of requirements where each contains:
    - A user story in the format "As a [role], I want [feature], so that [benefit]"
    - A numbered list of acceptance criteria in EARS format (Easy Approach to Requirements Syntax)
    - Ensure the double whitespace at the end of an acceptance criteria is there to ensure rendering the markdown will show a newline
  - Example format:
```
### 1. Data-Level Transformation Support

**User Story:** As a developer, I want to transform data at the structural level before rendering, so that I can perform operations like filtering and sorting without parsing rendered output.

**Acceptance Criteria:**

1. <a name="1.1"></a>The system SHALL provide a DataTransformer interface that operates on structured data instead of bytes
2. <a name="1.2"></a>The system SHALL allow data transformers to receive Record arrays and Schema information
3. <a name="1.3"></a>The system SHALL apply data transformers before rendering to avoid parse/render cycles
4. <a name="1.4"></a>The system SHALL maintain the existing byte-level Transformer interface for backward compatibility
5. <a name="1.5"></a>The renderer SHALL detect whether a transformer implements DataTransformer and apply it at the appropriate stage
6. <a name="1.6"></a>The system SHALL preserve the original document data when transformations are not applied
```
- When asking the user questions and offering options, the model MUST use the AskUserQuestion tool.
- The model SHOULD consider edge cases, user experience, technical constraints, and success criteria in the initial requirements

**Self-Review Checklist (before skill review):**
Before triggering skill reviews, the model MUST verify:
- [ ] Each requirement has a user story in "As a [role], I want [feature], so that [benefit]" format
- [ ] All acceptance criteria use EARS keywords (SHALL, SHOULD, MAY, WHEN, WHERE, IF, THEN)
- [ ] Each acceptance criterion is testable (can be verified with a concrete test)
- [ ] Anchor tags follow the pattern `<a name="X.Y"></a>` for cross-referencing
- [ ] No vague terms without definition (e.g., "fast", "reliable", "user-friendly")
- [ ] Edge cases and error conditions are addressed

- After updating the requirement document, the model MUST use BOTH design-critic and peer-review-validator subagents sequentially to review the document:
  1. FIRST: Use the Task tool with subagent_type="general-purpose" to run the design-critic skill (invoke the Skill tool with skill="design-critic") to perform a critical review that challenges assumptions, identifies gaps, and questions necessity
  2. SECOND: Use the Task tool with subagent_type="peer-review-validator" to validate the requirements and critical review findings by consulting external AI systems (Gemini, Codex, Q Developer)
  3. The model MUST synthesize the findings from both reviews and present the key insights, questions, and recommendations to the user
- After presenting the synthesized review findings, the model MUST ask the user "Do the requirements look good or do you want additional changes?"
- If the user responds with affirmations like "yes", "looks good", "approved", or similar, consider this explicit approval and proceed to the next phase
- If the user provides feedback or requests changes, the model MUST make the modifications and repeat the review cycle (design-critic → peer-review-validator → user approval)
- If the user's response is unclear, the model MUST ask a clarifying question before proceeding
- The model MUST document all decisions, answered questions, and their rationales in specs/{feature_name}/decision_log.md as they occur throughout the requirements phase
- The model SHOULD suggest specific areas where the requirements might need clarification or expansion
- The model MAY ask targeted questions about specific aspects of the requirements that need clarification
- The model MAY suggest options when the user is unsure about a particular aspect
