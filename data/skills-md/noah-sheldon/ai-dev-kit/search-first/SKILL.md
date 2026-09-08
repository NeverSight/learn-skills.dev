---
name: search-first
description: Search-first methodology — search before coding discipline, effective search strategies, when to search vs reason, query formulation, result verification, avoiding stale information, cross-referencing, documenting search findings.
origin: AI Dev Kit
---

# Search-First Methodology

Discipline of searching for existing information before reasoning, coding, or making
architectural decisions. Reduces hallucination, avoids reinventing solutions, and
grounds work in verified, current information.

## When to Use

- Before implementing any feature that might have an existing library, pattern, or API.
- Before answering questions about library versions, breaking changes, or deprecations.
- Before designing integrations with third-party services (check their current docs).
- Before diagnosing unfamiliar errors or stack traces.
- Before choosing between technology options (search for recent comparisons).
- When working with technologies that change frequently (frontend frameworks, cloud services).
- Before writing custom implementations of well-known algorithms or patterns.

## Core Concepts

### 1. Search Before Coding — The Golden Rule

```
┌─────────────────────────────────┐
│  User asks a question or       │
│  requests a feature             │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│  SEARCH FIRST                   │
│  1. Local codebase (grep/glob)  │
│  2. Documentation (Context7)    │
│  3. Web search (Exa)            │
│  4. GitHub issues/PRs           │
└──────────────┬──────────────────┘
               │
      ┌────────┴────────┐
      ▼                 ▼
┌──────────┐    ┌──────────────┐
│ Found it │    │ Didn't find  │
│ → Use it │    │ → Reason +   │
└──────────┘    │   implement  │
                └──────────────┘
```

**Why search first:**
- **Avoids hallucination** — LLMs make up API signatures; docs don't
- **Saves time** — existing solutions are faster than building from scratch
- **Ensures accuracy** — library APIs change; search finds the current version
- **Prevents reinvention** — don't write auth middleware if the framework has it

### 2. Effective Search Strategies

**Tiered search approach:**

```python
# Tier 1: Local codebase — is this already solved here?
grep_search("OAuth2 middleware", glob="*.py")
glob("**/*auth*.py")

# Tier 2: Documentation — what does the official source say?
context7_lookup("FastAPI OAuth2 middleware")

# Tier 3: Web search — what does the community know?
exa_search("FastAPI OAuth2 middleware best practices 2025")

# Tier 4: GitHub — are there known issues or discussions?
search_github_issues("FastAPI OAuth2 middleware", repo="tiangolo/fastapi")
```

**When each tier applies:**

| Tier | Source | When to Use |
|---|---|---|
| 1 | Local codebase | "How do we handle X in this project?" |
| 2 | Official docs | "What's the current API for library Y?" |
| 3 | Web search | "What are best practices for Z?" |
| 4 | GitHub/forums | "Are there known bugs with W?" |

### 3. When to Search vs When to Reason

```
Search when:
├── Question is about a specific technology, library, or API
├── Need current version information (version numbers, endpoints)
├── Looking for best practices or community patterns
├── Debugging an unfamiliar error message
├── Evaluating technology choices
└── Need migration guides or breaking change information

Reason when:
├── Designing a novel architecture for your specific constraints
├── Writing original business logic (not library-specific code)
├── Analyzing trade-offs between approaches you already understand
├── Debugging logic errors in your own code
├── Refactoring code structure you're familiar with
└── Deriving algorithms or data structures from first principles
```

### 4. Search Query Formulation

```
# Formula: [Technology] + [Specific Topic] + [Context/Constraint] + [Recency]

# Examples:
"FastAPI dependency injection async generator cleanup"
"PostgreSQL JSONB query performance indexing 2025"
"React Server Components data fetching patterns Next.js 15"
"Stripe webhook signature verification Python"
"AWS Lambda cold start optimization provisioned concurrency"

# Add specificity:
"Pydantic v2" not "Pydantic"       # Version matters
"FastAPI 0.115" not "FastAPI"      # Specific version
"2025" or "2026" for recent info   # Recency signal
"migration" for version upgrades    # Intent signal
"breaking changes" for risk assessment
```

**Query anti-patterns:**

```
# Too vague
"Python auth"
"React performance"
"AWS lambda"

# Too long (keyword soup)
"how to implement oauth2 authentication in fastapi with jwt tokens and refresh tokens and role based access control 2025"

# Better
"FastAPI OAuth2 JWT refresh tokens 2025"
```

### 5. Result Verification

```python
def verify_search_results(
    results: list[dict],
    required_signals: list[str] = None,
) -> list[dict]:
    """Verify that search results actually answer the question."""

    verified = []
    for r in results:
        signals = {
            "is_recent": is_within_days(r.get("date"), 365),
            "has_code": bool(re.search(r"```|def |class |import ", r.get("content", ""))),
            "is_official": any(
                d in r.get("url", "")
                for d in ["docs.", "github.com", "official", ".org/"]
            ),
            "matches_topic": topic_overlap(r.get("content", ""), r.get("query", "")),
        }

        if required_signals:
            if not all(signals.get(s) for s in required_signals):
                continue

        r["verification"] = signals
        r["verification_score"] = sum(signals.values()) / len(signals)
        verified.append(r)

    return sorted(verified, key=lambda x: x["verification_score"], reverse=True)
```

**Verification checklist:**
- [ ] Result is from a credible source (official docs, recognized expert, active repo)
- [ ] Result is recent enough for the technology in question
- [ ] Result directly addresses the question, not a tangentially related topic
- [ ] Code examples compile/run (check version compatibility)
- [ ] Multiple sources confirm the same information

### 6. Avoiding Stale Information

```python
def is_result_stale(result: dict, technology: str) -> bool:
    """Determine if a search result is too old for the technology."""

    # Fast-moving tech: 6-month staleness threshold
    fast_moving = ["react", "next.js", "fastapi", "pydantic", "typescript", "tailwind"]

    # Moderate: 12-month threshold
    moderate = ["python", "django", "postgresql", "docker", "aws"]

    # Slow-moving: 24-month threshold
    stable = ["sql", "http", "rest", "git", "linux"]

    tech = technology.lower()
    if any(f in tech for f in fast_moving):
        max_age = 180
    elif any(m in tech for m in moderate):
        max_age = 365
    else:
        max_age = 730

    pub_date = result.get("published_date")
    if not pub_date:
        return True  # No date = potentially stale

    age_days = (datetime.now() - parse_date(pub_date)).days
    return age_days > max_age
```

### 7. Cross-Referencing Search Results

```python
def cross_reference_results(
    results: list[dict],
    min_agreement: int = 2,
) -> dict:
    """Find claims supported by multiple independent sources."""

    # Extract key claims from each result
    claims: dict[str, list[str]] = {}
    for r in results:
        # Use LLM to extract claims
        extracted = extract_claims(r.get("content", ""))
        for claim in extracted:
            claims.setdefault(claim, []).append(r["url"])

    # Score by agreement
    scored_claims = []
    for claim, sources in claims.items():
        unique_sources = list(set(sources))
        scored_claims.append({
            "claim": claim,
            "source_count": len(unique_sources),
            "sources": unique_sources,
            "verified": len(unique_sources) >= min_agreement,
        })

    return {
        "verified_claims": [c for c in scored_claims if c["verified"]],
        "disputed_claims": [c for c in scored_claims if not c["verified"]],
        "total_claims": len(scored_claims),
    }
```

### 8. Documenting Search Findings

```markdown
## Search Log: [Topic]

**Date:** YYYY-MM-DD
**Queried by:** [Agent/User]

### Queries Executed
1. `[Query 1]` → [N] results, best: [Title] ([URL])
2. `[Query 2]` → [N] results, best: [Title] ([URL])
3. `[Query 3]` → [N] results, best: [Title] ([URL])

### Key Findings
- [Finding 1] — confirmed by [Source A], [Source B]
- [Finding 2] — confirmed by [Source C]
- [Finding 3] — disputed: [Source D] says X, [Source E] says Y

### Decision
Based on search results: [conclusion and rationale]

### Confidence
High/Medium/Low — [reason]
```

## Anti-Patterns

- **Skipping search and reasoning from training data** — LLMs hallucinate API details
- **Accepting the first search result** — top result isn't always the best or most current
- **Not checking version compatibility** — code from v1 won't work with v2
- **Searching without context** — vague queries waste time and return irrelevant results
- **Ignoring official documentation** — blog posts can be wrong; docs are authoritative
- **Not documenting searches** — future you won't remember what was searched and why
- **Searching when you should reason** — don't search for "how to write a for loop"

## Best Practices

1. **Always search before coding** — local codebase → docs → web → GitHub, in order.
2. **Formulate specific queries** — [Technology] + [Topic] + [Constraint] + [Year].
3. **Verify every result** — check source credibility, recency, and relevance.
4. **Cross-reference across sources** — 2+ independent sources confirming = reliable.
5. **Flag stale information** — fast-moving tech has a 6-month staleness threshold.
6. **Prefer official docs** over blog posts, and recent posts over old ones.
7. **Document your searches** — queries, results, and decisions for future reference.
8. **Know when to stop searching** — if 3+ queries return nothing relevant, switch to reasoning.
9. **Include version numbers** in queries for technology-specific searches.
10. **Use code-specific queries** — add "example", "pattern", or "implementation" to get code results.

## Related Skills

- `exa-search` — Executing web searches with Exa
- `deep-research` — Full research methodology for complex investigations
- `documentation-lookup` — Looking up official documentation
- `codebase-onboarding` — Searching local codebases to understand existing patterns
- `iterative-retrieval` — Progressive context loading from search results
