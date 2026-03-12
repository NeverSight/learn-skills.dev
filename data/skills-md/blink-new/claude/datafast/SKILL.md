---
name: datafast
description: Accelerate adoption of DataFast analytics across any stack by codifying the installation, attribution, event, proxy, and API patterns that drive reliable conversion intelligence
---

## When to Use This Skill

- You need to instrument a website (static, SPA, Next.js, Astro, etc.) with DataFast tracking.
- Revenue needs to be attributed to marketing channels (Stripe, LemonSqueezy, Polar, custom providers).
- You want to record custom events/goals reliably despite ad blockers.
- You must proxy the tracker/script for increased data quality or hashed navigation.
- You want to export/import historical analytics or query DataFast APIs.

## Quickstart (4 steps)

1. **Install the tracking script** inside `<head>`:
   ```html
   <script
     defer
     data-website-id="dfid_XXXX"
     data-domain="example.com"
     src="https://datafa.st/js/script.js"
   ></script>
   ```
   - Customize via `data-allow-localhost`, `data-api-url`, `data-debug`, `data-allowed-hostnames`, `data-disable-console`, `data-allow-file-protocol`.
   - Include the `datafast-queue` snippet to queue calls that happen before the library loads.
2. **Connect payment providers** (Stripe, LemonSqueezy, Polar, Shopify, etc.) from the Revenue tab so DataFast auto-tracks revenue.
3. **Add custom goals/events** with `window.datafast("my_goal")`, `data-fast-goal` attributes, or the server-side Goals API.
4. **Optional proxy** to bypass ad blockers: rewrite `/js/script.js` and `/api/events` to your domain and forward visitor IP with `x-datafast-real-ip`.

## Installation Reference

- Scripts load via `<Script />` components in frameworks (Next.js App Router, React, Vue, Astro, etc.) or declaratively in `public/index.html`.
- For hash-based navigation, use the hash-enabled script `https://datafa.st/js/script.hash.js`.
- Use GTM, Shopify, Webflow, Wix, Podia, Kajabi, Ghost, Bubble, Framer, Astro, React Router, Laravel, Django, FastAPI, Flask, Express, PHP, Nginx, Firebase, Rocket, etc., by dropping the same script into the `<head>` or platform-specific head/custom code sections.

## Revenue Attribution Best Practices

- After the tracking script is live, go to **Website Settings → Revenue** and add each payment provider.
- Always pass `datafast_visitor_id` (and optionally `datafast_session_id`) when creating checkout sessions:
  - **Stripe Checkout / PaymentIntent**: read the cookies from `cookies()` or `request.cookies` and add them to `metadata`.
  - **LemonSqueezy**: include DataFast cookies under `custom`.
  - **Polar**: add cookies to `metadata`.
  - **Paddle / Dodo Payments / Easytool / Custom**: call the Payments API or trigger a `payment` goal with the customer email.
- For gateways where DataFast already pulls revenue (Shopify, Stripe, LemonSqueezy, Polar), keep the tracking snippet installed but omit redundant manual events.
- Document the metadata mapping and ensure downstream jobs read `datafast_visitor_id` for each financial event.

## Custom Events & Goals

### Method 1 – `window.datafast()` (client-side)
- Fire `window?.datafast("goal_name")` on clicks, success pages, or after API responses.
- Record parameters: `window.datafast("checkout", { price: "49", plan: "pro" })`.

### Method 2 – HTML data attributes
- Add `data-fast-goal="goal_name"` to buttons/links.
- Enrich with `data-fast-goal-*` attributes (`data-fast-goal-price="49"` becomes `{ price: "49" }`).

### Method 3 – Server-side Goals API
- POST to `https://datafa.st/api/v1/goals` with `datafast_visitor_id`, `name`, and optional `metadata`.
- Authenticate with `Authorization: Bearer YOUR_API_KEY`.
- Ensure the visitor already had at least one pageview (tracked via the script).

## Funnels, Scrolls, & Filters

- Use `data-fast-scroll` on critical sections (features, pricing, testimonials) to send scroll goals when 50% of the element is visible.
- Combine scroll goals with funnels (`landing page visit → feature scroll → CTA click`) to spot drop-offs.
- Track UTM/ref/via parameters automatically tracked by DataFast; encourage marketing links to include `?ref=`, `?utm_source=`, `?utm_medium=`, `?utm_campaign=`, `?utm_term=`, and `?utm_content`.
- Use filters to slice by country, device, campaign, URL path, or custom goals; hover charts expose filter shortcuts.
- Provide docs for `datafast_ignore` localStorage to exclude internal traffic.

## Proxy & Hosting Guidance

- Proxy requests so the script loads from `/js/script.js` and events post to `/api/events` on your domain.
- Forward the visitor IP with `x-datafast-real-ip` to keep geolocation accurate.
- Next.js rewrites, Express HTTP proxy, Flask/FastAPI routes, PHP scripts, Nginx/Caddy rules, Firebase Functions, and DigitalOcean/Nginx examples are ready-made patterns—adapt whichever matches your stack.
- Allowlist additional domains via `data-allowed-hostnames="app.io,shop.example.com"` and set `data-domain` to the root domain to share cookies across subdomains.
- Use `data-api-url` or `datafast_events` endpoints when custom routing is needed; the tracker auto-detects proxied setups.

## API & Export/Import

- DataFast APIs (Overview, Timeseries, Devices, Pages, Countries, Referrers, Campaigns, Goals, Payments, Visitors, Metadata, Realtime) all require `Authorization: Bearer <API_KEY>`.
- Use the **Payments API** to push revenue from unsupported providers: include `amount`, `currency`, `transaction_id`, and the visitor ID.
- Use the **Goals API** for server-side events (max 10 metadata keys).
- Import Plausible exports into DataFast to keep historical data; reference `Import your Plausible data`.
- Export to dashboards via the API Playground, Real-time endpoints, or custom scripts.

## Mobile & Support

- Install the DataFast mobile app (iOS/Android) to monitor metrics on the go; connect any site with an API key.
- Use Google Search Console integration for keyword influence; ensure your domain is verified and you have owner/full permissions.
- Track GitHub commits in your dashboard to correlate releases with revenue spikes.
- Reach out to `marc@datafa.st` or `https://feedback.datafa.st/` for help, feature requests, or troubleshooting.

## Troubleshooting Checklist

- Script not firing headers? Confirm the tag is inside `<head>` and the `data-website-id` domain matches `data-domain`.
- No revenue? Verify payment provider connection plus metadata cookies in Stripe/LemonSqueezy/Polar sessions.
- Goals not recorded? Ensure goal names use lowercase/underscores/hyphens and do not exceed 64 characters.
- Vercel preview showing no data? Enable `data-allow-localhost="true"` during staging or rely on proxied script in production.
- Proxy showing all visitors from server IP? Add `x-datafast-real-ip` or forward `X-Forwarded-For`.

## References

- Script configuration reference: `data-allowed-hostnames`, `data-api-url`, `data-allow-localhost`, `data-disable-console`, `data-debug`.
- Revenue attribution guides (Stripe Checkout, PaymentIntent, Checkout Links, LemonSqueezy, Polar, Paddle, Dodo Payments, Easytool).
- Technology-specific install docs for Shopify, Webflow, Wix, Ghost, Next.js, Astro, Laravel, React Router, Firebase, Astro middleware, Caddy, Nginx, DigitalOcean, etc.
