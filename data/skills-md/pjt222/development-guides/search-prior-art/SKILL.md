---
name: search-prior-art
description: >
  Search for prior art relevant to a specific invention or patent claim.
  Covers patent literature, non-patent literature (academic papers, products,
  open source), defensive publications, and standard-essential patents.
  Use when evaluating whether an invention is novel and non-obvious before
  filing, challenging the validity of an existing patent, supporting a
  freedom-to-operate analysis, documenting a defensive publication, or
  responding to a patent office action questioning novelty or obviousness.
license: MIT
allowed-tools: Read Grep Glob WebFetch WebSearch
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: intellectual-property
  complexity: intermediate
  language: natural
  tags: intellectual-property, prior-art, patents, novelty, obviousness, invalidity, fto
---

# Search Prior Art

Conduct a structured prior art search to find publications, patents, products, or disclosures that predate a specific invention. Used to assess patentability (can this be patented?), challenge validity (should this patent have been granted?), or establish freedom-to-operate (is this design covered by existing rights?).

## When to Use

- Evaluating whether an invention is novel and non-obvious before filing a patent application
- Challenging the validity of an existing patent by finding prior art the examiner missed
- Supporting a freedom-to-operate analysis by finding prior art that limits a blocking patent's scope
- Documenting a defensive publication to prevent others from patenting a concept
- Responding to a patent office action that questions novelty or obviousness

## Inputs

- **Required**: Invention description (what it does, how it works, what problem it solves)
- **Required**: Search purpose (patentability, invalidity, FTO, defensive)
- **Required**: Critical date (filing date of the patent application, or invention date for prior art)
- **Optional**: Known related patents or publications
- **Optional**: Technology classification codes (IPC, CPC)
- **Optional**: Key inventors or companies in the field

## Procedure

### Step 1: Decompose the Invention into Searchable Elements

Break the invention into its constituent technical features.

1. Read the invention description (or patent claims if searching against an existing patent)
2. Extract the **essential elements** — each independent technical feature:
   - What components does it have?
   - What steps does the process follow?
   - What technical effect does it achieve?
   - What problem does it solve and how?
3. Identify the **novel combination** — what makes this different from the known art:
   - Is it a new element added to known elements?
   - Is it a new combination of known elements?
   - Is it a known element applied in a new field?
4. Generate search terms for each element:
   - Technical terms, synonyms, and abbreviations
   - Broader and narrower terms (hierarchy)
   - Alternative descriptions of the same concept
5. Document the **Search Map**: elements, terms, and relationships

```
Search Map Example:
+------------------+-----------------------------------+-----------+
| Element          | Search Terms                      | Priority  |
+------------------+-----------------------------------+-----------+
| Attention layer  | attention mechanism, self-         | High      |
|                  | attention, multi-head attention    |           |
| Sparse routing   | mixture of experts, sparse MoE,   | High      |
|                  | top-k routing, expert selection    |           |
| Training method  | knowledge distillation, teacher-   | Medium    |
|                  | student, progressive training      |           |
+------------------+-----------------------------------+-----------+
```

**Expected:** A complete decomposition with search terms for each element. The novel combination is identified — this is what the search must either find (to invalidate) or confirm is absent (to support novelty).

**On failure:** If the invention is too abstract to decompose, ask for a more specific description. If the claims are unclear, focus on the broadest reasonable interpretation of each claim element.

### Step 2: Search Patent Literature

Search patent databases systematically.

1. Construct queries combining element terms:
   - Search each element individually first (broad)
   - Then combine elements to find closer art (narrow)
   - Use classification codes to filter by technology area
2. Search multiple databases:
   - **Google Patents**: Good for full-text search, free, large corpus
   - **USPTO PatFT/AppFT**: US patents and applications, official source
   - **Espacenet**: European patents, excellent classification search
   - **WIPO Patentscope**: PCT applications, global coverage
3. Apply date filters:
   - Prior art must predate the **critical date** (filing date or priority date)
   - Include publications up to 1 year before filing (grace period varies by jurisdiction)
4. For each relevant result, record:
   - Document number, title, filing date, publication date
   - Which elements it discloses (map to Search Map)
   - Whether it discloses the novel combination
5. Classify results by relevance:
   - **X reference**: Discloses the invention alone (anticipation)
   - **Y reference**: Discloses key elements, combinable with other references (obviousness)
   - **A reference**: Background art, defines the general state of the art

**Expected:** A classified list of patent references mapped to the invention's elements. X references (if found) are showstoppers for novelty. Y references are the building blocks for obviousness arguments.

**On failure:** If no relevant patent art is found, this doesn't mean the invention is novel — non-patent literature (Step 3) may contain the critical reference. Absence in one database doesn't mean absence everywhere.

### Step 3: Search Non-Patent Literature

Search academic papers, products, open source, and other non-patent disclosures.

1. **Academic literature**:
   - Google Scholar, arXiv, IEEE Xplore, ACM Digital Library
   - Search using the same terms from Step 1
   - Conference papers and workshop proceedings often predate patent filings
2. **Products and commercial disclosures**:
   - Product documentation, user manuals, marketing materials
   - Internet Archive (Wayback Machine) for date-verified web content
   - Trade publications and press releases
3. **Open source and code**:
   - GitHub, GitLab — search for implementations of the technical features
   - README files, documentation, and commit histories for date evidence
   - Software releases with version dates
4. **Standards and specifications**:
   - IEEE, IETF (RFCs), W3C, ISO standards
   - Standards-essential patents must be disclosed; search standard bodies' IP databases
5. **Defensive publications**:
   - IBM Technical Disclosure Bulletin
   - Research Disclosure journal
   - IP.com Prior Art Database
6. For each result, verify the **publication date** is before the critical date:
   - Web pages: use Wayback Machine for date evidence
   - Software: use release dates or commit timestamps
   - Papers: use publication date, not submission date

**Expected:** Non-patent references that complement the patent search. Academic papers and open-source code are often the most powerful prior art because they tend to describe technical details more explicitly than patents.

**On failure:** If non-patent literature is sparse, the technology may be primarily developed in corporate R&D (patent-heavy). Shift emphasis to patent literature and focus on the combination-based obviousness argument.

### Step 4: Analyze and Map Results

Evaluate how the collected prior art relates to the invention.

1. Create a **claim chart** mapping prior art to invention elements:

```
Claim Element vs. Prior Art Matrix:
+------------------+--------+--------+--------+--------+
| Element          | Ref #1 | Ref #2 | Ref #3 | Ref #4 |
+------------------+--------+--------+--------+--------+
| Element A        |   X    |   X    |        |   X    |
| Element B        |        |   X    |   X    |        |
| Element C        |   X    |        |   X    |        |
| Novel combo A+B+C|        |        |        |        |
+------------------+--------+--------+--------+--------+
X = element disclosed in this reference
```

2. Assess **novelty**: Does any single reference disclose all elements?
   - If yes → invention is anticipated (not novel)
   - If no → invention may be novel (proceed to obviousness)
3. Assess **obviousness**: Can a small number of references (2-3) be combined to cover all elements?
   - Is there motivation to combine? (would a skilled person see a reason to combine these?)
   - Do the references teach away from the combination? (suggest it wouldn't work?)
4. For **FTO searches**: Does the prior art narrow the blocking patent's claims?
   - Prior art that overlaps with the blocking patent's claims limits their enforceable scope
5. Document the analysis clearly with citation to specific passages

**Expected:** A clear claim chart showing which elements are covered by which references, with an assessment of novelty and obviousness. Each mapping cites specific passages or figures in the references.

**On failure:** If the claim chart shows gaps (elements not found in any prior art), those gaps represent the potentially novel aspects. Focus follow-up searches on those specific gaps.

### Step 5: Document and Deliver

Package the search results for their intended use.

1. Write the **Prior Art Search Report**:
   - Purpose and scope of the search
   - Search methodology (databases, queries, date ranges)
   - Results summary (number of references found, classification breakdown)
   - Top references with detailed analysis (claim charts)
   - Assessment: novelty, obviousness, and FTO implications
   - Limitations and recommendations for further search
2. Organize references:
   - Sorted by relevance (X references first, then Y, then A)
   - Each reference with full bibliographic data and access link
   - Key passages highlighted or extracted
3. Recommendations based on search purpose:
   - **Patentability**: File/don't file, suggested claim scope based on prior art gaps
   - **Invalidity**: Strongest combination of references, suggested legal argument
   - **FTO**: Risk level, design-around opportunities, licensing considerations
   - **Defensive**: Whether to publish as defensive disclosure based on white space found

**Expected:** A complete, well-organized search report that directly supports the intended decision. References are accessible and analysis is traceable.

**On failure:** If the search is inconclusive (no strong X or Y references, but some relevant background), state the conclusion clearly: "No anticipatory art found; closest art addresses elements A and B but not C. Recommend filing with claims emphasizing element C." Inconclusive is a valid and useful result.

## Validation Checklist

- [ ] Invention decomposed into distinct searchable elements
- [ ] Novel combination explicitly identified
- [ ] Patent databases searched (minimum 2 databases)
- [ ] Non-patent literature searched (academic + products + open source)
- [ ] All references predate the critical date (dates verified)
- [ ] Claim chart maps elements to references with passage citations
- [ ] Novelty and obviousness assessed with reasoning
- [ ] Results classified by relevance (X, Y, A references)
- [ ] Report includes methodology, limitations, and recommendations
- [ ] Search is reproducible (queries and databases documented)

## Common Pitfalls

- **Keyword tunnel vision**: Searching only exact terms misses synonyms and alternative descriptions. Use the term hierarchy from Step 1
- **Patent-only search**: Non-patent literature (papers, products, code) is often more explicit than patents. Don't skip Step 3
- **Date carelessness**: Prior art must predate the critical date. A brilliant reference from one day after the filing date is worthless
- **Ignoring foreign language art**: Major inventions may first appear in Chinese, Japanese, Korean, or German patent literature. Machine translation makes these searchable
- **Confirmation bias**: Searching to confirm novelty rather than searching to find invalidating art. The best search tries hardest to find the closest art
- **Stopping too early**: The first few results are rarely the best. Iterate search terms based on what early results reveal about the field's vocabulary

## Related Skills

- `assess-ip-landscape` — Broader landscape mapping that contextualizes specific prior art searches
- `review-research` — Literature review methodology overlaps significantly with prior art search
- `security-audit-codebase` — Systematic search methodology parallels (thoroughness, documentation, reproducibility)
