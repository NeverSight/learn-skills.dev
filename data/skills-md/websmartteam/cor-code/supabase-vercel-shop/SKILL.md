---
name: supabase-vercel-shop
description: Build a complete Supabase + Vercel e-commerce platform with CMS and admin panel. Use for shop setup, online store creation, stripe integration, product catalog, admin dashboard, or CMS projects. Includes database schema, RBAC authentication, content management, checkout flow, and zero-hardcoding architecture with mandatory testing.
allowed-tools:
  - Read
  - Write
  - Edit
  - MultiEdit
  - Bash
  - Glob
  - Grep
  - Task
  - mcp__supabase__*
  - mcp__context7__*
user-invocable: true
---

# Supabase + Vercel E-Commerce Platform

Production-tested architecture for e-commerce with full CMS capabilities. Built with Next.js 16+, Supabase, Stripe, Vercel, and Tailwind CSS v4.

## Execution Options

| Method | Context | Best For |
|--------|---------|----------|
| **ecommerce-builder agent** | Isolated (own context) | Full builds, keeps main chat clean |
| **Direct skill reference** | Main conversation | Quick lookups, specific patterns |

**Recommended**: Use the `ecommerce-builder` sub-agent for full builds - it loads this skill automatically and returns only a summary, keeping your main conversation uncluttered.

## Core Principle: Zero Hardcoding

**EVERY piece of content MUST come from Supabase. NO EXCEPTIONS.**

```typescript
// WRONG - Fallback hides broken CMS
<h1>{content?.title || 'Welcome'}</h1>

// CORRECT - Shows nothing if missing (forces fix)
{content?.title && <h1>{content.title}</h1>}

// CORRECT - Explicit error if required data missing
if (!content) throw new Error('Required CMS content missing');
```

## 🚨 MANDATORY: Hardcode Detection After EVERY Change

**YOU MUST run hardcode detection after adding ANY frontend or backend code.**

This is NON-NEGOTIABLE. Claude defaults to hardcoding - catch it immediately.

### Required Test Commands (Run After Every File Change)

```bash
# 1. Check for hardcoded brand/company names
grep -rn "{{BRAND_NAME}}\|Welcome to\|Our Company\|My Store" src/ --include="*.tsx" --include="*.ts"

# 2. Check for hardcoded prices (any currency)
grep -rn "£[0-9]\|\$[0-9]\|€[0-9]" src/ --include="*.tsx" --include="*.ts"

# 3. Check for Lorem ipsum placeholder text
grep -rn "Lorem\|ipsum\|dolor sit" src/ --include="*.tsx" --include="*.ts"

# 4. Check for fallback patterns (|| 'text')
grep -rn "|| '\||| \"" src/ --include="*.tsx" --include="*.ts"

# 5. Check for hardcoded URLs
grep -rn "https://example\|http://localhost\|www\." src/ --include="*.tsx" --include="*.ts"

# 6. Check for hardcoded contact info
grep -rn "@gmail\|@yahoo\|@hotmail\|555-\|123-" src/ --include="*.tsx" --include="*.ts"
```

### Automated Pre-Commit Hook

```bash
#!/bin/bash
# .husky/pre-commit - BLOCK commits with hardcoded content

ERRORS=0

# Brand names
if grep -rq "Welcome to\|Our Company\|My Store\|Your Brand" src/ --include="*.tsx"; then
  echo "❌ BLOCKED: Hardcoded brand names found"
  ERRORS=$((ERRORS + 1))
fi

# Fallback patterns
if grep -rq "|| '\||| \"" src/ --include="*.tsx"; then
  echo "❌ BLOCKED: Fallback patterns found (|| 'text')"
  grep -rn "|| '\||| \"" src/ --include="*.tsx"
  ERRORS=$((ERRORS + 1))
fi

# Hardcoded prices
if grep -rq "£[0-9]\|\$[0-9]" src/ --include="*.tsx"; then
  echo "❌ BLOCKED: Hardcoded prices found"
  ERRORS=$((ERRORS + 1))
fi

if [ $ERRORS -gt 0 ]; then
  echo "❌ Commit blocked. Fix hardcoded content first."
  exit 1
fi

echo "✅ No hardcoded content detected"
```

## 🚫 ABSOLUTE BAN: Fallback Patterns

**FALLBACKS HIDE BROKEN CMS CONNECTIONS. NEVER USE THEM.**

Claude's training data is full of fallback patterns. Fight this instinct.

### Banned Patterns (NEVER Write These)

```typescript
// ❌ BANNED - String fallbacks
{title || 'Default Title'}
{description ?? 'No description available'}
{content?.text || 'Loading...'}
{settings.brandName || 'Company Name'}

// ❌ BANNED - Conditional with fallback
{title ? title : 'Fallback'}
{data.length > 0 ? data : defaultData}

// ❌ BANNED - Default function parameters for content
function Hero({ title = 'Welcome' }) {}
function Card({ price = 0, name = 'Product' }) {}

// ❌ BANNED - Nullish coalescing for content
const displayTitle = title ?? 'Untitled';
const brandName = settings?.name ?? 'Brand';
```

### Correct Patterns (ALWAYS Use These)

```typescript
// ✅ CORRECT - Conditional render (shows nothing if missing)
{content?.title && <h1>{content.title}</h1>}
{products?.length > 0 && <ProductGrid products={products} />}

// ✅ CORRECT - Early return for missing required data
if (!content) return null;
if (!product) throw new Error('Product not found');

// ✅ CORRECT - Loading states from database
{isLoading && <Skeleton />}
{!isLoading && content && <Content data={content} />}

// ✅ CORRECT - Error boundaries
if (!settings) {
  console.error('CMS settings not loaded');
  return null;  // Force fix, don't hide with fallback
}
```

### Why Fallbacks Are Dangerous

1. **Hide broken database connections** - You deploy, CMS is down, users see "Welcome" instead of nothing
2. **Mask missing data** - Content team forgets to add text, default shows instead of error
3. **Create false confidence** - "It works!" when actually CMS isn't being read at all
4. **Impossible to debug** - No errors, no warnings, just wrong content

## 🧹 MANDATORY: Legacy Cleanup After Migration

**When migrating from hardcoded to CMS, DELETE the old code. No exceptions.**

### Migration Checklist

```markdown
## Content Migration: [Component Name]

### Pre-Migration
- [ ] Identified all hardcoded content
- [ ] Created database records for each piece
- [ ] Verified CMS content loads correctly

### Migration
- [ ] Updated component to fetch from CMS
- [ ] Removed ALL hardcoded strings
- [ ] Removed ALL fallback patterns
- [ ] Removed unused imports

### Post-Migration CLEANUP (CRITICAL)
- [ ] Deleted old hardcoded constants file
- [ ] Deleted commented-out old code
- [ ] Deleted unused variables
- [ ] Deleted temporary migration helpers
- [ ] Ran hardcode detection tests
- [ ] Verified no fallbacks remain
```

### What MUST Be Deleted

```typescript
// ❌ DELETE: Old constants files
// src/lib/constants.ts - DELETE ENTIRE FILE after migration
export const BRAND_NAME = 'Company';  // DELETE
export const HERO_TITLE = 'Welcome';  // DELETE

// ❌ DELETE: Commented "for reference" code
// const oldTitle = 'Welcome to Our Store'; // keeping for reference
// DELETE THIS - It's in git history if needed

// ❌ DELETE: Migration helpers
// TODO: Remove after CMS working
const tempFallback = 'Temporary';  // DELETE

// ❌ DELETE: Unused type definitions
interface OldHardcodedContent {  // DELETE if not used
  title: string;
  description: string;
}
```

### Verification After Cleanup

```bash
# 1. Check no orphaned imports
grep -rn "from.*constants" src/ --include="*.tsx"

# 2. Check no TODO comments about migration
grep -rn "TODO.*migration\|TODO.*remove\|TODO.*CMS" src/ --include="*.tsx"

# 3. Check no commented code blocks
grep -rn "^// const\|^// export\|^// function" src/ --include="*.tsx"

# 4. Verify clean git diff
git diff --stat  # Should only show modified files, no leftover
```

**What MUST be in CMS:**
- All page text (headings, paragraphs, CTAs)
- All images (hero, products, icons)
- Navigation items
- Footer content
- Product data
- Brand story content
- Contact information
- SEO metadata
- Social media links

**What CAN be hardcoded:**
- Component structure/layout
- Tailwind classes
- Technical configuration
- Environment variable names

## Tech Stack

| Layer | Technology |
|-------|------------|
| Framework | Next.js 16+ / React 19 |
| Styling | Tailwind CSS v4 |
| Database | Supabase |
| Payments | Stripe |
| Hosting | Vercel (London lhr1) |
| Auth | Supabase Auth with RBAC |

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        PUBLIC FRONTEND                           │
├─────────────────────────────────────────────────────────────────┤
│  Homepage → Products → Cart → Checkout → Order Confirmation     │
│      ↓          ↓        ↓        ↓              ↓              │
│  page_content  products  local   Stripe    orders table         │
└─────────────────────────────┬───────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│                      ADMIN DASHBOARD                             │
├─────────────────────────────────────────────────────────────────┤
│  Dashboard → Products → Orders → Content → Settings → Users     │
│      ↓          ↓         ↓         ↓          ↓         ↓      │
│  Analytics   CRUD      Status    CMS Edit   Config    RBAC      │
└─────────────────────────────────────────────────────────────────┘
```

## Placeholders

Replace these with project-specific values:

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{{BRAND_NAME}}` | Brand/company name | Your Brand |
| `{{PROJECT_ID}}` | Supabase project ID | abcdefghijklmnop |
| `{{PROJECT_URL}}` | Supabase project URL | https://[PROJECT_ID].supabase.co |
| `{{CONTACT_EMAIL}}` | Contact email | hello@yourbrand.com |
| `{{STRIPE_ACCOUNT}}` | Stripe account ref | acct_xxx |
| `{{VERCEL_PROJECT}}` | Vercel project name | your-shop |
| `{{GITHUB_ORG}}` | GitHub organisation | YourOrganisation |

## Quick Start Checklist

### Phase 1: Discovery & Setup (MANDATORY FIRST)
1. **Project Discovery**: Ask user about existing infrastructure (see [SETUP.md](SETUP.md))
   - Supabase project (exists or create?)
   - Git repository (exists or create?)
   - Vercel project (exists or create?)
   - Stripe account (exists or create?)
2. **Record Project IDs**: Document all IDs in project CLAUDE.md
3. **Supabase MCP**: Configure project-specific MCP (NOT global)
4. **Environment Variables**: Set up .env.local with all required vars

### Phase 2: Database, Storage & Auth
5. **Database Setup**: Run migrations in order (see [DATABASE.md](DATABASE.md))
6. **Storage Buckets**: Configure image storage (see [STORAGE.md](STORAGE.md))
7. **Auth & Roles**: Configure RBAC system (see [AUTH.md](AUTH.md))

### Phase 3: Admin & CMS
8. **Admin Panel**: Scaffold admin routes (see [ADMIN.md](ADMIN.md))
9. **CMS Content**: Populate page_content table (see [CMS.md](CMS.md))

### Phase 4: Public Site
10. **Frontend**: Build public pages (see [FRONTEND.md](FRONTEND.md))
11. **Shop Integration**: Connect Stripe (see [SHOP.md](SHOP.md))
12. **Checkout Flow**: Cart, checkout, orders (see [CHECKOUT.md](CHECKOUT.md))

### Phase 5: Deploy
13. **Deploy**: Vercel with London (lhr1) region
14. **Stripe Webhooks**: Configure production webhook URL
15. **Final Test**: End-to-end checkout test

## Detailed Documentation

| File | Purpose |
|------|---------|
| [SETUP.md](SETUP.md) | **START HERE** - Project discovery, MCP config, env vars |
| [DATABASE.md](DATABASE.md) | Complete Supabase schema with all tables |
| [STORAGE.md](STORAGE.md) | Supabase Storage buckets, policies, upload patterns |
| [AUTH.md](AUTH.md) | Role-based access control system |
| [ADMIN.md](ADMIN.md) | Admin dashboard architecture |
| [CMS.md](CMS.md) | Content management patterns |
| [SHOP.md](SHOP.md) | Products, cart, wishlist |
| [CHECKOUT.md](CHECKOUT.md) | Cart page, checkout, orders, Stripe webhooks |
| [FRONTEND.md](FRONTEND.md) | Public storefront components |

## Key Patterns

### 1. Supabase Client Setup

```typescript
// src/lib/supabase.ts - Browser client
import { createBrowserClient } from '@supabase/ssr';

export const supabase = createBrowserClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

// src/lib/supabase-server.ts - Server clients
import 'server-only';
import { createServerClient } from '@supabase/ssr';
import { createClient } from '@supabase/supabase-js';
import { cookies } from 'next/headers';

// Session-based (respects RLS)
export async function createServerSupabaseClient() {
  const cookieStore = await cookies();
  return createServerClient(url, anonKey, {
    cookies: {
      getAll: () => cookieStore.getAll(),
      setAll: (cookies) => cookies.forEach(c => cookieStore.set(c.name, c.value, c.options))
    }
  });
}

// Service role (bypasses RLS - use for admin operations)
export function createServiceRoleClient() {
  return createClient(url, serviceRoleKey, {
    auth: { autoRefreshToken: false, persistSession: false }
  });
}
```

### 2. CMS Content Fetching

```typescript
// src/lib/cms.ts
export async function getPageContent(page: string): Promise<Record<string, unknown>> {
  const { data } = await supabase
    .from('page_content')
    .select('section, content')
    .eq('page', page)
    .eq('is_active', true)
    .order('display_order');

  return (data || []).reduce((acc, item) => {
    acc[item.section] = item.content;
    return acc;
  }, {});
}

export async function getSetting(key: string): Promise<unknown> {
  const { data } = await supabase
    .from('site_settings')
    .select('value')
    .eq('key', key)
    .single();
  return data?.value;
}
```

### 3. Admin Auth Guard

```typescript
// src/lib/auth.ts
export async function getCurrentUser(): Promise<AuthUser | null> {
  const supabase = await createServerSupabaseClient();
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) return null;

  // Use service role for role queries (bypasses RLS)
  const serviceClient = createServiceRoleClient();
  const { data: roles } = await serviceClient
    .from('user_roles')
    .select('role_id')
    .eq('user_id', user.id);

  const roleIds = roles?.map(r => r.role_id) ?? [];
  const isAdmin = roleIds.some(r => ['super_admin', 'admin', 'shop_editor', 'cms_editor'].includes(r));

  return { ...user, isAdmin, isSuperAdmin: roleIds.includes('super_admin'), roles: roleIds };
}
```

## Anti-Patterns (Don't Do This)

- **NO fallback text** - If CMS returns nothing, show nothing or error
- **NO hardcoded brand names** - Always from `site_settings.brand_name`
- **NO inline styles for admin** - Use admin CSS design system
- **NO dollar signs** - UK sites use £ (pound sterling)
- **NO American English** - Use UK spellings (colour, organisation)
- **NO localhost testing** - Deploy to Vercel preview URLs

## UK Standards (Mandatory)

- **Currency**: GBP (£) with amounts in pence for Stripe
- **Date format**: DD/MM/YYYY
- **Spelling**: UK English (colour, centre, organisation)
- **Region**: Vercel deployment to London (lhr1)
- **Phone format**: +44 prefix

## UK Icon Standards (CRITICAL)

**ALL icons must be UK-appropriate. NO American-specific symbols.**

### Financial Icons - ALWAYS Use Pound (£)

```tsx
// ✅ CORRECT - UK Pound Sterling Icon
const PoundIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
    <path d="M6 20h12M6 12h8M10 20V10c0-4 5-6 9-3" />
  </svg>
);

// ❌ WRONG - Dollar sign (American)
const DollarIcon = () => (
  <svg>
    <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
  </svg>
);
```

### Icon Substitution Rules

| American Icon | UK Replacement | Notes |
|---------------|----------------|-------|
| `$` Dollar | `£` Pound | ALL financial contexts |
| Dollar bill | Pound note | Currency imagery |
| US flag | Union Jack | ONLY if flag needed |
| Fahrenheit | Celsius | Temperature displays |
| US outlet | UK plug | Electrical contexts |

### Currency Display Patterns

```tsx
// ✅ CORRECT - UK currency formatting
function formatPrice(pence: number): string {
  return new Intl.NumberFormat('en-GB', {
    style: 'currency',
    currency: 'GBP'
  }).format(pence / 100);
}

// Dashboard stat cards - ALWAYS pound icon
<StatCard
  title="Total Revenue"
  value={`£${revenue.toLocaleString('en-GB')}`}
  icon={<PoundIcon />}  // NEVER DollarIcon!
/>

// Price displays
<span className="price">£{price.toFixed(2)}</span>  // £49.99 format
```

### Icon Library Guidance

When using icon libraries (Lucide, Heroicons, etc.):

```tsx
// ✅ CORRECT - Use generic or UK-appropriate icons
import { Banknote, CreditCard, Wallet } from 'lucide-react';  // Generic financial
import { PoundSterling } from 'lucide-react';  // UK-specific

// ❌ WRONG - Avoid US-specific
import { DollarSign, Landmark } from 'lucide-react';  // American connotations
```

### Admin Dashboard Icons

ALL admin dashboard icons MUST follow UK standards:

```tsx
// Revenue/financial displays
<PoundIcon />           // ✅ Revenue, earnings, totals
<CreditCard />          // ✅ Payments (generic)
<Wallet />              // ✅ Balance (generic)
<BanknoteIcon />        // ✅ Cash/currency (generic)

// NEVER use
<DollarSign />          // ❌ American
<CircleDollarSign />    // ❌ American
```

### Hardcode Detection - Icons

Add to pre-commit checks:

```bash
# Check for American currency icons
grep -r "DollarSign\|dollar\|Dollar" src/components/ --include="*.tsx"
grep -r "\\\$[0-9]" src/ --include="*.tsx"  # Dollar amounts in code
grep -r "USD\|usd" src/ --include="*.tsx"   # USD currency references
```

### Icon Checklist Before Deploy

- [ ] All financial icons use £ pound symbol
- [ ] No dollar signs ($) anywhere in UI
- [ ] Currency formatted as GBP with en-GB locale
- [ ] Icon library imports avoid US-specific icons
- [ ] Admin dashboard stat cards use PoundIcon
- [ ] Price displays show £ prefix
