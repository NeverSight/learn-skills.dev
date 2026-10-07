---
name: monomind-before-after
description: "Create verified before/after screenshot comparisons for UI changes and emit a PR-ready Markdown table through the external @vercel/before-and-after CLI. Use for visual diffs, PR screenshots, production-versus-preview URLs, image pairs, mobile or responsive viewports, or CSS-selector element proof. Skip non-visual claims."
---

# Monomind Before and After

Produce a controlled visual comparison, verify both captures, and package the pair for review. This skill integrates with the external [`@vercel/before-and-after`](https://www.npmjs.com/package/@vercel/before-and-after) package; it does not vendor or relicense that software. The package remains subject to [PolyForm Shield 1.0.0](https://polyformproject.org/licenses/shield/1.0.0).

## Establish the comparison

Collect these inputs before capture:

- **Before source:** a deployed URL, local URL, or existing image.
- **After source:** a deployed URL, local URL, or existing image.
- **Capture boundary:** whole viewport, full page, or a stable element selector.
- **Viewport:** desktop, mobile, tablet, or an explicit size.
- **Destination:** local evidence only, Markdown output, or a specific pull request.

The current task state is usually the after source, but never infer the before source. If only one state is supplied, ask for the missing comparison source. Do not switch branches, stash work, or start an unknown server to manufacture it.

## Preflight

1. Record the revision or deployment id represented by each source and verify that local URLs are served by the intended task process.
2. Open or probe both sources. Stop on authentication, protection, or routing failures instead of capturing an error page. Use approved credentials or a project-approved bypass only within existing authority.
3. Check for the scoped CLI:

   ```bash
   command -v before-and-after
   before-and-after --help
   ```

   Verify the installed help before relying on flags and record the package version when the CLI exposes it. If it is absent, use `npx --yes @vercel/before-and-after` for a one-off run or install the documented toolchain with `npm i -g @vercel/before-and-after agent-browser` only when package download or global installation is authorized. Never substitute the unscoped package name.
4. Remove notifications, secrets, personal data, payment data, and unrelated windows from the capture surface.

## Capture matched states

Use the same data, authentication state, viewport, and boundary on both sides. Prefer a stable selector when the changed element occupies only part of the page.

```bash
# Two URLs or two image paths
before-and-after "<before>" "<after>" --output "<artifact-dir>"

# One matching selector
before-and-after "<before-url>" "<after-url>" "<selector>" --output "<artifact-dir>"

# Different selectors when the element structure changed
before-and-after "<before-url>" "<after-url>" "<before-selector>" "<after-selector>" --output "<artifact-dir>"

# One-off execution without a global install
npx --yes @vercel/before-and-after "<before>" "<after>" --output "<artifact-dir>"

# Approved public pair with PR-ready Markdown output
before-and-after "<before>" "<after>" --markdown
```

Use the CLI's `--mobile` or `--size <WxH>` mode when a mobile, tablet, or custom viewport is part of the claim; for example, use `--size 768x1024` for the documented tablet dimensions. Use `--full` only when full-page or scroll coverage is explicitly required; a focused viewport or element makes most changes easier to review.

Store outputs in the repository's gitignored evidence directory or `.artifacts/<task>/`.

## Produce PR-ready Markdown

`--markdown` may upload images. The published package documentation names `0x0.st` as its default public upload destination, so classify the captures before running it:

- For approved public screenshots, generate the table with the package's Markdown mode.
- For private or sensitive captures, use a project-approved `--upload <handler>` or keep the pair local and return the paths.
- If publication authority is missing, stop after local verification; do not upload merely to make a table render.

When a pull request update is authorized, preserve its existing body and add one comparison section containing the generated table. Reopen the PR and confirm both images render before claiming integration succeeded.

The review surface should contain one clear pair:

```markdown
| Before | After |
| --- | --- |
| ![Before](<approved-before-url>) | ![After](<approved-after-url>) |
```

## Verify the evidence

Open both output images at full resolution and confirm:

- the intended states, element, viewport, and data match;
- the changed behavior is visible without relying on the caption;
- neither side shows an error page, loading placeholder, overlay, or sensitive data;
- any uploaded URLs resolve from the review surface;
- the report names both source revisions/deployments, viewport, selector, command, output, and caveat.

## Completion criteria

- Before and after are genuine matched states from identified sources.
- The pair visibly supports the stated UI claim.
- Local files and any published URLs were inspected successfully.
- The Markdown table is PR-ready or the missing publication authority is explicit.
- External package installation, upload, and PR mutation stayed within authority.
