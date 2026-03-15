---
name: remix-glossary
description: Glossary of terms used in Remix agent publishing flows
metadata:
  tags: remix, glossary
---

# Glossary

| Term | Definition |
|------|------------|
| API Key | User-generated key from `https://remix.gg/api-keys` used for bearer auth (`Authorization: Bearer <api_key>`). |
| Draft | Editable game version state used by the agent REST flow. |
| Validation | Readiness checks for metadata + SDK hooks. |
| Blocker | Machine-readable issue returned from `GET /v1/games/{gameId}/versions/{versionId}/validate`. |
| Launch Readiness | Aggregate readiness payload from `GET /v1/games/{gameId}/launch-readiness`, including `status`, `valid`, and `readyForSubmission`. |
| Thread Context | Version thread payload from `GET /v1/games/{gameId}/versions/{versionId}/thread` with `threadId` and resolved HTML. |
| Status | Version state from `status` endpoint: `draft`, `blocked`, `review`, `approved`, or `live`. |
| Live Version | The currently launched version; cannot be modified by agent REST code updates. |
