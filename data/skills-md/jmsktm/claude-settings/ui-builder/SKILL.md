---
name: ui-builder
description: Expert guide for building beautiful, responsive UI with React, Tailwind CSS, Shadcn/ui, and modern design patterns. Use when creating components, layouts, animations, or styling.
---

# UI/UX Builder Skill

## Overview

This skill helps you build beautiful, accessible, and responsive user interfaces using modern React patterns, Tailwind CSS, and component libraries like Shadcn/ui.

## Core Principles

### 1. Mobile-First Design
- Start with mobile layout
- Use responsive breakpoints: sm (640px), md (768px), lg (1024px), xl (1280px)
- Test on multiple screen sizes

### 2. Accessibility
- Use semantic HTML
- Add ARIA labels where needed
- Ensure keyboard navigation works
- Maintain color contrast ratios
- Support screen readers

### 3. Performance
- Lazy load heavy components
- Optimize images
- Use CSS animations over JS when possible
- Minimize re-renders

### 4. Consistency
- Use design tokens (colors, spacing, typography)
- Follow established patterns
- Maintain visual hierarchy

## Tailwind CSS Patterns

### Layout

```typescript
// Flex layouts
<div className="flex items-center justify-between gap-4">
  <div>Left</div>
  <div>Right</div>
</div>

// Grid layouts
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  <div>Card 1</div>
  <div>Card 2</div>
  <div>Card 3</div>
</div>

// Container
<div className="container mx-auto px-4 sm:px-6 lg:px-8 max-w-7xl">
  Content
</div>

// Centering
<div className="flex items-center justify-center min-h-screen">
  <div>Centered</div>
</div>
```

### Responsive Design

```typescript
// Mobile first
<div className="text-sm md:text-base lg:text-lg">
  Responsive text
</div>

// Hide/show by breakpoint
<div className="hidden md:block">
  Desktop only
</div>

<div className="block md:hidden">
  Mobile only
</div>

// Responsive padding/margin
<div className="p-4 md:p-6 lg:p-8">
  Responsive padding
</div>
```

### Colors & Themes

```typescript
// Background colors
<div className="bg-white dark:bg-gray-900">
  Content
</div>

// Text colors
<p className="text-gray-900 dark:text-white">
  Text
</p>

// Hover states
<button className="bg-blue-500 hover:bg-blue-600 transition-colors">
  Hover me
</button>

// Focus states
<input className="border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200" />
```

### Spacing

```typescript
// Margin/Padding scale: 0, 1(4px), 2(8px), 4(16px), 6(24px), 8(32px), 12(48px), 16(64px)
<div className="p-4">Padding 16px</div>
<div className="mt-8 mb-4">Margin top 32px, bottom 16px</div>
<div className="space-y-4">Vertical spacing between children</div>
<div className="gap-6">Gap between flex/grid items</div>
```

## Common Component Patterns

### Button

```typescript
// components/ui/button.tsx
import { cn } from '@/lib/utils'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'outline' | 'ghost' | 'destructive'
  size?: 'sm' | 'md' | 'lg'
}

export function Button({
  className,
  variant = 'default',
  size = 'md',
  ...props
}: ButtonProps) {
  return (
    <button
      className={cn(
        'inline-flex items-center justify-center rounded-md font-medium transition-colors',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2',
        'disabled:opacity-50 disabled:pointer-events-none',
        {
          'bg-blue-600 text-white hover:bg-blue-700': variant === 'default',
          'border border-gray-300 bg-white hover:bg-gray-50': variant === 'outline',
          'hover:bg-gray-100': variant === 'ghost',
          'bg-red-600 text-white hover:bg-red-700': variant === 'destructive',
        },
        {
          'h-8 px-3 text-sm': size === 'sm',
          'h-10 px-4': size === 'md',
          'h-12 px-6 text-lg': size === 'lg',
        },
        className
      )}
      {...props}
    />
  )
}
```

### Card

```typescript
// components/ui/card.tsx
export function Card({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    <div className={cn('rounded-lg border bg-white p-6 shadow-sm', className)}>
      {children}
    </div>
  )
}

export function CardHeader({ children }: { children: React.ReactNode }) {
  return <div className="mb-4">{children}</div>
}

export function CardTitle({ children }: { children: React.ReactNode }) {
  return <h3 className="text-lg font-semibold">{children}</h3>
}

export function CardContent({ children }: { children: React.ReactNode }) {
  return <div>{children}</div>
}
```

### Input

```typescript
// components/ui/input.tsx
export function Input({ className, ...props }: React.InputHTMLAttributes<HTMLInputElement>) {
  return (
    <input
      className={cn(
        'flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2',
        'text-sm placeholder:text-gray-400',
        'focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
        'disabled:cursor-not-allowed disabled:opacity-50',
        className
      )}
      {...props}
    />
  )
}
```

### Modal/Dialog

```typescript
'use client'
import { useEffect } from 'react'
import { X } from 'lucide-react'

interface DialogProps {
  open: boolean
  onClose: () => void
  title?: string
  children: React.ReactNode
}

export function Dialog({ open, onClose, title, children }: DialogProps) {
  useEffect(() => {
    if (open) {
      document.body.style.overflow = 'hidden'
    } else {
      document.body.style.overflow = 'unset'
    }
    return () => {
      document.body.style.overflow = 'unset'
    }
  }, [open])

  if (!open) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/50 backdrop-blur-sm"
        onClick={onClose}
      />

      {/* Dialog */}
      <div className="relative z-50 w-full max-w-lg rounded-lg bg-white p-6 shadow-xl">
        {title && (
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-xl font-semibold">{title}</h2>
            <button
              onClick={onClose}
              className="rounded-md p-1 hover:bg-gray-100"
            >
              <X className="h-5 w-5" />
            </button>
          </div>
        )}
        {children}
      </div>
    </div>
  )
}
```

### Dropdown Menu

```typescript
'use client'
import { useState, useRef, useEffect } from 'react'

export function DropdownMenu({ trigger, children }: {
  trigger: React.ReactNode
  children: React.ReactNode
}) {
  const [open, setOpen] = useState(false)
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (ref.current && !ref.current.contains(event.target as Node)) {
        setOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  return (
    <div className="relative" ref={ref}>
      <div onClick={() => setOpen(!open)}>{trigger}</div>
      {open && (
        <div className="absolute right-0 mt-2 w-56 rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5">
          <div className="py-1">{children}</div>
        </div>
      )}
    </div>
  )
}

export function DropdownMenuItem({ children, onClick }: {
  children: React.ReactNode
  onClick?: () => void
}) {
  return (
    <button
      className="block w-full px-4 py-2 text-left text-sm hover:bg-gray-100"
      onClick={onClick}
    >
      {children}
    </button>
  )
}
```

### Form

```typescript
// components/forms/contact-form.tsx
'use client'
import { useState } from 'react'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'

export function ContactForm() {
  const [loading, setLoading] = useState(false)
  const [errors, setErrors] = useState<Record<string, string>>({})

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    setLoading(true)
    setErrors({})

    const formData = new FormData(e.currentTarget)
    const email = formData.get('email') as string
    const message = formData.get('message') as string

    // Validation
    const newErrors: Record<string, string> = {}
    if (!email) newErrors.email = 'Email is required'
    if (!message) newErrors.message = 'Message is required'

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors)
      setLoading(false)
      return
    }

    try {
      const response = await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, message }),
      })

      if (!response.ok) throw new Error('Failed to send')

      // Success
      e.currentTarget.reset()
      alert('Message sent!')
    } catch (error) {
      setErrors({ submit: 'Failed to send message' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="email" className="block text-sm font-medium mb-1">
          Email
        </label>
        <Input
          id="email"
          name="email"
          type="email"
          placeholder="you@example.com"
        />
        {errors.email && (
          <p className="mt-1 text-sm text-red-600">{errors.email}</p>
        )}
      </div>

      <div>
        <label htmlFor="message" className="block text-sm font-medium mb-1">
          Message
        </label>
        <textarea
          id="message"
          name="message"
          rows={4}
          className="w-full rounded-md border border-gray-300 px-3 py-2"
          placeholder="Your message..."
        />
        {errors.message && (
          <p className="mt-1 text-sm text-red-600">{errors.message}</p>
        )}
      </div>

      {errors.submit && (
        <p className="text-sm text-red-600">{errors.submit}</p>
      )}

      <Button type="submit" disabled={loading}>
        {loading ? 'Sending...' : 'Send Message'}
      </Button>
    </form>
  )
}
```

## Animations

### Tailwind Transitions

```typescript
// Hover effects
<div className="transition-all duration-200 hover:scale-105">
  Hover to scale
</div>

// Opacity fade
<div className="transition-opacity duration-300 opacity-0 hover:opacity-100">
  Fade in
</div>

// Transform
<div className="transition-transform duration-200 hover:translate-x-2">
  Slide on hover
</div>
```

### Framer Motion

```typescript
'use client'
import { motion } from 'framer-motion'

// Fade in
<motion.div
  initial={{ opacity: 0 }}
  animate={{ opacity: 1 }}
  transition={{ duration: 0.5 }}
>
  Fades in
</motion.div>

// Slide in
<motion.div
  initial={{ x: -100, opacity: 0 }}
  animate={{ x: 0, opacity: 1 }}
  transition={{ duration: 0.5 }}
>
  Slides in
</motion.div>

// Stagger children
<motion.div
  initial="hidden"
  animate="visible"
  variants={{
    visible: {
      transition: {
        staggerChildren: 0.1
      }
    }
  }}
>
  {items.map(item => (
    <motion.div
      key={item.id}
      variants={{
        hidden: { opacity: 0, y: 20 },
        visible: { opacity: 1, y: 0 }
      }}
    >
      {item.title}
    </motion.div>
  ))}
</motion.div>
```

## Icons

### Lucide React

```typescript
import { Search, User, Settings, ChevronRight } from 'lucide-react'

// Basic usage
<Search className="h-5 w-5" />

// With color
<User className="h-5 w-5 text-blue-600" />

// In button
<button className="flex items-center gap-2">
  <Settings className="h-4 w-4" />
  Settings
</button>
```

## Loading States

### Skeleton

```typescript
export function Skeleton({ className }: { className?: string }) {
  return (
    <div className={cn('animate-pulse rounded-md bg-gray-200', className)} />
  )
}

// Usage
<div className="space-y-4">
  <Skeleton className="h-12 w-full" />
  <Skeleton className="h-12 w-full" />
  <Skeleton className="h-12 w-3/4" />
</div>
```

### Spinner

```typescript
export function Spinner({ className }: { className?: string }) {
  return (
    <div
      className={cn(
        'animate-spin rounded-full border-2 border-gray-300 border-t-blue-600',
        'h-8 w-8',
        className
      )}
    />
  )
}
```

## Dark Mode

### Setup

```typescript
// app/providers.tsx
'use client'
import { ThemeProvider } from 'next-themes'

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
      {children}
    </ThemeProvider>
  )
}

// app/layout.tsx
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  )
}
```

### Theme Toggle

```typescript
'use client'
import { useTheme } from 'next-themes'
import { Moon, Sun } from 'lucide-react'

export function ThemeToggle() {
  const { theme, setTheme } = useTheme()

  return (
    <button
      onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
      className="rounded-md p-2 hover:bg-gray-100 dark:hover:bg-gray-800"
    >
      <Sun className="h-5 w-5 dark:hidden" />
      <Moon className="hidden h-5 w-5 dark:block" />
    </button>
  )
}
```

### Dark Mode Styles

```typescript
// Tailwind dark mode
<div className="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
  Dark mode aware
</div>

// tailwind.config.js
module.exports = {
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
      }
    }
  }
}
```

## Best Practices

### Accessibility Checklist
- [ ] Use semantic HTML (header, nav, main, footer, article, section)
- [ ] Add alt text to images
- [ ] Ensure sufficient color contrast (4.5:1 for normal text)
- [ ] Support keyboard navigation (tab, enter, escape)
- [ ] Add ARIA labels where needed
- [ ] Use focus-visible for keyboard focus
- [ ] Test with screen reader

### Performance Checklist
- [ ] Use next/image for images
- [ ] Lazy load components not in viewport
- [ ] Minimize client-side JavaScript
- [ ] Use CSS animations over JS
- [ ] Implement loading skeletons
- [ ] Optimize font loading
- [ ] Use proper image formats (WebP, AVIF)

### Responsive Design Checklist
- [ ] Design mobile-first
- [ ] Test on multiple screen sizes
- [ ] Use responsive images
- [ ] Implement touch-friendly tap targets (44x44px minimum)
- [ ] Test landscape and portrait
- [ ] Handle safe areas on mobile
- [ ] Consider foldable devices

## Utility Function

```typescript
// lib/utils.ts
import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

## Common Layouts

### Dashboard Layout

```typescript
export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-screen">
      {/* Sidebar */}
      <aside className="w-64 border-r bg-gray-50">
        <nav className="p-4">Sidebar</nav>
      </aside>

      {/* Main content */}
      <div className="flex-1 overflow-auto">
        <header className="border-b bg-white px-6 py-4">
          Header
        </header>
        <main className="p-6">{children}</main>
      </div>
    </div>
  )
}
```

### Landing Page Hero

```typescript
export function Hero() {
  return (
    <section className="flex min-h-screen items-center justify-center bg-gradient-to-b from-blue-50 to-white">
      <div className="container px-4 text-center">
        <h1 className="mb-6 text-5xl font-bold tracking-tight md:text-6xl lg:text-7xl">
          Your Amazing Product
        </h1>
        <p className="mx-auto mb-8 max-w-2xl text-lg text-gray-600 md:text-xl">
          A compelling description that explains what your product does
        </p>
        <div className="flex flex-col gap-4 sm:flex-row sm:justify-center">
          <Button size="lg">Get Started</Button>
          <Button size="lg" variant="outline">Learn More</Button>
        </div>
      </div>
    </section>
  )
}
```

## When to Use This Skill

Invoke this skill when:
- Building new UI components
- Creating layouts and page structures
- Implementing responsive design
- Adding animations and transitions
- Working with forms and inputs
- Implementing dark mode
- Ensuring accessibility
- Optimizing UI performance
- Creating loading states
- Building navigation components
