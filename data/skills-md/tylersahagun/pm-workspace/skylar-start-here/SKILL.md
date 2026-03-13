---
name: skylar-start-here
description: Get the AskElephant app and Storybook running locally for a designer. Use when the designer says "start the app", "run locally", "see my changes", "open storybook", "first time setup", "how do I see the app", or "set up my environment".
---

# Start Here -- Running the App Locally

This skill gets the AskElephant web app or Storybook running so the designer can see their changes visually. Handle all technical steps silently. Speak only in terms of what the designer will see, not what commands are running.

---

## Triggers

Activate this skill when the designer says any of:

- "Start the app"
- "Run locally"
- "Open Storybook"
- "Start Storybook"
- "I want to see the components"
- "How do I see my changes?"
- "First time setup"
- "Set up my environment"
- "I can't see the app"

---

## Procedure

### Step 1: Check Submodule Status

The elephant-ai repo is a git submodule. Check if it's initialized:

```bash
# In the workspace root (pm-workspace/)
ls elephant-ai/apps/web/package.json
```

If the file doesn't exist, initialize the submodule:

```bash
git submodule update --init --recursive
```

Tell the designer: "Setting up the codebase for the first time. This takes a minute."

### Step 2: Check Dependencies

Check if `node_modules` exists in the elephant-ai directory:

```bash
ls elephant-ai/node_modules/.package-lock.json
```

If missing, install dependencies:

```bash
cd elephant-ai && pnpm install
```

Tell the designer: "Installing project dependencies. Almost ready."

### Step 3: Start the Requested Server

**If the designer wants Storybook** (component viewer -- recommended for design work):

```bash
cd elephant-ai/apps/web && pnpm storybook
```

Wait for the server to start. Check the terminal output for the URL (typically `localhost:6006`).

Tell the designer: "Storybook is running. Open **localhost:6006** in your browser. You'll see every component in our design system organized by category. Use the sidebar on the left to navigate."

**If the designer wants the full app:**

```bash
cd elephant-ai/apps/web && pnpm dev
```

Wait for the server to start. Check terminal for the URL (typically `localhost:5173` or `localhost:3001`).

Tell the designer: "The app is running. Open **localhost:5173** in your browser. You'll see the full AskElephant application."

### Step 4: Handle Errors

If the server fails to start:

1. Read the error message
2. Common fixes:
   - **Port in use**: Kill the process using the port, then retry
   - **Missing dependency**: Run `pnpm install` and retry
   - **TypeScript error**: Fix the type error in the source file
   - **Build error**: Read the error, fix the file, and retry
3. Tell the designer what happened in plain terms: "There was a small configuration issue. I fixed it and restarted. You're good to go."

### Step 5: Orientation (First Time Only)

If this is the designer's first time, explain what they're seeing:

**For Storybook:**
"You're looking at our component library in Storybook. Here's how to navigate:

- **Left sidebar**: All our components organized by category (UI, Chat, Engagements, etc.)
- **Canvas tab**: Shows the component rendered at full size
- **Controls panel** (bottom): Lets you toggle component props to see different states
- **Viewport button** (toolbar): Switch between mobile (375px), tablet (768px), and desktop (1280px)
- **Theme button** (toolbar): Toggle between light and dark mode

The `ui/` folder in the sidebar contains all our design system primitives -- buttons, cards, inputs, badges, etc. Start there to get familiar with the building blocks."

**For the full app:**
"You're seeing the AskElephant web app. You'll need to log in to see most features. The main areas are:

- **Sidebar navigation**: Main app sections
- **Chat**: The AI chat interface
- **Engagements**: Meeting and call views
- **Settings**: Configuration pages

For design iteration, Storybook is usually better because you can see components in isolation without needing to navigate through the app."

---

## Checking If a Server Is Already Running

Before starting a new server, check the terminal files to see if one is already running:

1. List terminal files to find active processes
2. If Storybook or dev server is already running, tell the designer: "Storybook is already running at localhost:6006. Just refresh your browser to see your latest changes."

---

## Stopping a Server

When the designer says "stop the app" or "stop Storybook":

1. Find the terminal running the server
2. Send Ctrl+C to stop it
3. Tell the designer: "Server stopped."

---

## Restarting After Changes

When the designer asks to see changes and a server is running:

- **Most changes**: Hot reload handles it automatically. Tell the designer: "Your changes are live. Just check your browser -- it should update automatically."
- **CSS token changes**: May require a full page refresh. Tell the designer: "Refresh your browser to see the style changes."
- **New files/dependencies**: May require a server restart. Handle it automatically.
