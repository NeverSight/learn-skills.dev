---
name: analyze-document
description: "Analyze and provide detailed feedback on documents including PDFs, text files, and other formats. Use this skill when the user asks for your thoughts on a document, wants a review, analysis, summary, critique, or evaluation of any written material. Supports document upload, file path references, or direct text content."
---

# Analyze Document

## Input Parameters

| Parameter         | Required | Description                                                                         | Example                                      |
| ----------------- | -------- | ----------------------------------------------------------------------------------- | -------------------------------------------- |
| `document_source` | Yes      | The document to analyze — can be a file path, uploaded file, or direct text content | /path/to/document.pdf or direct text content |

## Procedure

1. If no document is provided, ask the user to either upload the file, provide a file path, or share the text content directly
2. Read the document using appropriate tools (`read_file` for text files; PDF extraction for PDFs)
3. Analyze structure, content, clarity, and relevance — provide feedback on strengths, areas for improvement, and key observations

## Notes

- Always obtain document content before beginning analysis
- Provide constructive, balanced feedback

## Example

```
what do you think of this document?
review this PDF and give me your thoughts
summarize and critique this document
give me detailed feedback on this report
can you analyze this text for me
```
