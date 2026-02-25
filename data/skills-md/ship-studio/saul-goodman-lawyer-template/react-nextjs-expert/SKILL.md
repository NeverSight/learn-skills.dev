---
name: react-nextjs-expert
description: Expert guidance for React and Next.js 14+ App Router development. Use this skill when creating components, pages, layouts, or any React/Next.js code. Ensures proper patterns for Server Components, Client Components, routing, data fetching, and Tailwind CSS styling.
---

# React & Next.js Expert

Expert guidance for Next.js 14+ with App Router. This project uses React Server Components by default.

## File-Based Routing

```
app/
├── page.tsx           → yoursite.com
├── about/page.tsx     → yoursite.com/about
├── blog/[slug]/page.tsx → yoursite.com/blog/any-post
├── layout.tsx         → Wraps all pages (navigation, footer)
└── globals.css        → Global styles + Tailwind
```

## Server vs Client Components

**Server Components (default)** - Run on server, can't use hooks or browser APIs:
```tsx
// app/page.tsx - Server Component by default
export default function Home() {
  return <h1>Hello</h1>  // Renders on server
}
```

**Client Components** - Add `'use client'` for interactivity:
```tsx
'use client'
import { useState } from 'react'

export default function Counter() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(count + 1)}>{count}</button>
}
```

## When to Use Client Components

Add `'use client'` only when you need:
- `useState`, `useEffect`, or other hooks
- Event handlers (`onClick`, `onChange`, etc.)
- Browser APIs (`window`, `localStorage`)
- Third-party libraries that use hooks

## Component Patterns

**Page component:**
```tsx
export default function AboutPage() {
  return (
    <main className="min-h-screen p-8">
      <h1 className="text-4xl font-bold">About Us</h1>
      <p className="mt-4 text-gray-600">Our story...</p>
    </main>
  )
}
```

**Reusable component:**
```tsx
// components/Button.tsx
interface ButtonProps {
  children: React.ReactNode
  variant?: 'primary' | 'secondary'
  onClick?: () => void
}

export function Button({ children, variant = 'primary', onClick }: ButtonProps) {
  const styles = variant === 'primary'
    ? 'bg-blue-600 text-white'
    : 'bg-gray-200 text-gray-800'

  return (
    <button className={`px-4 py-2 rounded ${styles}`} onClick={onClick}>
      {children}
    </button>
  )
}
```

## Layout Pattern

```tsx
// app/layout.tsx
import './globals.css'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <nav className="p-4 bg-gray-100">
          <a href="/">Home</a>
          <a href="/about" className="ml-4">About</a>
        </nav>
        {children}
        <footer className="p-4 bg-gray-100 mt-8">
          &copy; 2024 My Site
        </footer>
      </body>
    </html>
  )
}
```

## Tailwind CSS

Use Tailwind classes for all styling. Never create separate CSS files.

**Common patterns:**
```tsx
// Spacing: p-4, m-2, px-6, py-3, mt-8, mb-4
// Text: text-xl, font-bold, text-gray-600, text-center
// Layout: flex, grid, items-center, justify-between
// Sizing: w-full, h-screen, max-w-4xl, min-h-screen
// Colors: bg-blue-600, text-white, border-gray-300
// Responsive: md:flex-row, lg:text-xl, sm:p-4
```

## Images

```tsx
import Image from 'next/image'

<Image
  src="/logo.png"      // From public folder
  alt="Company Logo"
  width={200}
  height={100}
/>
```

## Links

```tsx
import Link from 'next/link'

<Link href="/about" className="text-blue-600 hover:underline">
  About Us
</Link>
```

## Common Mistakes to Avoid

1. **Don't create .html files** - This is React, use .tsx
2. **Don't use `<script>` tags** - Use React patterns
3. **Don't create .css files** - Use Tailwind classes
4. **Don't forget `'use client'`** - Add it when using hooks
5. **Don't nest layouts incorrectly** - One layout.tsx per route segment
