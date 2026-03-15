---
name: performance-optimization
description: Expert guide for optimizing Next.js performance - images, fonts, code splitting, caching, and Core Web Vitals. Use when improving load times or debugging performance issues.
---

# Performance Optimization Skill

## Overview

This skill helps you optimize your Next.js application for maximum performance. From image optimization to code splitting, this covers all the techniques you need to achieve excellent Core Web Vitals scores.

## Core Web Vitals

### 1. Largest Contentful Paint (LCP)
Target: < 2.5s

**Optimize:**
- Use `next/image` for images
- Implement proper caching
- Use CDN for static assets
- Optimize server response time
- Reduce render-blocking resources

### 2. First Input Delay (FID) / Interaction to Next Paint (INP)
Target: < 100ms / < 200ms

**Optimize:**
- Minimize JavaScript execution
- Code split large bundles
- Use Web Workers for heavy tasks
- Defer non-critical JavaScript
- Optimize event handlers

### 3. Cumulative Layout Shift (CLS)
Target: < 0.1

**Optimize:**
- Set image dimensions
- Reserve space for ads
- Avoid inserting content above existing content
- Use `transform` instead of layout properties

## Image Optimization

### Next.js Image Component
```typescript
import Image from 'next/image'

// ✅ Optimized
export function OptimizedImage() {
  return (
    <Image
      src="/hero.jpg"
      alt="Hero image"
      width={1200}
      height={600}
      priority  // For above-fold images
      quality={85}  // Default: 75
      placeholder="blur"
      blurDataURL="data:image/..." // Or import for static
    />
  )
}

// For external images, configure domains
// next.config.js
module.exports = {
  images: {
    domains: ['example.com'],
    // Or use remotePatterns for more control
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**.example.com',
      },
    ],
  },
}
```

### Responsive Images
```typescript
<Image
  src="/hero.jpg"
  alt="Hero"
  fill
  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
  style={{ objectFit: 'cover' }}
  priority
/>
```

### Image Formats
```typescript
// next.config.js
module.exports = {
  images: {
    formats: ['image/avif', 'image/webp'],
  },
}
```

## Font Optimization

### Using next/font
```typescript
// app/layout.tsx
import { Inter, Roboto_Mono } from 'next/font/google'

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
})

const robotoMono = Roboto_Mono({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-roboto-mono',
})

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={`${inter.variable} ${robotoMono.variable}`}>
      <body className="font-sans">{children}</body>
    </html>
  )
}

// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      fontFamily: {
        sans: ['var(--font-inter)'],
        mono: ['var(--font-roboto-mono)'],
      },
    },
  },
}
```

### Local Fonts
```typescript
import localFont from 'next/font/local'

const customFont = localFont({
  src: './fonts/custom-font.woff2',
  display: 'swap',
  variable: '--font-custom',
})
```

## Code Splitting

### Dynamic Imports
```typescript
import dynamic from 'next/dynamic'

// Load component only when needed
const HeavyComponent = dynamic(() => import('@/components/heavy-component'), {
  loading: () => <p>Loading...</p>,
  ssr: false,  // Disable SSR for this component
})

export function Page() {
  return (
    <div>
      <HeavyComponent />
    </div>
  )
}
```

### Conditional Loading
```typescript
'use client'
import { useState } from 'react'
import dynamic from 'next/dynamic'

const Chart = dynamic(() => import('@/components/chart'), {
  ssr: false,
})

export function Dashboard() {
  const [showChart, setShowChart] = useState(false)

  return (
    <div>
      <button onClick={() => setShowChart(true)}>Show Chart</button>
      {showChart && <Chart />}
    </div>
  )
}
```

### Named Exports
```typescript
const ComponentA = dynamic(() =>
  import('@/components/bundle').then((mod) => mod.ComponentA)
)
```

## React Optimization

### React.memo
```typescript
import { memo } from 'react'

// Only re-renders if props change
const ExpensiveComponent = memo(function ExpensiveComponent({
  data,
}: {
  data: Data
}) {
  return <div>{/* Expensive rendering */}</div>
})

// Custom comparison
const MemoizedComponent = memo(
  Component,
  (prevProps, nextProps) => {
    return prevProps.id === nextProps.id
  }
)
```

### useMemo
```typescript
'use client'
import { useMemo } from 'react'

export function DataTable({ items }: { items: Item[] }) {
  // Only recalculate when items change
  const sortedItems = useMemo(() => {
    return items.sort((a, b) => a.name.localeCompare(b.name))
  }, [items])

  return (
    <table>
      {sortedItems.map((item) => (
        <tr key={item.id}>
          <td>{item.name}</td>
        </tr>
      ))}
    </table>
  )
}
```

### useCallback
```typescript
'use client'
import { useCallback, useState } from 'react'

export function Parent() {
  const [count, setCount] = useState(0)

  // Stable function reference
  const handleClick = useCallback(() => {
    console.log('clicked')
  }, [])

  return <Child onClick={handleClick} />
}
```

## Caching Strategies

### API Route Caching
```typescript
// app/api/data/route.ts
export async function GET() {
  const data = await fetchData()

  return Response.json(data, {
    headers: {
      'Cache-Control': 'public, s-maxage=60, stale-while-revalidate=30',
    },
  })
}
```

### Data Fetching Caching
```typescript
// Revalidate every hour
const data = await fetch('https://api.example.com/data', {
  next: { revalidate: 3600 },
})

// Never cache (always fresh)
const data = await fetch('https://api.example.com/data', {
  cache: 'no-store',
})

// Cache forever
const data = await fetch('https://api.example.com/data', {
  cache: 'force-cache',
})
```

### Tag-based Revalidation
```typescript
// Tag the fetch
const data = await fetch('https://api.example.com/posts', {
  next: { tags: ['posts'] },
})

// Revalidate all 'posts' fetches
import { revalidateTag } from 'next/cache'

export async function POST() {
  // Mutate data
  await createPost()
  // Revalidate
  revalidateTag('posts')
}
```

## Bundle Optimization

### Analyze Bundle
```bash
# Add to package.json
{
  "scripts": {
    "analyze": "ANALYZE=true next build"
  }
}

# Install bundle analyzer
npm install @next/bundle-analyzer
```

```javascript
// next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
})

module.exports = withBundleAnalyzer({
  // Your config
})
```

### Tree Shaking
```typescript
// ❌ Bad - Imports entire library
import _ from 'lodash'

// ✅ Good - Only imports what you need
import debounce from 'lodash/debounce'
```

### Remove Unused Dependencies
```bash
# Find unused dependencies
npx depcheck

# Remove them
npm uninstall unused-package
```

## Streaming and Suspense

### Streaming Components
```typescript
// app/dashboard/page.tsx
import { Suspense } from 'react'

async function SlowComponent() {
  const data = await slowFetch()
  return <div>{data}</div>
}

export default function Dashboard() {
  return (
    <div>
      <h1>Dashboard</h1>
      <Suspense fallback={<Loading />}>
        <SlowComponent />
      </Suspense>
    </div>
  )
}
```

### Multiple Suspense Boundaries
```typescript
export default function Page() {
  return (
    <div>
      <Suspense fallback={<HeaderSkeleton />}>
        <Header />
      </Suspense>

      <Suspense fallback={<ContentSkeleton />}>
        <Content />
      </Suspense>

      <Suspense fallback={<SidebarSkeleton />}>
        <Sidebar />
      </Suspense>
    </div>
  )
}
```

## Database Query Optimization

### Use Prisma Efficiently
```typescript
// ❌ Bad - N+1 query problem
const users = await prisma.user.findMany()
for (const user of users) {
  const posts = await prisma.post.findMany({ where: { userId: user.id } })
}

// ✅ Good - Single query with include
const users = await prisma.user.findMany({
  include: {
    posts: true,
  },
})

// ✅ Better - Select only what you need
const users = await prisma.user.findMany({
  select: {
    id: true,
    name: true,
    posts: {
      select: {
        id: true,
        title: true,
      },
    },
  },
})
```

### Database Indexes
```prisma
model Post {
  id        String   @id @default(cuid())
  title     String
  userId    String
  createdAt DateTime @default(now())

  // Add indexes for frequently queried fields
  @@index([userId])
  @@index([createdAt])
  @@index([userId, createdAt])
}
```

## Prerendering Strategies

### Static Site Generation (SSG)
```typescript
// Fully static - generated at build time
export default async function Page() {
  const data = await fetch('https://api.example.com/data')
  return <div>{/* Render data */}</div>
}
```

### Incremental Static Regeneration (ISR)
```typescript
// Revalidate every 60 seconds
export const revalidate = 60

export default async function Page() {
  const data = await fetch('https://api.example.com/data')
  return <div>{/* Render data */}</div>
}
```

### Dynamic Rendering
```typescript
// Force dynamic rendering
export const dynamic = 'force-dynamic'

export default async function Page() {
  const data = await fetch('https://api.example.com/data', {
    cache: 'no-store',
  })
  return <div>{/* Render data */}</div>
}
```

## Lazy Loading

### Images
```typescript
<Image
  src="/image.jpg"
  alt="Image"
  width={500}
  height={300}
  loading="lazy"  // Default behavior
/>
```

### Components on Scroll
```typescript
'use client'
import { useEffect, useState, useRef } from 'react'
import dynamic from 'next/dynamic'

const HeavyComponent = dynamic(() => import('@/components/heavy'))

export function LazySection() {
  const [isVisible, setIsVisible] = useState(false)
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true)
          observer.disconnect()
        }
      },
      { threshold: 0.1 }
    )

    if (ref.current) {
      observer.observe(ref.current)
    }

    return () => observer.disconnect()
  }, [])

  return (
    <div ref={ref}>
      {isVisible ? <HeavyComponent /> : <div>Loading...</div>}
    </div>
  )
}
```

## Performance Monitoring

### Measuring Performance
```typescript
'use client'
import { useEffect } from 'react'

export function PerformanceMonitor() {
  useEffect(() => {
    // Measure LCP
    new PerformanceObserver((list) => {
      const entries = list.getEntries()
      const lastEntry = entries[entries.length - 1]
      console.log('LCP:', lastEntry.renderTime || lastEntry.loadTime)
    }).observe({ type: 'largest-contentful-paint', buffered: true })

    // Measure FID
    new PerformanceObserver((list) => {
      const entries = list.getEntries()
      entries.forEach((entry) => {
        console.log('FID:', entry.processingStart - entry.startTime)
      })
    }).observe({ type: 'first-input', buffered: true })

    // Measure CLS
    let clsScore = 0
    new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        if (!entry.hadRecentInput) {
          clsScore += entry.value
        }
      }
      console.log('CLS:', clsScore)
    }).observe({ type: 'layout-shift', buffered: true })
  }, [])

  return null
}
```

## Best Practices Checklist

- [ ] Use `next/image` for all images
- [ ] Optimize fonts with `next/font`
- [ ] Implement code splitting for large components
- [ ] Use React.memo for expensive components
- [ ] Implement proper caching strategies
- [ ] Set up Suspense boundaries
- [ ] Optimize database queries
- [ ] Enable ISR for semi-static content
- [ ] Lazy load below-the-fold content
- [ ] Monitor Core Web Vitals
- [ ] Minimize JavaScript bundle size
- [ ] Use CDN for static assets
- [ ] Implement proper loading states
- [ ] Test on slow 3G connections

## When to Use This Skill

Invoke this skill when:
- Optimizing page load times
- Improving Core Web Vitals scores
- Reducing bundle size
- Debugging performance issues
- Setting up caching strategies
- Implementing lazy loading
- Optimizing images or fonts
- Improving database query performance
