---
name: avoid-anecdotal-types
description: Use when creating types from example data. Use when types don't match all cases. Use when API responses vary.
---

# Avoid Types Based on Anecdotal Data

## Overview

**Don't infer types from a single example.**

If you create a type based on one API response or one sample, you'll miss edge cases. Get authoritative type definitions or examine multiple examples to understand the full shape of your data.

## When to Use This Skill

- Creating types for external APIs
- Typing data from databases
- Working with third-party services
- Debugging "impossible" type errors

## The Iron Rule

```
Types should be based on specifications, not samples.
One example doesn't show all possibilities.
```

**Remember:**
- APIs have optional fields, variants, edge cases
- Sample data shows the common case, not all cases
- "Works with my data" ≠ "Type is correct"
- Get the spec, not just an example

## Detection: Example-Based Types

```typescript
// Created from looking at one API response
interface GeocodingResult {
  lat: number;
  lng: number;
  address: string;
  city: string;
  country: string;
}

// But the real API might return:
// - Missing city for some locations
// - Multiple results (array)
// - Error responses
// - Different formats for different countries
```

## Sources of Truth

### 1. Official Documentation/Spec

```typescript
// From API documentation:
interface GeocodingResult {
  lat: number;
  lng: number;
  formatted_address: string;
  address_components: AddressComponent[];  // Not flat city/country!
  partial_match?: boolean;                  // Optional!
}
```

### 2. TypeScript/JSON Schema Definitions

```typescript
// Many APIs provide TypeScript types
import { GeocodingResult } from '@google/maps-types';

// Or JSON Schema
import Ajv from 'ajv';
const validate = ajv.compile(geocodingSchema);
```

### 3. Generated Types from OpenAPI/GraphQL

```typescript
// Auto-generated from API specification
import { GeocodingResponse } from './generated/api-types';
```

## Real Example: GitHub API

```typescript
// From looking at one user:
interface GitHubUser {
  id: number;
  login: string;
  name: string;
  email: string;
  company: string;
  bio: string;
}

// Reality from GitHub's API docs:
interface GitHubUser {
  id: number;
  login: string;
  name: string | null;    // Can be null!
  email: string | null;   // Can be null!
  company: string | null; // Can be null!
  bio: string | null;     // Can be null!
  // ... many more fields, some conditional
}
```

One example user had all fields filled in. Many don't.

## The JSON.parse Problem

```typescript
// Dangerous: trusting parsed JSON
const response = await fetch('/api/user');
const user: User = await response.json();  // No runtime validation!

// The server might return:
// - Missing fields
// - Extra fields
// - Different types than expected
// - Error responses
```

## Runtime Validation

Use runtime validation to ensure data matches your types:

```typescript
import { z } from 'zod';

const UserSchema = z.object({
  id: z.number(),
  name: z.string().nullable(),
  email: z.string().email().nullable(),
});

type User = z.infer<typeof UserSchema>;

async function fetchUser(id: string): Promise<User> {
  const response = await fetch(`/api/user/${id}`);
  const data = await response.json();
  return UserSchema.parse(data);  // Throws if invalid
}
```

Now you'll catch mismatches at runtime, not in production bugs.

## Multiple Examples

If you can't get a spec, examine multiple examples:

```typescript
// Look at edge cases:
// - New user (minimal data)
// - Old user (all fields filled)
// - Deleted user (special state)
// - Admin user (extra fields)
// - Different locales

// Build type that handles ALL cases:
interface User {
  id: number;
  login: string;
  name: string | null;
  role?: 'user' | 'admin';
  deletedAt?: Date;
}
```

## Common Anecdotal Patterns

### "My Data Has This Field"

```typescript
// Your test data:
const user = { name: "Alice", age: 30 };

// But age is optional for some users!
interface User {
  name: string;
  age?: number;  // Should be optional
}
```

### "The API Always Returns..."

```typescript
// Your experience:
const response = { data: [...], total: 100 };

// But empty results might differ:
const emptyResponse = { data: [], total: 0 };  // OK
const notFound = { error: "Not found" };        // Oops, no data field!
```

### "This Field is Always a Number"

```typescript
// Your examples:
{ id: 123 }
{ id: 456 }

// But some systems return:
{ id: "abc-123" }  // String in some cases!
```

## Pressure Resistance Protocol

### 1. "The Example Works"

**Pressure:** "I tested it and it works fine"

**Response:** It works with your test data. What about edge cases?

**Action:** Get the spec or test with varied data.

### 2. "We Don't Have Documentation"

**Pressure:** "There's no API spec available"

**Response:** Examine multiple responses. Check error cases. Ask the API owners.

**Action:** Build defensive types with optional fields and validation.

## Red Flags - STOP and Reconsider

- Types created from copying one JSON response
- All properties required when API might not always include them
- Missing error/empty state handling
- Types that only match "happy path" data

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "It works in testing" | Testing shows one path, not all |
| "We control the API" | APIs change, have edge cases |
| "We'll fix it if it breaks" | Users hit edge cases first |

## Quick Reference

```typescript
// DON'T: Type from one example
interface User {
  id: number;
  name: string;  // What if null?
  email: string; // What if missing?
}

// DO: Type from specification
interface User {
  id: number;
  name: string | null;
  email?: string;
}

// DO: Runtime validation
const UserSchema = z.object({
  id: z.number(),
  name: z.string().nullable(),
  email: z.string().optional(),
});

// DO: Get official types
import { User } from '@api/types';
```

## The Bottom Line

**Types based on samples will miss edge cases.**

One API response or one database record doesn't show all possibilities. Use official documentation, generated types, or runtime validation. When creating types from examples, examine multiple cases including edge cases and errors.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 42: Avoid Types Based on Anecdotal Data.
