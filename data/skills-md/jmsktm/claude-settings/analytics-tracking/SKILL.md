---
name: Analytics Tracking
slug: analytics-tracking
description: Expert guide for tracking user analytics, events, conversions, A/B testing, and data-driven insights. Use when implementing analytics, tracking user behavior, or optimizing conversions.
category: observability
complexity: moderate
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "add analytics"
  - "track events"
  - "implement tracking"
  - "conversion tracking"
  - "A/B testing"
  - "user behavior"
  - "analytics setup"
  - "page views"
  - "funnel analysis"
tags:
  - analytics
  - tracking
  - events
  - conversions
  - A/B testing
  - metrics
  - user-behavior
  - posthog
  - google-analytics
---

# Analytics & Tracking Skill

Comprehensive analytics and event tracking implementation for Next.js applications. From basic page views to complex conversion funnels, this skill covers everything needed for data-driven decisions including provider integration, custom event systems, A/B testing, and privacy compliance.

Track user interactions, measure conversion funnels, run experiments, and gain actionable insights into user behavior. Integrate with popular analytics platforms like Vercel Analytics, PostHog, Mixpanel, and Google Analytics while maintaining privacy compliance.

## Core Workflows

### Workflow 1: Google Analytics 4 (GA4) Setup
**Purpose:** Implement Google Analytics for comprehensive web analytics

**Steps:**
1. Install @next/third-parties package
2. Add GoogleAnalytics component to layout
3. Implement custom event tracking
4. Set up conversion goals

**Implementation:**
```typescript
// Install
// npm install @next/third-parties

// app/layout.tsx
import { GoogleAnalytics } from '@next/third-parties/google'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <GoogleAnalytics gaId="G-XXXXXXXXXX" />
      </body>
    </html>
  )
}

// Track Events
'use client'

export function TrackableButton() {
  const handleClick = () => {
    window.gtag('event', 'button_click', {
      event_category: 'engagement',
      event_label: 'cta_button',
      value: 1
    })
  }

  return <button onClick={handleClick}>Click Me</button>
}
```

### Workflow 2: Vercel Analytics Integration
**Purpose:** Zero-config analytics for Vercel deployments

**Steps:**
1. Install @vercel/analytics
2. Add Analytics component
3. Track custom events

**Implementation:**
```typescript
// npm install @vercel/analytics

// app/layout.tsx
import { Analytics } from '@vercel/analytics/react'
import { SpeedInsights } from '@vercel/speed-insights/next'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
        <SpeedInsights />
      </body>
    </html>
  )
}

// Track Custom Events
import { track } from '@vercel/analytics'

track('Purchase', { amount: 99.99, currency: 'USD' })
```

### Workflow 3: PostHog (Open Source Analytics)
**Purpose:** Full-featured product analytics with feature flags and session replay

**Steps:**
1. Install posthog-js
2. Create PostHog provider
3. Implement event tracking
4. Set up feature flags

**Implementation:**
```typescript
// lib/posthog.ts
import posthog from 'posthog-js'

export function initPostHog() {
  if (typeof window !== 'undefined') {
    posthog.init(process.env.NEXT_PUBLIC_POSTHOG_KEY!, {
      api_host: process.env.NEXT_PUBLIC_POSTHOG_HOST || 'https://app.posthog.com',
      loaded: (posthog) => {
        if (process.env.NODE_ENV === 'development') posthog.debug()
      }
    })
  }
}

// app/providers.tsx
'use client'
import { useEffect } from 'react'
import { initPostHog } from '@/lib/posthog'

export function Providers({ children }) {
  useEffect(() => {
    initPostHog()
  }, [])

  return <>{children}</>
}

// Track Events
import posthog from 'posthog-js'

posthog.capture('user_signed_up', {
  plan: 'pro',
  source: 'landing_page'
})
```

### Workflow 4: Custom Analytics System
**Purpose:** Build a unified analytics abstraction layer

**Implementation:**
```typescript
// hooks/use-analytics.ts
'use client'
import { useCallback } from 'react'

type EventProperties = Record<string, any>

export function useAnalytics() {
  const track = useCallback((eventName: string, properties?: EventProperties) => {
    if (typeof window !== 'undefined') {
      // Google Analytics
      window.gtag?.('event', eventName, properties)

      // PostHog
      window.posthog?.capture(eventName, properties)

      // Custom backend
      fetch('/api/analytics/track', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          event: eventName,
          properties,
          timestamp: new Date().toISOString(),
          url: window.location.href,
          referrer: document.referrer,
        })
      }).catch(() => {})
    }
  }, [])

  const identify = useCallback((userId: string, traits?: EventProperties) => {
    if (typeof window !== 'undefined') {
      window.gtag?.('config', 'GA_MEASUREMENT_ID', { user_id: userId })
      window.posthog?.identify(userId, traits)
    }
  }, [])

  const page = useCallback((pageName: string, properties?: EventProperties) => {
    if (typeof window !== 'undefined') {
      window.gtag?.('event', 'page_view', {
        page_title: pageName,
        ...properties
      })
      window.posthog?.capture('$pageview', properties)
    }
  }, [])

  return { track, identify, page }
}
```

### Workflow 5: Conversion Funnel Tracking
**Purpose:** Track and analyze multi-step conversion funnels

**Implementation:**
```typescript
// lib/funnel.ts
type FunnelStep =
  | 'landing'
  | 'signup'
  | 'onboarding'
  | 'first_action'
  | 'activation'

export class FunnelTracker {
  private steps: FunnelStep[] = []

  trackStep(step: FunnelStep, properties?: Record<string, any>) {
    this.steps.push(step)

    track('Funnel Step Completed', {
      step,
      step_number: this.steps.length,
      funnel_id: 'user_activation',
      ...properties
    })

    // Track drop-off if user hasn't progressed
    setTimeout(() => {
      if (this.steps[this.steps.length - 1] === step) {
        track('Funnel Drop Off', {
          at_step: step,
          steps_completed: this.steps.length
        })
      }
    }, 60000)
  }
}

// Usage
const funnel = new FunnelTracker()
funnel.trackStep('landing')
funnel.trackStep('signup', { method: 'email' })
funnel.trackStep('onboarding', { completed_steps: 3 })
```

### Workflow 6: A/B Testing Implementation
**Purpose:** Run controlled experiments with statistical significance

**Implementation:**
```typescript
// lib/ab-test.ts
'use client'
import { useState, useEffect } from 'react'

type Variant = 'A' | 'B'

export function useABTest(testName: string): Variant {
  const [variant, setVariant] = useState<Variant>('A')

  useEffect(() => {
    const key = `ab_test_${testName}`
    let userVariant = localStorage.getItem(key) as Variant

    if (!userVariant) {
      userVariant = Math.random() > 0.5 ? 'A' : 'B'
      localStorage.setItem(key, userVariant)

      track('AB Test Assigned', {
        test_name: testName,
        variant: userVariant
      })
    }

    setVariant(userVariant)
  }, [testName])

  return variant
}

// Usage
function PricingPage() {
  const variant = useABTest('pricing_layout')

  if (variant === 'A') {
    return <PricingLayoutA />
  }
  return <PricingLayoutB />
}

// Advanced A/B Testing with PostHog
import { useFeatureFlagEnabled } from 'posthog-js/react'

export function PricingPage() {
  const showNewPricing = useFeatureFlagEnabled('new-pricing-layout')

  if (showNewPricing) {
    return <NewPricingLayout />
  }
  return <OldPricingLayout />
}
```

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Basic setup | "add analytics to my app" |
| Track event | "track [event name]" |
| Page views | "track page views" |
| Conversions | "set up conversion tracking" |
| A/B testing | "implement A/B test" |
| Feature flags | "add feature flags" |
| User identification | "identify users" |
| Funnel analysis | "track conversion funnel" |

## Common Events to Track

**User Authentication:**
```typescript
track('User Signed Up', { method: 'email' })
track('User Logged In', { method: 'google' })
track('User Logged Out')
```

**Engagement:**
```typescript
track('Button Clicked', { button_id: 'cta', location: 'hero' })
track('Link Clicked', { url: '/pricing', text: 'See Pricing' })
track('Video Played', { video_id: 'intro', duration: 120 })
track('Form Submitted', { form_id: 'contact', success: true })
```

**E-commerce:**
```typescript
track('Product Viewed', { product_id: '123', name: 'Pro Plan' })
track('Product Added to Cart', { product_id: '123', quantity: 1 })
track('Checkout Started', { cart_total: 99.99 })
track('Order Completed', {
  order_id: 'ORD-123',
  total: 99.99,
  items: 3
})
```

## Privacy & Consent

```typescript
// components/cookie-consent.tsx
'use client'
import { useState, useEffect } from 'react'

export function CookieConsent() {
  const [showBanner, setShowBanner] = useState(false)

  useEffect(() => {
    const consent = localStorage.getItem('cookie_consent')
    if (!consent) {
      setShowBanner(true)
    } else if (consent === 'accepted') {
      initAnalytics()
    }
  }, [])

  const accept = () => {
    localStorage.setItem('cookie_consent', 'accepted')
    setShowBanner(false)
    initAnalytics()
  }

  const decline = () => {
    localStorage.setItem('cookie_consent', 'declined')
    setShowBanner(false)
  }

  if (!showBanner) return null

  return (
    <div className="fixed bottom-0 left-0 right-0 bg-gray-900 text-white p-4">
      <p>We use cookies to improve your experience.</p>
      <button onClick={accept}>Accept</button>
      <button onClick={decline}>Decline</button>
    </div>
  )
}
```

## Best Practices

- **Privacy First:** Respect user consent and privacy regulations (GDPR, CCPA)
- **Consistent Naming:** Use snake_case for event names
- **Rich Context:** Include relevant properties with every event
- **User Identification:** Link anonymous and authenticated sessions
- **Event Taxonomy:** Document your event naming conventions
- **Sampling:** Use sampling for high-volume events
- **Testing:** Test tracking in development before production
- **Data Quality:** Validate events before sending
- **Performance:** Batch events and avoid blocking the main thread
- **Documentation:** Maintain an event dictionary

## Dependencies

```bash
# Vercel Analytics
npm install @vercel/analytics @vercel/speed-insights

# Google Analytics
npm install @next/third-parties

# PostHog
npm install posthog-js

# Mixpanel
npm install mixpanel-browser
```

## Error Handling

- **Network Failures:** Queue events locally and retry
- **Blocked Trackers:** Gracefully degrade without breaking the app
- **Invalid Events:** Validate event structure before sending
- **Rate Limits:** Implement client-side rate limiting
- **Missing User ID:** Use anonymous IDs until identification

## Performance Tips

- Use `requestIdleCallback` for non-critical tracking
- Batch multiple events into single requests
- Lazy load analytics scripts
- Use beacon API for page unload events
- Avoid tracking on every keystroke
- Sample high-frequency events

## When to Use This Skill

Invoke this skill when:
- Setting up analytics tracking
- Implementing conversion tracking
- Creating A/B tests
- Tracking user behavior
- Setting up funnels
- Implementing GDPR compliance
- Debugging analytics issues
- Optimizing conversions
- Creating analytics dashboards
- Tracking custom events
