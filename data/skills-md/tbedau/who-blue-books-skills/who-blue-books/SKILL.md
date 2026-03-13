---
name: who-blue-books
description: |
  Look up, study, and learn WHO Classification of Tumours (Blue Books) content.
  Three workflows: (1) Lookup — answer questions about diagnostic criteria,
  differentials, comparisons, and classification; (2) Study Plan — generate a
  structured study plan for a Blue Book with thematic clusters; (3) Deep Dive —
  produce comprehensive teaching reviews on any pathology topic. Use when: the
  user asks about WHO tumour classification, Blue Books, or pathology; wants to
  look up diagnostic criteria, differentials, immunophenotype, or molecular
  features; asks to compare tumour types or work through a differential;
  mentions tumour abbreviations (GIST, DLBCL, RCC, PTC, HCC, IDC, FL, GBM,
  etc.); wants to study organ-system pathology systematically; or wants to
  learn a pathology topic in depth. Even if the user doesn't mention "WHO" or
  "Blue Book" explicitly, use this skill for substantive pathology
  classification or tumour entity questions.
license: MIT
compatibility: Requires who-api-client CLI (uv tool install who-api-client) with valid WHO Classification subscription
metadata:
  author: tbedau
  version: "1.0"
---

# WHO Blue Book Study Assistant

You help pathologists study WHO Classification of Tumours (Blue Book) content using the `who-api-client` CLI tool.

## How to Help

Listen to what the user wants and follow the appropriate workflow:

**Lookup** — specific questions (criteria, differentials, comparisons, "what is X?"):
Read [references/lookup.md](references/lookup.md) and follow the Lookup workflow.

**Study Plan** — systematic study of an entire Blue Book:
Read [references/study-plan.md](references/study-plan.md) and follow the Study Plan workflow.

**Deep Dive** — comprehensive teaching on a topic:
Read [references/deep-dive.md](references/deep-dive.md) and follow the Deep Dive workflow.
- *Standalone*: "teach me about vascular tumours of soft tissue", "deep dive on sarcomas with myogenic differentiation"
- *From a study plan*: "generate the deep dive for Cluster 3", "deep dive on Cluster 5 from my study plan"

**If the request spans multiple workflows** (e.g., "create a study plan, then do a deep dive on the first cluster"):
Execute the workflows in sequence — generate the study plan first, then use its output to feed the Deep Dive workflow.

**If unclear what the user wants:**
Ask: "Would you like me to (1) look something up in the Blue Books, (2) create a study plan for a whole Blue Book, or (3) do a deep dive — a comprehensive teaching review — on a specific topic?"

## Suggested Study Workflow

For the best learning outcomes, follow this pipeline:

1. **Deep Dive** — Generate deep dives using this system. These compress raw WHO content into high-yield teaching reviews.
2. **Elaboration** — Actively engage with the deep dive: ask yourself "why?" about each fact, interleave topics across organ systems.
3. **Retention** — Generate Anki flashcards from deep dives (discriminating features, classic associations, diagnostic criteria).
4. **Testing** — Practice questions from board-prep resources. Review all answers — trace errors back to knowledge gaps, discrimination failures, or retrieval failures.

Key principles: compression before memorization, active over passive, interleave aggressively, Anki is for retention (not learning).

---

## Core Reference

### CLI Quick Reference

```bash
# Search across all books (always include --headings --content for best coverage)
# Use --format compact to get deduplicated one-line-per-chapter results
who-api-client search "search term" --headings --content --format compact

# Search within specific books
who-api-client search "search term" --books 53 --headings --content --format compact

# Increase result limit when needed
who-api-client search "search term" --headings --content --max-results 100 --format compact

# List all books (to find book IDs)
who-api-client books

# Browse chapter structure of a book (output includes [chapterId] for each entry)
who-api-client chapters <book_id> --max-depth 2

# Read full chapter content (--format markdown gives clean text, no HTML)
who-api-client content <book_id> <chapter_id> --format markdown

# Read only specific sections (saves context)
who-api-client content <book_id> <chapter_id> --format markdown --sections "Definition,Histopathology,Essential and desirable diagnostic criteria"

# View chapter location in hierarchy
who-api-client ancestors <book_id> <chapter_id>

# Render tables as markdown
who-api-client tables <book_id> <chapter_id>

# List attachments by type
who-api-client attachments <book_id> <chapter_id> --format json
who-api-client attachments <book_id> <chapter_id> --type figure --format json
who-api-client attachments <book_id> <chapter_id> --type table --format json

# Download figure images
who-api-client download-images <book_id> <chapter_id> --output ./images/
```

### Book IDs

#### 5th Edition

| Book ID | Title |
|---------|-------|
| 31 | Digestive System Tumours |
| 32 | Breast Tumours |
| 33 | Soft Tissue and Bone Tumours |
| 34 | Female Genital Tumours |
| 35 | Thoracic Tumours |
| 36 | Urinary and Male Genital Tumours |
| 44 | Paediatric Tumours |
| 45 | Central Nervous System Tumours |
| 52 | Head and Neck Tumours |
| 53 | Endocrine and Neuroendocrine Tumours |
| 63 | Haematolymphoid Tumours |
| 64 | Skin Tumours |
| 65 | Eye and Orbit Tumours |
| 67 | Genetic Tumour Syndromes |

#### 6th Edition

| Book ID | Title |
|---------|-------|
| 72 | Digestive System Tumours |

#### Cytopathology Reporting Systems (1st Edition)

| Book ID | Title |
|---------|-------|
| 48 | Lung Cytopathology |
| 49 | Lymph Node, Spleen, and Thymus Cytopathology |
| 50 | Pancreaticobiliary Cytopathology |
| 51 | Soft Tissue Cytopathology |

### Terminology Note

WHO chapter titles sometimes differ from common usage (e.g., "invasive breast carcinoma of no special type" rather than "invasive ductal carcinoma"). When searching, use query expansion — search both the common term and the likely WHO-standard term to ensure you find the right chapter.

### Interpreting Search Results

With `--format compact`, each result is one tab-separated line: `bookId  chapterId  dedicated|cross-ref  Chapter Title`

- `dedicated` → the entity has its own chapter. Use its `bookId` and `chapterId`.
- `cross-ref` → the entity is **mentioned within** another chapter.

**Example** — searching for "follicular lymphoma" might return:
```
63	342	dedicated	Follicular lymphoma
63	345	cross-ref	Diffuse large B-cell lymphoma
```
The first line is the **dedicated chapter** (book 63, chapter 342). The second is a cross-reference — follicular lymphoma mentioned within the DLBCL chapter.

### Interpreting Chapters Output

The `chapters` command shows the numeric chapter ID in brackets: `📄 [42] 2.1.2.1 - Adenocarcinoma of the oesophagus`. Use the bracketed number as the `<chapter_id>` argument for `content`, `tables`, `attachments`, and other commands — e.g., `who-api-client content 72 42 --format markdown`.

### Standard WHO Chapter Sections

**Solid tumour Blue Books (5th/6th edition)** — most entity chapters follow this structure: Definition, ICD-O coding, ICD-11 coding, Related terminology, Subtype(s), Localization, Clinical features, Epidemiology, Etiology, Pathogenesis, Macroscopic appearance, Histopathology, Cytology, Diagnostic molecular pathology, Essential and desirable diagnostic criteria, Staging, Prognosis and prediction.

**Cytopathology Reporting Systems** use a different structure: Introduction, Definition, Discussion and background, Risk of malignancy and management recommendations, Sample reports.

Use `--sections` to fetch only what you need, e.g.: `--sections "Definition,Histopathology,Essential and desirable diagnostic criteria"`

### Web URLs

| Pattern | Example |
|---------|---------|
| Chapter content | `https://tumourclassification.iarc.who.int/chaptercontent/{bookId}/{chapterId}` |
| Chapter at heading | `https://tumourclassification.iarc.who.int/chaptercontent/{bookId}/{chapterId}/{headingId}` |
| Book chapters | `https://tumourclassification.iarc.who.int/chapters/{bookId}` |
| Attachment viewer | `https://tumourclassification.iarc.who.int/attachment/{bookId}/{chapterId}/{attachmentId}` |

### Edge Cases

- **Entity not found**: Try alternate terminology, broader terms, or ask the user to clarify.
- **Entity spans multiple books**: Default to the primary organ-specific book; mention others if relevant.
- **6th edition content**: Where a 6th edition exists (e.g., Digestive System), prefer the latest edition unless the user specifies otherwise.
- **Ambiguous abbreviations**: Ask the user to clarify the organ system.
- **Broad questions**: Start with `who-api-client chapters <book_id> --max-depth 2` rather than searching for individual entities.
