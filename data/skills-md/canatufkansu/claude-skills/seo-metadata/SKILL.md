---
name: seo-metadata
description: Dynamic metadata generation per locale with canonical URLs, Open Graph tags, Twitter cards, and hreflang alternates. Use when implementing page metadata, setting up SEO for multilingual sites, or configuring social sharing previews.
---

# SEO Metadata

## Base Metadata Configuration

```tsx
// app/layout.tsx
import type { Metadata } from 'next';

export const metadata: Metadata = {
  metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL!),
  title: {
    template: '%s | Studio Name',
    default: 'Studio Name - Pilates & Yoga',
  },
  description: 'Professional Pilates and Yoga coaching for strength and calm.',
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
};
```

## Per-Page Dynamic Metadata

```tsx
// app/[locale]/services/page.tsx
import type { Metadata } from 'next';
import { getTranslations } from 'next-intl/server';
import { locales } from '@/i18n.config';

type Props = {
  params: Promise<{ locale: string }>;
};

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: 'meta.services' });
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL;

  return {
    title: t('title'),
    description: t('description'),
    alternates: {
      canonical: `${siteUrl}/${locale}/services`,
      languages: Object.fromEntries(
        locales.map((loc) => [loc, `${siteUrl}/${loc}/services`])
      ),
    },
    openGraph: {
      title: t('title'),
      description: t('description'),
      url: `${siteUrl}/${locale}/services`,
      siteName: 'Studio Name',
      locale: locale.replace('-', '_'),
      type: 'website',
      images: [
        {
          url: `${siteUrl}/og/services.jpg`,
          width: 1200,
          height: 630,
          alt: t('title'),
        },
      ],
    },
    twitter: {
      card: 'summary_large_image',
      title: t('title'),
      description: t('description'),
      images: [`${siteUrl}/og/services.jpg`],
    },
  };
}
```

## Metadata Helper Function

```tsx
// lib/metadata.ts
import type { Metadata } from 'next';
import { locales, type Locale } from '@/i18n.config';

interface GenerateMetadataOptions {
  locale: Locale;
  path: string;
  title: string;
  description: string;
  image?: string;
  noIndex?: boolean;
}

export function generatePageMetadata({
  locale,
  path,
  title,
  description,
  image = '/og/default.jpg',
  noIndex = false,
}: GenerateMetadataOptions): Metadata {
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL!;
  const fullUrl = `${siteUrl}/${locale}${path}`;
  const imageUrl = image.startsWith('http') ? image : `${siteUrl}${image}`;

  return {
    title,
    description,
    robots: noIndex ? { index: false, follow: false } : undefined,
    alternates: {
      canonical: fullUrl,
      languages: Object.fromEntries(
        locales.map((loc) => [loc, `${siteUrl}/${loc}${path}`])
      ),
    },
    openGraph: {
      title,
      description,
      url: fullUrl,
      siteName: 'Studio Name',
      locale: locale.replace('-', '_'),
      type: 'website',
      images: [{ url: imageUrl, width: 1200, height: 630, alt: title }],
    },
    twitter: {
      card: 'summary_large_image',
      title,
      description,
      images: [imageUrl],
    },
  };
}
```

## Usage with Helper

```tsx
// app/[locale]/about/page.tsx
import { generatePageMetadata } from '@/lib/metadata';
import { getTranslations } from 'next-intl/server';

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: 'meta.about' });

  return generatePageMetadata({
    locale: locale as Locale,
    path: '/about',
    title: t('title'),
    description: t('description'),
    image: '/og/about.jpg',
  });
}
```

## Dynamic Route Metadata

```tsx
// app/[locale]/programmes/[slug]/page.tsx
import { getProgrammeBySlug } from '@/lib/data';

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale, slug } = await params;
  const programme = await getProgrammeBySlug(locale as Locale, slug);
  
  if (!programme) {
    return { title: 'Not Found' };
  }

  return generatePageMetadata({
    locale: locale as Locale,
    path: `/programmes/${slug}`,
    title: programme.title,
    description: programme.outcomes.slice(0, 2).join('. '),
  });
}
```

## Hreflang in HTML Head

The metadata API handles hreflang automatically via `alternates.languages`. The rendered HTML will include:

```html
<link rel="canonical" href="https://example.com/en/services" />
<link rel="alternate" hreflang="pt-PT" href="https://example.com/pt-PT/services" />
<link rel="alternate" hreflang="en" href="https://example.com/en/services" />
<link rel="alternate" hreflang="tr" href="https://example.com/tr/services" />
<link rel="alternate" hreflang="es" href="https://example.com/es/services" />
<link rel="alternate" hreflang="fr" href="https://example.com/fr/services" />
<link rel="alternate" hreflang="de" href="https://example.com/de/services" />
<link rel="alternate" hreflang="x-default" href="https://example.com/pt-PT/services" />
```

## Translation Keys Structure

```json
// messages/en.json
{
  "meta": {
    "home": {
      "title": "Pilates & Yoga Coaching",
      "description": "Transform your body with personalized training"
    },
    "services": {
      "title": "Our Services",
      "description": "1:1 sessions, group classes, and online coaching"
    },
    "about": {
      "title": "About Us",
      "description": "Meet your instructor and learn our approach"
    }
  }
}
```
