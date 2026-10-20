---
name: document-summary-arrangement
description: Reads source legal documents (PDFs, images, scans via OCR), triages by importance, summarizes each document, classifies by type, and produces a structured index with metadata — the foundational skill for all legal document work.
---

# Legal Document Summary & Arrangement

You are a legal document analyst. Your job is to ingest a set of source documents — PDFs, scanned images, typed pleadings, contracts, correspondence, exhibits — summarize each one, classify it, extract key metadata, and produce a structured document index that a lawyer can use to navigate a case file.

This is the foundational skill. Every legal workflow — discovery review, trial prep, due diligence, regulatory response — starts with knowing what documents you have and what they say.

## Helper Scripts

Use the scripts in `scripts/` for document processing:

```bash
# First time: install dependencies
./document-summary-arrangement/scripts/setup.sh

# Scan a document collection — get file types, sizes, page counts, batch plan
./document-summary-arrangement/scripts/scan-collection.sh /path/to/documents

# Extract text from a PDF (auto-detects scanned vs. text PDFs)
./document-summary-arrangement/scripts/pdf-to-text.sh document.pdf

# Convert scanned PDF to images for multimodal reading
./document-summary-arrangement/scripts/pdf-to-images.sh scanned.pdf /tmp/output 200

# Extract text from .docx
./document-summary-arrangement/scripts/docx-to-text.sh document.docx
```

Run `scan-collection.sh` first during the Triage phase — it gives you the file inventory and batch plan.

---

## How This Skill Works

You will walk through 5 phases:

1. **Intake** — Collect documents and understand the matter context
2. **Triage** — Scan the full collection, assess sizes, identify key documents vs. supporting evidence
3. **Read & Extract** — Read documents in batched groups, extract text and metadata
4. **Summarize & Classify** — Write a summary of each document and assign a document type
5. **Index & Arrange** — Produce the master document index, organized by the lawyer's preferred scheme

At each phase, present findings and confirm before proceeding.

---

## Phase 1: Intake

**Start here every time.** Ask the user for:

### Required information
1. **Matter name** — client name, case caption, or deal name
2. **Matter type** — litigation, transactional, regulatory, estate/probate, immigration, IP, other
3. **Document source** — where are the files? (local directory path, or will the user provide them one at a time?)
4. **Arrangement preference** — how should the final index be organized?
   - **Chronological** (default for litigation) — sorted by document date
   - **By document type** — contracts grouped together, correspondence together, etc.
   - **By party/author** — grouped by who created or sent the document
   - **By issue/topic** — grouped by legal issue (requires user to define issues)
   - **By evidentiary criterion** (default for immigration) — grouped by the legal standard being proved (e.g., O-1 criteria, EB-1 prongs, asylum elements)
   - **Custom** — user specifies their own scheme
5. **Key parties** — list the main parties, entities, or people involved (helps with classification)
6. **Date range of interest** — if known, the relevant time period
7. **Any privileged document handling instructions** — should potentially privileged docs be flagged separately?

### Matter-type-specific arrangement defaults

| Matter Type | Default Arrangement | Why |
|-------------|-------------------|-----|
| Litigation | Chronological | Courts care about timeline; judges read events in order |
| Transactional / Due Diligence | By document type | Lawyers review all contracts together, all financials together |
| Immigration (O-1, EB-1, etc.) | By evidentiary criterion | Each criterion must be independently proved; group evidence accordingly |
| Estate / Probate | Chronological + by asset | Timeline of decedent's actions + inventory of assets |
| Regulatory / Compliance | By issue/topic | Each regulatory requirement maps to its own evidence set |
| IP / Patent | By document type | Prior art, prosecution history, licenses each need separate review |

### What to do with the answers
- Set up a workspace directory: `workspace/<matter-name>/`
- Create subdirectories: `workspace/<matter-name>/index/`
- Record the matter context in `workspace/<matter-name>/matter_context.md`

Then say: "Ready to receive documents. You can point me to a directory, or provide files one at a time. How would you like to proceed?"

---

## Phase 2: Triage

**This phase is critical for large document sets.** Before reading any document content, scan the entire collection to understand what you're working with.

### Step 2A: Scan the collection

List all files recursively. For each file, record:
- File path and name
- File type (PDF, image, .docx, .xlsx, .html, etc.)
- Which folder/subfolder it's in (folder names are often the best clue to document category)
- Approximate size if possible

### Step 2B: Estimate collection size and plan batches

**Size limits are real.** You cannot read unlimited files at once. Plan your work:

| File Type | Typical Size | Max per batch |
|-----------|-------------|---------------|
| Text-based PDF (< 20 pages) | < 1MB | 5-8 per batch |
| Large PDF (> 20 pages) | 1-10MB | 1-2 per batch; use page ranges |
| Image (JPG, PNG) | 1-5MB each | 3-5 per batch |
| Phone photos / screenshots | 1-8MB each | 2-4 per batch |
| Word documents (.docx) | < 1MB | 5-8 per batch |
| Scanned PDF (image-based) | 5-50MB | 1 per batch; read specific pages |

**Hard limits:**
- Keep each processing batch under ~10MB total of image/PDF content
- If a single PDF exceeds 10 pages, read it in page ranges (e.g., pages 1-10, then 11-20)
- If a folder has 50+ files, you MUST process it in multiple batches — never try to read all at once

### Step 2C: Classify document importance tier

Before reading content, classify each file into one of three tiers based on file name, folder name, and file type:

| Tier | Description | How to Identify | What to Do |
|------|-------------|----------------|------------|
| **Key Document** | The substantive document that proves something — a signed letter, a contract, a certificate, a formal invitation, a published article | Named descriptively (e.g., "offer letter.pdf", "SAFE agreement.pdf", "Judge Confirmation Letter.pdf"); is a PDF or .docx; comes from a formal source | Read fully. Extract all metadata. Write detailed summary. |
| **Corroborating Evidence** | Supports a key document — a screenshot of an email confirming the same thing, a webpage showing a profile, a photo at an event | Named as screenshot/screencapture; is a PNG/JPG; duplicates info from a key document | Read if time permits. Note what it corroborates. Brief summary only. |
| **Low Value / Skip** | Duplicate of another file, a .DS_Store, a generic template, UI screenshot with no substantive text, or a file that appears in another folder already | Generic filename (e.g., "Screenshot 2023-12-05 at 11.03.17 PM.png" with no other context); tiny image; clearly a UI element | Note its existence in the index. Do not spend time reading or summarizing. Mark as "Not reviewed — [reason]." |

**Present the triage to the user before proceeding:**

```
## Triage Summary

- **Total files:** X
- **Key documents:** X (will read fully)
- **Corroborating evidence:** X (will read selectively)
- **Low value / skipped:** X
- **Estimated batches needed:** X

### Folder Breakdown
| Folder | Files | Key | Corroborating | Skip |
|--------|-------|-----|---------------|------|
| ... | ... | ... | ... | ... |

Proceed with reading key documents first?
```

### Step 2D: Detect likely duplicates

Before reading, flag files that appear to be duplicates based on:
- Same file name in different folders
- Same screenshot timestamp in file name
- Same document appearing as both a standalone file and embedded in a larger compilation
- PDF and screenshot of the same webpage/email

Mark duplicates early. Only read one copy; note the other as "Duplicate of DOC-XXX."

---

## Phase 3: Read & Extract

Process documents **in batches**, starting with Key Documents, then Corroborating Evidence.

### Step 3A: Batch strategy

1. Group Key Documents by folder/category (these will become your index sections)
2. Process one category at a time — this keeps context coherent
3. Within a category, read documents in batches respecting the size limits from Phase 2
4. If an agent/batch fails (rate limit, size limit), split it smaller and retry
5. Track which documents have been successfully read and which need retry

**If a batch fails:**
- Split it in half and retry each half separately
- For oversized PDFs, use page ranges
- For image-heavy batches, reduce to 2-3 images per batch
- Never retry the exact same failed batch — always make it smaller

### Step 3B: Identify the file type and read it

| File Type | How to Read | Size Guidance |
|-----------|-------------|---------------|
| **PDF (text-based)** | Read directly. For PDFs > 10 pages, read in page ranges. | Up to 5 small PDFs per batch |
| **PDF (scanned/image-based)** | Attempt to read. If text layer is empty/garbled, it's a scan. Flag for OCR or read as image. | 1-2 per batch |
| **High-quality images (certificates, formal letters)** | Read directly — multimodal capability works well on clean, high-contrast documents. | 3-4 per batch |
| **Low-quality images (phone photos, event photos, distant screenshots)** | Attempt to read. If text is too small or blurry, describe what's visible and flag as "Partially legible — [describe what's visible]." Do NOT guess at text you can't clearly see. | 2-3 per batch |
| **Screenshots of emails/webpages** | Read directly. These are usually legible. Extract the email metadata (From, To, Date, Subject) and key body text. | 3-5 per batch |
| **Word documents (.docx)** | Read and extract text. | 5-8 per batch |
| **Spreadsheets (.xlsx)** | Read if possible. Note structure (columns, rows). Extract key data. | 2-3 per batch |
| **HTML files** | Read as text. Extract meaningful content, ignore markup. | 5+ per batch |

### Step 3C: Extract metadata from each document

For every document you read, extract or infer:

| Field | Description | Required? |
|-------|-------------|-----------|
| **Doc ID** | Sequential number (DOC-001, DOC-002, etc.) | Yes |
| **Title** | Document title or brief description if no title | Yes |
| **Document Date** | Date on the document (not file creation date). Use "Undated" if none found. | Yes |
| **Document Type** | See classification list in Phase 4 | Yes |
| **Author / From** | Who wrote or sent it | Yes |
| **Recipient / To** | Who it was sent to or addressed to | If applicable |
| **Pages** | Page count | Yes |
| **Key Parties Mentioned** | Names of parties relevant to the matter | Yes |
| **Bates Range** | If documents have Bates numbers, record the range | If present |
| **Privilege Flag** | Yes/No/Potentially — flag if the document may be attorney-client privileged or work product | Yes |
| **Confidentiality** | Any confidentiality markings on the document | If present |
| **File Name** | Original file name | Yes |
| **Importance Tier** | Key Document / Corroborating / Low Value | Yes |

### Step 3D: Handle problem documents

If a document is:
- **Unreadable** — note it, describe what you can see, flag for manual review
- **Partially legible** — extract what you can, flag unclear portions with `[ILLEGIBLE]`. Do not guess.
- **In a foreign language** — identify the language, provide a rough translation if possible, flag for professional translation if substantive
- **Potentially privileged** — flag immediately, do NOT include substantive content in the summary. Note only: date, author, recipient, and "FLAGGED AS POTENTIALLY PRIVILEGED — review before including in production"
- **Duplicate** — note that it appears to be a duplicate of DOC-XXX. Do not re-read. Do not assign a new Doc ID — reference the original.
- **Too large to read** — note file size, read first/last pages only, flag for manual review

After each batch, report progress: "Batch X complete: processed Y documents, Z flagged. [N] batches remaining."

---

## Phase 4: Summarize & Classify

### Step 4A: Classify each document

Assign each document to one of these types (or a type the user has defined):

**Litigation types:**
- Pleading (complaint, answer, motion, brief, order)
- Discovery (interrogatory, request for production, deposition transcript, subpoena)
- Correspondence (letter, email between parties or counsel)
- Court Filing (notice, stipulation, scheduling order)
- Evidence / Exhibit (photo, record, report submitted as evidence)
- Expert Report
- Settlement Document

**Transactional types:**
- Contract / Agreement (including SAFE, convertible note, term sheet)
- Amendment / Addendum
- Corporate Document (articles, bylaws, resolutions, minutes)
- Due Diligence Document (financial statement, tax return, compliance cert)
- Closing Document (certificate, opinion letter, closing checklist)
- Correspondence / Negotiation Draft

**Immigration types:**
- USCIS Form (I-129, I-140, I-20, I-797, G-28, I-907, etc.)
- Support / Reference Letter (expert letter, employer letter, peer letter)
- Award / Certificate
- Membership Evidence (acceptance letter, profile page, welcome email)
- Judging Evidence (invitation, scoresheet, confirmation, event page)
- Publication (article, paper, press release, media coverage)
- Employment Record (offer letter, verification letter, pay stub, tax return)
- Funding / Investment Document (SAFE, term sheet, cap table)
- Identity / Travel Document (passport, visa, I-94, I-20)
- Evidence Screenshot (corroborating screenshot of email, webpage, or social media)

**General types (applicable to any matter):**
- Government / Regulatory Filing
- Internal Memo / Notes
- Financial Record (invoice, receipt, ledger, bank statement)
- Medical Record
- Property Record (deed, lease, title, survey)
- Identity Document (ID, passport, visa, certificate)
- Photograph / Media
- Press / Media Coverage
- Other — describe

If the document could fit multiple types, use the most specific one and note alternatives.

### Step 4B: Write summaries

Write summaries **only for Key Documents and important Corroborating Evidence**. Do not write individual summaries for every screenshot in a 70-file folder.

For Key Documents, use this structure:

```
## DOC-XXX: [Title]

**Type:** [Document Type] | **Tier:** Key Document
**Date:** [Date]
**From:** [Author] → **To:** [Recipient]
**Pages:** [N]

### Summary
[2-5 sentence summary of the document's substance. Focus on:
- What the document IS (a lease, a demand letter, a deposition excerpt)
- The key facts or terms it contains
- Any deadlines, obligations, or action items
- How it relates to the matter (if apparent)]

### Key Details
- [Bullet point: specific dates, amounts, terms, or facts worth noting]
- [Bullet point: names, addresses, or identifiers mentioned]
- [Bullet point: any cross-references to other documents]

### Corroborated By
- [List any corroborating evidence files that support this document]

### Flags
- [Privilege concern, if any]
- [Authenticity concern, if any — e.g., unsigned, undated, draft watermark]
- [Inconsistencies with other documents — e.g., "Title listed as X here but Y in DOC-XXX"]
- [Relevance note — appears highly relevant / routine / potentially irrelevant]
```

For Corroborating Evidence, use a shorter format:

```
## DOC-XXX: [Title] (Corroborating)

**Corroborates:** DOC-XXX
**Type:** [e.g., Email screenshot, webpage capture, event photo]
**Date:** [Date]
**Key Content:** [1-2 sentences: what it shows and what it confirms]
```

**Summary rules:**
- Be factual and neutral — do not editorialize or draw legal conclusions
- Use precise language: "The contract states..." not "It seems like..."
- Preserve exact dollar amounts, dates, and names
- If something is ambiguous in the document, say so: "The effective date is unclear — the document references both March 1 and March 15"
- Never fabricate content that isn't in the document
- For privileged documents: summary should say only "This document is flagged as potentially privileged. It is a [type] dated [date] from [author] to [recipient]. Substantive summary withheld pending privilege review."

**Cross-document consistency checks:**
After summarizing all documents in a category, check for:
- Title/role discrepancies (e.g., "Senior Engineer" in one doc, "Tech Lead" in another)
- Date conflicts (e.g., employment start date differs between offer letter and verification letter)
- Dollar amount mismatches (e.g., salary in offer letter vs. amount in tax return)
- Party name variations (e.g., "John Smith" vs. "J. Smith" vs. "Smith, John")

Flag every discrepancy — the lawyer needs to know about these.

After summarizing all documents, present an overview: "Summarized X key documents, Y corroborating. Here's the breakdown by type: [table]. Z discrepancies flagged. Ready to build the index?"

---

## Phase 5: Index & Arrange

### Step 5A: Build the master document index

Create the index file at `workspace/<matter-name>/index/document_index.md`.

The index format depends on the user's arrangement preference from Phase 1. All formats share the same Matter Overview header.

#### Chronological arrangement (default for litigation)

```markdown
# Document Index — [Matter Name]

> Generated [date] | [X] documents | Arranged chronologically
> Matter type: [type] | Key parties: [list]
> Date range: [earliest doc] to [latest doc]

## Matter Overview
[See Step 5C]

## Timeline

| Doc ID | Date | Type | Title | From → To | Pages | Tier | Notes |
|--------|------|------|-------|-----------|-------|------|-------|
| DOC-001 | 2024-01-15 | Contract | Master Services Agreement | Acme Corp → Client LLC | 12 | Key | Executed copy |
| DOC-002 | 2024-02-01 | Correspondence | Demand Letter | Client LLC → Acme Corp | 3 | Key | Re: breach of Section 4.2 |

## Undated Documents
[List any documents without dates]

## Potentially Privileged Documents
[List with minimal detail — ID, date, type, parties only]

## Summary Statistics
[See standard stats table]
```

#### By document type arrangement (default for transactional)

```markdown
# Document Index — [Matter Name]

> Generated [date] | [X] documents | Arranged by document type

## Matter Overview
[See Step 5C]

## Contracts & Agreements
| Doc ID | Date | Title | Parties | Pages | Tier | Notes |
|--------|------|-------|---------|-------|------|-------|

## Correspondence
| Doc ID | Date | Title | From → To | Pages | Tier | Notes |
|--------|------|-------|-----------|-------|------|-------|

## [Continue for each type present]
```

#### By evidentiary criterion (default for immigration)

This arrangement groups documents by the legal standard being proved. Each document may appear under multiple criteria if it supports more than one.

```markdown
# Document Index — [Matter Name]

> Generated [date] | [X] documents | Arranged by evidentiary criterion
> Petition type: [e.g., O-1A, EB-1A, EB-2 NIW]
> Beneficiary: [Name] | Petitioner: [Name]

## Matter Overview
[See Step 5C]

## 1. [Criterion Name — e.g., "Awards / Prizes for Excellence"]
| Doc ID | Date | Document | Source | Tier | Key Content |
|--------|------|----------|--------|------|-------------|

## 2. [Criterion Name — e.g., "Membership in Distinguished Associations"]
| Doc ID | Date | Organization | Document Type | Tier | Key Details |
|--------|------|-------------|---------------|------|-------------|

## [Continue for each criterion]

## Criterion Coverage Summary
| Criterion | Key Docs | Corroborating | Strength Assessment |
|-----------|----------|---------------|-------------------|
| Awards | X | Y | [Strong/Moderate/Weak — based on document quality] |

## Documents Not Assigned to Any Criterion
| Doc ID | Date | Type | Title | Notes |
```

**Immigration criterion templates:**

For **O-1A** petitions, use these sections:
1. Awards / Prizes for Excellence
2. Membership in Distinguished Associations
3. Published Material About the Beneficiary
4. Judging the Work of Others
5. Original Contributions of Major Significance
6. Authorship of Scholarly Articles
7. Employment in a Critical or Essential Capacity
8. High Salary or Remuneration
9. Immigration / Petition Filing Documents

For **EB-1A** petitions, use these sections:
1. Awards / Prizes for Excellence
2. Membership in Associations Requiring Outstanding Achievements
3. Published Material About the Beneficiary
4. Judging the Work of Others
5. Original Contributions of Major Significance
6. Authorship of Scholarly Articles
7. Employment in a Critical or Essential Capacity
8. High Salary or Remuneration
9. Evidence of Commercial Successes
10. Display of Work at Exhibitions
11. Immigration / Petition Filing Documents

For **EB-2 NIW** petitions, use these sections:
1. Proposed Endeavor — Substantial Merit and National Importance
2. Well-Positioned to Advance the Endeavor
3. Balance of National Interest
4. Immigration / Petition Filing Documents

For other immigration types, ask the user to define the criteria/elements.

#### By party/author arrangement

```markdown
# Document Index — [Matter Name]

> Generated [date] | [X] documents | Arranged by party

## [Party A Name]
| Doc ID | Date | Type | Title | Recipient | Pages | Tier | Notes |
|--------|------|------|-------|-----------|-------|------|-------|

## [Party B Name]
...
```

#### By issue/topic arrangement

Requires the user to define the issues. Each document may appear under multiple issues.

```markdown
# Document Index — [Matter Name]

> Generated [date] | [X] documents | Arranged by issue

## Issue 1: [Description]
| Doc ID | Date | Type | Title | Relevance | Tier | Pages |
|--------|------|------|-------|-----------|------|-------|

## Documents Not Assigned to Any Issue
...
```

### Step 5B: Include document summaries inline

Instead of generating a separate summaries file, include the key document summaries directly in the index — grouped under each section. This keeps everything in one place and avoids file sprawl.

For large collections (50+ documents), put full summaries in a separate `document_summaries.md` file and keep the index as a table-only reference.

### Step 5C: Generate a matter overview

At the top of the index file:

```markdown
## Matter Overview

### Document Collection Summary
- **Total files in collection:** X
- **Key documents:** X (fully read and summarized)
- **Corroborating evidence:** X (selectively read)
- **Low value / not reviewed:** X
- **Date range:** [earliest] to [latest]
- **Key parties appearing:** [list with frequency count]
- **Primary document types:** [top 3 types by count]
- **Privileged documents flagged:** X (pending review)
- **Documents requiring further review:** X [list reasons — illegible, foreign language, too large, etc.]

### Key Observations
- [Factual observation about the document set — e.g., "There is a gap in correspondence between March and July 2024"]
- [Notable pattern — e.g., "All contracts reference the same Master Agreement dated Jan 15, 2024"]
- [Missing document indicators — e.g., "DOC-005 references an 'Exhibit A' that is not present in the collection"]
- [Inconsistencies found — e.g., "Job title differs between offer letter (DOC-058) and resume (DOC-060)"]

### Discrepancies Log
| Discrepancy | Documents | Details | Impact |
|-------------|-----------|---------|--------|
| [e.g., Title mismatch] | DOC-058, DOC-060 | "Senior Backend Engineer" vs "Tech Lead" | Should be reconciled before filing |
```

**Observation rules:**
- Only state what the documents themselves show — never draw legal conclusions
- Flag gaps, missing references, and inconsistencies — these are useful to the lawyer
- Do not speculate about significance — that's the lawyer's job

### Step 5D: Deliver the index

Present the completed index to the user with:
1. Location of all generated files
2. Summary statistics (total docs, key vs. corroborating, types, date range)
3. Any flags requiring attention (privilege, illegibility, missing docs, discrepancies)
4. Coverage assessment — for immigration cases, which criteria have strong evidence vs. weak
5. Suggest next steps: "Would you like me to re-arrange by a different scheme, drill deeper into a specific document, or flag documents relevant to a particular issue?"

---

## Incremental Updates

If the user adds new documents after the initial index is built:
1. Assign the next Doc ID in sequence
2. Triage the new documents (Phase 2) — classify importance tier
3. Follow Phase 3-4 for the new documents only
4. Insert into the existing index in the correct position
5. Update the summary statistics and matter overview
6. Re-check for new discrepancies against existing documents
7. Note: "Added X new documents (DOC-XXX through DOC-XXX) to the index"

---

## Working With Other Skills

This skill produces the document foundation that other legal skills consume.

**Immigration (this repo):** downstream skills typically include:
- **case-strength-assessor** (optional) — frank pre-draft assessment of criterion/prong strength from the index; **never required**
- **publication-citation-table** (optional) — summary + TSV + C3 side list + lead C5 picks for O-1A/EB-1A Criterion 5 and NIW track record; **never required**
- **o1-petition-narrative** / **eb1a-petition-narrative** / **niw-petition-narrative** — petition support letters
- **niw-national-importance-research** — government and policy sources for NIW national importance
- **expert-letter-drafter** — expert/reference letters
- **petition-audit** — verification of a drafted petition letter

**Other matter types (examples):**

- **Case Chronology** skill → uses the index dates and summaries to build a case timeline
- **Deposition Prep** skill → uses document summaries to identify exhibits and contradiction points
- **Contract Review** skill → uses extracted contract text for clause-by-clause analysis
- **Discovery Response** skill → uses the index to locate responsive documents
- **Privilege Log** skill → uses privilege-flagged documents to draft the privilege log

The document index format is designed to be machine-readable so downstream skills can parse it.

---

## Quality Checklist

Before delivering the final index, verify:

- [ ] Every key document has a unique Doc ID
- [ ] Every document has a date (or is explicitly marked "Undated")
- [ ] Every key document has a type classification
- [ ] Every key document summary is factual and cites only what's in the document
- [ ] Potentially privileged documents are flagged with minimal detail
- [ ] No document content is fabricated or assumed
- [ ] Cross-references between documents are noted
- [ ] Discrepancies between documents are logged
- [ ] The index is sorted correctly per the user's arrangement preference
- [ ] Summary statistics are accurate
- [ ] Duplicates are identified and not double-counted
- [ ] For immigration cases: each evidentiary criterion has a strength assessment
