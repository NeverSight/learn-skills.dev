---
name: skr-address-resolution
description: Add .skr domain name resolution and display to Solana Mobile React Native apps. Use when the user requests to integrate .skr domain validation, resolve .skr domains to wallet addresses, display .skr names instead of addresses, add reverse lookup from addresses to domains, or implement .skr name features anywhere wallet addresses are shown (profiles, friend lists, transaction history, etc.)
---

# Solana Domains (.skr Resolution)

Enable .skr domain name resolution in React Native apps to display human-readable names instead of wallet addresses.

## What This Skill Does

Implements complete .skr domain resolution for Solana Mobile apps:
- **Forward lookup**: Resolve `.skr` domains (e.g., `alice.skr`) to wallet addresses
- **Reverse lookup**: Resolve wallet addresses to `.skr` domain names
- **Display**: Show `.skr` names instead of truncated addresses throughout the app
- **Backend + Frontend**: Integrates API endpoints into existing backend (or creates minimal Express server if none exists) plus React Native client code

## When to Use

Use this skill when the user asks to:
- "Add .skr domain resolution to my app"
- "Display .skr names instead of wallet addresses"
- "Validate .skr domains"
- "Show user's .skr name in their profile"
- "Add .skr support to my React Native Solana app"
- Integrate .skr domains anywhere wallet addresses are displayed

## Integration Approach

Ask the user which integration they want:
1. **Both**: Backend API + frontend integration (default, recommended)
2. **Backend only**: Just the API endpoints
3. **Frontend only**: Just the React Native client code (assumes backend exists)

Most users will want option 1 (both), as .skr resolution requires an API to keep RPC calls secure.

## Implementation Workflow

### Step 1: Assess Existing Backend

**IMPORTANT**: Before creating any backend, thoroughly check what the user already has:

1. **Search for existing backend frameworks:**
   - Look for `express`, `fastify`, `nestjs`, `hono`, `koa`, or other Node.js servers
   - Check `package.json` files for backend dependencies
   - Look for server entry points (`server.ts`, `index.ts`, `app.ts`, `main.ts`)
   - Check for API route folders (`routes/`, `api/`, `controllers/`)

2. **Check for existing API structure:**
   - Existing route definitions
   - Middleware setup
   - How other endpoints are organized

3. **Ask the user if unclear:**
   - "I see you have an Express server in `/backend`. Should I add the .skr endpoints there?"
   - "What backend framework are you using?"
   - "Do you have an existing API I should integrate with?"

### Step 2: Backend Implementation

**Priority order:**

1. **If existing backend found**: Add the .skr resolution endpoints to the user's existing backend
   - Match their existing code style and patterns
   - Add routes to their existing router/app
   - Use their existing middleware and error handling patterns
   - Only install the new dependencies needed (`@onsol/tldparser`, `@solana/web3.js`)

2. **If no backend exists**: Create a minimal Express API server with .skr domain resolution

**Core logic to implement** (framework-agnostic):

**Required Packages (add to existing backend or new server):**
```bash
npm install @onsol/tldparser @solana/web3.js
# Only if creating new Express server:
npm install express cors
npm install -D @types/express @types/cors typescript ts-node
```

**Key Implementation Points:**
1. Initialize Solana connection to mainnet (`https://api.mainnet-beta.solana.com`)
2. Create TldParser instance: `new TldParser(connection)`
3. Implement two endpoints (adapt to user's framework/routing style):
   - `POST /api/resolve-domain`: Domain → Address lookup
   - `POST /api/resolve-address`: Address → Domain reverse lookup
4. Use `parser.getOwnerFromDomainTld(domain)` for forward lookup
5. Use `parser.getParsedAllUserDomainsFromTld(publicKey, 'skr')` for reverse lookup

**Adapting to existing backends:**
- **Express**: Add routes to existing `app` or router
- **Fastify**: Register routes with `fastify.post()`
- **NestJS**: Create a new controller/service
- **Hono/Koa**: Add routes using their respective patterns
- **Next.js API routes**: Create `/api/resolve-domain.ts` and `/api/resolve-address.ts`

**See:** [references/backend-implementation.md](references/backend-implementation.md) for complete Express code (adapt patterns for other frameworks)

### Step 3: Frontend Integration

Create React Native hook and components to call the backend API.

**Required Setup:**
- API base URL: `http://10.0.2.2:3000` for Android emulator (maps to localhost)
- For physical devices: Use computer's IP address (e.g., `http://192.168.1.5:3000`)

**Key Implementation Points:**
1. Create `use-domain-lookup.ts` hook with `resolveDomain()` and `resolveAddress()` methods
2. Use hook in components to fetch .skr domains on mount
3. Fallback to truncated addresses (e.g., `5FHw...k3wZ`) when no domain found
4. Cache results to avoid repeated API calls

**Common Use Cases:**
- **Profile display**: Show user's .skr domain in welcome message
- **Friend lists**: Replace addresses with .skr names
- **Transaction history**: Display sender/receiver as .skr domains
- **Search**: Allow searching by .skr domain or address

**See:** [references/frontend-implementation.md](references/frontend-implementation.md) for complete code

### Step 4: Testing & Validation

After implementing:
1. Test backend endpoints with curl or Postman
2. Test frontend with a known .skr domain (Seeker users have these by default)
3. Verify fallback behavior when domain doesn't exist
4. Check error handling for invalid inputs

## Key Technical Details

### Domain Resolution Library

Uses `@onsol/tldparser` from AllDomains protocol:
- **Forward**: `parser.getOwnerFromDomainTld(domain)` - Returns PublicKey or null
- **Reverse**: `parser.getParsedAllUserDomainsFromTld(publicKey, 'skr')` - Returns array of domains

**Important**: When calling `getOwnerFromDomainTld()`, pass domain name WITHOUT `.skr` extension.

### Domain Validation

A valid .skr domain:
- Ends with `.skr` extension
- Returns successfully from the AllDomains API
- Is registered on Solana mainnet

Invalid inputs return 404 from the API.

### Error Handling

**Backend responses:**
- `200`: Success with data
- `400`: Invalid input (missing/malformed domain or address)
- `404`: Domain not found or address has no .skr domain
- `500`: Server error (RPC issues, network problems)

**Frontend behavior:**
- On error: Fall back to truncated address display
- Show loading states during API calls
- Handle network failures gracefully

## Resources

### Backend Implementation
Reference Express API code with TypeScript. **Adapt this to the user's existing backend framework:**
- Core domain resolution logic (framework-agnostic)
- Example Express routes (adapt for Fastify, NestJS, Hono, Next.js API routes, etc.)
- Error handling and validation patterns
- Package.json with required dependencies

**File:** [references/backend-implementation.md](references/backend-implementation.md)

### Frontend Implementation
React Native integration code including:
- Custom `useDomainLookup()` hook
- Example components for different use cases
- Mobile Wallet Adapter integration
- Utility functions for address truncation

**File:** [references/frontend-implementation.md](references/frontend-implementation.md)

## External Documentation

- **AllDomains Developer Guide**: https://docs.alldomains.id/protocol/developer-guide/ad-sdks/svm-sdks/solana-mainnet-sdk
- **@onsol/tldparser NPM**: https://www.npmjs.com/package/@onsol/tldparser
- **Solana Mobile Docs**: https://docs.solanamobile.com/react-native/overview
