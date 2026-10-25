---
name: meta-ads
description: "Launch and verify Meta (Facebook/Instagram) ad campaigns end to end — the Business Manager permission chain, programmatic campaign creation via the Marketing API, the steps that only exist in the browser UI, crop-safe creative, and pixel/Conversions API tracking that is actually proven to work. Use when setting up Meta API access, creating or debugging campaigns, or verifying Meta conversion tracking."
---

# Meta Ads — setup, launch, verification

Everything here was learned by getting it wrong in production first. The API
rejections are real rejections, the permission chain is the one that actually
unblocks, and the verification section exists because measuring the wrong thing
produced three confidently-wrong conclusions in a single session.

**Route by task:**

| Task | Read |
|---|---|
| Getting API access at all | §1, then `reference/setup.md` |
| Creating campaigns in code | §3, then `reference/publishing.md` |
| Steps the API cannot do | §4, then `reference/browser.md` |
| Pixel / CAPI / "is it tracking?" | §2 and §5, then `reference/tracking.md` |
| Making the images | §6, then `reference/creative.md` |

---

## 1. The permission chain (where most people get stuck)

To create ads via the API you need **four separate grants**. Missing any one
produces a different, unhelpful error that names none of the others.

1. **A Meta app.** If the business already has one, use it — a second app means
   a second review and a second publishing step.
2. **The system user has a ROLE ON THE APP.** Business Settings → Apps → *app* →
   Add People → pick the system user → **Develop app**.
   Without this, token generation fails with *"No permissions available"* and
   gives no hint which of the four grants is missing. This is the step people
   skip.
3. **The system user has the ASSETS.** Business Settings → System Users →
   *user* → Assign assets:
   - Ad account → **Manage campaigns** (not "Manage ad account", which is
     finances and permissions)
   - Page → **Ads**
   - Pixel / dataset → **Use events dataset**
4. **Generate the token.** System Users → Generate token → select the app →
   **Never** expiry → tick `ads_management`.

**Prefer a system user over a personal user token.** A personal token dies when
the person's password changes or their session is invalidated; a system-user
token belongs to the business and survives staff turnover.

**Prefer Never expiry.** A time-boxed token lapses silently and takes the
integration with it — usually discovered days later as "why did spend stop".

Two more grants only surface at ad-creation time, long after the token works:

- **Instagram account connected to the ad account.** Advantage+ placements
  include Instagram, so creation fails with *"Ad account has no access to this
  Instagram account"*. Fix in Business Settings → Instagram accounts →
  *account* → Connect assets → the ad account.
- **The app must be Live, not Development.** *"Ads creative post was created by
  an app that is in development mode"*. Publishing needs a Privacy Policy URL
  and a Category. Development mode blocks **creative creation only** — every
  other call works, so this fails late, after you have already created a
  campaign and ad set.

Run `scripts/preflight.mjs` before anything else. It checks all of the above
and writes nothing.

---

## 2. Verification traps — read before believing any test result

Three separate false negatives in one launch. Each looked like a real bug. Each
was the instrument, not the system.

| Trap | What happened | Use instead |
|---|---|---|
| **Testing on localhost** | Pixel and embed verified on `localhost`. Both were blocked in production by a CSP that localhost does not send. | Always verify against the **deployed** URL. A localhost pass proves nothing about production headers. |
| **`performance.getEntriesByType('resource')`** | Concluded "the Lead never fires" because no request appeared. `fbevents` uses `navigator.sendBeacon` when an `eventID` is present, and **sendBeacon never appears in resource timing**. | Meta's **Test Events** tool. It is Meta's own instrumentation and it ends the argument. |
| **"Received From: Browser" in Test Events** | Concluded server-side CAPI was broken because no server rows appeared. **Test Events only shows server events when the server sends a `test_event_code`.** | Have the server return its own send result (§5). Absence of display ≠ absence of delivery. |

The pattern: **absence of evidence read as evidence of absence, from an
instrument that structurally could not observe the thing being measured.**
Before concluding something is broken, ask what the instrument can actually see.

**Change one thing at a time.** One "isolation test" removed two variables at
once and the wrong one got the blame, costing an hour.

---

## 3. Creating campaigns — the rejections, in order

Each of these is a real 400 that stops creation. Set them up front.

```js
// CAMPAIGN
{
  objective: 'OUTCOME_LEADS',
  status: 'PAUSED',
  special_ad_categories: [],               // or ['EMPLOYMENT'|'HOUSING'|'CREDIT'|...]
  buying_type: 'AUCTION',
  is_adset_budget_sharing_enabled: false,  // REQUIRED when budget is on the ad set
}

// AD SET
{
  daily_budget: 3000,                       // CENTS. 3000 = $30.00
  billing_event: 'IMPRESSIONS',
  bid_strategy: 'LOWEST_COST_WITHOUT_CAP',  // required; a cap throttles a cold pixel
  optimization_goal: 'OFFSITE_CONVERSIONS',
  promoted_object: { pixel_id, custom_event_type: 'LEAD' },
  targeting: {
    geo_locations: { custom_locations: [{ latitude, longitude, radius: 25, distance_unit: 'mile' }] },
    age_min: 18, age_max: 65, genders: [1, 2],
  },
}
```

| Error | Cause |
|---|---|
| `must specify True or False in is_adset_budget_sharing_enabled` | budget on the ad set, flag absent |
| `Bid amount or bid constraints required` | no explicit `bid_strategy` |
| `daily budget must be greater than $0` | budget arrived as `null` — see below |
| `Ad account has no access to this Instagram account` | IG not connected to the ad account |
| `created by an app that is in development mode` | app not published |
| `standard_enhancements has been deprecated` | drop the field, set it in the UI (§4) |

**The `null` budget was a caller bug worth remembering.**
`argv[argv.indexOf('--flag') + 1]` returns `argv[0]` when the flag is absent,
because `indexOf` returns `-1`. `Number('--apply')` is `NaN`, which
`JSON.stringify` turns into `null`, which Meta reports as a zero budget. Check
the flag is present *and* range-check the value before sending.

**Always create PAUSED**, verify in the UI, then enable deliberately. An agent
that creates ACTIVE ads spends real money on unreviewed creative.

**Clean up orphans.** A failed run leaves a campaign or ad set behind. Delete it
before retrying, or duplicates accumulate and delivery splits across them.

`scripts/campaign.mjs` implements all of this from a JSON config.

---

## 4. What only the browser can do

Some required steps have no API. An agent driving Meta needs the browser for:

| Step | Where |
|---|---|
| Create the system user, assign app role and assets, generate the token | Business Settings |
| Publish the app (Development → Live) | App Dashboard → Settings → Basic |
| Connect Instagram to the ad account | Business Settings → Instagram accounts |
| **Opt out of Advantage+ creative enhancements** | Ads Manager → ad → Creative |
| **Check ad previews per placement** | Ads Manager → ad → Preview |
| Test Events | Events Manager |
| Disable automatic event detection | Events Manager → pixel → Settings |
| Add a payment method | Billing |

Two of these are load-bearing and routinely skipped:

**Advantage+ creative enhancements auto-crop images and overlay text.** The API
field `standard_enhancements` is deprecated and its per-feature replacement is a
moving target, so set it in the UI. Confirm via API by reading
`degrees_of_freedom_spec` on the creative — you want
`advantage_plus_creative: OPT_OUT`.

**Ad previews render each placement for real.** This is what catches creative
that survives a full-size render and dies in feed. Look at them before enabling.

See `reference/browser.md` for deep links, agent-driving guidance, and the
things an agent must never do in that UI (credentials, payment details, and
anything that opens a modal dialog).

---

## 5. Conversion tracking that is actually proven

**Both paths, one event id.** The browser pixel and the server Conversions API
send the same `event_id`; Meta collapses them into one conversion. The server
path survives ad blockers — roughly a third of an audience — so it is not
optional.

The browser must forward what the server cannot know:

```js
meta: {
  event_id: evId,                          // same id both sides — this is the dedupe key
  event_source_url: window.location.href,
  fbp: cookie('_fbp'),   // first-party cookies on YOUR domain; a server running
  fbc: cookie('_fbc'),   // anywhere else never receives them otherwise
}
```

**Make the server report its own outcome.** A CAPI call is correctly non-fatal —
losing an attribution event must never fail a form submission — which means it
can rot silently forever. Return the result so one `curl` proves the whole
server path in isolation:

```js
return json({ success: true, id, meta_capi: r.ok ? `sent:${n}` : `failed:${err}` });
```

**Fire events on what you mean.** A `Schedule` fired when a calendar *renders*
means "someone saw a calendar", not "someone booked" — optimizing toward it
trains Meta to find people who arrive and leave. Use the embed's own success
callback and make the render a separate custom event.

**Optimize for volume, measure on truth.** Meta needs roughly 50 conversions per
week per ad set to exit the learning phase. If the true outcome is rarer than
that, bid on the higher-volume upstream event and keep the real one for
reporting.

**Watch for automatic events.** Meta's automatic event detection invents events
(commonly `Subscribe`) from ordinary form interactions, which then pollute
optimization. Disable it in pixel settings.

### CSP will silently break all of it

If the site sends a Content-Security-Policy, these must be allowed or the pixel
dies with no visible error:

```
script-src   https://connect.facebook.net
connect-src  https://www.facebook.com  https://connect.facebook.net
frame-src    https://www.facebook.com
```

A blocked `fbevents.js` leaves `fbq` as the inline stub: it queues events and
sends nothing, forever. The check that detects it:

```js
typeof window.fbq.callMethod === 'function'   // real library loaded
window.fbq.queue.length                        // >0 and growing = stub, blocked
```

`fbq.loaded` and `fbq.version` are set by the **inline stub** and prove nothing.

---

## 6. Creative: the crop-safe zone

**A 1080×1920 asset is cropped for feed placements.** 4:5 removes ~285px from
each end; 1:1 removes ~420px. Anything near the top or bottom is destroyed in
exactly the placement where most impressions land.

**Keep every critical element inside the 1:1 safe band: y 420 → 1500.** Stack
identifier, message and CTA as one block centred in that band so the whole
message survives any crop. Verify by simulating the crops rather than trusting
the full-size render:

```js
for (const h of [1350, 1080]) {
  await sharp(file).extract({ left: 0, top: (1920 - h) / 2, width: 1080, height: h })
    .toFile(`crop_${h}.jpg`);
}
```

Then look at the Ads Manager preview, which renders each placement for real.

**Special Ad Categories** (Employment, Housing, Credit, Social Issues) strip the
targeting you would normally rely on: no age or gender targeting, no detailed
interest or behaviour targeting, and a minimum 15-mile radius. **Consequence:
the creative IS the targeting.** With no interest targeting, the only thing
making the right person recognise themselves is the ad itself — put the audience
identifier in the image as literal words, not a clever hook.

Employment and Credit also forbid earnings claims. Guard it in code, in every
place copy can be edited, and fail loudly:

```js
const MONEY = /\$\s?\d|\b\d+\s?(k|dollars|usd)\b|\bper hour\b|\/hr\b/i;
```

---

## Launch checklist

- [ ] System user has app role, ad account, Page, and pixel
- [ ] App published (not Development mode)
- [ ] Instagram connected to the ad account
- [ ] Token has `ads_management`, Never expiry
- [ ] `scripts/preflight.mjs` passes
- [ ] Copy checked against the category's content rules
- [ ] Creative content inside y 420–1500; crops simulated
- [ ] Advantage+ creative enhancements OPT_OUT
- [ ] Created PAUSED; ad previews checked per placement in Ads Manager
- [ ] `fbq.callMethod` is a function **on the deployed site**
- [ ] Conversion event confirmed **Processed** in Test Events
- [ ] Server CAPI confirmed `sent:N` via its own response
- [ ] Test records deleted from the database afterwards
- [ ] Token rotated if it appeared in any transcript, log, or screenshot
