---
name: frontend-master
description: Master skill for frontend development with Next.js + React + Tailwind stack. Decision framework for choosing components, animations, assets, and tools. Routes to specialized skills for implementation details. Use as entry point for any frontend task.
allowed-tools: Read, Edit, Write, Bash (*), Playwright MCP tools
---

# Frontend Master Skill

Unified decision framework for modern frontend development.

**Stack:** Next.js 14+ (App Router) · React 18+ · Tailwind CSS · TypeScript · Framer Motion

## Quick Decision Matrix

```yaml
WHAT DO YOU NEED?
│
├─► UI Components
│   ├─ Basic (buttons, forms, dialogs) → shadcn/ui
│   ├─ SaaS polish (tickers, marquees) → Magic UI [skill: frontend-magic-ui]
│   └─ Dramatic effects (spotlight, 3D) → Aceternity [skill: frontend-aceternity]
│
├─► Animations
│   ├─ Just plays/loops (loaders, feedback) → Lottie [skill: frontend-lottie]
│   └─ Reacts to input (hover, data) → Rive [skill: frontend-rive]
│
├─► Assets
│   ├─ Icons → Iconify/Lucide [skill: frontend-iconify]
│   ├─ Avatars → DiceBear (FREE) [skill: frontend-image-generation]
│   ├─ Photos → Unsplash (FREE) [skill: frontend-image-generation]
│   └─ Illustrations → unDraw (FREE) [skill: frontend-image-generation]
│
├─► Theming
│   ├─ Colors/palette → Color System [skill: frontend-color-system]
│   └─ Typography → Google Fonts [skill: frontend-google-fonts]
│
└─► Quality
    ├─ Code checks → Debug & Linting [skill: frontend-debug-linting]
    └─ Visual QA → Playwright [skill: frontend-playwright]
```

---

## 1. Project Setup Checklist

```bash
# New Next.js project
npx create-next-app@latest my-app --typescript --tailwind --eslint --app

# Essential dependencies
npm install clsx tailwind-merge framer-motion
npm install -D prettier eslint-config-prettier

# UI foundation
npx shadcn@latest init
npx shadcn@latest add button card input dialog
```

### Recommended Structure

```
src/
├── app/                    # Next.js App Router
│   ├── layout.tsx          # Root layout + fonts
│   ├── page.tsx            # Home page
│   └── (routes)/           # Route groups
├── components/
│   ├── ui/                 # shadcn components
│   ├── magicui/            # Magic UI components
│   └── [feature]/          # Feature components
├── lib/
│   ├── fonts.ts            # Font configuration
│   ├── utils.ts            # cn() helper
│   └── constants.ts        # App constants
├── styles/
│   └── globals.css         # Tailwind + CSS vars
└── public/
    ├── animations/         # .lottie, .riv files
    ├── icons/              # Downloaded SVGs
    └── images/             # Static images
```

---

## 2. Component Selection Guide

### UI Components Decision Tree

```yaml
Need a component?
│
├─► Form element (input, select, checkbox)
│   └─► shadcn/ui — accessible, unstyled base
│
├─► Data display (table, card, list)
│   └─► shadcn/ui — consistent patterns
│
├─► Marketing/Landing page
│   ├─► Stats/numbers → Magic UI: NumberTicker
│   ├─► Logo carousel → Magic UI: Marquee
│   ├─► Feature grid → Magic UI: BentoGrid
│   ├─► Hero spotlight → Aceternity: Spotlight, Aurora
│   ├─► 3D hover cards → Aceternity: 3DCard
│   ├─► Text reveal → Aceternity: TextGenerateEffect
│   └─► Device mockup → Magic UI: Safari, iPhone
│
└─► Interactive element
    ├─► Simple hover/focus → Tailwind transitions
    ├─► Complex entrance → Framer Motion
    └─► State machine → Rive
```

### Animation Decision Tree

```yaml
Animation needed?
│
├─► Does it react to user input?
│   ├─ NO → Lottie (just plays)
│   └─ YES → Does it have multiple states?
│       ├─ Simple hover → CSS/Framer Motion
│       └─ Complex states → Rive
│
├─► What type?
│   ├─ Loading spinner → Lottie
│   ├─ Success/error → Lottie
│   ├─ Empty state illustration → Lottie
│   ├─ Animated toggle/checkbox → Rive
│   ├─ Progress driven by data → Rive
│   └─ Hero background effect → Aceternity
```

**Quick Reference:**
| Need | Solution |
|------|----------|
| Loader spinner | Lottie |
| Success checkmark | Lottie |
| Animated button | Rive |
| Data-driven progress | Rive |
| Hero spotlight | Aceternity |
| Number ticker | Magic UI |

---

## 3. Styling Best Practices

### Tailwind Patterns

```tsx
// ✅ Use cn() for conditional classes
import { cn } from "@/lib/utils"

<button className={cn(
  "px-4 py-2 rounded-md font-medium",
  "bg-primary text-primary-foreground",
  "hover:bg-primary/90 transition-colors",
  disabled && "opacity-50 cursor-not-allowed"
)}>

// ✅ Responsive: mobile-first
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

// ✅ Dark mode with CSS variables
<div className="bg-background text-foreground">

// ❌ Avoid arbitrary values when Tailwind has it
<div className="mt-[16px]">  // Bad
<div className="mt-4">       // Good
```

### Color System Setup

→ See **[frontend-color-system]** for full guide

```css
/* globals.css - shadcn theme structure */
:root {
  --background: 0 0% 100%;
  --foreground: 240 10% 3.9%;
  --primary: 239 84% 67%;
  --primary-foreground: 0 0% 98%;
  /* ... */
}

.dark {
  --background: 240 10% 3.9%;
  --foreground: 0 0% 98%;
  /* ... */
}
```

### Typography Setup

→ See **[frontend-google-fonts]** for font pairings

```tsx
// lib/fonts.ts
import { Inter, Plus_Jakarta_Sans } from 'next/font/google'

export const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
})

export const jakarta = Plus_Jakarta_Sans({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-jakarta',
})

// app/layout.tsx
<html className={`${inter.variable} ${jakarta.variable}`}>

// tailwind.config.ts
fontFamily: {
  sans: ['var(--font-inter)'],
  display: ['var(--font-jakarta)'],
}
```

**Font Pairing Presets:**
| Project Type | Heading | Body |
|--------------|---------|------|
| Modern SaaS | Plus Jakarta Sans | Inter |
| Corporate | Source Sans 3 | Source Serif 4 |
| Editorial | Playfair Display | Lora |
| Dev Tools | Geist | Inter |

---

## 4. Assets Strategy

### Icons

→ See **[frontend-iconify]** for full API

```tsx
// Recommended: @iconify/react with Lucide set
import { Icon } from '@iconify/react'

<Icon icon="lucide:home" className="w-5 h-5" />

// Or download SVGs for performance
curl -o ./public/icons/home.svg "https://api.iconify.design/lucide/home.svg"
```

### Images — FREE FIRST

→ See **[frontend-image-generation]** for all options

```yaml
ALWAYS FREE FIRST:
  Avatars:      DiceBear, Boring Avatars, UI Avatars
  Photos:       Unsplash, Picsum
  Illustrations: unDraw, Storyset
  Backgrounds:  Haikei, Hero Patterns

AI GENERATION ONLY WHEN:
  - Custom branded asset needed
  - No suitable free alternative
  - User explicitly requests
```

```tsx
// Avatar with fallback
const fallback = `https://api.dicebear.com/7.x/lorelei/svg?seed=${name}`
<img src={src || fallback} onError={e => e.target.src = fallback} />

// Placeholder photo
<img src="https://source.unsplash.com/800x600/?technology" />
```

---

## 5. SSR & Hydration Rules

**Critical for Next.js App Router:**

```tsx
// 1. Client components need directive
'use client'

// 2. Browser-only code → useEffect
const [mounted, setMounted] = useState(false)
useEffect(() => setMounted(true), [])
if (!mounted) return <Skeleton />

// 3. Heavy animations → dynamic import
import dynamic from 'next/dynamic'
const Globe = dynamic(() => import('@/components/globe'), { ssr: false })

// 4. Window/document access → check first
if (typeof window !== 'undefined') {
  // browser code
}
```

**Components requiring 'use client':**
- All Aceternity components
- All Magic UI animated components
- Lottie/Rive players
- Anything using useState, useEffect, event handlers

---

## 6. Performance Checklist

```yaml
Images:
  ✓ Use next/image with proper sizing
  ✓ Add priority to LCP images
  ✓ Lazy load below-fold images

Fonts:
  ✓ Use next/font (auto self-hosted)
  ✓ Only 'latin' subset unless needed
  ✓ display: 'swap' always

Animations:
  ✓ Reduce particles on mobile
  ✓ Respect prefers-reduced-motion
  ✓ Pause when not in viewport

Components:
  ✓ Dynamic import heavy components
  ✓ Lazy load below-fold sections
  ✓ Memoize expensive renders
```

```tsx
// Reduced motion check
const prefersReducedMotion = window.matchMedia(
  '(prefers-reduced-motion: reduce)'
).matches

// Viewport visibility
import { useInView } from 'react-intersection-observer'
const { ref, inView } = useInView({ threshold: 0.1 })
useEffect(() => {
  inView ? animation.play() : animation.pause()
}, [inView])
```

---

## 7. Quality Gates

### Before Every Delivery

→ See **[frontend-debug-linting]** and **[frontend-playwright]**

```yaml
CODE CHECKS (required):
  npm run lint        → 0 errors
  npm run typecheck   → 0 errors
  npm run format      → clean

VISUAL QA (required):
  1. npm run dev
  2. browser_navigate → page
  3. browser_take_screenshot → looks correct
  4. browser_console_messages { onlyErrors: true } → EMPTY
  5. browser_resize { width: 375 } → mobile works
```

### Common Issues Quick Fix

```yaml
TypeScript:
  "Type 'X' not assignable to 'Y'" → Fix type or add assertion
  "Object possibly undefined" → Add ?. or ?? fallback

React:
  "Missing useEffect dependencies" → Add deps or useCallback
  "Each child needs unique key" → Add key={item.id}

Hydration:
  "Text content mismatch" → 'use client' + mounted check
  "Hydration failed" → dynamic import with ssr: false

Console:
  "Failed to fetch" → Check API/network
  "Cannot read property of undefined" → Add loading state
```

---

## 8. Common Patterns

### Responsive Container

```tsx
<div className="container mx-auto px-4 sm:px-6 lg:px-8 max-w-7xl">
  {children}
</div>
```

### Section Spacing

```tsx
<section className="py-16 md:py-24 lg:py-32">
  <div className="container">
    <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold mb-8">
      Title
    </h2>
  </div>
</section>
```

### Card Grid

```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  {items.map(item => (
    <Card key={item.id}>
      <CardHeader>
        <CardTitle>{item.title}</CardTitle>
      </CardHeader>
      <CardContent>{item.content}</CardContent>
    </Card>
  ))}
</div>
```

### Loading State

```tsx
function Component() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  if (loading) return <Skeleton className="h-32 w-full" />
  if (!data) return <EmptyState />
  return <Content data={data} />
}
```

---

## 9. Skill Reference Map

| Task | Primary Skill | When to Use |
|------|---------------|-------------|
| Dramatic hero effects | frontend-aceternity | Spotlight, aurora, 3D cards |
| Color palette/theme | frontend-color-system | Brand colors, dark mode |
| Linting & debugging | frontend-debug-linting | Before every delivery |
| Typography | frontend-google-fonts | Font setup, pairings |
| Icons | frontend-iconify | Search & integrate icons |
| Images & avatars | frontend-image-generation | FREE assets first |
| Simple animations | frontend-lottie | Loaders, feedback |
| SaaS components | frontend-magic-ui | Tickers, marquees, mockups |
| Visual testing | frontend-playwright | Screenshot verification |
| Interactive animations | frontend-rive | State-driven animations |

---

## 10. Quick Start Templates

### Landing Page Hero

```tsx
'use client'
import { Spotlight } from '@/components/ui/spotlight'
import { FlipWords } from '@/components/ui/flip-words'

export function Hero() {
  return (
    <section className="relative h-screen bg-black overflow-hidden">
      <Spotlight className="absolute -top-40 left-0" fill="white" />
      <div className="relative z-10 container flex flex-col items-center justify-center h-full text-center">
        <h1 className="text-4xl md:text-6xl font-bold text-white mb-6">
          Build <FlipWords words={["faster", "better", "smarter"]} /> apps
        </h1>
        <p className="text-xl text-gray-400 max-w-2xl mb-8">
          Description text here
        </p>
        <Button size="lg">Get Started</Button>
      </div>
    </section>
  )
}
```

### Stats Section

```tsx
'use client'
import { NumberTicker } from '@/components/magicui/number-ticker'

const stats = [
  { value: 10000, label: 'Users', suffix: '+' },
  { value: 99.9, label: 'Uptime', suffix: '%' },
  { value: 50, label: 'Countries', suffix: '+' },
]

export function Stats() {
  return (
    <section className="py-16 bg-muted">
      <div className="container grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
        {stats.map(stat => (
          <div key={stat.label}>
            <div className="text-4xl font-bold">
              <NumberTicker value={stat.value} />
              {stat.suffix}
            </div>
            <div className="text-muted-foreground">{stat.label}</div>
          </div>
        ))}
      </div>
    </section>
  )
}
```

---

## External Resources

- **shadcn/ui:** https://ui.shadcn.com
- **Tailwind CSS:** https://tailwindcss.com/docs
- **Next.js:** https://nextjs.org/docs
- **Framer Motion:** https://www.framer.com/motion
- **Magic UI:** https://magicui.design
- **Aceternity:** https://ui.aceternity.com
- **LottieFiles:** https://lottiefiles.com
- **Rive:** https://rive.app

For latest API of any library → use context7 skill
