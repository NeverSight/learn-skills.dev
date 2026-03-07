---
name: fork-intelligence
description: Discover valuable GitHub fork divergence beyond stars. TRIGGERS - fork analysis, fork intelligence, find forks, valuable forks, fork divergence, fork discovery, upstream forks.
allowed-tools: Read, Bash, Grep, Glob
---

# Fork Intelligence

Systematic methodology for discovering valuable work in GitHub fork ecosystems. Stars-only filtering misses 60-100% of substantive forks — this skill uses branch-level divergence analysis, upstream PR cross-referencing, and domain-specific heuristics to find what matters.

Validated empirically across 10 repositories spanning Python, Rust, TypeScript, C++/Python, and Node.js (tensortrade, backtesting.py, kokoro, pymoo, firecrawl, barter-rs, pueue, dukascopy-node, ArcticDB, flowsurface).

## FIRST — TodoWrite Task Templates

**MANDATORY**: Select and load the appropriate template before any fork analysis.

### Template A — Full Analysis (new repository)

```
1. Get upstream baseline (stars, forks, default branch, last push)
2. List all forks with pagination, note timestamp clusters
3. Filter to unique-timestamp forks (skip bulk mirrors)
4. Check default branch divergence (ahead_by/behind_by)
5. Check non-default branches for all forks with recent push or >1 branch
6. Evaluate commit content, author emails, tags/releases
7. Cross-reference upstream PR history from fork owners
8. Tier ranking and cross-fork convergence analysis
9. Produce report with actionable recommendations
```

### Template B — Quick Scan (triage only)

```
1. Get upstream baseline
2. List forks, filter by timestamp clustering
3. Check default branch divergence only
4. Report forks with ahead_by > 0
```

### Template C — Targeted Fork Evaluation (specific fork)

```
1. Compare fork vs upstream on all branches
2. Examine commit messages and changed files
3. Check for tags/releases, open issues, PRs
4. Assess cherry-pick viability
```

---

## Signal Priority Order

Ranked by empirical reliability across 10 repositories. See [signal-priority.md](./references/signal-priority.md) for details.

| Rank | Signal                          | Reliability | What It Catches                                      |
| ---- | ------------------------------- | ----------- | ---------------------------------------------------- |
| 1    | **Branch-level divergence**     | Highest     | Work on feature branches (50%+ of substantive forks) |
| 2    | **Upstream PR cross-reference** | High        | Rebased/force-pushed work invisible to compare API   |
| 3    | **Tags/releases on fork**       | High        | Independent maintenance intent                       |
| 4    | **Commit email domains**        | High        | Institutional contributors (`@company.com`)          |
| 5    | **Timestamp clustering**        | Medium      | Eliminates 85%+ mirror noise                         |
| 6    | **Cross-fork convergence**      | Medium      | Reveals unmet upstream demand                        |
| 7    | **Stars**                       | Lowest      | Often anti-correlated with actual value              |

---

## Pipeline — 7 Steps

### Step 1: Upstream Baseline

```bash
UPSTREAM="OWNER/REPO"
gh api "repos/$UPSTREAM" --jq '{forks_count, pushed_at, default_branch, stargazers_count}'
```

### Step 2: List All Forks + Timestamp Clustering

```bash
# List all forks with activity signals
gh api "repos/$UPSTREAM/forks" --paginate \
  --jq '.[] | {full_name, pushed_at, stargazers_count, default_branch}'
```

**Timestamp clustering**: Forks sharing exact `pushed_at` with upstream are bulk mirrors created by GitHub's fork mechanism and never touched. Group by `pushed_at` — forks with unique timestamps warrant investigation. This alone eliminates 85%+ of noise.

```bash
# Filter to unique-timestamp forks (skip bulk mirrors)
gh api "repos/$UPSTREAM/forks" --paginate \
  --jq '.[] | {full_name, pushed_at, stargazers_count}' | \
  jq -s 'group_by(.pushed_at) | map(select(length == 1)) | flatten'
```

### Step 3: Default Branch Divergence

```bash
BRANCH=$(gh api "repos/$UPSTREAM" --jq '.default_branch')

# For each candidate fork
gh api "repos/$UPSTREAM/compare/$BRANCH...FORK_OWNER:$BRANCH" \
  --jq '{ahead_by, behind_by, status}'
```

The `status` field meanings:

- `identical` — pure mirror, skip
- `behind` — stale mirror, skip
- `diverged` — has original commits AND is behind (interesting)
- `ahead` — has original commits, up-to-date with upstream (rare, most valuable)

**Important**: Always compare from the upstream repo's perspective (`repos/UPSTREAM/compare/...`). The reverse direction (`repos/FORK/compare/...`) returns 404 for some repositories.

### Step 4: Non-Default Branch Analysis (CRITICAL)

**This is the single biggest methodology improvement.** Across all 10 repos tested, 50%+ of the most valuable fork work lived exclusively on feature branches.

Examples:

- flowsurface/aviu16: 7,000-line GPU shader heatmap only on `shader-heatmap`
- ArcticDB/DerThorsten: 147 commits across `conda_build`, `clang`, `apple_changes`
- pueue/FrancescElies: Duration display only on `cesc/duration`
- barter-rs: 6 of 12 top forks had work only on feature branches

```bash
# List branches on a fork
gh api "repos/FORK_OWNER/REPO/branches" --jq '.[].name' | head -20

# Check divergence on a specific branch
gh api "repos/$UPSTREAM/compare/$BRANCH...FORK_OWNER:FEATURE_BRANCH" \
  --jq '{ahead_by, behind_by, status}'
```

**Heuristics for which forks need branch checks**:

- Any fork with `pushed_at` more recent than upstream but `ahead_by == 0` on default branch
- Any fork with more than 1 branch
- Branch count > 10 is suspicious — likely non-trivial work (ArcticDB: Rohan-flutterint had 197 branches)

### Step 5: Commit Content Evaluation

```bash
gh api "repos/$UPSTREAM/compare/$BRANCH...FORK_OWNER:BRANCH" \
  --jq '.commits[] | {sha: .sha[:8], message: .commit.message | split("\n")[0], date: .commit.committer.date[:10], author: .commit.author.email}'
```

**What to look for**:

- Commit email domains reveal institutional contributors (`@man.com`, `@quantstack.net`)
- Subtract merge commits from ahead_by count (e.g., akeda2/pueue showed 35 ahead but 28 were upstream merges)
- Build system changes (`CMakeLists.txt`, `Cargo.toml`, `pyproject.toml`) indicate platform enablement
- Protobuf schema changes indicate architectural-level features
- Test files alongside source changes signal production-intent work

### Step 6: Fork-Specific Signals

```bash
# Tags/releases (strongest independent maintenance signal)
gh api "repos/FORK_OWNER/REPO/tags" --jq '.[].name' | head -10
gh api "repos/FORK_OWNER/REPO/releases" --jq '.[] | {tag_name, name, published_at}' | head -5

# Open issues on the fork (signals independent project maintenance)
gh api "repos/FORK_OWNER/REPO/issues?state=open" --jq 'length'

# Check if repo was renamed (strong divergence intent signal)
gh api "repos/FORK_OWNER/REPO" --jq '.name'
```

| Signal                    | Strength                  | Example                                 |
| ------------------------- | ------------------------- | --------------------------------------- |
| Tags/releases on fork     | Highest                   | pueue/freesrz93 had 6 releases          |
| Open PRs against upstream | High                      | Formal proposals with review context    |
| Open issues on the fork   | High                      | Independent project maintenance         |
| Repo renamed              | Medium                    | flowsurface/sinaha81 became volume_flow |
| Build config changes      | High (compiled languages) | Cargo.toml, CMakeLists.txt diff         |
| Description changed       | Weak                      | Many vanity renames with no code        |

### Step 7: Cross-Fork Convergence + Upstream PR History

```bash
# Check upstream PRs from fork owners
gh api "repos/$UPSTREAM/pulls?state=all" --paginate \
  --jq '.[] | select(.head.repo.fork) | {number, title, state, user: .user.login}'
```

**Cross-fork convergence**: When multiple forks independently solve the same problem, it signals unmet upstream demand:

- firecrawl: 3 forks adopted Patchright for anti-detection
- flowsurface: 3 forks added technical indicators independently
- kokoro: 2 independent batched inference implementations
- barter-rs: 4 forks added Bybit support

**Upstream PR cross-reference catches**:

- Rebased/force-pushed work invisible to compare API
- Work that was merged upstream (fork shows 0 ahead but was historically significant)
- Declined PRs with valuable code that the fork still maintains

---

## Tier Classification

After running the pipeline, classify forks into tiers:

| Tier                          | Criteria                                                  | Action                                  |
| ----------------------------- | --------------------------------------------------------- | --------------------------------------- |
| **Tier 1: Major Extensions**  | New features, architectural changes, >10 original commits | Deep evaluation, cherry-pick candidates |
| **Tier 2: Targeted Features** | Focused additions, bug fixes, 2-10 commits                | Cherry-pick individual commits          |
| **Tier 3: Infrastructure**    | CI/CD, packaging, deployment, docs                        | Evaluate if relevant to your setup      |
| **Tier 4: Historical**        | Merged upstream or stale but once significant             | Note for context, no action needed      |

---

## Domain-Specific Patterns

Different codebases exhibit different fork behaviors. See [domain-patterns.md](./references/domain-patterns.md) for full details.

| Domain                      | Key Pattern                                                                | Example                                               |
| --------------------------- | -------------------------------------------------------------------------- | ----------------------------------------------------- |
| **Scientific/ML**           | Researchers fork-implement-publish-vanish, zero social engagement          | pymoo: 300-file fork with 0 stars                     |
| **Trading/Finance**         | Exchange connectors dominate; best forks are private                       | barter-rs: 4 independent Bybit impls                  |
| **Infrastructure/DevTools** | Self-hosting/SaaS-removal is the dominant theme                            | firecrawl: devflowinc/firecrawl-simple (630 stars)    |
| **C++/Python Mixed**        | Feature work lives on branches; email domains reveal institutions          | ArcticDB: @man.com, @quantstack.net                   |
| **Node.js Libraries**       | Check npm publication as separate packages                                 | dukascopy-node: kyo06 published `dukascopy-node-plus` |
| **Rust CLI**                | Cargo.toml diff is reliable quick filter; "superset" forks add subcommands | pueue: freesrz93 added 7 subcommands                  |

---

## Quick-Scan Pipeline (5-minute triage)

For rapid triage of any new repo:

```bash
UPSTREAM="OWNER/REPO"
BRANCH=$(gh api "repos/$UPSTREAM" --jq '.default_branch')

# 1. Baseline
gh api "repos/$UPSTREAM" --jq '{forks_count, pushed_at, stargazers_count}'

# 2. Forks with unique timestamps (skip mirrors)
gh api "repos/$UPSTREAM/forks" --paginate \
  --jq '.[] | {full_name, pushed_at, stargazers_count}' | \
  jq -s 'group_by(.pushed_at) | map(select(length == 1)) | flatten | sort_by(.pushed_at) | reverse'

# 3. Check ahead_by for each candidate
# (loop over candidates from step 2)

# 4. Check upstream PRs from fork authors
gh api "repos/$UPSTREAM/pulls?state=all" --paginate \
  --jq '.[] | select(.head.repo.fork) | {number, title, state, user: .user.login}'
```

---

## Known Limitations

| Limitation                                      | Impact                                 | Workaround                                                        |
| ----------------------------------------------- | -------------------------------------- | ----------------------------------------------------------------- |
| GitHub compare API 250-commit limit             | Highly divergent forks may truncate    | Use `gh api repos/FORK/commits?per_page=1` to get total count     |
| Private forks invisible                         | Trading firms keep best work private   | Accepted limitation                                               |
| Force-pushed branches break compare API         | Shows 0 ahead despite significant work | Cross-reference upstream PR history                               |
| Renamed forks may break API calls               | Old URLs may 404                       | Use `gh api repos/FORK_OWNER/REPO --jq '.name'` to detect renames |
| Rate limiting on large fork ecosystems          | >1000 forks = many API calls           | Use timestamp clustering to reduce calls by 85%+                  |
| Maintainer dev forks look like independent work | Branch names 1:1 with upstream PRs     | Cross-reference branch names against upstream PR branch names     |

---

## Report Template

Use this structure for the final analysis report:

```markdown
# Fork Analysis Report: OWNER/REPO

**Repository**: OWNER/REPO (N stars, M forks)
**Analysis date**: YYYY-MM-DD

## Fork Landscape Summary

| Metric                                | Value  |
| ------------------------------------- | ------ |
| Total forks                           | N      |
| Pure mirrors                          | N (X%) |
| Divergent forks (ahead on any branch) | N      |
| Substantive forks (meaningful work)   | N      |
| Stars-only miss rate                  | X%     |

## Tiered Ranking

### Tier 1: Major Extensions

(fork details with ahead_by, key features, files changed)

### Tier 2: Targeted Features

...

### Tier 3: Infrastructure/Packaging

...

## Cross-Fork Convergence Patterns

(themes that multiple forks independently implemented)

## Actionable Recommendations

- Cherry-pick candidates
- Feature inspiration
- Security fixes
```

---

## Post-Change Checklist

After modifying THIS skill:

1. [ ] YAML frontmatter valid (no colons in description)
2. [ ] Trigger keywords current in description
3. [ ] All `./references/` links resolve
4. [ ] Pipeline steps numbered consistently
5. [ ] Shell commands tested against a real repository
6. [ ] Append changes to [evolution-log.md](./references/evolution-log.md)
