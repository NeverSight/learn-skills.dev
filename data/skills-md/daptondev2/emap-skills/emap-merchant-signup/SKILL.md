---
name: emap-merchant-signup
description: >-
  Guides a partner building an EMAP merchant-signup form on their own
  website. Covers Integration 1 (full form — all 6 signup steps hosted on the
  partner site, each step proxied to EMAP's API), Integration 2 (redirect
  handoff — browser redirects to EMAP with step-1 data in URL params, EMAP
  prefills and auto-submits the form), and Integration 3 (email-based signup —
  partner backend POSTs step-1 data to EMAP's REST API, EMAP creates the record
  and emails the merchant a secure link to complete their full application).
  Provides field references, code templates, and a security checklist.
---

# Merchant Signup Integration

A developer guide for embedding an EMAP merchant signup form on a partner website.
The merchant fills in their basic business information on the **partner's site**;
EMAP handles all subsequent steps (company details, banking, e-signature) — or,
with Integration 1, the partner hosts all 6 steps themselves.

**Contents**
- [Before you start — Required questions](#before-you-start--required-questions) ← **start here, always**
- [Reference files](#reference-files) — load only when implementing that feature
- [Step 0: Detect project setup](#step-0-detect-project-setup)
- [Step 0.5: Install the verify gate hook](#step-05-install-the-verify-gate-hook) ← **do this before writing any code**
- [Step 1: Partner attribution (optional)](#step-1-partner-attribution-optional)
- [Step 2: Choose integration mode](#step-2-choose-integration-mode)
- [Build Integration 1: Full form](#build-integration-1-full-form)
- [Build Integration 2: Redirect handoff](#build-integration-2-redirect-handoff)
- [Build Integration 3: Email-based signup](#build-integration-3-email-based-signup)
- [Integration 3: Resume link](#integration-3-resume-link)
- [Verify loop: schema conformance](#verify-loop-schema-conformance) ← **run before calling any build done**
- [Verify: security and coverage](#verify-security-and-coverage)
- [Guardrails](#guardrails)

---

## Before you start — Required questions

> **STOP. Do not read any reference files, do not open any templates, and do not generate any code until BOTH questions below have been asked and answered by the developer.**

### Question 1 — Which integration variant?

Use AskUserQuestion with exactly these 3 options (no other options, no sequence numbers in labels):

- **Redirect handoff (Integration 2)** — The merchant fills out a single step-1 form on your site. On submit, they are redirected straight into EMAP's onboarding signup flow to complete the remaining steps. No backend required.
- **Full form (Integration 1)** — You host the entire 6-step merchant signup experience on your site. The merchant completes all steps (1–6) without ever leaving your platform. Each step is proxied to EMAP's API. Requires a backend.
- **Email-based signup (Integration 3)** — The merchant fills out a single step-1 form on your site. Your backend submits it to EMAP, which creates their account and sends them a secure resume link by email. The merchant clicks the link and continues the full onboarding flow from their inbox. Requires a backend.

Do not proceed until the developer has chosen one of the three variants.

### Question 2 — Partner key

After the developer has chosen their variant, use AskUserQuestion with exactly these 3 options. The description for each option must include the retrieval instructions exactly as written below — this is what the developer reads to know where to find or get their key:

- **Yes, I have a partner key** — description: "Log in to the partner portal → Integration → API Integration → copy the API key shown there → paste it here."
- **No, I don't have a partner key** — description: "Sign up as a partner at https://emap.easypaydirect.com/signup/partner. Once registered, go to Integration → API Integration → copy the partner key → come back and paste it here."
- **Skip (proceed without a key)** — description: "Signups will still work, but they won't be attributed to your partner account."

**If the developer selects "Yes, I have a partner key":**
Ask them to paste the key now. Store it mentally as `EMAP_PARTNER_KEY`. Proceed to Step 0.

**If the developer selects "No, I don't have a partner key":**
Tell them to follow the sign-up link in the option description above, then come back and paste their key in the chat when ready. Proceed to Step 0 without a key for now — if they paste it later, use it as `EMAP_PARTNER_KEY`.

**If the developer selects "Skip (proceed without a key)":**
Proceed to Step 0 without a partner key.

> **Only after both questions are answered** should you continue to [Step 0](#step-0-detect-project-setup) and begin reading reference files or generating code.

---

## Reference files

Load a reference only when implementing that feature — do not read all upfront.

| File | Read it when… |
|---|---|
| [`signup-steps-schema.json`](signup-steps-schema.json) | **building or verifying ANY form (all 3 integrations)** — the authoritative, machine-readable source for every field's widget `type` (`select`/`radio`/`checkbox-group`/`text`/etc.), option labels (`staticDropdowns`), dynamic dropdown endpoints, and per-country validation (`countryVariants`). **Never infer a widget type or a hardcoded field's option labels from field name or from a markdown table — always resolve them from this file.** |
| [`references/field-catalog.md`](references/field-catalog.md) | building **Integration 2 or 3** — complete field list, types, constraints, and which fields trigger auto-submit. **Not applicable to Integration 1** — its country/industry value formats differ; use `mode-1-fullform.md` and the schema above instead. |
| [`references/mode-1-fullform.md`](references/mode-1-fullform.md) | implementing Integration 1 — all 6-step API contracts, field rules, UUID lifecycle, conditional logic. This file documents API payload/value rules only — it does **not** tell you which HTML widget to render or which validation is per-country; get that from `signup-steps-schema.json`. |
| [`references/mode-2-redirect.md`](references/mode-2-redirect.md) | implementing Integration 2 — URL construction, auto-submit logic, partner attribution, UTM pass-through |
| [`references/mode-3-api.md`](references/mode-3-api.md) | implementing Integration 3 — email-based signup API contract, request/response shapes, resume link, error handling |
| [`references/api-errors.md`](references/api-errors.md) | handling errors — all HTTP status codes, response shapes, and recommended developer actions |
| [`references/security-checklist.md`](references/security-checklist.md) | before going live — all security requirements that must pass |
| [`references/dropdown-fallbacks.json`](references/dropdown-fallbacks.json) | implementing a dropdown-proxy route — static snapshot of every EMAP `/api/partner/*` dropdown response, served when the live call fails or returns no usable data |

---

## Step 0: Detect project setup

Before generating any code, answer these questions:

1. **Does the project have a server-side backend?**
   - Yes (Node/Express, PHP, Python, Next.js, etc.) → All three integrations are available.
   - No (static site, client-side only) → **Only Integration 2** is available. Integrations 1
     and 3 require a backend to hold the partner key server-side. If the developer wants
     Integration 1 or 3 on a static site, offer to scaffold a serverless function
     (Vercel, Netlify, Cloudflare Workers).

2. **What framework or language is in use?**
   - Use the matching template from `templates/integration-1/`, `templates/integration-2/`, or `templates/integration-3/`.
   - If no matching template exists, generate code following the pattern in `node-express.js`.

---

## Step 0.5: Install the verify gate hook

> **STOP. Do not write, edit, or generate a single form/backend file — in a brand-new project or
> an existing one you're continuing — until all 3 steps below are done.** This applies even if
> `merchant-signup/`, templates, or other build output already exist in this project from an
> earlier session: existing code does not mean the hook was ever installed. Check for
> `.claude/hooks/emap-verify-gate.py` first; if it's missing, treat this project as never having
> done Step 0.5, regardless of what else is already built.
>
> This wires up an automated Stop-hook so a build cannot be silently declared "done" after only
> manual curl/browser testing — it forces the [Verify loop](#verify-loop-schema-conformance) to
> actually run and pass before the session can end.

1. **Copy the hook script.** Create `.claude/hooks/emap-verify-gate.py` in the target project
   with the exact contents of [`hooks/emap-verify-gate.py`](hooks/emap-verify-gate.py) from this
   skill. Make it executable (`chmod +x .claude/hooks/emap-verify-gate.py`).

2. **Register the hook.** Read [`hooks/settings.snippet.json`](hooks/settings.snippet.json) and
   merge its `hooks` key into the target project's `.claude/settings.json`:
   - If `.claude/settings.json` doesn't exist, create it with just that `hooks` key.
   - If it exists but has no `hooks.Stop`, add the `hooks.Stop` array from the snippet.
   - If `hooks.Stop` already has entries, **append** the snippet's single entry to the existing
     array — never overwrite another hook that's already registered there.

3. **Mark the build in progress.** As soon as you start generating code for a chosen integration
   mode, write `.claude/emap-build-state.json`:
   ```json
   { "status": "in_progress", "integration": "1" }
   ```
   (use `"2"` or `"3"` to match the mode being built). This is what activates the gate — from this
   point on, the session cannot Stop until the file is updated to `"status": "verified"` by a
   passing run of the [Verify loop](#verify-loop-schema-conformance).

**Verify before proceeding:** confirm `.claude/hooks/emap-verify-gate.py` exists, is executable,
and `.claude/settings.json` actually contains the `Stop` hook entry — don't just assume the writes
succeeded. Only after all 3 files are confirmed on disk should you continue to
[Step 1](#step-1-partner-attribution-optional) or begin generating code.

If the target project cannot run Python 3 (rare), tell the developer the automated gate can't be
installed and that they must run the Verify loop manually before accepting the build — do not
skip Step 0.5 silently.

---

## Step 1: Partner attribution (optional)

Partner attribution links the merchant signup to the partner's account in EMAP.
It is optional — signups work without it, but the partner will not get credit.

- **Integration 2 (redirect):** Pass `secretKey={partner_key}` as a URL query parameter.
  The value is the partner's `security_key` from their EMAP account.
  Store it in the backend environment as `EMAP_PARTNER_SECRET_KEY` and append it server-side.
  Never hardcode it in client-side JavaScript or commit it to source control.

- **Integration 3 (API):** Pass `partner_key` in the JSON request body from your backend.
  Store it as `EMAP_PARTNER_KEY` in your environment. **Never send it to the browser or log it.**

If the developer does not yet have a partner key, refer them back to the instructions in
[Before you start — Required questions](#before-you-start--required-questions).
Integration works without a key; signups will simply not be attributed.

---

## Step 2: Choose integration mode

| | Integration 1 — Full form | Integration 2 — Redirect handoff | Integration 3 — Email-based signup |
|---|---|---|---|
| **How it works** | Partner hosts all 6 steps; backend proxies each step to EMAP API | Partner hosts a single-step form (same fields as Int-1 Step 1); on submit, all fields are appended as URL params and browser redirects to EMAP `/signup?params` | Partner hosts a single-step form; backend POSTs step-1 fields to EMAP REST API; EMAP emails the merchant a secure link to complete their application |
| **Where merchant continues** | Partner's site — all 6 steps | EMAP, from step 2 onward (immediately after redirect) | EMAP, from step 2 onward (after clicking email link) |
| **Backend required?** | Yes — proxies all 6 EMAP API calls | No — redirect is client-side | Yes — `partner_key` must stay server-side |
| **Auto-submit on EMAP?** | N/A — merchant never visits EMAP | Yes, when all non-excluded step-1 fields are provided | N/A — EMAP processes the record server-to-server |
| **Best for** | Full branding control across all 6 steps, enterprise integrations | Simple embed, static sites, fastest integration | Clean partner-side UX for step 1; merchant completes the rest on EMAP after clicking their email link |

Ask the developer which mode they want, or recommend based on their setup from Step 0.

---

## Build Integration 1: Full form

**Before writing any file below:** check that `.claude/hooks/emap-verify-gate.py` exists in this
project. If it doesn't — even if `merchant-signup/` or other build output already exists here —
go do [Step 0.5](#step-05-install-the-verify-gate-hook) first.

Read [`references/mode-1-fullform.md`](references/mode-1-fullform.md) before proceeding.

### Steps

1. **Use the template** from `templates/integration-1/`:
   - `node-express.js` — backend that proxies all 6 steps and serves dropdown data.
   - `plain-html.html` — complete 6-step form. Works with the Express backend above.
   - If the project uses a different stack, **port the template 1:1** — same field list, same widget
     type per field, same validation, same conditional logic, same backend routes — rather than
     regenerating the form from the prose reference alone. Use `signup-steps-schema.json` as the
     field-by-field spec while porting.

2. **Configure environment variables:**
   ```
   EMAP_BASE_URL=https://emap.epd.dev
   EMAP_PARTNER_KEY=your_key_here   # optional; enables partner attribution
   PORT=3000
   ```

3. **Implement all 6 dropdown-proxy backend routes** (required even on a different stack — a missing
   or misconfigured route is the most common cause of a dropdown rendering with no options):
   ```
   GET /api/countries          → proxies EMAP GET /api/partner/countries
   GET /api/states             → proxies EMAP GET /api/partner/states
   GET /api/industry-types     → proxies EMAP GET /api/partner/industry-types
   GET /api/shopping-carts     → proxies EMAP GET /api/partner/shopping-carts
   GET /api/referral-sources   → proxies EMAP GET /api/partner/referral-sources
   GET /api/interest-details   → proxies EMAP GET /api/partner/interest-details
   ```
   Follow the `dropdownProxy()` pattern in `node-express.js` (same-origin proxy, cache 1 hour, no auth).
   Verify each route actually returns populated `data` before wiring the frontend `<select>` to it.
   **Each route must fall back to the static snapshot in [`references/dropdown-fallbacks.json`](references/dropdown-fallbacks.json)
   when the live EMAP call errors, times out, or returns an empty/missing `data` array** — the
   `node-express.js` template already does this (inlined as `DROPDOWN_FALLBACKS`); port that
   fallback logic along with the rest of the proxy if you're generating a different stack. This is
   what stops a dropdown from silently rendering with zero options when EMAP's dropdown API is
   briefly down or slow.

4. **Understand the step flow:**
   - Step 1 (`POST /api/v1/signup`) returns a `uuid`. Collect: first name, last name, email, phone, company name, website, country, annual sales, **industry type**, and (if US) business state. Store the `uuid` in `localStorage('emap_uuid')`.
   - Steps 2, 3, 5, 6 call `POST /api/v1/application/step` with the `uuid` and the appropriate `step_count`.
   - Step 4 calls `POST /api/v1/ownership` (no `step_count`; uses dot-notation field names).
   - Step 6 success → clear `localStorage` and show a completion panel.

5. **Pre-fill Step 2 from Step 1 data:**
   When Step 1 succeeds and the form advances to Step 2, automatically populate:
   - `legal_name` ← value of `company_name` from Step 1
   - `name` (DBA / "doing business as") ← value of `company_name` from Step 1
   The merchant can edit these fields in Step 2 if the legal name differs from the trading name.
   Only pre-fill when the fields are currently empty (do not overwrite if the merchant has already typed something or if the session was restored from localStorage).

6. **No back-navigation between steps:**
   Once a merchant submits a step successfully, they **cannot** return to a previous step.
   - Do **not** render Back buttons on any step (steps 2–6).
   - Do **not** call `goToStep(n)` with a lower step number from any UI action.
   This is intentional — each step is persisted to EMAP's API on submit, and EMAP does not
   support replaying an earlier step after it has been accepted.

7. **Handle conditional fields:**
   - `industry_type` is collected in **Step 1** (not Step 2) and submitted with `POST /api/v1/signup`. Show `industry_type_other` when `industry_type = other` (step 1).
   - `country=US` → show `business_state` (step 1) and `state.1` (step 4).
   - `business_organized` is not `Sole-Proprietorship` and `emap_country` (Step 1) ≠ `CA` → show `federal_tax_id` (step 2).
   - `emap_country` (Step 1) ≠ `US` → show `business_register_number` (step 2).
   - `is_physical_address_same_as_legal_address=0` → show the physical address block (step 2).
   - `marketingModel` includes `2` → show `subscription_frequency`; if frequency=`3` show `subscription_frequency_other` (step 2).
   - `fulfillment_by` is `Vendor` or `Others` → show `fullfillment_company` (double-l, step 3).
   - `primary_contact=0` → show `first_name.1`, `last_name.1`, `email.1`, `primary_contact_job_title` (step 4).
   - `ownership_percentage.1 < 51` → show Owner 2 section (step 4).
   - `country.1=US` → show `driver_license_state.1` and `driver_license_expiration_date.1` (step 4).
   - `emap_country` (Step 1) = `CA` → show `institution_number` + `customer_pay_currency` (step 5).
   - `bad_experience=true` → show `bad_experience_happened` (step 6).

8. **Widget type — never guess, always resolve from the schema.** These fields are hardcoded
   value sets, not dynamic dropdown data, and have repeatedly been generated as a `<select>` of
   raw values by mistake. Check `signup-steps-schema.json` for each one's `type` before rendering:
   - `marketingModel` → **checkbox-group** (`staticDropdowns.marketing_model`), not a select. Render
     the `label` text (e.g. "Recurring/Continuity/Subscription"), send the integer `value`.
   - `is_physical_address_same_as_legal_address`, `primary_contact`, `bankruptcy_filed.1/.2`,
     `bankruptcy_discharged.1/.2`, `current_processing`, `bad_experience`,
     `multiple_merchant_accounts`, `leave_deposit` → **radio buttons** (Yes/No), not a select.
   - `terms_and_conditions_agreed` → **checkbox**, not a select.
   - Fields backed by `optionsSource: dynamicDropdownEndpoints.*` (`country`, `industry_type`,
     `shopping_cart`, `howdidyouhear`, etc.) are correctly rendered as `<select>`.

9. **Per-country field validation — must be enforced, not just displayed as a hint.** Read
   `countryVariants` in `signup-steps-schema.json` for these fields and wire the matching
   `maxLength`/`minLength`/`pattern` into both the input's HTML attributes AND a submit-time JS
   check (the same way the SSN mask below is enforced) — a label or placeholder that *says*
   "9 digits" does nothing on its own:
   - `routing_number` — US: exactly 9 digits (`^[0-9]{9}$`).
   - `account_number` — US: 8–17 characters.
   - `federal_tax_id`, `institution_number` — see their `countryVariants`/`pattern` in the schema.

10. **Card percentage (step 3):** `card_swiped + customer_entered + staff_entered` must equal 100.
    Validate client-side and block submission if not.

11. **SSN (step 4):** For US/CA owners, apply Cleave.js mask `blocks:[3,2,4] delimiters:["-","-"]`
    to format as `XXX-XX-XXXX`. Validate: `ssn.replace(/-/g,'').length >= 9`.
    For other countries, show a plain text field labelled "Personal Tax ID / Government ID Number".

12. **DOB (step 4):** Owner must be between 18 and 100 years old.
    `maxDate = today − 18 years`, `minDate = today − 100 years`.
    Enforce this **both client-side** (date input `min`/`max` attributes plus a submit-time check)
    **and server-side** (recompute the owner's age from the submitted date in your `/api/step/4`
    handler before proxying to EMAP) — a client-only check can be bypassed by calling your backend
    directly.

13. **Handle all response shapes** on each step (see [`references/api-errors.md`](references/api-errors.md)):
    - `{"status":true}` → advance to next step.
    - HTTP 422 → display per-field errors.
    - HTTP 429 → ask the merchant to wait and retry.
    - HTTP 5xx → show generic "please try again".

14. **Test:**
    - Complete all 6 steps with test data against the EMAP staging URL.
    - Verify Step 6 shows the success panel and `localStorage` is cleared.
    - Verify `legal_name` and `name` (DBA) are pre-filled with the company name when Step 2 loads.
    - Confirm no Back buttons appear on any step.
    - Test card percentage validator and Owner 2 conditional display.
    - Test SSN Cleave.js mask and DOB age gate — confirm both the browser form AND a direct
      `POST /api/step/4` call with an underage/over-100 DOB are rejected with a 422.
    - Confirm all dropdown-backed selects (`country`, `state`, `industry_type`, `shopping_cart`,
      `howdidyouhear`) actually populate with options at runtime.
    - Simulate an EMAP dropdown-API outage (point `EMAP_BASE_URL` at an unreachable host) and
      confirm each dropdown still populates from `references/dropdown-fallbacks.json` instead of
      rendering empty.
    - Confirm `marketingModel` renders as labeled checkboxes and
      `is_physical_address_same_as_legal_address` as labeled radios — not raw-value selects.
    - Confirm `routing_number` rejects a US value that isn't exactly 9 digits, and `account_number`
      rejects a US value outside 8–17 characters.
    - **Run the [Verify loop: schema conformance](#verify-loop-schema-conformance)** and then
      [Verify: security and coverage](#verify-security-and-coverage) before telling the developer
      the form is done. Manual curl/browser testing above does not substitute for either — the
      verify gate hook (Step 0.5) will block the session from ending until the loop has completed
      with zero `CONFIRMED` findings.

---

## Build Integration 2: Redirect handoff

**Before writing any file below:** check that `.claude/hooks/emap-verify-gate.py` exists in this
project. If it doesn't — even if `merchant-signup/` or other build output already exists here —
go do [Step 0.5](#step-05-install-the-verify-gate-hook) first.

Read [`references/mode-2-redirect.md`](references/mode-2-redirect.md) before proceeding.

### Overview

Integration 2 is a **single-step form** — it collects exactly the same fields as Integration 1
Step 1 (basic merchant info). There is **no Terms and Conditions checkbox**. On submit, all form
fields are serialized as URL query parameters and the browser redirects to
`{EMAP_BASE_URL}/signup?{params}`. EMAP reads the params, prefills its form, and either shows
the form to the merchant or auto-submits it (if all auto-submit fields are present), landing the
merchant directly on step 2.

### Fields collected (same as Integration 1 Step 1)

| Field | Type | Notes |
|---|---|---|
| `first_name` | text | Required |
| `last_name` | text | Required |
| `email` | email | Required |
| `phone` | tel | Required |
| `company_name` | text | Required |
| `website` | url | Required |
| `country` | select | Required — pass **full country name** (e.g. `United States`), not a 2-char code |
| `business_state` | select | Required only when `country = United States` |
| `annual_sales` | number | Required |
| `industry_type` | select | Required — loaded from EMAP API (`/api/partner/industry-types`), use `name` as value |
| `industry_type_other` | text | Conditional — shown when `industry_type = Other` |
| `promo_code` | text | Optional |

**No T&C checkbox.** Do not add one — the merchant agrees to terms on EMAP after step 6.

### Steps

1. **Use the template** from `templates/integration-2/` matching the project stack.
   - No backend: use `plain-html.html` — client-side form that builds and follows the redirect URL.
   - Has backend: use `node-express.js` — server builds the URL and returns it to the client,
     keeping `EMAP_PARTNER_SECRET_KEY` out of the browser.

2. **On submit — build redirect URL:**
   ```javascript
   const params = new URLSearchParams();
   params.set('first_name', formData.get('first_name'));
   params.set('last_name',  formData.get('last_name'));
   params.set('email',      formData.get('email'));
   params.set('phone',      formData.get('phone'));
   params.set('company_name', formData.get('company_name'));
   params.set('website',    formData.get('website'));
   params.set('country',    formData.get('country'));       // full name
   if (formData.get('business_state')) params.set('business_state', formData.get('business_state'));
   params.set('annual_sales', formData.get('annual_sales'));
   params.set('industry_type', formData.get('industry_type'));
   if (formData.get('promo_code'))    params.set('promo_code', formData.get('promo_code'));
   // UTM pass-through (see step 3)
   window.location.href = EMAP_BASE_URL + '/signup?' + params.toString();
   ```

3. **Pass UTM params through.** Read `utm_campaign`, `utm_source`, `utm_medium`, `utm_term`,
   `utm_content`, `gclid`, `gbraid`, `wbraid` from the current page URL and append them to the
   redirect URL. The templates do this automatically.

4. **Configure environment variables:**
   ```
   EMAP_BASE_URL=https://emap.epd.dev
   EMAP_PARTNER_SECRET_KEY=your_key_here   # optional; enables partner attribution
   ```

5. **Set `Referrer-Policy: no-referrer`** on your form page. This prevents the EMAP URL
   (which contains PII in the query string) from leaking into the `Referer` header sent to
   third-party analytics on the EMAP page.

6. **Test:**
   - Partial prefill: pass `first_name`, `last_name`, `company_name`, `phone`, `email` only.
     EMAP shows the form prefilled; the merchant fills in the rest manually.
   - Full prefill (auto-submit): pass all non-excluded fields. EMAP auto-submits; merchant
     lands on step 2. See [`references/mode-2-redirect.md`](references/mode-2-redirect.md).
   - **Run the [Verify loop: schema conformance](#verify-loop-schema-conformance)** and then
     [Verify: security and coverage](#verify-security-and-coverage) before telling the developer
     the form is done. Manual testing above does not substitute for either — the verify gate hook
     (Step 0.5) will block the session from ending until the loop has completed with zero
     `CONFIRMED` findings.

---

## Build Integration 3: Email-based signup

**Before writing any file below:** check that `.claude/hooks/emap-verify-gate.py` exists in this
project. If it doesn't — even if `merchant-signup/` or other build output already exists here —
go do [Step 0.5](#step-05-install-the-verify-gate-hook) first.

Read [`references/mode-3-api.md`](references/mode-3-api.md) before proceeding.

### Steps

1. **Create the form.** Use the field list in [`references/field-catalog.md`](references/field-catalog.md)
   (Integration 3 columns). Note: the API uses `name` for company name, not `company_name`.

2. **Create a backend endpoint** (e.g. `POST /api/signup`) that:
   - Receives and validates the form data server-side.
   - Reads `EMAP_PARTNER_KEY` and `EMAP_BASE_URL` from the environment.
   - Calls `POST {EMAP_BASE_URL}/api/v1/signup` with the validated data plus `partner_key` and
     `trigger_email: true`. This flag tells EMAP to dispatch the welcome/verification email as
     part of this same call — without it, the account is created but no email is sent.
   - Returns the EMAP response (or a mapped version) to the browser.
   Use the matching template from `templates/integration-3/`.

3. **Configure environment variables:**
   ```
   EMAP_BASE_URL=https://emap.epd.dev
   EMAP_PARTNER_KEY=your_key_here   # never commit this
   ```

4. **Handle all response shapes** on the client side (see
   [`references/api-errors.md`](references/api-errors.md) for the full table):
   - `{"status":true,"uuid":"..."}` → show "Application submitted! Check your inbox."
   - `{"verificationLink":true,"url":"..."}` → existing user; show message or redirect to `url`.
   - `{"status":false,"message":"Company already exists"}` → tell merchant to check their email.
   - HTTP 422 → display per-field errors from `response.errors`.
   - HTTP 429 → tell merchant to wait and retry.

5. **Test** by submitting with a unique email. Verify `{"status":true,"uuid":"..."}` is returned
   and the welcome email arrives.
   - **Run the [Verify loop: schema conformance](#verify-loop-schema-conformance)** and then
     [Verify: security and coverage](#verify-security-and-coverage) before telling the developer
     the form is done. Manual testing above does not substitute for either — the verify gate hook
     (Step 0.5) will block the session from ending until the loop has completed with zero
     `CONFIRMED` findings.

---

## Integration 3: Resume link

This is for **resending** the email only — the initial email is triggered by `trigger_email: true`
on the `/api/v1/signup` call itself (see step 2 above). Use
`POST {EMAP_BASE_URL}/api/v1/signup/resume-link` to re-email the merchant a link to continue
their application, e.g. if the first email never arrived. The merchant receives a "Finish Later"
email with a direct link to their in-progress application on EMAP.

**Request (from your backend, not the browser):**
```
POST /api/v1/signup/resume-link
Content-Type: application/json

{ "email": "merchant@example.com" }
```

**Response:** Always `{"status":true,"message":"Resume link sent"}` regardless of whether
the email address exists — this prevents account enumeration.

**Rate limit:** 5 requests per 5 minutes per IP on your backend's outbound call.

**When to call it:**
- The merchant says "I didn't get the email" and requests it again.
- You want to add a "Resend link" button to your confirmation page.

Always proxy this through your backend — never call EMAP directly from the browser.

---

## Verify loop: schema conformance

> **Definition of done.** A build is not done until this loop has completed with zero `CONFIRMED`
> findings. Your final response to the developer must include the verify agent's raw findings
> JSON from the last round (or explicitly state it returned `[]`) — not a paraphrase, not a
> summary of manual testing you did instead. If Step 0.5's hook is installed, the session cannot
> Stop until `.claude/emap-build-state.json` says `"status": "verified"` (see step 6 below) —
> treat that as the actual finish line for the build, not your own judgment that it "looks done."

Do this for **every** integration mode, after the form and backend are written and before you tell
the developer the build is done. Its purpose is to catch the exact class of bug this skill has
shipped before: a rule that exists in `signup-steps-schema.json` (or `field-catalog.md` for Int 2/3)
but wasn't actually wired into the generated code — a `<select>` used where a checkbox-group was
required, a country-specific length limit shown as a hint but not enforced, a dropdown wired to a
proxy route that doesn't return data, etc. Do not rely on having "read the schema earlier" — the
generated code is the thing being graded, not your memory of the instructions.

**Roles** — three, not two. A single verify agent's own findings are not trustworthy enough to act
on directly (it can hallucinate a mismatch or misread the schema); they must be independently
confirmed before the build agent spends a fix cycle on them.

1. **Build agent** — you. Writes the code, applies fixes. Never grades its own output.
2. **Verify agent** (fresh `general-purpose` agent per round) — reads the schema/reference docs and
   the generated files, proposes findings. Proposes only — does not decide what's real.
3. **Confirm agent** (fresh `general-purpose` agent **per individual finding**, spawned in parallel)
   — independently re-derives the same finding from the primary source (the exact schema field and
   the exact file/line cited) without trusting the verify agent's description of it, and returns a
   verdict. Only `CONFIRMED` findings ever reach the build agent.

**Findings contract.** The verify agent must return a JSON array — not prose — each item shaped as:
```json
{
  "file": "relative/path/to/file",
  "field": "schema field key, or 'route:/api/countries', or 'storage:emap_uuid'",
  "category": "widget_type | hardcoded_label | country_validation | conditional_logic | dropdown_route | other",
  "expected": "what signup-steps-schema.json / field-catalog.md says",
  "actual": "what the generated code actually does, with a line reference",
  "severity": "blocker | minor"
}
```
An empty array (`[]`) is a valid, expected result — do not treat "I found nothing" as a failure to
justify by inventing an item.

**Loop:**

1. **Build agent** finishes the form + backend for the chosen integration mode.
2. **Build agent** spawns a **verify agent** with this brief: *"Read `signup-steps-schema.json`
   (and, for Integration 2/3, `references/field-catalog.md`). Read the generated form/backend files
   at `<paths>`. For every field in scope, check: (a) the rendered widget type matches the schema's
   `type` (select vs. radio vs. checkbox-group vs. checkbox vs. text) — do not accept a `<select>`
   for a field whose schema entry is `radio` or `checkbox-group`; (b) hardcoded-option fields
   (`staticDropdowns`) render the human-readable `label`, not the raw `value`/`slug`; (c) every
   `countryVariants` constraint (`pattern`/`exactLength`/`minLength`/`maxLength`) is enforced by
   actual validation code (HTML attribute AND/OR a submit-time check), not only shown as label/hint
   text; (d) every `dependsOn`/`visibleIf` conditional is implemented and the shown/hidden field is
   also required/optional to match; (e) all 6 dropdown-proxy routes exist, return non-empty data for
   a live test country, AND fall back to `references/dropdown-fallbacks.json` (not an empty array)
   when the live EMAP call is made to fail/timeout. Return findings strictly as the JSON array
   defined in the Findings contract above — no prose, no markdown. Return `[]` if none exist — do
   not invent findings to justify the pass."*
3. **Verify agent** returns its findings array. **If the array is empty, skip straight to step 6**
   (there is nothing to confirm).
4. **Build agent spawns one confirm agent per finding, in parallel**, with this brief per finding:
   *"A verify agent claims: `<the single finding JSON>`. Do not trust this description. Independently
   open `<file>` at the cited location and independently look up `<field>` in
   `signup-steps-schema.json` (or `field-catalog.md`) yourself. Decide from the primary sources only:
   is this finding real? Return `{finding, verdict: "CONFIRMED" | "REJECTED", reason}`."*
5. **Build agent keeps only `CONFIRMED` findings**, discards `REJECTED` ones (a rejected finding is
   not reported to the developer and is not a reason to loop again).
6. **If there are zero `CONFIRMED` findings** → conformance passed. If Step 0.5's hook is
   installed, write `.claude/emap-build-state.json`:
   ```json
   { "status": "verified", "integration": "1", "rounds": 1, "confirmed_findings": [] }
   ```
   (match `integration` and `rounds` to what actually happened). Then proceed to
   [Verify: security and coverage](#verify-security-and-coverage), then hand off to the developer.
7. **If there is at least one `CONFIRMED` finding** → the build agent fixes every one of them
   directly in the code (do not just re-read the docs and re-explain the rule — change the file),
   then returns to step 2 with a **fresh** verify agent for a full re-check (do not reuse the prior
   verify agent instance, and do not skip re-verification of fields that already passed — a fix can
   regress an unrelated field).
8. **Cap at 5 verify→confirm→fix rounds.** If `CONFIRMED` findings remain after 5 rounds, stop
   looping, report exactly those remaining `CONFIRMED` findings to the developer, and do not claim
   the build is done. If Step 0.5's hook is installed, write `.claude/emap-build-state.json` with
   `"status": "blocked"` (not `"verified"`) plus the remaining findings, so the gate reflects that
   the loop ran to its cap rather than was skipped:
   ```json
   { "status": "blocked", "integration": "1", "rounds": 5, "confirmed_findings": [ /* ... */ ] }
   ```

---

## Verify: security and coverage

Before going live, run through [`references/security-checklist.md`](references/security-checklist.md).

Quick self-check:
- [ ] HTTPS on your site — form page and backend endpoint.
- [ ] Partner key in env only — not in client-side code, not in the form HTML, not in git.
- [ ] `Referrer-Policy: no-referrer` on the form page (critical for Integration 2).
- [ ] Backend validation before forwarding to EMAP.
- [ ] Submit button disabled on first click (double-submit prevention).
- [ ] Generic user-facing errors — do not expose EMAP's raw error messages.

---

## Guardrails

**Never print, log, commit, or send to the browser the partner key (`EMAP_PARTNER_KEY` / `EMAP_PARTNER_SECRET_KEY`).**
**Never call EMAP's API (`/api/v1/signup`) directly from browser-side JavaScript — always go through your backend.**
**Never store PII (name, email, phone) in your database after forwarding to EMAP — EMAP is the system of record.**
**Never add document upload fields — EMAP collects documents in its own UI after step 6.**
**Do not modify field validation rules — EMAP will reject submissions that don't pass its server-side rules.**
