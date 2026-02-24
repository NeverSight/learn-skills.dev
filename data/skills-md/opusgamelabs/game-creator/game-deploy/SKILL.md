---
name: game-deploy
description: Deploy browser games to GitHub Pages or other hosting. Use when deploying a game, setting up hosting, or publishing a game build.
disable-model-invocation: true
---

# Game Deployment

Deploy your browser game for public access.

## GitHub Pages Deployment

### Prerequisites

- GitHub CLI installed (`gh`)
- Git repository initialized and pushed to GitHub

### Quick Deploy

```bash
npm run build && npx gh-pages -d dist
```

### Full Setup

1. **Build the game**:

```bash
npm run build
```

2. **Ensure `vite.config.js` has the correct base path** if deploying to a subdirectory:

```js
export default defineConfig({
  base: '/<repo-name>/',
  // ... rest of config
});
```

3. **Deploy with GitHub CLI**:

```bash
gh repo create <game-name> --public --source=. --push
npm install -D gh-pages
npx gh-pages -d dist
```

4. **Enable GitHub Pages** in repo settings (should auto-detect the `gh-pages` branch).

Your game is live at: `https://<username>.github.io/<repo-name>/`

### Automated Deploys

Add to `package.json`:

```json
{
  "scripts": {
    "deploy": "npm run build && npx gh-pages -d dist"
  }
}
```

## Play.fun Registration

After deploying, register your game on Play.fun for monetization. Use the `/game-creator:playdotfun` skill for integration details.

The deployed URL becomes your `gameUrl` when registering:

```typescript
await client.games.register({
  name: 'Your Game Name',
  gameUrl: 'https://<username>.github.io/<repo-name>/',
  maxScorePerSession: 500,
  maxSessionsPerDay: 20,
  maxCumulativePointsPerDay: 5000
});
```

## Other Hosting Options

- **Vercel**: `npx vercel --prod` (auto-detects Vite)
- **Netlify**: Connect repo, set build command to `npm run build`, publish dir to `dist`
- **Railway**: Use the Railway skill for deployment
- **itch.io**: Upload the `dist/` folder as an HTML5 game

## Pre-Deploy Checklist

- [ ] `npm run build` succeeds with no errors
- [ ] Test the production build with `npm run preview`
- [ ] Remove any `console.log` debug statements
- [ ] Verify all assets are included in the build
- [ ] Check mobile/responsive behavior if applicable
- [ ] Set appropriate `<title>` and meta tags in `index.html`
