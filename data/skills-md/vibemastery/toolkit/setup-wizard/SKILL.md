---
name: setup-wizard
description: "First-time Laravel project setup. Use when the user says 'get started', 'set up a new project', 'install Laravel', or 'I am a beginner'. Installs Laravel Herd, creates a fresh project with Inertia + React, Pest, and Filament, and configures Laravel Boost for Claude Code. Runs once per project only."
---

# VibeMastery Setup Wizard

You are guiding a complete beginner through setting up their first Laravel project.
**Tone**: Friendly, calm, encouraging. Never assume technical knowledge.
**Narration rule**: Before running each command, tell the builder in one plain-English sentence what you're about to do and why. After it finishes, confirm success or explain any error in plain language before continuing.

---

## Before You Begin

Greet the builder with this message (adapt naturally, don't paste verbatim):

> "Welcome! I'm going to set up your first Laravel project. This takes about 10–15 minutes and I'll walk you through every step. You won't need to understand everything right now — I'll explain what matters as we go."

Ask: **"What do you want to call your project?"**

Rules for the name:
- Lowercase letters, numbers, and hyphens only
- No spaces (use hyphens instead: `my-blog`, `photo-gallery`)
- Keep it short and descriptive

Store it as `PROJECT_NAME` — you'll use it throughout. Confirm the name before proceeding.

Also ask: **"Where would you like to create the project? Just press Enter to use the default (`~/Projects`), or type a different path."**

Store it as `PROJECTS_DIR` — default to `~/Projects` if they don't specify.

Also ask: **"Will your project need user accounts — things like login, registration, or a user dashboard?"**

- **Yes** → set `AUTH=true`
- **No / not sure** → set `AUTH=false`

And: **"Will you need an admin panel to manage your data — for example, viewing users, editing content, or managing orders?"**

- **Yes** → set `ADMIN=true`
- **No / not sure** → set `ADMIN=false`

Both can be added later, but it's easier to include them from the start if they know they'll need them.

---

## Step 1 — Detect Your Computer Type

*Tell the builder: "First, let me check what kind of computer you're using so I can give you the right instructions."*

Run:
```bash
uname -s
```

- **Output `Darwin`** → macOS path (continue to Step 2-Mac)
- **Output `MINGW64`, `MSYS`, or `CYGWIN`** → Windows path (continue to Step 2-Win)
- **Output `Linux`** → Stop and explain: *"This wizard supports macOS and Windows. Linux isn't supported yet — check back soon, or visit vibemastery.ai for alternatives."*

---

## Step 2-Mac — Install Laravel Herd (macOS)

*Tell the builder: "Laravel Herd is an app that manages PHP and your local server — it's the official, easiest way to run Laravel on a Mac."*

First check if Herd is already installed:
```bash
herd --version
```

If it's already installed, say "Herd is already installed — great!" and skip to Step 3.

If not installed:
> "Let's download Laravel Herd. Go to **herd.laravel.com/download** in your browser and download the DMG file. Open it, drag Herd to your Applications folder, then launch it."

Wait for confirmation that Herd has opened. It will run a short onboarding wizard that installs PHP automatically — tell them to follow it and let you know when it finishes.

> "Herd should be showing a setup wizard on your screen. Follow the steps it shows you — it installs PHP and Composer automatically. Let me know when it says it's ready."

Wait for confirmation Herd is running. Then verify:
```bash
php -v && composer --version
```

If this fails: *"Herd didn't add PHP to your terminal yet. Close this terminal window, open a new one, and type `php -v` again. This is normal the first time."*

Continue to Step 3.

---

## Step 2-Win — Install Laravel Herd (Windows)

*Tell the builder: "Laravel Herd for Windows manages PHP and your local server automatically — it's the official way to run Laravel on Windows."*

First check if Herd is already installed:
```bash
herd --version
```

If already installed, skip to Step 3.

If not installed:
> "Please go to **herd.laravel.com** in your browser and download the Windows installer. Run it and follow the setup steps — it installs PHP and Composer for you automatically. Let me know when the Herd icon appears in your taskbar."

Wait for confirmation. Then verify:
```bash
php -v && composer --version
```

If this fails: *"Close this terminal, open a new one, and try `php -v` again. Herd needs a fresh terminal to be recognised."*

Continue to Step 3.

---

## Step 3 — Create the Laravel Project

*Tell the builder: "Now I'll create your actual Laravel project. This downloads the framework and sets everything up in a new folder."*

Navigate to their chosen directory:
```bash
mkdir -p {{PROJECTS_DIR}} && cd {{PROJECTS_DIR}}
```

Create the project — use the command that matches their choices:

**If AUTH=true:**
```bash
laravel new {{PROJECT_NAME}} --react --pest --database=sqlite --git --npm --boost
```

**If AUTH=false:**
```bash
laravel new {{PROJECT_NAME}} --react --no-authentication --pest --database=sqlite --git --npm --boost
```

> "This one command creates the project, installs React and Inertia, sets up Pest for testing, connects your AI assistant to the project, and initialises Git — all in one go. It downloads about 100 MB of packages, so give it a few minutes."

Move into the project folder for the rest of the setup:
```bash
cd {{PROJECT_NAME}}
```

### Install the VibeMastery Stack

**If ADMIN=true** — Install Filament (admin panel):
```bash
composer require filament/filament:"^5.0"
php artisan filament:install --panels
```

When Filament asks for a panel ID, use `admin`.

Then create your admin user:
```bash
php artisan make:filament-user
```

It will ask for a name, email, and password — these are your login credentials for the panel.

> "Your admin panel is ready at `/admin`. Log in with the credentials you just created."

Then refresh Laravel Boost so it picks up all the newly installed packages:
```bash
php artisan boost:update
```

---

## Step 4 — Set Up Your Local Website Address

*Tell the builder: "Right now your project is just files on your computer. This step gives it a real web address you can open in your browser — like `{{PROJECT_NAME}}.test`."*

```bash
herd link
herd secure
```

> "Open your browser and go to `https://{{PROJECT_NAME}}.test`. You should see the Laravel welcome page."

If the page doesn't load: *"Make sure Herd is running, then try again. If it still doesn't work, let me know what error you see."*

---

## Step 5 — Configure Your AI Coding Tool

You are the AI tool running this skill. Identify which tool you are (Claude Code, Codex, OpenCode, or other) and continue to the matching section below.

### For Claude Code

> "Laravel Boost was already set up as part of the project creation — Claude can see your project's routes, database schema, and documentation automatically. Nothing extra needed."

### For OpenCode

*Tell the builder: "I'm going to create a small config file so OpenCode knows how to work with your project."*

Read `references/opencode.json.template`, replace `{{PROJECT_NAME}}`, write to `opencode.json`.

### For Codex

No extra configuration is needed. Codex picks up project context automatically from your project structure.

---

## Step 6 — First Run

*Tell the builder: "Everything is set up. Let's see your project running for the first time."*

Open `https://{{PROJECT_NAME}}.test` in the browser. You should see the Laravel welcome page.

> "🎉 Your project is live! Whenever you're working on it, run `npm run dev` in your terminal to enable live reloading. You don't need it just to view the site — only when you're actively making changes."

Create the first Git commit:
```bash
git add -A
git commit -m "Initial VibeMastery project setup"
```

> "I've saved a snapshot of your project. This is your starting point — you can always come back to this."

---

## Handoff

End the session with this message (adapt naturally):

> "Your project is ready at **{{PROJECT_NAME}}.test**. From now on, just tell me what you want to build — you never need to run the Setup Wizard again."

Remind them:
- They can run tests with `php artisan test`
- If ADMIN=true: their admin panel is at `https://{{PROJECT_NAME}}.test/admin`
- If they get an error they don't understand, they can ask you to explain it

Then give this closing instruction:

> "One last thing — close this tab and open your project folder (`{{PROJECTS_DIR}}/{{PROJECT_NAME}}`) in a new window. That's where you'll do all your building from now on."

**The setup is complete. The builder is ready to build.**
