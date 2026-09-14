---
name: flows-review-checks
description: >-
  Canonical Flows technical-review checks and scoring (hunt commands, coverage
  scope, package audit, public criteria, Must/Should/Nice). Loaded by
  flows-code-review and by any external review skill. Do not copy these
  checks into another skill. Do not use this skill to fix code. Use when an
  orchestrator says to load flows-review-checks, or when aligning two review
  flows on the same bar.
allowed-tools: Read, Glob, Grep, Bash, Write
---

# Flows review checks (shared)

This file is the **public** definition of what a Flows technical review must search for in this repo, how strict each bar is, and how to score 1.1, 1.3–1.6, 2.1–2.6, 3.1.

It does **not** decide:
- whether you build the app
- Codespace vs local
- Jira / Zendesk / git round folders
- output paths (`reviews/code-review/…` vs `reviews/external-submissions/…`)

The **caller** sets those. Then it reads this file and runs every check.

Do not edit the app. Do not “fix it now.”

Load **`code-quality`** from the same `cognitedata/builder-skills` repo (see hunt 1.5). Run its **searches**. Ignore every “fix / replace / write the file / pnpm add” instruction in that skill. Other skills (`test-coverage`, …) stay fixers and are not the review bar.

## Caller contract

Before any command in this file:

1. `cd` to the **app root** (the directory with `package.json` and `src/`).
2. All greps and test/coverage commands run from that directory.
3. The caller names where to write artifacts. This file only defines **content**.

If a search was not run, that check is not a pass.

## What the caller must produce

Whatever the filenames, the review must include:

1. **File inventory** — every `.ts`/`.tsx` except `node_modules`, `dist`, `.cognite-bundles`. Include `vitest.config.*` / `vite.config.*` / `jest.config.*`. Columns: Structure, Quality, Patterns, Tests, Notes. Then read every non-trivial production file (skip barrels, generated types, tests).
2. **Findings** — every hunt below, with hits or `none`. Then must / should / nice with `file:line`.
3. **Package audit** — Step 2 in this file.
4. **Scored report** — criteria 1.1, 1.3–1.6, 2.1–2.6, 3.1, must/should/nice lists, `_Impact:_` on every Must Fix.

A 1–2 on any criterion is Must Fix. 3 is Should Fix. Gaps at 4 are Nice Fix.

---

## Step 1 — Hunt

Run **every** command. Do not sample `src/` and stop.

### 1.1 Coverage and test config (criterion 1.4) — before you believe any %

Read `vitest.config.*`, `vite.config.*` (`test` / `coverage` blocks), and `jest.config.*`. Then:

```bash
grep -n -A 40 -E "coverage|exclude|include|coveragePathIgnorePatterns|collectCoverageFrom|testPathIgnorePatterns" vitest.config.ts vitest.config.mts vitest.config.js vite.config.ts vite.config.mts jest.config.ts jest.config.js jest.config.mjs 2>/dev/null
```

Record two lists:

1. **`coverage.exclude` / `coveragePathIgnorePatterns` / inverted `coverage.include`** — files not measured.
2. **`test.exclude` / `testPathIgnorePatterns`** — tests that never run.

Allowed coverage excludes: `*.test.*`, `*.spec.*`, `vite-env.d.ts`, `src/main.tsx`, generated code. Nothing else under `src/` — not `src/pages/`, `src/components/`, `src/hooks/`, `src/services/`, individual feature files, or `src/**/*.tsx`.

If production files are excluded, the printed coverage number is invalid. Criterion 1.4 scores **1 or 2** even if Vitest prints ≥ 80%. Same if tests themselves are on an exclude list so they do not run.

### 1.2 Correctness (criterion 1.1)

```bash
grep -rn --include="*.ts" --include="*.tsx" -E "ErrorBoundary|componentDidCatch|getDerivedStateFromError" src/
grep -rn --include="*.ts" --include="*.tsx" -E "(TODO|FIXME|HACK|XXX):" src/ | grep -v ".test." | grep -v ".spec."
grep -rn --include="*.tsx" --include="*.ts" -B 2 -A 15 "useEffect" src/
grep -rn --include="*.tsx" -E "useQuery|useMutation|isLoading|isPending|isError" src/
```

Flag: no ErrorBoundary; fetch UI with no loading / error / empty state; `useEffect` with timers, listeners, or async work and no cleanup; TODOs on critical paths.

### 1.3 CDF Raw (criterion 2.6)

```bash
grep -rn --include="*.ts" --include="*.tsx" -E "client\.raw\.|\.raw\.(listRows|insertRows|retrieveRow|deleteRows)|listRows|insertRows|retrieveRow" src/
```

If there are **no hits**, 2.6 is **N/A**. Do not fold Raw issues into 2.1.

Flag: Raw as the primary store; paging with no limit/cursor; download-then-filter in the client.

### 1.4 DMS and limits (criteria 2.1–2.5)

```bash
grep -rn --include="*.ts" --include="*.tsx" -E "instances\.(list|search|query|aggregate|retrieve)" src/
grep -rn --include="*.ts" --include="*.tsx" -E "QueuedTaskRunner|cdfTaskRunner" src/
grep -rn --include="*.ts" --include="*.tsx" -E "429|Retry-After|exponential|backoff" src/
```

Flag: `instances.list` for read-heavy UI that could be `query`/`search`; no limit/cursor; client-side filter of large results; no concurrency cap and no 429 handling.

### 1.5 Quality and testability (criteria 1.5, 1.6) — includes `code-quality`

Load `skills/code-quality/SKILL.md` from **this same repo** (`cognitedata/builder-skills`). Local file if the workspace is `builder-skills`; otherwise:

```bash
curl -fsSL https://raw.githubusercontent.com/cognitedata/builder-skills/main/skills/code-quality/SKILL.md
```

Use it for the bars (150-line components, naming, ViewModel, DI, dead code). **Do not apply its fixes.** Run every command below (same searches as that skill).

```bash
grep -rn --include="*.ts" --include="*.tsx" -E ": any|as any|<any>|as unknown as" src/
grep -rn --include="*.ts" --include="*.tsx" "vi\.mock" src/
grep -rn --include="*.ts" --include="*.tsx" -E "createContext|useContext" src/hooks/ src/contexts/ 2>/dev/null
grep -rn --include="*.ts" --include="*.tsx" -E "^import.*from\s+['\"]\.\./" src/hooks/
grep -rn --include="*.ts" --include="*.tsx" -E "new CogniteClient|createCogniteClient" src/
grep -rn --include="*.ts" --include="*.tsx" -E "class\s+\w+(Service|Client|Repository|Manager)" src/
grep -rn --include="*.tsx" --include="*.ts" -l "useQuery\|useMutation\|sdk\.\|client\." src/pages/ src/views/ 2>/dev/null
grep -rn --include="*.ts" --include="*.tsx" -l "ViewModel" src/hooks/ 2>/dev/null
grep -rn --include="*.tsx" --include="*.ts" -E "console\.(log|debug)" src/
grep -rn --include="*.tsx" --include="*.ts" -E "path:\s*['\"]|<Route" src/
pnpm run lint 2>/dev/null || npm run lint 2>/dev/null || true
pnpm exec tsc --noEmit 2>/dev/null || npx tsc --noEmit 2>/dev/null || true
```

Component size (flag `.tsx` over **150 lines**, then read — mixed fetch + render is the problem, not length alone):

```bash
node -e "const fs=require('fs'),path=require('path');function walk(d){return fs.readdirSync(d,{withFileTypes:true}).flatMap(e=>{const p=path.join(d,e.name);return e.isDirectory()?walk(p):p.endsWith('.tsx')?[p]:[]})}walk('src').map(p=>({p,l:fs.readFileSync(p,'utf8').split('\n').length})).sort((a,b)=>b.l-a.l).forEach(({l,p})=>console.log(l,p))"
```

Possibly unused production files:

```bash
for file in $(find src -name "*.ts" -o -name "*.tsx" | grep -v ".test." | grep -v ".spec." | grep -v "node_modules"); do
  basename=$(basename "$file" | sed 's/\.[^.]*$//')
  imports=$(grep -rn --include="*.ts" --include="*.tsx" "$basename" src/ | grep -v "$file" | wc -l)
  if [ "$imports" -eq 0 ]; then echo "UNUSED: $file"; fi
done
```

Flag: `any` / `as unknown as` in production; lint or `tsc` errors; `new CogniteClient` outside bootstrap; hooks that import deps instead of context; pages with `useQuery` / SDK and no ViewModel; `vi.mock` with no comment; `console.log`/`debug`; unused files; unreachable routes; components over 150 lines that mix data fetching with UI.

Per `code-quality`: **lint errors and production `any` are blocking** (Must Fix). Unreachable pages / unused files / large dead blocks are Must Fix (already 1.5).

### Findings shape

```markdown
# Findings: [app name]

## Config inspected
- Coverage config file(s): …
- Production paths excluded from coverage: … (or none)
- Tests excluded from the test run: … (or none)

## Searches
| Check | Hits (file:line or none) |
| ----- | ------------------------ |
| ErrorBoundary | |
| coverage/test exclude | |
| CDF Raw | |
| instances.list/query/search | |
| QueuedTaskRunner / 429 | |
| any / vi.mock | |
| lint / tsc | |
| CogniteClient / DI / ViewModel | |
| unused files / console.log | |
| components > 150 lines | |

## Must / should / nice
- [ ] … — file:line — criterion
```

Every later score must point at this hunt.

---

## Step 2 — Packages

Two commands — do **not** loop `npm view` per package:

```bash
npm outdated --json 2>/dev/null || true
npm audit --json 2>/dev/null || true
```

From `npm outdated --json`: packages absent are up-to-date; packages present show `current` / `wanted` / `latest`. Flag any in `dependencies` (not `devDependencies`) that are ≥ 1 major behind.

From `npm audit --json`: parse severity counts and advisories. **High or critical CVEs are Must Fix** (1.3 scores 1–2).

Spot-check `npm view <pkg> deprecated` only for packages that are already flagged (major behind, in audit, or an unfamiliar name).

Health: **Pass** (up-to-date or ≤ 1 minor behind, 0 critical/high CVEs) | **Warn** (1 major behind in `dependencies`, or moderate CVE) | **Fail** (≥ 2 majors behind, or high/critical CVE, or deprecated).

Table shape:

```markdown
## Package audit: [app name]

### Dependencies

| Package | Used version | Latest | Deprecated | CVEs | Health |
| ------- | ------------ | ------ | ---------- | ---- | ------ |

### Security audit

| Severity | Count |
| -------- | ----- |
| Critical | 0 |
| High | 0 |
| Moderate | 0 |
| Low | 0 |

#### Vulnerabilities

| Package | Severity | Title | Patched in | Advisory |
| ------- | -------- | ----- | ---------- | -------- |
```

---

## Step 3 — Test coverage

Only after Step 1.1. If production files were excluded, say so **before** quoting Vitest’s number, and score 1.4 as 1–2.

```bash
npx vitest run --coverage
# or: npx jest --coverage
# or: npm test -- --coverage
```

Record framework, pass/fail/skip counts, statement/branch/function/line percentages.

No test runner, or tests that do not start, is a 1.4 finding by itself.

**Hard gate:** line coverage of **all** `src/**/*.ts(x)` except tests, `vite-env.d.ts`, and `main.tsx` must be **≥ 80%**. If the tool was measuring a smaller set, the number does not count.

For each non-trivial file: matching `.test.ts` / `.spec.ts`? If not, Tests: `✗`. Hooks and services should take dependencies from React context. `vi.mock` without a comment is a 1.6 finding.

---

## Step 4 — Score the public criteria

Use hunt hits, files you read, coverage **scope**, and the package audit. Each score needs one or two sentences with paths. **N/A** only when the criterion does not apply (2.6 with no Raw usage is the usual case). Do not score **1.2** here.

### 1.1 No known bugs

**Check:** TODOs on critical paths; missing ErrorBoundary; fetch UI without loading/error/empty; `useEffect` leaks; null-unsafe access.

**Fail this criterion (1–2) if:** primary flows crash or silently fail; no error UI on core fetches; data can be corrupted.

**Score 3 if:** no ErrorBoundary, or several screens missing empty/error states, but core paths still fail visibly rather than corrupt data.

| Score | Why |
| ----- | --- |
| 5 | No known defects; edge cases handled or explicitly out of scope with safe failure modes. |
| 4 | Minor issues only; none affect core user flows or data integrity. |
| 3 | Some known bugs or rough edges; workarounds exist or impact is limited. |
| 2 | Material bugs, unreliable flows, or silent failures; users or data could be harmed. |
| 1 | Broken primary flows or data corruption risk. |

### 1.3 Dependencies and packages

**Check:** lockfile, majors behind, CVEs, deprecated, install scripts.

**Fail this criterion (1–2) if:** high or critical CVE, deprecated production dep, or ≥ 2 majors behind on a production dep with no plan.

| Score | Why |
| ----- | --- |
| 5 | Dependencies are current, trustworthy, and scanned; no red flags. |
| 4 | Small updates or pinning tweaks needed; no serious supply-chain signals. |
| 3 | Outdated or heavy deps; plan to upgrade documented. |
| 2 | High-risk packages, excessive bundle, or unclear provenance. |
| 1 | Known-vulnerable, deprecated, or malicious-adjacent dependency usage. |

### 1.4 Test coverage

**Check:** tooling actually runs; **what is excluded**; line coverage at full `src/` scope; tests exist for non-trivial modules.

**Fail this criterion (1–2) if any of these are true:**
- Coverage tooling missing or tests do not run
- Production files (pages, hooks, components, services, feature modules) are in `coverage.exclude` / `coveragePathIgnorePatterns`, or omitted from `coverage.include`
- Test files are in `test.exclude` / `testPathIgnorePatterns` so they never run
- Full-scope line coverage is below 80%

The number Vitest/Jest prints does not override the bullets above.

| Score | Why |
| ----- | --- |
| 5 | Critical paths well covered; honest ≥ 80% line coverage; failures easy to localize. |
| 4 | Good honest coverage (≥ 80%) with a few gaps in secondary modules. |
| 3 | Core flows partially tested; honest coverage below 80% or important branches missing. |
| 2 | Sparse tests; coverage well below 80%; **or coverage looks high because files were excluded**. |
| 1 | No meaningful automated tests, tooling not configured, or most of the app excluded from measurement. |

### 1.5 Dead code and maintainability

**Check:** unused exports, unreachable routes, commented-out blocks, lint/`tsc`, `any`, unused files (`code-quality` Steps 1, 8, 9).

**Fail this criterion (1–2) if:** unreachable pages, unused files, large dead blocks, **lint errors**, or **production `any` / `as any`**.

| Score | Why |
| ----- | --- |
| 5 | Codebase is lean; dead paths removed or clearly feature-flagged with owners. |
| 4 | Minor cruft; quick cleanup possible. |
| 3 | Noticeable dead code or duplication; increases review and bug surface. |
| 2 | Large unused areas or confusing structure; hard to reason about behavior. |
| 1 | Unmaintainable tangle; dead code masks real execution paths. |

### 1.6 Coding patterns and testability

**Check:** DI via React context; interface-based services; ViewModel hooks for pages; no `new CogniteClient` outside bootstrap (`code-quality` Steps 5–6).

```typescript
const defaultDependencies = { useDataSource, useAnalytics };
export type UseMyHookContextType = typeof defaultDependencies;
export const UseMyHookContext = createContext<UseMyHookContextType>(defaultDependencies);
export function useMyHook() {
  const { useDataSource } = useContext(UseMyHookContext);
}
```

**Fail this criterion (1–2) if:** hooks/services hard-code the SDK or other deps with no injection path, so tests can only use `vi.mock`; or pages mix fetch + render with no ViewModel on core screens.

| Score | Why |
| ----- | --- |
| 5 | DI via context throughout; interface-based services; ViewModel hooks for pages; type-safe mocks. |
| 4 | Mostly good patterns; one or two hooks import directly but still testable. |
| 3 | Mixed: some injectable, others import directly; `vi.mock` used frequently. |
| 2 | Most hooks hard-code dependencies; tests rely on module mocking throughout. |
| 1 | No DI; global singletons or direct SDK calls throughout. |

### 2.1 DMS query patterns (search / query vs heavier paths)

**Check:** Read-heavy UI should use `instances.query` or `instances.search`, not default to `instances.list`.

| Score | Why |
| ----- | --- |
| 5 | Read paths use the lightest suitable DMS API; writes and exceptions are documented. |
| 4 | Mostly correct; one or two calls could move to query/search. |
| 3 | Mix of appropriate and heavy reads; performance risk under load. |
| 2 | Default pattern is heavier than needed; likely to stress Postgres or DMS. |
| 1 | Systematic misuse of APIs contrary to platform guidance. |

### 2.2 Server-side filtering

**Check:** Filters, limits, and projections in the API request — not download-then-filter in the browser.

**Fail this criterion (1–2) if:** large or unbounded reads are reduced in memory.

| Score | Why |
| ----- | --- |
| 5 | Payloads are tight; filtering expressed in queries; pagination is real, not simulated. |
| 4 | Minor over-fetch; easy to tighten. |
| 3 | Repeated patterns of client-side filtering on medium result sets. |
| 2 | Large downloads with in-memory filtering; obvious scalability issue. |
| 1 | Unbounded or near-unbounded reads with client-side reduction. |

### 2.3 Limits, pagination, and prefetch

**Check:** Explicit limits; cursor or page; no prefetch of pages the user may never open.

**Fail this criterion (1–2) if:** lists are unbounded, or N+1 / deep prefetch.

| Score | Why |
| ----- | --- |
| 5 | Limits and paging match UX; no wasteful speculative loading. |
| 4 | Reasonable; small tuning opportunities. |
| 3 | Occasional high limits or redundant page fetches. |
| 2 | Frequent large pages or prefetch storms. |
| 1 | Unbounded lists, deep prefetch chains, or N+1 DMS patterns. |

### 2.4 Rate of calls — do not hammer DMS

**Check:** Debounce, batch, cache; no identical requests in a tight loop.

**Fail this criterion (1–2) if:** request storms against DMS.

| Score | Why |
| ----- | --- |
| 5 | Request rate matches user intent; caching/dedup in place. |
| 4 | Mostly fine; a hot path could batch or debounce slightly. |
| 3 | Chatty UI or polling without backoff; risk under concurrent users. |
| 2 | Clear risk of overwhelming DMS or shared quotas. |
| 1 | Tight loops, runaway polling, or duplicate parallel identical calls. |

### 2.5 Throttling and 429 responses — backoff with jitter

**Check:** `cdfTaskRunner` / `QueuedTaskRunner` (or equivalent concurrency cap) around CDF calls; on 429, exponential backoff with jitter; respect `Retry-After`; bounded retries.

**Fail this criterion (1–2) if:** many parallel CDF calls with **neither** a concurrency cap **nor** 429 handling.

Missing `QueuedTaskRunner` but TanStack Query (or similar) retries with backoff: score 3, not a pass.

| Score | Why |
| ----- | --- |
| 5 | Backoff + jitter implemented; retries bounded; behavior degrades gracefully. |
| 4 | Backoff exists; jitter or caps could be improved. |
| 3 | Naive fixed-interval retries or missing handling for throttling. |
| 2 | Aggressive retries on 429; thundering herd risk. |
| 1 | No handling; infinite or immediate tight retries on errors. |

### 2.6 CDF Raw

**Check:** `client.raw`, `listRows`, `insertRows`, `retrieveRow`. Unbounded paging; full-table scan then filter; Raw as the primary store.

**N/A if unused** — do not score this under 2.1.

**Fail this criterion (1–2) if:** Raw is the system of record, or rows are listed without a bound and filtered in the client.

| Score | Why |
| ----- | --- |
| 5 | Raw unused, or used for a narrow documented case with limits and server-side filter. |
| 4 | Legitimate Raw use; small tightening (limit/cursor) still needed. |
| 3 | Raw used more than needed; risk under growth. |
| 2 | Unbounded Raw reads or client-side filter of a table. |
| 1 | Raw as primary store, or scan-the-database patterns. |

### 3.1 Aura design system

**Check:** Aura components and tokens for layout, forms, tables, feedback, typography.

A score of 3 does not block approval. Missing `aria-label` / unlabeled inputs → Should Fix even if Aura scores 4–5.

| Score | Why |
| ----- | --- |
| 5 | Aura used consistently; custom pieces match design language. |
| 4 | Mostly Aura; isolated custom widgets with acceptable alignment. |
| 3 | Mix of ad-hoc UI and Aura; some inconsistency for users. |
| 2 | Largely non-Aura; visually disconnected from platform. |
| 1 | Clashing patterns, inaccessible controls, or no alignment with Aura when feasible. |

---

## Step 5 — Categorize findings

- **Must fix** (score 1–2): high/critical CVEs, broken core flows, unbounded API calls, coverage < 80% **or coverage/test exclude lists hiding code or tests**, unreachable pages or significant dead code, **lint errors**, **production `any`**, no DI path, unbounded or primary-store CDF Raw.
- **Should fix** (score 3): missing ErrorBoundary, missing loading/error/empty on some screens, missing `QueuedTaskRunner` when some retry exists, missing tests for non-trivial modules, client-side filtering of large datasets, missing backoff, a11y gaps, `vi.mock` overuse, oversized components that mix fetch and UI, naming / folder-structure misses from `code-quality`.
- **Nice to fix** (score 4 gaps): minor Aura inconsistencies, small cleanup, non-critical package updates, minor dead exports.

Each Must Fix item needs `_Impact:_` (one sentence on user/customer consequence).

Scores table every report must include:

| Area | Criterion | Score | Notes |
| ---- | --------- | ----- | ----- |
| User & customer | 1.1 Known bugs | /5 | |
| User & customer | 1.3 Packages | /5 | |
| User & customer | 1.4 Tests & coverage | /5 | |
| User & customer | 1.5 Dead code | /5 | |
| User & customer | 1.6 Patterns & testability | /5 | |
| Cognite services | 2.1 DMS query patterns | /5 | |
| Cognite services | 2.2 Server-side filter | /5 | |
| Cognite services | 2.3 Limits & pages | /5 | |
| Cognite services | 2.4 Call rate | /5 | |
| Cognite services | 2.5 429 backoff | /5 | |
| Cognite services | 2.6 CDF Raw | /5 or N/A | |
| Brand | 3.1 Aura | /5 | |

---

## Step 6 — Shared verify

The caller may add extra verify steps (artifact paths, no GitHub curl, Codespace, …). These always apply:

1. Every hunt in Step 1 has hits or `none` (blank is not a result), including the `code-quality` searches.
2. `code-quality` was loaded from `cognitedata/builder-skills` (local or `main`). Its fix steps were not applied.
3. Coverage config was read. If excludes hide production code or tests, 1.4 is 1–2 and there is a Must Fix item — even if the printed % is ≥ 80%.
4. Every scored criterion (1.1, 1.3–1.6, 2.1–2.6, 3.1) has a score or **N/A** (2.6 only).
5. Every Must Fix has `_Impact:_`.
6. Open must/should/nice counts match the lists.
