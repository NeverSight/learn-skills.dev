---
name: landing-page-optimizer
description: Optimize landing pages for conversions, performance, and SEO. Use when improving landing pages, increasing conversions, or optimizing page performance.
---

# Landing Page Optimizer

## Instructions

When optimizing landing pages:

1. **Audit current page** (speed, UX, conversion elements)
2. **Identify improvement areas**
3. **Implement optimizations**
4. **Set up tracking**

## Above the Fold Checklist

- [ ] **Clear headline** - Value proposition in <5 seconds
- [ ] **Supporting subheadline** - Expand on benefit
- [ ] **Hero image/video** - Relevant, high-quality
- [ ] **Primary CTA** - Contrasting color, action-oriented
- [ ] **Social proof** - Logos, ratings, testimonials
- [ ] **No navigation distractions** - Minimal or hidden nav

## Page Structure Template

```tsx
// Optimal landing page structure
<main>
  {/* 1. Hero Section */}
  <section className="min-h-[80vh] flex items-center">
    <div className="max-w-6xl mx-auto px-4 grid lg:grid-cols-2 gap-12 items-center">
      <div>
        <Badge>New Feature</Badge>
        <h1 className="text-4xl lg:text-6xl font-bold mt-4">
          Main Value Proposition
        </h1>
        <p className="text-xl text-gray-600 mt-6">
          Supporting statement that expands on the benefit
        </p>
        <div className="flex gap-4 mt-8">
          <Button size="lg">Primary CTA</Button>
          <Button size="lg" variant="outline">Secondary CTA</Button>
        </div>
        <div className="flex items-center gap-6 mt-8">
          <div className="flex -space-x-2">
            {avatars.map(a => <Avatar key={a.id} src={a.src} />)}
          </div>
          <p className="text-sm text-gray-600">
            <strong>2,000+</strong> happy customers
          </p>
        </div>
      </div>
      <div>
        <img src="/hero-image.png" alt="Product preview" />
      </div>
    </div>
  </section>

  {/* 2. Social Proof - Logos */}
  <section className="py-12 bg-gray-50">
    <p className="text-center text-gray-500 mb-8">Trusted by leading companies</p>
    <div className="flex justify-center gap-12 opacity-60">
      {logos.map(logo => <img key={logo.name} src={logo.src} alt={logo.name} />)}
    </div>
  </section>

  {/* 3. Problem/Solution */}
  <section className="py-20">
    <div className="max-w-3xl mx-auto text-center">
      <h2 className="text-3xl font-bold">The Problem</h2>
      <p className="text-xl text-gray-600 mt-4">
        Describe the pain point your audience faces
      </p>
    </div>
  </section>

  {/* 4. Features/Benefits */}
  <section className="py-20 bg-gray-50">
    <h2 className="text-3xl font-bold text-center">How It Works</h2>
    <div className="grid md:grid-cols-3 gap-8 mt-12 max-w-6xl mx-auto">
      {features.map(feature => (
        <Card key={feature.title}>
          <feature.icon className="w-12 h-12 text-primary-500" />
          <h3 className="text-xl font-semibold mt-4">{feature.title}</h3>
          <p className="text-gray-600 mt-2">{feature.description}</p>
        </Card>
      ))}
    </div>
  </section>

  {/* 5. Testimonials */}
  <section className="py-20">
    <h2 className="text-3xl font-bold text-center">What Customers Say</h2>
    <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mt-12">
      {testimonials.map(t => (
        <TestimonialCard key={t.name} {...t} />
      ))}
    </div>
  </section>

  {/* 6. Pricing (if applicable) */}
  <section className="py-20 bg-gray-50">
    <PricingTable plans={plans} />
  </section>

  {/* 7. FAQ */}
  <section className="py-20">
    <h2 className="text-3xl font-bold text-center">FAQ</h2>
    <Accordion items={faqs} className="max-w-3xl mx-auto mt-12" />
  </section>

  {/* 8. Final CTA */}
  <section className="py-20 bg-primary-600 text-white text-center">
    <h2 className="text-3xl font-bold">Ready to Get Started?</h2>
    <p className="text-xl opacity-90 mt-4">Join 2,000+ companies already using our product</p>
    <Button size="lg" variant="secondary" className="mt-8">
      Start Free Trial
    </Button>
    <p className="text-sm opacity-75 mt-4">No credit card required</p>
  </section>
</main>
```

## CTA Optimization

### Button Best Practices

```tsx
// Good CTAs
<Button>Start Free Trial</Button>
<Button>Get Started Free</Button>
<Button>Try It Free for 14 Days</Button>
<Button>Book a Demo</Button>

// Add urgency/value
<Button>
  Get 50% Off Today
  <span className="text-sm opacity-75 block">Offer ends midnight</span>
</Button>

// Reduce friction
<div className="text-center">
  <Button size="lg">Start Free Trial</Button>
  <p className="text-sm text-gray-500 mt-2">
    No credit card required • Cancel anytime
  </p>
</div>
```

### CTA Placement

1. **Hero section** - Primary CTA above fold
2. **After features** - Reinforce value
3. **After testimonials** - Social proof boost
4. **Sticky header/footer** - Always accessible
5. **Exit intent popup** - Last chance

## Performance Optimization

### Image Optimization

```tsx
// Next.js Image component
import Image from 'next/image';

<Image
  src="/hero.png"
  alt="Product screenshot"
  width={1200}
  height={800}
  priority // Above-fold images
  placeholder="blur"
  blurDataURL={blurData}
/>

// Lazy load below-fold images
<Image
  src="/feature.png"
  loading="lazy"
  ...
/>
```

### Critical CSS

```tsx
// Inline critical styles for above-fold
<head>
  <style dangerouslySetInnerHTML={{ __html: criticalCSS }} />
  <link rel="preload" href="/fonts/inter.woff2" as="font" crossOrigin="" />
</head>
```

### Performance Targets

| Metric | Target |
|--------|--------|
| LCP | < 2.5s |
| FID/INP | < 100ms |
| CLS | < 0.1 |
| Total Size | < 1MB |
| Time to Interactive | < 3s |

## SEO Optimization

### Meta Tags

```tsx
// app/layout.tsx or pages/_app.tsx
export const metadata = {
  title: 'Product Name - Main Benefit | Brand',
  description: 'Clear description with keywords. 150-160 chars.',
  openGraph: {
    title: 'Product Name - Main Benefit',
    description: 'Description for social sharing',
    images: [{ url: '/og-image.png', width: 1200, height: 630 }],
  },
  twitter: {
    card: 'summary_large_image',
  },
};
```

### Structured Data

```tsx
<script type="application/ld+json">
  {JSON.stringify({
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "Product Name",
    "applicationCategory": "BusinessApplication",
    "offers": {
      "@type": "Offer",
      "price": "29",
      "priceCurrency": "USD"
    },
    "aggregateRating": {
      "@type": "AggregateRating",
      "ratingValue": "4.8",
      "reviewCount": "1250"
    }
  })}
</script>
```

## Conversion Tracking

```tsx
// Google Analytics 4 events
const trackCTA = (ctaName: string) => {
  gtag('event', 'cta_click', {
    cta_name: ctaName,
    page_location: window.location.href,
  });
};

// Track scroll depth
useEffect(() => {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          gtag('event', 'section_viewed', {
            section_name: entry.target.id,
          });
        }
      });
    },
    { threshold: 0.5 }
  );

  document.querySelectorAll('section[id]').forEach((section) => {
    observer.observe(section);
  });
}, []);
```

## A/B Testing Elements

Priority elements to test:
1. **Headline copy** - Different value propositions
2. **CTA text** - "Start Free" vs "Get Started" vs "Try Now"
3. **CTA color** - High contrast options
4. **Hero image** - Product vs people vs abstract
5. **Social proof placement** - Above vs below fold
6. **Pricing display** - Monthly vs annual default
7. **Form length** - Email only vs full form

## Mobile Optimization

```tsx
// Thumb-friendly CTAs
<Button className="w-full md:w-auto h-14 text-lg">
  Get Started
</Button>

// Sticky mobile CTA
<div className="fixed bottom-0 left-0 right-0 p-4 bg-white border-t md:hidden">
  <Button className="w-full">Start Free Trial</Button>
</div>

// Reduce content on mobile
<p className="hidden md:block">
  {fullDescription}
</p>
<p className="md:hidden">
  {shortDescription}
</p>
```

## Quick Wins Checklist

- [ ] Headline communicates value in 5 seconds
- [ ] CTA button is high contrast and above fold
- [ ] Page loads in under 3 seconds
- [ ] Social proof visible above fold
- [ ] Mobile-optimized with thumb-friendly CTAs
- [ ] No broken images or links
- [ ] Forms have minimal required fields
- [ ] Trust badges near CTAs (security, guarantees)
- [ ] Clear pricing (no hidden fees messaging)
- [ ] Testimonials include photos and titles
