---
name: setup-deploy
description: Configure the Puzzmo CLI for uploading game builds
---

# Setup Deploy

Configure the project to deploy game builds to Puzzmo using the CLI.

## Steps

1. Install the Puzzmo CLI as a dev dependency:
   ```
   npm install --save-dev @puzzmo/cli
   ```

2. Add deploy scripts to `package.json`:
   ```json
   {
     "scripts": {
       "deploy": "npm run build && puzzmo upload GAMESLUG dist",
       "deploy:only": "puzzmo upload GAMESLUG dist"
     }
   }
   ```

3. Replace `GAMESLUG` with the actual game slug.

4. Create a `.gitignore` if it doesn't exist, including:
   ```
   node_modules/
   dist/
   .env
   ```

5. Initialize a git repository if not already initialized:
   ```
   git init
   ```

6. Add a `README.md` with basic instructions:
   ```markdown
   # Game Name

   ## Development
   npm run dev

   ## Build
   npm run build

   ## Deploy
   puzzmo login <your-token>
   npm run deploy
   ```

## Success Criteria

- `npm run build` completes without errors
- `puzzmo upload` command is configured in package.json
- `.gitignore` excludes node_modules and dist
- Game slug matches across all config files
