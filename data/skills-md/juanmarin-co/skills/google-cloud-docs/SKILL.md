---
name: google-cloud-docs
description: Use when official Google Cloud documentation is needed.
---

Google Developer Knowledge provides searchable official Google Cloud documentation as JSON containing Markdown.

## REST API

Service URL: `https://developerknowledge.googleapis.com`

`answerQuery` synthesizes a direct answer from multiple documents. `searchDocumentChunks` returns ranked source excerpts without answering the question. Use `answerQuery` for broad guidance and `searchDocumentChunks` when exact documented details or direct source inspection matter.

### Answer a question

`POST /v1:answerQuery`

JSON body:

```json
{"query":"QUESTION"}
```

Returns a synthesized answer with citations and source excerpts.

### Search documentation

`GET /v1/documents:searchDocumentChunks`

Query parameters:

- `query`: required search terms. Prefer two to five precise terms.
- `filter`: optional source filter, such as `data_source = "docs.cloud.google.com"`.
- `pageSize`: optional result limit.
- `pageToken`: optional continuation token.

Returns ranked excerpts with their source documents and an optional continuation token.

### Retrieve one document

`GET /v1/documents/{uri_without_scheme}`

Convert a documentation URI such as `https://docs.cloud.google.com/run/docs/overview/what-is-cloud-run` to `documents/docs.cloud.google.com/run/docs/overview/what-is-cloud-run`. Use the optional `view` query parameter to select the returned fields.

### Retrieve several documents

`GET /v1/documents:batchGet`

Repeat the `names` query parameter for each resource name, up to 20 documents. Each value has the form `documents/{uri_without_scheme}`. Use the optional `view` query parameter to select the returned fields.

### `view` parameter

Both single and batch retrieval accept these values:

- `DOCUMENT_VIEW_BASIC`: metadata only; use when identifying documents.
- `DOCUMENT_VIEW_CONTENT`: metadata and Markdown content; use when reading documents. This is the default.
- `DOCUMENT_VIEW_FULL`: every available document field; use only when fields beyond metadata and content are needed.

## Authentication

Try configured credentials in this order:

1. Get an access token from `gcloud auth print-access-token`. Send it as `Authorization: Bearer TOKEN` and send the project from `gcloud config get-value project` as `X-Goog-User-Project: PROJECT_ID`.
2. If that credential is rejected, retry with a token from `gcloud auth application-default print-access-token`.
3. If `DEVELOPERKNOWLEDGE_API_KEY` or `GOOGLE_API_KEY` is set, send it as the `key` query parameter or `X-Goog-Api-Key` header.
