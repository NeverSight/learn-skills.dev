---
name: acgti-anime-persona-quiz
description: ACG Type Indicator — MBTI-inspired anime character persona quiz built with Vue 3, TypeScript, and Vite
triggers:
  - add a new character to ACGTI
  - add quiz questions to the anime personality test
  - how do I extend the ACGTI character database
  - modify ACGTI archetype definitions
  - customize the ACGTI quiz scoring engine
  - deploy ACGTI to Cloudflare Pages
  - how does ACGTI calculate quiz results
  - set up ACGTI locally for development
---

# ACGTI Anime Persona Quiz

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

ACGTI (ACG Type Indicator) is a purely client-side Vue 3 + TypeScript quiz that maps 39 seven-point Likert-scale questions onto four MBTI dimensions (E/I, S/N, T/F, J/P), matches the result to one of 8 anime archetypes, and then selects a specific anime character from a 40+ entry database. No backend, no user data collection — everything runs in the browser.

---

## Installation & Local Development

```bash
# Clone the repo
git clone https://github.com/tianxingleo/ACGTI.git
cd ACGTI

# Install dependencies (Node 18+ recommended)
npm install

# Start dev server (Vite, hot-reload)
npm run dev

# Type-check
npx tsc --noEmit

# Production build → dist/
npm run build

# Preview production build locally
npm run preview
```

The `dist/` folder uses `base: './'` (relative paths), so it deploys directly to any static host.

---

## Project Architecture

```
src/
├── components/          # Reusable UI (QuestionCard, ResultSummary, SharePoster …)
├── composables/
│   ├── useQuiz.ts       # Quiz state machine & answer logic
│   └── useShare.ts      # PNG poster export
├── data/                # ALL content lives here as JSON
│   ├── questions.json
│   ├── archetypes.json
│   ├── characters.json
│   ├── characterVisuals.json
│   └── characterProbabilities.json
├── pages/               # Vue route-level components
├── types/quiz.ts        # Shared TypeScript types
├── utils/
│   ├── quizEngine.ts    # Score → archetype → character pipeline
│   ├── characterVisuals.ts
│   ├── characterProbability.ts
│   └── storage.ts       # localStorage helpers
└── router/index.ts
```

---

## Core Types (`src/types/quiz.ts`)

Understanding these types is essential before touching any data file or engine logic.

```typescript
// MBTI dimension keys
export type Dimension = 'EI' | 'SN' | 'TF' | 'JP';

// One question entry
export interface Question {
  id: number;
  text: string;
  dimension: Dimension;
  archetypeWeights: Record<string, number>; // archetype id → weight (-3..+3)
  tags?: string[];
}

// One of 8 archetypes
export interface Archetype {
  id: string;           // e.g. "glowing-protagonist"
  name: string;
  mbtiTypes: string[];  // e.g. ["ENFJ","ENFP"]
  description: string;
  strengths: string[];
  weaknesses: string[];
  color: string;        // hex
}

// Anime character entry
export interface Character {
  id: string;           // unique slug, becomes the "character code"
  name: string;
  series: string;
  mbtiType: string;     // e.g. "ENFJ"
  archetypeId: string;
  tags: string[];
  stats: {              // 0–100 six-axis radar
    energy: number;
    intuition: number;
    empathy: number;
    logic: number;
    order: number;
    chaos: number;
  };
}

// Visual theming per character
export interface CharacterVisual {
  characterId: string;
  portraitUrl: string;
  backgroundUrl: string;
  primaryColor: string;
  accentColor: string;
}

// Final computed result passed to ResultPage
export interface QuizResult {
  mbtiType: string;               // e.g. "INFP"
  dimensionScores: Record<Dimension, number>; // 50–100, direction-normalised
  archetypeId: string;
  characterId: string;
}
```

---

## Scoring Engine (`src/utils/quizEngine.ts`)

The engine is a pure function pipeline — ideal extension point.

```typescript
import questions from '@/data/questions.json';
import archetypes from '@/data/archetypes.json';
import characters from '@/data/characters.json';
import type { Dimension, QuizResult } from '@/types/quiz';

type Answers = Record<number, number>; // questionId → -3..+3

/** Step 1: Sum raw signed scores per MBTI dimension */
function calcDimensionRaw(answers: Answers): Record<Dimension, number> {
  const raw: Record<Dimension, number> = { EI: 0, SN: 0, TF: 0, JP: 0 };
  for (const q of questions) {
    const val = answers[q.id] ?? 0;
    raw[q.dimension as Dimension] += val;
  }
  return raw;
}

/** Step 2: Normalise to 50–100 (50 = perfectly balanced) */
function normaliseDimension(raw: number, questionCount: number): number {
  const max = questionCount * 3;           // maximum possible absolute value
  const clamped = Math.max(-max, Math.min(max, raw));
  return Math.round(50 + (Math.abs(clamped) / max) * 50);
}

/** Step 3: Derive MBTI letter for one dimension */
function mbtiLetter(dimension: Dimension, raw: number): string {
  const positive: Record<Dimension, string> = { EI: 'E', SN: 'N', TF: 'T', JP: 'J' };
  const negative: Record<Dimension, string> = { EI: 'I', SN: 'S', TF: 'F', JP: 'P' };
  return raw >= 0 ? positive[dimension] : negative[dimension];
}

/** Full pipeline */
export function computeResult(answers: Answers): QuizResult {
  const dims: Dimension[] = ['EI', 'SN', 'TF', 'JP'];
  const raw = calcDimensionRaw(answers);

  // Count questions per dimension for normalisation
  const countPerDim = dims.reduce((acc, d) => {
    acc[d] = questions.filter(q => q.dimension === d).length;
    return acc;
  }, {} as Record<Dimension, number>);

  const dimensionScores = dims.reduce((acc, d) => {
    acc[d] = normaliseDimension(raw[d], countPerDim[d]);
    return acc;
  }, {} as Record<Dimension, number>);

  const mbtiType = dims.map(d => mbtiLetter(d, raw[d])).join('');

  // Match archetype (archetypes list mbtiTypes they cover)
  const archetype = archetypes.find(a => a.mbtiTypes.includes(mbtiType))
    ?? archetypes[0];

  // Pick best-fit character within archetype
  const candidates = characters.filter(c => c.archetypeId === archetype.id);
  // Default: first match; extendable with probability weighting
  const character = candidates[0];

  return {
    mbtiType,
    dimensionScores,
    archetypeId: archetype.id,
    characterId: character.id,
  };
}
```

---

## Adding a New Character

Edit `src/data/characters.json` — append one object following the schema:

```json
{
  "id": "hatsune-miku",
  "name": "初音ミク",
  "series": "VOCALOID",
  "mbtiType": "ENFP",
  "archetypeId": "chaotic-spark",
  "tags": ["vocaloid", "energetic", "creative"],
  "stats": {
    "energy": 90,
    "intuition": 85,
    "empathy": 75,
    "logic": 50,
    "order": 40,
    "chaos": 80
  }
}
```

Then add the matching visual entry to `src/data/characterVisuals.json`:

```json
{
  "characterId": "hatsune-miku",
  "portraitUrl": "https://your-cdn.example.com/miku-portrait.webp",
  "backgroundUrl": "https://your-cdn.example.com/miku-bg.webp",
  "primaryColor": "#39C5BB",
  "accentColor": "#86EFDF"
}
```

And an optional prior probability in `src/data/characterProbabilities.json`:

```json
{
  "characterId": "hatsune-miku",
  "baseProbability": 0.15
}
```

> **Rules:**  
> • `id` must be unique and kebab-case.  
> • `mbtiType` must be one of the 16 standard types.  
> • `archetypeId` must match an `id` in `archetypes.json`.  
> • `stats` values are integers 0–100.

---

## Adding New Quiz Questions

Edit `src/data/questions.json` — append to the array:

```json
{
  "id": 40,
  "text": "在一个陌生的聚会上，你更倾向于主动找人搭话还是等别人来找你？",
  "dimension": "EI",
  "archetypeWeights": {
    "glowing-protagonist": 2,
    "ice-observer": -2,
    "oath-captain": 1,
    "agile-spinner": 1,
    "gentle-healer": 0,
    "shadow-strategist": -1,
    "chaotic-spark": 2,
    "moonlit-guardian": -1
  },
  "tags": ["social", "introvert-extrovert"]
}
```

**Guidelines:**
- `id` must be unique and increment sequentially.
- `dimension` is one of `"EI" | "SN" | "TF" | "JP"`.
- `archetypeWeights` keys must match all 8 archetype `id` values; weights range **-3 to +3**.
- Positive weight = answer "strongly agree" nudges toward that archetype.
- Keep question text in Chinese (Simplified) to match existing copy.

---

## Modifying Archetypes (`src/data/archetypes.json`)

```json
{
  "id": "glowing-protagonist",
  "name": "发光主角位",
  "mbtiTypes": ["ENFJ", "ENFP"],
  "description": "天生的领袖与感召者，能点燃周围人的热情。",
  "strengths": ["感召力强", "共情深刻", "行动力高"],
  "weaknesses": ["容易过度承担", "情绪波动大"],
  "color": "#FF6B6B"
}
```

> Each MBTI type (16 total) should appear in **exactly one** archetype's `mbtiTypes` array. The engine uses a first-match lookup — gaps cause a fallback to `archetypes[0]`.

---

## `useQuiz` Composable (state management)

```typescript
// src/composables/useQuiz.ts — typical usage from a page component
import { useQuiz } from '@/composables/useQuiz';

const {
  currentQuestion,   // Ref<Question>
  currentIndex,      // Ref<number>
  totalQuestions,    // number (39)
  progress,          // ComputedRef<number> 0–100
  answer,            // (value: number) => void  — records -3..+3 and advances
  goBack,            // () => void
  result,            // Ref<QuizResult | null>
  isComplete,        // ComputedRef<boolean>
  resetQuiz,         // () => void
} = useQuiz();
```

---

## Share / Export Poster (`useShare`)

```typescript
import { useShare } from '@/composables/useShare';

const { exportPNG, shareNative } = useShare();

// exportPNG wraps html2canvas on the #share-poster element
await exportPNG('#share-poster', 'my-acgti-result.png');

// shareNative uses Web Share API with fallback to clipboard copy
await shareNative({
  title: 'My ACGTI Result',
  text: `I got ${result.value?.characterId}!`,
  url: 'https://acgti.tianxingleo.top',
});
```

---

## Routing (`src/router/index.ts`)

```typescript
// Five named routes
const routes = [
  { path: '/',          name: 'home',       component: HomePage },
  { path: '/intro',     name: 'intro',      component: IntroPage },
  { path: '/quiz',      name: 'quiz',       component: QuizPage },
  { path: '/result',    name: 'result',     component: ResultPage },
  { path: '/characters',name: 'characters', component: CharactersPage },
  { path: '/about',     name: 'about',      component: AboutPage },
];
```

Navigate programmatically after quiz completion:

```typescript
import { useRouter } from 'vue-router';
const router = useRouter();
router.push({ name: 'result' });
```

---

## localStorage Utilities (`src/utils/storage.ts`)

```typescript
import { saveResult, loadResult, clearResult } from '@/utils/storage';
import type { QuizResult } from '@/types/quiz';

// Persist result across page refreshes
saveResult(result);

// Restore on ResultPage mount
const saved: QuizResult | null = loadResult();

// Reset for retake
clearResult();
```

---

## Deployment

### Cloudflare Pages (recommended)

1. Connect GitHub repo → Cloudflare Pages dashboard.
2. Build command: `npm run build`
3. Build output directory: `dist`
4. No environment variables required (pure frontend).

### GitHub Actions CI

The repo includes a workflow that runs on every push to `main`/`dev` and on PRs:

```yaml
# .github/workflows/ci.yml (existing)
- run: npm ci
- run: npm run build
```

### Release a version

```bash
git tag v1.2.0
git push origin v1.2.0
# GitHub Actions auto-builds dist/, zips it, creates a Release
```

---

## Common Patterns & Tips

### Filtering characters by archetype in a component

```typescript
import characters from '@/data/characters.json';
import type { Character } from '@/types/quiz';

const archetypeId = 'glowing-protagonist';
const subset: Character[] = characters.filter(
  (c) => c.archetypeId === archetypeId
);
```

### Accessing visuals by character ID

```typescript
import visuals from '@/data/characterVisuals.json';
import { enrichCharacterVisuals } from '@/utils/characterVisuals';

const enriched = enrichCharacterVisuals(characters, visuals);
// enriched[i] = { ...Character, ...CharacterVisual }
```

### Reactive dimension label (E vs I, etc.)

```typescript
function dimensionLabel(dim: Dimension, score: number): string {
  const labels: Record<Dimension, [string, string]> = {
    EI: ['E 外向', 'I 内向'],
    SN: ['N 直觉', 'S 实感'],
    TF: ['T 思考', 'F 情感'],
    JP: ['J 判断', 'P 知觉'],
  };
  // score > 50 means positive pole; score === 50 means balanced (show both)
  return score >= 50 ? labels[dim][0] : labels[dim][1];
}
```

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `npm run build` fails with type errors | New JSON data doesn't match types | Run `npx tsc --noEmit` and fix mismatches in `src/types/quiz.ts` |
| Character not appearing in results | `archetypeId` mismatch between `characters.json` and `archetypes.json` | Ensure `archetypeId` exactly matches an archetype `id` |
| New question not affecting scores | `dimension` key is wrong | Must be exactly `"EI"`, `"SN"`, `"TF"`, or `"JP"` |
| Poster export is blank | `html2canvas` can't load cross-origin images | Host character images on a CORS-enabled CDN or use base64 data URIs |
| Route returns 404 on Cloudflare Pages | SPA fallback not configured | Add `_redirects` file: `/* /index.html 200` in `public/` |
| Dev server errors on `@/` imports | Vite alias not resolving | Check `vite.config.ts` has `resolve: { alias: { '@': '/src' } }` |
