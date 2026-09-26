---
name: opencals-build-booking-site
description: >-
  Build, customise and deploy a production booking website on the Opencals
  hosted API by starting from one of the official open-source Next.js templates
  (salon, barbershop, clinic, padel/squash club) and the @opencals/storefront-sdk.
  Use when the user wants a booking/appointment/scheduling site, an Opencals
  storefront, gives you a business idea + inspiration and asks you to build the
  booking site, or says "build me a booking website". Covers picking a template,
  scaffolding, wiring services + availability + checkout, rebranding, and
  deploying to Vercel. For the exact API/SDK call shapes, use the companion
  `opencals-storefront-api` skill.
---

# Build an Opencals booking storefront

You are helping someone stand up a real, bookable storefront on the Opencals
hosted booking API. You do **not** build a booking engine — availability maths,
timezones and double-booking are handled by the API. Your job is the frontend:
start from a template, point it at their store, restyle it, deploy it.

For exact SDK method names and argument shapes, use the companion
**`opencals-storefront-api`** skill — it is the ground truth for availability,
carts, appointments, checkout, discounts, self-service, guests/attendees, custom
durations and rate limiting. This skill is the build workflow around it.

## When to use this skill

Trigger when the user wants a booking, appointment, or scheduling website; an
"Opencals storefront"; hands you a business description + inspiration
(screenshots, a competitor site) and asks for the booking site. If they need a
*self-hosted* booking engine or data residency, this is the wrong tool — tell
them so and point them at Cal.com or Easy!Appointments.

## Primary journey: idea + inspiration → live site

1. **Understand the business.** What do they sell time for — people's time
   (stylist, clinician, coach) or *things* (courts, rooms, lanes, equipment), or
   both? Group sessions? Multiple locations? Online/delivery? This decides the
   template and the modelling.
2. **Pick the closest template** (below). Match the *booking shape* first, looks
   second — restyling is cheap, re-architecting isn't.
3. **Scaffold → configure → wire → rebrand → deploy** (the workflow below).
4. Pull design cues from their inspiration into the template's tokens/components;
   keep the wired booking flow intact.

If the goal is to add booking to an **existing** site rather than build a new
one, the same SDK and API apply — lean on the `opencals-storefront-api` skill and
embed the flow into their app (or an iframe/widget) instead of scaffolding a new
template.

## Prerequisites (ask for these first)

1. **What kind of business** — pick the closest starting template:
   - `template-haar` — salon (services + gallery, warm/editorial)
   - `template-frisor` — barbershop (dark, editorial)
   - `template-clarity` — clinic (department-first, medical; passwordless login)
   - `template-volt` (a.k.a. padel template) — padel & squash club (dark/technical):
     a **hybrid** of bookable resources (courts) and staff-led sessions
     (coaching). Start here for any venue that rents out interchangeable units —
     courts, lanes, rooms, bays, equipment — especially alongside classes or
     lessons. See "Resource-booking businesses" below.
2. **An Opencals Storefront API key** (`sfk_...`) — from the Opencals dashboard.
   If they don't have one, direct them to create a store and a storefront key
   before deploying (the site builds without it, but won't return live data).
3. Node.js 20+ and a Vercel account (free tier is fine) for deployment.

## Workflow

### 1. Scaffold from the closest template

```bash
npx create-next-app -e https://github.com/letsopencals/template-haar my-booking-site
cd my-booking-site
npm install
```

Swap the repo for `template-frisor`, `template-clarity` or `template-volt` as
appropriate. These are complete apps — services catalogue, real-time
availability, cart, checkout, Stripe payments and customer accounts are already
wired. Do not rebuild them.

### 2. Configure environment

Copy `.env.example` to `.env.local` and fill in:

```
OPENCALS_API_KEY=sfk_your_key_here          # Required — the storefront key
AUTH_SECRET=<random string>                 # Required — session encryption
# OPENCALS_API_URL=https://api.opencals.com # Optional — defaults to this
# NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_...  # Optional — for payments
```

Generate `AUTH_SECRET` with `openssl rand -base64 32`.

### 3. Understand the SDK wiring (do not reinvent it)

The SDK is initialised once via a side-effect import in `lib/opencals.ts`, which
every API route imports at the top. Services are class-based
(`ProductService`, `CartService`, `AppointmentService`, `CheckoutService`,
`AuthService`, `SelfService`, …). See `references/booking-flow.md` for the
build-level overview, and the `opencals-storefront-api` skill for the exact
call shapes — **use those, do not invent method names.**

### 4. Rebrand and customise

Mostly design, not plumbing: colour/font tokens in `app/globals.css`, copy and
business details in `lib/site-config.ts`; services/staff/locations come from the
store via the API. See `references/customizing.md`.

### 5. Verify locally

```bash
npm run dev
```

Confirm services load, availability returns slots, and a test booking completes.
API routes surface real errors via `handleApiError` — read them, don't swallow.

### 6. Deploy to Vercel

```bash
npx vercel
```

Add the same env vars in the Vercel project settings, then `npx vercel --prod`.
Free tier is fine for launch; the user pays Opencals only for bookings.

## Resource-booking businesses (courts, lanes, rooms, equipment)

Some venues book *things*, often many interchangeable units, sometimes alongside
staff-led classes. The padel/volt template is the worked example. Model each with
the conflict rule that fits — don't force everything through "staff". Custom
duration uses `allowCustomDuration`, not duration-variant products. Full details,
the three-rule decision table, and the grid data strategy are in
`references/resource-booking.md` (and the API shapes in the
`opencals-storefront-api` skill's `custom-duration.md` / `availability.md`).

## Resources

- [Opencals](https://opencals.com) — main site
- [Docs & API reference](https://opencals.com/docs)
- [@opencals/storefront-sdk on npm](https://www.npmjs.com/package/@opencals/storefront-sdk)
- [Dashboard](https://app.opencals.com) — create stores, manage storefront API keys

## Guardrails

- Never hard-code services, prices or availability in the frontend — they come
  from the API.
- Never invent SDK method names. Use the `opencals-storefront-api` skill or the
  template's existing `app/api/` routes.
- The frontend is MIT-licensed: it's fine to strip all Opencals branding from
  the UI. The API itself is not open source and is not part of what you ship.
