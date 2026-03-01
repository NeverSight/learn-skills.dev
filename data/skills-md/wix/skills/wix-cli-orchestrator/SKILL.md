---
name: wix-cli-orchestrator
description: "BLOCKING REQUIREMENT - When user requests to add/build/create/implement ANY feature or component for a Wix CLI app, you MUST invoke this skill IMMEDIATELY as your absolute FIRST action - when exploring, reading files, BEFORE launching any agents - make sure this skill is loaded. Trigger on add, build, create, I want, implement, help me where X is any feature/component. Non-negotiable - invoke immediately upon recognizing a Wix feature build request."
compatibility: Requires Wix CLI development environment.
---

# Wix CLI Orchestrator

Helps select the appropriate Wix CLI extension type based on use case and requirements.

## ⚠️ MANDATORY WORKFLOW CHECKLIST ⚠️

**Before reporting completion to the user, ALL boxes MUST be checked:**

- [ ] **Step 1:** Determined extension type(s) needed
  - [ ] Asked clarifying questions if requirements were unclear
  - [ ] Checked for implicit Data Collection need — unless user provided a collection ID directly (see [Data Collection Inference](#data-collection-inference))
  - [ ] Obtained app namespace if Data Collection extension is being created
  - [ ] Determined full scoped collection IDs if Data Collection extension is being created (see [Collection ID Coordination](#collection-id-coordination))
  - [ ] Explained recommendation with reasoning
- [ ] **Step 2:** Checked references, spawned discovery if needed
  - [ ] Checked relevant reference files for required APIs
  - [ ] Spawned discovery only if API not found in references
  - [ ] Skip if all APIs are in reference files or no external APIs needed
- [ ] **Step 3:** Waited for discovery sub-agent to complete (if spawned)
  - [ ] Received SDK methods with imports
- [ ] **Step 4:** Spawned implementation sub-agent(s) with skill context
  - [ ] Included user requirements in prompt
  - [ ] Included SDK context from discovery (if any)
  - [ ] Instructed sub-agent to invoke `wds-docs` skill FIRST when using @wix/design-system (for correct imports, especially icons)
- [ ] **Step 5:** Waited for implementation sub-agent(s) to complete
  - [ ] All files created
  - [ ] Extension registered in extensions.ts
- [ ] **Step 6:** Invoked `wix-cli-app-validation` skill
- [ ] **Step 7:** Validation passed
  - [ ] Dependencies installed
  - [ ] TypeScript compiled
  - [ ] Build succeeded
  - [ ] Preview deployed
- [ ] **Step 8:** Collected and presented ALL manual action items to user
  - [ ] Reviewed output from every sub-agent for manual steps
  - [ ] Aggregated into a single actionable list at the end of the conversation

**🛑 STOP:** If any box is unchecked, do NOT proceed to the next step.

---

## Your Role

You are a **decision-maker and orchestrator**, not an implementer. **Decide → Check References → Discovery (if needed) → Implementation Sub-Agent(s) → Validation → Surface Manual Actions.** Ask clarifying questions if unclear; recommend extension type; check reference files first, spawn discovery only for missing SDK methods; spawn implementation sub-agents; run validation; aggregate and present all manual action items at the end.

---

## ❌ ANTI-PATTERNS (DO NOT DO)

| ❌ WRONG                                    | ✅ CORRECT                                     |
| ------------------------------------------- | ---------------------------------------------- |
| Writing implementation code yourself        | Spawning a sub-agent to implement              |
| Invoking implementation skills directly     | Spawning sub-agent with skill context          |
| Discovering extension SDK (dashboard, etc.) | Extension SDK is in skill reference files      |
| Spawning discovery without checking refs    | Check skill refs first                         |
| Reporting done without validation           | Always run `wix-cli-app-validation` at the end |
| Reading/writing files after invoking skills | Let sub-agents handle ALL file operations      |
| Letting manual action items get buried      | Aggregate all manual steps at the very end     |

**CRITICAL:** After this planner skill loads, you should ONLY:

- Spawn sub-agents (for discovery and implementation)
- Invoke `wix-cli-app-validation` skill at the end

You should NEVER: Read, Write, Edit files for implementation yourself

## Quick Decision Helper

Answer these questions to find the right extension:

1. **What are you trying to build?**
   - Admin interface → Dashboard Extensions
   - Backend logic → Backend Extensions
   - Data storage / CMS collections → Data Collection
   - Site component → Site Extensions (app projects only)

2. **Who will see it?**
   - Admin users only → Dashboard Extensions
   - Site visitors → Site Extensions
   - Server-side only → Backend Extensions

3. **Where will it appear?**
   - Dashboard sidebar/page → Dashboard Page or Modal
   - Existing Wix app dashboard → Dashboard Plugin
   - Anywhere on site → Site Widget
   - Wix business solution page → Site Plugin
   - During business flow → Service Plugin
   - After event occurs → Event Extension

## Decision Flow (Not sure?)

- **Admin:** Need full-page UI? → Dashboard Page. Need popup/form? → Dashboard Modal. Extending Wix app dashboard? → Dashboard Plugin. **Modal constraint:** Dashboard Pages cannot use `<Modal />`; use a separate Dashboard Modal extension and `dashboard.openModal()`.
- **Backend:** During business flow (checkout/shipping/tax)? → Service Plugin. After event (webhooks/sync)? → Event Extension. Custom HTTP endpoints? → Backend Endpoints. Need CMS collections for app data? → Data Collection.
- **Site:** User places anywhere? → Site Widget. Fixed slot on Wix app page? → Site Plugin. Scripts/analytics only? → Embedded Script.

### Data Collection Inference

**CRITICAL:** Data collections are often needed implicitly — don't wait for the user to explicitly say "create a CMS collection." Infer the need automatically.

**Skip this section if the user provides a collection ID directly** (e.g., an existing site-level collection). In that case, use the provided ID as-is — no Data Collection extension or namespace scoping needed.

**Always include a Data Collection extension when ANY of these are true:**

| Indicator | Example |
| --- | --- |
| User mentions saving/storing/persisting app-specific data | "save the fee amount", "store product recommendations" |
| A dashboard page will **manage** (CRUD) domain entities | "dashboard to manage fees", "admin page to edit rules" |
| A service plugin reads app-configured data at runtime | "fetch fee rules at checkout", "look up shipping rates" |
| User mentions "dedicated database/collection" | "save in a dedicated database collection" |
| Multiple extensions reference the same custom data | Dashboard manages fees + service plugin reads fees |

**Why this matters:** Without the Data Collection extension, the collection won't be created when the app is installed, the Wix Data APIs may not work (code editor not enabled), and collection IDs won't be properly scoped to the app namespace.

**If data collection is inferred, follow the [App Namespace Requirement](#step-1-ask-clarifying-questions-if-needed) to obtain the namespace before proceeding.**

## Quick Reference Table

| Extension Type        | Category  | Visibility  | Use When                      | Skill                     |
| --------------------- | --------- | ----------- | ----------------------------- | ------------------------- |
| Dashboard Page        | Dashboard | Admin only  | Full admin pages              | `wix-cli-dashboard-page`   |
| Dashboard Modal       | Dashboard | Admin only  | Popup dialogs                 | `wix-cli-dashboard-modal` |
| Dashboard Plugin      | Dashboard | Admin only  | Extend Wix app dashboards     | (none yet)                |
| Dashboard Menu Plugin | Dashboard | Admin only  | Add menu items                | (none yet)                |
| Service Plugin        | Backend   | Server-side | Customize business flows      | `wix-cli-service-plugin`   |
| Event Extension       | Backend   | Server-side | React to events               | `wix-cli-backend-event`   |
| Backend Endpoints     | Backend   | API         | Custom HTTP handlers          | `wix-cli-backend-api`     |
| Data Collection       | Backend   | Data        | CMS collections for app data  | `wix-cli-data-collection` |
| Site Widget           | Site      | Public      | Standalone widgets            | `wix-cli-site-widget`     |
| Site Plugin           | Site      | Public      | Extend Wix business solutions | `wix-cli-site-plugin`     |
| Embedded Script       | Site      | Public      | Inject scripts/analytics      | `wix-cli-embedded-script` |

**Key constraint:** Dashboard Page cannot use `<Modal />`; use a separate Dashboard Modal and `dashboard.openModal()`.

## Extension Comparison

| Site Widget vs Site Plugin | Dashboard Page vs Modal | Service Plugin vs Event |
| -------------------------- | ----------------------- | ----------------------- |
| Widget: user places anywhere. Plugin: fixed slot in Wix app. | Page: full page. Modal: overlay; use for popups. | Service: during flow. Event: after event. |

## Decision & Handoff Workflow

Follow the checklist; steps below add detail.

### Step 1: Ask Clarifying Questions (if needed)

Only ask for configuration values when **absolutely necessary** for the implementation to proceed — i.e., the sub-agent literally cannot generate working code without it. If a value can be configured later or added as a manual step, don't block on it.

**App Namespace Requirement:**
When creating a Data Collection, you MUST ask the user for their app namespace from Wix Dev Center. This is a required parameter that must be obtained from the user's Dev Center dashboard and cannot be recommended or guessed.

**Instructions to give the user:**

**If you don't have an app namespace yet:**
1. Go to [Wix Dev Center](https://manage.wix.com/studio/custom-apps/)
2. Select your app
3. In the left menu, select **Develop > Extensions**
4. Click **+ Create Extension** and find the **Data Collections** extension
5. Click **+ Create**
6. You will be prompted to create an app namespace - follow the prompts to set it up

**If you already have an app namespace:**
1. Go to [Wix Dev Center](https://manage.wix.com/studio/custom-apps/)
2. Open your app dashboard
3. Click the three dots (...) menu button in the top-right corner (next to "Test App" button)
4. Select "View ID & keys" from the dropdown menu
5. In the modal that opens, scroll to the bottom to find the "Namespace" field
6. Copy the Namespace value

If unclear on approach (placement, visibility, configuration, integration), ask clarifying questions. If the answer could change the extension type, wait for the response before proceeding. Otherwise, proceed with the best-fit extension type.

### Collection ID Coordination

**Applies ONLY when a Data Collection extension is being created.** If the user provides a collection ID directly, use it as-is — no namespace scoping, no Data Collection extension needed.

When a Data Collection is created alongside other extensions that reference the same collections:

1. **Get the app namespace** (see App Namespace Requirement above)
2. **Determine the `idSuffix`** for each collection (the `wix-cli-data-collection` skill documents the full ID format)
3. **Pass the full scoped collection ID** (`<app-namespace>/<idSuffix>`) to every other sub-agent (dashboard page, service plugin, etc.) so they use it in all Wix Data API calls

### Step 2: Make Your Recommendation

Use Quick Reference Table and decision content above. State extension type and brief reasoning (placement, functionality, integration).

### Step 3: Check References, Then Discover (if needed)

**Workflow: References first, search only for gaps.**

1. **Identify required APIs** from user requirements
2. **Check relevant reference files:**
   - Backend events → `wix-cli-backend-event/references/COMMON-EVENTS.md`
   - Wix Data → `wix-cli-dashboard-page/references/WIX_DATA.md`
   - Dashboard SDK → `wix-cli-dashboard-page/references/DASHBOARD_API.md`
   - Service Plugin SPIs → `wix-cli-service-plugin/references/*.md`
3. **Verify the specific method/event exists** in references
4. **ONLY spawn discovery if NOT found** in reference files

**Platform APIs (never discover - in references):**
- Wix Data, Dashboard SDK, Event SDK (common events), Service Plugin SPIs

**Vertical APIs (discover if needed):**
- Wix Stores, Wix Bookings, Wix Members, Wix Pricing Plans, third-party integrations

**Decision table:**

| User Requirement                     | Check References / Discovery Needed? | Reason / Reference File                             |
| ------------------------------------ | ------------------------------------ | --------------------------------------------------- |
| "Display store products"             | ✅ YES (Spawn discovery)             | Wix Stores API not in reference files               |
| "Show booking calendar"              | ✅ YES (Spawn discovery)             | Wix Bookings API not in reference files             |
| "Send emails to users"               | ✅ YES (Spawn discovery)             | Wix Triggered Emails not in reference files         |
| "Get member info"                    | ✅ YES (Spawn discovery)             | Wix Members API not in reference files              |
| "Listen for cart events"             | Check `COMMON-EVENTS.md`             | Spawn discovery only if event missing in reference  |
| "Store data in collection"           | WIX_DATA.md ✅ Found                 | ❌ Skip discovery (covered by `WIX_DATA.md`)        |
| "Create CMS collections for my app"  | Reference: `wix-cli-data-collection` | ❌ Skip discovery (covered by dedicated skill)       |
| "Show dashboard toast"               | DASHBOARD_API.md ✅ Found            | ❌ Skip discovery                                   |
| "Show toast / navigate"              | DASHBOARD_API.md ✅ Found            | ❌ Skip discovery                                   |
| "UI only (forms, inputs)"            | N/A (no external API)                | ❌ Skip discovery                                   |
| "Settings page with form inputs"     | N/A (UI only, no external API)       | ❌ Skip discovery                                   |
| "Dashboard page with local state"    | N/A (no external API)                | ❌ Skip discovery                                   |

**MCP Tools the sub-agent should use:**

- `mcp__wix-mcp-remote__SearchWixSDKDocumentation` - SDK methods and APIs (**Always use maxResults: 5**)
- `mcp__wix-mcp-remote__ReadFullDocsArticle` - Full documentation when needed (only if search results need more detail)

**Discovery sub-agent prompt template:**

```
Discover SDK methods for [SPECIFIC API/EVENT NOT IN REFERENCE FILES].

Search MCP documentation (use maxResults: 5):
- Search SDK documentation for [SPECIFIC API] with maxResults: 5
- Only use ReadFullDocsArticle if search results need more context

Return ONLY a concise summary in this format:

## SDK Methods & Interfaces

| Name                      | Type   | TypeScript Type                              | Description       |
| ------------------------- | ------ | -------------------------------------------- | ----------------- |
| `moduleName.methodName()` | Method | `(params: ParamType) => Promise<ReturnType>` | Brief description |

**Import:** `import { methodName } from '@wix/sdk-module';`

Include any gotchas or constraints discovered.

## Manual Action Items
List any manual steps the user must perform (e.g., configure dashboard settings, enable permissions). Write "None" if there are no manual steps.

**Permissions:** If Wix app permissions are required, list them here using the SCOPE ID format (not human-readable names). Examples:
- `@wix/data` read operations (query, get) require "SCOPE.DC-DATA.READ"
- `@wix/data` write operations (insert, update, remove) require "SCOPE.DC-DATA.WRITE"
- Embedded scripts require "SCOPE.DC-APPS.MANAGE-EMBEDDED-SCRIPTS"
- Check the Wix SDK documentation "Method Permissions Scopes IDs" section for the exact scope ID.
- IMPORTANT: Use scope IDs like "SCOPE.DC-DATA.READ", NOT human-readable names like "Read Data Items".
```

**If discovery is spawned, wait for it to complete before proceeding to Step 4.**

### Step 4: Spawn Implementation Sub-Agent(s)

⚠️ **BLOCKING REQUIREMENT** ⚠️

You MUST spawn sub-agent(s) for implementation. Do NOT invoke implementation skills directly. Do NOT write code yourself.

**Spawn an implementation sub-agent with the skill context:**

The sub-agent prompt should include:

1. The skill to load (e.g., `wix-cli-dashboard-page`)
2. The user's requirements
3. The SDK context from the discovery sub-agent
4. Instruction to invoke the `wds-docs` skill only when needed (e.g. when looking up WDS component props or examples)

**Implementation sub-agent prompt MUST include:**

1. ✅ The skill to load (full path or name)
2. ✅ The user's original requirements (copy verbatim)
3. ✅ SDK methods discovered (with imports and types) — **only if discovery was performed**
4. ✅ Instruction to invoke `wds-docs` skill FIRST when using @wix/design-system (critical for correct imports, especially icons)
5. ✅ Any constraints or gotchas discovered
6. ✅ Collection Context with full scoped collection IDs — **only if Data Collection is being created**
7. ✅ Instruction to return manual action items (see below)

**Implementation sub-agent prompt template:**

```
Load and follow the skill: wix-cli-[skill-name]

User Requirements:
[EXACT user request - copy verbatim]

[ONLY IF DISCOVERY WAS PERFORMED:]
SDK Context:
[Methods with imports from discovery]

Constraints:
[Any gotchas or limitations from discovery]

⚠️ MANDATORY when using WDS: Invoke the wds-docs skill FIRST to get correct imports (icons are from @wix/wix-ui-icons-common, NOT @wix/design-system/icons).

⚠️ MANDATORY when using Data Collections: Use EXACT collection ID from `idSuffix` (case-sensitive). Example: If `idSuffix` is "product-recommendations", use "<app-namespace>/product-recommendations" NOT "productRecommendations".

⚠️ MANDATORY: At the END of your response, include a section titled "## Manual Action Items" listing ANY steps the user must perform manually (e.g., configuring settings in the Wix dashboard, enabling permissions, setting up external services, etc.). If there are no manual steps, write "None". This section MUST always be present in your final response.

Implement this extension following the skill guidelines.
```

**PARALLEL EXECUTION:** When multiple independent extensions are needed, spawn ALL sub-agents in parallel:

| Extension Combination            | Parallel? | Reason                              |
| -------------------------------- | --------- | ----------------------------------- |
| Dashboard Page + Site Widget     | ✅ YES    | Independent UI contexts             |
| Dashboard Page + Dashboard Modal | ✅ YES    | Modal code is independent from page |
| Dashboard Page + Backend API     | ✅ YES    | Frontend vs backend                 |
| Site Widget + Embedded Script    | ✅ YES    | Different rendering contexts        |
| Service Plugin + Event Extension | ✅ YES    | Independent backend handlers        |
| Data Collection + Dashboard Page | ✅ YES    | Data schema vs UI                   |
| Data Collection + Backend API    | ✅ YES    | Data schema vs HTTP handlers        |
| Data Collection + Site Widget    | ✅ YES    | Data schema vs site UI              |

**Pre-spawn coordination required (then parallel is fine):**

- When a Data Collection + other extensions reference the same collections: determine the full scoped collection IDs (`<app-namespace>/<idSuffix>`) BEFORE spawning sub-agents, then pass the IDs to all sub-agents and run them in parallel

**Sequential execution required:**

- When one extension imports types/interfaces from another
- When user explicitly says "first X, then Y"

**Extension Type to Skill Mapping:** See [Quick Reference Table](#quick-reference-table) above.

**Wait for sub-agents to complete before proceeding to Step 5.**

### Step 5: Run Validation

⚠️ **BLOCKING REQUIREMENT** ⚠️

After ALL implementation sub-agents complete, you MUST run validation by invoking the `wix-cli-app-validation` skill.

**Do NOT report completion to the user until validation passes.**

If validation fails:

1. Review the errors
2. Spawn a new implementation sub-agent to fix the issues
3. Run validation again
4. Repeat until validation passes

### Step 6: Report Completion

Only after validation passes, provide a **concise summary section** at the top of your response that includes:

**Required format:**

```markdown
## ✅ Implementation Complete

[1-2 sentence description of what was built]

**Extensions Created:**
- [Extension 1 Name] - [Brief purpose]
- [Extension 2 Name] - [Brief purpose]
- [Extension 3 Name] - [Brief purpose]

**Build Status:**
- ✅ Dependencies: [Installed / status message]
- ✅ TypeScript: [No compilation errors / status]
- ✅ Build: [Completed successfully / status]
- ✅/⚠️ Preview: [Running at URL / Failed - reason]

**⚠️ IMPORTANT: [X] manual step(s) required to complete setup** (see "Manual Steps Required" section below)
```

**Critical rules:**
- The summary MUST explicitly state how many manual steps are required
- The summary MUST reference where to find the manual steps ("see Manual Steps Required section below")
- If there are NO manual steps, state: "✅ No manual steps required — you're ready to go!"
- Keep the summary concise (under 200 words)
- Present build status clearly with ✅ or ⚠️ indicators

### Step 7: Surface Manual Action Items

⚠️ **BLOCKING REQUIREMENT** ⚠️

**Sub-agents often report manual steps the user must take (e.g., configure permissions in the Wix dashboard, enable specific features, etc.). These MUST NOT get lost.**

After ALL sub-agents complete, you MUST:

1. **Review every sub-agent's output** for any "Manual Action Items" section or any mention of steps the user needs to perform manually
2. **Aggregate ALL manual action items** from every sub-agent into a single, deduplicated list
3. **Reference them in the summary section** (Step 6) by stating how many manual steps exist
4. **Present them prominently** at the very end of your final message to the user, under a clear heading

**Complete workflow for manual steps:**

1. **In the summary (Step 6):** Include the line `**⚠️ IMPORTANT: [X] manual step(s) required to complete setup** (see "Manual Steps Required" section below)`
2. **At the end of your response:** Present the full detailed manual steps section

**Format for the manual steps section:**

```markdown
## 🔧 Manual Steps Required

The following actions need to be done manually by you:

### 1. [Action Category/Title]
[Detailed description with specific instructions]
- Step-by-step if needed
- Include where to find things in the UI
- Provide example values if helpful

### 2. [Action Category/Title]
[Detailed description]

### 3. [Action Category/Title]
[Detailed description]

[Continue for all manual steps...]
```

**If no manual steps are needed:**
```markdown
## 🔧 Manual Steps Required

No manual steps required — you're all set! Your implementation is complete and ready to use.
```

**Rules:**
- The summary section (Step 6) MUST reference the manual steps
- This detailed manual steps section MUST be the **last thing** in your final response to the user
- Even if you think the items were mentioned earlier in the conversation, **repeat them here** — assume the user only reads the final summary
- Include full context for each item (e.g., "In the Wix dashboard, go to Settings > Permissions and enable X" rather than just "enable X")
- Group related steps together under category headings for clarity
- If a sub-agent didn't include a "Manual Action Items" section, review its full output for any implicit manual steps (phrases like "you'll need to", "make sure to", "don't forget to", "manually", "go to the dashboard", etc.)
- Number the main categories/sections (1, 2, 3...) for easy reference

**Summary:** Discovery = business domain SDK only (Stores, Bookings, etc.) — skip for extension SDK and data collections. Implementation = load extension skill; invoke `wds-docs` FIRST when using WDS (for correct imports). Validation = `wix-cli-app-validation`. Manual actions = always aggregated and surfaced at the end.

## Cost Optimization

- **Check references first** — read relevant reference files before spawning discovery
- **Skip discovery** when all required APIs are in reference files
- **maxResults: 5** for all MCP SDK searches
- **ReadFullDocsArticle** only when search results need more context
- **Implementation prompts:** include only relevant SDK context from discovery (if performed)
- **Parallelize** independent sub-agents when possible
- **Invoke wds-docs** first when using WDS (prevents import errors)
- **Targets:** discovery output 500-1000 tokens; implementation prompt minimal; each search under 2000-3000 tokens

## Documentation

For detailed documentation on all extension types, see [references/DOCUMENTATION.md](references/DOCUMENTATION.md).
