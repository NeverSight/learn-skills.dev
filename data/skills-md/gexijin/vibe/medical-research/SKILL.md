---
name: medical-research
description: Retrieves scientific papers from PubMed and creates plain-language research summaries. Use when users ask about medical research, scientific studies, clinical trials, disease treatments, or want to understand recent scientific literature on any biomedical topic.
---

# Medical Research

## Purpose

This Skill retrieves scientific papers from PubMed and creates accessible, plain-language summaries of current research on any biomedical or life sciences topic. It bridges the gap between complex scientific literature and general understanding.

## When to Use This Skill

Automatically activate when users:
- Ask about scientific research on medical topics (e.g., "What's the latest on Alzheimer's treatment?")
- Want to understand current studies on diseases or conditions
- Request information about clinical trials or treatment approaches
- Mention specific research areas (immunotherapy, gene therapy, drug development)
- Ask questions like "summarize research on..." or "what does research say about..."
- Need to understand scientific consensus on health topics

## Instructions

When generating a research summary, follow these steps:

### 1. Identify the Research Query

- Accept natural language queries (e.g., "immunotherapy for breast cancer")
- Clarify if the topic is too broad (e.g., "cancer" → suggest narrowing to specific type)
- Verify spelling of medical terms
- If ambiguous, ask for clarification before proceeding

### 2. Retrieve Scientific Papers

Use the skill's built-in `pubmed_search.py` script located in `.claude/skills/medical-research/`:

```bash
python3 .claude/skills/medical-research/pubmed_search.py "your search query"
```

- Default retrieves 10 most recent papers
- For comprehensive summaries, consider increasing `max_results` in the script
- Capture paper details: titles, authors, abstracts, PMIDs, publication dates

### 3. Analyze and Synthesize Findings

Review the retrieved papers and identify:

1. **Main Research Themes**
   - What are the major topics being studied?
   - What questions are researchers trying to answer?
   - What approaches or methods are common?

2. **Key Findings**
   - What are the main discoveries or results?
   - What treatments or interventions show promise?
   - What mechanisms are being investigated?

3. **Clinical Implications**
   - How might this research affect patient care?
   - What are practical applications?
   - What changes to treatment guidelines might result?

4. **Challenges and Limitations**
   - What problems remain unsolved?
   - What resistance mechanisms exist?
   - What gaps in knowledge persist?

5. **Emerging Directions**
   - What new approaches are being developed?
   - What future research is needed?
   - What technologies are being applied?

### 4. Write Plain-Language Summary

Structure the summary for general audience understanding:

```markdown
# Research Summary: [Topic]

**Search Query:** [exact query used]
**Papers Found:** [total count]
**Papers Reviewed:** [number analyzed]
**Date:** [YYYY-MM-DD]

## Overview

[2-3 paragraphs explaining what this research area is about and why it matters. Use simple language, define medical terms, provide context for non-experts.]

## Key Research Themes

### Theme 1: [Name]
[Description in plain language]
- Key finding 1
- Key finding 2
- Why it matters

### Theme 2: [Name]
[Description in plain language]
- Key finding 1
- Key finding 2
- Why it matters

[Continue for major themes...]

## What This Means for Patients/Treatment

[Plain language explanation of clinical significance]
- Practical implication 1
- Practical implication 2
- Timeline for real-world impact (if applicable)

## Challenges and Open Questions

[What problems remain, explained simply]
- Challenge 1
- Challenge 2
- What researchers are working on next

## Key Terminology

[Define 3-5 important terms used in the research]
- **Term 1**: Plain language definition
- **Term 2**: Plain language definition

## Selected Recent Papers

[List 3-5 most significant papers with brief descriptions]

1. **[Paper Title]** (PMID: [number], [Year])
   - Authors: [First 3 et al.]
   - Key contribution: [1-2 sentences]
   - [PubMed URL]

## Summary

[2-3 paragraphs pulling it all together, highlighting the current state of research and future directions]

---

*This summary is based on scientific literature available in PubMed and is intended for educational purposes. It does not constitute medical advice.*
```

### 5. Save the Summary

- Automatically save as markdown file
- Use filename format: `Research_Summary_{Topic}_{YYYY-MM-DD}.md`
- Replace spaces in topic with underscores
- Place in current working directory
- Confirm file location to user

## Quality Guidelines

### Content Standards

- **Accessibility**: Write at a 10th-grade reading level
- **Accuracy**: Faithfully represent research findings; don't oversimplify to the point of distortion
- **Balance**: Include both promising developments and challenges
- **Currency**: Focus on papers from the last 1-2 years when possible
- **Context**: Explain why research matters and how it fits into bigger picture
- **Clarity**: Define medical/scientific terms; use analogies when helpful

### Language Guidelines

**Do:**
- Use active voice ("Researchers found..." not "It was found...")
- Define abbreviations on first use (e.g., "TNBC (triple-negative breast cancer)")
- Use concrete examples
- Explain mechanisms in simple terms
- Provide context for numbers and statistics
- Use analogies to explain complex concepts

**Don't:**
- Use jargon without explanation
- Oversimplify to the point of inaccuracy
- Make claims stronger than the research supports
- Provide medical advice
- Use passive voice excessively
- Assume prior knowledge of biology/medicine

### Credibility Standards

- **Objectivity**: Present findings without bias
- **Accuracy**: Cite specific PMIDs and paper details
- **Transparency**: Note when information is limited or preliminary
- **Disclaimers**: Always include educational/non-medical-advice disclaimer
- **Dates**: Include publication years to show currency

## Examples

### Example 1: Treatment Research

**User request**: `Summarize research on immunotherapy for melanoma`

**Expected behavior**:
1. Run: `python3 .claude/skills/medical-research/pubmed_search.py "immunotherapy melanoma"`
2. Analyze ~10 recent papers
3. Identify themes: resistance mechanisms, combination therapies, biomarkers
4. Write plain-language summary explaining immune checkpoint inhibitors, how they work, current challenges
5. Save as `Research_Summary_Immunotherapy_Melanoma_2025-12-13.md`

### Example 2: Disease Mechanism

**User request**: `What does research say about Alzheimer's disease causes?`

**Expected behavior**:
1. Activate Skill automatically
2. Run: `python3 .claude/skills/medical-research/pubmed_search.py "Alzheimer's disease pathogenesis"`
3. Synthesize findings on amyloid, tau, inflammation, genetic factors
4. Explain competing theories in accessible language
5. Highlight controversies and ongoing debates
6. Save comprehensive summary

### Example 3: Emerging Technology

**User request**: `Tell me about CRISPR gene therapy research`

**Expected behavior**:
1. Run: `python3 .claude/skills/medical-research/pubmed_search.py "CRISPR gene therapy clinical trials"`
2. Focus on clinical applications, safety, efficacy
3. Explain CRISPR technology simply (e.g., "molecular scissors that can edit DNA")
4. Include specific examples of diseases being treated
5. Address ethical considerations if prominent in literature
6. Save summary with examples

## Best Practices

### Do's

✓ Start with broad overview before diving into details
✓ Use subheadings to break up long sections
✓ Include "Key Terminology" section for important terms
✓ Provide specific examples from papers
✓ Explain statistical significance in plain language
✓ Note when findings are preliminary or need replication
✓ Connect research to real-world impact

### Don'ts

✗ Don't recommend specific treatments or medications
✗ Don't use unexplained acronyms (EGFR, VEGF, etc.)
✗ Don't ignore negative findings or failures
✗ Don't exaggerate promises ("cure for cancer")
✗ Don't skip the educational disclaimer
✗ Don't assume readers have science background
✗ Don't make summary too technical

## Handling Edge Cases

### Few or No Papers Found

If PubMed returns few results:
```
The search for "[query]" returned only [N] papers. This may indicate:
1. Very new or emerging research area
2. Query may need refinement
3. Limited research on this specific topic

Would you like me to:
- Try a broader search term?
- Search for related concepts?
- Proceed with available papers?
```

### Highly Technical Results

If papers are extremely technical:
```
Note: This is a highly specialized research area. I've translated
the technical findings into accessible language, but some complexity
is unavoidable. Key terms are defined in the "Key Terminology" section.
```

### Controversial Topics

For topics with conflicting research:
```
## Research Perspectives

Current research shows differing viewpoints:

**Perspective 1**: [Explanation with supporting papers]
**Perspective 2**: [Alternative view with supporting papers]

The scientific community is actively investigating these questions,
and consensus may emerge as more evidence accumulates.
```

### Outdated Research

If most papers are older than 2 years:
```
Note: The most recent papers in this search are from [year]. This
may indicate:
- Established research area with stable findings
- Reduced current research activity
- Search terms may benefit from updating

The summary focuses on foundational findings that remain current.
```

## Technical Requirements

### Tools to Use

- **Bash**: Run the `pubmed_search.py` script
- **Read**: Optionally read papers or abstracts if more detail needed
- **Write**: Save the completed summary to markdown file
- **WebFetch** (optional): Retrieve full papers from PubMed if abstracts insufficient

### Search Strategy

1. **Start specific**: Use precise medical terms
2. **Iterate if needed**: Broaden or narrow based on results
3. **Check paper count**: Aim for 10-20 papers for comprehensive summary
4. **Verify relevance**: Ensure retrieved papers match the query
5. **Note search date**: Document when search was performed

### Script Modifications

If needed, users can modify `pubmed_search.py`:
- Increase `max_results` for more comprehensive reviews
- Update `Entrez.email` with their email address
- Adjust abstract length display

## File Output Specifications

### Default Format: Markdown

```
Filename: Research_Summary_{Topic}_{YYYY-MM-DD}.md
Location: Current working directory
Encoding: UTF-8
Sections: All sections from template
```

### Content Requirements

- Minimum 800 words for comprehensive topics
- At least 3 major themes identified
- 3-5 key terms defined
- 3-5 papers highlighted
- Include all template sections

## Quality Checklist

Before saving, verify:

- [ ] Summary is accessible to non-scientists
- [ ] Medical terms are defined
- [ ] Key findings are accurate to source papers
- [ ] Clinical implications explained
- [ ] Challenges and limitations included
- [ ] Recent papers cited with PMIDs
- [ ] Educational disclaimer included
- [ ] Filename follows format
- [ ] All sections complete
- [ ] Free of unexplained jargon

## Related Resources

- **PubMed**: https://pubmed.ncbi.nlm.nih.gov/
- **Biopython Entrez Documentation**: For script customization
- **MeSH Terms**: Medical Subject Headings for refined searches
- **NIH Plain Language**: For accessibility guidelines

---

**Version**: 1.0
**Last Updated**: December 2025
**Maintained By**: Vibe Project
