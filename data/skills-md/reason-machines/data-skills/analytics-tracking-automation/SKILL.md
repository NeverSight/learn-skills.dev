---
name: analytics-tracking-automation
description: AI-powered GA4 + GTM event tracking automation — analyzes sites, designs event schemas, syncs GTM containers, runs preview verification, and publishes tracking implementations.
triggers:
  - set up GA4 and GTM tracking for my website
  - automate Google Analytics 4 event tracking setup
  - analyze this site and create a GTM tracking plan
  - generate GA4 event schema and sync to Google Tag Manager
  - audit my existing GTM container and tracking setup
  - create a tracking implementation for this Shopify store
  - help me plan and deploy analytics tracking
  - verify my GTM preview and publish the container
---

# Analytics Tracking Automation

> Skill by [ara.so](https://ara.so) — Data Skills collection.

This skill enables AI agents to plan, implement, and deploy GA4 + GTM tracking setups. It automates site analysis, page grouping, event schema design, GTM container synchronization, preview verification, and publishing—supporting both generic websites and Shopify storefronts.

## What This Skill Does

The `analytics-tracking-automation` project provides a local-first workflow that:

1. **Analyzes** a website by crawling pages and identifying business intent
2. **Groups pages** by purpose (e.g., product, pricing, contact)
3. **Designs event schemas** (GA4 events, parameters, triggers) based on site structure
4. **Syncs to GTM** by creating/updating tags, triggers, variables via Google Tag Manager API
5. **Verifies in preview** using automated Playwright-based checks
6. **Publishes** the GTM container version when verification passes
7. **Supports Shopify** with specialized tracking for cart, checkout, and purchase flows
8. **Maintains artifacts** for resumable, reviewable tracking work

## Installation

### For Use in AI Agent Environments

The recommended installation is to clone the repository and install the skill bundle:

```bash
git clone https://github.com/jtrackingai/analytics-tracking-automation.git
cd analytics-tracking-automation
npm install
npm run install:skills
```

This installs the umbrella skill into your agent's skills directory and makes the `event-tracking` CLI available.

### No-Clone Alternative

```bash
npx skills add jtrackingai/analytics-tracking-automation
```

### Verify Installation

```bash
npx event-tracking --version
```

The CLI requires Node.js 18+ and will auto-install Playwright Chromium on first `npm install`.

## Core CLI Commands

The `event-tracking` CLI is the primary interface. All commands accept `--help` for detailed options.

### Start a New Tracking Setup

```bash
npx event-tracking init \
  --url https://www.example.com \
  --output ./output \
  --ga4-measurement-id G-XXXXXXXXXX
```

This creates a site artifact directory under `./output/` (e.g., `./output/www_example_com/`) and runs:
- Site crawl and page classification
- Business intent page grouping
- Event schema generation
- Schema review checkpoint

### Resume an Existing Run

```bash
npx event-tracking resume \
  --artifact-dir ./output/www_example_com \
  --continue-through sync
```

Resumes from the last checkpoint and continues through the specified stage (`schema`, `sync`, `preview`, `publish`).

### Audit an Existing GTM Setup

```bash
npx event-tracking audit \
  --url https://www.example.com \
  --gtm-account-id 123456789 \
  --gtm-container-id 12345678 \
  --output ./output
```

Compares live GTM configuration against recommended tracking plan and produces a health report.

### Sync Schema to GTM

```bash
npx event-tracking sync \
  --artifact-dir ./output/www_example_com \
  --gtm-account-id 123456789 \
  --gtm-container-id 12345678
```

Creates/updates tags, triggers, and variables in GTM based on `event-schema.json`. Requires Google OAuth (prompted interactively).

### Verify GTM Preview

```bash
npx event-tracking verify \
  --artifact-dir ./output/www_example_com \
  --gtm-preview-url "https://tagmanager.google.com/?gtm_preview=..."
```

Runs automated browser checks against GTM preview mode, validates event firing, and produces a verification report.

### Publish GTM Container

```bash
npx event-tracking publish \
  --artifact-dir ./output/www_example_com \
  --gtm-account-id 123456789 \
  --gtm-container-id 12345678 \
  --version-name "v1.0 - Initial tracking"
```

Publishes the current workspace version to live.

### Shopify-Specific Setup

```bash
npx event-tracking init \
  --url https://store.example.com \
  --output ./output \
  --platform shopify \
  --ga4-measurement-id G-XXXXXXXXXX
```

Uses Shopify-optimized tracking (cart, checkout, purchase events).

## Configuration

### Environment Variables

```bash
# Google OAuth credentials (create in Google Cloud Console)
export GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
export GOOGLE_CLIENT_SECRET=your-client-secret

# Optional: GA4 Measurement ID
export GA4_MEASUREMENT_ID=G-XXXXXXXXXX

# Optional: GTM Account/Container IDs
export GTM_ACCOUNT_ID=123456789
export GTM_CONTAINER_ID=12345678
```

### OAuth Setup

To sync with GTM, you need Google OAuth credentials:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project and enable Tag Manager API
3. Create OAuth 2.0 credentials (Desktop app type)
4. Set redirect URI to `http://localhost:3000/oauth/callback`
5. Export `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`

First sync will open a browser for OAuth consent. Credentials are cached in the artifact directory (`oauth-tokens.json`).

## Artifact Directory Structure

Each site run creates an artifact directory like `./output/www_example_com/`:

```
www_example_com/
├── site-analysis.json          # Crawl results, page inventory
├── page-groups.json            # Business intent groupings
├── event-schema.json           # GA4 events, parameters, triggers
├── gtm-sync-result.json        # GTM API operation results
├── verification-report.json    # Preview verification checks
├── oauth-tokens.json           # Cached OAuth credentials
└── checkpoint.json             # Last completed stage
```

These files are reviewable, editable, and resumable.

## TypeScript API Examples

### Programmatic Site Analysis

```typescript
import { analyzeSite } from 'analytics-tracking-automation';

async function analyzeSiteExample() {
  const result = await analyzeSite({
    url: 'https://www.example.com',
    outputDir: './output',
    maxPages: 100,
    includeSubdomains: false,
  });

  console.log('Pages discovered:', result.pages.length);
  console.log('Page groups:', result.pageGroups);
  console.log('Recommended events:', result.events.length);
}
```

### Generate Event Schema

```typescript
import { generateEventSchema } from 'analytics-tracking-automation';

async function generateSchemaExample() {
  const schema = await generateEventSchema({
    artifactDir: './output/www_example_com',
    pageGroups: ['home', 'product', 'pricing', 'contact'],
    businessGoals: ['signup', 'purchase', 'demo_request'],
  });

  console.log('Generated events:', schema.events);
  console.log('Event parameters:', schema.parameters);
  console.log('GTM triggers:', schema.triggers);
}
```

### Sync to GTM

```typescript
import { syncToGTM } from 'analytics-tracking-automation';

async function syncExample() {
  const syncResult = await syncToGTM({
    artifactDir: './output/www_example_com',
    gtmAccountId: process.env.GTM_ACCOUNT_ID!,
    gtmContainerId: process.env.GTM_CONTAINER_ID!,
    oauthCredentials: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    },
  });

  console.log('Tags created:', syncResult.tagsCreated);
  console.log('Triggers created:', syncResult.triggersCreated);
  console.log('Variables created:', syncResult.variablesCreated);
}
```

### Verify Preview

```typescript
import { verifyPreview } from 'analytics-tracking-automation';

async function verifyExample() {
  const report = await verifyPreview({
    artifactDir: './output/www_example_com',
    gtmPreviewUrl: 'https://tagmanager.google.com/?gtm_preview=...',
    testPages: [
      { url: 'https://www.example.com/', expectedEvents: ['page_view'] },
      { url: 'https://www.example.com/pricing', expectedEvents: ['page_view', 'view_pricing'] },
      { url: 'https://www.example.com/contact', expectedEvents: ['page_view', 'contact_intent'] },
    ],
  });

  console.log('Checks passed:', report.passed);
  console.log('Checks failed:', report.failed);
  console.log('Issues:', report.issues);
}
```

### Publish Container

```typescript
import { publishContainer } from 'analytics-tracking-automation';

async function publishExample() {
  const result = await publishContainer({
    gtmAccountId: process.env.GTM_ACCOUNT_ID!,
    gtmContainerId: process.env.GTM_CONTAINER_ID!,
    versionName: 'v1.0 - Initial tracking setup',
    versionDescription: 'GA4 events for core user journeys',
    oauthCredentials: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    },
  });

  console.log('Published version:', result.publishedVersion);
  console.log('Live container URL:', result.containerUrl);
}
```

## Common Patterns

### Full End-to-End Setup

```typescript
import {
  analyzeSite,
  generateEventSchema,
  syncToGTM,
  verifyPreview,
  publishContainer,
} from 'analytics-tracking-automation';

async function fullSetup(url: string, outputRoot: string) {
  // 1. Analyze site
  const analysis = await analyzeSite({ url, outputDir: outputRoot });
  const artifactDir = analysis.artifactDir;

  // 2. Generate schema
  const schema = await generateEventSchema({ artifactDir });

  // 3. Review (manual checkpoint)
  console.log('Review schema before syncing:', schema);
  // User reviews and edits event-schema.json if needed

  // 4. Sync to GTM
  const syncResult = await syncToGTM({
    artifactDir,
    gtmAccountId: process.env.GTM_ACCOUNT_ID!,
    gtmContainerId: process.env.GTM_CONTAINER_ID!,
    oauthCredentials: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    },
  });

  // 5. Enter GTM preview mode manually, then verify
  const previewUrl = '...'; // GTM preview URL from user
  const verifyReport = await verifyPreview({ artifactDir, gtmPreviewUrl: previewUrl });

  if (verifyReport.passed === verifyReport.total) {
    // 6. Publish
    await publishContainer({
      gtmAccountId: process.env.GTM_ACCOUNT_ID!,
      gtmContainerId: process.env.GTM_CONTAINER_ID!,
      versionName: 'v1.0 - Automated setup',
      oauthCredentials: {
        clientId: process.env.GOOGLE_CLIENT_ID!,
        clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
      },
    });
    console.log('Published successfully');
  } else {
    console.error('Verification failed, fix issues before publishing');
  }
}
```

### Shopify Tracking Setup

```typescript
import { analyzeSite, generateEventSchema, syncToGTM } from 'analytics-tracking-automation';

async function shopifySetup(storeUrl: string) {
  const analysis = await analyzeSite({
    url: storeUrl,
    outputDir: './output',
    platform: 'shopify',
  });

  const schema = await generateEventSchema({
    artifactDir: analysis.artifactDir,
    platform: 'shopify',
    shopifyEvents: ['add_to_cart', 'begin_checkout', 'purchase'],
  });

  await syncToGTM({
    artifactDir: analysis.artifactDir,
    gtmAccountId: process.env.GTM_ACCOUNT_ID!,
    gtmContainerId: process.env.GTM_CONTAINER_ID!,
    platform: 'shopify',
    oauthCredentials: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    },
  });

  console.log('Shopify tracking synced. Manual verification required in Shopify admin.');
}
```

### Audit Existing Setup

```typescript
import { auditGTM } from 'analytics-tracking-automation';

async function auditExample(url: string) {
  const auditReport = await auditGTM({
    url,
    gtmAccountId: process.env.GTM_ACCOUNT_ID!,
    gtmContainerId: process.env.GTM_CONTAINER_ID!,
    outputDir: './output',
    oauthCredentials: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    },
  });

  console.log('Healthy tags:', auditReport.healthy);
  console.log('Drifted tags:', auditReport.drifted);
  console.log('Missing events:', auditReport.missing);
  console.log('Recommendations:', auditReport.recommendations);
}
```

### Resume from Checkpoint

```typescript
import { resumeWorkflow } from 'analytics-tracking-automation';

async function resumeExample(artifactDir: string) {
  const result = await resumeWorkflow({
    artifactDir,
    continueThrough: 'publish', // 'schema' | 'sync' | 'preview' | 'publish'
  });

  console.log('Resumed from:', result.lastCheckpoint);
  console.log('Completed through:', result.completedStage);
}
```

## Debugging and Troubleshooting

### Selector Debugging with Playwright

If preview verification reports selector mismatches or events not firing:

```bash
# Open site in headed browser for visual inspection
npm run debug:open -- https://www.example.com

# Launch codegen to capture correct selectors
npm run debug:codegen -- https://www.example.com
```

Then update selectors in `event-schema.json`:

```json
{
  "events": [
    {
      "eventName": "click_cta",
      "trigger": {
        "type": "click",
        "selector": "button.cta-button" // Updated selector
      }
    }
  ]
}
```

### OAuth Token Issues

If OAuth fails or tokens are stale:

```bash
# Remove cached tokens
rm ./output/www_example_com/oauth-tokens.json

# Re-run sync to trigger new OAuth flow
npx event-tracking sync --artifact-dir ./output/www_example_com
```

### GTM API Errors

Common GTM API issues:

- **401 Unauthorized**: OAuth credentials invalid or expired
- **403 Forbidden**: User lacks GTM account/container permissions
- **404 Not Found**: GTM account or container ID incorrect
- **429 Rate Limit**: Too many API requests; add delays between operations

Check GTM permissions: User must have at least "Publish" access to the container.

### Preview Verification Failures

If automated verification fails:

1. **Check GTM Preview URL**: Must be active and match container
2. **Inspect browser logs**: Add `--verbose` flag for detailed Playwright logs
3. **Test manually**: Open preview URL in browser, check dataLayer in console
4. **Validate selectors**: Use `npm run debug:codegen` to verify element targeting
5. **Network issues**: Ensure site is accessible and not behind VPN/firewall

### Shopify Manual Verification

Shopify tracking requires manual verification in Shopify admin:

1. Install GTM via Shopify admin (Settings → Online Store → Preferences)
2. Add GTM container ID
3. Test checkout flow in preview mode
4. Verify `add_to_cart`, `begin_checkout`, `purchase` events in GTM debug view

### Common Event Schema Fixes

Fix missing events:

```json
{
  "events": [
    {
      "eventName": "form_submit",
      "trigger": {
        "type": "formSubmit",
        "selector": "form#contact-form"
      },
      "parameters": {
        "form_id": "contact-form",
        "form_destination": "contact"
      }
    }
  ]
}
```

Fix parameter mapping:

```json
{
  "parameters": {
    "page_type": {
      "type": "dataLayer",
      "source": "pageType"
    },
    "user_id": {
      "type": "cookie",
      "source": "user_id"
    }
  }
}
```

### Telemetry Configuration

Anonymous startup signals are sent by default. Opt out:

```bash
npx event-tracking config telemetry --disable
```

Richer diagnostics (opt-in):

```bash
npx event-tracking config telemetry --enable-diagnostics
```

Check current preference:

```bash
npx event-tracking config telemetry --show
```

## Advanced Configuration

### Custom Crawler Settings

Edit artifact `site-analysis.json` before schema generation:

```json
{
  "crawlConfig": {
    "maxPages": 200,
    "includeSubdomains": true,
    "excludePatterns": ["/blog/*", "/admin/*"],
    "followExternalLinks": false
  }
}
```

### Custom Page Grouping

Override auto-generated page groups in `page-groups.json`:

```json
{
  "groups": [
    {
      "name": "conversion",
      "intent": "purchase",
      "patterns": ["/checkout/*", "/cart", "/order-confirmation"]
    },
    {
      "name": "support",
      "intent": "help",
      "patterns": ["/help/*", "/faq", "/contact"]
    }
  ]
}
```

### Event Schema Customization

Manually edit `event-schema.json` for fine-grained control:

```json
{
  "events": [
    {
      "eventName": "custom_conversion",
      "trigger": {
        "type": "click",
        "selector": "button[data-track='conversion']"
      },
      "parameters": {
        "conversion_type": {
          "type": "element",
          "source": "data-conversion-type"
        },
        "conversion_value": {
          "type": "element",
          "source": "data-value"
        }
      },
      "conditions": {
        "pagePathContains": "/pricing"
      }
    }
  ]
}
```

## When to Use This Skill

This skill is ideal when:

- Setting up GA4 + GTM tracking from scratch
- Auditing or refactoring existing tracking implementations
- Implementing Shopify storefront tracking
- Automating repetitive tracking tasks across multiple sites
- Needing reviewable, resumable tracking workflows
- Working with non-technical stakeholders who need business-friendly artifacts

This skill is NOT ideal for:

- Real-time production debugging (use GTM Debug View instead)
- Server-side tracking or custom measurement protocols
- Multi-destination tracking (Adobe, Segment, etc.) without GTM
- Sites requiring authentication or complex session flows

## Key Files and Extension Points

- **`src/core/analyzer.ts`**: Site crawl and page classification logic
- **`src/core/schema-generator.ts`**: Event schema generation
- **`src/core/gtm-sync.ts`**: GTM API integration
- **`src/core/verifier.ts`**: Automated preview verification
- **`src/platforms/shopify.ts`**: Shopify-specific tracking
- **`event-schema.json`**: Editable event schema artifact
- **`page-groups.json`**: Editable page grouping artifact

Extend by forking and modifying these files, or by editing artifacts between CLI stages.

## Further Reading

- **Skill contract**: See `SKILL.md` in repository for agent-facing workflow details
- **Developer guide**: See `DEVELOPING.md` for CLI internals and maintainer workflow
- **Skill installation**: See `docs/README.install.md` for advanced install options
- **JTracking website**: [https://www.jtracking.ai/skills](https://www.jtracking.ai/skills)

## Support

For issues, questions, or feature requests, contact [support@jtracking.ai](mailto:support@jtracking.ai) or open an issue on GitHub.
