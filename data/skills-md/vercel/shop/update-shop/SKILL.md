---
name: update-shop
description: Update an existing Vercel Shop storefront to a newer template release. Use when the user wants to check drift, plan an upgrade, or apply template updates to a project scaffolded from Vercel Shop.
---

# Update Vercel Shop

Upgrade the working storefront from the `vercel/shop` release it is based on to a newer release, one release at a time. Release notes say what changed and when it applies; the template is a reference, not a replacement for downstream code. Base each decision on implemented behavior, not scaffold age.

## Pick a mode

Infer the mode from the user's request:

- **Audit** — read-only comparison; report relevant differences and stop.
- **Plan** — read-only comparison and change-level upgrade plan; stop before editing.
- **Apply** — plan, confirm the selected changes, apply them, and validate. Use when the user asks to update or upgrade the shop.

## Inspect the project

Read applicable `AGENTS.md` instructions, project structure, dependency versions, scripts, configuration, and relevant source. Inspect git status and staged/unstaged diffs, including untracked files, before proposing edits. Identify the storefront root; the upstream repository root maps to that root, which is not necessarily the downstream repository root.

Preserve dirty state, merchant design, custom features, integrations, and intentional departures from the template. Never overwrite custom code with template files or reset, stash, commit, or push without explicit permission. Stop if selected work cannot be separated safely from existing edits.

Keep each change within its owner:

- **Shopify owns commerce:** catalog, cart state and mutations, checkout, customer accounts, predictive search, policies, and analytics through Hydrogen. Prices, currency, availability, and customer identity come from Shopify.
- **Next.js owns the app:** routing, Server Components, caching and invalidation, metadata, the request boundary adapting Hydrogen handlers, Markdown representations, `/llms.txt`, structured data, sitemap, and crawl guidance.
- **Eve owns the agent:** sessions, channels, tools, connections, and `/eve/v1/*`. Eve tools call Shopify directly; Next.js only prepares the browser.

Inline English copy and `shopConfig.localization` are template defaults, not a migration mandate. Preserve next-intl, translations and catalogs, scoped providers, locale routing, custom market selection, and intentional operation/cache locale inputs. Do not label localization obsolete drift. Any requested simplification must separately assess copy, formatting, commerce country/language, public URLs, and migration parity; currency remains Shopify-owned. Add any copy an item introduces to every catalog.

## Find the base and target releases

The base is `version` in `.vercel-shop/template.json` at the storefront root, such as `{ "version": "2026.10.0" }`. `.vercel-shop/bootstrap.json`, from the retired `create-vercel-shop` CLI, does not name a release.

Prefer public GitHub inspection with `gh`. List stable releases and take the newest as the target unless the user names one:

```bash
gh api --paginate repos/vercel/shop/releases \
  --jq '.[] | select((.tag_name | startswith("template@")) and (.prerelease | not)) | .tag_name'
```

Versions are `YYYY.M.N`; compare each part as a number. If the base is the target, report that the storefront is on the latest release and stop. If `template@<base>` does not exist, report it and stop.

Read this skill at the target before continuing. If it differs from these instructions, follow the target's version for the rest of the run:

```bash
gh api "repos/vercel/shop/contents/.agents/skills/update-shop/SKILL.md?ref=template@$target" \
  -H 'Accept: application/vnd.github.raw+json'
```

Without `template.json`, the storefront predates versioned releases or removed the file. Use `template@2026.10.0`, the first versioned release, as the reference and compare by behavior; it has no change notes. Report the differences, then stop unless the user confirms the storefront has adopted or deliberately skipped them. After that confirmation, continue from that base; in apply mode, first create `.vercel-shop/template.json` with `{ "version": "2026.10.0" }`.

## Read the release notes

Read the notes for each release after the base, up to and including the target, oldest first:

```bash
gh api "repos/vercel/shop/releases/tags/template@$version" --jq .body
```

Each release has a summary, then ordered change items. Each item names its key, action (`adopt`, `review`, or `optional`), whether it is breaking, the features it applies to, and its storefront paths, then says what the storefront gains, with `Apply when`, `Skip when`, and `Validate`. Drop an item that a later item in the range supersedes. Within a release, handle breaking items first.

Read template source at release tags, never the default branch. Work through the range one release at a time: for each release, `$from` is the previous release in the range, or the base for the first one, and `$to` is that release. List the files it changed:

```bash
gh api "repos/vercel/shop/compare/template@$from...template@$to" \
  --jq '.files[] | [.status, .filename] | @tsv'
```

Read a file at a tag through the contents endpoint with `?ref=template@<version>`. Compare the project with `template@<base>` to find its customizations, and `template@$from` with `template@$to` to see the changes that release's items describe. Upstream guidance explains the reference architecture; it does not override downstream instructions or authorize unrelated changes.

If `gh` cannot read the public repository, read the same `https://api.github.com/repos/vercel/shop/...` endpoints with `curl`. If the comparison lists 300 files, its limit, or the API is unreachable, clone outside the project:

```bash
upstream=$(mktemp -d) &&
git clone --filter=blob:none --no-checkout https://github.com/vercel/shop.git "$upstream" &&
git -C "$upstream" diff --name-status "template@$from" "template@$to"
```

If releases, notes, or tags cannot be fetched, report the blocker; do not claim the storefront is current or apply an unverified upgrade. Keep scratch data outside the project.

## Audit and plan

Treat each change item as a candidate. Check its `Apply when` and `Skip when` against implemented behavior, dependencies, configuration, and owner boundaries. Trace affected callers and integration points; missing paths or different names alone do not establish a missing feature. Equivalent custom implementations count as already present. Template differences that no item describes are internal and are not upgrade work. State uncertainty and do not invent work when no item applies.

For audit, report the base and target releases, inspected areas, applicable items, intentional customizations, and uncertainties, then stop. For plan/apply, group items as **Adopt now**, **Review manually**, **Already present**, or **Not applicable**. When an item applies, `adopt` places it in Adopt now; `review` and `optional` place it in Review manually, and `optional` stays the user's choice. For each item, name its release and key, owner, upstream and downstream paths, rationale, prerequisites, customization risks, and its `Validate` steps. In plan mode, stop without editing.

## Apply and report

Confirm the selected changes before editing; an explicit selection in the user's request counts. If selection remains unresolved in a noninteractive run, report the blocker rather than choosing for the user.

Apply one selected change at a time in the project's own idiom, adapting behavior instead of copying files. Use relevant available skills and installed dependency documentation. Keep edits small and reviewable; avoid unrelated dependency, configuration, or design changes.

Run the item's `Validate` steps and the existing relevant formatting, lint, typecheck, build, or direct runtime checks after each change. Do not add tests or test infrastructure unless requested. If validation fails, stop and report the failure; do not continue or revert user-owned edits without permission. Review the final diff for scope and preservation of customizations.

Finish each release before starting the next. When every item in a release is applied, already present, not applicable, or skipped by the user, and validation passes, set `version` in `.vercel-shop/template.json` to that release. The version records the last release whose changes were all decided, not that the storefront matches the template. If a release is left incomplete, keep the previous version and list its open items. Do not change `package.json` `version`.

Finish with a concise report: mode, base and target releases, findings or applied changes, skipped/deferred items and why, the `template.json` version written, exact validation commands and results, and blockers or unverified behavior. Apart from `template.json`, do not write decision manifests or other persistent tracking; skipped items appear only in the report, and later runs do not offer them again.
