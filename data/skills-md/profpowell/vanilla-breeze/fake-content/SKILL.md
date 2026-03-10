---
name: fake-content
description: Generate realistic fake content for HTML prototypes. Use when populating pages with sample text, products, testimonials, or other content. NOT generic lorem ipsum.
allowed-tools: Read, Write, Edit, Bash
---

# Fake Content Skill

Generate realistic fake content using @faker-js/faker. Create contextually appropriate sample data for prototypes and development.

## Philosophy

- **Realistic over generic** - Use proper names, realistic prices, believable text
- **Contextually appropriate** - Match content to the page purpose
- **Consistent within context** - Same person name throughout a section
- **Locale-aware** - Match content to page language

## Setup

Install faker as a dev dependency:

```bash
npm install @faker-js/faker --save-dev
```

## Content Types

### Person

Generate realistic user data:

```javascript
import { faker } from '@faker-js/faker';

const person = {
  name: faker.person.fullName(),
  email: faker.internet.email(),
  phone: faker.phone.number(),
  jobTitle: faker.person.jobTitle(),
  avatar: faker.image.avatar(),
  bio: faker.person.bio()
};
```

**HTML Template:**

```html
<article class="team-member">
  <img src="[avatar URL]" alt="[name]"/>
  <h3>[name]</h3>
  <p class="title">[jobTitle]</p>
  <p class="bio">[bio]</p>
  <a href="mailto:[email]">[email]</a>
</article>
```

---

### Product

Generate e-commerce product data:

```javascript
import { faker } from '@faker-js/faker';

const product = {
  name: faker.commerce.productName(),
  description: faker.commerce.productDescription(),
  price: faker.commerce.price({ min: 10, max: 500, dec: 2 }),
  category: faker.commerce.department(),
  sku: faker.string.alphanumeric(8).toUpperCase(),
  rating: faker.number.float({ min: 3.5, max: 5, fractionDigits: 1 }),
  reviews: faker.number.int({ min: 10, max: 500 })
};
```

**HTML Template:**

```html
<product-card sku="[sku]">
  <img src="/assets/images/placeholder/product-400x400.svg"
       alt="[name]"/>
  <h3>[name]</h3>
  <p>[description]</p>
  <data class="price" value="[price]">$[price]</data>
  <p class="category">[category]</p>
  <p class="rating">[rating] stars ([reviews] reviews)</p>
</product-card>
```

---

### Testimonial

Generate customer testimonials:

```javascript
import { faker } from '@faker-js/faker';

const testimonial = {
  quote: faker.lorem.sentences({ min: 2, max: 4 }),
  author: faker.person.fullName(),
  company: faker.company.name(),
  role: faker.person.jobTitle(),
  avatar: faker.image.avatar()
};
```

**HTML Template:**

```html
<blockquote class="testimonial">
  <p>"[quote]"</p>
  <footer>
    <img src="[avatar]" alt="[author]"/>
    <cite>[author]</cite>
    <span class="role">[role], [company]</span>
  </footer>
</blockquote>
```

---

### Article

Generate blog posts and news articles:

```javascript
import { faker } from '@faker-js/faker';

const article = {
  title: faker.lorem.sentence({ min: 5, max: 10 }),
  author: faker.person.fullName(),
  date: faker.date.recent({ days: 30 }),
  excerpt: faker.lorem.sentences(2),
  body: faker.lorem.paragraphs(5),
  category: faker.helpers.arrayElement(['Technology', 'Business', 'Lifestyle', 'Health']),
  readTime: faker.number.int({ min: 3, max: 15 })
};
```

**HTML Template:**

```html
<article class="blog-post">
  <header>
    <h2>[title]</h2>
    <p class="meta">
      By <span class="author">[author]</span> |
      <time datetime="[date ISO]">[date formatted]</time> |
      [readTime] min read
    </p>
  </header>
  <img src="/assets/images/placeholder/card-400x225.svg"
       alt="Article illustration"/>
  <p class="excerpt">[excerpt]</p>
  <div class="content">[body as paragraphs]</div>
</article>
```

---

### Company

Generate business/organization data:

```javascript
import { faker } from '@faker-js/faker';

const company = {
  name: faker.company.name(),
  catchPhrase: faker.company.catchPhrase(),
  buzzPhrase: faker.company.buzzPhrase(),
  industry: faker.company.buzzNoun(),
  phone: faker.phone.number(),
  email: faker.internet.email({ provider: 'company.com' }),
  website: faker.internet.url(),
  address: {
    street: faker.location.streetAddress(),
    city: faker.location.city(),
    state: faker.location.state({ abbreviated: true }),
    zip: faker.location.zipCode(),
    country: faker.location.country()
  }
};
```

**HTML Template:**

```html
<div class="company-info">
  <h3>[name]</h3>
  <p class="tagline">[catchPhrase]</p>
  <address>
    [street]<br/>
    [city], [state] [zip]<br/>
    [country]
  </address>
  <p>
    <a href="tel:[phone]">[phone]</a><br/>
    <a href="mailto:[email]">[email]</a><br/>
    <a href="[website]">[website]</a>
  </p>
</div>
```

---

### Event

Generate event/calendar data:

```javascript
import { faker } from '@faker-js/faker';

const event = {
  title: faker.lorem.sentence({ min: 3, max: 7 }),
  description: faker.lorem.paragraph(),
  date: faker.date.future({ years: 1 }),
  startTime: faker.date.future(),
  endTime: faker.date.future(),
  location: {
    venue: faker.company.name(),
    address: faker.location.streetAddress(),
    city: faker.location.city()
  },
  organizer: faker.person.fullName(),
  price: faker.commerce.price({ min: 0, max: 200 }),
  capacity: faker.number.int({ min: 20, max: 500 })
};
```

**HTML Template:**

```html
<article class="event-card">
  <time datetime="[date ISO]">
    <span class="month">[month]</span>
    <span class="day">[day]</span>
  </time>
  <div class="details">
    <h3>[title]</h3>
    <p>[description]</p>
    <p class="location">[venue], [city]</p>
    <p class="time">[startTime] - [endTime]</p>
    <data class="price" value="[price]">$[price]</data>
  </div>
</article>
```

---

### FAQ

Generate question/answer pairs:

```javascript
import { faker } from '@faker-js/faker';

const faq = {
  question: faker.lorem.sentence().replace('.', '?'),
  answer: faker.lorem.sentences({ min: 2, max: 4 })
};

// Generate multiple FAQs
const faqs = faker.helpers.multiple(
  () => ({
    question: faker.lorem.sentence().replace('.', '?'),
    answer: faker.lorem.sentences({ min: 2, max: 4 })
  }),
  { count: 8 }
);
```

**HTML Template:**

```html
<details class="faq-item">
  <summary>[question]</summary>
  <p>[answer]</p>
</details>
```

---

## Locale Support

Faker supports 70+ locales. Match content to your page's language:

```javascript
// Import locale-specific faker
import { fakerDE } from '@faker-js/faker';  // German
import { fakerFR } from '@faker-js/faker';  // French
import { fakerES } from '@faker-js/faker';  // Spanish
import { fakerJA } from '@faker-js/faker';  // Japanese

// Use locale-specific instance
const germanPerson = {
  name: fakerDE.person.fullName(),    // "Max Müller"
  city: fakerDE.location.city(),       // "München"
  phone: fakerDE.phone.number()        // "+49 30 12345678"
};
```

**Common Locales:**

| Code | Language | Import |
|------|----------|--------|
| `de` | German | `fakerDE` |
| `fr` | French | `fakerFR` |
| `es` | Spanish | `fakerES` |
| `it` | Italian | `fakerIT` |
| `pt_BR` | Portuguese (Brazil) | `fakerPT_BR` |
| `ja` | Japanese | `fakerJA` |
| `zh_CN` | Chinese (Simplified) | `fakerZH_CN` |
| `ko` | Korean | `fakerKO` |
| `ar` | Arabic | `fakerAR` |
| `nl` | Dutch | `fakerNL` |

**Detect Page Language:**

```javascript
// Get lang from HTML
const lang = document.documentElement.lang || 'en';

// Map to faker locale
const fakerLocales = {
  'en': faker,
  'de': fakerDE,
  'fr': fakerFR,
  'es': fakerES
};

const localFaker = fakerLocales[lang] || faker;
```

---

## Content Guidelines

### Text Length

| Content Type | Recommended Length |
|--------------|-------------------|
| Product name | 2-5 words |
| Product description | 15-30 words |
| Testimonial | 20-50 words |
| Bio | 15-25 words |
| Headline | 5-10 words |
| Article excerpt | 20-40 words |
| Article body | 5-10 paragraphs |
| FAQ question | 8-15 words |
| FAQ answer | 30-60 words |
| Event description | 20-40 words |
| Company tagline | 5-10 words |

### Realistic Proportions

```javascript
// Good: Realistic price range
faker.commerce.price({ min: 19.99, max: 299.99 })

// Good: Realistic rating
faker.number.float({ min: 3.5, max: 5, fractionDigits: 1 })

// Good: Varying review counts
faker.number.int({ min: 5, max: 500 })
```

### Consistency

Keep related data consistent within a section:

```javascript
// Generate person once, reuse data
const author = {
  firstName: faker.person.firstName(),
  lastName: faker.person.lastName()
};

// Use consistently
const fullName = `${author.firstName} ${author.lastName}`;
const email = faker.internet.email({
  firstName: author.firstName,
  lastName: author.lastName
});
```

---

## Seeding for Reproducibility

Use seeds to generate consistent data across runs:

```javascript
import { faker } from '@faker-js/faker';

// Set seed for reproducible results
faker.seed(12345);

// Same seed = same output every time
const name = faker.person.fullName(); // Always "John Smith"
```

---

## Generate Multiple Items

```javascript
import { faker } from '@faker-js/faker';

// Generate array of products
const products = faker.helpers.multiple(
  () => ({
    name: faker.commerce.productName(),
    price: faker.commerce.price(),
    description: faker.commerce.productDescription()
  }),
  { count: 10 }
);

// Generate with index
const items = faker.helpers.multiple(
  (_, index) => ({
    id: index + 1,
    name: faker.commerce.productName()
  }),
  { count: 5 }
);
```

---

## Quick Reference

| Need | Faker Method |
|------|-------------|
| Full name | `faker.person.fullName()` |
| First name | `faker.person.firstName()` |
| Email | `faker.internet.email()` |
| Phone | `faker.phone.number()` |
| Job title | `faker.person.jobTitle()` |
| Company | `faker.company.name()` |
| Catchphrase | `faker.company.catchPhrase()` |
| Product name | `faker.commerce.productName()` |
| Price | `faker.commerce.price()` |
| Department | `faker.commerce.department()` |
| Description | `faker.commerce.productDescription()` |
| Paragraph | `faker.lorem.paragraph()` |
| Paragraphs | `faker.lorem.paragraphs(5)` |
| Sentences | `faker.lorem.sentences(3)` |
| Recent date | `faker.date.recent()` |
| Future date | `faker.date.future()` |
| Street address | `faker.location.streetAddress()` |
| City | `faker.location.city()` |
| Country | `faker.location.country()` |
| UUID | `faker.string.uuid()` |
| URL | `faker.internet.url()` |
| Avatar URL | `faker.image.avatar()` |
| Random from array | `faker.helpers.arrayElement([...])` |
| Multiple items | `faker.helpers.multiple(fn, { count })` |

---

## Checklist

When generating fake content:

- [ ] Use faker methods, not lorem ipsum
- [ ] Match content length to context
- [ ] Keep related data consistent
- [ ] Use realistic value ranges
- [ ] Consider using seed for reproducibility
- [ ] Generate appropriate count for the UI

## Related Skills

- **content-author** - Write quality content for HTML documents
- **patterns** - Reusable HTML page patterns and component blocks
- **xhtml-author** - Write valid XHTML-strict HTML5 markup
- **placeholder-images** - Generate SVG placeholder images for prototypes
