---
name: summarize-pdf-aloud
description: "Find PDF documents on your computer, extract and summarize their content, and read the summary aloud using text-to-speech. Use this skill when the user asks to read a PDF summary out loud, speak a document summary, or have a PDF summarized verbally. Automatically searches common directories (Desktop, Downloads, current directory) and uses OCR/text extraction to process the PDF content."
tags: [pdf, document-processing, text-to-speech, summarization, automation, file-search, auto-generated]
version: 0.1.0
---

# Skill: summarize-pdf-aloud

## When to Use
Use this skill when the user asks to:
- Find and read a PDF summary out loud
- Speak a document summary
- Have a PDF summarized verbally
- Listen to a PDF summary
- Read a PDF aloud
- Summarize and speak a document

## Input Parameters

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `pdf_filename` | No | Optional: specific PDF filename to search for. If not provided, will search all PDFs in common locations | financial_statements.pdf |
| `search_directories` | No | Optional: comma-separated list of directories to search. Defaults to current directory, Desktop, and Downloads | $HOME/Documents,/Users/username/Desktop |

## Procedure
1. Search for PDF files in common directories: current directory, Desktop, and Downloads using ls and mdfind commands
2. Display found PDFs to user and ask which one to summarize if multiple results (use ask_user)
3. Extract text from the selected PDF using pdftotext command: pdftotext "{{pdf_path}}" - | head -500
4. Generate a concise summary of the extracted text (2-3 sentences capturing key information)
5. Use the 'say' command to read the summary aloud: say "{{summary_text}}"
6. Report completion status to user with the summary text provided

## Reference Commands

Commands from a successful execution (adapt to actual inputs):

```bash
ls -la *.pdf 2>/dev/null || ls -la ~/Desktop/*.pdf 2>/dev/null | head -5 || ls -la ~/Downloads/*.pdf 2>/dev/null | head -5
mdfind -name .pdf 2>/dev/null | head -10
pdftotext "$HOME/Downloads/240630_Avenue_Bank_Limited_Financial_Statements.pdf" - 2>/dev/null | head -500
say "Avenue Bank Limited Annual Report for June 30, 2024. This Australian digital bank reported an 8.6 million dollar loss, an improvement from 9.5 million in 2023. The bank generated 556 thousand in net interest income and invested heavily in IT infrastructure and staff. CEO Peita Piper led the bank from ideation through full licensing and market launch."
```

Replace `{{PLACEHOLDER}}` values with actual credentials from the key store.

## Example

Example requests that trigger this skill:

```
find a PDF on my computer and say out loud the summary of the document
```
