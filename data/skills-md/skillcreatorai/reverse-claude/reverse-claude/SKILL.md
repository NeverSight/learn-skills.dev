---
name: reverse-claude
description: >
  The reverse-engineering manual for Claude Code. Encodes all seven runtime systems (permissions,
  plugins, agents, compaction, self-configuration, query engine orchestration, message pipeline
  and cost tracking) as actionable patterns with 40+ named patterns extracted from ~28,000 lines
  of production source. Point this skill at Claude Code itself to understand, configure, and
  extend it.
whenToUse: >
  Use when: (1) configuring Claude Code — permissions, hooks, settings, CLAUDE.md rules,
  (2) building systems like Claude Code — command safety, plugin lifecycle, agent orchestration,
  context compaction, retry strategies, feature flags, (3) understanding how Claude Code works
  internally, (4) reviewing code that touches any of these patterns. This is the skill you
  point at Claude Code itself.
userInvocable: true
---

# Reverse-Claude: The Self-Configuring Runtime Intelligence Skill

This skill is Claude Code's mirror. It encodes how Claude Code works internally -- its permission cascade, plugin system, agent orchestrator, context compactor, and configuration surface -- extracted from ~13,000 lines of production source. **Point this skill at Claude Code itself to understand, configure, and extend it.**

## When to Use

- **Configuring Claude Code** — set up permissions, hooks, CLAUDE.md rules, settings
- **Building Claude Code-like systems** — command safety, plugin lifecycle, agent orchestration
- **Managing LLM context** — compaction hierarchies, retry strategies, circuit breakers
- **Understanding internals** — how permissions cascade, how agents spawn, how compaction works
- **Extending Claude Code** — writing plugins, skills, hooks, MCP integrations

---

## Module 1: Permissioned Invocation & Runtime Safety

### Invariant

**No command executes without passing through a multi-layered permission cascade that enforces deny > ask > allow > read-only > passthrough priority, with defense-in-depth against shell injection, env-var bypass, wrapper bypass, and parser differentials.**

### Pattern 1.1: Permission Decision Cascade

The master permission function implements a strict priority chain. Every command goes through this cascade:

```
1. AST parse (tree-sitter) -> reject if too complex
2. Sandbox auto-allow check -> still respects deny/ask rules
3. Exact match deny/ask/allow rules
4. Classifier-based deny/ask (LLM classifier)
5. Command operator permissions (pipes, redirects)
6. Split into subcommands -> per-subcommand check:
   a. Exact match deny -> DENY
   b. Exact match ask -> ASK
   c. Prefix/wildcard deny -> DENY
   d. Prefix/wildcard ask -> ASK
   e. Path constraints -> ASK/DENY
   f. Exact match allow -> ALLOW
   g. Prefix/wildcard allow -> ALLOW
   h. Mode-specific (auto mode) -> ALLOW
   i. Read-only check -> ALLOW
   j. Passthrough -> prompt user
7. Command injection check (regex battery)
8. Classifier async auto-approve (race the user)
```

**Key rule: deny always wins.** Even in auto-allow modes, deny rules are checked on both the full command AND each subcommand.

**Pseudocode:**

```
function checkPermission(input, context):
  // 1. Exact match first (deny/ask/allow)
  exact = checkExactMatch(input, rules)
  if exact.behavior in ['deny', 'ask']: return exact

  // 2. Prefix/wildcard deny/ask (BEFORE allow - prevents bypass)
  {denyRules, askRules, allowRules} = matchRulesForInput(input)
  if denyRules[0]: return deny
  if askRules[0]: return ask

  // 3. Path constraints (after deny so explicit rules take precedence)
  pathResult = checkPathConstraints(input, cwd)
  if pathResult != passthrough: return pathResult

  // 4. Allow rules (exact, then prefix/wildcard)
  if exact.behavior == 'allow': return exact
  if allowRules[0]: return allow

  // 5. Mode-specific permission
  modeResult = checkPermissionMode(input)
  if modeResult != passthrough: return modeResult

  // 6. Read-only auto-allow
  if isReadOnly(input): return allow

  // 7. Passthrough -> prompt user with suggestions
  return {behavior: 'passthrough', suggestions: suggestRule(command)}
```

### Pattern 1.2: Asymmetric Env-Var Stripping

This is the most security-critical pattern. Allow and deny rules strip env vars differently:

- **Allow rules** strip ONLY safe env vars (build targets, logging, locale). `DOCKER_HOST=evil docker ps` does NOT match `allow(docker ps:*)`.
- **Deny/ask rules** strip ALL env vars via fixed-point iteration. `FOO=bar denied_cmd` still matches `deny(denied_cmd)`.

```
SAFE_ENV_VARS = {GOOS, GOARCH, NODE_ENV, RUST_LOG, LANG, TERM, NO_COLOR, ...}
NEVER_SAFE    = {PATH, LD_PRELOAD, DYLD_*, PYTHONPATH, NODE_PATH, HOME, SHELL, BASH_ENV, ...}

function stripForAllowRules(cmd):
  return stripOnlySafeEnvVars(cmd)  // Conservative

function stripForDenyRules(cmd):
  // Fixed-point iteration - strips interleaved wrappers + env vars
  seen = Set(cmd)
  queue = [cmd]
  while queue not empty:
    current = queue.pop()
    envStripped = stripAllLeadingEnvVars(current)
    wrapperStripped = stripSafeWrappers(current)  // timeout, nice, nohup, etc.
    for variant in [envStripped, wrapperStripped]:
      if variant not in seen: queue.push(variant); seen.add(variant)
  return all variants  // Check deny rules against ALL
```

**Why fixed-point:** Commands like `nohup FOO=bar timeout 5 evil_cmd` require iterative stripping because wrappers and env vars interleave.

### Pattern 1.3: Declarative Flag Validation (Read-Only Safety)

Commands are auto-allowed as "read-only" only if every flag is in a whitelist:

```
type CommandConfig = {
  safeFlags: Record<string, 'none' | 'string' | 'number' | 'char'>
  regex?: RegExp                    // Additional validation pattern
  dangerCallback?: (raw, args) => boolean  // Custom danger check
  respectsDoubleDash?: boolean      // Default: true
}

ALLOWLIST = {
  'git diff': { safeFlags: {'--stat': 'none', '--cached': 'none', ...} },
  'ps':       { safeFlags: {'-e': 'none', ...}, dangerCallback: blockBsdEFlag },
  'date':     { safeFlags: {'-u': 'none', ...}, dangerCallback: blockTimeSet },
}

function isCommandSafe(command):
  parsed = shellQuoteParse(command)
  if hasOperators(parsed): return false    // Pipes/redirects handled upstream
  config = matchAllowlist(parsed.command)
  if not config: return false

  // CRITICAL: Reject ANY token containing $
  // Prevents: git diff "$Z--output=/tmp/pwned" (parser differential)
  // Prevents: rg . "$Z--pre=bash" FILE (RCE via flag injection)
  if anyToken(t => t.contains('$')): return false

  // Reject brace expansion: {a,b} or {1..5}
  if anyToken(t => hasBraceExpansion(t)): return false

  return validateFlags(parsed.args, config.safeFlags)
    && (!config.regex || config.regex.test(command))
    && (!config.dangerCallback || !config.dangerCallback(raw, args))
```

### Pattern 1.4: Compound Command Security Gates

```
MAX_SUBCOMMANDS = 50  // Prevents DoS from exponential splitCommand
RULES:
  1. cd + git blocked      -> malicious dir could have bare repo hooks
  2. Multiple cd blocked   -> requires approval
  3. Any subcommand denied -> whole compound denied
  4. Prefix rules don't match across && boundaries
     (cd:* must NOT match "cd /path && python3 evil.py")
```

### Pattern 1.5: Speculative Classifier (Race the User)

```
// Fire LLM classifier BEFORE permission prompt shows
classifierPromise = startSpeculativeCheck(command)

// Show permission prompt to user
showPrompt(command)

// If classifier returns allow AND user hasn't interacted:
if await classifierPromise == 'allow' && !userHasInteracted():
  autoApprove()  // Dismiss prompt
else:
  discardClassifierResult()  // User is already engaged
```

### Pattern 1.6: Command Semantics (Exit Code Interpretation)

Not all non-zero exit codes are errors. The system overrides default interpretation per-command:

```
COMMAND_EXIT_CODE_OVERRIDES:
  grep:  exit 1 = "no match found" (not an error)
  find:  exit 1 = "partial access denied" (partial success)
  diff:  exit 1 = "files differ" (expected behavior)
  test:  exit 1 = "condition false" (not an error)
```

Without these overrides, the model would treat `grep pattern file` returning nothing as a tool failure and retry or apologize.

### Pattern 1.7: Git Operation Detection & Tracking

```
GIT_OPERATION_PATTERNS:
  commit:      /git\s+commit/
  push:        /git\s+push/
  cherry-pick: /git\s+cherry-pick/
  merge:       /git\s+merge/
  rebase:      /git\s+rebase/
  PR creation: /gh\s+pr\s+create/ or /glab\s+mr\s+create/

function detectAndTrackGitOps(command, exitCode):
  for pattern in GIT_OPERATION_PATTERNS:
    if pattern.test(command) and exitCode == 0:
      otelCounter.increment(pattern.name)
      if pattern.name == "commit":
        kind = command.includes("--amend") ? "amended" : "committed"
        trackCommitKind(kind)
```

**Why this matters:** Analytics, safety checks (e.g., warn before force-push), and session cost attribution all depend on knowing what git operations were performed.

### Edge Cases

- Shell wrappers (`timeout`, `nice`, `nohup`) stripped with precise flag regexes -- previously `[^ \t]+` matched `$(id)` allowing code execution
- `base64` on macOS: `respectsDoubleDash: false` because macOS base64 ignores `--`
- Windows: xargs removed (UNC paths in file contents trigger SMB resolution)
- Git-internal path detection: blocks `mkdir hooks && echo evil > hooks/pre-commit && git status`
- Single quotes: backslash is NOT escape inside single quotes (HackerOne fix)
- `grep` exit 1 is not an error — command semantics override default interpretation
- Git operation tracking fires OTel counters on successful git commands

### Anti-Patterns

- Matching deny rules against only the full command string (bypass via env vars or wrappers)
- Trusting shell-quote parse output without checking for `$` tokens
- Using symmetric stripping for allow and deny rules
- Allowing `sh:*`, `env:*`, `bash:*` as prefix rules (equivalent to allowing everything)
- Treating all non-zero exit codes as errors (grep 1, diff 1, find 1 are valid results)

---

## Module 2: Plugin/Skill Discovery & Lifecycle

### Invariant

**Plugins are always loaded from markdown files via a deterministic pipeline: walk directories -> parse frontmatter -> validate -> hydrate variables -> register as typed commands. State is persisted in a versioned JSON file with idempotent migration. Updates are background-only and never mutate in-memory session state.**

### Pattern 2.1: Filesystem-to-Registry Command Loader

```
function loadPluginCommands():
  if cached: return cache

  for each enabledPlugin:
    markdownFiles = walkDirectory(plugin.commandsPath)
    markdownFiles = dedup(markdownFiles)  // isDuplicatePath prevents double-load

    // SKILL.md takes priority over sibling .md files
    if directory has SKILL.md:
      markdownFiles = [SKILL.md only]

    for file in markdownFiles:
      frontmatter = parseYAMLFrontmatter(file)
      name = buildNamespacedName(file, plugin)  // "pluginName:namespace:commandName"
      command = createCommand(name, file, frontmatter, plugin)
      registry.add(command)

  cache = registry
  return registry

function createCommand(name, file, frontmatter, plugin):
  return {
    type: 'prompt',
    name,
    description: frontmatter.description ?? extractFromMarkdown(content),
    allowedTools: parseFrontmatter(frontmatter['allowed-tools']),
    model: frontmatter.model,
    getPromptForCommand(args, context):
      content = file.content
      if isSkill: content = "Base directory: ${dirname}\n\n" + content
      content = substituteArguments(content, args)
      content = substitutePluginVariables(content, plugin)
      content = substituteUserConfig(content, userConfig)
      content = content.replace('${CLAUDE_SKILL_DIR}', skillDir)
      content = content.replace('${CLAUDE_SESSION_ID}', sessionId)
      content = await executeShellCommandsInPrompt(content)
      return [{type: 'text', text: content}]
  }
```

**Variable substitution chain (order matters):**
1. `${CLAUDE_PLUGIN_ROOT}` -> plugin install path
2. `${user_config.X}` -> user settings (sensitive values -> placeholder)
3. `${CLAUDE_SKILL_DIR}` -> skill's directory
4. `${CLAUDE_SESSION_ID}` -> current session ID
5. Shell commands in prompt -> executed and replaced

### Pattern 2.2: Versioned State File with Idempotent Migration

```
// Schema evolution: V1 (flat map) -> V2 (per-scope arrays)
V1: { version: 1, plugins: Record<PluginId, InstalledPlugin> }
V2: { version: 2, plugins: Record<PluginId, PluginInstallationEntry[]> }

PluginScope = 'managed' | 'user' | 'project' | 'local'

function migrateToSingleFile():
  if migrationCompleted: return  // Idempotent guard

  try:
    // Attempt atomic rename first
    renameSync(v2FilePath, mainFilePath)
    migrationCompleted = true; return
  catch ENOENT: pass

  mainData = readFileSync(mainFilePath)
  if mainData.version == 1:
    v2Data = migrateV1ToV2(mainData)  // All V1 entries -> 'user' scope
    writeFileSync(mainFilePath, v2Data)
    cleanupLegacyCache(v2Data)  // Remove non-versioned flat directories

  migrationCompleted = true  // Set even on error to prevent retry
```

**Dual-layer state model:**
- **Disk state**: source of truth, updated by background operations
- **Memory state**: snapshot at startup, never updated by background ops
- **Pending updates**: detected by comparing disk vs memory install paths

### Pattern 2.3: Background Update with Notification Buffer

```
let callback = null
let pendingNotification = null

function onPluginsUpdated(cb):
  callback = cb
  // Deliver buffered notification if update finished before listener mounted
  if pendingNotification?.length > 0:
    cb(pendingNotification)
    pendingNotification = null
  return () => { callback = null }

function autoUpdateInBackground():
  // Fire and forget
  void (async () => {
    marketplaces = getAutoUpdateEnabled()
    await Promise.allSettled(marketplaces.map(refreshMarketplace))  // git pull each
    updated = await updatePlugins(marketplaces)  // Per-plugin, per-scope
    if updated.length > 0:
      if callback: callback(updated)
      else: pendingNotification = updated  // Buffer for late listener
  })()
```

### Pattern 2.4: Error-Isolated Subsystem Loading

```
function initializePlugins():
  {enabled, disabled, errors} = await loadAllPlugins()

  // Each subsystem wrapped individually -- one failure doesn't block others
  try: commands = await getPluginCommands()
  catch e: errors.push({source: 'plugin-commands', error: e})

  try: agents = await loadPluginAgents()
  catch e: errors.push({source: 'plugin-agents', error: e})

  try: await loadPluginHooks()
  catch e: errors.push({source: 'plugin-hooks', error: e})

  // Merge with LSP error preservation (don't clobber existing errors)
  setState(prev => {
    existingLsp = prev.errors.filter(isLspError)
    deduped = existingLsp.filter(e => !newErrors.has(e.key))
    return {...prev, errors: [...deduped, ...errors]}
  })
```

### Pattern 2.5: Imperative Plugin Registry with Settings Toggle

```
REGISTRY = new Map()

function registerBuiltinPlugin(definition):
  REGISTRY.set(definition.name, definition)

function getBuiltinPlugins():
  enabled, disabled = [], []
  for (name, def) of REGISTRY:
    if def.isAvailable && !def.isAvailable(): continue  // Feature gate
    isEnabled = settings.enabledPlugins[id] ?? (def.defaultEnabled ?? true)
    plugin = buildLoadedPlugin(name, def, isEnabled)
    if isEnabled: enabled.push(plugin)
    else: disabled.push(plugin)
  return {enabled, disabled}
```

### Pattern 2.6: MCP Server Lifecycle & Name Contracts

MCP (Model Context Protocol) servers extend Claude Code with external tools. The lifecycle:

```
LIFECYCLE:
  1. Config declares MCP servers (in settings.json or plugin manifest)
  2. On startup, each server connection is initiated (status: pending)
  3. Server connects and registers its tools (status: connected)
  4. Tools are normalized and added to the tool registry
  5. On failure, server marked as failed (tools unavailable)
  6. On session end, all connections closed

NAME NORMALIZATION (critical for permission rules):
  function normalizeMcpName(rawName):
    return rawName
      .replace(/[^a-zA-Z0-9]/g, '_')  // non-alphanumeric -> underscore
      .replace(/_{2,}/g, '_')          // dedupe consecutive underscores
      .replace(/^_|_$/g, '')           // trim edges

PERMISSION RULE FORMAT:
  mcp__serverName           // all tools from this server
  mcp__serverName__toolName // specific tool
  mcp__serverName__*        // wildcard (all tools)
```

**Why name normalization matters:** A server named `my-cool.server` becomes `my_cool_server` in tool names and permission rules. Without normalization, permission rules like `mcp__my-cool.server__*` would silently fail to match.

### Edge Cases

- Symlinks accepted as skill directories
- ENOENT gracefully skipped (skill dir might not exist yet)
- Win32 path normalization: backslash -> forward slash for `CLAUDE_SKILL_DIR`
- `source: 'bundled'` (not `'builtin'`) to stay in analytics pipeline
- Delisted plugin enforcement runs on mount before commands load
- Settings divergence guard: `isPluginInstalled` checks BOTH install file AND settings
- MCP server names normalized: `my-server.v2` becomes `my_server_v2` in tool names
- MCP servers can require OAuth — auth flow handled at connection time
- Pending MCP servers polled every 500ms up to 30s before agent dispatch

### Anti-Patterns

- Loading plugins synchronously at startup (blocks REPL)
- Mutating in-memory state from background update (stale cache bugs)
- Single error handler for all subsystems (one failure kills everything)
- Allowing plugin updates to auto-activate without session restart
- Not normalizing MCP server names (permission rules silently fail to match)

---

## Module 3: Agent Orchestration & Skill Execution

### Invariant

**Every agent invocation flows through a single validation pipeline (permission check -> agent resolution -> MCP requirement check -> isolation setup -> execution mode routing -> result mapping), regardless of execution mode. Feature flags control schema shape and execution routing at runtime, enabling dead code elimination at build time.**

### Pattern 3.1: Polymorphic Execution Router

A single tool definition handles four execution modes through one `call()` entry point:

```
EXECUTION MODES:
  1. Sync foreground  -- while-loop consuming iterator, blocking
  2. Async background -- fire-and-forget, progress tracked, notified on complete
  3. Teammate spawn   -- flat roster model (teammates can't spawn teammates)
  4. Remote launch    -- separate process entirely

function call(input, context):
  // 1. Validate + resolve agent type
  agent = resolveAgentType(input.subagent_type)
  permissions = checkPermissions(input)

  // 2. Wait for required MCP servers
  if hasPendingRequiredServers:
    poll every 500ms up to 30s:
      if anyRequired.failed: break early
      if noneRequired.pending: break

  // 3. Setup isolation (worktree if requested)
  worktree = input.isolation == 'worktree' ? createWorktree() : null

  // 4. Route to execution mode
  if input.run_in_background:
    return asyncLaunch(agent, input, worktree)
  else:
    return syncExecute(agent, input, worktree)
```

### Pattern 3.2: Foreground-to-Background Transition

The core concurrency pattern: a while-loop racing message iteration against a background signal:

```
function syncExecute(agent, input, worktree):
  iterator = runAgent(agent, input)
  backgroundSignal = createBackgroundPromise()
  messages = []

  while true:
    result = await Promise.race([
      iterator.next().then(r => ({type: 'message', result: r})),
      backgroundSignal    .then(() => ({type: 'background'}))
    ])

    if result.type == 'background':
      // Clean transition: stop foreground, spawn async continuation
      void Promise.race([iterator.return(), sleep(1000)])  // 1s cleanup timeout
      void continueAsAsync(messages, agent, input)
      return {status: 'async_launched', agentId}

    if result.result.done: break
    messages.push(result.result.value)

  return finalize(messages)
```

**Auto-background timer:** Agents can auto-background after 120s if feature-flagged.

### Pattern 3.3: Conditional Schema Construction (Dead Code Elimination)

```
// Schema fields gated by feature flags at module load time
inputSchema = lazySchema(() => {
  base = z.object({description, prompt, subagent_type?, model?, run_in_background?})
  multiAgent = z.object({name?, team_name?, mode?})
  full = base.merge(multiAgent).extend({isolation, cwd?})

  // Feature gates strip fields -- model never sees removed parameters
  if !feature('KAIROS'): full = full.omit({cwd: true})
  if isBackgroundDisabled: full = full.omit({run_in_background: true})
  return full
})

// Build-time elimination via string literal comparison
if ("external" === 'ant'):  // Always false in external builds
  // Entire remote agent block eliminated by bundler
```

### Pattern 3.4: Multi-Tier Feature Flag Cache with Override Chain

```
PRIORITY (highest to lowest):
  1. Env overrides     -- deterministic, for eval harnesses
  2. Config overrides  -- runtime, for /config UI
  3. In-memory cache   -- authoritative after init
  4. Disk cache        -- survives restarts
  5. Default value     -- hardcoded fallback

function getFeatureValue(feature, defaultValue):
  // 1. Env overrides (CLAUDE_INTERNAL_FC_OVERRIDES JSON)
  overrides = getEnvOverrides()
  if feature in overrides: return overrides[feature]

  // 2. Config overrides (user-set via /config)
  configOverrides = getConfigOverrides()
  if feature in configOverrides: return configOverrides[feature]

  // 3. Feature system disabled? Return default
  if !isEnabled(): return defaultValue

  // 4. Track exposure (deferred if pre-init)
  trackExposure(feature)

  // 5. In-memory cache (authoritative after SDK init)
  if inMemoryCache.has(feature): return inMemoryCache.get(feature)

  // 6. Disk cache (survives process restarts)
  cached = diskConfig.cachedFeatures?[feature]
  return cached ?? defaultValue
```

**Critical edge cases:**
- Empty/malformed payload protection: `{features: {}}` must NOT clear caches (prevents total flag blackout)
- Auth availability race: client may be created before auth is available, needs destroy+recreate on auth arrival
- Pending exposure dedup: features accessed before init tracked in Set, logged once after init
- Refresh subscriber catch-up: if init completes before subscriber registers, fire on next microtask
- Client replacement guard: check `client !== thisClient` before AND after async operations
- Process handler accumulation: named refs stored so `process.off()` works across reinit cycles

### Pattern 3.5: Discriminated Union Result Mapping

```
type Output =
  | {status: 'completed', content, totalTokens}
  | {status: 'async_launched', agentId, outputFile}
  | {status: 'teammate_spawned', ...}    // Internal only
  | {status: 'remote_launched', taskId}   // Internal only

function mapResultToWireFormat(data, toolUseId):
  switch data.status:
    'teammate_spawned': return teammateFormat(data)
    'remote_launched':  return remoteFormat(data)
    'async_launched':   return asyncFormat(data)   // Include progress hints
    'completed':        return completedFormat(data) // Include usage trailer
  data satisfies never  // Exhaustiveness check at compile time
```

### Pattern 3.6: Cascading Abort Controller

Tool execution uses hierarchical abort controllers for clean cancellation:

```
HIERARCHY:
  parentAbort (session-level, user Ctrl+C)
    └── siblingAbort (per-turn, shared across concurrent tools)
          └── toolAbort (per-tool, individual cancellation)

RULES:
  - Parent abort cascades to all children (session termination)
  - Sibling abort cascades to all tools in current turn
    (triggered by Bash error in any concurrent tool)
  - Tool abort cancels only that tool (timeout or individual failure)
  - Combined signals: combinedAbortSignal(parent, child) fires on EITHER

function childAbortController(parentSignal):
  child = new AbortController()
  parentSignal.addEventListener('abort', () => child.abort(parentSignal.reason))
  return child
```

### Pattern 3.7: API Client Lifecycle (Multi-Provider)

```
PROVIDERS: Anthropic (default), Bedrock, Vertex

function getOrCreateClient():
  // Memoized — one client per process
  if cached and authUnchanged: return cached
  client = new Anthropic({apiKey, baseURL, ...providerConfig})
  cached = client
  return client

// Critical: client replacement guard
// Auth may arrive after client creation (OAuth dialog pending)
function initializeWithAuth():
  clientBeforeAuth = getOrCreateClient()
  await authFlow()
  if authNowAvailable and !clientCreatedWithAuth:
    destroyClient(clientBeforeAuth)
    cached = null  // Force recreation with auth
    newClient = getOrCreateClient()
    return newClient
```

**Why multi-provider matters:** Bedrock uses SigV4 auth, Vertex uses Google OAuth, direct Anthropic uses API keys. The client abstraction hides this but the auth lifecycle is fundamentally different.

### Edge Cases

- Recursive fork guard: prevents re-entry via querySource matching + message-scan fallback
- Teammates cannot spawn teammates (flat roster)
- In-process teammates cannot manage background agents (lifecycle tied to leader)
- Iterator cleanup with 1s timeout prevents blocking if MCP server cleanup hangs
- Partial result recovery: if error occurs but assistant messages exist, finalize with partial results
- One-shot agent optimization: skip agentId hint and usage trailer (~135 chars saved per invocation)
- AbortController hierarchy: parent->sibling->tool, Bash errors cascade to siblings only
- Client replacement: destroy+recreate when auth arrives after initial client creation
- Bedrock/Vertex: different auth flows but same client interface

### Anti-Patterns

- Blocking startup on feature flag network fetch (must be non-blocking with disk cache fallback)
- Clearing feature flag caches on empty API response
- Symmetric schema for all build targets (prevents dead code elimination)
- Polling without early-exit on failure (30s wasted if MCP server already failed)

---

## Module 4: Context Compaction & Retry

### Invariant

**Context is finite. The system must proactively compress history before hitting limits, using a hierarchy of increasingly expensive strategies, while preserving enough working state (recent files, plans, skills, tool pairings) for the model to continue without capability loss. Retry logic must classify errors and never amplify cascading failures.**

### Pattern 4.1: Compaction Hierarchy (Priority Order)

```
HIERARCHY (cheapest first):
  1. Micro-compact (pre-request)     -- clear stale tool results, zero API cost
  2. Session memory compact          -- use pre-computed running summary, zero summarization cost
  3. Full compact                    -- API call to summarize all messages, most expensive
  4. Reactive compact                -- emergency fallback on prompt_too_long response

THRESHOLDS:
  effectiveWindow = contextWindow - min(maxOutputTokens, 20K)
  autoCompactAt   = effectiveWindow - 13K buffer
  warningAt       = autoCompactAt - 20K
  blockingAt      = effectiveWindow - 3K

POST-COMPACT BUDGETS:
  Files:  50K tokens total, 5K per file, max 5 files (most recently accessed)
  Skills: 25K tokens total, 5K per skill (truncation keeps head where instructions live)
```

### Pattern 4.2: Micro-Compact (Tiered In-Place Reduction)

Two independent strategies, chosen by cache state:

```
COMPACTABLE_TOOLS = {FileRead, Bash, Grep, Glob, WebSearch, WebFetch, FileEdit, FileWrite}

function microcompact(messages, querySource):
  // Strategy 1: Time-based (cache cold -- gap > 60min)
  if timeSinceLastAssistant > threshold:
    toolIds = collectCompactableToolIds(messages)
    keepSet = toolIds.slice(-max(1, config.keepRecent))
    for each toolResult not in keepSet:
      toolResult.content = '[Old tool result content cleared]'
    resetCachedMCState()  // Stale IDs would cause cache_edit errors
    return {messages}

  // Strategy 2: Cache-editing (cache warm, main thread only)
  if supportsAPICacheEdits && isMainThread:
    candidates = getCacheDeletionCandidates()
    return {messages, cacheEdits: {deletedToolIds: candidates}}

  // Strategy 3: No-op
  return {messages}
```

**The 60-minute default matches server-side cache TTL** -- clearing is guaranteed post-cache-expiry, never forces a miss that wouldn't have happened.

### Pattern 4.3: Full Compaction with State Preservation

```
function compactConversation(messages, options):
  // 1. Pre-compact hooks (extensible plugin points)
  hookResults = await runPreCompactHooks()

  // 2. Strip images/attachments (reduce input before summarization)
  stripped = stripImagesFromMessages(messages)  // [image] markers
  stripped = stripReinjectedAttachments(stripped)  // Skill listings re-injected anyway

  // 3. Summarize via forked agent (cache sharing) or streaming
  for attempt in 0..MAX_PTL_RETRIES:
    try:
      summary = await summarizeViaForkedAgent(stripped, cacheSharingParams)
      break
    catch PromptTooLong:
      // Truncate oldest API-round groups, retry
      stripped = truncateHeadForPTLRetry(stripped, error)
      if stripped == null: throw  // Can't truncate further

  // 4. Post-compact state restoration
  fileAttachments = await createPostCompactFileAttachments(messages)
  skillAttachments = createSkillAttachmentIfNeeded()
  planAttachments = restorePlanIfNeeded()
  boundaryMarker = createBoundaryMarker(metadata)

  // 5. Post-compact cleanup
  runPostCompactCleanup(querySource)

  return {boundaryMarker, summary, attachments: [...files, ...skills, ...plans]}
```

### Pattern 4.4: Prompt-Too-Long Retry with Grouped Truncation

```
function truncateHeadForPTLRetry(messages, ptlResponse):
  // Strip own marker from previous retries (prevent stalling)
  input = messages[0].isPTLMarker ? messages.slice(1) : messages

  groups = groupMessagesByApiRound(input)  // Group by assistant message.id
  if groups.length < 2: return null  // Can't truncate further

  tokenGap = parseTokenGapFromError(ptlResponse)
  if tokenGap:
    // Drop oldest groups until gap covered
    dropCount = 0; accumulated = 0
    for group in groups:
      accumulated += estimateTokens(group); dropCount++
      if accumulated >= tokenGap: break
  else:
    dropCount = max(1, floor(groups.length * 0.2))  // Fallback: 20%

  dropCount = min(dropCount, groups.length - 1)  // Always keep at least one group
  sliced = groups.slice(dropCount).flat()

  // Prepend synthetic user marker if first remaining message is assistant
  if sliced[0].type == 'assistant':
    return [createUserMessage(PTL_RETRY_MARKER), ...sliced]
  return sliced
```

### Pattern 4.5: Session Memory Compact (Cursor-Based Preservation)

```
function sessionMemoryCompact(messages, sessionMemory):
  // Find cursor: last summarized message
  cursorIndex = messages.findIndex(m => m.id == sessionMemory.lastSummarizedId)
  if cursorIndex < 0: return null  // Fall back to legacy compact

  // Expand backward to meet minimums
  keepIndex = cursorIndex + 1
  while keepIndex > 0:
    tokens = estimateTokens(messages.slice(keepIndex))
    textBlocks = countTextBlockMessages(messages.slice(keepIndex))
    if tokens >= minTokens && textBlocks >= minTextBlockMessages: break
    if tokens >= maxTokens: break  // Hard cap
    keepIndex--

  // CRITICAL: Preserve API invariants
  keepIndex = adjustForAPIInvariants(messages, keepIndex)
  return {summary: sessionMemory.content, messagesToKeep: messages.slice(keepIndex)}

function adjustForAPIInvariants(messages, startIndex):
  // Step 1: Pull in orphaned tool_use blocks
  // (tool_result in kept range must have matching tool_use)
  toolResultIds = collectToolResultIds(messages.slice(startIndex))
  toolUseIds = collectToolUseIds(messages.slice(startIndex))
  missing = toolResultIds.filter(id => !toolUseIds.has(id))
  for i in reverse(0..startIndex):
    if messages[i] has tool_use with missing id:
      startIndex = i

  // Step 2: Pull in thinking blocks sharing message.id
  // (streaming yields separate messages per content block with same id)
  keptIds = collectAssistantMessageIds(messages.slice(startIndex))
  for i in reverse(0..startIndex):
    if messages[i].id in keptIds:
      startIndex = i

  return startIndex
```

### Pattern 4.6: Auto-Compact with Circuit Breaker

```
MAX_CONSECUTIVE_FAILURES = 3  // Was wasting ~250K API calls/day at 50+ failures

function autoCompactIfNeeded(messages, tokenCount, trackingState):
  // Guards
  if trackingState.consecutiveFailures >= MAX_CONSECUTIVE_FAILURES: return
  if querySource in ['session_memory', 'compact']: return  // Recursion prevention
  if isContextCollapseMode: return  // Different system handles this
  if tokenCount < autoCompactThreshold: return

  // Priority: session memory compact > full compact
  try:
    if sessionMemoryAvailable && !hasCustomInstructions:
      await sessionMemoryCompact(messages)
    else:
      await fullCompact(messages)
    trackingState.consecutiveFailures = 0
  catch:
    trackingState.consecutiveFailures++
```

### Pattern 4.7: Classified Retry with Adaptive Backoff

```
function withRetry(apiCall, options):
  consecutive529s = options.initialConsecutive529Errors ?? 0

  for attempt in 1..maxRetries:
    try:
      return await apiCall()
    catch error:
      classification = classifyError(error)

      switch classification:
        'fast_mode_429_short':    // < 20s retry-after
          await sleep(retryAfterMs)
          continue with fast mode

        'fast_mode_429_long':     // Unknown/long retry-after
          enterCooldown(min 10min, default 30min)
          disable fast mode; continue

        'non_foreground_529':     // Background agent hit capacity
          bail immediately        // Never amplify cascading failures

        'consecutive_529':
          consecutive529s++
          if consecutive529s >= 3: try model fallback or surface error

        'max_tokens_overflow':
          newMax = parseAvailableContext(error) - 1K_safety_buffer
          if newMax >= thinkingBudget + 1: retry with newMax

        'auth_error':
          refreshCredentials(); getNewClient(); retry

        'persistent_mode':        // Unattended operation
          retry indefinitely, max backoff 5min
          reset cap 6hr, heartbeat every 30s

function getRetryDelay(attempt, retryAfterHeader, maxDelay = 32000):
  if retryAfterHeader: return parseSeconds(retryAfterHeader) * 1000
  baseDelay = min(500 * 2^(attempt-1), maxDelay)
  jitter = random() * 0.25 * baseDelay
  return baseDelay + jitter
```

### Pattern 4.8: Scoped Post-Compact Cache Invalidation

```
function runPostCompactCleanup(querySource):
  isMainThread = querySource in ['repl_main_thread*', 'sdk', undefined]

  // Always reset (any thread)
  resetMicrocompactState()
  clearSystemPromptSections()
  clearClassifierApprovals()
  clearSpeculativeChecks()
  sweepFileContentCache()
  clearSessionMessagesCache()

  // Main thread only (sub-agents share module-level state)
  if isMainThread:
    resetContextCollapse()
    getUserContext.cache.clear()  // Outer memoize
    resetMemoryFilesCache()      // Inner cache

  // Intentionally NOT cleared: skill content, skill names
  // (skills are re-injected post-compact anyway)
```

### Pattern 4.9: Thinking Block Budget Accounting

Modern Claude models support extended thinking. Token accounting must handle:

```
THINKING BLOCKS:
  - thinking: visible reasoning (counts toward output tokens)
  - redacted_thinking: reasoning hidden from user (still counts toward output)
  - Budget: thinkingBudget field in API request (1024-2048 minimum)

TOKEN ESTIMATION WITH THINKING:
  effectiveOutput = outputTokens + thinkingTokens
  maxTokensOverride >= thinkingBudget + 1  // Must leave room for at least 1 output token

  // During message normalization:
  if model doesn't support thinking:
    strip all thinking/redacted_thinking blocks from messages
  else:
    preserve thinking blocks for context continuity

COST IMPACT:
  Thinking tokens billed at output token rate.
  A 4K-token thinking budget on every turn doubles effective output cost.
  Cost tracker must account: mu.outputTokens += usage.output_tokens (includes thinking)
```

### Pattern 4.10: Session Memory (Long-Term Fact Persistence)

Orthogonal to compaction (which summarizes messages). Session memory preserves facts across sessions:

```
SESSION MEMORY LIFECYCLE:
  1. Extraction: background process analyzes conversation, extracts facts
  2. Persistence: facts stored with lastSummarizedMessageId as cursor
  3. Retrieval: on session resume, inject memory as context
  4. Compaction integration: if memory available, use as compact summary
     (avoids expensive summarization API call)

CURSOR MODEL:
  lastSummarizedMessageId tracks what's been processed.
  Messages after this ID are "unsummarized" — must be preserved during compaction.
  If cursor not found in messages (edited externally), fall back to legacy compact.
```

### Edge Cases

- Prompt-too-long during compact itself: retry by truncating oldest API-round groups (max 3 retries)
- API user abort during compact: detected via `isApiErrorMessage` flag
- WebSocket idle timeout during long compaction: keep-alive heartbeat every 30s
- `slice(-0)` returns full array: floored `keepRecent` to `max(1, ...)`
- Sub-agent compaction must NOT reset main-thread module-level state
- SDK sometimes drops 529 status during streaming: check `"type":"overloaded_error"` in message body
- Fast mode overage disabled: read from response header, enter cooldown
- Pre-seeded 529 counter from streaming fallback carries across retry instances
- Thinking blocks: strip if model doesn't support them, budget must be >= 1024
- `maxTokensOverride` must leave room for thinking budget + 1 output token
- Session memory cursor not found: falls back to legacy full compact
- Resumed session with no cursor: treats all messages as unsummarized

### Anti-Patterns

- Running full compaction when micro-compact would suffice (wasted API calls)
- No circuit breaker on auto-compact (can waste 250K+ API calls/day on stuck sessions)
- Retrying 529s from background agents (amplifies cascading failures)
- Clearing all caches after sub-agent compaction (corrupts main thread state)
- Not preserving API invariants when truncating (orphaned tool_results crash the API)
- Setting retry delay without jitter (thundering herd)

---

## Cross-Cutting Patterns

### Signal-Based Refresh with Catch-Up

Used by both feature flags and plugin updates:

```
signal = createSignal()

function onRefresh(listener):
  unsub = signal.subscribe(listener)
  // Catch-up: if init already completed, fire once on next microtask
  if alreadyInitialized:
    queueMicrotask(() => { if stillSubscribed: listener() })
  return () => { subscribed = false; unsub() }
```

### Safe Config Mutation with Change Detection

```
function setConfigOverride(feature, value):
  saveConfig(current => {
    overrides = current.overrides ?? {}
    if value === undefined:
      if !(feature in overrides): return current  // No-op, same ref
      {[feature]: _, ...rest} = overrides
      return rest.length == 0 ? omit(current, 'overrides') : {...current, overrides: rest}
    if isEqual(overrides[feature], value): return current  // No-op
    return {...current, overrides: {...overrides, [feature]: value}}
  })
  signal.emit()  // Subscribers do their own change detection
```

### API-Round Grouping (Not Human-Turn)

```
// Messages grouped by new assistant message.id, not by human turns
// This enables operation on single-prompt agentic sessions
function groupByApiRound(messages):
  groups = []; current = []; lastAssistantId = null
  for msg in messages:
    if msg.type == 'assistant' && msg.id != lastAssistantId && current.length > 0:
      groups.push(current); current = [msg]
    else: current.push(msg)
    if msg.type == 'assistant': lastAssistantId = msg.id
  if current.length > 0: groups.push(current)
  return groups
```

---

## Module 5: Self-Configuration (Point It At Itself)

This module makes the skill actionable. When invoked, Claude can use these patterns to actually configure Claude Code's behavior.

### Invariant

**Claude Code's behavior is fully configurable through four surfaces: settings.json (permissions, hooks, env, model), CLAUDE.md files (project instructions), plugin manifests (extensions), and the /config command (interactive). Settings merge across sources with strict priority: policy > local > project > user > plugin.**

### Pattern 5.1: Settings File Hierarchy

```
PRIORITY (highest wins):
  1. Policy settings    — /etc/claude-code/managed-settings.json (admin-controlled)
  2. Flag settings      — inline via SDK or file path
  3. Local settings     — .claude/settings.local.json (gitignored, personal)
  4. Project settings   — .claude/settings.json (committed, shared)
  5. User settings      — ~/.claude/settings.json (global personal)
  6. Plugin settings    — via plugin manifests (lowest priority)

MERGE RULES:
  - Objects: deep merge (higher priority keys override)
  - Arrays: concatenate and deduplicate across sources
  - Primitives: highest priority source wins
```

### Pattern 5.2: Permission Rules

Configure what Claude can do without asking:

```
// In settings.json or .claude/settings.json
{
  "permissions": {
    "allow": [
      "Read",                    // All file reads
      "Bash(git:*)",             // All git commands
      "Bash(npm test)",          // Exact command
      "Bash(cargo build:*)",     // Prefix match
      "Write(src/**/*.ts)",      // Glob match on paths
      "mcp__serverName__*"       // All tools from an MCP server
    ],
    "deny": [
      "Bash(rm -rf:*)",          // Block destructive commands
      "Bash(curl:*)",            // Block network from shell
      "Write(.env*)"             // Block writing secrets
    ],
    "defaultMode": "auto"        // auto | default | plan | acceptEdits | dontAsk
  }
}
```

**Rule syntax:**
- `Tool` — matches all uses of that tool
- `Tool(exact command)` — exact string match
- `Tool(prefix:*)` — prefix match (word boundary enforced)
- `Tool(glob pattern)` — glob matching for file paths
- `mcp__server__tool` — MCP tool permission
- Deny always beats allow (same priority logic as Module 1)

### Pattern 5.3: Hooks (Automated Behaviors)

Hooks run shell commands, prompts, agents, or HTTP calls in response to events:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'About to run bash'",
            "timeout": 5000
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "npx prettier --write $CLAUDE_FILE_PATH",
            "timeout": 10000,
            "statusMessage": "Formatting..."
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Check if the user's request is clear before proceeding"
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "cat ~/daily-context.md",
            "statusMessage": "Loading daily context..."
          }
        ]
      }
    ]
  }
}
```

**Hook events:**
| Event | Fires When | Common Use |
|-------|-----------|------------|
| `PreToolUse` | Before any tool runs | Validation, logging |
| `PostToolUse` | After any tool completes | Formatting, linting |
| `UserPromptSubmit` | User sends a message | Input validation |
| `SessionStart` | New session begins | Context loading |
| `SessionEnd` | Session closes | Cleanup, summaries |
| `PreCompact` | Before compaction | State preservation |
| `PostCompact` | After compaction | Cache warming |
| `Stop` | Agent stops | Notifications |
| `Notification` | System notification | Alerts, logging |
| `TaskCreated` | New task created | Progress tracking |
| `TaskCompleted` | Task finished | Reporting |

**Hook types:**
| Type | What It Does | Best For |
|------|-------------|----------|
| `command` | Runs shell command | Formatting, linting, git hooks |
| `prompt` | Sends prompt to Claude | Validation, context injection |
| `agent` | Spawns a sub-agent | Complex automated workflows |
| `http` | Makes HTTP request | External service integration |

### Pattern 5.4: CLAUDE.md Project Instructions

The instruction hierarchy that controls Claude's behavior per-project:

```
DISCOVERY ORDER (all loaded, lower overrides higher):
  1. /etc/claude-code/CLAUDE.md          — system-wide (admin)
  2. ~/.claude/CLAUDE.md                 — user global
  3. <project-root>/CLAUDE.md            — project root (committed)
  4. <project-root>/.claude/CLAUDE.md    — project config dir
  5. <project-root>/.claude/rules/*.md   — modular rules (all .md files loaded)
  6. <project-root>/CLAUDE.local.md      — local overrides (gitignored)

FEATURES:
  - @include directives: @path, @./relative, @~/home, @/absolute
  - Works in leaf text nodes only (not inside code blocks)
  - Circular reference prevention built in
  - Frontmatter extraction with glob patterns
```

**Best practice for team projects:**
```
project/
  CLAUDE.md                    # Shared conventions, architecture overview
  .claude/
    settings.json              # Shared permissions and hooks
    rules/
      testing.md               # Testing conventions
      api-patterns.md          # API design rules
      security.md              # Security requirements
  CLAUDE.local.md              # Personal preferences (gitignored)
  .claude/
    settings.local.json        # Personal permissions (gitignored)
```

### Pattern 5.5: Configuration Recipes

**Recipe: Lock down a production repo**
```json
{
  "permissions": {
    "deny": [
      "Bash(rm -rf:*)", "Bash(git push --force:*)", "Bash(git reset --hard:*)",
      "Bash(DROP TABLE:*)", "Bash(DELETE FROM:*)",
      "Write(.env*)", "Write(*secret*)", "Write(*credential*)"
    ],
    "defaultMode": "plan"
  }
}
```

**Recipe: Auto-format on every file write**
```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write",
      "hooks": [{
        "type": "command",
        "command": "npx prettier --write \"$CLAUDE_FILE_PATH\" 2>/dev/null || true",
        "timeout": 10000,
        "statusMessage": "Formatting..."
      }]
    }]
  }
}
```

**Recipe: Auto-lint after bash commands**
```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "if echo \"$CLAUDE_TOOL_INPUT\" | grep -q 'git commit'; then npm run lint 2>/dev/null; fi",
        "timeout": 30000,
        "statusMessage": "Linting..."
      }]
    }]
  }
}
```

**Recipe: Inject daily context on session start**
```json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "echo '---'; echo 'Active sprint:'; cat ~/sprint-context.md 2>/dev/null; echo '---'; echo 'Recent PRs:'; gh pr list --limit 5 2>/dev/null",
        "timeout": 10000,
        "statusMessage": "Loading context..."
      }]
    }]
  }
}
```

**Recipe: Full autonomous mode for trusted projects**
```json
{
  "permissions": {
    "allow": [
      "Read", "Write(src/**)", "Write(tests/**)",
      "Bash(git:*)", "Bash(npm:*)", "Bash(cargo:*)",
      "Bash(python:*)", "Bash(pytest:*)",
      "Edit", "Glob", "Grep"
    ],
    "deny": [
      "Bash(rm -rf /)", "Bash(sudo:*)",
      "Write(.env*)", "Write(*secret*)"
    ],
    "defaultMode": "auto"
  }
}
```

**Recipe: Modular project rules via .claude/rules/**
```markdown
<!-- .claude/rules/api-patterns.md -->
When writing API endpoints:
- Always validate input with zod schemas
- Return consistent error shapes: {error: string, code: number}
- Add OpenAPI JSDoc comments to every endpoint
- Rate limit all public endpoints
```

```markdown
<!-- .claude/rules/testing.md -->
Testing conventions:
- Every new function gets a test file in __tests__/
- Use vitest, not jest
- Mock external services, never databases
- Minimum 80% branch coverage for new code
```

### Pattern 5.6: Plugin/Skill Installation

```bash
# Install a plugin marketplace
claude plugin install anthropics/claude-code-plugins

# Enable/disable specific plugins
# In settings.json:
{
  "enabledPlugins": {
    "my-plugin@marketplace-name": true,
    "another-plugin@marketplace-name": false
  }
}

# Create a local skill (no marketplace needed)
mkdir -p ~/.claude/skills/my-skill/
cat > ~/.claude/skills/my-skill/SKILL.md << 'EOF'
---
name: my-skill
description: What this skill does
userInvocable: true
---
# My Skill
Instructions for Claude when this skill is invoked...
EOF
```

### Edge Cases

- `settings.local.json` is always gitignored -- safe for personal API keys and preferences
- Policy settings (`/etc/claude-code/managed-settings.json`) cannot be overridden by user/project
- `allowManagedPermissionRulesOnly: true` locks permission rules to admin-only
- `disableAllHooks: true` kills all hooks including status line
- Hooks with `once: true` fire only once per session
- `async: true` hooks don't block the tool execution
- Invalid settings fields are preserved in files for user correction (not silently dropped)

### Anti-Patterns

- Putting secrets in `settings.json` instead of `settings.local.json`
- Using `dontAsk` mode without deny rules (no safety net)
- Writing hooks that modify the same files Claude is editing (race conditions)
- Putting implementation details in CLAUDE.md (it's for conventions and rules, not code)
- Using `Bash(*)` as an allow rule (equivalent to no permission system)

---

## Module 6: Query Engine & Main Loop Orchestration

### Invariant

**Every iteration of the main loop produces exactly one API call, consumes its streamed response, executes any tool calls concurrently, and either terminates or continues with accumulated messages. The loop is an AsyncGenerator — the caller pulls messages one at a time. Recovery from errors is state-machine-based with named transitions.**

### Pattern 6.1: The Agentic Message Loop

```
function* query(messages, systemPrompt, canUseTool, tools):
  state = { messages, turnCount: 1, recoveryCount: 0 }

  while true:
    msgs = state.messages

    # 1. Context compression pipeline (ORDER MATTERS)
    msgs = applyToolResultBudget(msgs)    // trim large results
    msgs = snipOldMessages(msgs)          // remove beyond horizon
    msgs = microcompactLargeResults(msgs) // summarize or cache-edit
    msgs = collapseArchivedSegments(msgs) // project collapsed view
    compacted = autocompactIfOverThreshold(msgs)
    if compacted: msgs = compacted

    # 2. Pre-flight guard
    if tokenCount(msgs) > HARD_LIMIT and !autoRecoveryEnabled:
      yield ErrorMessage("prompt too long"); return

    # 3. Stream model response; execute tools concurrently
    toolExecutor = StreamingToolExecutor(tools, canUseTool)
    assistantMsgs = []

    for event in callModel(msgs, systemPrompt):
      if event.type == "assistant":
        assistantMsgs.append(event)
        for block in event.toolUseBlocks:
          toolExecutor.startTool(block)  // concurrent execution begins
      yield event
      for result in toolExecutor.completedResults():
        yield result  // drain during streaming

    # 4. No tool calls: attempt recovery or finish
    if not hasToolUse:
      if isPromptTooLong: try collapse/reactive compact or return
      if isMaxOutputTokens and recoveryCount < 3:
        inject resumeNudge; recoveryCount++; continue
      return  // turn complete

    # 5. Drain remaining tool results
    toolResults = drain(toolExecutor.remaining())

    # 6. Inject post-tool attachments
    toolResults += getMemoryAttachments() + getSkillAttachments()

    # 7. Guard turn limit
    if ++turnCount > maxTurns: return

    # 8. Continue loop
    state.messages = msgs + assistantMsgs + toolResults
```

### Pattern 6.2: Session Lifecycle Wrapper (QueryEngine)

```
class QueryEngine:
  messages: Message[]     // full conversation history
  totalUsage: Usage       // cumulative token counts
  permissionDenials: []   // tracked for final result

  function* submitMessage(prompt):
    # Wrap canUseTool to track denials
    wrappedCanUseTool = (tool, input) =>
      result = canUseTool(tool, input)
      if result != "allow": permissionDenials.append(denial)
      return result

    # Process user input (slash commands, attachments)
    {newMessages, shouldQuery} = processUserInput(prompt)
    messages.push(...newMessages)

    if not shouldQuery:
      yield commandOutput; yield Result(success); return

    # Consume query generator
    for message in query(messages, systemPrompt, wrappedCanUseTool):
      switch message.type:
        "assistant":  messages.push(message); yield toSDK(message)
        "user":       messages.push(message); yield toSDK(message)
        "stream_event": trackUsage(message.event)  // accumulate tokens
        "system" where "compact_boundary":
          messages.splice(0, boundaryIndex)  // GC pre-compact messages
        "attachment" where "max_turns_reached":
          yield Result(error_max_turns); return

      if totalCost >= maxBudget:
        yield Result(error_max_budget); return

    yield Result(success, cost, usage, denials)
```

### Pattern 6.3: Streaming Tool Execution (Concurrent + Ordered)

```
class StreamingToolExecutor:
  tools: TrackedTool[] = []
  siblingAbort = childAbortController(parentAbort)

  addTool(block):
    safe = toolDef.isConcurrencySafe(block.input)
    tools.push({id, block, status: "queued", safe, results: []})
    processQueue()

  canExecute(safe):
    executing = tools.filter(t => t.status == "executing")
    return executing.empty OR (safe AND all executing are safe)

  processQueue():
    for tool in tools where status == "queued":
      if canExecute(tool.safe):
        launchAsync(tool)  // chains processQueue on completion
      else if NOT tool.safe:
        break  // preserve ordering for exclusive tools

  launchAsync(tool):
    tool.status = "executing"
    for update in runToolUse(tool.block, context):
      if update.isError AND tool.isBash:
        siblingAbort.abort("sibling_error")  // cascade kill
      tool.results.push(update)
    tool.status = "completed"
    processQueue()  // unblock next

  *getCompletedResults():  // ordered drain
    for tool in tools:
      if tool.status == "completed":
        tool.status = "yielded"
        yield all tool.results
      else if tool.status == "executing" AND NOT tool.safe:
        break  // hold order for exclusive tools
```

**Key insight:** Concurrent-safe tools fan out in parallel. Non-concurrent tools serialize. Bash errors cascade-cancel all siblings via a child AbortController. Results are always emitted in tool-receive order regardless of completion order.

### Edge Cases

- Recovery is state-machine-based: implicit states via `State` object + `continue` (next_turn, reactive_compact_retry, max_output_tokens_recovery, stop_hook_blocking)
- Permissions are callback-injected, not hardcoded — the entire permission system is a single `canUseTool` function parameter
- Compact boundary handling: QueryEngine splices pre-boundary messages for GC — the only place conversation memory is physically freed
- Agent scope isolation: queue draining is scoped by `agentId` to prevent cross-agent message leaks
- Auto-background after 120s if feature-flagged

### Anti-Patterns

- Hardcoding permission checks in the query loop (makes testing/extension impossible)
- Running compaction layers in wrong order (snip must come before microcompact before autocompact)
- Not draining tool results during streaming (wastes tool I/O latency overlap)
- Missing turn limit guard (infinite loops on tool-calling models)

---

## Module 7: Message Pipeline & Cost Tracking

### Invariant

**Every internal `Message[]` must be normalized into strict `(UserMessage | AssistantMessage)[]` before any API call. Cost state is a monotonically increasing accumulator per session, partitioned by model. Every API error is classified by a string tag for retry logic AND converted to a user-visible message — dual-function design with shared cascade.**

### Pattern 7.1: Message Normalization Pipeline

```
function normalizeMessagesForAPI(messages, availableTools):
  toolNames = Set(availableTools.map(t => t.name))

  # Phase 1: Reorder attachments up to tool_result/assistant boundaries
  reordered = reorderAttachments(messages)
  reordered = reordered.filter(m => not m.isVirtual)

  # Phase 2: Build strip-map for past media errors
  # If assistant error matches known media error, walk backward to find
  # the user message with the offending image/doc block and mark it
  stripTargets = Map<messageUUID, Set<blockType>>
  for i, msg in reordered:
    if msg is synthetic API error:
      blockTypes = KNOWN_ERROR_TO_BLOCK_TYPES[errorText]
      if blockTypes:
        for j = i-1 downto 0:
          if reordered[j] is user and isMeta:
            stripTargets[reordered[j].uuid].addAll(blockTypes)
            break

  # Phase 3: Filter, merge, normalize
  result = []
  for msg in reordered:
    skip: progress messages, non-command system messages
    user:      strip unavailable tool_refs, strip flagged media blocks,
               merge with previous if consecutive
    assistant: strip unsupported thinking blocks, normalize tool_use inputs,
               insert placeholder if consecutive
    attachment: convert to user message content, merge with previous user
    result.append(normalized)

  # Phase 4: Ensure tool_use / tool_result pairing
  ensureToolResultPairing(result)
  return result
```

**Key insight:** The strip-map for past media errors is crucial — rather than re-sending a 50MB PDF on every retry, it retroactively removes the offending block from the user message that originally contained it.

### Pattern 7.2: Cost Accumulation Model

```
state = {
  totalCostUSD: 0,
  modelUsage: Map<modelName, ModelUsage>,  // per-model buckets
}

struct ModelUsage:
  inputTokens, outputTokens: int
  cacheReadInputTokens, cacheCreationInputTokens: int
  webSearchRequests: int
  costUSD: float
  contextWindow, maxOutputTokens: int

function addToTotalSessionCost(cost, usage, model):
  mu = state.modelUsage.getOrCreate(model, ModelUsage())
  mu.inputTokens      += usage.input_tokens
  mu.outputTokens     += usage.output_tokens
  mu.cacheReadTokens  += usage.cache_read_input_tokens ?? 0
  mu.cacheWriteTokens += usage.cache_creation_input_tokens ?? 0
  mu.costUSD          += cost
  state.totalCostUSD  += cost

  # OTel counters for observability
  costCounter.add(cost, {model})
  tokenCounter.add(usage.input_tokens,  {model, type: "input"})
  tokenCounter.add(usage.output_tokens, {model, type: "output"})

  # Recursive: account for advisor/sub-model usage
  for advisorUsage in getAdvisorUsage(usage):
    advisorCost = calculateUSDCost(advisorUsage.model, advisorUsage)
    addToTotalSessionCost(advisorCost, advisorUsage, advisorUsage.model)

function saveSessionCosts(sessionId):
  persist {sessionId, state} to config  // enables resume

function restoreSessionCosts(sessionId):
  stored = loadFromConfig(sessionId)
  if stored?.sessionId == sessionId: state = stored; return true
  return false
```

### Pattern 7.3: Error Classification (Dual-Function Cascade)

```
CLASSIFICATION (for machines — retry logic, analytics):
  function classifyAPIError(error) -> string:
    if error.aborted:                        return "aborted"
    if error is timeout:                     return "api_timeout"
    if "Repeated 529" in message:            return "repeated_529"
    if status == 429:                        return "rate_limit"
    if status == 529 or "overloaded_error":  return "server_overload"
    if "prompt is too long":                 return "prompt_too_long"
    if "PDF pages" in message:               return "pdf_too_large"
    if status == 400 and "image exceeds":    return "image_too_large"
    if status == 400 and "tool_use ids":     return "tool_use_mismatch"
    if "x-api-key" in message:               return "invalid_api_key"
    if status == 403 and "token revoked":    return "token_revoked"
    if status in {401, 403}:                 return "auth_error"
    if status >= 500:                        return "server_error"
    if status >= 400:                        return "client_error"
    if error is ConnectionError:             return "connection_error"
    return "unknown"

CONVERSION (for humans — user-visible messages):
  function errorToMessage(error, model) -> AssistantMessage:
    // Same cascade but produces contextual help text:
    // - 429: parses rate-limit headers for reset times
    // - prompt_too_long: preserves raw error in errorDetails
    //   (reactive compact parses "137500 > 135000" to calculate token gap)
    // - auth errors: shows re-auth guidance
    // - media errors: suggests stripping images
```

### Pattern 7.4: Post-Tool Hook Lifecycle

```
async *runPostToolUseHooks(context, tool, input, output):
  for result in executePostToolHooks(tool.name, input, output):
    match result:
      {cancelled}:            yield attach("hook_cancelled")
      {blockingError}:        yield attach("hook_blocking_error", error)
      {preventContinuation}:  yield attach("hook_stopped"); return  // hard stop
      {additionalContexts}:   yield attach("hook_additional_context", contexts)
      {updatedMCPToolOutput}: output = result.output; yield {output}
    on error:
      yield attach("hook_error_during_execution", formatError(err))

# CRITICAL: Hook 'allow' never overrides settings 'deny'
resolveHookPermission(hookResult, tool, input, context):
  if hookResult.behavior == "allow":
    ruleCheck = checkRuleBasedPermissions(tool, input)
    if ruleCheck == "deny": return ruleCheck  // settings win
    if ruleCheck == "ask":  return promptUser()
  return hookResult  // fall through to normal flow
```

### Edge Cases

- Bedrock requires merging consecutive same-role messages (Claude API doesn't)
- Message normalization must strip thinking blocks if model doesn't support them
- Cost tracker recursively accounts for advisor/sub-model usage (e.g., Haiku classifier costs)
- Session cost is persist-able to config, enabling resume across process restarts
- Error classification returns ~20 string tags — `"unknown"` is the catch-all
- `errorDetails` field in prompt-too-long errors feeds back into reactive compact token gap parsing
- Async hooks run shell commands in background, polled for completion via `checkForAsyncHookResponses()`
- Hook registry uses `Promise.allSettled` so one hook failure doesn't orphan others

### Anti-Patterns

- Not stripping media blocks from past failed messages (re-sends 50MB PDF every retry)
- Single error handler for all API errors (need separate classify + convert paths)
- Not tracking cost per-model (can't attribute spend to classifiers vs main model)
- Letting hook `allow` override settings `deny` (security hole)
- Synchronous hook execution (blocks the query loop)

---

## Smoke Tests

### Test 1: Permission Cascade Priority

```
Given: deny rule "rm:*", allow rule "rm -rf node_modules"
When:  command "rm -rf node_modules" is checked
Then:  result is DENY (deny always wins over allow)

Given: no rules configured
When:  command "cat README.md" is checked
Then:  result is ALLOW (read-only auto-allow)

Given: allow rule "git:*"
When:  command "FOO=bar git status" is checked
Then:  result is ALLOW (safe env var stripped for allow matching)

Given: allow rule "docker:*"
When:  command "DOCKER_HOST=evil docker ps" is checked
Then:  result is ASK (DOCKER_HOST not in safe env vars for allow)
```

### Test 2: Compaction Hierarchy Selection

```
Given: 15 minutes since last assistant message, cache warm
When:  microcompact runs
Then:  cache-editing path selected (not time-based)

Given: 90 minutes since last assistant message
When:  microcompact runs
Then:  time-based path selected, old tool results cleared to '[Old tool result content cleared]'

Given: session memory available with cursor at message #50, 100 messages total
When:  auto-compact triggers
Then:  session memory compact used (not full compact), messages after cursor preserved
       with API invariants (orphaned tool_use pulled in)

Given: 3 consecutive auto-compact failures
When:  auto-compact would trigger again
Then:  circuit breaker fires, no API call made
```

### Test 3: Agent Foreground-to-Background Transition

```
Given: agent running in sync foreground mode
When:  background signal fires mid-execution
Then:  1. Current iterator gets 1s cleanup timeout
       2. Existing messages replayed through progress tracker
       3. New async context continues iteration
       4. Caller receives {status: 'async_launched'} immediately
       5. Worktree preserved (not auto-cleaned)
```
