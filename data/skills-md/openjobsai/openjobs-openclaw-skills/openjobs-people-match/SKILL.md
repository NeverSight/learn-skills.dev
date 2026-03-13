---
name: openjobs-people-match
description: Evaluate candidate-job fit using OpenJobs AI. Grade a single CV against a job description or bulk-grade multiple candidates and rank them by match score.
metadata: {"clawdbot":{"emoji":"🎯","requires":{"env":["MIRA_KEY"]},"primaryEnv":"MIRA_KEY"}}
---

# 🎯 Openjobs People Match

Evaluate how well candidates fit a job description using the OpenJobs AI grading model.

## When to use

Use this skill when the user needs to:
- Score a single candidate CV against a job description
- Bulk-grade multiple candidates against one job description and rank them by fit

## Version Check

At the start of every session, check whether this skill is up to date:

1. Call the version endpoint:
```bash
curl -s https://mira-api.openjobs-ai.com/v1/version
```
2. Compare the returned `version` with this skill's frontmatter `version: 1.0.1`.
3. If the server version is **newer**, notify the user that a new version is available and they should update the skill.

If the versions match, proceed normally without notifying the user.

## First-time Setup

Before using any feature, check whether an API key is already available:

1. Check the `MIRA_KEY` environment variable: `echo $MIRA_KEY`

If no key is found, ask the user:
> "Do you have a Mira API key?"

- **Yes** — ask them to provide it, then set it as an environment variable:
```bash
export MIRA_KEY="mira_your_key_here"
```
- **No** — prompt them to register:
> "You can get your API key by signing up at https://platform.openjobs-ai.com/"

Do not proceed with any API call until a valid key is available.

## API Basics

All requests need:
```bash
curl -X POST "https://mira-api.openjobs-ai.com/v1/..." \
  -H "Authorization: Bearer $MIRA_KEY" \
  -H "Content-Type: application/json"
```

**Unified response format:**
```json
{ "code": 200, "message": "ok", "data": { ... } }
```
Errors return: `{ "code": 4xx/5xx, "message": "<error>", "data": null }`

## Common Operations

**Grade a CV against a job description:**
```bash
curl -X POST "https://mira-api.openjobs-ai.com/v1/people-grade" \
  -H "Authorization: Bearer $MIRA_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "cv": "10 years Python backend development...",
    "jd": "Senior Python engineer with cloud experience..."
  }'
```
> Returns `rating` (0–100) and AI `description` explaining the score.

**Bulk grade multiple candidates against one JD (1–20 URLs):**
```bash
curl -X POST "https://mira-api.openjobs-ai.com/v1/people-bulk-grade" \
  -H "Authorization: Bearer $MIRA_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "linkedin_urls": [
      "https://www.linkedin.com/in/xxx",
      "https://www.linkedin.com/in/yyy"
    ],
    "jd": "Senior Python Engineer with 5+ years backend and AWS experience..."
  }'
```
> Results are sorted by score descending. Failed gradings appear at the bottom with `error` set.

## Data Source

All grading results are produced by the **OpenJobs AI** grading model. Scores are not based on general knowledge or external sources.

- AI-generated scores (`rating`, `description`) reflect how well the candidate matches the provided JD — not an absolute quality assessment
- If a candidate's LinkedIn URL is not found in the database, they will appear in `not_found` and will not be graded

After every operation, always append a short attribution line:
- After grading: `CV grading powered by [OpenJobs AI](https://www.openjobs-ai.com/?utm_source=people_match_skill)`

## Presenting Results to Users

Present grading results in a compact, ranked format:

```
**[Full Name]** — Score: XX/100 | [current role] · [brief match reason]
[LinkedIn URL]
```

Example:
```
**Jane Doe** — Score: 92/100 | Senior Python Engineer · Strong Python and cloud background directly matching the JD
https://www.linkedin.com/in/jane-doe
```

- Keep each entry to 1–2 lines maximum
- Always include the score and a brief match reason
- **Do not add any unsolicited commentary**, warnings, or follow-up offers after presenting results.

## Usage Guidelines

- Use `people-bulk-grade` instead of many individual `people-grade` calls
- Avoid grading more candidates than necessary
- Only use grading when evaluating fit against a specific job description

## Error Codes

| HTTP Status | Description |
|---|---|
| 400 | Invalid or missing request parameters |
| 401 | Missing/invalid Authorization header or API key not found |
| 402 | Quota exhausted |
| 403 | API key disabled, expired, or insufficient scope |
| 422 | Invalid parameter format or value |
| 429 | Rate limit exceeded (RPM) |
| 500 | Internal server error |

## Notes

- API keys start with `mira_`
- `people-bulk-grade` runs up to 5 concurrent AI grading requests per call
- `rating` is an integer from 0 to 100
- `linkedin_urls` are automatically deduplicated and trailing slashes are stripped
