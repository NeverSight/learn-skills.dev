---
name: find-funding-opportunities
description: Search the Karma Funding Map for funding programs (grants, hackathons, bounties, accelerators, VC funds, RFPs) via the public API. Use when user says "find grants", "search hackathons", "look for bounties", "explore funding", "programs on Optimism", "what can I apply to", "funding opportunities", or asks about programs over or under a budget.
version: 1.2.0
tags: [programs, search, funding, discovery]
metadata:
  author: Karma
  category: discovery
---

# Funding Program Finder

Search the Karma Funding Map for funding programs via the public API.

The registry has 6 program types: grants, hackathons, bounties, accelerators, VC funds, and RFPs. Use "programs" / "opportunities" / "funding" — not just "grants".

For full API parameters, response shape, and known values, see [references/api-reference.md](references/api-reference.md).

## Workflow

### Step 1: Map the User's Request

| User says | Maps to |
|-----------|---------|
| "Ethereum programs" | `ecosystems=Ethereum` + ecosystem search strategy |
| "hackathons" | `type=hackathon` |
| "hackathons on Ethereum" | `type=hackathon` + ecosystem search strategy |
| "bounties on Solana" | `type=bounty` + ecosystem search strategy |
| "bounties over $500" | `type=bounty&minGrantSize=500` |
| "accelerator programs" | `type=accelerator` |
| "VCs investing in DeFi" | `type=vc_fund&name=DeFi` |
| "open RFPs from Optimism" | `type=rfp&organization=Optimism` |
| "grants and hackathons on Ethereum" | `type=grant,hackathon` + ecosystem search strategy |
| "DeFi funding on Optimism" | `name=DeFi` + ecosystem search strategy |
| "programs over $50K" | `minGrantSize=50000` |
| "funding under $100K" | `maxGrantSize=100000` |
| "infrastructure" | `name=infrastructure` |
| "active programs" | `status=active` |
| "retroactive funding on Optimism" | `categories=Retroactive%20Funding` + ecosystem search strategy |
| "programs on Karma" | `onlyOnKarma=true` |
| "what's closing this week" | `sortField=endsAt&sortOrder=asc&status=active` |
| (no query) | Ask what they're looking for |

Budget shorthand: K→000, M→000000 (e.g., $50K → 50000, $1M → 1000000).

**URL encoding:** Values with spaces must be percent-encoded in `curl` URLs (e.g., `categories=Retroactive%20Funding`).

### Step 2: Ecosystem Search Strategy

If the query has **no ecosystem** component, skip this step and go to Step 3.

The `ecosystems` metadata field is often empty — many programs are linked to an ecosystem only via the `communities` field. Use a two-phase approach:

**Phase 1 — Try `ecosystems=` first:**
Query with `ecosystems={name}`. If this returns sufficient results (5+), present them and move to Step 4.

**Phase 2 — Enrich with community lookup (only if Phase 1 is sparse):**
If Phase 1 returned fewer than 5 results, run these two additional queries and merge:
1. **Community UID lookup**: fetch all communities from `GET /v2/communities?limit=100`, find the best match by comparing against community names (case-insensitive, partial match), then query with `communityUid={uid}`
2. **`name={name}`** — text search on title, universal fallback

Deduplicate all merged results by `id` before presenting.

### Step 3: Build and Execute the Request

Use `curl` via Bash. **CRITICAL: Every request must include the tracking headers below. Never omit them.**

Before the first request, generate a tracking ID:

```bash
INVOCATION_ID=$(uuidgen)
```

Every `curl` call must include these query defaults and tracking headers (see [references/api-reference.md](references/api-reference.md) for details):

```
# Query defaults (override sortField=endsAt&sortOrder=asc for deadline queries)
isValid=accepted&limit=10&sortField=updatedAt&sortOrder=desc

# Required headers — include on every request
# Read the version from this skill's frontmatter metadata.version
-H "X-Source: skill:find-funding-opportunities"
-H "X-Invocation-Id: $INVOCATION_ID"
-H "X-Skill-Version: {metadata.version}"
```

```bash
# No ecosystem
curl -s -H "X-Source: skill:find-funding-opportunities" -H "X-Invocation-Id: $INVOCATION_ID" -H "X-Skill-Version: {metadata.version}" \
  "https://gapapi.karmahq.xyz/v2/program-registry/search?isValid=accepted&limit=10&sortField=updatedAt&sortOrder=desc&type=hackathon"

# Ecosystem — Phase 1
curl -s -H "X-Source: skill:find-funding-opportunities" -H "X-Invocation-Id: $INVOCATION_ID" -H "X-Skill-Version: {metadata.version}" \
  "https://gapapi.karmahq.xyz/v2/program-registry/search?isValid=accepted&limit=10&sortField=updatedAt&sortOrder=desc&ecosystems=Ethereum"

# Ecosystem — Phase 2 (only if Phase 1 returned < 5 results)
curl -s -H "X-Source: skill:find-funding-opportunities" -H "X-Invocation-Id: $INVOCATION_ID" -H "X-Skill-Version: {metadata.version}" \
  "https://gapapi.karmahq.xyz/v2/communities?limit=100"
# Match community UID from response, then:
curl -s -H "X-Source: skill:find-funding-opportunities" -H "X-Invocation-Id: $INVOCATION_ID" -H "X-Skill-Version: {metadata.version}" \
  "https://gapapi.karmahq.xyz/v2/program-registry/search?isValid=accepted&limit=10&sortField=updatedAt&sortOrder=desc&communityUid={uid}"
curl -s -H "X-Source: skill:find-funding-opportunities" -H "X-Invocation-Id: $INVOCATION_ID" -H "X-Skill-Version: {metadata.version}" \
  "https://gapapi.karmahq.xyz/v2/program-registry/search?isValid=accepted&limit=10&sortField=updatedAt&sortOrder=desc&name=Ethereum"
```

### Step 4: Format Results

Include the program type in each result. Adapt the detail line based on type:

```
Found 42 programs (showing top 10):

1. **Optimism Grants** [grant] — Optimism
   Retroactive and proactive funding for Optimism builders
   Budget: $10M | Status: Active
   Apply: https://app.charmverse.io/...

2. **ETHDenver 2026** [hackathon] — Ethereum
   Annual Ethereum hackathon and conference
   Dates: Mar 1–7, 2026 | Deadline: Feb 15, 2026
   Apply: https://ethdenver.com/apply

3. **Rust Smart Contract Audit** [bounty] — Solana
   Audit Solana program for vulnerabilities
   Reward: $5,000 | Difficulty: Advanced
   Apply: https://superteam.fun/...

Showing 10 of 42. Ask for more or narrow your search.
```

#### Field Mapping

- **Name**: `metadata.title` (fall back to `name`)
- **Type label**: `type` in brackets: `[grant]`, `[hackathon]`, `[bounty]`, `[accelerator]`, `[vc_fund]`, `[rfp]`
- **Ecosystem**: `metadata.ecosystems` joined with `, ` (fall back to `communities[0].name`)
- **Description**: `metadata.description` truncated to ~120 chars

#### Type-Specific Detail Line

- **grant**: `Budget: {programBudget} | Status: {status}`
- **hackathon**: `Dates: {startsAt}–{endsAt} | Deadline: {deadline}`
- **bounty**: `Reward: {programBudget} | Difficulty: {difficulty if available}`
- **accelerator**: `Stage: {stage if available} | Deadline: {deadline}`
- **vc_fund**: `Check size: {minGrantSize}–{maxGrantSize} | Stage: {stage if available}`
- **rfp**: `Budget: {programBudget} | Org: {organizations[0]} | Deadline: {deadline}`
- **fallback**: `Budget: {programBudget} | Status: {status}`

#### Common Fields

- **Deadline**: `deadline` (top-level) formatted as `Mon DD, YYYY` (or "Rolling" if null)
- **Apply link**: `submissionUrl` (top-level), fall back to `metadata.socialLinks.grantsSite` or `metadata.website` or `metadata.socialLinks.website` (first non-empty)

## Edge Cases

| Scenario | Response |
|----------|----------|
| No results | If the user specified an ecosystem, run the full ecosystem search strategy (Phase 1 + Phase 2) before giving up. If no ecosystem was specified, broaden non-ecosystem filters first (remove type, budget, or keyword filters). If still none: "No programs found matching your criteria. Try broadening — remove type, ecosystem, or budget filters." |
| No query | Ask: "What kind of funding are you looking for? I can search grants, hackathons, bounties, accelerators, VC funds, and RFPs — filtered by ecosystem, budget, category, or keywords." |
| "more results" / "page 2" | Re-run with `page=2` |
| API returns empty `programs` array | Check if filters are too narrow. Suggest removing one filter at a time. |
| API response missing expected fields | Use fallback values: show "N/A" for missing budget, "Rolling" for missing deadline, skip missing description. Never fail on a missing optional field. |

## Error Handling

| Error | Cause | Action |
|-------|-------|--------|
| HTTP 5xx | API server issue | "The Karma API is temporarily unavailable. Try again in a moment." |
| HTTP 429 | Rate limiting | Wait 5 seconds, retry once. If it fails again, tell the user to wait. |
| Connection timeout | Network or API down | "Could not reach the Karma API. Check your connection or try again shortly." |
| Malformed JSON response | Unexpected API change | "Got an unexpected response from the API. The response format may have changed." |
| Community lookup returns no match | User's ecosystem name doesn't match any community | Fall back to `ecosystems=` and `name=` queries only. Do not fail — partial results are better than none. |

## Troubleshooting

### Ecosystem search returns 0 results
The user asked for an ecosystem (e.g., "Monad grants") but all 3 queries returned nothing.
- Verify the ecosystem name against the known values in `references/api-reference.md`
- Try a broader `name=` search with just the keyword
- The ecosystem may genuinely have no programs listed yet — tell the user

### Community UID lookup finds no match
The community list (~48 entries) doesn't contain a match for the user's query.
- Try partial matching: "OP" should match "Optimism"
- Try without the community query — `ecosystems=` and `name=` may still return results
- Do not block on this — proceed with the other two queries

### Results look stale or incomplete
Programs may have outdated metadata (missing budgets, old deadlines).
- Present what's available; do not hide results with missing fields
- Use "N/A" or "Rolling" for missing values
- Note to the user: "Some programs may have incomplete information"
