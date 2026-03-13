---
name: integrate-uppy-transloadit-s3-uploading-to-nextjs
description: Add Uppy Dashboard + Transloadit uploads to a Next.js (App Router) app, with server-side signature generation and optional /s3/store export.
---

# Inputs

- Required env (server-only): `TRANSLOADIT_KEY`, `TRANSLOADIT_SECRET`
- Optional env: `TRANSLOADIT_TEMPLATE_ID` (recommended once you create a template)

For local dev, put these in `.env.local`. Never expose `TRANSLOADIT_SECRET` to the browser.

# Install

```bash
npm i @transloadit/utils @uppy/core @uppy/dashboard @uppy/transloadit
```

# Implement (Golden Path)

Pick the root:
- If your project has `src/app`, use `src/app/...`
- Else use `app/...`

## 1) Server: return signed Assembly options to the browser

Create `app/api/transloadit/assembly-options/route.ts` (or `src/app/api/transloadit/assembly-options/route.ts` if you use `src/`):

```ts
import { NextResponse } from 'next/server'
import { signParamsSync } from '@transloadit/utils/node'

export const runtime = 'nodejs'

function reqEnv(name: string): string {
  const v = process.env[name]
  if (!v) throw new Error(`Missing required env var: ${name}`)
  return v
}

function formatExpiresUtc(minutesFromNow: number): string {
  const ms = Date.now() + minutesFromNow * 60_000
  return new Date(ms).toISOString().replace(/\.\d{3}Z$/, 'Z')
}

export async function POST() {
  try {
    const authKey = reqEnv('TRANSLOADIT_KEY')
    const authSecret = reqEnv('TRANSLOADIT_SECRET')
    const templateId = process.env.TRANSLOADIT_TEMPLATE_ID

    const params: Record<string, unknown> = {
      auth: { key: authKey, expires: formatExpiresUtc(30) },
    }

    if (templateId) {
      params.template_id = templateId
    } else {
      // Minimal "known good" steps (works without pre-creating a template).
      params.steps = {
        resized: {
          robot: '/image/resize',
          use: ':original',
          width: 320,
        },
      }
    }

    const paramsString = JSON.stringify(params)
    const signature = signParamsSync(paramsString, authSecret)

    // Uppy expects `{ params: <string|object>, signature: <string> }`.
    return NextResponse.json({ params: paramsString, signature })
  } catch (err) {
    const message = err instanceof Error ? err.message : 'Unknown error'
    return NextResponse.json({ error: message }, { status: 500 })
  }
}
```

## 2) Client: mount Uppy Dashboard + Transloadit plugin

Add the CSS (for App Router, do it in your root layout):

```ts
import '@uppy/core/css/style.min.css'
import '@uppy/dashboard/css/style.min.css'
```

Create a client component like `app/upload-demo.tsx`:

```tsx
'use client'

import { useEffect, useMemo, useRef, useState } from 'react'
import Uppy from '@uppy/core'
import Dashboard from '@uppy/dashboard'
import Transloadit, { type AssemblyOptions } from '@uppy/transloadit'

export default function UploadDemo() {
  const dashboardEl = useRef<HTMLDivElement | null>(null)
  const [results, setResults] = useState<unknown>(null)
  const [uploadPct, setUploadPct] = useState<number>(0)

  const uppy = useMemo(() => {
    const instance = new Uppy({
      autoProceed: true,
      restrictions: { maxNumberOfFiles: 1 },
    })

    instance.use(Transloadit, {
      waitForEncoding: true,
      alwaysRunAssembly: true,
      assemblyOptions: async (): Promise<AssemblyOptions> => {
        const res = await fetch('/api/transloadit/assembly-options', { method: 'POST' })
        if (!res.ok) throw new Error(`Failed to get assembly options: ${res.status}`)
        return (await res.json()) as AssemblyOptions
      },
    })

    return instance
  }, [])

  useEffect(() => {
    if (!dashboardEl.current) return

    uppy.use(Dashboard, {
      target: dashboardEl.current,
      inline: true,
      proudlyDisplayPoweredByUppy: false,
      hideUploadButton: true,
      hideProgressDetails: false,
      height: 350,
    })

    const onResult = (stepName: string, result: unknown) =>
      setResults((prev: unknown) => {
        const base: Record<string, unknown> =
          typeof prev === 'object' && prev !== null ? { ...(prev as Record<string, unknown>) } : {}
        const existing = base[stepName]
        base[stepName] = Array.isArray(existing) ? existing.concat([result]) : [result]
        return base
      })

    const onUploadProgress = (_file: unknown, progress: { bytesUploaded: number; bytesTotal: number | null }) => {
      if (!progress?.bytesTotal) return
      setUploadPct(Math.round((progress.bytesUploaded / progress.bytesTotal) * 100))
    }

    uppy.on('transloadit:result', onResult)
    uppy.on('upload-progress', onUploadProgress)

    return () => {
      uppy.off('transloadit:result', onResult)
      uppy.off('upload-progress', onUploadProgress)
      uppy.getPlugin('Dashboard')?.uninstall()
      uppy.destroy()
    }
  }, [uppy])

  return (
    <section>
      <div ref={dashboardEl} />
      <div style={{ marginTop: 12 }}>{uploadPct}%</div>
      <pre style={{ marginTop: 12 }}>{results ? JSON.stringify(results, null, 2) : '(no results yet)'}</pre>
    </section>
  )
}
```

# Optional: /s3/store Export

Recommended approach: create Template Credentials in Transloadit (so you don’t ship AWS keys anywhere) and reference them in `/s3/store`.

Example steps:

```json
{
  "resized": { "robot": "/image/resize", "use": ":original", "width": 320 },
  "exported": {
    "robot": "/s3/store",
    "use": "resized",
    "credentials": "YOUR_TRANSLOADIT_TEMPLATE_CREDENTIALS_NAME",
    "path": "uppy-nextjs/${unique_prefix}/${file.url_name}",
    "acl": "private"
  }
}
```

If you intentionally want public objects, change `"acl"` to `"public-read"` (and consider bucket policy, access logs, and data retention).

Then create a template and set `TRANSLOADIT_TEMPLATE_ID`:

```bash
npx -y @transloadit/node templates create uppy-nextjs-resize-to-s3 ./steps.json -j
```

# References (Internal)

- Working reference implementation: `https://github.com/transloadit/skills/tree/main/scenarios/integrate-uppy-transloadit-s3-uploading-to-nextjs`
- Proven steps JSON: `https://github.com/transloadit/skills/blob/main/scenarios/integrate-uppy-transloadit-s3-uploading-to-nextjs/transloadit/steps/resize-only.json`, `https://github.com/transloadit/skills/blob/main/scenarios/integrate-uppy-transloadit-s3-uploading-to-nextjs/transloadit/steps/resize-to-s3.json`

Tested with (see the scenario lockfile for the exact versions):
- Next.js 16.1.6 (App Router)
- React 19.2.3
- @transloadit/utils 4.3.0 (Assembly signing)
- @uppy/core 5.2.0, @uppy/dashboard 5.1.1, @uppy/transloadit 5.5.0
