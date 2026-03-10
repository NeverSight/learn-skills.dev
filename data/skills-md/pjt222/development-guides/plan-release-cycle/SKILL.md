---
name: plan-release-cycle
description: >
  Plan a software release cycle with milestones, feature freezes,
  release candidates, and go/no-go criteria. Covers calendar-based
  and feature-based release strategies. Use when starting planning for a
  major or minor version release, transitioning from ad-hoc to structured
  release cadence, coordinating a release across multiple teams or components,
  defining quality gates for a regulated project, or planning the first
  public release (v1.0.0) of a project.
license: MIT
allowed-tools: Read Write Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: versioning
  complexity: intermediate
  language: multi
  tags: versioning, release-planning, milestones, release-cycle
---

# Plan Release Cycle

Plan a structured software release cycle by defining strategy (calendar-based or feature-based), setting milestones with target dates, establishing feature freeze criteria, managing release candidates, defining go/no-go checklists, and documenting rollback plans. Produces a `RELEASE-PLAN.md` artifact that guides the team from development through release.

## When to Use

- Starting planning for a major or minor version release
- Transitioning from ad-hoc releases to a structured release cadence
- Coordinating a release across multiple teams or components
- Defining quality gates and release criteria for a regulated project
- Planning the first public release (v1.0.0) of a project

## Inputs

- **Required**: Target version number (e.g., v2.0.0)
- **Required**: Desired release date or release window
- **Required**: List of planned features or scope (backlog, roadmap, or description)
- **Optional**: Team size and availability
- **Optional**: Release strategy preference (calendar-based or feature-based)
- **Optional**: Regulatory or compliance requirements affecting release
- **Optional**: Previous release velocity or cycle duration data

## Procedure

### Step 1: Determine Release Strategy

Choose between two primary strategies:

**Calendar-based** (time-boxed):
- Release on a fixed schedule (e.g., every 4 weeks, quarterly)
- Features that are not ready are deferred to the next release
- Predictable for users and downstream projects
- Best for: libraries, frameworks, tools with external consumers

**Feature-based** (scope-driven):
- Release when a defined set of features is complete
- Date adjusts to accommodate scope
- Risk of scope creep and indefinite delays
- Best for: internal tools, first releases, major rewrites

For most projects, a hybrid approach works well: set a target date with a defined scope, but allow a 1-2 week buffer. If scope is not met by the buffer deadline, defer remaining features.

Document the strategy choice with rationale.

**Expected:** Release strategy documented with rationale matching project context.

**On failure:** If the team cannot agree on a strategy, default to calendar-based with a feature-priority list. Time-boxing forces prioritization decisions.

### Step 2: Define Milestones

Break the release cycle into phases with target dates:

```markdown
## Release Plan: v2.0.0

### Timeline

| Phase | Start | End | Duration | Description |
|---|---|---|---|---|
| Development | 2026-02-17 | 2026-03-14 | 4 weeks | Active feature development |
| Feature Freeze | 2026-03-15 | 2026-03-15 | 1 day | No new features merged after this date |
| Stabilization | 2026-03-15 | 2026-03-21 | 1 week | Bug fixes, documentation, testing only |
| RC1 | 2026-03-22 | 2026-03-22 | 1 day | First release candidate tagged |
| RC Testing | 2026-03-22 | 2026-03-28 | 1 week | Community/team testing of RC |
| RC2 (if needed) | 2026-03-29 | 2026-03-29 | 1 day | Second RC if critical issues found |
| Go/No-Go | 2026-03-31 | 2026-03-31 | 1 day | Final decision meeting |
| Release | 2026-04-01 | 2026-04-01 | 1 day | Tag, publish, announce |
```

Typical phase durations:
- **Development**: 50-70% of total cycle
- **Stabilization**: 15-25% of total cycle
- **RC testing**: 10-20% of total cycle

**Expected:** Milestone table with dates, durations, and descriptions for each phase.

**On failure:** If the timeline is too compressed (stabilization < 1 week), either extend the release date or reduce scope. Never skip stabilization.

### Step 3: Set Feature Freeze Criteria

Define what "feature freeze" means for this release:

```markdown
### Feature Freeze Criteria

After feature freeze (2026-03-15):
- **Allowed**: Bug fixes, test additions, documentation updates, dependency security patches
- **Not allowed**: New features, API changes, refactoring, dependency upgrades (non-security)
- **Exception process**: Feature freeze exceptions require written justification and approval from [release owner]

### Feature Priority List
| Priority | Feature | Status | Owner | Notes |
|---|---|---|---|---|
| P0 (must) | New export format | In progress | [Name] | Blocks release |
| P0 (must) | Security audit fixes | Not started | [Name] | Compliance requirement |
| P1 (should) | Performance optimization | In progress | [Name] | Defer if not ready |
| P2 (nice) | Dark mode support | Not started | [Name] | Defer to v2.1.0 if needed |
```

P0 features block the release. P1 features should be included if ready. P2 features are deferred without delay.

**Expected:** Feature freeze rules documented with exception process and prioritized feature list.

**On failure:** If P0 features are at risk of missing the freeze date, escalate immediately. Options: extend development phase, split the feature into a smaller deliverable, or defer to a point release (v2.0.1).

### Step 4: Plan Release Candidate Process

Define how release candidates are produced and tested:

```markdown
### Release Candidate Process

1. **RC1 Tag**: Tag from the stabilization branch after all P0 features merged and CI green
   ```bash
   git tag -a v2.0.0-rc.1 -m "Release candidate 1 for v2.0.0"
   ```

2. **RC Distribution**: Publish RC to staging/testing channel
   - R: `install.packages("pkg", repos = "https://staging.r-universe.dev/user")`
   - Node.js: `npm install pkg@next`
   - Internal: Deploy to staging environment

3. **RC Testing Period**: 5-7 business days
   - Run full test suite including integration tests
   - Verify all P0 features work as documented
   - Test upgrade path from previous version
   - Check for regressions in existing functionality

4. **RC Evaluation**:
   - **No critical/high bugs**: Proceed to release
   - **Critical bugs found**: Fix, tag RC2, restart testing period
   - **More than 2 RCs needed**: Revisit scope and timeline

5. **RC2+ Tags**: Only if critical issues found in previous RC
   ```bash
   git tag -a v2.0.0-rc.2 -m "Release candidate 2 for v2.0.0"
   ```
```

**Expected:** RC process documented with tagging convention, distribution method, testing checklist, and escalation criteria.

**On failure:** If the RC process is skipped (pressure to release), document the risk. Untested releases have higher rollback probability.

### Step 5: Define Go/No-Go Checklist

Create the criteria that must be met before release approval:

```markdown
### Go/No-Go Checklist

#### Must Pass (release blocked if any fail)
- [ ] All CI checks passing on release branch
- [ ] Zero critical bugs open against this version
- [ ] Zero high-severity security vulnerabilities
- [ ] All P0 features verified and documented
- [ ] Changelog complete and reviewed
- [ ] Upgrade path tested from previous version (v1.x -> v2.0.0)
- [ ] License and attribution files up to date

#### Should Pass (release proceeds with documented risk)
- [ ] Zero high bugs open (non-critical)
- [ ] All P1 features included
- [ ] Performance benchmarks within acceptable range
- [ ] Documentation reviewed and spell-checked
- [ ] External dependencies at latest stable versions

#### Decision
- **Go**: All "Must Pass" items checked, majority of "Should Pass" items checked
- **No-Go**: Any "Must Pass" item unchecked
- **Conditional Go**: All "Must Pass" checked, significant "Should Pass" items unchecked — document accepted risks
```

**Expected:** Go/no-go checklist with clear pass/fail criteria and decision rules.

**On failure:** If the go/no-go meeting results in no-go, identify the blocking items, assign owners, set a new target date (typically 1-2 weeks later), and update the release plan.

### Step 6: Document Rollback Plan

Define how to roll back if the release causes critical issues in production:

```markdown
### Rollback Plan

#### Rollback Triggers
- Critical bug affecting >10% of users
- Data corruption or loss
- Security vulnerability introduced by the release
- Breaking change not documented in changelog

#### Rollback Procedure
1. **Revert package registry**: Unpublish or yank the release
   - R/CRAN: Contact CRAN maintainers (cannot self-unpublish)
   - npm: `npm unpublish pkg@2.0.0` (within 72 hours)
   - GitHub: Mark release as pre-release, publish point fix

2. **Communicate**: Notify users via GitHub issue, mailing list, or social channels
   - Template: "v2.0.0 has been rolled back due to [issue]. Please use v1.x.y until a fix is released."

3. **Fix forward**: Prefer a v2.0.1 patch release over a full rollback when possible

4. **Post-mortem**: Conduct a post-mortem within 48 hours of rollback to identify process gaps

#### Point Release Policy
- v2.0.1 for critical bug fixes within 1 week of release
- v2.0.2 for additional fixes within 2 weeks
- Patch releases do not require full RC cycle but must pass CI and critical test suite
```

Write the complete release plan to `RELEASE-PLAN.md` or `RELEASE-PLAN-v2.0.0.md`.

**Expected:** Rollback plan documented with triggers, procedure, communication template, and point release policy. Complete RELEASE-PLAN.md written.

**On failure:** If rollback is not feasible (e.g., database migration already applied), document the forward-fix procedure instead. Every release should have a recovery path.

## Validation

- [ ] Release strategy (calendar/feature/hybrid) documented with rationale
- [ ] Milestone table includes all phases with dates: development, freeze, stabilization, RC, release
- [ ] Feature freeze criteria defined with allowed/disallowed change types
- [ ] Feature priority list categorized (P0 must / P1 should / P2 nice)
- [ ] RC process documented: tagging convention, distribution, testing period, escalation
- [ ] Go/no-go checklist has clear "must pass" and "should pass" sections
- [ ] Rollback plan includes triggers, procedure, and communication template
- [ ] RELEASE-PLAN.md (or equivalent) file created and saved
- [ ] Timeline is realistic (stabilization is at least 15% of total cycle)

## Common Pitfalls

- **No stabilization phase**: Going directly from development to release. Even a 3-day stabilization period catches issues that active development masks.
- **Scope creep after freeze**: Allowing "just one more feature" after feature freeze. Every post-freeze addition resets testing and introduces regression risk.
- **Ignoring P0 risks**: Not escalating early when a P0 feature is at risk. The earlier scope is adjusted, the less disruption to the timeline.
- **Skipping RC for "small" releases**: Even minor releases benefit from at least one RC. A day of RC testing is cheaper than a post-release hotfix.
- **No rollback plan**: Assuming the release will succeed. Every release plan should answer "what if this goes wrong?" before publishing.
- **Calendar pressure overriding quality**: Releasing on a date because it was promised, despite failing go/no-go criteria. A delayed release is a minor inconvenience; a broken release is a trust violation.

## Related Skills

- `apply-semantic-versioning` -- Determine the version number for the planned release
- `manage-changelog` -- Maintain the changelog that feeds into release notes
- `plan-sprint` -- Sprint planning within the development phase of the release cycle
- `draft-project-charter` -- Project charter may define the release roadmap and success criteria
- `generate-status-report` -- Track progress against release milestones
