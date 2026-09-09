---
name: seo
description: Audits and fixes technical SEO, researches search demand, creates content briefs, and measures SEO/AEO performance. Use when asked to "audit SEO", "fix indexing", "improve AI visibility", "check keyword volume", "write an SEO brief", or "why did organic traffic drop". For writing the article use ghostwriter; for visual redesign use ui-design.
---

# SEO

- **IS:** one entry point for search visibility: evidence-led audits, implementation, demand research, writer briefs, and performance measurement across search and answer engines.
- **IS NOT:** writing the article (`ghostwriter`), standalone marketing copy (`copywriting`), visual redesign (`ui-design`), or tenant infrastructure (`multi-tenant-architecture`). Fix SEO copy and markup when they are part of the requested implementation.

## Route the task

| Request | Load | Deliverable |
|---|---|---|
| Audit a site, diagnose indexing, review a migration | `references/audit.md` and `references/validation-evidence.md` | Prioritized findings with URLs, observed evidence, impact, and correction |
| Fix or implement SEO | Audit references, then applicable implementation references below | Code changes, scoped checks, and served-page evidence for the changed behavior |
| Research demand, choose a target, brief a page | `references/research-protocol.md`; `references/brief-template.md` for a brief | Sourced demand table and decision, or a durable writer brief |
| Explain traffic movement, measure AI visibility, monitor SEO | `references/monitoring.md` | Property-scoped diagnosis or configured monitoring with explicit data gaps |

For a combined request, reuse one property and URL inventory across modes. An audit request produces findings; a request to fix them proceeds through implementation and verification within the user's authorized scope. A research-only request does not require crawling every URL or changing code.

## Establish the evidence boundary

Identify the exact public host, URL-prefix or domain property, production environment, project/subpath, audience, and business outcome. On a shared domain, filter each project's path separately. In analytics, verify hostname, path, conversion event and attribution window before interpreting a number.

Discover connected tools and existing project bindings first. Prefer the established reporting source, then an available equivalent, then a signed-in browser. No vendor is required. Ownership verification, API consent and a successful scoped query are separate states. An export for a neighboring property is not a fallback.

Use `No data` with its reason for inaccessible, missing, unsupported or unmeasured metrics; distinguish these from a measured zero. Label historical exports by their actual dates. Do useful public checks while an authenticated metric is unavailable.

## Working sequence

For substantial mixed work, track only the applicable steps:

- [ ] Confirm property, scope, baseline and intended outcome.
- [ ] Inspect live evidence and map affected route patterns or research questions.
- [ ] Prioritize blocking defects and high-value opportunities; separate observations from hypotheses.
- [ ] Implement authorized corrections or deliver the requested research/brief.
- [ ] Recheck the changed behavior, identify the tested environment, and report remaining gaps.

Prioritize crawl/index defects before cosmetic metadata changes. Page titles, headings and content structure follow the page's purpose and reader intent. Descriptive non-brand terms help category discovery; brand-led portfolio and product pages can be appropriate. Neither a fixed title character count nor question-shaped headings are ranking requirements.

Original evidence, useful comparisons and honest product limitations earn their place ahead of manufactured keyword permutations. Research likely reader questions; do not present invented query fan-outs as engine telemetry or create a page for every variation.

## References

| File | Read when |
|---|---|
| [references/audit.md](references/audit.md) | Crawling, diagnosing or prioritizing a site audit |
| [references/indexing-policy.md](references/indexing-policy.md) | Canonicals, redirects, exclusions, duplicate or programmatic pages |
| [references/nextjs-implementation.md](references/nextjs-implementation.md) | Implementing App Router metadata, sitemaps, rendering, status codes or schema; verify APIs against the installed Next.js docs |
| [references/answer-engines.md](references/answer-engines.md) | AI visibility, crawler policies, Markdown alternatives or `llms.txt` |
| [references/internationalisation.md](references/internationalisation.md) | Language/region variants and hreflang |
| [references/technical-hardening.md](references/technical-hardening.md) | CDN access, response headers, errors or preview environments affect discovery |
| [references/validation-evidence.md](references/validation-evidence.md) | Verifying findings, a built page or a deployed correction |
| [references/research-protocol.md](references/research-protocol.md) | Keyword/prompt metrics, opportunity selection and question maps |
| [references/brief-template.md](references/brief-template.md) | Producing a writer brief |
| [references/monitoring.md](references/monitoring.md) | Search/AI performance, attribution, anomalies or recurring work |
| [references/sources.md](references/sources.md) | A claim depends on current engine behavior, supported reports, or vendor research |

## Delivery

Findings go in chat unless a file is requested. Writer briefs go to the requested project destination; retain prior dated briefs when producing a new revision. Keep scratch crawls and exports out of the repository. No em dashes in authored reports or briefs.

Report what changed, why, exact verification evidence, and what remains unmeasured. A successful local build, ready deployment, public URL probe, Google index record and measured conversion are different evidence. Name the strongest state actually verified.

Sending recaps to others, scheduling recurring work, spending on tools and production deployment follow the user's authorization and host rules. Reuse an existing matching monitor rather than creating another owner or schedule.

## Gotchas

- A sitemap can parse while listing `/studio` that intentionally returns 404. Check its URLs, not just XML validity.
- A canvas gated on mounted state can leave the homepage and category hubs with only navigation in initial HTML. Inspect those hubs as well as deep pages; `use client` alone does not imply missing server-rendered content.
- `lastModified: new Date()` or a build timestamp describes generation, not necessarily a significant page update. Use content dates or omit the field.
- A canonical tag on each URL does not resolve two copies that both self-canonicalize. Compare content and choose the preferred URL.
- Two consistent JSON-LD scripts are not an error. Verify entity identity, eligible properties and visible supporting content instead of script count.
- DNS verification needs no invented meta token. Confirm scoped data access separately.
- A crawler user-agent probe does not authenticate a bot IP or establish index inclusion. Treat CDN logs and engine inspection as separate evidence.
- Prompt demand, measured citations, mentions, AI impressions and referral sessions are different quantities. Preserve engine, source, match type, scope and window.
- A vendor Search Console connector may under-report. Reconcile property, filters and aggregation against native Search Console before diagnosing a drop.

Maintenance only: `evals/evals.json` holds behavioral scenarios and routing prompts. It is loaded when changing the skill, not during ordinary SEO work.
