---
name: ai-integration-architect
description: 'Use when the user describes an organization''s current tools, team, and goals and wants a plan for how to embed AI (Claude) into their operations -- the overall integration architecture and rollout, not a single automation. Trigger on: "how should we bring AI into this company", "AI integration plan", "embed Claude into our workflows", "audit our tool stack for AI", "where should Claude sit in our architecture", "AI adoption rollout plan", or someone describing their current tools (Slack, a CRM, an org-management tool, automation platforms like n8n/Make/Zapier) and asking what to do with AI. Not for a single one-off automation request -- use agent-architecture-advisor for that instead. Not for picking a personal chat interface.'
---

# AI Integration Architect

Judgment for turning a description of a company's tools, team, and goals into an AI integration architecture and phased rollout -- generalized from a real engagement (see the worked example at the bottom). This is a company-level version of the same discipline agent-architecture-advisor applies to a single task: don't skip straight to "which tool," establish the picture first.

## Step 1: Intake -- get the picture before proposing anything

Don't design from a vague goal like "bring AI into the company." Get concrete on:

- **Current tool stack** -- what's actually in use today, including redundant/overlapping tools nobody's explained yet (two automation platforms, two chat tools). Redundancy that's "not yet explained" is itself a finding worth naming, not something to silently pick a favorite on.
- **Team size and existing roles** -- especially whether someone *already does* adjacent work (an existing agent-builder, an ops person who half-automates things by hand). Never design around or replace that person by default; the plan has to route through them, not past them.
- **The actual mandate** -- internal tooling, customer-facing product, or both. Don't let scope creep into the untasked half.
- **Access and blocking dependencies** -- what you don't have access to yet, and what single unknown (an API, a webhook, a permission) the rest of the plan depends on.
- **Non-technical blockers running in parallel** -- pay, role classification, authority to make changes. These aren't part of the technical plan but shouldn't get silently buried under it either; flag them as their own tracked item.

## Step 2: The core architectural call -- hub-and-spoke, not a mesh

The recurring right answer across tool integrations: find the **one system that should be the root** (the single source of truth for the domain the integration touches), treat every other surface as a **reflection** of it, and put **one automation layer** in the middle keeping the reflections in sync. Resist wiring every tool to every other tool directly -- that's a mesh, and it's what "redundant automation tools, not yet explained" usually turns into.

Within that structure, AI plays two genuinely different roles -- keep them conceptually separate when explaining the plan:
- **AI-as-agent**: embedded inside a workflow in the automation layer, doing a production job unattended. Part of the hub.
- **AI-as-architect**: a human using AI conversationally to reason about and construct those workflows. Sits outside the hub, used only while building/revising.

## Step 3: Check native-first before proposing any build

Before designing custom infrastructure for a piece of this, check what the tools already in place do out of the box -- persistent per-channel memory, built-in retrieval over connected documents, native escalation/follow-up behavior. A full custom layer frequently turns out to be reinventing a feature the platform already shipped. What survives this check is usually smaller and more concrete than the original ambition -- that's a sign the check worked, not that the plan got weaker.

## Step 4: Match interface to person, not one policy for everyone

Don't standardize on one tool for every person. Assign by actual role and technical comfort:
- Whoever does the heaviest architecture/build work → a coding-agent interface (structured config generation is more reliable there).
- Whoever does day-to-day tweaks but isn't a developer → a chat-based agent interface with the same underlying power, lower friction.
- Everyone else → their existing tools (chat, drive), unchanged. **If someone has to open the AI tool just to use an automation day to day, the automation isn't fully wired yet** -- that's a signal to fix the wiring, not a normal steady state.
- Personal/individual AI use by anyone → disconnected from this architecture entirely, not worth standardizing.

## Step 5: Sequence around the one blocking dependency

Identify the single unknown the whole architecture actually depends on (usually: does the root system expose an API or webhooks n8n/whatever hub can listen to). Don't keep designing past it -- resolving that one check unblocks everything else, and design work done before it's resolved risks being thrown away.

## Step 6: Phase the rollout around proof, not proposal

- **Phase 0 (no real access needed yet):** stand up a throwaway/test instance of the automation layer, wire a test AI connection to it, and prove the pattern end-to-end with fake data (simulate the missing integration with a fake webhook payload, for instance). This de-risks the technical approach before any real access exists.
- **Phase 1:** resolve the blocking dependency the moment access exists -- this is usually a five-minute check once you're actually in the system.
- **Phase 2:** ask whoever's closest to the pain ("what's the single most annoying manual task right now") and build *that* as the first real automation -- chosen for being real, not for being impressive. This is the proof that later justifies everything else.
- **Later phases:** loop in the existing agent-builder (if there is one) on that first automation, extend to a second use case incorporating their input, and only then evaluate consolidating/cutting redundant tools -- don't propose a cutover before showing working proof.

## Step 7: Adoption discipline

- Frame any change to an existing person's job as *"a faster way to do what you already do,"* never as a replacement -- especially to whoever already owns this work informally.
- Hold off pitching a broader capability (e.g. "a faster way to build agents generally") until there's a real, working demo and a read on how the team actually operates. Landing it too early reads as presumptuous rather than useful.

## Output shape

Three short documents, not one sprawling one:
1. **Situation summary** -- current state, roles, mandate, open items. The living status doc everything else points back to.
2. **Architecture** -- the hub-and-spoke decision, interface assignments, the native-vs-build check's outcome.
3. **Rollout strategy** -- concrete phased actions, anchored to a real start date, not abstract stage names.

Keep a running log of decisions and setup steps as they happen (commit-as-you-go, not written up after the fact) -- this is what turns one engagement into a reusable methodology for the next one.

## Worked example this was generalized from

A four-person AI startup ("the Hive") running Slack, Google Drive, GlassFrog (Holacracy org management), and two redundant automation tools (n8n and Make). The resolved architecture: GlassFrog as root, Slack/Drive as reflections, n8n as the hub, Claude sitting on top for reasoning/construction rather than as a fifth spoke. The blocking dependency was whether GlassFrog exposed webhooks/an API n8n could listen to. The rollout: a throwaway n8n instance + simulated GlassFrog webhook first (zero real access needed), then real GlassFrog access and the API check, then one real automation chosen by asking the team what was most annoying, only then a conversation about consolidating Make into n8n.
