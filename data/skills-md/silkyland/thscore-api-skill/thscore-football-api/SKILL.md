---
name: thscore-football-api
description: "Comprehensive development guide for integrating the THScore Football API. Covers authentication, regional server selection, all football endpoints (Live Data, Stats, Odds, Live Animation, Historical DB), TypeScript types, rate limiting, caching, error handling, and iFrame/WebView embedding. Triggers on any task involving football livescores, schedules, standings, odds, events, lineups, team/player profiles, or live animation embeds."
license: MIT
---

# THScore Football API – Developer Skill

Comprehensive best practices and reference guide for consuming the [THScore Football API](https://www.thscore.info/doc/docs.shtml). This skill provides TypeScript type definitions, endpoint stubs, rules, and complete code examples designed to make AI agent-assisted integrations reliable and production-ready.

---

## When to Apply

Reference this skill when:

- Setting up a THScore API client or HTTP wrapper
- Fetching **live scores**, match timelines, or in-play statistics
- Retrieving **league/cup reference data** (countries, league IDs, rules)
- Displaying **live football animation** (iFrame/WebView embed)
- Building **standings tables**, top-scorer boards, or FIFA ranking pages
- Integrating **Asian Handicap, European, or 1×2 odds** feeds
- Building scheduled jobs to sync **historical match data**
- Designing caching layers or database schemas for sports data
- Debugging API key errors, rate limit violations, or malformed responses

---

## Available Product Plans & Endpoint Sets

| Plan | # APIs | Key Features |
|------|--------|--------------|
| **Live Data** ($599/mo) | 22 | Livescores, Schedule, Events, Lineups, Live Text, Profile |
| **Stats** ($399/mo) | 13 | Match Analysis, Player Stats, Standings, Top Scorers, FIFA Ranking |
| **Odds** | — | 18 Bookmakers, Asian Handicap, European, 1×2 |
| **Odds Pro** | — | 200+ European Bookmakers |
| **Betfair** | — | Betfair exchange data |
| **Live Animation** ($1699/mo) | 1 | iFrame/WebView animation, 42 events |
| **Historical Database** | — | Past seasons, historical match data |
| **Common API** | ∞ | Shared by all paid plans: League & Cup Profiles, Countries, Bookmakers |

---

## Base URL & Authentication

```
http://www.thscore.info/<API_PATH>?api_key=<YOUR_API_KEY>
```

For **Asia-based servers** (lower latency):
```
http://api2.thscore.info/<API_PATH>?api_key=<YOUR_API_KEY>
```

> Always store `api_key` in environment variables, never hardcode it.

---

## TypeScript Types (`types.ts`)

```typescript
// ==========================================================
// types.ts
// THScore Football API – Complete TypeScript Type Definitions
// ==========================================================

// ── Common / Shared ────────────────────────────────────────

/** Unix timestamp (seconds) */
type UnixTimestamp = number;

/** ISO 3166-1 alpha-2 country code */
type CountryCode = string;

/** Match state integer returned by Livescores */
export enum MatchState {
  NotStarted    = 0,
  FirstHalf     = 1,
  HalfTime      = 2,
  SecondHalf    = 3,
  ExtraTimeFirst = 4,
  ExtraTimeHT   = 5,
  ExtraTimeSecond = 6,
  PenaltyShootout = 7,
  Finished      = -1,
  Postponed     = -11,
  Cancelled     = -12,
  TBD           = -13,
  Abandoned     = -14,
  Suspended     = -15,
  Delayed       = -16,
  Interrupted   = -17,
  ExtraTime     = -18,
  Walkover      = -19,
}

/** Match state labels (use to display to end users) */
export const MatchStateLabel: Record<MatchState, string> = {
  [MatchState.NotStarted]:       "Not Started",
  [MatchState.FirstHalf]:        "1st Half",
  [MatchState.HalfTime]:         "Half Time",
  [MatchState.SecondHalf]:       "2nd Half",
  [MatchState.ExtraTimeFirst]:   "Extra Time 1st",
  [MatchState.ExtraTimeHT]:      "Extra Time HT",
  [MatchState.ExtraTimeSecond]:  "Extra Time 2nd",
  [MatchState.PenaltyShootout]:  "Penalties",
  [MatchState.Finished]:         "Finished",
  [MatchState.Postponed]:        "Postponed",
  [MatchState.Cancelled]:        "Cancelled",
  [MatchState.TBD]:              "TBD",
  [MatchState.Abandoned]:        "Abandoned",
  [MatchState.Suspended]:        "Suspended",
  [MatchState.Delayed]:          "Delayed",
  [MatchState.Interrupted]:      "Interrupted",
  [MatchState.ExtraTime]:        "Extra Time",
  [MatchState.Walkover]:         "Walkover",
};

// ── Common API ─────────────────────────────────────────────
// GET /football_th/league/basic.aspx (1 hr limit / 1 day recommended)

export interface LeagueBasic {
  leagueId:      number;
  leagueName:    string;
  leagueNameEn:  string;
  countryId:     number;
  countryName:   string;
  countryNameEn: string;
  leagueLogo:    string;  // URL
  countryLogo:   string;  // URL
  type:          number;  // 1 = League, 2 = Cup, 3 = International
  curSeasonId:   number;
}

export interface LeagueBasicResponse {
  code:    number;
  message: string;
  results: LeagueBasic[];
}

// GET /football_th/league.aspx (30 min limit / 1 day recommended)

export interface LeagueFull extends LeagueBasic {
  seasonId:     number;
  seasonName:   string;
  startDate:    string;   // "YYYY-MM-DD"
  endDate:      string;   // "YYYY-MM-DD"
  primaryColor: string;   // Hex
  secondaryColor: string; // Hex
  officialSite: string;   // URL
  totalTeams:   number;
}

// GET /football_th/league.aspx?cmd=rule
// Returns league rules (round-robin format, stages, etc.)

export interface LeagueRule {
  leagueId:   number;
  seasonId:   number;
  info:       string; // HTML or plain text rules
}

// ── Live Data Plan ─────────────────────────────────────────

// GET /football_th/livescores.aspx (10 sec limit / 1 min recommended)

export interface LiveMatch {
  matchId:      number;
  leagueId:     number;
  leagueName:   string;
  homeTeamId:   number;
  homeTeamName: string;
  awayTeamId:   number;
  awayTeamName: string;
  homeScore:    number;
  awayScore:    number;
  homeHalfScore: number;
  awayHalfScore: number;
  state:        MatchState;
  matchTime:    UnixTimestamp;  // UTC kickoff time
  elapsed:      number;         // minutes elapsed (0 if not started)
  homeRed:      number;
  awayRed:      number;
  homeYellow:   number;
  awayYellow:   number;
  homeCorner:   number;
  awayCorner:   number;
  round:        string;
  hasAnimation: boolean;        // true if live animation is available
  animationMatchId?: number;    // use in animation iFrame URL
}

export interface LivescoresResponse {
  code:    number;
  message: string;
  results: LiveMatch[];
}

// GET /football_th/schedule/results.aspx (60 sec limit / 6 hr recommended)

export interface ScheduledMatch {
  matchId:      number;
  leagueId:     number;
  leagueName:   string;
  homeTeamId:   number;
  homeTeamName: string;
  awayTeamId:   number;
  awayTeamName: string;
  homeScore:    number | null; // null = future match
  awayScore:    number | null;
  state:        MatchState;
  matchTime:    UnixTimestamp;
  round:        string;
}

// GET /football_th/matchevent.aspx (60 sec limit)
// Events include: goals, bookings, substitutions

export enum EventType {
  Goal        = 1,
  OwnGoal     = 2,
  YellowCard  = 3,
  RedCard     = 4,
  YellowRed   = 5,
  Substitution = 6,
  Penalty     = 7,
  MissedPenalty = 8,
}

export interface MatchEvent {
  matchId:   number;
  type:      EventType;
  minute:    number;
  addedTime: number;          // stoppage time minutes
  teamId:    number;
  playerId:  number;
  playerName: string;
  relatedPlayerId?:   number; // e.g. player who was substituted
  relatedPlayerName?: string;
}

// GET /football_th/matchlineup.aspx

export interface Player {
  playerId:   number;
  playerName: string;
  shirtNumber: number;
  position:   string;  // "GK" | "DF" | "MF" | "FW"
  isStarting: boolean;
  isCaptain:  boolean;
  countryCode: CountryCode;
}

export interface MatchLineup {
  matchId:      number;
  homeTeamId:   number;
  awayTeamId:   number;
  homeLineup:   Player[];
  awayLineup:   Player[];
  homeSubs:     Player[];
  awaySubs:     Player[];
  homeFormation: string;  // e.g. "4-3-3"
  awayFormation: string;
  homeCoach:    string;
  awayCoach:    string;
}

// ── Profile (Live Data Plan) ────────────────────────────────
// GET /football_th/league.aspx   → LeagueFull (see above)
// GET /football_th/team.aspx

export interface Team {
  teamId:      number;
  teamName:    string;
  teamNameEn:  string;
  teamLogo:    string;  // URL
  countryId:   number;
  countryName: string;
  stadium:     string;
  capacity:    number;
  founded:     number;  // Year
  website:     string;
}

// GET /football_th/player.aspx

export interface PlayerProfile {
  playerId:    number;
  playerName:  string;
  playerNameEn: string;
  photo:       string;  // URL
  nationality: CountryCode;
  position:    string;
  dateOfBirth: string;  // "YYYY-MM-DD"
  height:      number;  // cm
  weight:      number;  // kg
  currentTeamId: number;
}

// ── Stats Plan ─────────────────────────────────────────────
// GET /football_th/league/table.aspx (doc: /doc/docs_id=43)

export interface StandingRow {
  rank:          number;
  teamId:        number;
  teamName:      string;
  played:        number;
  won:           number;
  drawn:         number;
  lost:          number;
  goalsFor:      number;
  goalsAgainst:  number;
  goalDifference: number;
  points:        number;
  form:          string[];  // last 5 results: "W" | "D" | "L"
  winRate:       number;    // percentage 0–100
  drawRate:      number;
  loseRate:      number;
}

export interface StandingsResponse {
  code:      number;
  leagueId:  number;
  seasonId:  number;
  results:   StandingRow[];
}

// GET /football_th/topscorer.aspx (doc: /doc/docs_id=39)

export interface TopScorer {
  rank:       number;
  playerId:   number;
  playerName: string;
  teamId:     number;
  teamName:   string;
  goals:      number;
  fieldGoals: number;
  penalties:  number;
  assists:    number;
  appearances: number;
}

// GET /football_th/fifaranking.aspx (doc: /doc/docs_id=47)

export interface FifaRankingEntry {
  rank:          number;
  previousRank:  number;
  teamId:        number;
  teamName:      string;
  countryCode:   CountryCode;
  points:        number;
  previousPoints: number;
  rankChange:    number;  // positive = up, negative = down
}

// ── Odds ───────────────────────────────────────────────────

export interface AsianHandicapOdds {
  matchId:     number;
  bookmaker:   string;
  home:        number;  // odds for home side
  handicap:    number;  // e.g. -0.5
  away:        number;
  updatedAt:   UnixTimestamp;
}

export interface EuropeanOdds {
  matchId:   number;
  bookmaker: string;
  home:      number;
  draw:      number;
  away:      number;
  updatedAt: UnixTimestamp;
}

// ── Live Animation ─────────────────────────────────────────
// (no API response type—it is an iFrame/WebView URL)

export interface AnimationEmbedParams {
  matchId:   number;
  accessKey: string;
}

export function buildAnimationUrl(params: AnimationEmbedParams): string {
  return `https://www.isportslive8.com/football/detail.html?matchId=${params.matchId}&accessKey=${params.accessKey}`;
}
```

---

## Rule Categories by Priority

| Priority | Category | Prefix | Impact |
|----------|----------|--------|--------|
| 1 | Authentication & Routing | `auth-` | CRITICAL |
| 2 | Rate Limiting & Caching | `limit-` | CRITICAL |
| 3 | Live Animation – When & How | `anim-` | HIGH |
| 4 | Endpoint-Specific Best Practices | `ep-` | HIGH |
| 5 | Error Handling & Resilience | `error-` | HIGH |
| 6 | Data Normalisation & Types | `data-` | MEDIUM |
| 7 | Security | `security-` | CRITICAL |

---

## Rules

### 1. Authentication & Routing (CRITICAL)

#### `auth-env-key` – Store API key in environment variable

❌ **Wrong:**
```typescript
const url = `http://www.thscore.info/football_th/livescores.aspx?api_key=abc123`;
```

✅ **Correct:**
```typescript
const API_KEY = process.env.THSCORE_API_KEY;
if (!API_KEY) throw new Error("THSCORE_API_KEY is not set");
const url = `http://www.thscore.info/football_th/livescores.aspx?api_key=${API_KEY}`;
```

#### `auth-asia-server` – Use `api2.thscore.info` for Asia-located servers

```typescript
// config.ts
export const THSCORE_HOST =
  process.env.THSCORE_REGION === "asia"
    ? "api2.thscore.info"
    : "www.thscore.info";

export function buildUrl(path: string, params: Record<string, string> = {}): string {
  const base = `http://${THSCORE_HOST}${path}`;
  const query = new URLSearchParams({
    api_key: process.env.THSCORE_API_KEY!,
    ...params,
  });
  return `${base}?${query.toString()}`;
}
```

---

### 2. Rate Limiting & Caching (CRITICAL)

| Endpoint | Hard Limit | Recommended |
|----------|-----------|-------------|
| `Livescores for Today` | 10 sec/call | 1 min/call |
| `Schedule & Results` | 60 sec/call | 6 hr/call |
| `League & Cup Profile (Basic)` | 1 hr/call | 1 day/call |
| `League & Cup Profile (Full)` | 30 min/call | 1 day/call |
| `Standings` | — | 1 hr/call |
| `Top Scorers` | — | 1 day/call |
| `FIFA Ranking` | — | 1 week/call |

#### `limit-tiered-cache` – Use appropriate TTL per endpoint type

```typescript
// cache.service.ts (using Redis)
import { Redis } from "ioredis";
const redis = new Redis(process.env.REDIS_URL!);

async function cachedFetch<T>(key: string, ttlSeconds: number, fetcher: () => Promise<T>): Promise<T> {
  const cached = await redis.get(key);
  if (cached) return JSON.parse(cached) as T;

  const data = await fetcher();
  await redis.setex(key, ttlSeconds, JSON.stringify(data));
  return data;
}

// Usage examples:
// Livescores — cache 60 seconds
const livescores = await cachedFetch("thscore:livescores", 60, fetchLivescores);

// League list — cache 24 hours
const leagues = await cachedFetch("thscore:leagues", 86400, fetchLeagues);

// Standings — cache 1 hour
const standings = await cachedFetch(`thscore:standings:${leagueId}`, 3600, () => fetchStandings(leagueId));
```

#### `limit-background-sync` – Never poll the API inside an HTTP request handler

```typescript
// BAD: polling inside a route handler
app.get("/api/livescores", async (req, res) => {
  const data = await fetch(buildUrl("/football_th/livescores.aspx")); // ← blocks users
  res.json(await data.json());
});

// GOOD: route handler reads from cache; a cron job populates it
app.get("/api/livescores", async (req, res) => {
  const cached = await redis.get("thscore:livescores");
  res.json(cached ? JSON.parse(cached) : { code: 503, message: "Data not ready yet" });
});

// cron job (every 60 seconds)
cron.schedule("* * * * *", async () => {
  const data = await fetchLivescores();
  await redis.setex("thscore:livescores", 90, JSON.stringify(data));
});
```

---

### 3. Live Animation – When & How (HIGH)

#### `anim-when` – When Live Animation data is available

Live Animation is only available during a **live match** in one of these active states:

```typescript
import { MatchState } from "./types";

const ANIMATION_STATES: MatchState[] = [
  MatchState.FirstHalf,
  MatchState.HalfTime,
  MatchState.SecondHalf,
  MatchState.ExtraTimeFirst,
  MatchState.ExtraTimeHT,
  MatchState.ExtraTimeSecond,
  MatchState.PenaltyShootout,
];

export function isAnimationAvailable(match: LiveMatch): boolean {
  return ANIMATION_STATES.includes(match.state) && match.hasAnimation === true;
}
```

> Check `hasAnimation: true` on the Livescores response. Do not embed the iFrame for scheduled/finished matches – the animation URL will return a blank page.

#### `anim-embed-html` – Embed the animation in a page (PC/H5 via iFrame)

```html
<!-- Match detail page -->
<div id="animation-container" style="display:none">
  <iframe
    id="match-animation"
    src=""
    width="100%"
    height="480"
    frameborder="0"
    allowfullscreen
    loading="lazy"
  ></iframe>
</div>
```

```typescript
// match-detail.ts
import { buildAnimationUrl, isAnimationAvailable, LiveMatch } from "./types";

function renderAnimation(match: LiveMatch): void {
  const container = document.getElementById("animation-container")!;
  const iframe = document.getElementById("match-animation") as HTMLIFrameElement;

  if (!isAnimationAvailable(match)) {
    container.style.display = "none";
    return;
  }

  const url = buildAnimationUrl({
    matchId:   match.animationMatchId ?? match.matchId,
    accessKey: process.env.THSCORE_ANIMATION_ACCESS_KEY!,
  });

  iframe.src = url;
  container.style.display = "block";
}
```

#### `anim-webview-mobile` – Load the animation in WebView (React Native)

```tsx
// AnimationPlayer.tsx
import React from "react";
import { WebView } from "react-native-webview";
import { buildAnimationUrl } from "../types";

interface Props {
  matchId: number;
  accessKey: string;
}

export const AnimationPlayer: React.FC<Props> = ({ matchId, accessKey }) => {
  const url = buildAnimationUrl({ matchId, accessKey });
  return (
    <WebView
      source={{ uri: url }}
      style={{ flex: 1 }}
      allowsFullscreenVideo
      mediaPlaybackRequiresUserAction={false}
    />
  );
};
```

#### `anim-domain-whitelist` – Register your domain in the control panel
- Go to **Console Panel → Animation → Domain Whitelist** before embedding via iFrame.
- On APP platforms using WebView, no whitelist is needed—direct URL access works.

---

### 4. Endpoint-Specific Best Practices (HIGH)

#### `ep-league-basic` – League & Cup Profile (Basic)

**Endpoint:** `GET /football_th/league/basic.aspx`
**Rate:** Hard limit 1 hr/call · Recommended 1 day/call
**Plan:** All paid football plans (Stats, Live Data, Odds, Odds Pro, Betfair)

What this endpoint returns:
- `leagueId` – Use to join with livescores, schedule, standings, and odds data.
- `leagueName` / `leagueNameEn` – Thai and English display names.
- `countryId` / `countryName` – Group leagues by country.
- `leagueLogo` / `countryLogo` – CDN image URLs.
- `type` – `1` = League, `2` = Cup, `3` = International.
- `curSeasonId` – Current active season; use when calling stats or standings endpoints.
- Covers **1,600+ leagues and cups across 140+ countries**.

✅ **Best practice:**

```typescript
// league-service.ts
import { LeagueBasic, LeagueBasicResponse } from "./types";
import { buildUrl, cachedFetch } from "./utils";

/** Fetch and cache the full league catalogue for 24 hours. */
export async function getLeagues(): Promise<LeagueBasic[]> {
  return cachedFetch<LeagueBasic[]>("thscore:leagues:basic", 86400, async () => {
    const res = await fetch(buildUrl("/football_th/league/basic.aspx"));
    const json: LeagueBasicResponse = await res.json();
    if (json.code !== 0) throw new Error(`API error: ${json.message}`);
    return json.results;
  });
}

/** Group leagues by country for a country-selector UI */
export function groupByCountry(leagues: LeagueBasic[]): Record<string, LeagueBasic[]> {
  return leagues.reduce((acc, league) => {
    const key = league.countryNameEn;
    if (!acc[key]) acc[key] = [];
    acc[key].push(league);
    return acc;
  }, {} as Record<string, LeagueBasic[]>);
}

/** Filter for Cups only */
export function getCups(leagues: LeagueBasic[]): LeagueBasic[] {
  return leagues.filter(l => l.type === 2);
}

/** Find league by name (case-insensitive) */
export function findLeague(leagues: LeagueBasic[], name: string): LeagueBasic | undefined {
  const q = name.toLowerCase();
  return leagues.find(l => l.leagueNameEn.toLowerCase().includes(q));
}
```

#### `ep-league-full` – League & Cup Profile (Full)

**Endpoint:** `GET /football_th/league.aspx`
**Rate:** Hard limit 30 min/call · Recommended 1 day/call
**Plan:** Live Data only

Additional fields beyond Basic:
- `seasonId`, `seasonName` – Active season details (e.g., "2024-2025")
- `startDate`, `endDate` – Season date range
- `primaryColor`, `secondaryColor` – Brand colours for UI theming
- `totalTeams` – Number of participating teams
- `officialSite` – Official league website

**Also supports:** `GET /football_th/league.aspx?cmd=rule`  
Returns league rules as plain text/HTML – useful for a league info page.

#### `ep-livescores` – Livescores for Today

**Endpoint:** `GET /football_th/livescores.aspx`
**Rate:** Hard limit 10 sec/call · Recommended 1 min/call
**Plan:** Live Data

Key response fields to use:
- `state` → map to `MatchState` enum
- `elapsed` → show live match clock
- `homeScore`, `awayScore`, `homeHalfScore`, `awayHalfScore` → score cards
- `homeCorner`, `awayCorner` → corner count
- `homeRed`, `awayRed` → red card indicators
- `hasAnimation` → gate for showing animation embed button

```typescript
// livescores.service.ts
import { LivescoresResponse, LiveMatch, MatchState, MatchStateLabel } from "./types";
import { buildUrl, cachedFetch } from "./utils";

export async function getLivescores(): Promise<LiveMatch[]> {
  return cachedFetch<LiveMatch[]>("thscore:livescores", 60, async () => {
    const res = await fetch(buildUrl("/football_th/livescores.aspx"));
    const json: LivescoresResponse = await res.json();
    if (json.code !== 0) throw new Error(`[Livescores] API error ${json.code}: ${json.message}`);
    return json.results;
  });
}

/** Returns only currently in-play matches */
export function getInPlayMatches(matches: LiveMatch[]): LiveMatch[] {
  const inPlayStates = [
    MatchState.FirstHalf, MatchState.HalfTime,
    MatchState.SecondHalf, MatchState.ExtraTimeFirst,
    MatchState.ExtraTimeHT, MatchState.ExtraTimeSecond,
    MatchState.PenaltyShootout,
  ];
  return matches.filter(m => inPlayStates.includes(m.state));
}

/** Returns a display-friendly score string e.g. "2 - 1 (1 - 0)" */
export function formatScore(match: LiveMatch): string {
  return `${match.homeScore} - ${match.awayScore} (HT: ${match.homeHalfScore} - ${match.awayHalfScore})`;
}

/** Display-friendly status with elapsed minutes */
export function formatStatus(match: LiveMatch): string {
  const label = MatchStateLabel[match.state] ?? "Unknown";
  if (match.elapsed > 0 && match.state === MatchState.FirstHalf || match.state === MatchState.SecondHalf) {
    return `${label} ${match.elapsed}'`;
  }
  return label;
}
```

#### `ep-standings` – League & Cup Standing

**Endpoint:** `GET /football_th/league/table.aspx` (see doc #43)
**Plan:** Stats

Response fields to display:
- `rank` – Position in table
- `played`, `won`, `drawn`, `lost` – Match record
- `goalsFor`, `goalsAgainst`, `goalDifference` – Goal stats
- `points` – Total points
- `form` – Array of last 5 results `["W","W","D","L","W"]`
- `winRate`, `drawRate`, `loseRate` – Percentage stats (useful for analysis tabs)

```typescript
// standings.service.ts
import { StandingRow, StandingsResponse } from "./types";
import { buildUrl, cachedFetch } from "./utils";

export async function getStandings(leagueId: number, seasonId: number): Promise<StandingRow[]> {
  const key = `thscore:standings:${leagueId}:${seasonId}`;
  return cachedFetch(key, 3600, async () => {
    const res = await fetch(buildUrl("/football_th/league/table.aspx", {
      leagueId: String(leagueId),
      seasonId: String(seasonId),
    }));
    const json: StandingsResponse = await res.json();
    if (json.code !== 0) throw new Error(`[Standings] API error: ${json.code}`);
    return json.results;
  });
}

/** Colour-code a form result for UI rendering */
export function formBadgeColor(result: string): string {
  return result === "W" ? "green" : result === "D" ? "gray" : "red";
}
```

---

### 5. Error Handling & Resilience (HIGH)

#### `error-retry-backoff` – Retry with exponential backoff for transient errors

```typescript
// utils/http.ts
export async function fetchWithRetry(url: string, maxRetries = 3): Promise<Response> {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 8000); // 8s timeout

      const res = await fetch(url, { signal: controller.signal });
      clearTimeout(timeout);

      if (res.ok) return res;
      if (res.status >= 500) throw new Error(`Server error ${res.status}`);
      throw new Error(`Client error ${res.status}: ${res.statusText}`);
    } catch (err) {
      if (attempt === maxRetries - 1) throw err;
      const delay = 1000 * Math.pow(2, attempt); // 1s, 2s, 4s
      console.warn(`[THScore] Attempt ${attempt + 1} failed. Retrying in ${delay}ms...`);
      await new Promise(r => setTimeout(r, delay));
    }
  }
  throw new Error("Unreachable");
}
```

#### `error-graceful-degrade` – Show stale data when API is unavailable

```typescript
export async function getLivescoresSafe(): Promise<LiveMatch[]> {
  try {
    return await getLivescores();
  } catch (err) {
    console.error("[THScore] Livescores unavailable, serving stale cache:", err);
    const stale = await redis.get("thscore:livescores:stale");
    return stale ? JSON.parse(stale) : [];
  }
}

// On successful fetch, always persist a "stale" backup
async function fetchAndPersist(): Promise<void> {
  const data = await getLivescores();
  await redis.set("thscore:livescores:stale", JSON.stringify(data)); // no TTL = forever
  await redis.setex("thscore:livescores", 60, JSON.stringify(data));
}
```

---

### 6. Data Normalisation & Types (MEDIUM)

#### `data-map-on-ingestion` – Transform API shape to your internal types immediately

Never pass raw THScore JSON directly to your UI or database. Always map through a typed transformer.

```typescript
// mappers.ts
import { LiveMatch, MatchState } from "./types";

/** Raw shape from API (untrusted, not typed) */
interface RawMatch {
  matchId: number;
  state: number;
  homeName: string;
  awayName: string;
  homeScore: number;
  awayScore: number;
  hHalf: number;
  aHalf: number;
  // ... more raw fields
}

export function mapRawMatch(raw: RawMatch): LiveMatch {
  return {
    matchId:       raw.matchId,
    homeTeamName:  raw.homeName,
    awayTeamName:  raw.awayName,
    homeScore:     raw.homeScore ?? 0,
    awayScore:     raw.awayScore ?? 0,
    homeHalfScore: raw.hHalf ?? 0,
    awayHalfScore: raw.aHalf ?? 0,
    state:         raw.state as MatchState,
    hasAnimation:  Boolean(raw.animId),
    animationMatchId: raw.animId ?? undefined,
    // ... map remaining fields
  } as LiveMatch;
}
```

---

### 7. Security (CRITICAL)

#### `security-proxy-all` – Always proxy through your backend

> THScore does not support CORS. Any request from a browser to `thscore.info` directly will be blocked. Your API key will remain exposed in network logs.

✅ **Architecture:**

```
Browser / App
     │
     ▼
Your Backend (Node / PHP / Python)   ← holds THSCORE_API_KEY
     │
     ▼
api2.thscore.info / www.thscore.info
```

```typescript
// routes/football.ts (Express example)
router.get("/livescores", async (req, res) => {
  const data = await getLivescoresSafe();
  res.json(data); // ← never expose raw API key to client
});
```

---

## Official Documentation Reference

| Topic | URL |
|-------|-----|
| Getting Started | https://www.thscore.info/doc/docs.shtml |
| Football API Home | https://www.thscore.info/doc/docs_id=42.shtml |
| League & Cup Profile (Basic) | `/football_th/league/basic.aspx` |
| League & Cup Profile (Full) | `/football_th/league.aspx` |
| Livescores for Today | `doc/docs_id=20` · `/football_th/livescores.aspx` |
| Schedule & Results | `doc/docs_id=21` · `/football_th/schedule/results.aspx` |
| Events & Stats (Match) | `doc/docs_id=15` |
| Lineups & Injury | `doc/docs_id=17` |
| League & Cup Standings | `doc/docs_id=43` |
| Top Scorers | `doc/docs_id=39` |
| FIFA Ranking | `doc/docs_id=47` |
| Live Animation Config | `doc/docs_id=242` |
| Animation Live URL Demo | https://www.isportslive8.com |
| All Football Leagues List | https://www.thscore.info/LeagueTh.aspx |
