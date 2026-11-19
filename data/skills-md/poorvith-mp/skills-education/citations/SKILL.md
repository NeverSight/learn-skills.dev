---
name: citations
last_reviewed: 2026-09-06
group: Research
description: >-
  Format citations and bibliographies in APA, MLA, Chicago, Harvard and IEEE with matching in-text
  forms. Use when formatting bibliographies in APA, MLA, Chicago, IEEE, or BibTeX.
---

# citations

## Core Philosophy
Citations are not bureaucratic formatting punishment; they are the provenance network of academic integrity. A citation provides an address for an idea, establishing an auditable chain of evidence that separates scholarly claims from unsourced assertion. Mismatched citation styles, broken in-text references, missing DOIs, and sloppy bibliography formatting instantly signal amateurism to peer reviewers and academic examiners. Mastering citations requires programmatic precision across the major style conventions: APA 7th, MLA 9th, Chicago 17th, Harvard, IEEE, and BibTeX.

---

## 4-Step Citation & Bibliography Pipeline

### Step 1: Style Guide Selection Matrix
1. **APA 7th Edition (American Psychological Association)**:
   - Social Sciences, Psychology, Education, Business.
   - Focus: Author-Date (`Smith, 2021`). Emphasizes publication recency.
2. **MLA 9th Edition (Modern Language Association)**:
   - Humanities, Literature, Cultural Studies, Art.
   - Focus: Author-Page (`Smith 42`). Emphasizes exact textual location.
3. **Chicago 17th Edition**:
   - History, Fine Arts, Publishing.
   - Two sub-systems:
     - *Notes & Bibliography*: Numbered footnotes/endnotes + comprehensive bibliography.
     - *Author-Date*: In-text parenthetical citations.
4. **IEEE (Institute of Electrical and Electronics Engineers)**:
   - Computer Science, Electrical Engineering, Telecommunications.
   - Focus: Bracketed numeric citation order `[1]`, `[2]`.
5. **Harvard Referencing**:
   - Widely used across UK, Commonwealth universities, and biological sciences.
   - Focus: Author-Date variant (`Smith 2021, p. 42`).

### Step 2: Multi-Author Rules Across Styles
1. **Two Authors**:
   - APA: `(Kahneman & Tversky, 1979)`
   - MLA: `(Kahneman and Tversky 112)`
   - IEEE: `[1]`
2. **Three or More Authors**:
   - APA 7th: Truncate immediately to first author + *et al.* in all citations: `(Vaswani et al., 2017)`.
   - MLA 9th: `(Vaswani et al. 5988)`.
   - Chicago: `Vaswani et al., "Attention Is All You Need,"...`

### Step 3: Digital Object Identifiers (DOIs) & URLs
1. **Standard DOI Formatting**:
   - Always format DOIs as live HTTPS URLs: `https://doi.org/10.xxxx/xxxxx`. Never write `doi: 10.xxxx` or `DOI: https://...`.
2. **Retrieval Dates**:
   - Only include "Retrieved Month DD, YYYY" if the source content is inherently dynamic with no archived version (e.g. live Wikipedia page or dashboard).

### Step 4: BibTeX & LaTeX Integration
1. **BibTeX Key Hygiene**:
   - Use deterministic keys: `[Author][Year][FirstKeyword]` (e.g. `vaswani2017attention`).
   - Protect capital letters in title strings using curly braces `{BERT}: {Pre-training} of {Deep} {Bidirectional} {Transformers}`.

---

## Deliverable Format: Canonical Multi-Style Citation Reference Sheet

### Reference Item:
- **Authors**: Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, Illia Polosukhin
- **Year**: 2017
- **Title**: Attention Is All You Need
- **Venue**: Advances in Neural Information Processing Systems (NeurIPS), Volume 30, pages 5998–6008.

### Formatted Outputs:

#### 1. APA 7th Edition:
- **In-Text**: (Vaswani et al., 2017) or Vaswani et al. (2017)
- **Reference List**:
  Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., & Polosukhin, I. (2017). Attention is all you need. *Advances in Neural Information Processing Systems*, *30*, 5998–6008.

#### 2. MLA 9th Edition:
- **In-Text**: (Vaswani et al. 6001)
- **Works Cited**:
  Vaswani, Ashish, et al. "Attention Is All You Need." *Advances in Neural Information Processing Systems*, vol. 30, 2017, pp. 5998–6008.

#### 3. Chicago 17th Edition (Notes & Bibliography):
- **Footnote**: 1. Ashish Vaswani et al., "Attention Is All You Need," *Advances in Neural Information Processing Systems* 30 (2017): 6001.
- **Bibliography**:
  Vaswani, Ashish, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, and Illia Polosukhin. "Attention Is All You Need." *Advances in Neural Information Processing Systems* 30 (2017): 5998–6008.

#### 4. IEEE Standard:
- **In-Text**: [1]
- **References**:
  [1] A. Vaswani *et al.*, "Attention is all you need," in *Adv. Neural Inf. Process. Syst.*, vol. 30, 2017, pp. 5998–6008.

#### 5. BibTeX:
```bibtex
@inproceedings{vaswani2017attention,
  author    = {Vaswani, Ashish and Shazeer, Noam and Parmar, Niki and Uszkoreit, Jakob and Jones, Llion and Gomez, Aidan N. and Kaiser, {\L}ukasz and Polosukhin, Illia},
  title     = {Attention Is All You Need},
  booktitle = {Advances in Neural Information Processing Systems},
  volume    = {30},
  pages     = {5998--6008},
  year      = {2017}
}
```

---

## Worked Example: Reconciling Mixed Citation Styles in a Research Paper

- **Problem**: A student submitting a paper to an IEEE conference mixed APA author-date parenthetical citations `(Shannon, 1948)` with un-numbered MLA bibliographies, triggering an immediate desk rejection.
- **Remediation**:
  1. Converted all in-text author citations into chronological numerical bracketed references `[1]`, `[2]`.
  2. Formatted author initials preceding last names (e.g. `C. E. Shannon`).
  3. Ordered the reference list by numerical appearance rather than alphabetical author sorting.
- **Result**: Resubmitted manuscript passed editorial technical screening with zero formatting flags.

---

## Verification Checklist

- [ ] Style guide adheres strictly to the publication target (APA 7th, MLA 9th, Chicago, IEEE, Harvard).
- [ ] In-text citation keys match the reference bibliography 1-to-1 without orphaned entries.
- [ ] DOIs formatted as valid HTTPS hyperlinks (`https://doi.org/...`).
- [ ] Multi-author truncation rules (*et al.*) applied accurately for the specific edition.
- [ ] Capitalization in BibTeX titles protected with `{Braces}` for proper rendering in LaTeX.

---

## Anti-Patterns

- **Mixing Styles Arbitrarily**: Using APA author-date parentheticals in the body while numbering references IEEE-style in the bibliography.
- **Missing In-Text Addresses**: Citing an entire 800-page textbook in the text without providing specific page numbers when directly quoting or referencing an exact theorem.
- **Raw Unformatted URLs**: Pasting naked search engine query links instead of stable DOIs or canonical permalinks.
