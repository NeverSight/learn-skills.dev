---
name: worldmonitor-intelligence-dashboard
description: Real-time global intelligence dashboard with AI-powered news aggregation, geopolitical monitoring, and infrastructure tracking
triggers:
  - set up worldmonitor dashboard
  - add geopolitical monitoring to my app
  - integrate worldmonitor news feeds
  - build situational awareness dashboard
  - configure worldmonitor AI intelligence
  - self-host worldmonitor
  - add OSINT dashboard to project
  - worldmonitor map layers and data feeds
---

# World Monitor Intelligence Dashboard

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

World Monitor is a real-time global intelligence dashboard combining AI-powered news aggregation (435+ feeds, 15 categories), dual map engine (3D globe + WebGL flat map with 45 data layers), geopolitical risk scoring, finance radar (92 exchanges), and cross-stream signal correlation — all from a single TypeScript/Vite codebase deployable as web, PWA, or native desktop (Tauri 2).

---

## Installation & Quick Start

```bash
git clone https://github.com/koala73/worldmonitor.git
cd worldmonitor
npm install
npm run dev          # Opens http://localhost:5173
```

No environment variables required for basic operation. All features work with local Ollama by default.

### Site Variants

```bash
npm run dev:tech       # tech.worldmonitor.app variant
npm run dev:finance    # finance.worldmonitor.app variant
npm run dev:commodity  # commodity.worldmonitor.app variant
npm run dev:happy      # happy.worldmonitor.app variant
```

### Production Build

```bash
npm run typecheck        # TypeScript validation
npm run build:full       # Build all variants
npm run build            # Build default (world) variant
```

---

## Project Structure

```
worldmonitor/
├── src/
│   ├── components/       # UI components (TypeScript)
│   ├── feeds/            # 435+ RSS/API feed definitions
│   ├── layers/           # Map data layers (deck.gl)
│   ├── ai/               # AI synthesis pipeline
│   ├── signals/          # Cross-stream correlation engine
│   ├── finance/          # Market data (92 exchanges)
│   ├── variants/         # Site variant configs (world/tech/finance/commodity/happy)
│   └── protos/           # Protocol Buffer definitions (92 protos, 22 services)
├── api/                  # Vercel Edge Functions (60+)
├── src-tauri/            # Tauri 2 desktop app (Rust)
├── docs/                 # Documentation source
└── vite.config.ts
```

---

## Environment Variables

Create a `.env.local` file (never commit secrets):

```bash
# AI Providers (all optional — Ollama works with no keys)
VITE_OLLAMA_BASE_URL=http://localhost:11434       # Local Ollama instance
VITE_GROQ_API_KEY=$GROQ_API_KEY                  # Groq cloud inference
VITE_OPENROUTER_API_KEY=$OPENROUTER_API_KEY      # OpenRouter multi-model

# Caching (optional, improves performance)
UPSTASH_REDIS_REST_URL=$UPSTASH_REDIS_REST_URL
UPSTASH_REDIS_REST_TOKEN=$UPSTASH_REDIS_REST_TOKEN

# Map tiles (optional, MapLibre GL)
VITE_MAPTILER_API_KEY=$MAPTILER_API_KEY

# Variant selection
VITE_SITE_VARIANT=world   # world | tech | finance | commodity | happy
```

---

## Core Concepts

### Feed Categories

World Monitor aggregates 435+ feeds across 15 categories:

```typescript
// src/feeds/categories.ts pattern
import type { FeedCategory } from './types';

const FEED_CATEGORIES: FeedCategory[] = [
  'geopolitics',
  'military',
  'economics',
  'technology',
  'climate',
  'energy',
  'health',
  'finance',
  'commodities',
  'infrastructure',
  'cyber',
  'space',
  'diplomacy',
  'disasters',
  'society',
];
```

### Country Intelligence Index

Composite risk scoring across 12 signal categories per country:

```typescript
// Example: accessing country risk scores
import { CountryIntelligence } from './signals/country-intelligence';

const intel = new CountryIntelligence();

// Get composite risk score for a country
const score = await intel.getCountryScore('UA');
console.log(score);
// {
//   composite: 0.82,
//   signals: {
//     military: 0.91,
//     economic: 0.74,
//     political: 0.88,
//     humanitarian: 0.79,
//     ...
//   },
//   trend: 'escalating',
//   updatedAt: '2026-03-17T08:00:00Z'
// }

// Subscribe to real-time updates
intel.subscribe('UA', (update) => {
  console.log('Risk update:', update);
});
```

### AI Synthesis Pipeline

```typescript
// src/ai/synthesize.ts pattern
import { AISynthesizer } from './ai/synthesizer';

const synth = new AISynthesizer({
  provider: 'ollama',           // 'ollama' | 'groq' | 'openrouter'
  model: 'llama3.2',            // any Ollama-compatible model
  baseUrl: process.env.VITE_OLLAMA_BASE_URL,
});

// Synthesize a news brief from multiple feed items
const brief = await synth.synthesize({
  items: feedItems,             // FeedItem[]
  category: 'geopolitics',
  region: 'Europe',
  maxTokens: 500,
  language: 'en',
});

console.log(brief.summary);    // AI-generated synthesis
console.log(brief.signals);    // Extracted signals array
console.log(brief.confidence); // 0-1 confidence score
```

### Cross-Stream Signal Correlation

```typescript
// src/signals/correlator.ts pattern
import { SignalCorrelator } from './signals/correlator';

const correlator = new SignalCorrelator();

// Detect convergence across military, economic, disaster signals
const convergence = await correlator.detectConvergence({
  streams: ['military', 'economic', 'disaster', 'escalation'],
  timeWindow: '6h',
  threshold: 0.7,
  region: 'Middle East',
});

if (convergence.detected) {
  console.log('Convergence signals:', convergence.signals);
  console.log('Escalation probability:', convergence.probability);
  console.log('Contributing events:', convergence.events);
}
```

---

## Map Engine Integration

### 3D Globe (globe.gl)

```typescript
// src/components/globe/GlobeView.ts
import Globe from 'globe.gl';
import { getCountryRiskData } from '../signals/country-intelligence';

export function initGlobe(container: HTMLElement) {
  const globe = Globe()(container)
    .globeImageUrl('//unpkg.com/three-globe/example/img/earth-dark.jpg')
    .backgroundImageUrl('//unpkg.com/three-globe/example/img/night-sky.png');

  // Load country risk layer
  const riskData = await getCountryRiskData();

  globe
    .polygonsData(riskData.features)
    .polygonCapColor(feat => riskToColor(feat.properties.riskScore))
    .polygonSideColor(() => 'rgba(0, 100, 0, 0.15)')
    .polygonLabel(({ properties: d }) =>
      `<b>${d.name}</b><br/>Risk: ${(d.riskScore * 100).toFixed(0)}%`
    );

  return globe;
}

function riskToColor(score: number): string {
  if (score > 0.8) return 'rgba(220, 38, 38, 0.8)';   // critical
  if (score > 0.6) return 'rgba(234, 88, 12, 0.7)';   // high
  if (score > 0.4) return 'rgba(202, 138, 4, 0.6)';   // elevated
  if (score > 0.2) return 'rgba(22, 163, 74, 0.5)';   // low
  return 'rgba(15, 118, 110, 0.4)';                    // minimal
}
```

### WebGL Flat Map (deck.gl + MapLibre GL)

```typescript
// src/components/map/DeckMap.ts
import { Deck } from '@deck.gl/core';
import { ScatterplotLayer, ArcLayer, HeatmapLayer } from '@deck.gl/layers';
import maplibregl from 'maplibre-gl';

export function initDeckMap(container: HTMLElement) {
  const map = new maplibregl.Map({
    container,
    style: 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json',
    center: [0, 20],
    zoom: 2,
  });

  const deck = new Deck({
    canvas: 'deck-canvas',
    initialViewState: { longitude: 0, latitude: 20, zoom: 2 },
    controller: true,
    layers: [
      // Event scatter layer
      new ScatterplotLayer({
        id: 'events',
        data: getActiveEvents(),
        getPosition: d => [d.lng, d.lat],
        getRadius: d => d.severity * 50000,
        getFillColor: d => severityToRGBA(d.severity),
        pickable: true,
      }),
      // Supply chain arc layer
      new ArcLayer({
        id: 'supply-chains',
        data: getSupplyChainData(),
        getSourcePosition: d => d.source,
        getTargetPosition: d => d.target,
        getSourceColor: [0, 128, 200],
        getTargetColor: [200, 0, 80],
        getWidth: 2,
      }),
    ],
  });

  return { map, deck };
}
```

---

## Finance Radar

```typescript
// src/finance/radar.ts pattern
import { FinanceRadar } from './finance/radar';

const radar = new FinanceRadar();

// Get market composite (7-signal)
const composite = await radar.getMarketComposite();
console.log(composite);
// {
//   score: 0.62,
//   signals: {
//     volatility: 0.71,
//     momentum: 0.58,
//     sentiment: 0.65,
//     liquidity: 0.44,
//     correlation: 0.78,
//     macro: 0.61,
//     geopolitical: 0.82
//   },
//   exchanges: 92,
//   timestamp: '2026-03-17T08:00:00Z'
// }

// Watch specific exchange
const exchange = await radar.getExchange('NYSE');
const crypto = await radar.getCrypto(['BTC', 'ETH', 'SOL']);
const commodities = await radar.getCommodities(['GOLD', 'OIL', 'WHEAT']);
```

---

## Language & RTL Support

World Monitor supports 21 languages with native-language feeds:

```typescript
// src/i18n/config.ts pattern
import { setLanguage, getAvailableLanguages } from './i18n';

const languages = getAvailableLanguages();
// ['en', 'ar', 'zh', 'ru', 'fr', 'es', 'de', 'ja', 'ko', 'pt',
//  'hi', 'fa', 'tr', 'pl', 'uk', 'nl', 'sv', 'he', 'it', 'vi', 'id']

// Switch language (handles RTL automatically)
await setLanguage('ar');  // Arabic — triggers RTL layout
await setLanguage('he');  // Hebrew — triggers RTL layout
await setLanguage('fa');  // Farsi — triggers RTL layout

// Configure feed language filtering
import { FeedManager } from './feeds/manager';
const feeds = new FeedManager({ language: 'ar', includeEnglish: true });
```

---

## Protocol Buffers (API Contracts)

```typescript
// src/protos — 92 proto definitions, 22 services
// Example generated client usage:

import { IntelligenceServiceClient } from './protos/generated/intelligence_grpc_web_pb';
import { CountryRequest } from './protos/generated/intelligence_pb';

const client = new IntelligenceServiceClient(
  process.env.VITE_API_BASE_URL || 'http://localhost:8080'
);

const request = new CountryRequest();
request.setCountryCode('DE');
request.setTimeRange('24h');
request.setSignalTypes(['military', 'economic', 'political']);

client.getCountryIntelligence(request, {}, (err, response) => {
  if (err) console.error(err);
  else console.log(response.toObject());
});
```

---

## Vercel Edge Function Pattern

```typescript
// api/feeds/aggregate.ts — Edge Function example
import type { VercelRequest, VercelResponse } from '@vercel/node';
import { aggregateFeeds } from '../../src/feeds/aggregator';
import { getCachedData, setCachedData } from '../../src/cache/redis';

export const config = { runtime: 'edge' };

export default async function handler(req: VercelRequest, res: VercelResponse) {
  const { category, region, limit = '20' } = req.query as Record<string, string>;

  const cacheKey = `feeds:${category}:${region}:${limit}`;
  const cached = await getCachedData(cacheKey);
  if (cached) return res.json(cached);

  const items = await aggregateFeeds({
    categories: category ? [category] : undefined,
    region,
    limit: parseInt(limit),
  });

  await setCachedData(cacheKey, items, { ttl: 300 }); // 5 min TTL
  return res.json(items);
}
```

---

## Desktop App (Tauri 2)

```bash
# Install Tauri CLI
cargo install tauri-cli

# Development
npm run tauri:dev

# Build native app
npm run tauri:build
# Outputs: .exe (Windows), .dmg/.app (macOS), .AppImage (Linux)
```

```rust
// src-tauri/src/main.rs — IPC command example
#[tauri::command]
async fn fetch_intelligence(country: String) -> Result<CountryData, String> {
    // Sidecar Node.js process handles feed aggregation
    // Tauri handles secure IPC between renderer and backend
    Ok(CountryData::default())
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![fetch_intelligence])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

---

## Docker / Self-Hosting

```bash
# Docker single-container
docker build -t worldmonitor .
docker run -p 3000:3000 \
  -e VITE_SITE_VARIANT=world \
  -e UPSTASH_REDIS_REST_URL=$UPSTASH_REDIS_REST_URL \
  -e UPSTASH_REDIS_REST_TOKEN=$UPSTASH_REDIS_REST_TOKEN \
  worldmonitor

# Docker Compose with Redis
docker compose up -d
```

```yaml
# docker-compose.yml
version: '3.9'
services:
  app:
    build: .
    ports: ['3000:3000']
    environment:
      - VITE_SITE_VARIANT=world
      - REDIS_URL=redis://redis:6379
    depends_on: [redis]
  redis:
    image: redis:7-alpine
    volumes: ['redis_data:/data']
volumes:
  redis_data:
```

### Vercel Deployment

```bash
npm i -g vercel
vercel --prod
# Set env vars in Vercel dashboard or via CLI:
vercel env add GROQ_API_KEY production
vercel env add UPSTASH_REDIS_REST_URL production
vercel env add UPSTASH_REDIS_REST_TOKEN production
```

---

## Common Patterns

### Custom Feed Integration

```typescript
// Add a custom RSS feed to the aggregation pipeline
import { FeedRegistry } from './src/feeds/registry';

FeedRegistry.register({
  id: 'my-custom-feed',
  name: 'My Intelligence Source',
  url: 'https://example.com/feed.xml',
  category: 'geopolitics',
  region: 'Asia',
  language: 'en',
  weight: 0.8,           // 0-1, affects signal weighting
  refreshInterval: 300,  // seconds
  parser: 'rss2',        // 'rss2' | 'atom' | 'json'
});
```

### Custom Map Layer

```typescript
// Register a custom deck.gl layer in the 45-layer system
import { LayerRegistry } from './src/layers/registry';
import { IconLayer } from '@deck.gl/layers';

LayerRegistry.register({
  id: 'my-custom-layer',
  name: 'Custom Events',
  category: 'infrastructure',
  defaultVisible: false,
  factory: (data) => new IconLayer({
    id: 'my-custom-layer-deck',
    data,
    getPosition: d => [d.lng, d.lat],
    getIcon: d => 'marker',
    getSize: 32,
    pickable: true,
  }),
});
```

### Site Variant Configuration

```typescript
// src/variants/my-variant.ts
import type { SiteVariant } from './types';

export const myVariant: SiteVariant = {
  id: 'my-variant',
  name: 'My Monitor',
  title: 'My Custom Monitor',
  defaultCategories: ['geopolitics', 'economics', 'military'],
  defaultRegion: 'Europe',
  defaultLanguage: 'en',
  mapStyle: 'dark',
  enabledLayers: ['country-risk', 'events', 'supply-chains'],
  aiProvider: 'ollama',
  theme: {
    primary: '#0891b2',
    background: '#0f172a',
    surface: '#1e293b',
  },
};
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Map not rendering | Check `VITE_MAPTILER_API_KEY` or use free CartoBasemap style |
| AI synthesis slow/failing | Ensure Ollama is running: `ollama serve && ollama pull llama3.2` |
| Feeds returning 429 errors | Enable Redis caching via `UPSTASH_REDIS_REST_*` env vars |
| Desktop app won't build | Ensure Rust + `cargo install tauri-cli` + platform build tools |
| RTL layout broken | Confirm `lang` attribute set on `<html>` by `setLanguage()` |
| TypeScript errors on build | Run `npm run typecheck` — proto generated files must exist |
| Redis connection refused | Check `REDIS_URL` or use Upstash REST API instead of TCP |
| `npm run build:full` fails mid-variant | Build individually: `npm run build -- --mode finance` |

### Ollama Setup for Local AI

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull recommended model
ollama pull llama3.2          # Fast, good quality
ollama pull mistral           # Alternative
ollama pull gemma2:9b         # Larger, higher quality

# Verify Ollama is accessible
curl http://localhost:11434/api/tags
```

### Verify Installation

```bash
npm run typecheck   # Should exit 0
npm run dev         # Should open localhost:5173
# Navigate to /api/health for API status
curl http://localhost:5173/api/health
```

---

## Resources

- **Live App**: [worldmonitor.app](https://worldmonitor.app)
- **Documentation**: [docs.worldmonitor.app](https://docs.worldmonitor.app)
- **Architecture**: [docs.worldmonitor.app/architecture](https://docs.worldmonitor.app/architecture)
- **Self-Hosting Guide**: [docs.worldmonitor.app/getting-started](https://docs.worldmonitor.app/getting-started)
- **Contributing**: [docs.worldmonitor.app/contributing](https://docs.worldmonitor.app/contributing)
- **Security Policy**: [SECURITY.md](https://github.com/koala73/worldmonitor/blob/main/SECURITY.md)
- **License**: AGPL-3.0 (non-commercial); commercial license required for SaaS/rebranding
