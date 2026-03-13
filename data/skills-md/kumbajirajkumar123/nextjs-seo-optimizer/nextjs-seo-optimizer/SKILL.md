---
name: nextjs-seo-optimizer
description: Comprehensive Next.js SEO optimization skill for metadata, sitemaps, robots.txt, structured data, and Core Web Vitals. Use when building or auditing Next.js applications for SEO, implementing metadata API, generating sitemaps, adding Open Graph tags, creating JSON-LD structured data, optimizing for search engines, or improving search rankings. Works with Next.js 13+ App Router and Pages Router.
---

# Next.js SEO Optimizer

Optimize Next.js applications for search engines with proper metadata, sitemaps, robots.txt, and structured data.

## Core SEO Implementation Strategy

Follow this order for maximum impact:

1. **Metadata API Setup** (Foundation) - Titles, descriptions, Open Graph
2. **Sitemap Generation** (Discovery) - Help search engines find all pages
3. **Robots.txt Configuration** (Control) - Manage crawler access
4. **Structured Data** (Rich Results) - Enable rich snippets
5. **Performance Optimization** (Rankings) - Core Web Vitals
6. **Internal Linking** (Architecture) - Site structure and flow

## 1. Metadata API Implementation

### Static Metadata (Fixed Content Pages)

Use for pages with unchanging content (home, about, contact):

```typescript
// app/layout.tsx or app/page.tsx
import { Metadata } from 'next'

export const metadata: Metadata = {
  title: {
    default: 'Your Site Name',
    template: '%s | Your Site Name' // Pages will be "Page Title | Your Site Name"
  },
  description: 'Compelling 150-160 character description with keywords',
  keywords: ['keyword1', 'keyword2', 'keyword3'],
  authors: [{ name: 'Author Name', url: 'https://example.com' }],
  creator: 'Company Name',
  publisher: 'Company Name',
  metadataBase: new URL('https://yourdomain.com'),
  alternates: {
    canonical: '/',
  },
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://yourdomain.com',
    title: 'Your Site Name',
    description: 'Compelling description for social sharing',
    siteName: 'Your Site Name',
    images: [{
      url: '/og-image.jpg', // 1200x630px recommended
      width: 1200,
      height: 630,
      alt: 'Image description',
    }],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Your Site Name',
    description: 'Compelling description',
    creator: '@yourtwitterhandle',
    images: ['/twitter-image.jpg'], // 1200x628px
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  verification: {
    google: 'verification-code',
    yandex: 'verification-code',
    yahoo: 'verification-code',
  },
}
```

### Dynamic Metadata (Database/CMS Content)

Use for blog posts, products, dynamic pages:

```typescript
// app/blog/[slug]/page.tsx
import { Metadata, ResolvingMetadata } from 'next'

type Props = {
  params: { slug: string }
  searchParams: { [key: string]: string | string[] | undefined }
}

export async function generateMetadata(
  { params, searchParams }: Props,
  parent: ResolvingMetadata
): Promise<Metadata> {
  // Fetch data
  const post = await fetchBlogPost(params.slug)
  
  // Optionally access and extend parent metadata
  const previousImages = (await parent).openGraph?.images || []
  const previousKeywords = (await parent).keywords || []
 
  return {
    title: post.title, // Will use template from layout
    description: post.excerpt.substring(0, 160),
    keywords: [...previousKeywords, ...post.tags],
    authors: [{ name: post.author.name }],
    openGraph: {
      title: post.title,
      description: post.excerpt,
      type: 'article',
      publishedTime: post.publishedAt,
      modifiedTime: post.updatedAt,
      authors: [post.author.name],
      images: [post.coverImage, ...previousImages],
      url: `https://yourdomain.com/blog/${params.slug}`,
    },
    twitter: {
      card: 'summary_large_image',
      title: post.title,
      description: post.excerpt,
      images: [post.coverImage],
    },
    alternates: {
      canonical: `https://yourdomain.com/blog/${params.slug}`,
    },
  }
}

export default function Page({ params }: Props) {
  // Page content
}
```

### Metadata Best Practices

**Title Optimization:**
- Length: 50-60 characters (mobile SERP display limit)
- Include primary keyword near the beginning
- Use template for consistency: `%s | Brand Name`
- Avoid keyword stuffing
- Make each title unique across pages

**Description Optimization:**
- Length: 150-160 characters (desktop SERP limit), 120 chars (mobile)
- Include primary and secondary keywords naturally
- Write compelling copy that encourages clicks
- Include call-to-action when appropriate
- Make each description unique

**Image Requirements:**
- Open Graph: 1200x630px (16:9 ratio)
- Twitter Card: 1200x628px (1.91:1 ratio)
- File size: < 1MB
- Format: JPG or PNG
- Include descriptive alt text

## 2. Sitemap Generation

### Built-in Static Sitemap (Simple Sites)

For sites with predictable static routes:

```typescript
// app/sitemap.ts
import { MetadataRoute } from 'next'
 
export default function sitemap(): MetadataRoute.Sitemap {
  return [
    {
      url: 'https://yourdomain.com',
      lastModified: new Date(),
      changeFrequency: 'yearly',
      priority: 1,
    },
    {
      url: 'https://yourdomain.com/about',
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 0.8,
    },
    {
      url: 'https://yourdomain.com/blog',
      lastModified: new Date(),
      changeFrequency: 'weekly',
      priority: 0.5,
    },
  ]
}
```

### Dynamic Sitemap (CMS/Database Content)

For sites with dynamic content from CMS or database:

```typescript
// app/sitemap.ts
import { MetadataRoute } from 'next'
 
export default async function sitemap(): MetadataRoute.Sitemap {
  // Fetch dynamic routes
  const posts = await fetch('https://api.example.com/posts').then((res) => res.json())
  const products = await fetch('https://api.example.com/products').then((res) => res.json())
  
  const postEntries: MetadataRoute.Sitemap = posts.map((post: any) => ({
    url: `https://yourdomain.com/blog/${post.slug}`,
    lastModified: new Date(post.updatedAt),
    changeFrequency: 'weekly',
    priority: 0.7,
  }))
  
  const productEntries: MetadataRoute.Sitemap = products.map((product: any) => ({
    url: `https://yourdomain.com/products/${product.slug}`,
    lastModified: new Date(product.updatedAt),
    changeFrequency: 'daily',
    priority: 0.9,
  }))
  
  return [
    {
      url: 'https://yourdomain.com',
      lastModified: new Date(),
      changeFrequency: 'yearly',
      priority: 1,
    },
    ...postEntries,
    ...productEntries,
  ]
}
```

### Using next-sitemap (Recommended for Large Sites)

See references/next-sitemap-guide.md for detailed setup with automatic generation.

**Priority Guidelines:**
- Homepage: 1.0
- Key landing pages: 0.8-0.9
- Blog posts / Products: 0.6-0.8
- Category pages: 0.5-0.7
- Other pages: 0.4-0.6

**Change Frequency Guidelines:**
- `always`: Stock prices, real-time data
- `hourly`: News sites, frequently updated content
- `daily`: Blogs, active e-commerce
- `weekly`: Standard blog posts
- `monthly`: Feature pages
- `yearly`: Static pages (about, contact)
- `never`: Archived content

## 3. Robots.txt Configuration

### Basic robots.txt (Built-in)

```typescript
// app/robots.ts
import { MetadataRoute } from 'next'
 
export default function robots(): MetadataRoute.Robots {
  return {
    rules: {
      userAgent: '*',
      allow: '/',
      disallow: ['/admin/', '/api/', '/private/'],
    },
    sitemap: 'https://yourdomain.com/sitemap.xml',
  }
}
```

### Advanced robots.txt (Multiple User Agents)

```typescript
// app/robots.ts
import { MetadataRoute } from 'next'
 
export default function robots(): MetadataRoute.Robots {
  const baseUrl = process.env.NEXT_PUBLIC_BASE_URL || 'https://yourdomain.com'
  
  return {
    rules: [
      {
        userAgent: '*',
        allow: '/',
        disallow: ['/admin/', '/api/', '/_next/', '/private/'],
        crawlDelay: 1,
      },
      {
        userAgent: 'Googlebot',
        allow: '/',
        disallow: ['/admin/', '/private/'],
      },
      {
        userAgent: 'GPTBot', // Block AI scrapers if desired
        disallow: ['/'],
      },
    ],
    sitemap: `${baseUrl}/sitemap.xml`,
    host: baseUrl,
  }
}
```

**Common Paths to Disallow:**
- `/admin/` - Admin panels
- `/api/` - API endpoints (unless public)
- `/_next/` - Next.js internal files
- `/private/` - Private/restricted content
- `/search?*` - Search result pages (prevent duplicate content)
- `/cart/` - Shopping cart pages
- `/checkout/` - Checkout pages
- `*?*` - All pages with query parameters (optional, use carefully)

**Environment-Specific Rules:**

```typescript
const isDevelopment = process.env.NODE_ENV === 'development'
const isStaging = process.env.VERCEL_ENV === 'preview'

if (isDevelopment || isStaging) {
  return {
    rules: {
      userAgent: '*',
      disallow: '/', // Block all indexing in dev/staging
    },
  }
}
```

## 4. Structured Data (JSON-LD)

Add structured data for rich search results. Always test at https://search.google.com/test/rich-results

### Organization Schema (Homepage)

```typescript
// app/page.tsx or components/StructuredData.tsx
export default function HomePage() {
  const organizationSchema = {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    name: 'Your Company Name',
    url: 'https://yourdomain.com',
    logo: 'https://yourdomain.com/logo.png',
    description: 'Company description',
    address: {
      '@type': 'PostalAddress',
      streetAddress: '123 Main St',
      addressLocality: 'City',
      addressRegion: 'State',
      postalCode: '12345',
      addressCountry: 'US',
    },
    contactPoint: {
      '@type': 'ContactPoint',
      telephone: '+1-234-567-8900',
      contactType: 'Customer Service',
    },
    sameAs: [
      'https://twitter.com/yourcompany',
      'https://facebook.com/yourcompany',
      'https://linkedin.com/company/yourcompany',
    ],
  }

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(organizationSchema) }}
      />
      {/* Page content */}
    </>
  )
}
```

### Article Schema (Blog Posts)

```typescript
export default function BlogPost({ post }: { post: Post }) {
  const articleSchema = {
    '@context': 'https://schema.org',
    '@type': 'BlogPosting',
    headline: post.title,
    description: post.excerpt,
    image: post.coverImage,
    author: {
      '@type': 'Person',
      name: post.author.name,
      url: `https://yourdomain.com/authors/${post.author.slug}`,
    },
    publisher: {
      '@type': 'Organization',
      name: 'Your Company',
      logo: {
        '@type': 'ImageObject',
        url: 'https://yourdomain.com/logo.png',
      },
    },
    datePublished: post.publishedAt,
    dateModified: post.updatedAt,
    mainEntityOfPage: {
      '@type': 'WebPage',
      '@id': `https://yourdomain.com/blog/${post.slug}`,
    },
  }

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(articleSchema) }}
      />
      {/* Article content */}
    </>
  )
}
```

### Product Schema (E-commerce)

```typescript
const productSchema = {
  '@context': 'https://schema.org',
  '@type': 'Product',
  name: product.name,
  image: product.images,
  description: product.description,
  sku: product.sku,
  brand: {
    '@type': 'Brand',
    name: product.brand,
  },
  offers: {
    '@type': 'Offer',
    url: `https://yourdomain.com/products/${product.slug}`,
    priceCurrency: 'USD',
    price: product.price,
    availability: product.inStock
      ? 'https://schema.org/InStock'
      : 'https://schema.org/OutOfStock',
    seller: {
      '@type': 'Organization',
      name: 'Your Company',
    },
  },
  aggregateRating: {
    '@type': 'AggregateRating',
    ratingValue: product.rating,
    reviewCount: product.reviewCount,
  },
}
```

### FAQ Schema

```typescript
const faqSchema = {
  '@context': 'https://schema.org',
  '@type': 'FAQPage',
  mainEntity: faqs.map((faq) => ({
    '@type': 'Question',
    name: faq.question,
    acceptedAnswer: {
      '@type': 'Answer',
      text: faq.answer,
    },
  })),
}
```

### Breadcrumb Schema

```typescript
const breadcrumbSchema = {
  '@context': 'https://schema.org',
  '@type': 'BreadcrumbList',
  itemListElement: breadcrumbs.map((crumb, index) => ({
    '@type': 'ListItem',
    position: index + 1,
    name: crumb.name,
    item: `https://yourdomain.com${crumb.path}`,
  })),
}
```

## 5. Core Web Vitals Optimization

These directly impact search rankings. See references/performance-optimization.md for detailed strategies.

**Quick Wins:**
- Use Next.js `<Image>` component (automatic optimization)
- Enable `experimental.optimizePackageImports` in next.config.js
- Implement proper caching headers
- Use dynamic imports for heavy components: `const HeavyComponent = dynamic(() => import('./HeavyComponent'))`
- Minimize use of client components (`'use client'`)
- Implement proper loading states

## 6. SEO Audit Checklist

When auditing or implementing SEO, check:

**Metadata:**
- [ ] All pages have unique titles (50-60 chars)
- [ ] All pages have unique descriptions (150-160 chars)
- [ ] metadataBase set in root layout
- [ ] Canonical URLs set for all pages
- [ ] Open Graph images (1200x630px)
- [ ] Twitter Card images (1200x628px)
- [ ] No duplicate metadata across pages

**Technical SEO:**
- [ ] sitemap.xml accessible at /sitemap.xml
- [ ] robots.txt accessible at /robots.txt
- [ ] Sitemap includes all public pages
- [ ] robots.txt references sitemap
- [ ] No accidentally blocked important pages
- [ ] HTTPS enabled and enforced
- [ ] 404 pages return 404 status code
- [ ] Redirects use 301 (permanent) properly

**Structured Data:**
- [ ] Organization schema on homepage
- [ ] Article schema on blog posts
- [ ] Product schema on product pages (if applicable)
- [ ] Breadcrumb schema on multi-level pages
- [ ] Valid JSON-LD (test with Google Rich Results Test)

**Performance:**
- [ ] LCP < 2.5s (Largest Contentful Paint)
- [ ] FID < 100ms (First Input Delay)
- [ ] CLS < 0.1 (Cumulative Layout Shift)
- [ ] Images optimized (WebP, correct sizes)
- [ ] Critical CSS inlined
- [ ] JavaScript bundles < 100KB (initial)

**Content:**
- [ ] Proper heading hierarchy (one H1 per page)
- [ ] Internal linking strategy implemented
- [ ] Alt text on all images
- [ ] Mobile-responsive design
- [ ] Accessible (WCAG 2.1 AA)

## 7. Common SEO Issues & Fixes

**Issue: Duplicate metadata**
- Fix: Use generateMetadata with unique data per page
- Fix: Implement proper canonical URLs

**Issue: Poor Core Web Vitals**
- Fix: Use Next.js Image component
- Fix: Implement code splitting
- Fix: Enable SWC minification
- See references/performance-optimization.md

**Issue: Missing structured data**
- Fix: Add JSON-LD to relevant page types
- Fix: Test with Google Rich Results Test

**Issue: Incorrect robots.txt blocking important pages**
- Fix: Test with Google Search Console robots.txt tester
- Fix: Review disallow rules carefully

**Issue: Sitemap not updating**
- Fix: Use dynamic sitemap with data fetching
- Fix: Implement next-sitemap for automatic generation

## 8. Testing & Validation Tools

Use these tools to validate SEO implementation:

**Google Tools:**
- Google Search Console - Monitor search performance
- Google Rich Results Test - Validate structured data
- PageSpeed Insights - Test Core Web Vitals
- Lighthouse - Comprehensive audit

**Third-Party Tools:**
- Screaming Frog - Crawl site and identify issues
- Ahrefs Site Audit - Technical SEO issues
- SEMrush Site Audit - Comprehensive SEO analysis
- Schema Markup Validator - Test JSON-LD

**Testing Commands:**
```bash
# Test metadata locally
curl -I http://localhost:3000/page-to-test

# View sitemap
curl http://localhost:3000/sitemap.xml

# View robots.txt
curl http://localhost:3000/robots.txt

# Run Lighthouse audit
npx lighthouse http://localhost:3000 --view
```

## Implementation Priority

For new projects:
1. Set up metadataBase in root layout
2. Add basic metadata to all pages
3. Create sitemap.ts
4. Create robots.ts
5. Add structured data to key pages
6. Optimize performance
7. Implement comprehensive testing

For existing projects:
1. Audit current SEO (use Lighthouse)
2. Fix critical issues (broken robots.txt, missing sitemaps)
3. Add missing metadata
4. Implement structured data
5. Optimize Core Web Vitals
6. Monitor with Google Search Console

## Next.js Version Compatibility

This skill supports:
- ✅ Next.js 13+ (App Router) - All features
- ⚠️ Next.js 12 (Pages Router) - Use legacy patterns, see references/pages-router-seo.md
- ❌ Next.js < 12 - Upgrade recommended

## Quick Start Commands

```bash
# Validate sitemap locally
curl http://localhost:3000/sitemap.xml | head -n 20

# Test robots.txt
curl http://localhost:3000/robots.txt

# Run SEO audit
npm run build && npm start
# Then in browser: DevTools > Lighthouse > SEO audit

# Test metadata extraction
curl -s http://localhost:3000 | grep -E '<title>|<meta'
```

## Environment Variables

Set these in `.env.local`:

```bash
NEXT_PUBLIC_BASE_URL=https://yourdomain.com
NEXT_PUBLIC_SITE_NAME="Your Site Name"
NEXT_PUBLIC_OG_IMAGE=https://yourdomain.com/og-image.jpg
GOOGLE_VERIFICATION_CODE=your-verification-code
```

## Additional Resources

For specific scenarios and advanced patterns:
- **next-sitemap setup**: See references/next-sitemap-guide.md
- **Performance optimization**: See references/performance-optimization.md
- **Pages Router migration**: See references/pages-router-seo.md
