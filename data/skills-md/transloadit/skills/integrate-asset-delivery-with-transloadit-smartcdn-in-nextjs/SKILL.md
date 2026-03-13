---
name: integrate-asset-delivery-with-transloadit-smartcdn-in-nextjs
description: Add Transloadit Smart CDN URL signing to a Next.js App Router project (server-side signing route + optional client demo page).
---

# Inputs

- Required env (server-only): `TRANSLOADIT_KEY`, `TRANSLOADIT_SECRET`
- Optional env: `TRANSLOADIT_SMARTCDN_WORKSPACE`, `TRANSLOADIT_SMARTCDN_TEMPLATE`, `TRANSLOADIT_SMARTCDN_INPUT`

For local dev, put these in `.env.local`. Never expose `TRANSLOADIT_SECRET` to the browser.

# Install

```bash
npm i @transloadit/utils
```

# Implement (App Router)

Pick the root:
- If your project has `src/app`, use `src/app/...`
- Else use `app/...`

## 1) Server route: sign Smart CDN URLs

Create `app/api/smartcdn/route.ts` (or `src/app/api/smartcdn/route.ts` if you use `src/`):

```ts
import { NextResponse } from 'next/server'
import { getSignedSmartCdnUrl } from '@transloadit/utils/node'

export const runtime = 'nodejs'

function reqEnv(name: string): string {
  const v = process.env[name]
  if (!v) throw new Error(`Missing required env var: ${name}`)
  return v
}

export async function GET() {
  try {
    const authKey = reqEnv('TRANSLOADIT_KEY')
    const authSecret = reqEnv('TRANSLOADIT_SECRET')

    const workspace = process.env.TRANSLOADIT_SMARTCDN_WORKSPACE || 'demo'
    const template = process.env.TRANSLOADIT_SMARTCDN_TEMPLATE || 'serve-preview'
    const input = process.env.TRANSLOADIT_SMARTCDN_INPUT || 'example.jpg'

    const url = getSignedSmartCdnUrl({ workspace, template, input, authKey, authSecret })

    return NextResponse.json({ url, workspace, template, input })
  } catch (err) {
    const message = err instanceof Error ? err.message : 'Unknown error'
    return NextResponse.json({ error: message }, { status: 500 })
  }
}
```

## 2) Optional: a tiny demo page

Create `app/smartcdn/page.tsx` (or `src/app/smartcdn/page.tsx`):

```tsx
import SmartCdnDemo from './smartcdn-demo'

export default function SmartCdnPage() {
  return (
    <main style={{ padding: 24 }}>
      <h1 style={{ fontSize: 20, fontWeight: 600 }}>Smart CDN Signed URL</h1>
      <SmartCdnDemo />
    </main>
  )
}
```

Create `app/smartcdn/smartcdn-demo.tsx` (or `src/app/smartcdn/smartcdn-demo.tsx`):

```tsx
'use client'

import { useEffect, useState } from 'react'

export default function SmartCdnDemo() {
  const [payload, setPayload] = useState<unknown>(null)

  useEffect(() => {
    let cancelled = false
    fetch('/api/smartcdn', { cache: 'no-store' })
      .then(async (res) => res.json())
      .then((json) => {
        if (!cancelled) setPayload(json)
      })
      .catch((err) => {
        if (!cancelled) setPayload({ error: String(err) })
      })
    return () => {
      cancelled = true
    }
  }, [])

  return (
    <pre data-testid="smartcdn-json">
      {payload ? JSON.stringify(payload, null, 2) : '(loading)'}
    </pre>
  )
}
```

# Quick Check

- Start dev server, then open `/smartcdn` or fetch `/api/smartcdn`.
- Expect JSON including a `url` and your `{ workspace, template, input }`.

# References (Internal)

- Working reference implementation: `https://github.com/transloadit/skills/tree/main/scenarios/integrate-asset-delivery-with-transloadit-smartcdn-in-nextjs`

Tested with (see the scenario lockfile for the exact versions):
- Next.js 16.1.6 (App Router)
- React 19.2.3
- @transloadit/utils 4.3.0 (Smart CDN signing)
