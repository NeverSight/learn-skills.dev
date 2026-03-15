---
name: new-product-website
description: End-to-end workflow for launching a new product landing page — scaffolding, theming, analytics, waitlist, domain, SEO, and deployment.
---

# New Product Website

Automates the full launch workflow for a new product landing page: scaffold Next.js app, configure theme, wire analytics + waitlist, deploy to Vercel, configure domain, and register with Google Search Console.

## Arguments

Provide the product name, domain, and a brief description. Example: `"MyApp at myapp.com — AI-powered task management"`

## Prerequisites

- **Vercel account** with a configured scope/team
- **Domain** purchased (Vercel Domains or external with Vercel nameservers)
- **PostHog** account (US or EU instance)
- **Resend** account for transactional/waitlist emails (shared account across projects)
- **Neon** Postgres database for email storage
- **Google Search Console** access
- **GitHub** org or personal account

## Stack

- Next.js 15 (App Router) + React 19 + TypeScript
- Tailwind CSS 3.4 + Framer Motion
- PostHog for analytics
- Resend for outbound emails, inbound receiving, and waitlist
- Neon Postgres for email storage (`{product}_emails` table)
- Vercel for hosting
- Google Search Console for SEO

## Workflow

### 1. Scaffold Project

```bash
mkdir ~/PROJECT_NAME && cd ~/PROJECT_NAME
```

Create these files manually (don't use `create-next-app` — it hangs on interactive prompts):

| File | Purpose |
|------|---------|
| `package.json` | next 15, react 19, framer-motion, lucide-react, posthog-js, @neondatabase/serverless |
| `tsconfig.json` | Standard Next.js TS config with `@/*` path alias |
| `next.config.ts` | Empty config |
| `postcss.config.mjs` | tailwindcss + autoprefixer |
| `tailwind.config.ts` | Custom theme (accent color, fonts, animations) |
| `src/app/globals.css` | Dark theme, gradient-text, noise-overlay, grid-bg |
| `src/app/layout.tsx` | Root layout with metadata, OG tags, PostHogProvider |
| `src/app/page.tsx` | Compose all sections |

### 2. Build Sections

Standard landing page sections (adapt content per product):

1. **Navbar** — Sticky, backdrop blur, logo + nav links + CTA button
2. **Hero** — Headline + subheadline + terminal/demo animation + waitlist CTA
3. **Stats** — Animated counters with real metrics
4. **How It Works** — 3-step flow with icons
5. **Results/Social Proof** — Real examples styled as platform cards
6. **Features** — 6-card grid with icons
7. **FAQ** — Accordion with AnimatePresence
8. **CTA** — Email capture form + "No spam" disclaimer
9. **Footer** — Logo + nav links

### 3. Wire PostHog

1. Log in to your PostHog instance
2. Create new project named after the product
3. Copy the project API key (starts with `phc_`)
4. Note the PostHog host URL (e.g., `https://us.i.posthog.com` or `https://eu.i.posthog.com`)
5. Create `src/components/posthog-provider.tsx`:

```tsx
"use client";
import posthog from "posthog-js";
import { PostHogProvider as PHProvider } from "posthog-js/react";
import { useEffect } from "react";

const POSTHOG_KEY = process.env.NEXT_PUBLIC_POSTHOG_KEY;
const POSTHOG_HOST = process.env.NEXT_PUBLIC_POSTHOG_HOST || "https://us.i.posthog.com";

export function PostHogProvider({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    if (POSTHOG_KEY && typeof window !== "undefined") {
      posthog.init(POSTHOG_KEY, {
        api_host: POSTHOG_HOST,
        person_profiles: "identified_only",
        capture_pageview: true,
        capture_pageleave: true,
      });
    }
  }, []);
  if (!POSTHOG_KEY) return <>{children}</>;
  return <PHProvider client={posthog}>{children}</PHProvider>;
}
export { posthog };
```

6. Wrap children in `layout.tsx` with `<PostHogProvider>`

### 4. Wire Resend (Domain + Waitlist + Inbound)

#### 4a. Add & Verify Domain in Resend

1. Log in to Resend > Domains > Add domain > enter `DOMAIN`
2. Resend will show DNS records (DKIM TXT, SPF MX + TXT). Add them via Vercel CLI:

```bash
# DKIM
vercel dns add DOMAIN 'resend._domainkey' TXT 'DKIM_VALUE' --scope YOUR_VERCEL_SCOPE
# SPF
vercel dns add DOMAIN 'send' MX 'feedback-smtp.us-east-1.amazonses.com' 10 --scope YOUR_VERCEL_SCOPE
vercel dns add DOMAIN 'send' TXT 'v=spf1 include:amazonses.com ~all' --scope YOUR_VERCEL_SCOPE
# DMARC (deliverability + anti-spoofing)
vercel dns add DOMAIN '_dmarc' TXT 'v=DMARC1; p=none;' --scope YOUR_VERCEL_SCOPE
```

3. Wait for Resend to verify (usually < 5 min)

#### 4b. Enable Inbound Receiving

1. In Resend > Domains > click your domain > Records tab
2. Toggle **"Enable Receiving"** ON
3. Resend shows an MX record for `@`. Add it:

```bash
vercel dns add DOMAIN '' MX 'inbound-smtp.us-east-1.amazonaws.com' 10 --scope YOUR_VERCEL_SCOPE
```

4. Verify with `dig MX DOMAIN +short` — should show `10 inbound-smtp.us-east-1.amazonaws.com.`
5. Wait for Resend to verify the MX record

#### 4c. Create Email Storage Table

Create a `{product}_emails` table in the project's Neon database:

```sql
CREATE TABLE IF NOT EXISTS {product}_emails (
    id SERIAL PRIMARY KEY,
    resend_id TEXT,
    direction TEXT NOT NULL DEFAULT 'inbound',
    from_email TEXT,
    to_email TEXT,
    subject TEXT,
    body_text TEXT,
    body_html TEXT,
    status TEXT DEFAULT 'received',
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_{product}_emails_created_at ON {product}_emails(created_at DESC);
```

#### 4d. Create Inbound Webhook

Create `src/app/api/webhooks/resend/route.ts`:

```tsx
import { NextResponse } from "next/server";
import { neon } from "@neondatabase/serverless";

interface ResendWebhookPayload {
  type: string;
  created_at: string;
  data: {
    email_id: string;
    from: string;
    to: string[];
    subject: string;
    text?: string;
    html?: string;
  };
}

async function fetchInboundContent(emailId: string) {
  const apiKey = process.env.RESEND_API_KEY;
  if (!apiKey) return null;
  try {
    const res = await fetch(
      `https://api.resend.com/emails/receiving/${emailId}`,
      { headers: { Authorization: `Bearer ${apiKey}` } }
    );
    if (!res.ok) return null;
    const data = await res.json();
    return { text: data?.text, html: data?.html };
  } catch {
    return null;
  }
}

export async function POST(request: Request) {
  try {
    const payload: ResendWebhookPayload = await request.json();
    console.log("[PRODUCT Webhook]", payload.type, payload.data.email_id);

    if (payload.type !== "email.received") {
      return NextResponse.json({ success: true, message: "ignored" });
    }

    const { data } = payload;

    // IMPORTANT: Only process emails addressed to @DOMAIN (shared Resend account)
    const isForUs = data.to.some((addr) => addr.endsWith("@DOMAIN"));
    if (!isForUs) {
      return NextResponse.json({ success: true, message: "not for DOMAIN" });
    }

    const content = await fetchInboundContent(data.email_id);

    const sql = neon(process.env.DATABASE_URL!);
    await sql`
      INSERT INTO {product}_emails (resend_id, direction, from_email, to_email, subject, body_text, body_html, status)
      VALUES (${data.email_id}, 'inbound', ${data.from}, ${data.to[0] || ""}, ${data.subject || ""}, ${content?.text || data.text || null}, ${content?.html || data.html || null}, 'received')
    `;

    // Forward to inbox
    const apiKey = process.env.RESEND_API_KEY;
    if (apiKey) {
      await fetch("https://api.resend.com/emails", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${apiKey}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          from: "PRODUCT Inbound <matt@DOMAIN>",
          to: "YOUR_EMAIL",
          subject: `[PRODUCT Inbound] ${data.subject || "(no subject)"}`,
          text: `From: ${data.from}\nTo: ${data.to.join(", ")}\n\n${content?.text || data.text || "(no body)"}`,
        }),
      });
    }

    return NextResponse.json({ success: true });
  } catch (error) {
    console.error("[PRODUCT Webhook] Error:", error);
    return NextResponse.json({ error: "Internal error" }, { status: 500 });
  }
}

export async function GET() {
  return NextResponse.json({ status: "ok" });
}
```

**Replace** `PRODUCT`, `DOMAIN`, and `{product}` with actual values.

#### 4e. Register Webhook with Resend

After deploying (step 5), register the webhook:

```bash
curl -X POST "https://api.resend.com/webhooks" \
  -H "Authorization: Bearer $RESEND_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"endpoint": "https://DOMAIN/api/webhooks/resend", "events": ["email.received"]}'
```

#### 4f. Create Waitlist/Audience

1. In Resend > Audience > create "{Product} Waitlist"
2. Copy the audience ID
3. Create `src/app/api/waitlist/route.ts`:

```tsx
import { NextResponse } from "next/server";
import { neon } from "@neondatabase/serverless";

export async function POST(req: Request) {
  try {
    const { email } = await req.json();
    if (!email || !email.includes("@"))
      return NextResponse.json({ error: "Invalid email" }, { status: 400 });

    const RESEND_API_KEY = process.env.RESEND_API_KEY;
    const RESEND_AUDIENCE_ID = process.env.RESEND_AUDIENCE_ID;
    if (!RESEND_API_KEY || !RESEND_AUDIENCE_ID)
      return NextResponse.json({ error: "Server config error" }, { status: 500 });

    // Add contact to audience
    const audienceRes = await fetch(
      `https://api.resend.com/audiences/${RESEND_AUDIENCE_ID}/contacts`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${RESEND_API_KEY}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, unsubscribed: false }),
      }
    );

    if (!audienceRes.ok)
      return NextResponse.json({ error: "Failed to subscribe" }, { status: 500 });

    // Send welcome email
    const emailRes = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${RESEND_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        from: "Matt <matt@DOMAIN>",
        to: [email],
        subject: "You're in — PRODUCT access request received",
        html: `<!-- Customize welcome email HTML here -->`,
      }),
    });

    // Log outbound email to DB
    try {
      const emailData = await emailRes.json().catch(() => null);
      const sql = neon(process.env.DATABASE_URL!);
      await sql`
        INSERT INTO {product}_emails (resend_id, direction, from_email, to_email, subject, status)
        VALUES (${emailData?.id || null}, 'outbound', 'matt@DOMAIN', ${email}, ${"Welcome email"}, 'sent')
      `;
    } catch (logErr) {
      console.error("Email log error:", logErr);
    }

    return NextResponse.json({ success: true });
  } catch {
    return NextResponse.json({ error: "Internal error" }, { status: 500 });
  }
}
```

4. CTA form calls `/api/waitlist` + fires `posthog?.capture("waitlist_signup", { email })`

### 5. Deploy to Vercel

```bash
# Init git and push to GitHub
git init && git add -A && git commit -m "Initial landing page"
gh repo create YOUR_ORG/PROJECT_NAME --private --source=. --push

# Deploy to Vercel
npx vercel --yes --scope YOUR_VERCEL_SCOPE

# Add domain
npx vercel domains add DOMAIN --scope YOUR_VERCEL_SCOPE

# Set env vars (production)
npx vercel env add NEXT_PUBLIC_POSTHOG_KEY production --scope YOUR_VERCEL_SCOPE <<< "KEY"
npx vercel env add NEXT_PUBLIC_POSTHOG_HOST production --scope YOUR_VERCEL_SCOPE <<< "https://us.i.posthog.com"
npx vercel env add RESEND_API_KEY production --scope YOUR_VERCEL_SCOPE <<< "KEY"
npx vercel env add RESEND_AUDIENCE_ID production --scope YOUR_VERCEL_SCOPE <<< "ID"
npx vercel env add DATABASE_URL production --scope YOUR_VERCEL_SCOPE <<< "postgresql://..."

# Production deploy
npx vercel --prod --scope YOUR_VERCEL_SCOPE
```

### 6. Google Search Console

1. Navigate to https://search.google.com/search-console
2. Add property > Domain > enter domain
3. Copy the TXT verification record
4. Add via Vercel DNS: `npx vercel dns add DOMAIN @ TXT "google-site-verification=..." --scope YOUR_VERCEL_SCOPE`
5. Click Verify
6. Submit sitemap: create `src/app/sitemap.ts`:

```tsx
import type { MetadataRoute } from "next";

export default function sitemap(): MetadataRoute.Sitemap {
  return [
    {
      url: "https://DOMAIN",
      lastModified: new Date(),
      changeFrequency: "weekly",
      priority: 1,
    },
  ];
}
```

7. In Search Console > Sitemaps, submit `https://DOMAIN/sitemap.xml`

### 7. Add to Analytics Dashboard

Add the new domain to the unified analytics dashboard at `~/analytics-dashboard/`.

1. Edit `src/lib/config.ts` — add a new entry to the `DOMAINS` array:

```ts
{
  slug: "my-app",           // kebab-case domain (used in URL paths)
  domain: "myapp.com",      // bare domain
  label: "MyApp",           // display name
  posthog: { projectId: "PROJECT_ID", host: "us" },  // "us" or "eu"
  gscProperty: "sc-domain:myapp.com",
  // If the project has a waitlist with PostHog tracking, add:
  customEvents: [{ event: "waitlist_signup", label: "Waitlist Signups" }],
  // If the project uses Resend for waitlist/audience, add:
  resend: { audienceId: "AUDIENCE_ID" },  // get ID from: curl https://api.resend.com/audiences -H "Authorization: Bearer $RESEND_API_KEY"
},
```

2. Commit, push, and deploy:

```bash
cd ~/analytics-dashboard
git add src/lib/config.ts
git commit -m "Add PROJECT_NAME to analytics dashboard"
git push
npx vercel --prod --scope YOUR_VERCEL_SCOPE
```

Dashboard URL: your analytics dashboard URL

### 8. Verify Everything

- [ ] Site loads at `https://DOMAIN`
- [ ] Waitlist form submits and shows success
- [ ] Welcome email received (check with `gmail` skill or Resend Sending tab)
- [ ] Email appears in Resend audience
- [ ] Outbound email logged in `{product}_emails` table (direction='outbound')
- [ ] PostHog captures `$pageview` and `waitlist_signup` events
- [ ] Resend domain fully verified (DKIM + SPF + DMARC + MX inbound)
- [ ] Inbound test: send email to `matt@DOMAIN`, confirm it appears in Resend Receiving tab
- [ ] Inbound webhook: confirm email stored in `{product}_emails` table (direction='inbound')
- [ ] Inbound forwarding: confirm `[PRODUCT Inbound]` email arrives at `YOUR_EMAIL`
- [ ] Domain filter: confirm webhook ignores emails to other domains on the shared Resend account
- [ ] Google Search Console shows "Ownership verified"
- [ ] Sitemap is submitted (may show "Couldn't fetch" initially — normal)
