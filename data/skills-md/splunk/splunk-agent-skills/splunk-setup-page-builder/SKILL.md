---
name: splunk-setup-page-builder
description: Build a certification-compliant first-run setup page for a Splunk app or add-on that collects non-secret settings via the configurations REST endpoint and secrets via storage/passwords, wires app.conf/default.meta correctly, and avoids the deprecated setup.xml mechanism. Use when the user wants a "Set up your app" screen, first-run configuration wizard, or a way to collect an endpoint/credential/API token for a Splunkbase app or TA. Route general app packaging, compatibility, upgrade, or removal lifecycle guidance unrelated to the setup page itself to app-and-add-on-lifecycle-advisor, and broader knowledge-object governance beyond this app's own default.meta to knowledge-object-governance.
license: Apache-2.0
allowed-tools:
  - shell
requires-mcp: false
metadata:
  splunk:
    domain: app-development
    products:
      - splunk-enterprise
      - splunk-cloud-platform
    entities:
      - setup pages
      - app.conf
      - configurations REST endpoint
      - storage/passwords
      - default.meta
      - Splunk apps and add-ons
      - AppInspect
    triggers:
      - setup page
      - first-run configuration
      - app setup screen
      - configure my app
      - splunkbase setup wizard
      - storage/passwords
      - credential setup
      - set up your app
    not-for:
      - replacing a full UCC-based (Add-on Builder) TA when the user explicitly wants UCC
      - collecting or logging raw credentials outside storage/passwords
      - installing or reconfiguring a production/shared Splunk instance without explicit user confirmation
      - modifying knowledge objects that belong to another app
      - general app packaging, compatibility, upgrade, deprecation, migration, or removal lifecycle guidance not tied to building the setup page itself
      - knowledge-object governance (ownership, orphans, ACL review, naming collisions) beyond this app's own default.meta
      - HEC or other data-ingestion configuration
      - authoring field extractions, CIM mappings, or SPL searches unrelated to the setup page
      - general Splunk product questions unrelated to setup pages
    outcomes:
      - setup_view wired in app.conf ([install] is_configured, [ui] setup_view)
      - Simple XML setup dashboard + JavaScript extension using the Splunk JS SDK
      - non-secret settings persisted via the configurations REST endpoint
      - secrets persisted encrypted via storage/passwords
      - default.meta permissions scoped to admin/power/sc_admin
      - a minimal home view/nav so the app doesn't fall through to unrelated shared content
      - an app.manifest and package that pass `splunk-appinspect` in both test and precert mode
---

# Splunk Setup Page Builder

Build a first-run setup page for a Splunk app or add-on: a screen that
appears the first time a user launches the app, collects whatever
configuration it needs (an endpoint URL, an API token, feature toggles,
etc.), and completes without using the deprecated `setup.xml` mechanism.

This is proven, not theoretical: the workflow below was built end-to-end
against a real Splunk Enterprise 10.4 instance, validated with
`splunk-appinspect` in both `test` and `precert` mode, and revised after
two real bugs were found during manual testing (see
[Known pitfalls](#known-pitfalls-fix-these-if-you-see-them-again) — do not
reintroduce either one). It was independently re-validated twice more by
fresh agent sessions with no prior context, each building a different toy
app from the instructions alone.

## Prerequisites

- A Splunk app directory to add the setup page to (existing app, or a
  fresh one you scaffold with `default/app.conf`, `default/data/ui/`, and
  `metadata/default.meta`).
- Target: Splunk Enterprise 9.x+ or Splunk Cloud Platform (equivalent
  release). No local Splunk instance is required to *write* the files, but
  installing into a real instance is required to verify them — see
  [Verification](#verification).
- `splunk-appinspect` installed locally for static validation
  (`pip install splunk-appinspect`; on macOS you may also need
  `brew install libmagic` for it to import cleanly).

## When to Use

Use this skill when a user is building a Splunk app/add-on for Splunkbase
(or an internal TA) that needs the user to provide configuration before it
can run — most commonly an API endpoint, credentials/token, or a small set
of feature settings — and wants a proper "Set up your app" experience
instead of hand-editing `.conf` files after install.

Do not use `default/setup.xml` for this. It is deprecated, unsupported on
Splunk Cloud Platform and search head clusters, and **fails Splunk
AppInspect's cloud check** (`check_setup_xml_in_default`) outright. Every
app that needs first-run configuration and wants to be Cloud-compatible
must use a setup *view* (Simple XML or React) instead, wired through
`app.conf`'s `[install] is_configured` / `[ui] setup_view`.

Do not install or reconfigure a production or shared Splunk instance
unless the user explicitly confirms that target. Never ask the user for
raw Splunk admin credentials — use whatever session/auth Splunk Web
already provides via the JS SDK.

Stay scoped to building the setup page itself. Route adjacent requests:

- General app/add-on packaging, compatibility, upgrade, deprecation, or
  removal guidance not about the setup page → `app-and-add-on-lifecycle-advisor`
  (advisory-only; it will not write or install anything — this skill remains
  the one that actually builds the setup page).
- Governance of existing shared knowledge objects (ownership, orphans, ACL
  review, naming collisions) beyond this app's own `default.meta` →
  `knowledge-object-governance`.
- HEC or other data-ingestion setup/troubleshooting →
  `hec-setup-and-troubleshooting`.
- Authoring field extractions, CIM mappings, or ad hoc SPL unrelated to the
  setup page → `field-extraction-and-cim-mapping` or `splunk-search`.
- General Splunk product questions unrelated to setup pages →
  `splunk-product-question-navigator`.

## Architecture

```
<app>/
├── app.manifest                              # required metadata for packaging/AppInspect
├── default/
│   ├── app.conf                               # [install] is_configured, [ui] setup_view, [triggers]
│   └── data/ui/
│       ├── views/
│       │   ├── setup_page_dashboard.xml       # the setup view (Simple XML)
│       │   └── home.xml                       # minimal landing view (see below)
│       └── nav/
│           └── default.xml                    # declares home.xml as the default view
├── metadata/
│   └── default.meta                           # permissions for the app + any custom conf file
├── appserver/static/
│   ├── javascript/setup_page.js               # setup logic, uses the Splunk JS SDK
│   └── styles/setup_page.css
└── README/
    └── <settings_conf_file>.conf.spec         # spec for any custom conf file you introduce
```

Two storage backends, chosen per field:

| Field type | Storage | Why |
| --- | --- | --- |
| Non-secret setting (URL, toggle, interval, ...) | The built-in `configurations` REST collection, targeting a custom `<name>.conf` file you define | No custom Python REST handler needed. Works out of the box, Cloud-safe. |
| Secret (token, password, API key) | `storage/passwords` | Splunk encrypts and stores it in `passwords.conf`; never write a secret into a plain conf file — that is an AppInspect failure and a real security risk. |

## Workflow Overview

### 1. Gather requirements

Ask the user (or infer from context):
- App id / directory (must match `app.conf [package] id` — letters,
  numbers, dots, underscores only).
- Which fields are non-secret settings vs. secrets. For each: name, type,
  required/optional, validation rule.
- Whether the app already has other views. If not, you'll add a minimal
  home view (step 6) so the app doesn't land users on unrelated shared
  content after setup.
- Whether this app already has a setup page to extend, or needs one from
  scratch.

### 2. Wire `app.conf`

```ini
[install]
is_configured = 0

[package]
id = <app_id>
check_for_updates = false

[id]
name = <app_id>
version = 1.0.0

[ui]
is_visible = 1
label = <Human Readable Label>
# No file extension; resolves to default/data/ui/views/setup_page_dashboard.xml
setup_view = setup_page_dashboard

[launcher]
author = <author>
description = <description>
version = 1.0.0

[triggers]
# One reload.<conf_file> line per custom conf file the setup page writes.
reload.<settings_conf_file> = simple
```

`check_for_updates = false` and the `[triggers]` reload line are both
things AppInspect will flag if you skip them — see
[AppInspect findings you should expect and fix](#appinspect-findings-you-should-expect-and-fix).

`[id] version` and `[launcher] version` are two separate fields that
must be kept equal to each other. Nothing enforces this automatically;
update both together at every release, or AppInspect/Splunkbase may see
a mismatched version depending on which field a given check reads.

### 3. Build the setup view (Simple XML + JS)

`default/data/ui/views/setup_page_dashboard.xml`:

```xml
<dashboard isDashboard="false"
           script="javascript/setup_page.js"
           stylesheet="styles/setup_page.css"
           hideTitle="true"
           version="1.1">
    <row>
        <panel>
            <html>
                <div id="main_container">
                    <h3>&lt;Human Readable Label&gt;</h3>
                    <!-- one <input> per field, plus a submit button and
                         success/error containers. See
                         references/setup-page.js for a complete
                         two-field (one setting + one secret) example. -->
                </div>
            </html>
        </panel>
    </row>
</dashboard>
```

`appserver/static/javascript/setup_page.js` uses the Splunk JS SDK
(`splunkjs/splunk`, loaded via `require`). The full, proven implementation
— validation, saving non-secret settings, saving secrets, completing
setup, reload + redirect, error rendering — is in
[`references/setup-page.js`](references/setup-page.js). **Copy it and
adapt the field names/validation; do not rewrite the SDK plumbing from
scratch** — it has already had two real bugs found and fixed in it (see
[Known pitfalls](#known-pitfalls-fix-these-if-you-see-them-again)). The
conventions below are implicit in that file; they are restated here so
you don't have to reverse-engineer them from the code:

- **Naming the settings conf file itself**: use `<app_id>_settings`
  (e.g. `my_app_settings`) unless the app already has a more specific
  name in mind. This is the `<name>.conf` file the `configurations`
  collection creates — not fixed by Splunk, just pick one and stay
  consistent with it everywhere (JS, `.conf.spec`, `[triggers]` reload
  line).
- **Stanza naming**: the stanza name inside that conf file is, likewise,
  not fixed by Splunk — pick something descriptive tied to the setting
  group (e.g. `region_settings` for a `region` field, `polling_settings`
  for a poll-interval field). Keep it consistent between the JS and the
  `.conf.spec` you write in step 7.
- **Naming the `storage/passwords` realm and name**: tie the realm to
  the app (`<app_id>_realm`) and the name to the specific secret field
  (the field's own name, e.g. `api_token`, `webhook_signing_secret`).
  This keeps multiple secrets in the same app distinguishable and
  matches the key format below.
- **You do not ship `default/<settings_conf_file>.conf` at all.** The
  `configurations` REST collection creates the file and stanza on disk in
  `local/` the first time the setup page saves — that's the whole point
  of using it instead of a custom REST handler. Only `default/app.conf`,
  `default/data/ui/*`, `metadata/default.meta`, and `app.manifest` are
  things you author; the settings conf file is runtime-created output,
  not a source file.
- **`storage/passwords` lookup key format is `<realm>:<name>:`** — realm,
  name, and a literal trailing colon, colon-joined. Build this string
  exactly this way to check whether a credential already exists
  (`passwords.item(key)`) before deciding whether to `create` or
  `update` it. Getting this wrong means every "update" silently becomes
  a no-op-then-mismatch or a duplicate.
- **Validate every field for its actual shape, not just presence or a
  prefix.** The URL example in
  [Known pitfalls](#known-pitfalls-fix-these-if-you-see-them-again) #1 is
  one instance of a general rule: presence-only or prefix-only checks
  pass garbage. Write a real pattern/range check for whatever the field
  actually is (a region code, a port number, an email, etc.), not just
  "is it non-empty."

### 4. Add a minimal home view + nav

If the app has no other views, add:

`default/data/ui/views/home.xml` — a one-panel dashboard explaining what
the app does and where to go to reconfigure it later.

`default/data/ui/nav/default.xml`:

```xml
<nav search_view="search" color="#5C6773">
    <view name="home" default="true" />
</nav>
```

Without this, clicking the app in Splunk Web's sidebar falls through to
whatever shared/global dashboard happens to exist on the instance (e.g.
another installed app's globally-exported dashboard), which is confusing
and looks broken even though the setup page itself works correctly.

### 5. Set permissions in `metadata/default.meta`

```ini
[]
access = read : [ * ], write : [ admin, power, sc_admin ]
export = none

[<settings_conf_file>]
access = read : [ admin, power, sc_admin ], write : [ admin, power, sc_admin ]
export = none
```

Include `sc_admin`, not just `admin` — `admin` alone is not available to
Splunk Cloud customers and AppInspect will warn on it
(`check_kos_are_accessible`).

### 6. Add `app.manifest`

Required for packaging/AppInspect (`check_for_valid_package_id`). Minimal
shape:

```json
{
  "schemaVersion": "2.0.0",
  "info": {
    "title": "<Human Readable Label>",
    "id": { "group": null, "name": "<app_id>", "version": "1.0.0" },
    "author": [{ "name": "<author>", "email": null, "company": null }],
    "releaseDate": null,
    "description": "<description>",
    "classification": { "intendedAudience": null, "categories": [], "developmentStatus": null },
    "commonInformationModels": null,
    "license": { "name": null, "text": null, "uri": null },
    "privacyPolicy": { "name": null, "text": null, "uri": null },
    "releaseNotes": { "name": null, "text": null, "uri": null }
  },
  "dependencies": {},
  "tasks": [],
  "inputGroups": {},
  "incompatibleApps": {},
  "platformRequirements": { "splunk": { "Enterprise": "*" } }
}
```

### 7. Write the conf spec for any custom settings file

`README/<settings_conf_file>.conf.spec` documenting every stanza/key you
introduce, using standard Splunk `.conf.spec` syntax — a `[stanza]`
header, `key = <type>` for each setting, and `*`-bulleted description
lines directly beneath it:

```
[<settings_stanza>]
<field_name> = <string>
* <what this field is and any format constraint, e.g. "Must look like a
  region code, e.g. us-east-1.">
* No default.
```

Use the value-type token that actually matches the field, not always
`<string>` — common ones are `<string>`, `<integer>`, `<bool>`,
`<seconds>`. For example, an integer field constrained to a range:

```
[<settings_stanza>]
poll_interval_seconds = <integer>
* How often, in seconds, the app polls its data source.
* Must be an integer between 30 and 3600 inclusive.
* No default.
```

This file is documentation for administrators, and the `configurations`
REST endpoint does not enforce these types or constraints itself.
Client-side JS validation only improves the setup-page experience; any
backend code or modular input that later consumes these values must
re-validate them before use. A value can reach the underlying conf file
through a path that never goes through your JS at all — a direct
`local/<file>.conf` edit, or a raw REST call to the same endpoint — so
nothing downstream may assume the setup page's validation ran.

Never document a secret field here — secrets don't go in this file at
all, since they never live in a plain conf file in the first place.

## Known pitfalls (fix these if you see them again)

These were found by actually testing this pattern end-to-end, not by
inspection. Both are easy to reintroduce if you copy an older reference
example without care.

1. **Presence-only or prefix-only validation.** This is a general rule,
   not just a URL-specific one: any check that only asks "is this
   non-empty" or "does this start with the right prefix" lets garbage
   through. The concrete case that was actually found: a regex like
   `/^https?:\/\//` accepts the literal string `http://` with nothing
   after it as a "valid" URL. Fixed by requiring a host:
   `/^https?:\/\/[^\s]+\..+/i`. Apply the same standard to every field —
   write a real pattern/range/format check for what the field actually
   is (a region code, a port number, a non-empty-and-shaped secret,
   etc.), not just presence.

2. **Do not gate the save on `is_configured`.** Splunk's own official
   setup-page examples check `is_configured` at the top of the submit
   handler and, if already `1`, skip straight to reload+redirect without
   saving anything. This silently discards any new values a user enters
   when they reopen the setup page later (e.g. via **Manage Apps > Set
   up**) to rotate a token or change a setting — verified by reproducing
   it: the encrypted password in `passwords.conf` was byte-for-byte
   unchanged after "updating" it, because the save was never reached.
   Always perform steps 2-5 of the workflow on submit, regardless of the
   current `is_configured` value. Splunk's platform-level redirect
   behavior (driven by `is_configured`) already prevents this page from
   being forced on users who are already configured; the submit handler
   does not need to re-enforce that.

   **This rule is about the behavior, not one specific variable name.**
   The submit handler (`completeSetup` / `onSubmit` / whatever you name
   it) must call the save logic — write the setting, write the secret,
   set `is_configured`, reload, redirect — **unconditionally, every
   time the user clicks submit.** Do not add *any* early-exit guard
   before the save that checks `is_configured`, under any name:
   `isAlreadyConfigured`, `isConfigured`, `alreadyConfigured`,
   `configuredAlready`, `skipIfConfigured`, `skipSave`, or anything
   equivalent. If you find yourself writing an `if` statement that reads
   `is_configured` and can `return` before reaching the save calls,
   delete it — that is this exact bug, regardless of what you called
   the variable.

## Verification

Static analysis alone is not sufficient proof — verify both:

1. **AppInspect** (catches structural/certification issues):
   ```sh
   splunk-appinspect inspect <app_dir_or_package> --mode test
   splunk-appinspect inspect <app_dir_or_package> --mode precert
   ```
   Expect 0 `error`/`failure`. Common findings to expect on a fresh app
   and how to fix them: see
   [`references/appinspect-checklist.md`](references/appinspect-checklist.md).

2. **A real Splunk instance** (catches behavioral issues AppInspect
   cannot see, like the two pitfalls above). Do not install into a
   production or shared instance without explicit confirmation. Minimum
   manual pass:
   - Fresh install with `is_configured=0` → confirm redirect to the setup
     page.
   - Submit with required fields empty → confirm validation blocks submit,
     no REST calls made.
   - Submit a field that satisfies "non-empty" but not real format
     validation (e.g. `http://` alone for a URL field) → confirm it is
     still rejected.
   - Submit valid values → confirm success message, redirect, and that
     the non-secret setting lands in the custom conf file and the secret
     lands **encrypted** in `passwords.conf` (never plaintext).
   - Restart Splunk → confirm `is_configured=1` persisted and the app does
     not redirect back to setup.
   - Reopen **Set up** and submit a new value for the secret → confirm the
     existing password entry is updated in place (no duplicate stanza),
     per pitfall #2 above.
   - Click the app in the sidebar → confirm it lands on the app's own home
     view, not unrelated shared content.

## Examples

- "Add a setup page to this add-on that collects a base API URL and an API
  token before the app can run." → gather the two fields, wire `app.conf`,
  build the setup view + JS from `references/setup-page.js`, add a home
  view/nav, set `default.meta`, add `app.manifest`, then verify with
  AppInspect and a real instance.
- "This app already has `app.conf` and a nav; add first-run setup that
  stores a webhook signing secret and a poll interval between 30 and 3600
  seconds." → same workflow, but skip step 4 (home view/nav already
  exists) and use range/length validation instead of a URL pattern, per
  the "validate every field for its actual shape" rule.
- "Our setup screen uses `default/setup.xml` and fails Splunk Cloud
  AppInspect vetting." → remove `default/setup.xml` entirely and rebuild
  the same fields as a `setup_view` per this skill's workflow; do not try
  to patch or relocate the existing `setup.xml`.

## Troubleshooting

- **AppInspect reports "Do not use `default/setup.xml` in the Cloud
  environment."** Remove the file; there is no supported way to keep it
  for Cloud compatibility. Rebuild the same configuration as a
  `setup_view` (this skill's entire approach).
- **AppInspect reports "Invalid XML File" or an undefined-entity error
  (e.g. `mdash`).** XML only defines five built-in entities (`&amp; &lt;
  &gt; &apos; &quot;`). Replace any named HTML entity (`&mdash;`,
  `&nbsp;`, etc.) with its numeric form (`&#8212;`, `&#160;`).
- **Changes to `setup_page.js` don't seem to take effect after
  reinstalling/restarting.** Splunk Web (and the browser) aggressively
  cache static JS. A `splunk restart` alone does not guarantee a fresh
  fetch. Hard-refresh (Cmd/Ctrl+Shift+R) or open the page in a private/
  incognito window before concluding a fix didn't work.
- **Reopening the setup page later ("Set up" from Manage Apps) to change
  a value has no effect** — the value looks unchanged after submit. This
  is [pitfall #2](#known-pitfalls-fix-these-if-you-see-them-again): an
  `is_configured` gate is silently skipping the save. Remove the gate.
- **Clicking the app in Splunk Web's sidebar lands on an unrelated
  dashboard from a different app.** The app has no home view/nav of its
  own, so Splunk falls through to shared/globally-exported content from
  another app. Add `default/data/ui/views/home.xml` and
  `default/data/ui/nav/default.xml` (step 4).
- **"Manage Apps" or "Set up" is unreachable, or Splunk reports a
  license feature error (e.g. `Requires license feature='Auth'`).** The
  target instance is running under a Free license, which disables
  authentication/RBAC entirely. This skill's setup pages depend on
  roles/capabilities and `storage/passwords`, both part of the Auth
  system — verification requires a Trial or Enterprise-licensed
  instance, not Free.

## Safety

- Never store a secret anywhere other than `storage/passwords`. Never log
  a secret value (including in error messages shown to the user).
- Never ask the user to type raw Splunk admin credentials into anything
  you write; rely on the session the JS SDK already has via Splunk Web.
- Do not install, restart, or reconfigure a shared/production Splunk
  instance without the user's explicit confirmation of that target.
- Do not modify knowledge objects belonging to another app.
