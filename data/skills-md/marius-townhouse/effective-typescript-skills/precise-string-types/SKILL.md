---
name: precise-string-types
description: Use when working with string-typed properties. Use when string values have a limited set of options. Use when keyof could provide better type safety.
---

# Prefer More Precise Alternatives to String Types

## Overview

**The string type is enormous. Use narrower types when possible.**

String literal unions, template literal types, and keyof give you better type safety, autocomplete, and documentation than plain string.

## When to Use This Skill

- Defining properties with limited valid values
- Creating function parameters that accept specific strings
- Working with object keys or property names
- Seeing "stringly typed" code
- Getting no autocomplete on string parameters

## The Iron Rule

```
NEVER use plain string when the valid values are limited.
```

**No exceptions:**
- Not for "there might be more values later"
- Not for "it's simpler"
- Not for "the enum is overkill"

## Detection: The "Stringly Typed" Smell

If a string can only be certain values, make that explicit.

```typescript
// ❌ VIOLATION: Too broad - accepts any string
interface Album {
  artist: string;
  title: string;
  releaseDate: string;     // What format? Any string works!
  recordingType: string;   // "live" or "studio"... but also "banana"
}

// These are all valid but wrong:
const album: Album = {
  artist: 'Miles Davis',
  title: 'Kind of Blue',
  releaseDate: 'August 17th, 1959',  // Wrong format
  recordingType: 'Studio',            // Wrong case
};
```

## Solution: String Literal Unions

```typescript
// ✅ CORRECT: Precise types
type RecordingType = 'studio' | 'live';

interface Album {
  artist: string;
  title: string;
  releaseDate: Date;         // Use Date, not string
  recordingType: RecordingType;
}

const album: Album = {
  artist: 'Miles Davis',
  title: 'Kind of Blue',
  releaseDate: new Date('1959-08-17'),
  recordingType: 'Studio',
  //             ~~~~~~~~ Type '"Studio"' is not assignable to type 'RecordingType'
};
```

## Benefits of Precise Types

### 1. Catches Typos

```typescript
type Direction = 'north' | 'south' | 'east' | 'west';

function move(direction: Direction) { /* ... */ }

move('nroth');  // Error: Did you mean 'north'?
```

### 2. Provides Autocomplete

```typescript
// With string: no suggestions
function move(direction: string) { }
move('|')  // Nothing

// With union: suggestions appear
function move(direction: Direction) { }
move('|')  // Suggests: north, south, east, west
```

### 3. Documents Valid Values

```typescript
/** What environment was this recording made in? */
type RecordingType = 'live' | 'studio';

// The type IS the documentation
function getAlbums(type: RecordingType) { }
// IDE shows: (parameter) type: "live" | "studio"
```

## Using keyof for Object Keys

```typescript
// ❌ BAD: Any string is accepted
function pluck(records: any[], key: string): any[] {
  return records.map(r => r[key]);
}

// ✅ GOOD: Only valid keys accepted
function pluck<T>(records: T[], key: keyof T): T[keyof T][] {
  return records.map(r => r[key]);
}

const albums: Album[] = [/* ... */];

pluck(albums, 'artist');     // OK, returns string[]
pluck(albums, 'artits');     // Error: Did you mean 'artist'?
```

## Even Better: Generic Key Parameter

```typescript
function pluck<T, K extends keyof T>(records: T[], key: K): T[K][] {
  return records.map(r => r[key]);
}

const dates = pluck(albums, 'releaseDate');
//    ^? const dates: Date[]  // Precise return type!

const artists = pluck(albums, 'artist');
//    ^? const artists: string[]
```

## Template Literal Types for Patterns

```typescript
// Match strings like "GET /users" or "POST /items"
type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE';
type ApiRoute = `${HttpMethod} /${string}`;

function handleRoute(route: ApiRoute) { }

handleRoute('GET /users');     // OK
handleRoute('POST /items');    // OK
handleRoute('PATCH /users');   // Error: not a valid HttpMethod
handleRoute('GET users');      // Error: missing /
```

## When String IS Appropriate

```typescript
interface Album {
  // These genuinely can be any string:
  artist: string;   // "Miles Davis", "Queen", etc.
  title: string;    // Unlimited possibilities
  
  // These should NOT be string:
  recordingType: RecordingType;  // Limited options
  genre: Genre;                   // Limited options
}
```

## Pressure Resistance Protocol

### 1. "We Might Add More Values"

**Pressure:** "What if we add more recording types later?"

**Response:** Add them to the union. TypeScript will flag all the places you need to handle them.

**Action:** Start with the known values. Expand when needed.

### 2. "Users Might Enter Anything"

**Pressure:** "User input could be any string"

**Response:** Validate at the boundary. Use precise types internally.

**Action:** Parse/validate user input, then use precise types in your code.

### 3. "Enums Are Too Much"

**Pressure:** "I don't want to create an enum for this"

**Response:** String literal unions are lighter than enums and just as precise.

**Action:** Use `type X = 'a' | 'b' | 'c'` instead of enum.

## Red Flags - STOP and Reconsider

- Comments explaining valid string values
- Runtime validation for string parameters
- Switch statements on strings with default "should never happen"
- String parameters with no autocomplete
- Bugs from typos in string values

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "It's just a string" | It's a string from a limited set. Express that. |
| "We'll validate later" | Validate at boundaries, use types internally. |
| "Too many values" | If finite, enumerate them. TypeScript handles it. |
| "Enums are ugly" | Use string literal unions instead. |

## Quick Reference

| You Have | Use Instead |
|----------|-------------|
| `string` with N valid values | `'value1' \| 'value2' \| ...` |
| Object key parameter | `keyof T` |
| String with pattern | Template literal type |
| Date as string | `Date` |
| URL as string | Consider branded type |

## Migration Pattern

```typescript
// Step 1: Find strings with limited values
interface Config {
  environment: string;  // "dev", "staging", "prod"
}

// Step 2: Create the union type
type Environment = 'development' | 'staging' | 'production';

// Step 3: Use it
interface Config {
  environment: Environment;
}

// Step 4: Fix all the errors (that's the point!)
const config: Config = { environment: 'dev' };
//                                    ~~~~~ Did you mean 'development'?
```

## The Bottom Line

**string is the any of string types.**

When values are limited, express that limitation. Use string literal unions for finite sets, keyof for object keys, and template literal types for patterns. Your code will be safer and your IDE more helpful.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 35: Prefer More Precise Alternatives to String Types.
