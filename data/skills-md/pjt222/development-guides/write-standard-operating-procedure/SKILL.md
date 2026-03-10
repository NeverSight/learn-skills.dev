---
name: write-standard-operating-procedure
description: >
  Write a GxP-compliant Standard Operating Procedure (SOP). Covers regulatory
  SOP template structure (purpose, scope, definitions, responsibilities,
  procedure, references, revision history), approval workflow design,
  periodic review scheduling, and operational procedures for system use. Use
  when a new validated system requires operational procedures, when existing
  informal procedures need formalisation, when an audit finding cites missing
  procedures, when a change control triggers SOP updates, or when periodic
  review identifies outdated procedural content.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: compliance
  complexity: intermediate
  language: multi
  tags: gxp, sop, procedure, documentation, compliance, quality-management
---

# Write Standard Operating Procedure

Create a GxP-compliant Standard Operating Procedure that provides clear, auditable instructions for regulated activities.

## When to Use

- A new validated system requires operational procedures
- Existing procedures need formalisation into SOP format
- An audit finding cites missing or inadequate procedures
- A change control triggers SOP updates
- Periodic review identifies outdated procedural content

## Inputs

- **Required**: Process or system the SOP covers
- **Required**: Regulatory context (GMP, GLP, GCP, 21 CFR Part 11, EU Annex 11)
- **Required**: Target audience (roles that will follow this SOP)
- **Optional**: Existing informal procedures, work instructions, or training materials
- **Optional**: Related SOPs that interface with this procedure
- **Optional**: Audit findings or regulatory observations driving the SOP creation

## Procedure

### Step 1: Assign Document Control Metadata

```markdown
# Standard Operating Procedure
## Document ID: SOP-[DEPT]-[NNN]
## Title: [Descriptive Title of the Procedure]

| Field | Value |
|-------|-------|
| Document ID | SOP-[DEPT]-[NNN] |
| Version | 1.0 |
| Effective Date | [YYYY-MM-DD] |
| Review Date | [YYYY-MM-DD + review period] |
| Department | [Department name] |
| Author | [Name, Title] |
| Reviewer | [Name, Title] |
| Approver | [Name, Title] |
| Classification | [GxP-Critical / GxP-Supporting] |
| Supersedes | [Previous SOP ID or "N/A — New"] |
```

**Expected:** Every SOP has a unique ID following the organisation's document numbering convention.
**On failure:** If no numbering convention exists, establish one before proceeding: [TYPE]-[DEPT]-[3-digit sequential].

### Step 2: Write the Purpose and Scope

```markdown
### 1. Purpose
This SOP defines the procedure for [specific activity] to ensure [regulatory objective].

### 2. Scope
**In scope:**
- [System, process, or activity covered]
- [Applicable departments or roles]
- [Specific regulatory requirements addressed]

**Out of scope:**
- [Related activities covered by other SOPs — reference them]
- [Systems or departments not covered]
```

**Expected:** Purpose is one to two sentences. Scope clearly defines boundaries.
**On failure:** If scope overlaps with an existing SOP, either reference the existing SOP for the overlapping section or revise both SOPs to eliminate the overlap.

### Step 3: Define Terms and Abbreviations

```markdown
### 3. Definitions and Abbreviations

| Term | Definition |
|------|-----------|
| ALCOA+ | Attributable, Legible, Contemporaneous, Original, Accurate + Complete, Consistent, Enduring, Available |
| CCB | Change Control Board |
| GxP | Good [Manufacturing/Laboratory/Clinical] Practice — umbrella for all regulated quality standards |
| SOP | Standard Operating Procedure |
| [Add terms specific to this SOP] | [Definition] |
```

**Expected:** Every abbreviation and technical term used in the SOP is defined.
**On failure:** If a term is ambiguous or domain-specific, consult the organisation's glossary or the relevant regulatory guidance for the authoritative definition.

### Step 4: Assign Responsibilities

```markdown
### 4. Responsibilities

| Role | Responsibilities |
|------|-----------------|
| System Owner | Ensure SOP compliance, approve changes, conduct periodic review |
| System Administrator | Execute daily operations per this SOP, report deviations |
| Quality Assurance | Review SOP for regulatory compliance, approve new versions |
| End Users | Follow procedures as written, report issues to system administrator |
| Training Coordinator | Ensure all affected personnel are trained before SOP effective date |
```

**Expected:** Every action in the Procedure section can be traced to a responsible role.
**On failure:** If a procedural step has no assigned role, it is an orphaned responsibility. Assign an owner before the SOP is approved.

### Step 5: Write the Procedure Section

This is the core of the SOP. Write step-by-step instructions:

```markdown
### 5. Procedure

#### 5.1 [First Major Activity]
1. [Action verb] [specific instruction]. Reference: [form, system screen, tool].
2. [Action verb] [specific instruction].
   - If [condition], then [action].
   - If [alternative condition], then [alternative action].
3. [Action verb] [specific instruction].
4. Record the result in [form/system/log].

#### 5.2 [Second Major Activity]
1. [Action verb] [specific instruction].
2. Verify [specific criterion].
3. If verification fails, initiate [deviation procedure — reference SOP-XXX].

#### 5.3 Deviation Handling
1. If any step cannot be performed as written, STOP and document the deviation.
2. Notify [role] within [timeframe].
3. Complete Deviation Form [form reference].
4. Do not proceed until [role] provides disposition.
```

Writing rules for GxP SOPs:
- Start each step with an action verb (verify, record, enter, approve, notify)
- Be specific enough to be followed by a trained operator without interpretation
- Include decision points with clear criteria for each path
- Reference exact form names, system screens, or tool identifiers
- Include hold points where work must stop pending approval or verification

**Expected:** A trained person unfamiliar with the specific process could follow these steps correctly.
**On failure:** If subject matter experts say the procedure is ambiguous, add detail or break the step into sub-steps. Ambiguity in SOPs is a recurring audit finding.

### Step 6: Add References, Attachments, and Revision History

```markdown
### 6. References
| Document ID | Title |
|-------------|-------|
| SOP-QA-001 | Document Control |
| SOP-IT-015 | User Access Management |
| [Regulation reference] | [e.g., 21 CFR Part 11] |

### 7. Attachments
| Attachment | Description |
|-----------|-------------|
| Form-001 | [Form name and purpose] |
| Template-001 | [Template name and purpose] |

### 8. Revision History
| Version | Date | Author | Change Description |
|---------|------|--------|--------------------|
| 1.0 | [Date] | [Name] | Initial release |
```

**Expected:** All referenced documents are accessible to users, and revision history starts from version 1.0.
**On failure:** If referenced documents do not exist yet, either create them or remove the reference and note the gap in the SOP review.

### Step 7: Route for Review and Approval

```markdown
### Approval Signatures

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Author | [Name] | | |
| Technical Reviewer | [Name] | | |
| QA Reviewer | [Name] | | |
| Approver (Department Head) | [Name] | | |

### Training Requirement
All personnel listed in Section 4 must complete training on this SOP before the effective date. Training must be documented in the training management system.

### Periodic Review
This SOP must be reviewed at least every [2 years / annually] or when triggered by:
- Change control affecting the covered process or system
- Audit finding related to the covered process
- Regulatory guidance update affecting the covered requirements
```

**Expected:** SOP is reviewed by a subject matter expert and approved by quality before becoming effective.
**On failure:** If the approval workflow is delayed, the effective date must be pushed back. An SOP cannot be effective without completed approvals.

## Validation

- [ ] Document ID follows the organisation's numbering convention
- [ ] Purpose is specific and concise (1-2 sentences)
- [ ] Scope clearly defines in-scope and out-of-scope boundaries
- [ ] All abbreviations and technical terms are defined
- [ ] Every role in the Responsibilities section maps to procedure steps
- [ ] Procedure steps start with action verbs and are specific enough to follow without interpretation
- [ ] Decision points have clear criteria for each path
- [ ] Deviation handling is defined
- [ ] All referenced documents exist and are accessible
- [ ] Revision history is complete from version 1.0
- [ ] Approval signatures include author, reviewer, and approver
- [ ] Periodic review schedule is defined

## Common Pitfalls

- **Too vague**: "Ensure data quality" is not a procedural step. "Verify that all 15 fields in Form-001 are populated and within range per Appendix A" is.
- **Too detailed**: Including troubleshooting for every possible error makes the SOP unreadable. Reference a separate work instruction for complex troubleshooting.
- **No deviation handling**: Every SOP must define what to do when the procedure cannot be followed as written. Silence on deviations implies no deviations are possible.
- **Effective before training**: An SOP that is effective before all users are trained creates an immediate compliance gap.
- **Orphaned SOPs**: SOPs that are never reviewed become outdated and unreliable. Set review dates and track them in the document control system.

## Related Skills

- `design-compliance-architecture` — identifies which systems and processes need SOPs
- `manage-change-control` — triggers SOP updates when processes change
- `design-training-program` — ensures users are trained on new and updated SOPs
- `conduct-gxp-audit` — audits assess SOP adequacy and adherence
- `write-validation-documentation` — SOPs and validation docs share approval workflows
