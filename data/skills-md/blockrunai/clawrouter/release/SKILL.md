---
name: release
description: Use this skill for EVERY ClawRouter release. Enforces the full checklist — version sync, CHANGELOG, blockrun server constant, build, tests, npm publish, git tag, GitHub release. No step can be skipped.
---

# ClawRouter Release Checklist

**This skill is mandatory for every release. Execute every step in order. Do not skip.**

## Step 1: Confirm the New Version

Read the current version:

```bash
cat package.json | grep '"version"'
```

Ask: "What version are we releasing?" Confirm it follows semver and is higher than current.

---

## Step 2: Update `package.json` Version

Edit `package.json` — bump `"version"` to the new version.

---

## Step 3: Write CHANGELOG Entry

Open `CHANGELOG.md`. Add a new section at the top (after the header) in this format:

```markdown
## v{VERSION} — {DATE}

- **Feature/Fix name** — description
- **Feature/Fix name** — description
```

Rules:

- Date format: `Mar 8, 2026`
- One bullet per logical change
- Every bullet must be present — no "see git log"
- Include **all** changes since the previous release

---

## Step 4: Sync `CURRENT_CLAWROUTER_VERSION` in blockrun

**This is the most commonly forgotten step.**

File: `/Users/vickyfu/Documents/blockrun-web/blockrun/src/app/api/v1/chat/completions/route.ts`

Find this line:

```typescript
const CURRENT_CLAWROUTER_VERSION = "x.y.z";
```

Update it to match the new version. Verify with:

```bash
grep CURRENT_CLAWROUTER_VERSION /Users/vickyfu/Documents/blockrun-web/blockrun/src/app/api/v1/chat/completions/route.ts
```

**Do not skip this.** It controls the update nudge shown to users running outdated versions.

---

## Step 5: Build

```bash
npm run build
```

Fix any TypeScript or build errors before proceeding.

---

## Step 6: Run Tests

```bash
npm test
npm run typecheck
npm run lint
```

All must pass. Fix failures before proceeding.

---

## Step 7: Commit Everything

Stage and commit:

```bash
git add package.json CHANGELOG.md
git commit -m "chore: bump version to {VERSION}"
```

If blockrun's route.ts was updated, commit that separately in the blockrun repo.

---

## Step 8: Push to GitHub

```bash
git push origin main
```

---

## Step 9: Create Git Tag

```bash
git tag v{VERSION}
git push origin v{VERSION}
```

---

## Step 10: Create GitHub Release

```bash
gh release create v{VERSION} \
  --title "v{VERSION}" \
  --notes "$(sed -n '/^## v{VERSION}/,/^## v[0-9]/p' CHANGELOG.md | head -n -1)"
```

Verify the release on GitHub: https://github.com/BlockRunAI/ClawRouter/releases

The release notes **must** match the CHANGELOG entry exactly.

---

## Step 11: Publish to npm

```bash
npm publish --access public
```

Verify: https://npmjs.com/package/@blockrun/clawrouter

Expected output: `+ @blockrun/clawrouter@{VERSION}`

---

## Step 12: Final Verification

Run this checklist to confirm everything is in sync:

```bash
# 1. package.json version
cat package.json | grep '"version"'

# 2. CHANGELOG has the entry
head -10 CHANGELOG.md

# 3. blockrun CURRENT_CLAWROUTER_VERSION
grep CURRENT_CLAWROUTER_VERSION /Users/vickyfu/Documents/blockrun-web/blockrun/src/app/api/v1/chat/completions/route.ts

# 4. npm package is live
npm view @blockrun/clawrouter version

# 5. GitHub tag exists
git tag | grep v{VERSION}

# 6. GitHub release exists
gh release view v{VERSION}
```

All 6 must match the new version. If any mismatch, fix before declaring the release done.

---

## Common Mistakes (Never Repeat These)

| Mistake                                                   | Prevention                            |
| --------------------------------------------------------- | ------------------------------------- |
| Forgot to update `CURRENT_CLAWROUTER_VERSION` in blockrun | Step 4 — always check                 |
| CHANGELOG entry missing or incomplete                     | Step 3 — write it before building     |
| npm publish before tests pass                             | Steps 5-6 must precede Step 11        |
| GitHub release notes empty                                | Step 10 — extract from CHANGELOG      |
| Git tag not pushed                                        | Step 9 — push tag separately          |
| docs not reflecting new features                          | Update docs in same PR as the feature |
