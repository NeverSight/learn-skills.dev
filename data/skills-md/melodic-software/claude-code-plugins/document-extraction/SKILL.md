---
name: document-extraction
description: Extract requirements from existing documents including PDFs, Word docs, meeting transcripts, specifications, and web content. Identifies requirement candidates, categorizes them, and outputs in pre-canonical format.
allowed-tools: Read, Glob, Grep, Write, Task, WebFetch
---

# Document Extraction Skill

Extract requirements from existing documentation sources for systematic requirement mining.

## When to Use This Skill

**Keywords:** extract requirements, document mining, PDF requirements, transcript analysis, parse document, existing documentation, legacy requirements, competitive analysis

Invoke this skill when:

- Mining requirements from existing documents
- Processing meeting transcripts for requirements
- Extracting requirements from competitor products
- Analyzing regulatory documents for compliance requirements
- Converting legacy documentation to structured requirements

## Supported Document Types

| Type | Extension | Extraction Method |
|------|-----------|------------------|
| Markdown | .md | Direct Read |
| Text | .txt | Direct Read |
| PDF | .pdf | Read tool (PDF support) |
| Word | .docx | Read tool |
| Web Page | URL | WebFetch tool |
| Meeting Notes | .md, .txt | Transcript patterns |
| Specification | .md, .docx | Requirement patterns |

## Extraction Workflow

### Step 1: Document Assessment

Analyze the document to determine extraction strategy:

```yaml
document_assessment:
  path: "{file path or URL}"
  type: "{detected document type}"
  size: "{approximate size}"
  structure:
    has_sections: true|false
    has_lists: true|false
    has_tables: true|false
  quality:
    formal_language: true|false
    clear_requirements: true|false
    needs_interpretation: true|false
```

### Step 2: Pattern Matching

Apply requirement detection patterns:

**Explicit Requirement Markers:**

```text
- "The system shall..."
- "The system must..."
- "Users should be able to..."
- "REQ-XXX:"
- Numbered requirements (1.1, 1.2, etc.)
```

**EARS Patterns:**

```text
- "When [trigger], the [system] shall [response]"
- "While [state], the [system] shall [behavior]"
- "Where [feature], the [system] shall [behavior]"
- "If [condition], then the [system] shall [response]"
```

**Implicit Requirement Indicators:**

```text
- "It is important that..."
- "We need..."
- "The goal is to..."
- "Users expect..."
- "Performance should..."
```

### Step 3: Requirement Extraction

For each identified requirement:

```yaml
extracted_requirement:
  id: REQ-{sequence}
  text: "{cleaned requirement statement}"
  source: document
  source_file: "{file path}"
  source_location: "{section/page/line}"
  original_text: "{exact text from document}"
  type: functional|non-functional|constraint|assumption
  confidence: high|medium|low
  extraction_method: explicit|pattern|inferred
  needs_review: true|false
  review_notes: "{why review needed}"
```

### Step 4: Categorization

Categorize extracted requirements:

```yaml
categories:
  functional:
    - features
    - behaviors
    - interactions
  non_functional:
    - performance
    - security
    - usability
    - reliability
    - scalability
  constraints:
    - technical
    - business
    - regulatory
  assumptions:
    - environmental
    - user_behavior
    - dependencies
```

### Step 5: Deduplication

Identify and merge duplicate requirements:

```yaml
deduplication:
  strategy: semantic_similarity
  threshold: 0.8
  action: merge|flag_for_review
  merged_requirements:
    - id: REQ-merged-001
      sources: [REQ-001, REQ-015]
      text: "{consolidated requirement}"
```

## Document-Specific Strategies

### Meeting Transcripts

```yaml
transcript_extraction:
  focus_on:
    - Action items
    - Decisions made
    - Requirements discussed
    - Concerns raised
  patterns:
    - "We decided that..."
    - "The requirement is..."
    - "Action item:"
    - "TODO:"
    - "Need to..."
  speaker_context:
    - Note who said what
    - Weight by speaker role
```

### Regulatory Documents

```yaml
regulatory_extraction:
  focus_on:
    - Mandatory requirements ("shall", "must")
    - Prohibited actions ("shall not", "must not")
    - Conditional requirements ("if...then")
  compliance_mapping:
    - Reference section numbers
    - Note effective dates
    - Track version/revision
```

### Competitor Analysis

```yaml
competitor_extraction:
  focus_on:
    - Feature descriptions
    - User capabilities
    - Unique selling points
  output:
    - Feature requirements
    - Differentiation opportunities
    - Gap identification
  confidence: low  # Based on external observation
```

### Legacy Specifications

```yaml
legacy_extraction:
  focus_on:
    - Existing requirements
    - System behaviors
    - Integration points
  modernization:
    - Update terminology
    - Convert to EARS format
    - Flag deprecated requirements
```

## Output Format

### Per-Document Output

```yaml
extraction_result:
  source:
    file: "{path or URL}"
    type: "{document type}"
    extraction_date: "{ISO-8601}"
    confidence: high|medium|low

  statistics:
    total_candidates: {number}
    extracted: {number}
    filtered: {number}
    needs_review: {number}

  requirements:
    - id: REQ-{number}
      text: "{requirement}"
      type: functional|non-functional|constraint
      source_location: "{section/page}"
      confidence: high|medium|low
      original_text: "{exact source text}"

  review_items:
    - requirement_id: REQ-{number}
      reason: "{why review needed}"
      suggestion: "{proposed action}"

  metadata:
    sections_processed: {number}
    extraction_patterns_used: ["{pattern names}"]
```

## Autonomy Levels

### Guided Mode

```yaml
guided_behavior:
  document_selection: Human selects
  extraction_strategy: AI suggests, human approves
  each_requirement: AI highlights, human confirms
  categorization: AI suggests, human validates
```

### Semi-Autonomous Mode

```yaml
semi_auto_behavior:
  document_selection: AI suggests priority, human approves list
  extraction_strategy: AI chooses autonomously
  requirements: AI extracts all, human reviews in batches
  categorization: AI categorizes, human spot-checks
```

### Fully Autonomous Mode

```yaml
full_auto_behavior:
  document_selection: AI processes all relevant
  extraction_strategy: AI optimizes per document
  requirements: AI extracts, deduplicates, categorizes
  output: Full extraction report for final review
```

## Quality Indicators

### High Confidence Extraction

- Explicit requirement markers ("shall", "must")
- EARS-pattern matches
- Numbered requirement lists
- Clear imperative statements

### Medium Confidence Extraction

- Implicit indicators ("should", "needs to")
- Context-dependent interpretation
- Partial pattern matches
- Requires domain knowledge

### Low Confidence Extraction

- Inferred from descriptions
- Narrative text interpretation
- Competitive analysis
- Assumptions based on context

## Delegation

For related tasks, delegate to:

- **gap-analysis**: Check extracted requirements for completeness
- **domain-research**: Research unfamiliar terms or concepts
- **elicitation-methodology**: Route back for technique selection

## Output Location

Save extraction results to:

```text
.requirements/{domain}/documents/DOC-{filename}-{timestamp}.yaml
```

## Related

- `elicitation-methodology` - Parent hub skill
- `gap-analysis` - Post-extraction completeness checking
- `interview-conducting` - Clarify extracted requirements with stakeholders
