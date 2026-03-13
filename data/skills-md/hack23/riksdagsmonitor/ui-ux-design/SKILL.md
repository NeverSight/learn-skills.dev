---
name: ui-ux-design
description: User experience design, usability testing, information architecture, accessibility (WCAG 2.1 AA), mobile-first design for political transparency platforms
license: Apache-2.0
---

# UI/UX Design Skill

## Purpose

Comprehensive user experience and interface design guidance for Riksdagsmonitor, ensuring intuitive, accessible, and engaging experiences for diverse user groups across all 14 language versions.

## Core Principles

### 1. 👥 User-Centered Design
- **User Research**: Understand needs of journalists, researchers, citizens, policymakers
- **Personas**: Design for specific user archetypes
- **User Journey Mapping**: Optimize paths to key tasks
- **Iterative Testing**: Continuous usability testing, refinement

### 2. ♿ Accessibility First (WCAG 2.1 AA)
- **Perceivable**: All content accessible via multiple senses
- **Operable**: Interface navigable by keyboard, assistive tech
- **Understandable**: Clear language, predictable behavior
- **Robust**: Compatible with assistive technologies

### 3. 📱 Mobile-First Responsive
- **Mobile Priority**: Design for smallest screens first (320px+)
- **Progressive Enhancement**: Add features for larger screens
- **Touch-Friendly**: 44x44px minimum touch targets
- **Performance**: Fast load times on mobile networks

### 4. 🎨 Design System Consistency
- **Cyberpunk Theme**: Cyan, magenta, yellow on dark backgrounds
- **Component Library**: Reusable UI patterns
- **Typography Hierarchy**: Clear information structure
- **Visual Identity**: Consistent brand across all touchpoints

## User Research

### Primary User Personas

#### 1. 📰 Investigative Journalist (Sara)
**Demographics**: 35, Svenska Dagbladet, Stockholm
**Goals**:
- Find stories quickly (voting anomalies, committee conflicts)
- Export data for analysis
- Track specific MPs, committees over time

**Pain Points**:
- Too much data, hard to filter
- No real-time alerts
- Difficult to compare across time periods

**Design Priorities**:
- Advanced filtering, search
- Custom dashboards, saved views
- Data export (CSV, JSON)
- Alert notifications

#### 2. 🎓 Political Science Researcher (Erik)
**Demographics**: 42, Uppsala University, researcher
**Goals**:
- Access historical data (50+ years)
- Validate hypotheses with statistical analysis
- Replicate published studies

**Pain Points**:
- Data quality concerns
- Methodology transparency needed
- API documentation sparse

**Design Priorities**:
- Methodology documentation visible
- API access, rate limits clear
- Citation guidelines
- Downloadable datasets

#### 3. 👥 Engaged Citizen (Anna)
**Demographics**: 28, Gothenburg, first-time voter
**Goals**:
- Understand how Parliament works
- Track local MP's voting record
- Learn about political parties

**Pain Points**:
- Too complex, overwhelming
- Jargon, political terminology
- No onboarding, help

**Design Priorities**:
- Simplified onboarding flow
- Glossary, tooltips
- Educational content
- Visual hierarchy (reduce clutter)

#### 4. 🏢 Corporate Affairs Manager (Johan)
**Demographics**: 45, multinational corporation, lobbyist
**Goals**:
- Monitor legislation affecting business
- Track committee discussions
- Assess political risk

**Pain Points**:
- No legislative alerts
- Hard to map stakeholders
- Competitive intelligence gaps

**Design Priorities**:
- Custom alerts (keywords, topics)
- Stakeholder mapping tools
- Competitive benchmarking
- White-label option

## Information Architecture

### Site Structure
```
Riksdagsmonitor (Home)
│
├── 📊 Dashboards
│   ├── Voting Discipline
│   ├── Committee Effectiveness
│   ├── Coalition Alignment
│   ├── Party Comparison
│   ├── Election Forecasting
│   ├── Risk Assessment
│   └── Ministry Performance
│
├── 👥 MPs (Ledamöter)
│   ├── Search/Filter
│   ├── Individual Profiles
│   └── Comparison Tool
│
├── 🗳️ Votes (Voteringar)
│   ├── Recent Votes
│   ├── Historical Trends
│   └── Party Positions
│
├── 📋 Committees (Utskott)
│   ├── Committee Overview
│   ├── Effectiveness Metrics
│   └── Member Lists
│
├── 📰 News & Analysis
│   ├── Latest Updates
│   ├── Weekly Reports
│   └── Quarterly Reviews
│
├── 📚 About
│   ├── Methodology
│   ├── Data Sources
│   ├── Privacy Policy
│   └── Contact
│
└── 🔗 Resources
    ├── API Documentation
    ├── Glossary
    └── User Guide
```

### Navigation Patterns

#### Primary Navigation
```html
<nav class="primary-nav" aria-label="Main navigation">
  <ul>
    <li><a href="#dashboards">Dashboards</a></li>
    <li><a href="#mps">MPs</a></li>
    <li><a href="#votes">Votes</a></li>
    <li><a href="#committees">Committees</a></li>
    <li><a href="#news">News</a></li>
  </ul>
</nav>
```

#### Secondary Navigation (Contextual)
- Dashboard filters (time range, party, committee)
- Sorting options (alphabetical, by value)
- View toggles (table, chart, map)

## Visual Design

### Color Palette (Cyberpunk Theme)
```css
/* Primary Colors */
--primary-cyan: #00d9ff;      /* Data points, links */
--primary-magenta: #ff006e;   /* Alerts, critical items */
--primary-yellow: #ffbe0b;    /* Highlights, warnings */

/* Background Colors */
--dark-bg: #0a0e27;           /* Main background */
--mid-bg: #1a1e3d;            /* Cards, panels */
--light-bg: #2a2e4d;          /* Hover states */

/* Text Colors */
--light-text: #e0e0e0;        /* Body text */
--mid-text: #a0a0a0;          /* Secondary text */
--dark-text: #606060;         /* Disabled text */

/* Semantic Colors */
--success: #00ff88;           /* Positive trends */
--warning: #ffbe0b;           /* Caution items */
--error: #ff006e;             /* Errors, high risk */
--info: #00d9ff;              /* Information, tooltips */
```

### Typography
```css
/* Font Families */
--font-primary: 'Inter', sans-serif;      /* Body, UI */
--font-heading: 'Orbitron', sans-serif;   /* Headings, emphasis */
--font-mono: 'Fira Code', monospace;      /* Code, data */

/* Font Sizes (Fluid Typography) */
--font-xs: clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem);   /* 12-14px */
--font-sm: clamp(0.875rem, 0.8rem + 0.375vw, 1rem);     /* 14-16px */
--font-base: clamp(1rem, 0.9rem + 0.5vw, 1.125rem);     /* 16-18px */
--font-lg: clamp(1.25rem, 1.1rem + 0.75vw, 1.5rem);     /* 20-24px */
--font-xl: clamp(1.5rem, 1.3rem + 1vw, 2rem);           /* 24-32px */
--font-2xl: clamp(2rem, 1.7rem + 1.5vw, 3rem);          /* 32-48px */

/* Line Heights */
--leading-tight: 1.25;     /* Headings */
--leading-normal: 1.5;     /* Body text */
--leading-relaxed: 1.75;   /* Long-form content */
```

### Spacing System
```css
/* Spacing Scale (4px base) */
--space-xs: 0.25rem;   /* 4px */
--space-sm: 0.5rem;    /* 8px */
--space-md: 1rem;      /* 16px */
--space-lg: 1.5rem;    /* 24px */
--space-xl: 2rem;      /* 32px */
--space-2xl: 3rem;     /* 48px */
--space-3xl: 4rem;     /* 64px */
```

## UI Components

### Dashboard Cards
```html
<div class="dashboard-card">
  <header class="card-header">
    <h3 class="card-title">Voting Discipline</h3>
    <button class="card-action" aria-label="More options">⋮</button>
  </header>
  <div class="card-body">
    <canvas id="votingDisciplineChart"></canvas>
  </div>
  <footer class="card-footer">
    <span class="card-meta">Updated: 2026-02-11</span>
    <a href="#details" class="card-link">View details →</a>
  </footer>
</div>
```

### Data Tables
```html
<table class="data-table" role="table">
  <thead>
    <tr>
      <th scope="col" role="columnheader">
        MP Name
        <button aria-label="Sort by name">↕</button>
      </th>
      <th scope="col" role="columnheader">Party</th>
      <th scope="col" role="columnheader">Risk Score</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Anna Svensson</td>
      <td>S</td>
      <td><span class="badge badge-high">7.2</span></td>
    </tr>
  </tbody>
</table>
```

### Filters & Search
```html
<div class="filter-panel">
  <div class="search-box">
    <label for="search" class="sr-only">Search MPs</label>
    <input 
      type="search" 
      id="search" 
      placeholder="Search by name, party, committee"
      aria-describedby="search-help"
    >
  </div>
  
  <fieldset class="filter-group">
    <legend>Filter by Party</legend>
    <label>
      <input type="checkbox" name="party" value="S"> 
      <span>Socialdemokraterna (S)</span>
    </label>
    <!-- Repeat for other parties -->
  </fieldset>
</div>
```

### Loading States
```html
<!-- Skeleton Loader -->
<div class="skeleton-card" aria-busy="true" aria-label="Loading content">
  <div class="skeleton-header"></div>
  <div class="skeleton-body">
    <div class="skeleton-line"></div>
    <div class="skeleton-line"></div>
    <div class="skeleton-line short"></div>
  </div>
</div>

<!-- Spinner (fallback) -->
<div class="spinner" role="status">
  <span class="sr-only">Loading...</span>
</div>
```

## Responsive Breakpoints

```css
/* Mobile First Approach */

/* Extra Small: 320px - 479px (default, no media query) */
/* Small Phones */

/* Small: 480px - 767px */
@media (min-width: 30em) { /* 480px */
  /* Larger phones, portrait tablets */
}

/* Medium: 768px - 1023px */
@media (min-width: 48em) { /* 768px */
  /* Tablets, landscape */
}

/* Large: 1024px - 1279px */
@media (min-width: 64em) { /* 1024px */
  /* Small laptops, desktops */
}

/* Extra Large: 1280px - 1919px */
@media (min-width: 80em) { /* 1280px */
  /* Desktops, large screens */
}

/* XXL: 1920px+ */
@media (min-width: 120em) { /* 1920px */
  /* Very large screens */
}
```

## Accessibility Checklist

### WCAG 2.1 AA Compliance

#### Perceivable
- ✅ **Alt Text**: All images have descriptive alt attributes
- ✅ **Color Contrast**: 4.5:1 for normal text, 3:1 for large text
- ✅ **Text Resize**: Readable at 200% zoom
- ✅ **Audio/Video**: Captions, transcripts (if media present)

#### Operable
- ✅ **Keyboard Navigation**: All functions accessible via keyboard
- ✅ **Focus Indicators**: Visible focus states (2px outline, high contrast)
- ✅ **Skip Links**: "Skip to main content" for screen readers
- ✅ **No Keyboard Traps**: Users can navigate away from all elements

#### Understandable
- ✅ **Language Declaration**: `<html lang="en">` for each language version
- ✅ **Consistent Navigation**: Same across all pages
- ✅ **Predictable**: No unexpected context changes
- ✅ **Error Identification**: Clear error messages with suggestions

#### Robust
- ✅ **Valid HTML**: No parsing errors
- ✅ **ARIA Labels**: Proper use of ARIA attributes
- ✅ **Screen Reader Testing**: NVDA, JAWS, VoiceOver compatibility

## Usability Testing

### Testing Methods

#### 1. Hallway Testing (Guerrilla Testing)
- **When**: Early prototypes, quick validation
- **Method**: Show design to 5 random people, observe
- **Cost**: Low (time only)
- **Frequency**: Weekly during design phase

#### 2. Remote Moderated Testing
- **When**: Key user flows, complex interactions
- **Method**: Video call, task-based scenarios, think-aloud protocol
- **Cost**: Medium (participant compensation)
- **Frequency**: Bi-weekly, 5-8 participants per round

#### 3. A/B Testing
- **When**: Specific UI decisions (button copy, layout variants)
- **Method**: Split traffic 50/50, measure conversion, engagement
- **Cost**: Low (analytics tracking)
- **Frequency**: Continuous, 2-4 tests running simultaneously

#### 4. Analytics Review
- **When**: Ongoing performance monitoring
- **Method**: Google Analytics, heatmaps (Hotjar), session recordings
- **Cost**: Low (tooling costs)
- **Frequency**: Weekly reports, monthly deep dives

### Key Usability Metrics
```yaml
Task Success Rate:
  Target: >80% users complete primary tasks
  Measured: Can users find MP profile, view voting record, filter by party?

Time on Task:
  Target: <2 minutes for common tasks
  Measured: How long to find specific information?

Error Rate:
  Target: <5% errors per task
  Measured: Clicks on wrong elements, navigation mistakes

System Usability Scale (SUS):
  Target: >68 (above average)
  Measured: 10-question standardized survey

Net Promoter Score (NPS):
  Target: >30 (good for B2B SaaS)
  Measured: "How likely to recommend 0-10?"
```

## Multi-Language Considerations

### RTL (Right-to-Left) Support
- **Languages**: Arabic (ar), Hebrew (he)
- **CSS**: Use logical properties (`inline-start` not `left`)
- **Icons**: Mirror directional icons (arrows, chevrons)
- **Layout**: Flip entire layout horizontally

```css
/* RTL-Aware Styles */
[dir="rtl"] .element {
  direction: rtl;
  text-align: right;
}

/* Logical Properties (works for both LTR/RTL) */
.element {
  margin-inline-start: 1rem;   /* Not margin-left */
  padding-inline-end: 0.5rem;  /* Not padding-right */
}
```

### Cultural Adaptations
- **Date Formats**: US (MM/DD/YYYY) vs EU (DD/MM/YYYY) vs ISO (YYYY-MM-DD)
- **Number Formats**: 1,000.00 (US/UK) vs 1.000,00 (DE/FR/ES)
- **Currency**: SEK (kr), EUR (€), USD ($)
- **Colors**: Blue = trust (Western), red = luck (China), green = prosperity (Middle East)

## Performance Optimization

### Core Web Vitals
```yaml
Largest Contentful Paint (LCP):
  Target: <2.5s
  Strategies:
    - Optimize images (WebP, lazy loading)
    - Minimize CSS blocking
    - CDN for static assets

First Input Delay (FID):
  Target: <100ms
  Strategies:
    - Minimize JavaScript execution
    - Code splitting, defer non-critical JS
    - Use web workers for heavy computation

Cumulative Layout Shift (CLS):
  Target: <0.1
  Strategies:
    - Set explicit width/height for images
    - Reserve space for dynamic content
    - Avoid injecting content above fold
```

### Image Optimization
```html
<!-- Responsive Images -->
<picture>
  <source srcset="dashboard-mobile.webp" media="(max-width: 767px)" type="image/webp">
  <source srcset="dashboard-tablet.webp" media="(max-width: 1023px)" type="image/webp">
  <source srcset="dashboard-desktop.webp" type="image/webp">
  <img src="dashboard-desktop.jpg" alt="Voting discipline dashboard" loading="lazy">
</picture>
```

## Remember

- 👥 **Users First**: Design for real user needs, not assumptions
- ♿ **Accessibility**: WCAG 2.1 AA compliance is mandatory, not optional
- 📱 **Mobile Priority**: Design for 320px first, enhance for larger
- 🎨 **Consistency**: Follow design system, reuse components
- 🧪 **Test Early**: Usability testing in every sprint
- 🌍 **14 Languages**: Consider RTL, cultural adaptations
- ⚡ **Performance**: Core Web Vitals matter for UX and SEO

---

**Last Updated**: 2026-02-11  
**Maintained by**: Hack23 AB
