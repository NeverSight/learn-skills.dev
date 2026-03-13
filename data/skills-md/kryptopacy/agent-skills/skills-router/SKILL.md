---
name: skills-router
version: 2.1.0
description: >
  Meta-skill that routes any task to the correct specialist skill.
  Load at the start of every session. Triggers on: coding, frontend, backend,
  database, testing, deployment, payments, blockchain, AI, design, marketing,
  content, docs, mobile, DevOps, security, or productivity tasks.
keywords:
  - router
  - skill-selection
  - best-practices
  - meta-skill
  - task-routing
  - next.js
  - react
  - supabase
  - stripe
  - solana
  - playwright
  - typescript
  - tailwind
  - shadcn
  - zustand
  - vercel
  - deployment
  - database
  - postgres
  - rls
  - testing
  - tdd
  - e2e
  - blockchain
  - web3
  - nft
  - defi
  - threejs
  - nestjs
  - turborepo
  - monorepo
  - rag
  - ai-sdk
  - agents
  - voice-ai
  - design
  - ui
  - ux
  - mobile
  - expo
  - react-native
  - seo
  - copywriting
  - marketing
  - cro
  - pricing
  - onboarding
  - email
  - docs
  - readme
  - logging
  - debugging
  - code-review
  - qa
  - session
  - handoff
  - brainstorming
  - parallel-agents
  - dispatching
  - test-driven
  - tdd
  - agent-md
  - refactor
  - superdesign
---

# Skills Router

A meta-skill directory — maps any task to the right specialist skill before you write a single line of code.

## Agent Protocol

1. **Check for project context first.** Before routing, look for a project memory file in the project root and read it for stack-specific rules that override generic skill guidance. Check for any of these (whichever exists):
   - `GEMINI.md` — Gemini / Antigravity
   - `CLAUDE.md` — Claude Code
   - `AGENTS.md` — OpenAI Codex
   - `.cursorrules` — Cursor
   - `.github/copilot-instructions.md` — GitHub Copilot
   - `CONVENTIONS.md` — Aider and others
2. **Match your task** to the domain table below.
3. **Find the skill's `SKILL.md` file.** Skills may be installed locally or globally. Before concluding a skill is missing, you must check the following locations using proper absolute paths (resolve the user's home directory programmatically before using file-reading tools; do NOT pass literal `~/` or `%USERPROFILE%` strings to tools like `view_file`):
   - **Central Global:** `<USER_HOME_DIR>/.agents/skills/<skill-name>/SKILL.md` (Check here first, this is the source of truth)
   - **Agent-Specific Global:** `<USER_HOME_DIR>/<YOUR_AGENT_DIR>/skills/<skill-name>/SKILL.md` (e.g. `.cursor/skills`, `.gemini/antigravity/skills`, `.cline/skills`)
   - **Local Workspace:** `./.agents/skills/<skill-name>/SKILL.md` or `./.cursor/skills/<skill-name>/SKILL.md`
4. **If not found** in any of these paths, run the install command from the table (if one exists), **appending `-g`** to ensure it installs to the central `.agents` directory. Let the installation finish.
   - **Self-Healing Protocol:** If the install command explicitly fails (e.g., repository not found), immediately run `npx skills find <skill-name>` to get the updated, verified command. Use it to install, and then update the table in this `SKILL.md` file with the corrected link permanently.
5. **Load the skill** using the `view_file` tool on the exact absolute path to `SKILL.md`. Once loaded, you MUST output `"Loaded specialist skill: [name]"` in your chat response so the user sees the routing succeeded.
6. **Follow that skill's instructions** for the task.
7. **Before claiming done**, load the `verification-before-completion` skill (find it in the tables below and follow steps 3-5 to load it).
8. **If you used a skill not listed here**, add it to the **Pending Review** section at the bottom — never to the live tables.

> If no skill matches, you MUST append a proposed skill name and task description as a bullet point to the **Still Needed** section of this document, then proceed with built-in knowledge.

---

## Pre-Baked Critical Rules (Always Active)

These rules apply regardless of which skill you load:

- **Supabase RLS**: Always wrap `auth.uid()` in `(SELECT auth.uid())` — prevents per-row re-evaluation
- **One RLS policy per table/role/action** — never create duplicate permissive policies
- **Supabase browser client**: Singleton cached on `globalThis` only — prevents "Multiple GoTrueClient instances"
- **Server Components by default** — `'use client'` only when strictly required (event handlers, hooks, browser APIs)
- **Stripe webhooks**: Always verify signature with `stripe.webhooks.constructEvent()` before processing

---

## Domain → Skill Routing Table

### ⚛️ React / Next.js / Frontend

| Task | Skill | Install |
|------|-------|---------|
| React performance, data fetching, bundle size | `vercel-react-best-practices` | `npx skills add https://github.com/vercel-labs/agent-skills --skill vercel-react-best-practices` |
| React composition, compound components, boolean-prop refactors | `vercel-composition-patterns` | `npx skills add https://github.com/vercel-labs/agent-skills --skill vercel-composition-patterns` |
| UI review, accessibility audit, Web Interface Guidelines | `web-design-guidelines` | `npx skills add https://github.com/vercel-labs/agent-skills --skill web-design-guidelines` |
| shadcn/ui components, Tailwind themes, form/dialog patterns | `shadcn-ui` | `npx skills add https://github.com/google-labs-code/stitch-skills --skill shadcn-ui` |
| Zustand global state, persist middleware, hydration | `zustand-state-management` | `npx skills add https://github.com/jezweb/claude-skills --skill zustand-state-management` |
| Production-grade UI, distinctive design, avoiding generic AI aesthetics | `frontend-design` | `npx skills add https://github.com/anthropics/skills --skill frontend-design` |
| Design agent, UI iteration, template-driven design | `superdesign` | `npx skills find superdesign` |

### 🗄️ Database / Supabase / Postgres

| Task | Skill | Install |
|------|-------|---------|
| Supabase RLS, query optimization, indexes, connection pooling | `supabase-postgres-best-practices` | `npx skills add https://github.com/oldwinter/skills --skill supabase-postgres-best-practices` |

### 💳 Payments / Billing

| Task | Skill | Install |
|------|-------|---------|
| Stripe integration, CheckoutSessions, webhooks, subscriptions | `stripe-best-practices` | `npx skills add https://github.com/stripe/ai --skill stripe-best-practices` |
| Recurring billing, subscription lifecycle, dunning, invoicing | `billing-automation` | `npx skills add https://github.com/wshobson/agents --skill billing-automation` |

### ⛓️ Blockchain / Web3 / Solana

| Task | Skill | Install |
|------|-------|---------|
| Solana security audit, CPI, PDA, signer/ownership checks | `solana-vulnerability-scanner` | `npx skills find solana-vulnerability-scanner` |
| Meteora DeFi: DLMM, DAMM, bonding curves, Alpha Vaults | `meteora` | `npx skills add https://github.com/sendaifun/skills --skill meteora` |
| ERC-721, ERC-1155 NFT contracts, minting, metadata | `nft-standards` | `npx skills add https://github.com/wshobson/agents --skill nft-standards` |
| Smart contract testing, Hardhat, Foundry, mainnet forking | `web3-testing` | `npx skills add https://github.com/wshobson/agents --skill web3-testing` |

### 🧪 Testing / QA

| Task | Skill | Install |
|------|-------|---------|
| Browser automation, Playwright scripts, E2E tests | `playwright-skill` | `npx skills add https://github.com/testdino-hq/playwright-skill --skill playwright-skill` |
| Web app functional testing, decision trees | `webapp-testing` | `npx skills add https://github.com/ComposioHQ/awesome-claude-skills --skill webapp-testing` |
| Test-driven development, red-green-refactor, TDD workflow | `test-driven-development` | `npx skills add https://github.com/obra/superpowers --skill test-driven-development` |
| QA test plans, regression suites, bug reports, Figma validation | `qa-test-planner` | `npx skills add https://github.com/softaworks/agent-toolkit --skill qa-test-planner` |

### 🚀 Deployment / DevOps / Infra

| Task | Skill | Install |
|------|-------|---------|
| Turborepo monorepo, pipelines, caching, CI | `turborepo` | `npx skills add https://github.com/vercel/turborepo --skill turborepo` |
| Server management, process management, scaling strategy | `server-management` | `npx skills add https://github.com/sickn33/antigravity-awesome-skills --skill server-management` |
| Expo iOS/Android/web deployment | `expo-deployment` | `npx skills add https://github.com/expo/skills --skill expo-deployment` |

### 🤖 AI / LLM / Agents

| Task | Skill | Install |
|------|-------|---------|
| Vercel AI SDK, generateText, streamText, tool calling | `ai-sdk` | `npx skills add https://github.com/vercel/ai --skill ai-sdk` |
| Cloudflare Agents SDK, stateful agents, RPC, MCP | `agents-sdk` | `npx skills add https://github.com/cloudflare/skills --skill agents-sdk` |
| RAG systems, vector databases, semantic search | `rag-implementation` | `npx skills add https://github.com/wshobson/agents --skill rag-implementation` |
| Voice AI, OpenAI Realtime API, Vapi, Deepgram, ElevenLabs | `voice-ai-development` | `npx skills add https://github.com/sickn33/antigravity-awesome-skills --skill voice-ai-development` |
| Dispatching parallel agents, multi-agent coordination | `dispatching-parallel-agents` | `npx skills add https://github.com/obra/superpowers --skill dispatching-parallel-agents` |

### 📱 Mobile

| Task | Skill | Install |
|------|-------|---------|
| Mobile-first design, touch patterns, iOS/Android conventions | `mobile-design` | `npx skills add https://github.com/sickn33/antigravity-awesome-skills --skill mobile-design` |
| Telegram Mini Apps, TON ecosystem, WebApp API | `telegram-mini-app` | `npx skills add https://github.com/sickn33/antigravity-awesome-skills --skill telegram-mini-app` |

### 🎨 Design / UX

| Task | Skill | Install |
|------|-------|---------|
| UI/UX design system, accessibility, performance, charts | `ui-ux-pro-max` | `npx skills add https://github.com/oldwinter/skills --skill ui-ux-pro-max` |
| SEO audit: technical, on-page, Core Web Vitals | `seo-audit` | `npx skills add https://github.com/oldwinter/skills --skill seo-audit` |
| Full website audit, crawl, accessibility, performance | `audit-website` | `npx skills add https://github.com/oldwinter/skills --skill audit-website` |

### 📊 Backend / TypeScript / Architecture

| Task | Skill | Install |
|------|-------|---------|
| TypeScript types, performance, monorepo, migration | `typescript-expert` | `npx skills find typescript-expert` |
| NestJS modules, dependency injection, guards, TypeORM | `nestjs-expert` | `npx skills find nestjs-expert` |
| Logging strategy, wide events, canonical log lines | `logging-best-practices` | `npx skills add https://github.com/boristane/agent-skills --skill logging-best-practices` |
| Debugging bugs, test failures, unexpected behavior | `systematic-debugging` | `npx skills add https://github.com/obra/superpowers --skill systematic-debugging` |
| Code review, PR feedback, knowledge sharing | `code-review-excellence` | `npx skills add https://github.com/wshobson/agents --skill code-review-excellence` |

### 📧 Communications / Email

| Task | Skill | Install |
|------|-------|---------|
| Email deliverability, SPF/DKIM/DMARC, bounce rates, compliance | `email-best-practices` | `npx skills add https://github.com/resend/email-best-practices --skill email-best-practices` |
| Twilio SMS, voice calls, WhatsApp, 2FA | `twilio-communications` | `npx skills add https://github.com/sickn33/antigravity-awesome-skills --skill twilio-communications` |

### 🖼️ Documents / Media

| Task | Skill | Install |
|------|-------|---------|
| PDF creation, extraction, manipulation | `pdf` | `npx skills add https://github.com/ComposioHQ/awesome-claude-skills --skill pdf` |
| PowerPoint creation, editing, template workflows | `pptx` | `npx skills add https://github.com/ComposioHQ/awesome-claude-skills --skill pptx` |
| Remotion video, animation, programmatic rendering | `remotion-best-practices` | `npx skills add https://github.com/oldwinter/skills --skill remotion-best-practices` |
| Three.js scenes, cameras, renderers, Object3D | `threejs-fundamentals` | `npx skills add https://github.com/cloudai-x/threejs-skills --skill threejs-fundamentals` |
| Mermaid diagrams, flowcharts, sequence diagrams | `mermaid-visualizer` | `npx skills add https://github.com/oldwinter/skills --skill mermaid-visualizer` |
| Domain naming, brainstorming, TLD strategy | `domain-name-brainstormer` | `npx skills add https://github.com/ComposioHQ/awesome-claude-skills --skill domain-name-brainstormer` |

### ✍️ Content / Writing / Marketing

| Task | Skill | Install |
|------|-------|---------|
| Marketing copy, headlines, CTAs, landing pages | `copywriting` | `npx skills add https://github.com/coreyhaines31/marketingskills --skill copywriting` |
| Remove AI writing patterns, humanize content | `humanizer` | `npx skills add https://github.com/oldwinter/skills --skill humanizer` |
| Data visualization, stakeholder presentations, narratives | `data-storytelling` | `npx skills add https://github.com/wshobson/agents --skill data-storytelling` |
| Psychological principles, mental models, persuasion | `marketing-psychology` | `npx skills add https://github.com/coreyhaines31/marketingskills --skill marketing-psychology` |

### 🏷️ Product / Growth / CRO

| Task | Skill | Install |
|------|-------|---------|
| In-app paywalls, upgrade screens, freemium conversion | `paywall-upgrade-cro` | `npx skills find paywall-upgrade-cro` |
| Signup/registration flow optimization, reduce dropoff | `signup-flow-cro` | `npx skills find signup-flow-cro` |
| User onboarding, activation, aha moment, retention | `onboarding-cro` | `npx skills add https://github.com/coreyhaines31/marketingskills --skill onboarding-cro` |
| Pricing tiers, value metrics, packaging, willingness to pay | `pricing-strategy` | `npx skills find pricing-strategy` |
| Product Hunt, launch planning, go-to-market, waitlists | `launch-strategy` | `npx skills find launch-strategy` |
| 10x features, product strategy, high-leverage opportunities | `game-changing-features` | `npx skills find game-changing-features` |
| Ideation, creative thinking, exploring possibilities | `brainstorming` | `npx skills add https://github.com/obra/superpowers --skill brainstorming` |

### 📚 Docs / README

| Task | Skill | Install |
|------|-------|---------|
| Writing/editing `/docs` directory or `.md` files | `docs-writer` | `npx skills add https://github.com/google-gemini/gemini-cli --skill docs-writer` |
| Writing or improving README files | `crafting-effective-readmes` | `npx skills add https://github.com/softaworks/agent-toolkit --skill crafting-effective-readmes` |
| Browser automation for docs validation | `agent-browser` | `npx skills add https://github.com/oldwinter/skills --skill agent-browser` |

### 🔧 Agent Productivity / Skills Management

| Task | Skill | Install |
|------|-------|---------|
| Find and install skills from skills.sh | `find-skills` | `npx skills add https://github.com/oldwinter/skills --skill find-skills` |
| Create new skills, SKILL.md authoring | `skill-creator` | `npx skills add https://github.com/oldwinter/skills --skill skill-creator` |
| Refactor AGENT.md, CLAUDE.md, memory files | `agent-md-refactor` | `npx skills add https://github.com/softaworks/agent-toolkit --skill agent-md-refactor` |
| Writing skills, skills authoring workflow | `writing-skills` | `npx skills add https://github.com/obra/superpowers --skill writing-skills` |
| Session transfer, context handoff between agents | `session-handoff` | `npx skills add https://github.com/softaworks/agent-toolkit --skill session-handoff` |
| Execute a written implementation plan | `executing-plans` | `npx skills add https://github.com/obra/superpowers --skill executing-plans` |

### ✅ Verification

| Task | Skill | Install |
|------|-------|---------|
| Before claiming any task complete, fixed, or passing | `verification-before-completion` | `npx skills add https://github.com/obra/superpowers --skill verification-before-completion` |

---

## Still Needed (run `npx skills find <name>` to resolve)

- `superdesign`
- `typescript-expert`
- `nestjs-expert`
- `solana-vulnerability-scanner`
- `paywall-upgrade-cro`
- `signup-flow-cro`
- `pricing-strategy`
- `launch-strategy`
- `game-changing-features`

---

## ⏳ Pending Review

> **Agents**: Append newly discovered skills HERE only. Never edit the live routing tables above.
> **Humans**: Review entries below, verify the install command on skills.sh, then promote to the correct table.

| Skill | Description | Install Command | Proposed In Session |
|-------|-------------|-----------------|---------------------|
| _(empty)_ | | | |

### 🔒 Security Note
Before promoting any pending entry:
1. Verify the GitHub repo exists and is from a trusted owner
2. Check the skill's page on [skills.sh](https://skills.sh) for security badges (Socket, Snyk, Gen Agent Trust Hub)
3. Review the SKILL.md content in the repo before installing
4. Never install skills from repos you don't recognise

---

## Install Note

- **Verified** `npx skills add https://github.com/...` commands were confirmed on skills.sh
- **`npx skills find <name>`** searches skills.sh live and returns the confirmed install command
- **IMPORTANT:** Always append `-g` to the `npx skills add` commands listed in the tables above when executing them to ensure central installation.
