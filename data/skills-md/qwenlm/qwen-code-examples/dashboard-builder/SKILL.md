---
name: dashboard-builder
description: Build full-stack dashboard applications using React/Next.js + shadcn/ui + Tailwind CSS + Recharts + Express with customizable data sources. Use when creating data visualization dashboards, business intelligence interfaces, monitoring systems, KPI displays, analytics platforms, or any project requiring data visualization with modern UI components and dynamic effects.
---

# Dashboard Builder

Build professional data visualization dashboards with modern UI, rich visualizations, and dynamic effects.

## Tech Stack

- **Frontend**: Next.js 14+ (App Router) + React 18+
- **UI Components**: shadcn/ui + Tailwind CSS
- **Charts**: Recharts
- **Animations**: Framer Motion
- **Backend**: Express.js
- **Data Sources**: Configurable APIs, databases, or static data

## Design Requirements

### Visual Style (Professional PC Dashboard)
- **Dark theme** with subtle gradients (not flashy)
- **Clean card design** with soft shadows and borders
- **Professional color palette**:
  - Background: slate-900 (#0f172a) to slate-950 (#020617)
  - Cards: slate-800/50 with subtle border
  - Success: emerald-500 (#10b981)
  - Danger: rose-500 (#f43f5e)
  - Accent: blue-500 (#3b82f6)
- **Large typography** optimized for big screens (4K, ultra-wide)
- **Grid-based layout** with clear visual hierarchy

### Animation Requirements
- **Entrance animations**: Subtle fade in + slide up on page load
- **Scroll-triggered animations**: Cards animate when scrolling into view
- **Number counting animation**: Values animate smoothly
- **Progress bar animation**: Bars fill with easing
- **Hover effects**: Cards lift slightly with shadow
- **Live data pulse**: Subtle indicator when data updates

## Project Structure

```
project-root/
├── app/
│   ├── layout.tsx
│   ├── page.tsx              # Landing/input page
│   └── dashboard/
│       └── page.tsx          # Results dashboard
├── components/
│   ├── ui/                   # shadcn components
│   ├── charts/
│   │   ├── LineChart.tsx
│   │   ├── BarChart.tsx
│   │   ├── AreaChart.tsx
│   │   └── PieChart.tsx
│   ├── dashboard/
│   │   ├── KPICard.tsx
│   │   ├── DataCard.tsx
│   │   ├── StatsPanel.tsx
│   │   └── DataTable.tsx
│   └── effects/
│       └── AnimatedNumber.tsx
├── lib/
│   ├── api.ts
│   ├── utils.ts
│   └── animations.ts
├── server/
│   ├── index.ts
│   ├── routes/
│   │   └── data.ts
│   └── services/
│       └── dataService.ts
└── styles/
    └── globals.css
```

## PC Big Screen Layout

### 4K Dashboard Grid (3840x2160)

```tsx
export default function DashboardPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-900 to-slate-950 p-6">
      {/* Header */}
      <header className="flex items-center justify-between mb-8">
        <h1 className="text-4xl font-bold text-white">Dashboard</h1>
        <div className="flex items-center gap-4">
          <LiveIndicator />
          <span className="text-slate-400 text-lg">Last updated: {time}</span>
        </div>
      </header>

      {/* KPI Row */}
      <div className="grid grid-cols-4 gap-6 mb-8">
        <KPICard title="Metric 1" value={125000} prefix="$" trend={5.2} />
        <KPICard title="Metric 2" value={2340} prefix="$" trend={1.8} />
        <KPICard title="Metric 3" value={18.5} suffix="%" trend={0} />
        <KPICard title="Metric 4" value={12} trend={0} />
      </div>

      {/* Main Content */}
      <div className="grid grid-cols-12 gap-6">
        {/* Main Chart - 8 columns */}
        <div className="col-span-8">
          <Card className="h-[500px]">
            <CardHeader>
              <CardTitle>Main Metric Trend</CardTitle>
            </CardHeader>
            <CardContent>
              <LineChart data={metricData} />
            </CardContent>
          </Card>
        </div>

        {/* Side Panel - 4 columns */}
        <div className="col-span-4 space-y-6">
          <Card>
            <CardHeader><CardTitle>Top Items</CardTitle></CardHeader>
            <CardContent>
              <DataTable data={topItems} />
            </CardContent>
          </Card>
          <Card>
            <CardHeader><CardTitle>Comparison</CardTitle></CardHeader>
            <CardContent>
              <PieChart data={comparisonData} />
            </CardContent>
          </Card>
        </div>

        {/* Timeline Row - Full width */}
        <div className="col-span-12">
          <h2 className="text-2xl font-semibold text-white mb-4">Trend Analysis</h2>
          <div className="grid grid-cols-4 gap-6">
            {timelineData.map(item => (
              <DataCard key={item.period} {...item} />
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
```

## Core Components

### KPI Card

```tsx
import { Card, CardContent } from "@/components/ui/card"
import { TrendingUp, TrendingDown, Minus } from "lucide-react"
import { AnimatedNumber } from "./AnimatedNumber"

interface KPICardProps {
  title: string
  value: number
  prefix?: string
  suffix?: string
  trend?: number
}

export function KPICard({ title, value, prefix = '', suffix = '', trend = 0 }: KPICardProps) {
  return (
    <Card className="bg-slate-800/50 border-slate-700/50">
      <CardContent className="pt-6">
        <p className="text-slate-400 text-sm font-medium mb-2">{title}</p>
        <div className="flex items-end justify-between">
          <span className="text-3xl font-bold text-white">
            {prefix}<AnimatedNumber value={value} />{suffix}
          </span>
          {trend !== 0 && (
            <span className={cn(
              "flex items-center text-sm font-medium",
              trend > 0 ? "text-emerald-500" : "text-rose-500"
            )}>
              {trend > 0 ? <TrendingUp className="w-4 h-4 mr-1" /> : <TrendingDown className="w-4 h-4 mr-1" />}
              {Math.abs(trend)}%
            </span>
          )}
        </div>
      </CardContent>
    </Card>
  )
}
```

### Data Card (Generic Timeline Card)

```tsx
'use client'
import { motion } from 'framer-motion'
import { useInView } from 'framer-motion'
import { useRef } from 'react'
import { Card, CardContent } from "@/components/ui/card"

interface DataCardProps {
  period: string
  currentValue: number
  baselineValue: number
  percentChange: number
  description: string
}

export function DataCard({ period, currentValue, baselineValue, percentChange, description }: DataCardProps) {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, margin: "-50px" })
  const isPositive = percentChange >= 0

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 30 }}
      animate={isInView ? { opacity: 1, y: 0 } : {}}
      transition={{ duration: 0.5, ease: "easeOut" }}
    >
      <Card className="bg-slate-800/50 border-slate-700/50 overflow-hidden">
        <div className={cn(
          "h-1",
          isPositive ? "bg-emerald-500" : "bg-rose-500"
        )} />
        <CardContent className="pt-6">
          <div className="flex items-baseline gap-2 mb-4">
            <span className="text-4xl font-bold text-white">{period}</span>
          </div>

          <div className="space-y-3">
            <div className="flex justify-between text-sm">
              <span className="text-slate-400">Baseline Value</span>
              <span className="text-slate-300">{baselineValue}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-slate-400">Current Value</span>
              <span className="text-white font-medium">{currentValue}</span>
            </div>

            {/* Change percentage */}
            <div className={cn(
              "text-2xl font-bold text-center py-3 rounded-lg",
              isPositive ? "text-emerald-500 bg-emerald-500/10" : "text-rose-500 bg-rose-500/10"
            )}>
              {isPositive ? '+' : ''}{percentChange.toFixed(2)}%
            </div>

            {/* Progress bar */}
            <div className="h-1.5 bg-slate-700 rounded-full overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={isInView ? { width: `${Math.min(Math.abs(percentChange), 100)}%` } : {}}
                transition={{ duration: 1, ease: "easeOut", delay: 0.3 }}
                className={cn(
                  "h-full rounded-full",
                  isPositive ? "bg-emerald-500" : "bg-rose-500"
                )}
              />
            </div>

            <p className="text-slate-400 text-sm">{description}</p>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  )
}
```

### Animated Number

```tsx
'use client'
import { useEffect, useState } from 'react'
import { animate } from 'framer-motion'

interface AnimatedNumberProps {
  value: number
  decimals?: number
  duration?: number
}

export function AnimatedNumber({ value, decimals = 2, duration = 1 }: AnimatedNumberProps) {
  const [display, setDisplay] = useState(0)

  useEffect(() => {
    const controls = animate(display, value, {
      duration,
      ease: "easeOut",
      onUpdate: (v) => setDisplay(v)
    })
    return () => controls.stop()
  }, [value, duration])

  return <>{display.toFixed(decimals)}</>
}
```

### Live Indicator

```tsx
export function LiveIndicator() {
  return (
    <div className="flex items-center gap-2">
      <span className="relative flex h-3 w-3">
        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
        <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500" />
      </span>
      <span className="text-emerald-500 text-sm font-medium">LIVE</span>
    </div>
  )
}
```

## Automation Scripts

### Automatic Setup and Run

To simplify the development setup process, we provide an automated script that will:

1. Create a new Next.js project with all required dependencies
2. Install shadcn/ui components
3. Set up sample dashboard components
4. Start the development server

Run the setup script with:

```bash
./setup-and-run.sh
```

The script will prompt you for a project name and automatically handle all setup steps, then start the development server at `http://localhost:3000`.

### Manual Setup

If you prefer manual setup, follow these steps:

1. Create a new Next.js app:
   ```bash
   npx create-next-app@latest my-dashboard --typescript --tailwind --eslint
   ```

2. Install required dependencies:
   ```bash
   cd my-dashboard
   npm install shadcn-ui recharts framer-motion lucide-react
   ```

3. Initialize and add shadcn/ui components:
   ```bash
   npx shadcn-ui@latest init
   npx shadcn-ui@latest add card button badge table scroll-area alert
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

## CSS Styles

```css
/* globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --background: 222.2 84% 4.9%;
  --foreground: 210 40% 98%;
  --card: 222.2 84% 4.9%;
  --card-foreground: 210 40% 98%;
  --primary: 217.2 91.2% 59.8%;
  --primary-foreground: 222.2 47.4% 11.2%;
}

/* Big screen typography */
@media (min-width: 2560px) {
  html { font-size: 18px; }
}

@media (min-width: 3840px) {
  html { font-size: 20px; }
}

/* Smooth scrolling */
html {
  scroll-behavior: smooth;
}

/* Card hover effect */
.card-hover {
  @apply transition-all duration-300;
}

.card-hover:hover {
  @apply -translate-y-1 shadow-lg shadow-slate-900/50;
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Auto-Refresh Hook

```tsx
'use client'
import { useEffect, useState, useCallback } from 'react'

export function useLiveData<T>(
  fetcher: () => Promise<T>,
  interval = 60000
) {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [isRefreshing, setIsRefreshing] = useState(false)
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null)

  const refresh = useCallback(async () => {
    setIsRefreshing(true)
    try {
      const result = await fetcher()
      setData(result)
      setLastUpdated(new Date())
    } finally {
      setLoading(false)
      setTimeout(() => setIsRefreshing(false), 300)
    }
  }, [fetcher])

  useEffect(() => {
    refresh()
    const timer = setInterval(refresh, interval)
    return () => clearInterval(timer)
  }, [refresh, interval])

  return { data, loading, isRefreshing, lastUpdated, refresh }
}
```

## Resources

- [references/data-api-integration.md](references/data-api-integration.md) - API endpoints, data handling, error handling
- [references/recharts-patterns.md](references/recharts-patterns.md) - Chart patterns and customization
- [references/big-screen-ui.md](references/big-screen-ui.md) - Big screen layout guidelines
- [QUICKSTART.md](QUICKSTART.md) - Quick start template and initialization guide
- [DATA_INTEGRATION.md](DATA_INTEGRATION.md) - Detailed data integration steps and examples
- [ADDITIONAL_COMPONENTS.md](ADDITIONAL_COMPONENTS.md) - Additional components for large screen dashboards
