---
name: document-intelligence
description: |
  **[REQUIRED]** For **ALL** document/file extraction, parsing, or processing tasks with Snowflake Cortex AI.
  Use when: extracting data from PDFs, parsing documents/files, processing invoices/contracts/reports, 
  analyzing charts/blueprints, building document pipelines, reading files from stage, OCR tasks.
  Triggers: 
  - Documents: document extraction, parse document, documents in stage, docs, paperwork, papers, pages, forms, sheets
  - Files: file extraction, parse file, files in stage, process files, read PDF, attachments, uploads, assets, blobs, objects, artifacts, staged files, uploaded files
  - Formats: PDFs, Word docs, Excel files, spreadsheets, slides, presentations, images, scans, screenshots, scanned documents
  - Business docs: invoices, receipts, bills, statements, quotes, purchase orders, POs, contracts, agreements, policies, claims, reports, manuals, guides, specs, datasheets, applications, certificates, licenses, letters, memos, proposals, work orders, medical scans, lab results, prescriptions, medical records, patient records, healthcare documents, clinical notes, discharge summaries, insurance claims, EOBs, radiology reports, pathology reports
  - Actions: extract from file, extract info, get data from, pull info from, read text from, OCR, digitize, scrape, capture data, analyze these, parse these
  - Functions: AI_EXTRACT, AI_PARSE_DOCUMENT, AI_COMPLETE, document AI
---

# Document Intelligence

Entry point for all document processing tasks using Snowflake Cortex AI.

## Reference Files

This skill uses reference documentation for detailed function guidance:

| Reference | Location | Use For |
|-----------|----------|---------|
| AI_EXTRACT | `reference/ai-extract.md` | Structured extraction (fields, tables) |
| AI_PARSE_DOCUMENT | `reference/ai-parse-doc.md` | Full content parsing (text, layout, images) |

**Load reference context** when user needs specific function details:
- For structured extraction → Read `reference/ai-extract.md`
- For content parsing → Read `reference/ai-parse-doc.md`

## When to Use

- User wants to extract data from documents (PDFs, images, Office files)
- User mentions AI_EXTRACT or AI_PARSE_DOCUMENT
- User wants to process invoices, contracts, forms, reports
- User needs to analyze charts, blueprints, diagrams
- User wants to build document processing pipelines

## Workflow

```
Start
  ↓
Step 1: Gather Document Info
  ↓
  ├─→ Local file → PUT to Snowflake stage
  │
  ├─→ Other storage (GDrive, Dropbox, etc.) → Load openflow skill
  │                                              ↓
  │                                           Setup connector
  │                                              ↓
  │                                           Return here
  ↓
Step 2: Determine Extraction Goal
  ↓
  ├─→ Structured fields/tables ─────────────────────────────────────┐
  │                                                                 │
  ├─→ Full text with layout → Load ai-parse-doc/SKILL.md (LAYOUT)   │
  │                                                                 │
  ├─→ Text via OCR → Load ai-parse-doc/SKILL.md (OCR)               │
  │                                                                 │
  └─→ Images/charts/blueprints → **Flow C: Visual Analysis**         │
                                                                    ↓
                                            Step 2.5: Test Run & Refinement
                                                                    │
                                              ┌─────────────────────┴──────────────────────┐
                                              ↓                                            │
                                        Select test file                                   │
                                              ↓                                            │
                                        Run AI_EXTRACT on single file                      │
                                              ↓                                            │
                                        Review results                                     │
                                              ↓                                            │
                                        Satisfied? ──Yes──→ Choose next action             │
                                              │              │                             │
                                              No             ├─→ Batch extraction ─────────┘
                                              ↓              ├─→ Store result
                                        Ask expected answer  ├─→ Add more fields
                                              ↓              └─→ Done
                                        LLM-judge refines prompt
                                              ↓
                                        Retry test (max 3x) ─────────────────────────┐
                                              │                                      │
                                              └──────────────────────────────────────┘
  ↓
Step 3: Post-Processing Options
  ↓
  ├─→ Store results → Create table / Create pipeline
  │
  └─→ Build RAG/search integration
```

### Step 1: Gather Document Information

**Ask** user about their document using `ask_user_question`:

**Question 1 - File Format:**
```
What type of file do you want to process?
Options:
1. PDF
2. Image (PNG, JPEG, TIFF)
3. Office document (DOCX, PPTX)
4. HTML or TXT file
5. CSV file - AI_EXTRACT only
6. MD or EML file - AI_EXTRACT only
7. Excel file (XLSX, XLS) - not supported
8. Legacy Office (DOC, PPT) - needs conversion
```

**Supported Formats Summary:**
- **AI_EXTRACT supports:** PDF, images (PNG, JPEG, TIFF), DOCX, PPTX, HTML, TXT, CSV, MD, EML
- **AI_PARSE_DOCUMENT supports:** PDF, images (PNG, JPEG, TIFF), DOCX, PPTX, HTML, TXT

**If user selects "CSV file":** CSV files are supported by AI_EXTRACT only (not AI_PARSE_DOCUMENT). Continue to Step 2 to determine extraction goal.

**If user selects "MD or EML file":** MD and EML files are supported by AI_EXTRACT only (not AI_PARSE_DOCUMENT). Continue to Step 2 to determine extraction goal.

**If user selects "HTML or TXT file":** HTML and TXT files are supported by both AI_EXTRACT and AI_PARSE_DOCUMENT. Continue to Step 2 to determine extraction goal.

**If user selects "Legacy Office (DOC, PPT)":**
```
Legacy Office formats (DOC, PPT) are not directly supported.

Please convert to modern formats:
- DOC → DOCX (Save As in Word)
- PPT → PPTX (Save As in PowerPoint)
- Or export as PDF

Then upload the converted file and continue.
```

**If user selects "Excel file (XLSX, XLS)":**

Excel files are not directly supported by AI_EXTRACT or AI_PARSE_DOCUMENT. Inform the user of their options:

```
Excel files (.xlsx, .xls) are not directly supported by the document AI functions.

You have two options:

Option 1: Convert to PDF
- Export the Excel file as PDF from Excel/Google Sheets
- Then upload the PDF and use AI_EXTRACT or AI_PARSE_DOCUMENT

Option 2: Load directly into Snowflake (Recommended for tabular data)
- Snowflake has native Excel support for loading data into tables:

-- Infer schema from Excel file
SELECT * FROM TABLE(
  INFER_SCHEMA(
    LOCATION => '@my_stage/data.xlsx',
    FILE_FORMAT => 'TYPE=EXCEL'
  )
);

-- Query Excel file directly  
SELECT * FROM @my_stage/data.xlsx 
(FILE_FORMAT => 'TYPE=EXCEL', SHEET_NAME => 'Sheet1');

-- Load into table
COPY INTO my_table FROM @my_stage/data.xlsx
FILE_FORMAT = (TYPE = EXCEL)
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;

Which option would you like to proceed with?
```

If user chooses Option 1 (convert to PDF), guide them to upload the PDF and continue with the normal flow.

If user chooses Option 2 (load directly), help them with the Snowflake SQL commands above.

**Question 2 - File Location:**
```
Where is your file stored?
Options:
1. Internal Snowflake stage (e.g., @my_db.my_schema.my_stage/file.pdf)
2. External stage (S3, Azure Blob, GCS)
3. Local file on my computer
4. Other storage (Google Drive, Dropbox, SharePoint, OneDrive, Box)
5. Need help setting up a stage
```

**If user selects "Local file on my computer":**

Help user upload file to a Snowflake stage using PUT command.

1. **First, ensure a stage exists** (or create one):
```sql
-- Create a stage if needed (with server-side encryption)
CREATE STAGE IF NOT EXISTS my_db.my_schema.doc_stage
  DIRECTORY = (ENABLE = TRUE)
  ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')
  COMMENT = 'Stage for document processing';
```

2. **Ask user for file path:**
```
What is the full path to your local file?
Example: /Users/username/Documents/invoice.pdf
         C:\Users\username\Documents\invoice.pdf
```

3. **Generate PUT command** (must be run via SnowSQL, Snowflake CLI, or Python connector):

```sql
-- Using SnowSQL or Snowflake CLI
PUT file:///path/to/your/file.pdf @my_db.my_schema.doc_stage AUTO_COMPRESS=FALSE;
```

**Provide instructions based on user's tool:**

**Option A - SnowSQL:**
```bash
# Install SnowSQL if not installed
# https://docs.snowflake.com/en/user-guide/snowsql-install-config

# Connect and upload
snowsql -a <account> -u <username>
PUT file:///path/to/file.pdf @my_db.my_schema.doc_stage AUTO_COMPRESS=FALSE;
```

**Option B - Snowflake CLI (snow):**
```bash
# Upload using Snowflake CLI
snow stage copy /path/to/file.pdf @my_db.my_schema.doc_stage --overwrite
```

**Option C - Python:**
```python
from snowflake.connector import connect

conn = connect(account='...', user='...', password='...')
cursor = conn.cursor()

# Upload file
cursor.execute("""
    PUT file:///path/to/file.pdf @my_db.my_schema.doc_stage 
    AUTO_COMPRESS=FALSE OVERWRITE=TRUE
""")

print("File uploaded successfully!")
conn.close()
```

**Option D - Multiple files:**
```sql
-- Upload all PDFs from a directory
PUT file:///path/to/folder/*.pdf @my_db.my_schema.doc_stage AUTO_COMPRESS=FALSE;
```

4. **Verify upload:**
```sql
-- List files in stage
LIST @my_db.my_schema.doc_stage;

-- Or using directory table
SELECT * FROM DIRECTORY(@my_db.my_schema.doc_stage);
```

5. **Refresh directory table** (required for DIRECTORY queries):
```sql
ALTER STAGE @my_db.my_schema.doc_stage REFRESH;
```

After file is uploaded, continue with extraction using the stage path.

**If user selects "Other storage":**
- Inform user that files need to be ingested into a Snowflake stage first
- **Load** the `openflow` skill to help set up a connector for their storage provider
- After openflow setup completes, return here to continue with extraction

**Question 3 - Content Type:**
```
What kind of content is in your document?
Options:
1. Structured forms (invoices, receipts, applications)
2. Reports/articles with text and tables
3. Charts, graphs, blueprints, diagrams
4. General text (manuals, policies, contracts)
```

### Step 2: Determine Extraction Goal

**Ask** user what they want to extract:

```
What do you want to extract?
Options:
1. Specific fields (names, dates, amounts, IDs)
2. Tables with defined columns
3. Full text with layout preservation (tables, headers, structure)
4. Text only via OCR (quick text extraction)
5. Images and visual content for analysis (charts, blueprints)
```

**Route based on response:**

| User Selection | Route To | Function |
|----------------|----------|----------|
| Specific fields, Tables | **Step 2.5** (Test first) → then `ai-extract/SKILL.md` | AI_EXTRACT |
| Full text with layout | **Step 2.4** (Page optimization) → `ai-parse-doc/SKILL.md` | AI_PARSE_DOCUMENT (LAYOUT mode) |
| Text only via OCR | **Step 2.4** (Page optimization) → `ai-parse-doc/SKILL.md` | AI_PARSE_DOCUMENT (OCR mode) |
| Images, Charts, Blueprints | **Step 2.6** (Visual Analysis) | AI_COMPLETE (direct, no parsing) |

### Step 2.4: Page Optimization (For AI_PARSE_DOCUMENT)

**Only applies when user selected LAYOUT mode or OCR mode (NOT Visual Analysis).**

Before parsing, ask user about page optimization to improve performance and reduce costs:

**Ask** user:
```
Would you like to parse the entire document or specific pages?
Options:
1. Parse entire document
2. Parse specific page range (e.g., pages 1-50)
3. Parse specific pages (e.g., pages 1, 5, 10, 25)
4. I'm not sure - help me decide
```

**If "Parse entire document":**
```sql
-- Parse all pages with page_split for easier processing
SELECT AI_PARSE_DOCUMENT(
  TO_FILE('@stage', 'document.pdf'),
  {'mode': 'LAYOUT', 'page_split': true}
) AS parsed;
```

**If "Parse specific page range":**

Ask for the range:
```
What page range would you like to parse?
Example: 1-50 (parses pages 1 through 50)
Note: Page numbers are 1-indexed for your input, converted to 0-indexed internally.
```

```sql
-- Parse specific range (page_filter uses 0-indexed pages)
-- For user input "1-50", use start: 0, end: 50
SELECT AI_PARSE_DOCUMENT(
  TO_FILE('@stage', 'document.pdf'),
  {'mode': 'LAYOUT', 'page_filter': [{'start': 0, 'end': 50}]}
) AS parsed;
```

**If "Parse specific pages":**

Ask for page numbers:
```
Which specific pages would you like to parse?
Example: 1, 5, 10, 25 (parses only these pages)
Note: Page numbers are 1-indexed for your input, converted to 0-indexed internally.
```

```sql
-- Parse specific pages (0-indexed internally)
-- For user input "1, 5, 10, 25", use [0, 4, 9, 24]
SELECT AI_PARSE_DOCUMENT(
  TO_FILE('@stage', 'document.pdf'),
  {'mode': 'LAYOUT', 'page_filter': [0, 4, 9, 24]}
) AS parsed;
```

**If "I'm not sure":**

Provide guidance:
```
Here's how to decide:

• Parse entire document: Best for full text extraction, RAG pipelines, 
  or when you need all content. Works well for documents ≤500 pages.

• Parse specific page range: Best when you know the relevant section 
  (e.g., "chapters 1-3 are on pages 1-75"). Faster and cheaper.

• Parse specific pages: Best for extracting just a table of contents, 
  specific chapters, or known important pages.

Tips:
- First page often has title, author, date
- Last few pages often have references, appendix
- Table of contents usually in first 5 pages

Would you like me to first get the page count so you can decide?
```

If user wants page count:
```sql
-- Quick page count check (minimal processing)
SELECT AI_PARSE_DOCUMENT(
  TO_FILE('@stage', 'document.pdf'),
  {'mode': 'OCR', 'page_filter': [{'start': 0, 'end': 1}]}
):pageCount AS total_pages;
```

**Then proceed to load** `reference/ai-parse-doc.md` with the selected page options.

### Step 2.5: Test Run & Prompt Refinement (For Structured Extraction)

**Only applies when user selected "Specific fields" or "Tables".**

This step validates extraction on a single file before batch processing, with iterative prompt refinement using LLM-as-judge.

#### 2.5a: Define Initial Extraction Fields

**Ask** user for the fields they want to extract:

```
What fields do you want to extract? Please provide field names and descriptions.
Example: 
- invoice_number: The invoice or bill number
- vendor_name: Name of the vendor or supplier
- total_amount: The total amount due
```

Build the initial responseFormat:
```sql
responseFormat => {
  'invoice_number': 'What is the invoice number?',
  'vendor_name': 'What is the vendor name?',
  'total_amount': 'What is the total amount?'
}
```

#### 2.5b: Select Test File

**Ask** user using `ask_user_question`:

```
How would you like to select the test file?
Options:
1. Use the first file in the stage
2. Let me pick a specific file from the stage
3. I'll provide the exact file path
```

**If "first file":**
```sql
-- Get first file from stage
SELECT relative_path 
FROM DIRECTORY(@db.schema.stage) 
WHERE relative_path LIKE '%.pdf' 
LIMIT 1;
```

**If "pick from stage":**
```sql
-- List available files
SELECT relative_path, size, last_modified
FROM DIRECTORY(@db.schema.stage)
WHERE relative_path LIKE '%.pdf'
ORDER BY last_modified DESC
LIMIT 10;
```
Then ask user to select from the list.

#### 2.5c: Run Test Extraction

Execute AI_EXTRACT on the single test file:

```sql
-- Test extraction on single file
SELECT AI_EXTRACT(
  file => TO_FILE('@db.schema.stage', '<selected_test_file>'),
  responseFormat => {
    'field1': 'question1',
    'field2': 'question2'
    -- ... user-defined fields
  }
) AS test_result;
```

**Display results to user in a readable format:**
```sql
SELECT 
  test_result:response:field1::STRING AS field1,
  test_result:response:field2::STRING AS field2
FROM (SELECT AI_EXTRACT(...) AS test_result);
```

#### 2.5d: Review Results

**Ask** user using `ask_user_question`:

```
Here are the test extraction results:

| Field | Extracted Value |
|-------|-----------------|
| invoice_number | INV-2024-001 |
| vendor_name | Acme Corp |
| total_amount | $1,234.56 |

Are you satisfied with these results?
Options:
1. Yes, proceed with full extraction
2. No, some fields need improvement
3. No, start over with different fields
```

**If "Yes":** Proceed to **Load** `ai-extract/SKILL.md` for full batch extraction with validated responseFormat.

**If "Start over":** Return to Step 2.5a.

**If "Some fields need improvement":** Continue to refinement loop.

#### 2.5e: Prompt Refinement Loop (LLM-as-Judge)

**Ask** user which field(s) need improvement:

```
Which field(s) gave incorrect results?
(Select all that apply)
```

**For each problematic field, ask:**

```
For the field "[field_name]":
- Current extraction: "[actual_result]"
- What should the correct value be?
```

**Use Claude as LLM-judge to refine the prompt:**

```sql
-- LLM-as-judge prompt refinement
SELECT AI_COMPLETE(
  'claude-3-5-sonnet',
  $You are an expert at crafting extraction prompts for document AI.

TASK: Improve an extraction question that didn't produce the expected result.

FIELD: [field_name]
ORIGINAL QUESTION: "[original_question]"
EXTRACTED VALUE: "[actual_result]"  
EXPECTED VALUE: "[expected_result]"
DOCUMENT TYPE: [document_type from Step 1]

Analyze why the original question may have failed and provide an improved question that would more accurately extract the expected value.

Consider:
- Is the question too vague or too specific?
- Should it reference a specific location in the document?
- Should it specify the format of the expected answer?
- Are there synonyms or alternative phrasings that might work better?

Return ONLY the improved question, nothing else.$
) AS improved_question;
```

**Update the responseFormat with refined question(s)** and retry test extraction.

#### 2.5f: Iteration Limits

- Maximum **3 refinement iterations** per field
- After 3 attempts, **ask** user:
  ```
  We've tried 3 prompt variations for "[field_name]" without success.
  Options:
  1. Continue anyway with best result so far
  2. Skip this field for now
  3. Let me manually specify the extraction question
  4. Try fallback method (AI_PARSE_DOCUMENT + AI_COMPLETE)
  ```

**If "Try fallback method":** Proceed to **Step 2.5f-fallback** below.

---

#### 2.5f-fallback: AI_PARSE_DOCUMENT + AI_COMPLETE Structured Outputs

When AI_EXTRACT doesn't produce accurate results even after prompt refinement, use this alternative approach:

1. **Parse the document text** using AI_PARSE_DOCUMENT
2. **Extract fields** from the parsed text using AI_COMPLETE with structured outputs

This method can be more effective for complex documents where AI_EXTRACT struggles.

**Step 1: Parse document to get text content**

```sql
-- Parse document using OCR or LAYOUT mode
SELECT AI_PARSE_DOCUMENT(
  TO_FILE('@db.schema.stage', '<test_file>'),
  {'mode': 'LAYOUT'}
):content::STRING AS document_text;
```

**Step 2: Build JSON schema for structured output**

Convert the user's fields into a JSON schema:

```sql
-- Example: For fields invoice_number, vendor_name, total_amount
-- Build this schema:
{
  'type': 'json',
  'schema': {
    'type': 'object',
    'properties': {
      'invoice_number': {
        'type': 'string',
        'description': 'The invoice or bill number'
      },
      'vendor_name': {
        'type': 'string', 
        'description': 'Name of the vendor or supplier'
      },
      'total_amount': {
        'type': 'string',
        'description': 'The total amount due'
      }
    },
    'required': ['invoice_number', 'vendor_name', 'total_amount']
  }
}
```

**Step 3: Extract using AI_COMPLETE with structured outputs**

```sql
-- Complete extraction with structured output
WITH parsed_doc AS (
  SELECT AI_PARSE_DOCUMENT(
    TO_FILE('@db.schema.stage', '<test_file>'),
    {'mode': 'LAYOUT'}
  ):content::STRING AS document_text
)
SELECT AI_COMPLETE(
  'claude-3-5-sonnet',
  'Extract the following information from this document text. Return ONLY the requested fields in JSON format.

DOCUMENT TEXT:
' || document_text || '

Extract these fields:
- invoice_number: The invoice or bill number
- vendor_name: Name of the vendor or supplier  
- total_amount: The total amount due',
  {
    'response_format': {
      'type': 'json',
      'schema': {
        'type': 'object',
        'properties': {
          'invoice_number': {'type': 'string', 'description': 'The invoice or bill number'},
          'vendor_name': {'type': 'string', 'description': 'Name of the vendor or supplier'},
          'total_amount': {'type': 'string', 'description': 'The total amount due'}
        },
        'required': ['invoice_number', 'vendor_name', 'total_amount']
      }
    },
    'max_tokens': 4096
  }
) AS extraction_result
FROM parsed_doc;
```

**Step 4: Compare results with AI_EXTRACT**

Display both results to user:

```
Fallback extraction results:

| Field | AI_EXTRACT Result | AI_COMPLETE Result |
|-------|-------------------|-------------------|
| invoice_number | INV-2024-001 | INV-2024-001 |
| vendor_name | Acme | Acme Corporation |
| total_amount | 1234 | $1,234.56 |

Which result is more accurate?
Options:
1. AI_COMPLETE results are better - use fallback method
2. AI_EXTRACT results are better - stick with original
3. Neither is correct - try manual specification
```

**Step 5: If fallback is better, use for batch processing**

```sql
-- Batch extraction using AI_PARSE_DOCUMENT + AI_COMPLETE
SELECT 
  relative_path AS file_path,
  PARSE_JSON(AI_COMPLETE(
    'claude-3-5-sonnet',
    'Extract the following information from this document text. Return ONLY the requested fields.

DOCUMENT TEXT:
' || AI_PARSE_DOCUMENT(
      TO_FILE('@db.schema.stage', relative_path),
      {'mode': 'LAYOUT'}
    ):content::STRING || '

Extract: invoice_number, vendor_name, total_amount',
    {
      'response_format': {
        'type': 'json',
        'schema': {
          'type': 'object',
          'properties': {
            'invoice_number': {'type': 'string'},
            'vendor_name': {'type': 'string'},
            'total_amount': {'type': 'string'}
          },
          'required': ['invoice_number', 'vendor_name', 'total_amount']
        }
      },
      'max_tokens': 4096
    }
  )) AS extracted_data
FROM DIRECTORY(@db.schema.stage)
WHERE relative_path LIKE '%.pdf';
```

**Structured Output Schema Examples**

For different data types:

```sql
-- String fields
'field_name': {'type': 'string', 'description': 'Description of field'}

-- Number fields  
'amount': {'type': 'number', 'description': 'Numeric amount'}

-- Integer fields
'quantity': {'type': 'integer', 'description': 'Whole number quantity'}

-- Boolean fields
'is_paid': {'type': 'boolean', 'description': 'Whether invoice is paid'}

-- Enum fields (constrained values)
'status': {
  'type': 'string',
  'enum': ['pending', 'approved', 'rejected'],
  'description': 'Document status'
}

-- Array fields
'line_items': {
  'type': 'array',
  'items': {
    'type': 'object',
    'properties': {
      'description': {'type': 'string'},
      'quantity': {'type': 'integer'},
      'unit_price': {'type': 'number'},
      'total': {'type': 'number'}
    },
    'required': ['description', 'quantity', 'unit_price', 'total']
  },
  'description': 'List of line items'
}

-- Nested objects
'address': {
  'type': 'object',
  'properties': {
    'street': {'type': 'string'},
    'city': {'type': 'string'},
    'state': {'type': 'string'},
    'zip': {'type': 'string'}
  },
  'required': ['street', 'city', 'state', 'zip'],
  'description': 'Mailing address'
}
```

**Complete Invoice Extraction Example (Fallback Method)**

```sql
WITH parsed_doc AS (
  SELECT 
    relative_path,
    AI_PARSE_DOCUMENT(
      TO_FILE('@db.schema.stage', relative_path),
      {'mode': 'LAYOUT'}
    ):content::STRING AS document_text
  FROM DIRECTORY(@db.schema.stage)
  WHERE relative_path LIKE '%.pdf'
)
SELECT 
  relative_path AS file_path,
  PARSE_JSON(AI_COMPLETE(
    'claude-3-5-sonnet',
    'You are an expert document extraction assistant. Extract the following information from the invoice document below.

DOCUMENT:
' || document_text || '

Extract all requested fields. If a field is not found, use null.',
    {
      'response_format': {
        'type': 'json',
        'schema': {
          'type': 'object',
          'properties': {
            'invoice_number': {'type': 'string', 'description': 'Invoice or bill number'},
            'invoice_date': {'type': 'string', 'description': 'Date of invoice (YYYY-MM-DD format)'},
            'due_date': {'type': 'string', 'description': 'Payment due date (YYYY-MM-DD format)'},
            'vendor': {
              'type': 'object',
              'properties': {
                'name': {'type': 'string'},
                'address': {'type': 'string'},
                'phone': {'type': 'string'},
                'email': {'type': 'string'}
              },
              'required': ['name']
            },
            'customer': {
              'type': 'object', 
              'properties': {
                'name': {'type': 'string'},
                'address': {'type': 'string'}
              },
              'required': ['name']
            },
            'line_items': {
              'type': 'array',
              'items': {
                'type': 'object',
                'properties': {
                  'description': {'type': 'string'},
                  'quantity': {'type': 'number'},
                  'unit_price': {'type': 'number'},
                  'total': {'type': 'number'}
                },
                'required': ['description', 'total']
              }
            },
            'subtotal': {'type': 'number'},
            'tax_amount': {'type': 'number'},
            'total_amount': {'type': 'number'},
            'currency': {'type': 'string', 'description': 'Currency code (e.g., USD, EUR)'},
            'payment_terms': {'type': 'string'}
          },
          'required': ['invoice_number', 'vendor', 'total_amount']
        }
      },
      'max_tokens': 4096
    }
  )) AS invoice_data
FROM parsed_doc;
```

**When to prefer the fallback method:**

| Scenario | Recommendation |
|----------|----------------|
| Complex nested data (addresses, line items) | Use fallback - better at structured objects |
| Documents with unusual layouts | Use fallback - LAYOUT mode captures more context |
| Need specific data types (numbers, booleans) | Use fallback - schema enforces types |
| Simple flat fields | Stick with AI_EXTRACT - faster and simpler |
| High volume batch processing | Test both, compare accuracy and cost |

---

#### 2.5g: Next Steps After Validation

Once user is satisfied with test results, **ask** what they want to do next:

```
Test extraction validated successfully! What would you like to do next?
Options:
1. Extract from all files in the stage (batch processing)
2. Add more fields to extract
3. Store this single result to a table
4. Try on another test file first
5. Done - I only needed this one file
```

**Route based on response:**

| User Selection | Action |
|----------------|--------|
| Extract from all files | Proceed to batch extraction (Step 2.5h) |
| Add more fields | Return to Step 2.5a with existing fields preserved |
| Store this result | Generate INSERT statement for single result |
| Try another test file | Return to Step 2.5b with same responseFormat |
| Done | End workflow, display final results |

**If "Add more fields":**
```
You currently have these fields defined:
- invoice_number
- vendor_name  
- total_amount

What additional fields would you like to extract?
```

**If "Store this result":**

**Ask** user:
```
How would you like to store the results?
Options:
1. Just store this single result
2. Store and create a pipeline for future files
```

**If "Just store this single result":**

**IMPORTANT - First ask about large files:**

```
Can any of your files be longer than the page limit?
- AI_EXTRACT: 125 pages max
- AI_PARSE_DOCUMENT: 500 pages max
Options:
1. No - all files are within the limit
2. Yes - some files may exceed the limit
3. Not sure
```

**Then ask about page optimization (to reduce cost and improve speed):**

```
Would you like to process the entire document or only specific pages?
This can significantly reduce processing time and cost.

Options:
1. Process entire document (all pages)
2. Process only the first page (common for invoices/forms with header info)
3. Process specific page range (e.g., pages 1-5)
4. Process specific pages (e.g., pages 1, 3, 10)
```

**If user selects page optimization (options 2, 3, or 4):**

First, create the page extraction stored procedure (one-time setup):

```sql
-- Create stage for extracted pages (with server-side encryption)
CREATE STAGE IF NOT EXISTS db.schema.extracted_pages_stage
  DIRECTORY = (ENABLE = TRUE)
  ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')
  COMMENT = 'Stage for extracted PDF pages';

-- Create page extraction stored procedure
CREATE OR REPLACE PROCEDURE db.schema.extract_pdf_pages(
    stage_name STRING, 
    file_name STRING, 
    dest_stage_name STRING,
    page_selection VARIANT  -- Can be: integer (single page), array of integers, or object with 'start' and 'end'
)
RETURNS VARIANT
LANGUAGE PYTHON
RUNTIME_VERSION = '3.9'
PACKAGES = ('snowflake-snowpark-python', 'pypdf2')
HANDLER = 'run'
AS
$
from PyPDF2 import PdfReader, PdfWriter
from snowflake.snowpark import Session
from snowflake.snowpark.file_operation import FileOperation
from io import BytesIO
import os
import json

def run(session: Session, stage_name: str, file_name: str, dest_stage_name: str, page_selection) -> dict:
    result = {
        "status": "success",
        "source_file": file_name,
        "total_pages": 0,
        "extracted_pages": [],
        "output_file": ""
    }
    
    try:
        # Download PDF from stage
        file_url = f"{stage_name}/{file_name}"
        get_result = session.file.get(file_url, '/tmp/')
        file_path = os.path.join('/tmp/', file_name)
        
        if not os.path.exists(file_path):
            return {"status": "error", "message": f"File {file_name} not found in {stage_name}"}

        with open(file_path, 'rb') as f:
            pdf_data = f.read()
            pdf_reader = PdfReader(BytesIO(pdf_data))
            num_pages = len(pdf_reader.pages)
            result["total_pages"] = num_pages
            
            # Determine which pages to extract (convert to 0-indexed)
            pages_to_extract = []
            
            if isinstance(page_selection, int):
                # Single page (1-indexed input)
                pages_to_extract = [page_selection - 1]
            elif isinstance(page_selection, list):
                # List of specific pages (1-indexed input)
                pages_to_extract = [p - 1 for p in page_selection]
            elif isinstance(page_selection, dict):
                # Range with 'start' and 'end' (1-indexed input)
                start = page_selection.get('start', 1) - 1
                end = min(page_selection.get('end', num_pages), num_pages)
                pages_to_extract = list(range(start, end))
            
            # Validate pages
            pages_to_extract = [p for p in pages_to_extract if 0 <= p < num_pages]
            
            if not pages_to_extract:
                return {"status": "error", "message": "No valid pages to extract"}
            
            # Create new PDF with selected pages
            writer = PdfWriter()
            for page_num in pages_to_extract:
                writer.add_page(pdf_reader.pages[page_num])
                result["extracted_pages"].append(page_num + 1)  # Return 1-indexed
            
            # Generate output filename
            base_name = os.path.splitext(file_name)[0]
            if len(pages_to_extract) == 1:
                output_filename = f'{base_name}_page_{pages_to_extract[0] + 1}.pdf'
            else:
                output_filename = f'{base_name}_pages_{pages_to_extract[0] + 1}_to_{pages_to_extract[-1] + 1}.pdf'
            
            output_path = os.path.join('/tmp/', output_filename)
            
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            # Upload to destination stage
            FileOperation(session).put(
                f"file://{output_path}",
                dest_stage_name,
                auto_compress=False
            )
            
            result["output_file"] = output_filename
            
            # Cleanup
            os.remove(file_path)
            os.remove(output_path)
                
        return result
        
    except Exception as e:
        return {"status": "error", "message": str(e)}
$;
```

**Extract pages based on user selection:**

```sql
-- Option 2: First page only
CALL db.schema.extract_pdf_pages(
  '@db.schema.my_stage',
  'invoice.pdf',
  '@db.schema.extracted_pages_stage',
  1  -- Single page (1-indexed)
);

-- Option 3: Page range (e.g., pages 1-5)
CALL db.schema.extract_pdf_pages(
  '@db.schema.my_stage',
  'invoice.pdf',
  '@db.schema.extracted_pages_stage',
  {'start': 1, 'end': 5}  -- Range (1-indexed, inclusive)
);

-- Option 4: Specific pages (e.g., pages 1, 3, 10)
CALL db.schema.extract_pdf_pages(
  '@db.schema.my_stage',
  'invoice.pdf',
  '@db.schema.extracted_pages_stage',
  [1, 3, 10]  -- Array of pages (1-indexed)
);
```

**Then run AI_EXTRACT on extracted pages:**

```sql
-- Extract from the optimized PDF (fewer pages = faster + cheaper)
SELECT AI_EXTRACT(
  file => TO_FILE('@db.schema.extracted_pages_stage', '<output_file_from_procedure>'),
  responseFormat => {
    'invoice_number': 'What is the invoice number?',
    'vendor_name': 'What is the vendor name?',
    'total_amount': 'What is the total amount?'
  }
) AS result;
```

**If "No" (process entire document) or files are within limits:**
```sql
-- Create table and insert single result
CREATE TABLE IF NOT EXISTS db.schema.extraction_results (
  file_path STRING,
  extracted_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
  invoice_number STRING,
  vendor_name STRING,
  total_amount STRING
);

INSERT INTO db.schema.extraction_results (file_path, invoice_number, vendor_name, total_amount)
SELECT 
  '<test_file_path>',
  result:response:invoice_number::STRING,
  result:response:vendor_name::STRING,
  result:response:total_amount::STRING
FROM (SELECT AI_EXTRACT(...) AS result);
```

**If "Yes" or "Not sure" - files may exceed 125 pages:**

**Ask** user how they want to handle large documents:

```
Your files may exceed AI_EXTRACT's 125-page limit. How would you like to handle them?

Options:
1. Chunk into 125-page segments (process each chunk separately)
   - Best for: Invoices, receipts, forms where each page is independent
   - Results can be aggregated after processing

2. Keep entire document together (use AI_PARSE_DOCUMENT + AI_COMPLETE)
   - Best for: Documents where context spans multiple pages
   - Supports up to 500 pages
   - Uses structured outputs for extraction

Use cases for keeping document together:
• Contracts - terms may reference other sections, cross-references
• Legal documents - clauses depend on definitions elsewhere
• Research papers - methodology affects interpretation of results
• Technical manuals - procedures reference diagrams in other sections
• Policy documents - exceptions and conditions span pages
• Loan agreements - terms interconnected across sections
• Insurance policies - coverage details reference exclusions
• Merger/acquisition documents - financial data relates to legal terms
• Patent applications - claims reference detailed descriptions
• Medical records - diagnosis relates to test results and history
```

**If "Chunk into 125-page segments":**
Proceed to Pipeline Option B (chunking pipeline) below.

**If "Keep entire document together":**
Proceed to Pipeline Option C (AI_PARSE_DOCUMENT + AI_COMPLETE flow) below.

**If "Store and create a pipeline":**

This creates a complete pipeline that automatically processes new files added to the stage.

**IMPORTANT - First ask about large files:**

```
Can any of your files be longer than the page limit?
- AI_EXTRACT: 125 pages max
- AI_PARSE_DOCUMENT: 500 pages max
Options:
1. No - all files are within the limit
2. Yes - some files may exceed the limit
3. Not sure
```

**Then ask about page optimization (to reduce cost and improve speed):**

```
Would you like to process entire documents or only specific pages in your pipeline?
Processing fewer pages = faster execution + lower cost.

Options:
1. Process entire documents (all pages)
2. Process only the first page of each document
3. Process a specific page range (e.g., pages 1-5)
4. Process specific pages (e.g., pages 1, 3, 10)
```

---

#### Pipeline Option A: Standard Pipeline (Files within page limits)

If user selects "No" (files within limits) AND "Process entire documents":

```sql
-- Step 1: Create results table
CREATE TABLE IF NOT EXISTS db.schema.extraction_results (
  file_path STRING,
  file_name STRING,
  extracted_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
  invoice_number STRING,
  vendor_name STRING,
  total_amount STRING,
  raw_response VARIANT
);

-- Step 2: Insert current result
INSERT INTO db.schema.extraction_results (file_path, file_name, invoice_number, vendor_name, total_amount, raw_response)
SELECT 
  '<test_file_path>',
  SPLIT_PART('<test_file_path>', '/', -1),
  result:response:invoice_number::STRING,
  result:response:vendor_name::STRING,
  result:response:total_amount::STRING,
  result
FROM (SELECT AI_EXTRACT(...) AS result);

-- Step 3: Create stream on stage to detect new files
CREATE OR REPLACE STREAM db.schema.doc_extraction_stream 
  ON STAGE @db.schema.my_stage;

-- Step 4: Create task to process new files automatically
CREATE OR REPLACE TASK db.schema.doc_extraction_task
  WAREHOUSE = my_warehouse
  SCHEDULE = '5 MINUTE'
  WHEN SYSTEM$STREAM_HAS_DATA('db.schema.doc_extraction_stream')
AS
  INSERT INTO db.schema.extraction_results (file_path, file_name, invoice_number, vendor_name, total_amount, raw_response)
  SELECT 
    relative_path,
    SPLIT_PART(relative_path, '/', -1),
    result:response:invoice_number::STRING,
    result:response:vendor_name::STRING,
    result:response:total_amount::STRING,
    result
  FROM (
    SELECT 
      relative_path,
      AI_EXTRACT(
        file => TO_FILE('@db.schema.my_stage', relative_path),
        responseFormat => {
          'invoice_number': 'What is the invoice number?',
          'vendor_name': 'What is the vendor name?',
          'total_amount': 'What is the total amount?'
        }
      ) AS result
    FROM db.schema.doc_extraction_stream
    WHERE METADATA$ACTION = 'INSERT'
      AND relative_path LIKE '%.pdf'
  );

-- Step 5: Resume the task
ALTER TASK db.schema.doc_extraction_task RESUME;

-- Verify task is running
SHOW TASKS LIKE 'doc_extraction_task' IN SCHEMA db.schema;
```

---

#### Pipeline Option A.1: Page-Optimized Pipeline (Process specific pages only)

If user selects page optimization (options 2, 3, or 4), create a pipeline that extracts specific pages before running AI_EXTRACT:

**Step 1: Create the page extraction stored procedure** (if not already created - see "Store this result" section above)

**Step 2: Create results table with page tracking**

```sql
CREATE TABLE IF NOT EXISTS db.schema.extraction_results (
  result_id INT AUTOINCREMENT,
  file_path STRING,
  file_name STRING,
  pages_processed STRING,        -- Which pages were extracted
  extracted_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
  invoice_number STRING,
  vendor_name STRING,
  total_amount STRING,
  raw_response VARIANT
);
```

**Step 3: Create the page-optimized extraction task**

For **first page only** (most common for invoices):

```sql
-- Stream on source stage
CREATE OR REPLACE STREAM db.schema.doc_source_stream 
  ON STAGE @db.schema.my_stage;

-- Task: Extract first page and run AI_EXTRACT
CREATE OR REPLACE TASK db.schema.page_optimized_extraction_task
  WAREHOUSE = my_warehouse
  SCHEDULE = '5 MINUTE'
  WHEN SYSTEM$STREAM_HAS_DATA('db.schema.doc_source_stream')
AS
DECLARE
  file_record RECORD;
  extract_result VARIANT;
  output_file STRING;
BEGIN
  FOR file_record IN (
    SELECT relative_path 
    FROM db.schema.doc_source_stream 
    WHERE METADATA$ACTION = 'INSERT' 
      AND relative_path LIKE '%.pdf'
  ) DO
    -- Extract first page only
    extract_result := (
      CALL db.schema.extract_pdf_pages(
        '@db.schema.my_stage',
        :file_record.relative_path,
        '@db.schema.extracted_pages_stage',
        1  -- First page only
      )
    );
    
    output_file := extract_result:output_file::STRING;
    
    -- Run AI_EXTRACT on the single page
    INSERT INTO db.schema.extraction_results (file_path, file_name, pages_processed, invoice_number, vendor_name, total_amount, raw_response)
    SELECT 
      :file_record.relative_path,
      SPLIT_PART(:file_record.relative_path, '/', -1),
      'Page 1',
      result:response:invoice_number::STRING,
      result:response:vendor_name::STRING,
      result:response:total_amount::STRING,
      result
    FROM (
      SELECT AI_EXTRACT(
        file => TO_FILE('@db.schema.extracted_pages_stage', :output_file),
        responseFormat => {
          'invoice_number': 'What is the invoice number?',
          'vendor_name': 'What is the vendor name?',
          'total_amount': 'What is the total amount?'
        }
      ) AS result
    );
  END FOR;
END;

ALTER TASK db.schema.page_optimized_extraction_task RESUME;
```

For **specific page range** (e.g., pages 1-5):

```sql
CREATE OR REPLACE TASK db.schema.page_range_extraction_task
  WAREHOUSE = my_warehouse
  SCHEDULE = '5 MINUTE'
  WHEN SYSTEM$STREAM_HAS_DATA('db.schema.doc_source_stream')
AS
DECLARE
  file_record RECORD;
  extract_result VARIANT;
  output_file STRING;
BEGIN
  FOR file_record IN (
    SELECT relative_path 
    FROM db.schema.doc_source_stream 
    WHERE METADATA$ACTION = 'INSERT' 
      AND relative_path LIKE '%.pdf'
  ) DO
    -- Extract pages 1-5
    extract_result := (
      CALL db.schema.extract_pdf_pages(
        '@db.schema.my_stage',
        :file_record.relative_path,
        '@db.schema.extracted_pages_stage',
        {'start': 1, 'end': 5}  -- Page range
      )
    );
    
    output_file := extract_result:output_file::STRING;
    
    INSERT INTO db.schema.extraction_results (file_path, file_name, pages_processed, invoice_number, vendor_name, total_amount, raw_response)
    SELECT 
      :file_record.relative_path,
      SPLIT_PART(:file_record.relative_path, '/', -1),
      'Pages 1-5',
      result:response:invoice_number::STRING,
      result:response:vendor_name::STRING,
      result:response:total_amount::STRING,
      result
    FROM (
      SELECT AI_EXTRACT(
        file => TO_FILE('@db.schema.extracted_pages_stage', :output_file),
        responseFormat => {
          'invoice_number': 'What is the invoice number?',
          'vendor_name': 'What is the vendor name?',
          'total_amount': 'What is the total amount?'
        }
      ) AS result
    );
  END FOR;
END;

ALTER TASK db.schema.page_range_extraction_task RESUME;
```

For **specific pages** (e.g., pages 1, 3, 10):

```sql
CREATE OR REPLACE TASK db.schema.specific_pages_extraction_task
  WAREHOUSE = my_warehouse
  SCHEDULE = '5 MINUTE'
  WHEN SYSTEM$STREAM_HAS_DATA('db.schema.doc_source_stream')
AS
DECLARE
  file_record RECORD;
  extract_result VARIANT;
  output_file STRING;
BEGIN
  FOR file_record IN (
    SELECT relative_path 
    FROM db.schema.doc_source_stream 
    WHERE METADATA$ACTION = 'INSERT' 
      AND relative_path LIKE '%.pdf'
  ) DO
    -- Extract specific pages
    extract_result := (
      CALL db.schema.extract_pdf_pages(
        '@db.schema.my_stage',
        :file_record.relative_path,
        '@db.schema.extracted_pages_stage',
        [1, 3, 10]  -- Specific pages array
      )
    );
    
    output_file := extract_result:output_file::STRING;
    
    INSERT INTO db.schema.extraction_results (file_path, file_name, pages_processed, invoice_number, vendor_name, total_amount, raw_response)
    SELECT 
      :file_record.relative_path,
      SPLIT_PART(:file_record.relative_path, '/', -1),
      'Pages 1, 3, 10',
      result:response:invoice_number::STRING,
      result:response:vendor_name::STRING,
      result:response:total_amount::STRING,
      result
    FROM (
      SELECT AI_EXTRACT(
        file => TO_FILE('@db.schema.extracted_pages_stage', :output_file),
        responseFormat => {
          'invoice_number': 'What is the invoice number?',
          'vendor_name': 'What is the vendor name?',
          'total_amount': 'What is the total amount?'
        }
      ) AS result
    );
  END FOR;
END;

ALTER TASK db.schema.specific_pages_extraction_task RESUME;
```

**Cost/Speed Comparison:**

| Approach | Pages Processed | Relative Cost | Speed |
|----------|-----------------|---------------|-------|
| Full document (10 pages) | 10 | 100% | Baseline |
| First page only | 1 | ~10% | ~10x faster |
| Pages 1-5 | 5 | ~50% | ~2x faster |
| Specific pages (1, 3, 10) | 3 | ~30% | ~3x faster |

---

#### Pipeline Option B: Large File Pipeline (Files > 125 pages)

If user selects "Yes" or "Not sure", create a chunking pipeline:

**Step 1: Create the chunking stored procedure**

This procedure splits PDFs into 125-page chunks and uploads them to a chunks stage:

```sql
-- Create stage for chunked files (with server-side encryption)
CREATE STAGE IF NOT EXISTS db.schema.chunks_stage
  ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');

-- Create chunking stored procedure
CREATE OR REPLACE PROCEDURE db.schema.split_document_into_chunks(
    stage_name STRING, 
    file_name STRING, 
    dest_stage_name STRING,
    chunk_size INT DEFAULT 125
)
RETURNS VARIANT
LANGUAGE PYTHON
RUNTIME_VERSION = '3.9'
PACKAGES = ('snowflake-snowpark-python', 'pypdf2')
HANDLER = 'run'
AS
$
from PyPDF2 import PdfReader, PdfWriter
from snowflake.snowpark import Session
from snowflake.snowpark.file_operation import FileOperation
from io import BytesIO
import os
import math

def run(session: Session, stage_name: str, file_name: str, dest_stage_name: str, chunk_size: int = 125) -> dict:
    result = {
        "status": "success",
        "source_file": file_name,
        "total_pages": 0,
        "chunks_created": 0,
        "chunk_files": []
    }
    
    try:
        # Construct the file URL and retrieve file
        file_url = f"{stage_name}/{file_name}"
        get_result = session.file.get(file_url, '/tmp/')
        file_path = os.path.join('/tmp/', file_name)
        
        if not os.path.exists(file_path):
            return {"status": "error", "message": f"File {file_name} not found in {stage_name}"}

        with open(file_path, 'rb') as f:
            pdf_data = f.read()
            pdf_reader = PdfReader(BytesIO(pdf_data))
            num_pages = len(pdf_reader.pages)
            result["total_pages"] = num_pages
            
            # Calculate number of chunks needed
            num_chunks = math.ceil(num_pages / chunk_size)
            result["chunks_created"] = num_chunks
            
            # Get base filename without extension
            base_name = os.path.splitext(file_name)[0]
            
            for chunk_num in range(num_chunks):
                start_page = chunk_num * chunk_size
                end_page = min((chunk_num + 1) * chunk_size, num_pages)
                
                writer = PdfWriter()
                for page_num in range(start_page, end_page):
                    writer.add_page(pdf_reader.pages[page_num])
                
                # Create chunk filename: original_chunk_1_pages_1_125.pdf
                chunk_filename = f'{base_name}_chunk_{chunk_num + 1}_pages_{start_page + 1}_{end_page}.pdf'
                chunk_file_path = os.path.join('/tmp/', chunk_filename)
                
                with open(chunk_file_path, 'wb') as output_file:
                    writer.write(output_file)
                
                if not os.path.exists(chunk_file_path):
                    return {"status": "error", "message": f"Failed to create chunk file {chunk_filename}"}

                # Upload chunk to destination stage
                FileOperation(session).put(
                    f"file://{chunk_file_path}",
                    dest_stage_name,
                    auto_compress=False
                )
                
                result["chunk_files"].append({
                    "chunk_number": chunk_num + 1,
                    "filename": chunk_filename,
                    "start_page": start_page + 1,
                    "end_page": end_page,
                    "page_count": end_page - start_page
                })
                
                # Clean up temp chunk file
                os.remove(chunk_file_path)
            
            # Clean up original temp file
            os.remove(file_path)
                
        return result
        
    except Exception as e:
        return {"status": "error", "message": str(e)}
$;
```

**Step 2: Create tables for tracking chunks and results**

```sql
-- Table to track chunking operations
CREATE TABLE IF NOT EXISTS db.schema.document_chunks (
  chunk_id INT AUTOINCREMENT,
  source_file STRING,
  chunk_file STRING,
  chunk_number INT,
  start_page INT,
  end_page INT,
  page_count INT,
  chunked_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
  processed BOOLEAN DEFAULT FALSE
);

-- Table for extraction results with chunk tracking
CREATE TABLE IF NOT EXISTS db.schema.extraction_results (
  result_id INT AUTOINCREMENT,
  source_file STRING,           -- Original file name
  chunk_file STRING,            -- Chunk file name (NULL if not chunked)
  chunk_number INT,             -- Chunk number (NULL if not chunked)
  file_name STRING,
  extracted_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
  invoice_number STRING,
  vendor_name STRING,
  total_amount STRING,
  raw_response VARIANT
);

-- Aggregated results view (joins chunks back together)
CREATE OR REPLACE VIEW db.schema.extraction_results_aggregated AS
SELECT 
  source_file,
  ARRAY_AGG(OBJECT_CONSTRUCT(
    'chunk_number', chunk_number,
    'invoice_number', invoice_number,
    'vendor_name', vendor_name,
    'total_amount', total_amount
  )) WITHIN GROUP (ORDER BY chunk_number) AS chunk_results,
  -- For single-value fields, take from first chunk
  MAX(CASE WHEN chunk_number = 1 OR chunk_number IS NULL THEN invoice_number END) AS invoice_number,
  MAX(CASE WHEN chunk_number = 1 OR chunk_number IS NULL THEN vendor_name END) AS vendor_name,
  -- For totals, might need custom logic (sum, last chunk, etc.)
  MAX(total_amount) AS total_amount,
  COUNT(*) AS total_chunks,
  MIN(extracted_at) AS first_extracted_at,
  MAX(extracted_at) AS last_extracted_at
FROM db.schema.extraction_results
GROUP BY source_file;
```

**Step 3: Create the chunking task (runs first)**

```sql
-- Stream on source stage
CREATE OR REPLACE STREAM db.schema.doc_source_stream 
  ON STAGE @db.schema.my_stage;

-- Task 1: Chunk large documents
CREATE OR REPLACE TASK db.schema.chunk_documents_task
  WAREHOUSE = my_warehouse
  SCHEDULE = '5 MINUTE'
  WHEN SYSTEM$STREAM_HAS_DATA('db.schema.doc_source_stream')
AS
DECLARE
  file_record RECORD;
  chunk_result VARIANT;
BEGIN
  -- Process each new file
  FOR file_record IN (
    SELECT relative_path 
    FROM db.schema.doc_source_stream 
    WHERE METADATA$ACTION = 'INSERT' 
      AND relative_path LIKE '%.pdf'
  ) DO
    -- Get page count first
    LET page_count INT := (
      SELECT AI_PARSE_DOCUMENT(
        TO_FILE('@db.schema.my_stage', :file_record.relative_path),
        {'mode': 'OCR', 'page_filter': [{'start': 0, 'end': 1}]}
      ):pageCount::INT
    );
    
    IF (page_count > 125) THEN
      -- Large file: chunk it
      chunk_result := (
        CALL db.schema.split_document_into_chunks(
          '@db.schema.my_stage',
          :file_record.relative_path,
          '@db.schema.chunks_stage',
          125
        )
      );
      
      -- Record chunks in tracking table
      INSERT INTO db.schema.document_chunks (source_file, chunk_file, chunk_number, start_page, end_page, page_count)
      SELECT 
        :file_record.relative_path,
        f.value:filename::STRING,
        f.value:chunk_number::INT,
        f.value:start_page::INT,
        f.value:end_page::INT,
        f.value:page_count::INT
      FROM TABLE(FLATTEN(input => :chunk_result:chunk_files)) f;
    ELSE
      -- Small file: record as single chunk for unified processing
      INSERT INTO db.schema.document_chunks (source_file, chunk_file, chunk_number, start_page, end_page, page_count)
      VALUES (:file_record.relative_path, :file_record.relative_path, 1, 1, :page_count, :page_count);
    END IF;
  END FOR;
END;

ALTER TASK db.schema.chunk_documents_task RESUME;
```

**Step 4: Create the extraction task (processes chunks)**

```sql
-- Stream on chunks table to detect new chunks to process
CREATE OR REPLACE STREAM db.schema.chunks_to_process_stream 
  ON TABLE db.schema.document_chunks
  SHOW_INITIAL_ROWS = TRUE;

-- Task 2: Extract from chunks
CREATE OR REPLACE TASK db.schema.extract_from_chunks_task
  WAREHOUSE = my_warehouse
  SCHEDULE = '2 MINUTE'
  WHEN SYSTEM$STREAM_HAS_DATA('db.schema.chunks_to_process_stream')
AS
  INSERT INTO db.schema.extraction_results (source_file, chunk_file, chunk_number, file_name, invoice_number, vendor_name, total_amount, raw_response)
  SELECT 
    dc.source_file,
    dc.chunk_file,
    dc.chunk_number,
    SPLIT_PART(dc.chunk_file, '/', -1),
    result:response:invoice_number::STRING,
    result:response:vendor_name::STRING,
    result:response:total_amount::STRING,
    result
  FROM db.schema.chunks_to_process_stream dc,
  LATERAL (
    SELECT AI_EXTRACT(
      file => TO_FILE(
        CASE 
          WHEN dc.chunk_file = dc.source_file THEN '@db.schema.my_stage'  -- Original file (small)
          ELSE '@db.schema.chunks_stage'  -- Chunked file
        END, 
        dc.chunk_file
      ),
      responseFormat => {
        'invoice_number': 'What is the invoice number?',
        'vendor_name': 'What is the vendor name?',
        'total_amount': 'What is the total amount?'
      }
    ) AS result
  )
  WHERE dc.METADATA$ACTION = 'INSERT';

ALTER TASK db.schema.extract_from_chunks_task RESUME;
```

**Step 5: Query aggregated results**

```sql
-- View results aggregated by source document
SELECT * FROM db.schema.extraction_results_aggregated;

-- View individual chunk results
SELECT * FROM db.schema.extraction_results ORDER BY source_file, chunk_number;

-- Check processing status
SELECT 
  dc.source_file,
  dc.chunk_number,
  dc.page_count,
  CASE WHEN er.result_id IS NOT NULL THEN 'Processed' ELSE 'Pending' END AS status
FROM db.schema.document_chunks dc
LEFT JOIN db.schema.extraction_results er 
  ON dc.source_file = er.source_file 
  AND dc.chunk_number = er.chunk_number
ORDER BY dc.source_file, dc.chunk_number;
```

---

#### Pipeline Option C: Full Document Pipeline (AI_PARSE_DOCUMENT + AI_COMPLETE)

Use this when documents must be processed as a whole and context from the entire document is important. Supports documents up to 500 pages.

**When to use this approach:**
- **Contracts** - Terms reference other sections (e.g., "as defined in Section 2.1")
- **Legal documents** - Clauses depend on definitions elsewhere in the document
- **Research papers** - Methodology section affects interpretation of results
- **Technical manuals** - Procedures reference diagrams or specs in other sections
- **Policy documents** - Exceptions and conditions span multiple pages
- **Loan/mortgage agreements** - Interest terms tied to conditions throughout
- **Insurance policies** - Coverage details reference exclusions and limitations
- **M&A documents** - Financial data interconnected with legal terms
- **Patent applications** - Claims reference detailed descriptions
- **Medical records** - Diagnosis relates to test results and patient history
- **Annual reports** - Financial statements relate to management discussion
- **RFP responses** - Technical approach references pricing and timeline

**Step 1: Create results table**

```sql
CREATE TABLE IF NOT EXISTS db.schema.extraction_results_full_doc (
  result_id INT AUTOINCREMENT,
  file_path STRING,
  file_name STRING,
  total_pages INT,
  extraction_method STRING DEFAULT 'AI_PARSE_DOCUMENT + AI_COMPLETE',
  extracted_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
  -- Add your extraction fields here
  contract_parties VARIANT,       -- For contracts
  effective_date STRING,
  termination_date STRING,
  total_value STRING,
  key_terms VARIANT,
  obligations VARIANT,
  raw_response VARIANT
);
```

**Step 2: Parse document and extract with structured outputs**

```sql
-- Single document extraction (for testing)
WITH parsed_doc AS (
  SELECT 
    AI_PARSE_DOCUMENT(
      TO_FILE('@db.schema.my_stage', 'contract.pdf'),
      {'mode': 'LAYOUT'}
    ) AS parsed_result
),
document_text AS (
  SELECT 
    parsed_result:content::STRING AS full_text,
    parsed_result:pageCount::INT AS total_pages
  FROM parsed_doc
)
SELECT 
  total_pages,
  AI_COMPLETE(
    'claude-3-5-sonnet',
    'You are an expert contract analyst. Extract the following information from this contract document.
    
IMPORTANT: The entire document content is provided below. Analyze it thoroughly as a complete document - 
terms and definitions in one section may affect interpretation of other sections.

DOCUMENT CONTENT:
' || full_text || '

Extract all requested fields. If information is not found, use null.',
    {
      'response_format': {
        'type': 'json',
        'schema': {
          'type': 'object',
          'properties': {
            'contract_parties': {
              'type': 'object',
              'properties': {
                'party_a': {'type': 'string', 'description': 'First party to the contract'},
                'party_b': {'type': 'string', 'description': 'Second party to the contract'},
                'additional_parties': {
                  'type': 'array',
                  'items': {'type': 'string'},
                  'description': 'Any additional parties'
                }
              },
              'required': ['party_a', 'party_b']
            },
            'effective_date': {'type': 'string', 'description': 'Contract effective/start date'},
            'termination_date': {'type': 'string', 'description': 'Contract end/termination date'},
            'total_value': {'type': 'string', 'description': 'Total contract value or consideration'},
            'key_terms': {
              'type': 'array',
              'items': {
                'type': 'object',
                'properties': {
                  'term_name': {'type': 'string'},
                  'description': {'type': 'string'},
                  'section_reference': {'type': 'string'}
                }
              },
              'description': 'Key terms and definitions'
            },
            'obligations': {
              'type': 'object',
              'properties': {
                'party_a_obligations': {
                  'type': 'array',
                  'items': {'type': 'string'}
                },
                'party_b_obligations': {
                  'type': 'array',
                  'items': {'type': 'string'}
                }
              }
            },
            'payment_terms': {
              'type': 'object',
              'properties': {
                'payment_schedule': {'type': 'string'},
                'payment_method': {'type': 'string'},
                'late_payment_penalty': {'type': 'string'}
              }
            },
            'termination_clauses': {
              'type': 'array',
              'items': {'type': 'string'},
              'description': 'Conditions under which contract can be terminated'
            },
            'governing_law': {'type': 'string', 'description': 'Jurisdiction/governing law'},
            'confidentiality': {'type': 'boolean', 'description': 'Whether confidentiality clause exists'},
            'non_compete': {'type': 'boolean', 'description': 'Whether non-compete clause exists'}
          },
          'required': ['contract_parties', 'effective_date', 'total_value']
        }
      },
      'max_tokens': 8192
    }
  ) AS extraction_result
FROM document_text;
```

**Step 3: Create the full-document extraction pipeline**

```sql
-- Stream on source stage
CREATE OR REPLACE STREAM db.schema.full_doc_stream 
  ON STAGE @db.schema.my_stage;

-- Task for full-document extraction
CREATE OR REPLACE TASK db.schema.full_document_extraction_task
  WAREHOUSE = my_warehouse
  SCHEDULE = '5 MINUTE'
  WHEN SYSTEM$STREAM_HAS_DATA('db.schema.full_doc_stream')
AS
  INSERT INTO db.schema.extraction_results_full_doc (
    file_path, file_name, total_pages, 
    contract_parties, effective_date, termination_date, 
    total_value, key_terms, obligations, raw_response
  )
  SELECT 
    relative_path,
    SPLIT_PART(relative_path, '/', -1),
    parsed_result:pageCount::INT,
    PARSE_JSON(extraction_result):contract_parties,
    PARSE_JSON(extraction_result):effective_date::STRING,
    PARSE_JSON(extraction_result):termination_date::STRING,
    PARSE_JSON(extraction_result):total_value::STRING,
    PARSE_JSON(extraction_result):key_terms,
    PARSE_JSON(extraction_result):obligations,
    PARSE_JSON(extraction_result)
  FROM (
    SELECT 
      relative_path,
      AI_PARSE_DOCUMENT(
        TO_FILE('@db.schema.my_stage', relative_path),
        {'mode': 'LAYOUT'}
      ) AS parsed_result,
      AI_COMPLETE(
        'claude-3-5-sonnet',
        'You are an expert contract analyst. Extract contract information from this document.

DOCUMENT:
' || AI_PARSE_DOCUMENT(
          TO_FILE('@db.schema.my_stage', relative_path),
          {'mode': 'LAYOUT'}
        ):content::STRING || '

Extract: contract_parties, effective_date, termination_date, total_value, key_terms, obligations, payment_terms, termination_clauses, governing_law, confidentiality, non_compete',
        {
          'response_format': {
            'type': 'json',
            'schema': {
              'type': 'object',
              'properties': {
                'contract_parties': {
                  'type': 'object',
                  'properties': {
                    'party_a': {'type': 'string'},
                    'party_b': {'type': 'string'}
                  },
                  'required': ['party_a', 'party_b']
                },
                'effective_date': {'type': 'string'},
                'termination_date': {'type': 'string'},
                'total_value': {'type': 'string'},
                'key_terms': {'type': 'array', 'items': {'type': 'object', 'properties': {'term_name': {'type': 'string'}, 'description': {'type': 'string'}}}},
                'obligations': {'type': 'object', 'properties': {'party_a_obligations': {'type': 'array', 'items': {'type': 'string'}}, 'party_b_obligations': {'type': 'array', 'items': {'type': 'string'}}}},
                'payment_terms': {'type': 'object', 'properties': {'payment_schedule': {'type': 'string'}, 'payment_method': {'type': 'string'}}},
                'termination_clauses': {'type': 'array', 'items': {'type': 'string'}},
                'governing_law': {'type': 'string'},
                'confidentiality': {'type': 'boolean'},
                'non_compete': {'type': 'boolean'}
              },
              'required': ['contract_parties', 'effective_date', 'total_value']
            }
          },
          'max_tokens': 8192
        }
      ) AS extraction_result
    FROM db.schema.full_doc_stream
    WHERE METADATA$ACTION = 'INSERT'
      AND relative_path LIKE '%.pdf'
  );

ALTER TASK db.schema.full_document_extraction_task RESUME;
```

**Additional Schema Templates for Full-Document Extraction:**

**Research Paper Schema:**
```sql
{
  'response_format': {
    'type': 'json',
    'schema': {
      'type': 'object',
      'properties': {
        'title': {'type': 'string'},
        'authors': {'type': 'array', 'items': {'type': 'string'}},
        'abstract': {'type': 'string'},
        'keywords': {'type': 'array', 'items': {'type': 'string'}},
        'methodology': {'type': 'string', 'description': 'Research methodology summary'},
        'key_findings': {'type': 'array', 'items': {'type': 'string'}},
        'conclusions': {'type': 'string'},
        'limitations': {'type': 'array', 'items': {'type': 'string'}},
        'future_work': {'type': 'string'},
        'references_count': {'type': 'integer'}
      },
      'required': ['title', 'authors', 'abstract', 'key_findings']
    }
  }
}
```

**Insurance Policy Schema:**
```sql
{
  'response_format': {
    'type': 'json',
    'schema': {
      'type': 'object',
      'properties': {
        'policy_number': {'type': 'string'},
        'policy_holder': {'type': 'string'},
        'insurer': {'type': 'string'},
        'policy_type': {'type': 'string', 'enum': ['life', 'health', 'auto', 'property', 'liability', 'other']},
        'effective_date': {'type': 'string'},
        'expiration_date': {'type': 'string'},
        'premium': {'type': 'object', 'properties': {'amount': {'type': 'number'}, 'frequency': {'type': 'string'}}},
        'coverage': {
          'type': 'array',
          'items': {
            'type': 'object',
            'properties': {
              'coverage_type': {'type': 'string'},
              'limit': {'type': 'string'},
              'deductible': {'type': 'string'}
            }
          }
        },
        'exclusions': {'type': 'array', 'items': {'type': 'string'}},
        'beneficiaries': {'type': 'array', 'items': {'type': 'string'}},
        'special_conditions': {'type': 'array', 'items': {'type': 'string'}}
      },
      'required': ['policy_number', 'policy_holder', 'insurer', 'coverage']
    }
  }
}
```

**Loan Agreement Schema:**
```sql
{
  'response_format': {
    'type': 'json',
    'schema': {
      'type': 'object',
      'properties': {
        'loan_number': {'type': 'string'},
        'borrower': {'type': 'string'},
        'lender': {'type': 'string'},
        'principal_amount': {'type': 'number'},
        'currency': {'type': 'string'},
        'interest_rate': {'type': 'object', 'properties': {'rate': {'type': 'number'}, 'type': {'type': 'string', 'enum': ['fixed', 'variable']}}},
        'loan_term': {'type': 'object', 'properties': {'duration': {'type': 'integer'}, 'unit': {'type': 'string'}}},
        'start_date': {'type': 'string'},
        'maturity_date': {'type': 'string'},
        'payment_schedule': {'type': 'string'},
        'collateral': {'type': 'array', 'items': {'type': 'string'}},
        'covenants': {'type': 'array', 'items': {'type': 'string'}},
        'default_conditions': {'type': 'array', 'items': {'type': 'string'}},
        'prepayment_terms': {'type': 'string'}
      },
      'required': ['loan_number', 'borrower', 'lender', 'principal_amount', 'interest_rate']
    }
  }
}
```

**Comparison: Chunking vs Full-Document Approach:**

| Aspect | Chunking (Option B) | Full Document (Option C) |
|--------|---------------------|--------------------------|
| Max pages | Unlimited (125-page chunks) | 500 pages |
| Context preservation | Limited (per chunk) | Full document context |
| Cross-references | May miss | Preserved |
| Best for | Independent pages (invoices) | Interconnected content (contracts) |
| Result aggregation | Required | Not needed |
| Processing complexity | Higher (multiple stages) | Simpler (single pass) |
| Use AI_EXTRACT | Yes (per chunk) | No (AI_COMPLETE instead) |

---

**Ask** user for pipeline parameters:
```
Configure your pipeline:
1. Warehouse name for processing: [default: current warehouse]
2. Schedule frequency: 
   - Every 1 minute
   - Every 5 minutes (recommended)
   - Every 15 minutes
   - Every hour
3. File pattern to match: [default: %.pdf]
```

#### 2.5h: Proceed to Full Batch Extraction

**Only reached if user explicitly selects "Extract from all files".**

1. **Confirm** the final responseFormat with user
2. **Load** `ai-extract/SKILL.md` with:
   - Validated responseFormat
   - Stage path
   - File pattern (if batch)
3. Skip schema definition in ai-extract (already done)

**Example handoff context:**
```
Proceeding to full extraction with validated schema:

Stage: @db.schema.stage
File pattern: %.pdf
Validated responseFormat:
{
  'invoice_number': 'What is the invoice or bill number shown at the top of the document?',
  'vendor_name': 'What is the name of the company or vendor issuing this invoice?',
  'total_amount': 'What is the final total amount due, including taxes?'
}

Test results confirmed accurate on: sample_invoice.pdf
```

### Step 2.6: Visual Analysis (For Charts, Blueprints, Diagrams)

**Only applies when user selected "Images and visual content for analysis".**

Visual Analysis uses AI_COMPLETE directly to analyze images. No parsing step is needed - AI_COMPLETE is a vision model that can directly interpret image files.

**IMPORTANT:** AI_COMPLETE requires image files (PNG, JPEG, etc.). If the user has a PDF, it must be converted to images first.

#### 2.6a: Check File Format

**Ask** user:
```
What format is your file?
Options:
1. Image file (PNG, JPEG, TIFF, BMP, GIF, WEBP)
2. PDF file (needs conversion to image)
```

---

#### If Image File: Proceed Directly to Analysis

```sql
-- Direct visual analysis with AI_COMPLETE
SELECT AI_COMPLETE(
  'claude-3-5-sonnet',
  [
    {
      'role': 'user',
      'content': [
        {'type': 'image', 'image_url': {'url': TO_FILE('@db.schema.stage', 'chart.png')}},
        {'type': 'text', 'text': 'Analyze this chart/diagram. Describe what you see and extract key information.'}
      ]
    }
  ],
  {'max_tokens': 4096}
) AS analysis;
```

---

#### If PDF File: Convert to Image First

**Step 1: Create the PDF-to-Image conversion stored procedure**

This procedure converts PDF pages to images using pdf2image and uploads them to an images stage:

```sql
-- Create stage for converted images (with server-side encryption)
CREATE STAGE IF NOT EXISTS db.schema.images_stage
  DIRECTORY = (ENABLE = TRUE)
  ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')
  COMMENT = 'Stage for PDF-to-image converted files';

-- Create PDF to image conversion stored procedure
CREATE OR REPLACE PROCEDURE db.schema.convert_pdf_to_images(
    stage_name STRING, 
    file_name STRING, 
    dest_stage_name STRING,
    dpi INT DEFAULT 200,
    image_format STRING DEFAULT 'PNG',
    specific_pages ARRAY DEFAULT NULL
)
RETURNS VARIANT
LANGUAGE PYTHON
RUNTIME_VERSION = '3.9'
PACKAGES = ('snowflake-snowpark-python', 'pdf2image', 'pillow')
HANDLER = 'run'
AS
$
from pdf2image import convert_from_bytes
from snowflake.snowpark import Session
from snowflake.snowpark.file_operation import FileOperation
from io import BytesIO
import os

def run(session: Session, stage_name: str, file_name: str, dest_stage_name: str, 
        dpi: int = 200, image_format: str = 'PNG', specific_pages: list = None) -> dict:
    result = {
        "status": "success",
        "source_file": file_name,
        "total_pages": 0,
        "images_created": 0,
        "image_files": []
    }
    
    try:
        # Download PDF from stage
        file_url = f"{stage_name}/{file_name}"
        get_result = session.file.get(file_url, '/tmp/')
        file_path = os.path.join('/tmp/', file_name)
        
        if not os.path.exists(file_path):
            return {"status": "error", "message": f"File {file_name} not found in {stage_name}"}

        with open(file_path, 'rb') as f:
            pdf_data = f.read()
        
        # Convert PDF to images
        # If specific_pages provided, only convert those pages (1-indexed)
        if specific_pages:
            images = convert_from_bytes(
                pdf_data, 
                dpi=dpi, 
                fmt=image_format.lower(),
                first_page=min(specific_pages),
                last_page=max(specific_pages)
            )
            # Filter to only requested pages
            page_indices = [p - min(specific_pages) for p in specific_pages]
            images = [images[i] for i in page_indices if i < len(images)]
        else:
            images = convert_from_bytes(pdf_data, dpi=dpi, fmt=image_format.lower())
        
        result["total_pages"] = len(images)
        
        # Get base filename without extension
        base_name = os.path.splitext(file_name)[0]
        ext = image_format.lower()
        if ext == 'jpeg':
            ext = 'jpg'
        
        for i, image in enumerate(images):
            page_num = specific_pages[i] if specific_pages else i + 1
            
            # Create image filename: original_page_1.png
            image_filename = f'{base_name}_page_{page_num}.{ext}'
            image_file_path = os.path.join('/tmp/', image_filename)
            
            # Save image
            image.save(image_file_path, format=image_format.upper())
            
            if not os.path.exists(image_file_path):
                return {"status": "error", "message": f"Failed to create image {image_filename}"}

            # Upload to destination stage
            FileOperation(session).put(
                f"file://{image_file_path}",
                dest_stage_name,
                auto_compress=False
            )
            
            result["image_files"].append({
                "page_number": page_num,
                "filename": image_filename,
                "format": image_format.upper()
            })
            result["images_created"] += 1
            
            # Clean up temp image file
            os.remove(image_file_path)
        
        # Clean up original temp file
        os.remove(file_path)
            
        return result
        
    except Exception as e:
        return {"status": "error", "message": str(e)}
$;
```

**Step 2: Ask which pages to convert**

```
Which pages of the PDF contain the charts/diagrams you want to analyze?
Options:
1. Convert all pages to images
2. Convert specific pages (e.g., 1, 3, 5)
3. Convert a page range (e.g., pages 1-10)
4. Convert just the first page to test
```

**Step 3: Convert PDF to images**

```sql
-- Convert specific pages (e.g., pages 1, 3, 5)
CALL db.schema.convert_pdf_to_images(
  '@db.schema.doc_stage',
  'blueprint.pdf',
  '@db.schema.images_stage',
  200,           -- DPI (higher = better quality, larger files)
  'PNG',         -- Format: PNG, JPEG
  [1, 3, 5]      -- Specific pages (1-indexed), or NULL for all pages
);

-- Convert all pages
CALL db.schema.convert_pdf_to_images(
  '@db.schema.doc_stage',
  'blueprint.pdf',
  '@db.schema.images_stage',
  200,
  'PNG',
  NULL           -- NULL = convert all pages
);
```

**Step 4: Verify converted images**

```sql
-- Refresh stage directory
ALTER STAGE db.schema.images_stage REFRESH;

-- List converted images
SELECT * FROM DIRECTORY(@db.schema.images_stage)
WHERE relative_path LIKE 'blueprint_%'
ORDER BY relative_path;
```

**Step 5: Analyze images with AI_COMPLETE**

```sql
-- Analyze a single converted image
SELECT AI_COMPLETE(
  'claude-3-5-sonnet',
  [
    {
      'role': 'user',
      'content': [
        {'type': 'image', 'image_url': {'url': TO_FILE('@db.schema.images_stage', 'blueprint_page_1.png')}},
        {'type': 'text', 'text': 'Analyze this blueprint/diagram. Identify all components, measurements, and annotations.'}
      ]
    }
  ],
  {'max_tokens': 4096}
) AS analysis;
```

---

#### 2.6b: Visual Analysis Prompts

**Ask** user what they want to analyze:

```
What would you like to analyze in the image?
Options:
1. Charts/graphs - extract data points, trends, labels
2. Blueprints/technical drawings - identify components, measurements
3. Diagrams/flowcharts - describe structure, relationships
4. General visual content - describe what you see
5. Custom analysis - I'll describe what I need
```

**Prompt templates by type:**

**Charts/Graphs:**
```sql
SELECT AI_COMPLETE(
  'claude-3-5-sonnet',
  [
    {
      'role': 'user',
      'content': [
        {'type': 'image', 'image_url': {'url': TO_FILE('@stage', 'chart.png')}},
        {'type': 'text', 'text': 'Analyze this chart. Extract:
1. Chart type (bar, line, pie, etc.)
2. Title and axis labels
3. All data points with their values
4. Key trends or insights
5. Any annotations or legends

Format the data points as a table if possible.'}
      ]
    }
  ],
  {'max_tokens': 4096}
) AS chart_analysis;
```

**Blueprints/Technical Drawings:**
```sql
SELECT AI_COMPLETE(
  'claude-3-5-sonnet',
  [
    {
      'role': 'user',
      'content': [
        {'type': 'image', 'image_url': {'url': TO_FILE('@stage', 'blueprint.png')}},
        {'type': 'text', 'text': 'Analyze this technical drawing/blueprint. Identify:
1. All labeled components and parts
2. Dimensions and measurements with units
3. Materials specifications if shown
4. Assembly instructions or notes
5. Scale information
6. Any warnings or special instructions'}
      ]
    }
  ],
  {'max_tokens': 4096}
) AS blueprint_analysis;
```

**Diagrams/Flowcharts:**
```sql
SELECT AI_COMPLETE(
  'claude-3-5-sonnet',
  [
    {
      'role': 'user',
      'content': [
        {'type': 'image', 'image_url': {'url': TO_FILE('@stage', 'diagram.png')}},
        {'type': 'text', 'text': 'Analyze this diagram/flowchart. Describe:
1. Overall purpose of the diagram
2. All nodes/boxes and their labels
3. Connections and relationships between elements
4. Flow direction and sequence
5. Decision points and branches
6. Start and end points'}
      ]
    }
  ],
  {'max_tokens': 4096}
) AS diagram_analysis;
```

**General Visual Analysis:**
```sql
SELECT AI_COMPLETE(
  'claude-3-5-sonnet',
  [
    {
      'role': 'user',
      'content': [
        {'type': 'image', 'image_url': {'url': TO_FILE('@stage', 'image.png')}},
        {'type': 'text', 'text': 'Describe this image in detail. Include all visible text, numbers, symbols, and visual elements.'}
      ]
    }
  ],
  {'max_tokens': 4096}
) AS visual_analysis;
```

---

#### 2.6c: Batch Visual Analysis

For analyzing multiple images:

```sql
-- Analyze all images in a stage
SELECT 
  relative_path AS image_file,
  AI_COMPLETE(
    'claude-3-5-sonnet',
    [
      {
        'role': 'user',
        'content': [
          {'type': 'image', 'image_url': {'url': TO_FILE('@db.schema.images_stage', relative_path)}},
          {'type': 'text', 'text': 'Analyze this chart and extract all data points.'}
        ]
      }
    ],
    {'max_tokens': 4096}
  ) AS analysis
FROM DIRECTORY(@db.schema.images_stage)
WHERE relative_path LIKE '%.png' OR relative_path LIKE '%.jpg';
```

---

#### 2.6d: Store Visual Analysis Results

```sql
-- Create table for visual analysis results
CREATE TABLE IF NOT EXISTS db.schema.visual_analysis_results (
  result_id INT AUTOINCREMENT,
  image_path STRING,
  source_pdf STRING,           -- Original PDF if converted from PDF
  page_number INT,             -- Page number if converted from PDF
  analysis_type STRING,        -- chart, blueprint, diagram, general
  analysis_result VARIANT,
  analyzed_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Insert analysis result
INSERT INTO db.schema.visual_analysis_results (image_path, source_pdf, page_number, analysis_type, analysis_result)
SELECT 
  'blueprint_page_1.png',
  'blueprint.pdf',
  1,
  'blueprint',
  PARSE_JSON(AI_COMPLETE(
    'claude-3-5-sonnet',
    [
      {
        'role': 'user',
        'content': [
          {'type': 'image', 'image_url': {'url': TO_FILE('@db.schema.images_stage', 'blueprint_page_1.png')}},
          {'type': 'text', 'text': 'Analyze this blueprint. Return a JSON object with keys: components (array), measurements (array), materials (array), notes (string).'}
        ]
      }
    ],
    {'max_tokens': 4096}
  ));
```

### Step 3: Post-Processing Options

After extraction/parsing is complete, **ask** user:

```
What would you like to do next?
Options:
1. Done - one-time extraction
2. Store results in a Snowflake table
3. Set up a pipeline for continuous processing
4. Build RAG/search integration
```

**If pipeline setup requested:**
```sql
-- Create stream on stage
CREATE OR REPLACE STREAM doc_stream ON STAGE @my_stage;

-- Create task for continuous processing
CREATE OR REPLACE TASK process_docs
  WAREHOUSE = my_warehouse
  SCHEDULE = '1 MINUTE'
WHEN SYSTEM$STREAM_HAS_DATA('doc_stream')
AS
  INSERT INTO extracted_data
  SELECT ... FROM doc_stream;
```

## Key Constraints

| Constraint | AI_EXTRACT | AI_PARSE_DOCUMENT |
|------------|------------|-------------------|
| Max file size | 100 MB | 50 MB |
| Max pages | 125 | 500 |
| Output format | JSON | Markdown |

## Stopping Points

- After Step 1 if file format is unsupported
- After Step 2 before routing to sub-skill
- After extraction completes for post-processing choice

## Output

Routes user to appropriate sub-skill with gathered context, then assists with post-processing.
