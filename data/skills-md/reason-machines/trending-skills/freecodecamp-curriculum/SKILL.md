---
name: freecodecamp-curriculum
description: Comprehensive guide for contributing to and working with freeCodeCamp's open-source codebase and curriculum platform
triggers:
  - help me contribute to freeCodeCamp
  - how do I add a curriculum challenge to freeCodeCamp
  - set up freeCodeCamp locally
  - how does freeCodeCamp's challenge system work
  - create a new freeCodeCamp certification
  - freeCodeCamp development environment setup
  - how to write freeCodeCamp challenge tests
  - freeCodeCamp codebase structure
---

# freeCodeCamp Curriculum & Platform Development

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

freeCodeCamp.org is a free, open-source learning platform with thousands of interactive coding challenges, certifications, and a full-stack curriculum. The codebase includes a React/TypeScript frontend, Node.js/Fastify backend, and a YAML/Markdown-based curriculum system.

---

## Architecture Overview

```
freeCodeCamp/
├── api/                   # Fastify API server (TypeScript)
├── client/                # Gatsby/React frontend (TypeScript)
├── curriculum/            # All challenges and certifications (YAML/Markdown)
│   └── challenges/
│       ├── english/
│       │   ├── responsive-web-design/
│       │   ├── javascript-algorithms-and-data-structures/
│       │   └── ...
│       └── ...
├── tools/
│   ├── challenge-helper-scripts/  # CLI tools for curriculum authoring
│   └── ui-components/             # Shared React components
├── config/                # Shared configuration
└── e2e/                   # Playwright end-to-end tests
```

---

## Local Development Setup

### Prerequisites

- Node.js 20+ (use `nvm` or `fnm`)
- pnpm 9+
- MongoDB (local or Atlas)
- A GitHub account (for OAuth)

### 1. Fork & Clone

```bash
git clone https://github.com/<YOUR_USERNAME>/freeCodeCamp.git
cd freeCodeCamp
```

### 2. Install Dependencies

```bash
pnpm install
```

### 3. Configure Environment

```bash
cp sample.env .env
```

Key `.env` variables to set:

```bash
# MongoDB
MONGOHQ_URL=mongodb://127.0.0.1:27017/freecodecamp

# GitHub OAuth (create at github.com/settings/developers)
GITHUB_ID=$GITHUB_OAUTH_CLIENT_ID
GITHUB_SECRET=$GITHUB_OAUTH_CLIENT_SECRET

# Auth
JWT_SECRET=$YOUR_JWT_SECRET
SESSION_SECRET=$YOUR_SESSION_SECRET

# Email (optional for local dev)
SENDGRID_API_KEY=$SENDGRID_API_KEY
```

### 4. Seed the Database

```bash
pnpm run seed
```

### 5. Start Development Servers

```bash
# Start everything (API + Client)
pnpm run develop

# Or start individually:
pnpm run develop:api      # Fastify API on :3000
pnpm run develop:client   # Gatsby on :8000
```

---

## Curriculum Challenge Structure

Challenges are stored as YAML/Markdown files under `curriculum/challenges/`.

### Challenge File Format

```yaml
# curriculum/challenges/english/02-javascript-algorithms-and-data-structures/basic-javascript/comment-your-javascript-code.md

---
id: bd7123c8c441eddfaeb5bdef  # unique MongoDB ObjectId-style string
title: Comment Your JavaScript Code
challengeType: 1              # 1=JS, 0=HTML, 2=JSX, 3=Vanilla JS, 5=Project, 7=Video
forumTopicId: 16783
dashedName: comment-your-javascript-code
---

# --description--

Comments are lines of code that JavaScript will intentionally ignore.

```js
// This is an in-line comment.
/* This is a multi-line comment */
```

# --instructions--

Try creating one of each type of comment.

# --hints--

hint 1

```js
assert(code.match(/(\/\/)/).length > 0);
```

hint 2

```js
assert(code.match(/(\/\*[\s\S]+?\*\/)/).length > 0);
```

# --seed--

## --seed-contents--

```js
// Your starting code here
```

# --solutions--

```js
// inline comment
/* multi-line
   comment */
```
```

### Challenge Types

| Type | Value | Description |
|------|-------|-------------|
| HTML | 0 | HTML/CSS challenges |
| JavaScript | 1 | JS algorithm challenges |
| JSX | 2 | React component challenges |
| Vanilla JS | 3 | DOM manipulation |
| Python | 7 | Python challenges |
| Project | 5 | Certification projects |
| Video | 11 | Video-based lessons |

---

## Creating a New Challenge

### Using the Helper Script

```bash
# Create a new challenge interactively
pnpm run create-challenge

# Or use the helper directly
cd tools/challenge-helper-scripts
pnpm run create-challenge --superblock responsive-web-design --block css-flexbox
```

### Manual Creation

1. Find the correct directory under `curriculum/challenges/english/`
2. Create a new `.md` file with a unique ID

```bash
# Generate a unique challenge ID
node -e "const {ObjectID} = require('mongodb'); console.log(new ObjectID().toString())"
```

3. Follow the challenge file format above

### Validate Your Challenge

```bash
# Lint and validate all curriculum files
pnpm run test:curriculum

# Test a specific challenge
pnpm run test:curriculum -- --challenge <challenge-id>

# Test a specific block
pnpm run test:curriculum -- --block basic-javascript
```

---

## Writing Challenge Tests

Tests use a custom assertion library. Inside `# --hints--` blocks:

### JavaScript Challenges

```markdown
# --hints--

`myVariable` should be declared with `let`.

```js
assert.match(code, /let\s+myVariable/);
```

The function should return `true` when passed `42`.

```js
assert.strictEqual(myFunction(42), true);
```

The DOM should contain an element with id `main`.

```js
const el = document.getElementById('main');
assert.exists(el);
```
```

### Available Test Utilities

```js
// DOM access (for HTML challenges)
document.querySelector('#my-id')
document.getElementById('test')

// Code inspection
assert.match(code, /regex/);          // raw source code string
assert.include(code, 'someString');

// Value assertions (Chai-style)
assert.strictEqual(actual, expected);
assert.isTrue(value);
assert.exists(value);
assert.approximately(actual, expected, delta);

// For async challenges
// Use __helpers object
const result = await fetch('/api/test');
assert.strictEqual(result.status, 200);
```

---

## API Development (Fastify)

### Route Structure

```typescript
// api/src/routes/example.ts
import { type FastifyPluginCallbackTypebox } from '../helpers/plugin-callback-typebox';
import { Type } from '@fastify/type-provider-typebox';

export const exampleRoutes: FastifyPluginCallbackTypebox = (
  fastify,
  _options,
  done
) => {
  fastify.get(
    '/example/:id',
    {
      schema: {
        params: Type.Object({
          id: Type.String()
        }),
        response: {
          200: Type.Object({
            data: Type.String()
          })
        }
      }
    },
    async (req, reply) => {
      const { id } = req.params;
      return reply.send({ data: `Result for ${id}` });
    }
  );

  done();
};
```

### Adding a New API Route

```typescript
// api/src/app.ts - register the plugin
import { exampleRoutes } from './routes/example';

await fastify.register(exampleRoutes, { prefix: '/api' });
```

### Database Access (Mongoose)

```typescript
// api/src/schemas/user.ts
import mongoose from 'mongoose';

const userSchema = new mongoose.Schema({
  email: { type: String, required: true, unique: true },
  completedChallenges: [
    {
      id: String,
      completedDate: Number,
      solution: String
    }
  ]
});

export const User = mongoose.model('User', userSchema);
```

---

## Client (Gatsby/React) Development

### Adding a New Page

```tsx
// client/src/pages/my-new-page.tsx
import React from 'react';
import { Helmet } from 'react-helmet';
import { useTranslation } from 'react-i18next';

const MyNewPage = (): JSX.Element => {
  const { t } = useTranslation();

  return (
    <>
      <Helmet>
        <title>{t('page-title.my-new-page')} | freeCodeCamp.org</title>
      </Helmet>
      <main>
        <h1>{t('headings.my-new-page')}</h1>
      </main>
    </>
  );
};

export default MyNewPage;
```

### Using the Redux Store

```tsx
// client/src/redux/selectors.ts pattern
import { createSelector } from 'reselect';
import { RootState } from './types';

export const userSelector = (state: RootState) => state.app.user;

export const completedChallengesSelector = createSelector(
  userSelector,
  user => user?.completedChallenges ?? []
);
```

```tsx
// In a component
import { useAppSelector } from '../redux/hooks';
import { completedChallengesSelector } from '../redux/selectors';

const MyComponent = () => {
  const completedChallenges = useAppSelector(completedChallengesSelector);
  return <div>{completedChallenges.length} challenges completed</div>;
};
```

### i18n Translations

```tsx
// Add keys to client/i18n/locales/english/translations.json
{
  "my-component": {
    "title": "My Title",
    "description": "My description with {{variable}}"
  }
}

// Use in component
const { t } = useTranslation();
t('my-component.title');
t('my-component.description', { variable: 'value' });
```

---

## Testing

### Unit Tests (Jest)

```bash
# Run all unit tests
pnpm test

# Run tests for a specific package
pnpm --filter api test
pnpm --filter client test

# Watch mode
pnpm --filter client test -- --watch
```

### Curriculum Tests

```bash
# Validate all challenges
pnpm run test:curriculum

# Validate specific superblock
pnpm run test:curriculum -- --superblock javascript-algorithms-and-data-structures

# Lint challenge markdown
pnpm run lint:curriculum
```

### E2E Tests (Playwright)

```bash
# Run all e2e tests
pnpm run test:e2e

# Run specific test file
pnpm run test:e2e -- e2e/learn.spec.ts

# Run with UI
pnpm run test:e2e -- --ui
```

### Writing E2E Tests

```typescript
// e2e/my-feature.spec.ts
import { test, expect } from '@playwright/test';

test('user can complete a challenge', async ({ page }) => {
  await page.goto('/learn/javascript-algorithms-and-data-structures/basic-javascript/comment-your-javascript-code');

  // Fill in the code editor
  await page.locator('.monaco-editor').click();
  await page.keyboard.type('// inline comment\n/* block comment */');

  // Run tests
  await page.getByRole('button', { name: /run the tests/i }).click();

  // Check results
  await expect(page.getByText('Tests Passed')).toBeVisible();
});
```

---

## Key pnpm Scripts Reference

```bash
# Development
pnpm run develop              # Start all services
pnpm run develop:api          # API only
pnpm run develop:client       # Client only

# Building
pnpm run build                # Build everything
pnpm run build:api            # Build API
pnpm run build:client         # Build client (Gatsby)

# Testing
pnpm test                     # Unit tests
pnpm run test:curriculum      # Validate curriculum
pnpm run test:e2e             # Playwright e2e

# Linting
pnpm run lint                 # ESLint all packages
pnpm run lint:curriculum      # Curriculum markdown lint

# Database
pnpm run seed                 # Seed DB with curriculum data
pnpm run seed:certified-user  # Seed a test certified user

# Utilities
pnpm run create-challenge     # Interactive challenge creator
pnpm run clean                # Clean build artifacts
```

---

## Superblock & Block Naming Conventions

Superblocks map to certifications. Directory names use kebab-case:

```
responsive-web-design/
javascript-algorithms-and-data-structures/
front-end-development-libraries/
data-visualization/
relational-database/
back-end-development-and-apis/
quality-assurance/
scientific-computing-with-python/
data-analysis-with-python/
machine-learning-with-python/
coding-interview-prep/
the-odin-project/
project-euler/
```

Block directories within a superblock:

```
responsive-web-design/
├── basic-html-and-html5/
├── basic-css/
├── applied-visual-design/
├── css-flexbox/
└── css-grid/
```

---

## Common Patterns & Gotchas

### Challenge ID Generation

Every challenge needs a unique 24-character hex ID:

```typescript
// tools/challenge-helper-scripts/helpers/id-gen.ts
import { ObjectId } from 'bson';
export const generateId = (): string => new ObjectId().toHexString();
```

### Adding Forum Links

Every challenge needs a `forumTopicId` linking to forum.freecodecamp.org:

```yaml
forumTopicId: 301090  # Must be a real forum post ID
```

### Curriculum Meta Files

Each block needs a `_meta.json`:

```json
{
  "name": "Basic JavaScript",
  "dashedName": "basic-javascript",
  "order": 0,
  "time": "5 hours",
  "template": "",
  "required": [],
  "isUpcomingChange": false,
  "isBeta": false,
  "isLocked": false,
  "isPrivate": false
}
```

### Testing with Authentication

```typescript
// In e2e tests, use the test user fixture
import { authedUser } from './fixtures/authed-user';

test.use({ storageState: 'playwright/.auth/user.json' });

test('authenticated action', async ({ page }) => {
  // page is already logged in
  await page.goto('/settings');
  await expect(page.getByText('Account Settings')).toBeVisible();
});
```

---

## Troubleshooting

### MongoDB Connection Issues

```bash
# Check if MongoDB is running
mongosh --eval "db.adminCommand('ping')"

# Start MongoDB (macOS with Homebrew)
brew services start mongodb-community

# Use in-memory MongoDB for tests
MONGOHQ_URL=mongodb://127.0.0.1:27017/freecodecamp-test pnpm test
```

### Port Conflicts

```bash
# API runs on 3000, Client on 8000
lsof -i :3000
kill -9 <PID>
```

### Curriculum Validation Failures

```bash
# See detailed error output
pnpm run test:curriculum -- --verbose

# Common issues:
# - Missing forumTopicId
# - Duplicate challenge IDs
# - Invalid challengeType
# - Malformed YAML frontmatter
```

### Node/pnpm Version Mismatch

```bash
# Use the project's required versions
node --version   # Should match .nvmrc
pnpm --version   # Should match packageManager in package.json

nvm use          # Switches to correct Node version
```

### Client Build Errors

```bash
# Clear Gatsby cache
pnpm --filter client run clean
pnpm run develop:client
```

---

## Contributing Workflow

```bash
# 1. Create a feature branch
git checkout -b fix/challenge-typo-in-basic-js

# 2. Make changes and test
pnpm run test:curriculum
pnpm test

# 3. Lint
pnpm run lint

# 4. Commit using conventional commits
git commit -m "fix(curriculum): correct typo in basic-javascript challenge"

# 5. Push and open PR against main
git push origin fix/challenge-typo-in-basic-js
```

Commit message prefixes: `fix:`, `feat:`, `chore:`, `docs:`, `refactor:`, `test:`

---

## Resources

- Contribution guide: https://contribute.freecodecamp.org
- Forum: https://forum.freecodecamp.org
- Discord: https://discord.gg/PRyKn3Vbay
- How to report bugs: https://forum.freecodecamp.org/t/how-to-report-a-bug/19543
