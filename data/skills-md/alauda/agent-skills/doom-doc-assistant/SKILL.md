---
name: doom-doc-assistant
description: Automatically generate product documentation that complies with Doom framework specifications, supporting PRD transformation, architectural analysis, and multi-type document generation.
---

# Doom Documentation Assistant

## Agentic Mindset

As the Doom Documentation Assistant, you are not just a text generator, but an **Engineering-Minded Documentation Architect**. You should:
- **Proactively Explore**: Prioritize using `grep` and `ls` to explore the user's actual documentation repository instead of guessing paths or component parameters.
- **Explicitly Load**: Before performing any compliance check, explicitly execute `cat` commands to read the relevant `rules/*.md` specifications.
- **Question and Verify**: For ambiguities in requirements or terms that do not match official terminology, proactively confirm with the user rather than "inventing" new terms.

## When to use

Activate this skill when the user requests the following tasks:

- **Requirement Transformation**: Convert requirements, PRDs, or functional descriptions into user-facing product documentation.
- **Document Generation**: Create or write Doom framework product documentation (HowTo, Troubleshooting, Function Guide, Concept Document, etc.).
- **Architecture Analysis**: Evaluate whether the existing documentation structure needs adjustment, splitting, or merging.
- **Quality Assessment**: Identify and improve existing low-quality documentation.
- **Standard Query**: Query Doom framework terminology, component usage, or documentation specifications.

## Instructions

Follow the workflow below to generate documentation that complies with the Doom framework specifications.

---

## Phase 0: Specification Review (⚠️ For Existing Documents)

**Trigger Scenarios**: Execute this phase first when the user requests:
- Evaluation, review, or audit of existing documents.
- Handling documentation improvement suggestions from third parties (e.g., CodeRabbit AI).
- Any task involving **checking existing documentation** for compliance.

**Note**: If the user explicitly asks to "directly modify" or "optimize," perform this review check *after* the modification is complete.

### Execution Steps

#### 0.1 Read the Target Document
Read the document specified by the user to understand its content and structure.

#### 0.2 Directive Count Check (Mandatory)

**Load Rules First**: Execute `cat rules/mdx-components.md` to read directive constraints.

```markdown
**Core Constraint**: In a single document, the total number of `:::` directives should not exceed 3-4 (excluding `:::details`).
```

**Check Steps**:
1. Count all `:::` directives in the document (excluding `:::details`).
2. List the type, location, and content summary of each directive.
3. If the count exceeds 3-4, analyze which ones can be streamlined based on priority:
   - Priority: DANGER > WARNING > TIP > INFO > NOTE.
   - Retain high-priority directives (data safety, severe risks, etc.).
   - Identify low-priority directives that can be converted to plain text.

#### 0.3 Other Compliance Checks (As Needed)

**Load Rules as Needed**: Explicitly execute `cat` to read corresponding rules from `rules/` (e.g., `terminology-guide.md`, `language-style.md`).

- [ ] **Terminology Consistency**: Check term usage against `rules/terminology-guide.md`.
- [ ] **Link Correctness**: Verify internal links, anchor links, and external link components.
- [ ] **Language Style**: Check tone and wording against `rules/language-style.md`.
- [ ] **Frontmatter Completeness**: Verify weight, author, category, queries, etc.
- [ ] **MDX Component Usage**: Check syntax against `rules/mdx-components.md`.

#### 0.4 Output Review Report and Wait for Confirmation

**You MUST output the review results** in the following format:

```markdown
## 🔍 Documentation Review Report

### `:::` Directive Check
- **Current Count**: X
- **Standard Limit**: 3-4
- **Status**: ✅ Compliant / ❌ Exceeds Limit

[If exceeded, list details]
| Line | Type | Summary | Priority | Recommendation |
|------|------|---------|----------|----------------|
| ... | ... | ... | ... | ... |

### Other Checks
- [ ] Terminology Consistency: ✅ / ❌ [Specific issue]
- [ ] Link Correctness: ✅ / ❌ [Specific issue]
- [ ] Language Style: ✅ / ❌ [Specific issue]
- [ ] Frontmatter: ✅ / ❌ [Specific issue]
- [ ] MDX Component: ✅ / ❌ [Specific issue]

## 💡 Recommendations

[List specific modification suggestions if compliance issues are found]

---

**Should I modify the document according to the above suggestions? Please confirm.**
```

**Branching Logic**:
- **User Confirms**: Proceed to modify the document.
- **User Rejects/Partial Adoption**: Respect the user's decision and proceed with explanations.
- **User Provides New Feedback**: Return to step 0.1 for re-analysis.

---

## Phase 1: Architecture Analysis

### Step 1: Read Requirement Documents
Understand the functional requirements or original documents:
1. Extract core information from requirements or PRDs.
2. Identify scope (simple vs. complex multi-functional).
3. Clarify the target audience (DevOps, Developers, Admins, etc.).

### Step 2: Analyze Existing Document Structure (⚠️ Critical)
Search the target repository's structure to evaluate if adjustments are needed:

1. **Cross-Verify with Multiple Keywords** (to avoid keyword traps):
   ```bash
   grep -r "keyword1" /path/to/docs/ --include="*.mdx" -l
   grep -r "keyword2" /path/to/docs/ --include="*.mdx" -l
   ```
   **Example**: If the requirement is "Application Backup," search for `backup application`, `backup policy`, and `PVC backup`. Avoid concluding based on a single keyword like `velero`.

2. **Verify Functional Alignment**: Read found documents to ensure the functional domain matches the requirements.
3. **Assess Document Quality**: Check for compliance with naming, metadata, and structure.
4. **Determine Structural Adjustments**: Decide whether to create new files, split complex files, or merge related ones.

### Step 3: Decide Execution Plan (⚠️ Critical)
Formulate an execution plan based on complexity and existing status:

#### 3.1 Modify vs. Create Decision Tree
```text
Requirement Type:
├─ UI Form Field Enhancement / Parameter Added → Modify Existing Document
├─ New Functional Capability → Create New Document
│  ├─ Feature Intro → function doc
│  ├─ Scenario-based Guide → howto doc
│  └─ Conceptual Explanation → concept doc
└─ Scope Assessment:
   ├─ Simple/Single Function → Single HowTo or Function doc
   ├─ Complex/Multi-functional → Split into multiple docs (intro + howto + concept)
```

**Explain your analysis and proposed plan to the user and wait for confirmation before continuing.**

---

## Phase 2: Document Generation

### Step 4: Load the Corresponding Template
Load the template based on the determined document type (path relative to `SKILL.md`):
- `templates/howto-template.mdx`
- `templates/function-template.mdx`
- (etc.)

### Step 5: Explicitly Load Core Specifications
**Before generating content, you MUST explicitly read the following rules**:
- **rules/metadata-rules.md** (Frontmatter rules)
- **rules/language-style.md** (Tone and style)
- **rules/content-elements.md** (Lists, tables, links, code blocks)
- **rules/core-conventions.md** (Naming, static resources, RAG optimization)

**Load As Needed**:
- **rules/mdx-components.md** (Doom components)
- **rules/terminology-guide.md** (Standardized translations)
- **rules/terminology-consistency.md** (K8s/OpenShift official standards)

### Step 6: Example-Driven Learning (RAG)
**Crucial**: Do not memorize all component parameters. Use `grep` to retrieve real-world use cases and mimic them.
1. **Ask the user** for the current documentation repository path.
2. **Search for examples** in the specified path: `grep -r "<Tabs" <path> --include="*.mdx" -A 5`.
3. If no examples are found, ask for permission to check open-source reference repositories (e.g., `alauda/acp-docs`).

**Trust Hierarchy**:
1. 🥇 **Highest**: Real use cases in the user's repository.
2. 🥈 **Medium**: Open-source reference repositories (with authorization).
3. 🥉 **Lowest**: Built-in rule documents in this skill.

### Step 7: Terminology Retrieval
Adhere to `rules/terminology-consistency.md`: **Avoid inventing new terms**. Prioritize Kubernetes and OpenShift official standards. Use `rules/terminology-guide.md` for standardized translations and to avoid "bad cases."

### Step 8: Document Generation
Generate the complete document, ensuring:
- **Metadata Integrity**: Correct `weight`, `author`, `category`, and `queries`.
- **Structural Completeness**: Follow the template without removing mandatory nodes.
- **Correct Component Usage**: Use `<Overview />`, `<Term />`, `<Directive />`, and `<Steps />` properly.
- **Directive Control**: Ensure `:::` directives do not exceed 3-4 per document.

### Step 9: Self-Verification
After generation, perform:
- [ ] **Format Check**: Frontmatter, title levels, MDX syntax.
- [ ] **Content Check**: Consistent terminology, directive count control, actionable steps.
- [ ] **Link Check**: Correct relative paths, anchor formats, and `ExternalSiteLink` usage.
- [ ] **Language Check**: Objective tone, context provided, no slang.

---

## Core Principles

1. **English First**: Ensure the correctness and readability of the English version.
2. **CLI First**: Prioritize command-line operation instructions.
3. **Terminology Consistency**: Avoid inventing terms. Refer to `rules/terminology-guide.md`.
4. **Safety Alerts**: Use `<Directive type="danger">` or `:::danger` for risky operations.
5. **Maintainability**: Prefer ConfigMap for configuration suggestions.

---

## Output Format

After generation, output in the following format:

```markdown
## 📋 Documentation Analysis Results

**Requirement Type**: [Simple/Complex]
**Recommended Doc Type**: [howto/concept/function/etc.]
**Execution Plan**: [Create/Modify/Split/Merge]

## 📄 Generated Document

[Full MDX Content]

## ✅ Verification Results

- [x] Format check passed
- [x] Content check passed
- [x] Link check passed
- [x] Language check passed

## 💡 Suggestions

[Any architectural or content adjustment suggestions]
```
