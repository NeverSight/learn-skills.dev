---
name: diagnostics
description: "Verify setup and troubleshoot the Personize stack — memory, governance, pipelines, and workspaces. Two modes: VERIFY (proactive, after setup) and FIX (reactive, when something breaks). Use this skill whenever the user says something isn't working, gets errors, sees empty recall results, has bad extraction quality, hits rate limits (429), or wants to verify their setup. Also trigger when they mention debugging Personize, testing their integration, health checks, smoke tests, 'why is recall returning nothing', 'my pipeline is failing', or 'guidelines aren't showing up'. This is the go-to skill for anything broken or needing verification."
license: Apache-2.0
compatibility: "Requires @personize/sdk or Personize MCP server and a Personize API key (sk_live_...)"
metadata: {"author": "personize-ai", "version": "1.0", "homepage": "https://personize.ai", "openclaw": {"emoji": "🔍", "requires": {"env": ["PERSONIZE_SECRET_KEY"]}}}
---

# Skill: Diagnostics

Verify setup and troubleshoot the Personize stack. Two modes:

- **VERIFY** — Proactive. Run after setting up memory, governance, pipelines, or workspaces to confirm they work.
- **FIX** — Reactive. Jump to the action that matches the symptom when something breaks.

---

## When to Use This Skill

**Verify mode:**
- Just finished memorizing data and want to confirm it's stored and recallable
- Just set up guidelines and want to confirm agents can see them
- Just wired a pipeline and want to run one record end-to-end
- Just set up a shared workspace and want to confirm agents can read/write
- Want to run a periodic health check

**Fix mode:**
- Recall returns irrelevant, empty, or noisy results
- Memorized data isn't being extracted correctly
- Guidelines aren't reaching agents or return wrong content
- Getting 429 rate limit errors or partial batch syncs
- Trigger.dev or n8n workflows are failing
- Shared workspace is going stale or agents aren't contributing

## When NOT to Use This Skill

- Need to store data → use **entity-memory**
- Need to create guidelines → use **governance**
- Need to build a pipeline → use **code-pipelines** or **no-code-pipelines**
- Need to understand the architecture → use **solution-architect**

---

## Works With Both SDK and MCP

| Interface | How it works | Best for |
|---|---|---|
| **SDK** (`@personize/sdk`) | Run verification scripts locally | Developers, CI/CD |
| **MCP** (Model Context Protocol) | Use `memory_recall_pro`, `ai_smart_guidelines` tools interactively | Claude Desktop, ChatGPT, Cursor |

---

## Quick Smoke Test

If the developer isn't sure what's wrong or just wants to verify everything works, run this:

```typescript
import { Personize } from '@personize/sdk';
const client = new Personize({ secretKey: process.env.PERSONIZE_SECRET_KEY! });

// 1. Auth — can we connect?
try {
  const me = await client.me();
  console.log(`✅ Auth: ${me.data.organization.name} (${me.data.plan.name})`);
} catch (e) {
  console.log('❌ Auth failed:', e.message);
  console.log('   → Check PERSONIZE_SECRET_KEY');
}

// 2. Memory — can we store and retrieve?
try {
  await client.memory.memorize({
    email: 'diagnostics-test@example.com',
    content: 'Test record for diagnostics. This person works at Acme Corp as a VP of Engineering.',
    enhanced: true,
  });
  const recall = await client.memory.recall({
    query: 'Who works at Acme Corp?',
    email: 'diagnostics-test@example.com',
  });
  console.log(`✅ Memory: ${recall.data.memories.length > 0 ? 'stored and recallable' : '⚠️ stored but not yet recallable (indexing may take 1-2 min)'}`);
} catch (e) {
  console.log('❌ Memory failed:', e.message);
  if (e.message.includes('429')) console.log('   → Rate limited. See FIX: RATE-LIMITS.');
}

// 3. Governance — can we fetch guidelines?
try {
  const guidelines = await client.ai.smartGuidelines({ message: 'test verification' });
  console.log(`✅ Governance: ${guidelines.data.compiledContext ? 'responding' : '⚠️ no guidelines set up yet'}`);
} catch (e) {
  console.log('❌ Guidelines failed:', e.message);
}

// 4. Digest — can we compile context?
try {
  const digest = await client.memory.smartDigest({
    email: 'diagnostics-test@example.com',
    include_properties: true,
    include_memories: true,
  });
  console.log(`✅ Digest: ${digest.data.compiledContext ? 'compiling context' : '⚠️ empty'}`);
} catch (e) {
  console.log('❌ Digest failed:', e.message);
}
```

### MCP equivalent

```
1. Call memory_store_pro with content "Test record. Works at Acme Corp as VP Engineering." and email "diagnostics-test@example.com"
2. Call memory_recall_pro with query "Who works at Acme Corp?" and email "diagnostics-test@example.com"
3. Call ai_smart_guidelines with message "test verification"
4. Confirm each returns data
```

Based on results, jump to the appropriate VERIFY or FIX action below.

---

## VERIFY Actions

Use after setting up a capability to prove it works.

| Action | When to Use | Reference |
|---|---|---|
| **VERIFY-MEMORY** | After memorizing data — confirm it's stored and recallable | `reference/verify-memory.md` |
| **VERIFY-GOVERNANCE** | After setting up guidelines — confirm agents can see them | `reference/verify-governance.md` |
| **VERIFY-PIPELINE** | After wiring a pipeline — run one record end-to-end | `reference/verify-pipeline.md` |
| **VERIFY-WORKSPACE** | After setting up a shared workspace — confirm agents can read/write | `reference/verify-workspace.md` |
| **HEALTH-CHECK** | Ongoing — diagnose quality, performance, and coverage issues | `reference/health-check.md` |

---

## FIX Actions

Use when something is broken. Jump to the action that matches the symptom.

| Action | When to Use | Reference |
|---|---|---|
| **BAD-RECALL** | Recall returns irrelevant, empty, or noisy results | `reference/bad-recall.md` |
| **BAD-EXTRACTION** | Memorized data isn't being extracted correctly | `reference/bad-extraction.md` |
| **GOVERNANCE-MISS** | Guidelines aren't reaching agents or return wrong content | `reference/governance-miss.md` |
| **RATE-LIMITS** | Getting 429 errors or partial batch syncs | `reference/rate-limits.md` |
| **PIPELINE-FAILURE** | Trigger.dev/n8n workflows failing or producing bad output | `reference/pipeline-failure.md` |
| **WORKSPACE-STALE** | Agents not contributing or workspace going stale | `reference/workspace-stale.md` |

---

## Constraints

> Keywords follow [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119): **MUST** = non-negotiable, **SHOULD** = strong default (override with stated reasoning), **MAY** = agent discretion.

1. **MUST** run the smoke test or appropriate verify action after every setup — because untested setups create false confidence and delayed failures.
2. **MUST** run diagnostic steps before suggesting fixes — because guessing wastes time and can introduce new problems.
3. **MUST** use real queries that match the developer's actual use case, not generic test strings — because verification with irrelevant queries can pass while real queries fail.
4. **SHOULD** show the developer the actual API response, not just pass/fail — because seeing the data builds understanding and catches quality issues.
5. **SHOULD** rank root causes by likelihood and check the most likely first — because systematic diagnosis is faster than shotgun debugging.
6. **SHOULD** verify the fix worked by re-running the failing operation — because a fix that doesn't resolve the symptom isn't a fix.
7. **SHOULD** clean up test data after verification — because leftover test records pollute memory and confuse downstream agents.
