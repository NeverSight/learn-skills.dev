---
name: starwave:design
description: 2. Create Feature Design Document
---

### 2. Create Feature Design Document

After the user approves the Requirements, you should develop a comprehensive design document based on the feature requirements, conducting necessary research during the design process.
The design document should be based on the requirements document, so ensure it exists first.

**Constraints:**

- The user provides the {feature_name} as part of the prompt, or by way of the current branch which will contain the name of the feature, either in whole or prefixed by specs/.
- Verify that the specs/{feature_name} folder exists and has a requirements.md file
- If the folder does NOT exist, the model MUST request the user to provide the {feature_name} using the question "I can't find the feature, can you provide it again?"
- If the requirements.md file does not exist in the folder, the model MUST inform the user that they need to use the requirements skill to create it first.
- If a decision_log.md file exists in the specs/{feature_name} folder, the decisions in there MUST be followed.
- The model MUST create a 'specs/{feature_name}/design.md' file if it doesn't already exist
- The model MUST identify areas where research is needed based on the feature requirements
- The model MUST conduct research and build up context in the conversation thread
- The model SHOULD NOT create separate research files, but instead use the research as context for the design and implementation plan
- The model MUST summarize key findings that will inform the feature design
- The model SHOULD cite sources and include relevant links in the conversation
- The model MUST create a detailed design document at 'specs/{feature_name}/design.md'
- The model MUST incorporate research findings directly into the design process
- The model MUST include the following sections in the design document:
  - Overview
  - Architecture
  - Components and Interfaces
  - Data Models
  - Error Handling
  - Testing Strategy
- When writing the Testing Strategy section, the model SHOULD evaluate acceptance criteria for property-based testing (PBT) candidates:
  - Review requirements that express universal guarantees (invariants, round-trip behavior, idempotence)
  - For components like parsers, serializers, data structures, or algorithms, consider whether PBT would provide better coverage than example-based tests alone
  - If PBT is appropriate, specify: the properties to test, the framework to use (based on project language), and the input generation approach
  - If PBT is not appropriate for the feature, this should be omitted from the Testing Strategy
- The model SHOULD include diagrams or visual representations when appropriate (use Mermaid for diagrams if applicable)
- The model MUST ensure the design addresses all feature requirements identified during the clarification process
- The model MUST use tools like context7 to retrieve relevant information about the libraries and tools

**Self-Review Checklist (before skill review):**
Before triggering skill reviews, the model MUST verify:
- [ ] Each requirement from requirements.md has a corresponding design element
- [ ] All acceptance criteria can be traced to specific components or interfaces
- [ ] Data models support all required operations from the requirements
- [ ] Error handling covers failure modes implied by requirements
- [ ] Testing strategy includes tests for each acceptance criterion
- [ ] No design elements exist without a corresponding requirement (scope creep check)

**Self-Validation via Explanation:**
- The model MUST use the explain-like skill (invoke the Skill tool with skill="explain-like") to explain the design at multiple expertise levels (beginner, intermediate, expert)
- This serves as a self-review mechanism: if the design cannot be clearly explained at each level, it may indicate gaps, overcomplexity, or logic issues
- The model SHOULD address any issues discovered during this explanation process before proceeding to skill reviews

- The model MUST use relevant skills to receive feedback on the design, after writing the initial design. The requirements MUST always take precedence over this feedback.
- The model MUST highlight design decisions and their rationales in a decision log document at specs/{feature_name}/decision_log.md
- The model MUST ask the user for input on specific technical decisions during the design process
- When asking the user questions and offering options, the model MUST use the AskUserQuestion tool.
- After updating the design document, the model MUST use the Task tool with subagent_type="general-purpose" to run the design-critic skill (invoke the Skill tool with skill="design-critic"), and the Task tool with subagent_type="peer-review-validator" to review the document and provide its questions to the user.
- After the review by the skills, the model MUST ask the user "Does the design look good?"
- The model MUST make modifications to the design document if the user requests changes or does not explicitly approve
- The model MUST ask for explicit approval after every iteration of edits to the design document
- The model MUST incorporate all user feedback into the design document before proceeding
