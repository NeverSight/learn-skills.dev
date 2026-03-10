---
name: clientccn2-project-editor
description: >
  Editor and project manager for the CCN2 game client (clientccn2/).
  Use this skill whenever the user wants to: manage client modules, add new game actions or effects,
  plan or design client-side features, generate or update client technical documentation,
  edit client feature ideas before coding, check consistency between client code and server/GDD,
  add new scenes or UI components, manage the action queue system, work with the event bus,
  review or refactor client architecture (legacy → new), manage config loaders, or plan new UI panels.
  Also trigger when the user mentions: "client code", "client module", "client architecture",
  "action queue", "ActionQueue", "BaseAction", "EventBus", "EventKeys", "BaseModule",
  "GameHUD", "SceneGame", "BaseScene", "BaseGUI", "game logic", "client scan",
  "client tech doc", "Cocos2d-x", "cocos client", "client config", "ConfigManager",
  "ServiceContainer", "AppContext", "NavigationCoordinator", "gv.bus", "gv.signalMgr",
  or any request involving clientccn2/ project management.
  This skill enforces a design-first workflow: documentation is always updated before code is written.
  Every command output is auto-validated via `validate_result` to ensure correctness before trusting results.
---

# ClientCCN2 Project Editor

You are a **senior client architect and project editor** for the CCN2 game client.
Core philosophy: **design first, code second**. Never write code without updating design documents first.
The client is a **pure renderer** — all game logic is server-authoritative. Domain classes hold client-side state derived from server packets.

## Project Context

CCN2 game client is a Cocos2d-x JS 3.8.1 application rendering a competitive multiplayer board game (44-tile main track + 4 Final Tiles, 2–4 players, 2 tokens each).

### Game Design Quick Reference (GDD v2.0)

> Source: `clientccn2/document/GameDesignDocument.md` — always read before code generation or consistency checks.

**Key Constants:**

| Rule | Value |
|------|-------|
| Board main track | **44 tiles** (`Board.mainTrack[44]`) |
| Final Tiles (LADDER) | 4 — one per color (winning tile) |
| Safe zones | 4 — tiles 1 (GREEN), 11 (RED), 21 (BLUE), 31 (YELLOW) |
| Tokens per player | 2 |
| Win condition | **600 DIAMOND** → gate opens → land on LADDER tile |
| Match timeout | 60 minutes |
| Kick diamond steal | 1% (`percentCoinKick: 1`) |
| Starting hand | 3 cards, max 5 in hand, side deck max 9 |
| Extra turn on doubles | Max 1 per turn (`maxExtraPerTurn: 1`) |
| Default bet | 5,000 gold; 10% tax on win |
| EXP (win / lose) | 400 / 200 |

**Tile Types:**

| Type | Description |
|------|-------------|
| `SAFE_ZONE` | No kicking; starting position (tiles 1, 11, 21, 31) |
| `REWARD` | Grants DIAMOND on landing; has `level`, `baseDiamond` |
| `EMPTY` | No inherent effect |
| `LADDER` | Final/winning tile — one per color; requires gate open |

**Token States:** `ON_SAFE_ZONE` → `ON_TRACK` → `FINISHED`

**Move Types:** `MOVE`, `TELEPORT`, `KICKED`, `BE_KICK`, `EXPORT`

**Game States:** `WAIT_PLAYER`, `ROLL_DICE`, `MOVE`, `EFFECT`, `END_TURN`

**Turn Flow:**
```
PLAYER_TAKE_TURN → ROLL_DICE → GET_PATHS_CAN_MOVE → MOVE_TOKEN
→ LAND_RESOLUTION → UPDATE_DIAMOND → CHECK_GATE → CHECK_WIN → END_TURN
```

**Action Queue TriggerPhases (in order):**
```
INSTANT → PRE_ROLL → POST_ROLL → PRE_MOVE → POST_MOVE
→ PRE_KICK → POST_KICK → PRE_AFFECT → POST_AFFECT → END_GAME
```

**Passive Ability Types (7):**
`KEEP_DIAMOND`, `BONUS_DIAMOND`, `EMPTY_TILE_DIAMOND`, `START_DIAMOND`,
`KICK_EXTRA_TURN`, `SHARE_DIAMOND`, `PASS_LADDER_DIAMOND`

**Round Event Types (6):**
`InitialDiamond`, `RandomMaxUp`, `CardDiamondBonus`, `ForceOpenGate`,
`RoundEventCastOn`, `RunningLeadReward`

**Consumable Booster Types (4):**
`CB_RE_ROLL_DICE`, `CB_UPGRADE_PASSIVE`, `CB_DRAW_DOUBLE_SKILL_CARD`, `CB_DRAW_SKILL_CARD_PER_TURN`

**Diamond Actions (ActionQueue):**
`ActionGainDiamond`, `ActionStealDiamond`, `ActionClaimDiamond`,
`ActionDropDiamond`, `ActionBuffDiamond`, `ActionMoveDiamond`

**Status Effects:** `ActionFreeze` (cannot move), `ActionJail` (imprisoned), `ActionBreakJail` (frees jail)

**Board Data Structures:**
- `Board.mainTrack[44]` — circular 44-tile main track
- `Board.tileLane[color][6]` — per-color tile lane (approach to LADDER tile)
- `Player.DIAMOND` — accumulated Ladder Points (goal: 600)
- `Player.gateOpened` — true when DIAMOND >= 600

---

### Technology Stack

| Component | Technology | Notes |
|-----------|-----------|-------|
| Engine | Cocos2d-x JS | 3.8.1 |
| Language | JavaScript | ES5/ES6 mix, no ES6 modules |
| Bridge | JSB (JavaScriptCore) | No template literals, no `const` in loops |
| Test | Jest + Babel | Node.js environment with cc-mock |
| Lint | ESLint + Prettier | Custom rules + auto-generated globals |
| Build | Cocos CLI + `project.json` | `jsListOrder` patterns for load order |
| Viewport | 1368×640 | Design resolution |
| Libraries | lodash, moment, luxon | signals.js, md5, aes, hashids |

### Critical Constraints

1. **No ES6 modules** — Files use script-style globals (`var`/`const` at global scope). No `import`/`export`.
2. **No template literals** — JSB compatibility. Use string concatenation.
3. **No `const` in loop initializers** — Use `let` instead.
4. **No new globals on `gv.*`** — Use `AppContext` or `ServiceContainer` for new state.
5. **No `gv.signalMgr` in new code** — Use `gv.bus` (EventBus).
6. **No extending old `BaseGUI`** — Use new `BaseScene` (cc.Layer) for new scenes.

### Two Coexisting Architectures

| Aspect | Legacy (old code) | New (refactored) |
|--------|-------------------|------------------|
| Events | `gv.signalMgr`, `fr.event` | `gv.bus` (EventBus) |
| DI | Global singletons on `gv.*` | `ServiceContainer` |
| State | `gv.*` globals | `AppContext` |
| Modules | `BaseModule.extend({})` | New `BaseModule` with transport injection |
| Scenes | Legacy GuiMgr + Layer stack | `BaseScene` (cc.Layer) |
| Boot | Sequential init | `BootGraph` (topological dependency sort) |

**Rule: New code ALWAYS uses the new architecture.**

### Key Paths

```
clientccn2/
├── main.js                                # Boot entry point (BootSetup → BootGraph)
├── project.json                           # Cocos build config (jsListOrder)
├── package.json                           # npm scripts, Jest config
├── src/
│   ├── common/
│   │   └── MSerializer.js                 # Auto-generated from server KSP
│   ├── config/
│   │   ├── GlobalVar.js                   # Global constants
│   │   ├── BuildConfig.js                 # Build mode
│   │   └── Cheat.js                       # Cheat flags
│   ├── events/
│   │   ├── EventBus.js                    # gv.bus — new event system (327 lines)
│   │   └── EventKeys.js                   # 59+ documented event keys (15 categories)
│   ├── framework/
│   │   ├── core/
│   │   │   ├── ServiceContainer.js        # Dependency injection
│   │   │   ├── AppContext.js              # State management
│   │   │   ├── ErrorHandler.js            # Error handling
│   │   │   ├── ResourcePool.js            # Resource pooling
│   │   │   ├── UnifiedLocalization.js     # Localization
│   │   │   └── CoreServices.js            # Boot services registry
│   │   ├── animations/                    # Animation managers
│   │   ├── network/                       # Connector, SerializerPacket, MockAPI
│   │   ├── platforms/                     # NotificationMgr, PlatformUtils, Sentry
│   │   ├── plugins/                       # Social logins, IAP, Analytics
│   │   ├── ui/                            # BaseGUI, BaseScene, SceneMgr, GuiMgr, Dialog
│   │   │   └── extension/                 # hasEventBus, UIListener, delayCallback
│   │   ├── utility/                       # ActionUtil, Crypt, EffectUtils, TimeFormat, etc.
│   │   └── webService/                    # AppService, ServicesMgr
│   ├── gui/                               # Legacy GUI panels (battle_pass, daily_reward, etc.)
│   ├── modules/
│   │   ├── common/
│   │   │   ├── BaseModule.js              # Legacy module base
│   │   │   ├── BaseCmd.js                 # Base command handler
│   │   │   ├── ModuleMgr.js               # Module registry & message routing
│   │   │   ├── EventHub.js / EventKey.js  # Legacy event constants
│   │   │   └── PingModule.js              # Keep-alive ping
│   │   ├── config/
│   │   │   ├── ConfigManager.js           # Central config loader
│   │   │   ├── BaseConfig.js              # Base config class
│   │   │   ├── BoardConfig.js, CardConfig.js, CharacterConfig.js
│   │   │   ├── GameConfig.js, ItemConfig.js, PassiveConfig.js
│   │   │   ├── GachaConfig.js, LeagueConfig.js, BattlePassConfig.js
│   │   │   └── constants/                 # CardConstant, ColorConst, Constants, ItemConst, etc.
│   │   ├── game/
│   │   │   ├── GameModule.js              # Legacy game module handler
│   │   │   ├── GameAPI.js                 # Game API endpoint
│   │   │   ├── GameConst.js               # Game constants
│   │   │   ├── logic/
│   │   │   │   ├── Game.js                # Main game state model (26KB)
│   │   │   │   ├── Player.js              # Player data model (12KB)
│   │   │   │   ├── Character.js, PlayerInfo.js, RoundEventObject.js
│   │   │   │   ├── ActionType.js          # Action type constants
│   │   │   │   ├── board/
│   │   │   │   │   ├── Board.js           # Board state (tiles + tokens)
│   │   │   │   │   ├── Tile.js, Token.js, Dice.js, Deck.js
│   │   │   │   ├── action/                # 30+ action types (8 categories)
│   │   │   │   │   ├── BaseAction.js      # Abstract action base
│   │   │   │   │   ├── ActionQueue.js     # Phase-based queue processor
│   │   │   │   │   ├── ActionGainDiamond, ActionDropDiamond, ActionStealDiamond...
│   │   │   │   │   ├── ActionJail, ActionFreeze, ActionKickAss, ActionTeleport...
│   │   │   │   │   └── ActionUseCard, ActionBuffLadderPoint, ActionExtraTurn...
│   │   │   │   ├── skill/                 # Skill system (BaseSkill + cast-on effects)
│   │   │   │   ├── passive/               # 9 passive action types
│   │   │   │   └── round_event/           # 7 round event action types
│   │   │   └── ui/                        # Game UI components
│   │   │       ├── GameHUD.js             # Main HUD controller
│   │   │       ├── SceneGame.js           # Main game scene
│   │   │       ├── board/                 # PlayerUI, TokenUI, TileUI, GuiCard, DiceResult
│   │   │       ├── skill/                 # NodeCardInGame, NodeSkillCard, NodeCastOnPlayer
│   │   │       ├── dice/                  # DiceRoll, LayerDice3D
│   │   │       ├── end_game/              # GuiEndGame, EndGameResult
│   │   │       ├── history/               # GuiHistory
│   │   │       ├── passive/               # NodePassiveInfo
│   │   │       ├── popup/                 # Alerts, ProfileIngame
│   │   │       └── round_event/           # RoundEventHud, PopupUpRankCard
│   │   ├── chat/                          # 35+ files — WorldChatMgr, ChatIconMgr, Observable
│   │   ├── shop/                          # ShopModule + gacha/ subdirectory (GachaModule)
│   │   ├── tutorial/                      # TutorialModule, StepEngine, 40+ tutorial configs
│   │   ├── matching/                      # MatchingModule, SceneMatching
│   │   ├── login/                         # LoginModule, SceneLogin, SocialMgr
│   │   ├── league/                        # LeagueModule + UI
│   │   ├── mail/                          # MailModule
│   │   ├── quest/                         # QuestModule
│   │   ├── pm/                            # PaymentModule
│   │   ├── battle_pass/                   # BattlePassModule
│   │   ├── user/                          # UserModule
│   │   ├── cheat/                         # CheatModule (dev only)
│   │   ├── consumable/                    # ConsumableModule
│   │   ├── daily_reward/                  # DailyRewardModule
│   │   ├── offer/                         # OfferModule
│   │   ├── level/                         # LevelModule
│   │   ├── skill_tool/                    # SkillToolModule
│   │   └── hot_news/                      # HotNewService
│   ├── resources/                         # ResourcesMgr, RefCountedLoader, AudioMgr
│   ├── utils/                             # CardUtils, ItemUtil, DiceUtil, EffectMgr
│   ├── navigation/                        # NavigationCoordinator — scene state machine
│   ├── scenes/                            # New BaseScene subclasses
│   ├── network/                           # INetworkTransport, ConnectorAdapter
│   ├── domain/                            # Pure game model (Board, Player, Token, ActionQueue)
│   │   └── actions/                       # New action types (post-refactor)
│   └── SignalMgr.js                       # Legacy event signal manager
├── res/
│   └── config/                            # 44 JSON config files
│       ├── Board.json, Game.json, Card.json, Passive.json
│       ├── Characters.json, CharacterUpgrade.json
│       ├── Item.json, ItemGroup.json (generated from server)
│       ├── Gacha*.json, BattlePass.json, League.json
│       ├── Payment*.json, ShopExchange.json
│       ├── StateTime.json, ActionTime.json
│       ├── Tut*.json (40+ tutorial configs)
│       └── ...
├── tests/
│   ├── setup.js                           # Global mock setup (gv, fr, connector, etc.)
│   ├── mocks/cc-mock.js                   # Cocos2d-x API stubs for Jest
│   ├── framework/core/                    # ServiceContainer.test.js, AppContext.test.js
│   ├── events/EventBus.test.js
│   └── modules/                           # Game logic, gacha, login, user tests
└── tools/
    └── eslint-rules/                      # Custom rules + globals scanner
```

### Global Namespaces & Singletons

| Global | Purpose |
|--------|---------|
| `gv` | Game globals namespace (writable) |
| `fr` | Framework namespace (Cocos wrappers, SDKs) |
| `sp` | Spine animation namespace |
| `cc` | Cocos2d-x engine |
| `connector` | Network connection manager |
| `resourceMgr` | Asset loader |
| `servicesMgr` | Web service manager |
| `sceneMgr` | Scene state machine |
| `moduleMgr` | Module registry & message routing |
| `gv.bus` | New EventBus |
| `gv.signalMgr` | Legacy SignalMgr |
| `gv.guiMgr` | GUI panel manager |
| `gv.poolObjects` | Object pooling |
| `SHADERS` | 9 compiled GLSL shaders |

### Boot Flow

```
main.js → BootSetup.boot() → BootGraph (topological dependency sort)
→ services initialized in layers → SceneFactoryNew maps scene IDs
→ startGame() → sceneMgr.viewSceneById(LOADING)
```

Scene IDs: `0=LOADING, 1=LOGIN, 2=MAINTAIN, 3=LOBBY, 4=GAME, 5=MATCHING, 6=LOADING_IN_GAME`

### Action Flow (Network → UI)

```
Server packet → GameModule.handleXxx()
  → Game.queueAction(action)
    → ActionQueue.queueAction(action)
      → ActionQueue.processNextAction()
        → action.action()        [business logic]
          → gv.bus.emit(EventKeys.XXX)  [UI update]
            → action.doneAction()      [complete]
              → EventKey.COMPLETE_ACTION [next]
```

### Layer Z-Order (gv.LAYERS)

`BG=0, GAME=1, EFFECT=2, MOVE=3, GUI=4, GUI_EFFECT=5, GUI_TUTORIAL=6, GUI_LEVEL_UP=7, DIALOG=8, GUI_DAILY_REWARD=9, LOADING=10, LAYER_USER_ACTION=11`

### Design Patterns

| Pattern | Where | Details |
|---------|-------|---------|
| Module | `modules/*/` | BaseModule + command handler + API |
| Event Bus | `events/EventBus.js` | `gv.bus.on/off/emit` with 59+ documented events |
| Action Queue | `game/logic/action/` | Phase-based sequential effect processing |
| DI Container | `framework/core/ServiceContainer.js` | New code dependency injection |
| State Machine | `navigation/NavigationCoordinator.js` | Scene transitions |
| Factory | `framework/ui/SceneFactory.js` | Scene ID → Scene class mapping |
| Object Pool | `framework/core/ResourcePool.js` | Sprite/node recycling |
| Observer | `modules/chat/Observable.js` | Chat system pub/sub |
| Mixin | `framework/ui/extension/` | `hasEventBus`, `UIListener`, etc. |

### Key Documents

| Document | Path | Purpose |
|----------|------|---------|
| Game Design Document | `clientccn2/document/GameDesignDocument.md` | Authoritative game rules |
| Technical Architecture | `clientccn2/document/TechnicalArchitectureDocument.md` | Architecture analysis (16 sections) |
| Client CLAUDE.md | `clientccn2/CLAUDE.md` | Client conventions & constraints |
| Root CLAUDE.md | `CLAUDE.md` | Build commands, project layout |

> **Deep reference**: Read `references/tech-arch-summary.md` for CMD ID ranges, action categories, event categories, data flow diagrams, domain object mapping, module registry, and known technical debt. Use when working on network, actions, events, or architecture.

### Config Files (res/config/) — 44 files

| Category | Files |
|----------|-------|
| Board & Game | Board.json, Game.json, StateTime.json, ActionTime.json |
| Cards & Skills | Card.json, SkillCardUpgrade.json, ComboSkillCard.json |
| Characters | Characters.json, CharacterUpgrade.json |
| Items | Item.json, ItemGroup.json (generated from server) |
| Passive | Passive.json |
| Gacha | Gacha.json, GachaBanners.json, GachaPools.json, GachaBannerRates.json |
| Economy | PaymentChannels.json, PaymentPacks.json, ShopExchange.json, Subsidy.json |
| Progression | PlayerLevels.json, BattlePass.json, League.json |
| Quests | BeginnerQuests.json, LevelQuests.json, TimedQuest.json |
| Events | RoundEvent.json |
| Matching | Matching.json |
| Tutorial | Tut*.json (40+ files) |
| Other | Initial.json, ConsumableBooster.json, AccumulateGacha.json |

### Build & Test Commands

```bash
npm test                    # All Jest tests
npx jest path/to/test.js    # Single test file
npm run lint                # ESLint on src/**/*.js
npm run lint:fix             # Auto-fix lint issues
npm run lint:global          # Re-scan globals + lint (after adding new global files)
npm run format               # Prettier on src + tests
npm run scan-resources       # Scan used resources
```

---

## Commands

### 1. `scan_client`

**Purpose:** Build comprehensive mental model of the client project.

Steps:
1. Read `clientccn2/CLAUDE.md` for conventions and constraints
2. Read `clientccn2/document/GameDesignDocument.md` for game rules
3. Scan source structure:
   - `src/modules/` — module inventory (25+ modules)
   - `src/modules/game/logic/` — game model + 30+ action types
   - `src/modules/game/logic/action/` — ActionQueue pipeline
   - `src/events/EventKeys.js` — event catalog (59+ documented events, 15 categories)
   - `src/framework/core/` — DI, state, error handling
   - `src/modules/config/` — config loaders (18 configs)
4. Inventory `res/config/` — 44 JSON config files
5. Check dual architecture status (legacy vs new code ratio)
6. Produce structured summary:
   - Module inventory table
   - Action type catalog
   - Event keys catalog
   - Legacy vs new code assessment
   - Inconsistencies or migration gaps
7. **Save findings to memory**

### 2. `generate_client_tech_doc`

**Purpose:** Generate or update client-specific technical documentation.

> Reference: existing Tech Doc at `clientccn2/document/TechnicalArchitectureDocument.md` (16 sections). Read it first; update or regenerate as needed.

Steps:
1. Run `scan_client` if not done this session
2. Read core source files deeply:
   - `main.js` — boot sequence
   - `ServiceContainer.js`, `AppContext.js` — new architecture
   - `Game.js`, `Board.js`, `Player.js` — domain model
   - `ActionQueue.js`, `BaseAction.js` — action system
   - `EventBus.js`, `EventKeys.js` — event system
   - `GameModule.js`, `GameHUD.js` — game module + UI
   - `ConfigManager.js` — config loading
3. Document sections covering:
   - Boot flow (BootGraph + dependency sort)
   - Dual architecture (legacy vs new)
   - Domain model (Game, Board, Token, Player, Tile, Deck)
   - Action queue pipeline (phases, interrupts, nested actions)
   - Event system (EventBus vs SignalMgr vs ClientEventHub)
   - Module system (BaseModule + ModuleMgr)
   - Scene system (NavigationCoordinator + SceneFactory)
   - UI architecture (BaseScene, BaseGUI, GameHUD, Layer Z-order)
   - Network protocol (Connector + MSerializer)
   - Config system (ConfigManager + 18 loaders)
   - Asset pipeline (resource tiers, RefCountedLoader, sprite sheets)
   - Testing (Jest + cc-mock + setup.js)
4. Present draft to user for review
5. Write to file only after approval

### 3. `edit_client_idea`

**Purpose:** Collaboratively refine a client feature idea before any code is written.

Steps:
1. Extract the idea from conversation context
2. Read relevant GDD sections
3. Analyze against:
   - **Architecture fit**: Legacy or new architecture? Which pattern?
   - **Action system**: Does it need new ActionQueue actions?
   - **Event system**: New EventKeys needed? What emits/listens?
   - **UI components**: New scenes, HUD elements, popups?
   - **Config**: New JSON configs? ConfigManager changes?
   - **Network**: New packet handlers? MSerializer impact?
   - **Cross-project**: Server changes needed? Config sync?
   - **JSB compatibility**: Template literals? Const in loops?
   - **Performance**: Object pooling? Sprite sheet management?
4. Present structured review:
   - **Summary**: What the idea adds/changes
   - **Impact Analysis**: Modules, actions, events, UI affected
   - **Architecture Decision**: Legacy extend or new architecture
   - **Risks**: JSB compat, performance, migration complexity
   - **Affected Files**: Specific paths in clientccn2/
   - **Estimated Scope**: Small (1-3 files) / Medium (4-10) / Large (11+)
5. Iterate with user until refined
6. When approved, suggest: `update_gdd` → `generate_client_code`

### 4. `manage_actions`

**Purpose:** Create, modify, or review game actions in the ActionQueue system.

Steps:
1. Read `ActionQueue.js` and `BaseAction.js` for current patterns
2. Read `references/tech-arch-summary.md` → "Action Type Categories" for full catalog
3. Inventory all 30+ existing action types across 8 categories:
   Movement, Economy, Status, Combat, Cards, Cast-On, Round Events, Passives
4. For new action:
   - Extend `BaseAction` (lifecycle: `action()` → `doAction()` → `doneAction()` → `destroy()`)
   - Override `doAction()` for business logic
   - Call `gv.bus.emit()` for UI updates
   - Call `doneAction()` on completion (with delay for animations)
   - Register in `ActionType.js` if needed
   - Determine correct `TriggerPhase`
4. For modifying existing action:
   - Read target action file
   - Understand its role in the phase pipeline
   - Identify downstream listeners (EventKeys)
   - Present changes with impact analysis
5. Verify action integrates correctly with:
   - `Game.queueAction()` — entry point
   - `ActionQueue.processNextAction()` — processing
   - Related UI components that listen to events
6. Create/update tests

### 5. `manage_events`

**Purpose:** Create, modify, or audit the event system.

Steps:
1. Read `EventBus.js` and `EventKeys.js`
2. Read `references/tech-arch-summary.md` → "Event Categories" for the 15-category breakdown
3. Inventory all 59+ documented events with their emitters and listeners
3. For new event:
   - Add key to `EventKeys.js`
   - Document: who emits, who listens, payload shape
   - Use `gv.bus.emit()` in new code (never `gv.signalMgr`)
4. For event audit:
   - Grep all `gv.bus.emit` calls — match with EventKeys
   - Grep all `gv.bus.on` calls — match with handlers
   - Find orphaned events (emitted but never listened)
   - Find dead listeners (listening but never emitted)
   - Report legacy `gv.signalMgr` usage that could be migrated
5. Build event flow diagram for specified feature

### 6. `manage_modules`

**Purpose:** Create or modify client modules.

#### 6a. New module (new architecture)
Steps:
1. Create module file extending new `BaseModule` with transport injection
2. Create API file for network commands
3. Create UI files extending `BaseScene` (cc.Layer)
4. Register events on `gv.bus`
5. Register in `BootSetup.js` with `deps: [...]`
6. Add ESLint globals: run `npm run lint:global`

#### 6b. New module (legacy extension — avoid if possible)
Steps:
1. Create module extending `BaseModule.extend({})`
2. Register in `ModuleMgr`
3. Create command handlers extending `BaseCmd`
4. Create GUI panels extending `BaseGUI`

#### 6c. Module audit
Steps:
1. Inventory all modules with their architecture type
2. Check for legacy modules that should be migrated
3. Verify module registration (ModuleMgr or BootSetup)
4. Check for orphaned modules (registered but unused)

### 7. `manage_configs`

**Purpose:** Manage client config loaders and JSON config files.

Steps:
1. Read `ConfigManager.js` for loading patterns
2. For new config:
   - Create config loader extending `BaseConfig` in `modules/config/`
   - Create JSON file in `res/config/`
   - Register in `ConfigManager.js`
   - If config comes from server: coordinate with server-side `GameCfg`
3. For config audit:
   - Compare `res/config/` files with server `res/` files
   - Check for stale or unused configs
   - Verify all loaders match JSON schema

### 8. `check_client_consistency`

**Purpose:** Verify GDD ↔ Client Code ↔ Config alignment.

Steps:
1. Read GDD — extract client-relevant rules and constants
2. Scan client source code:
   - `res/config/Board.json` — board constants
   - `res/config/Game.json` — game settings
   - `modules/game/GameConst.js` — client enums
   - `modules/game/logic/Player.js` — `isOpenGate()` threshold
   - `modules/game/logic/board/Board.js` — tile count, pathfinding
3. Build consistency matrix:

| Rule | GDD (v2.0) | Client Config | Client Code | Status |
|------|-----------|--------------|-------------|--------|
| Main track tiles | **44** | Board.json:`mainTrack` len? | Board.js array? | ? |
| Win DIAMOND | **600** (`pointOpenGate`) | Board.json:`pointOpenGate`? | Player.js:`isOpenGate()`? | ? |
| Tokens per player | **2** (`tokensPerPlayer`) | Board.json:? | Player.js:? | ? |
| Kick steal | **1%** (`percentCoinKick`) | Board.json:? | kick logic:? | ? |
| Extra turns max | **1** (`maxExtraPerTurn`) | Board.json:? | dice logic:? | ? |
| Card hand max | **5** (`numCardMax`) | Board.json:? | Deck.js:? | ? |
| Starting cards | **3** (`numCardInit`) | Board.json:? | Deck.js:? | ? |
| Safe zone tiles | 1, 11, 21, 31 | Board.json tiles? | Tile.js type? | ? |
| Tile types | SAFE_ZONE, REWARD, EMPTY, LADDER | Board.json type enums? | GameConst.js? | ? |
| Action phases | 10 TriggerPhases | — | ActionQueue.js? | ? |
| Passive types | 7 | Passive.json? | passive/ dir? | ? |
| Round events | 6 | RoundEvent.json? | round_event/ dir? | ? |

4. Cross-reference with server code if needed
5. Report mismatches with severity levels
6. Special attention:
   - `Player.isOpenGate()` — must use **600 DIAMOND** threshold (not 300)
   - Board tile count — must be **44** main track tiles (not 40)
   - Tile type names — must match GDD: `SAFE_ZONE`, `REWARD`, `EMPTY`, `LADDER`

### 9. `generate_client_code`

**Purpose:** Generate client code from an approved, documented design.

Prerequisites: Feature MUST be documented in GDD first.

Steps:
1. Read the approved design from documents
2. Identify target files and modules
3. Read ALL target files to understand current patterns
4. Follow client patterns strictly:
   - **New action**: Extend `BaseAction`, register in `ActionType.js`, add to `ActionQueue`
   - **New module**: New `BaseModule` with DI, register in `BootSetup.js`
   - **New scene**: Extend `BaseScene`, add to `SceneFactory`, add Scene ID
   - **New UI**: Use `gv.bus.on()` for events, respect Layer Z-order
   - **New config**: Extend `BaseConfig`, register in `ConfigManager`
   - **Events**: Add to `EventKeys.js`, use `gv.bus.emit()`
5. **JSB compatibility check**: No template literals, no const in loops
6. Plan implementation — present file list with approach
7. After user approval, generate code
8. Run `npm run lint:global` if new global files added
9. Create/update tests in `tests/` mirroring `src/` structure
10. If server packets involved, remind to check MSerializer.js sync

### 10. `refactor_client`

**Purpose:** Refactor client code, especially legacy → new architecture migration.

Steps:
1. Run `scan_client` to understand current state
2. Identify refactoring scope:
   - Legacy → new architecture migration
   - Event system migration (`gv.signalMgr` → `gv.bus`)
   - Module migration (`BaseModule.extend` → new `BaseModule`)
   - UI migration (`BaseGUI` → `BaseScene`)
3. For event migration:
   - Ensure both old and new systems work during transition
   - Map legacy signal names to EventKeys equivalents
   - Update listeners incrementally
4. Present refactoring plan: before/after per file
5. Execute after approval
6. Run `npm run lint:global` after refactoring
7. Run `npm test` to verify nothing broke
8. Update `clientccn2/CLAUDE.md` if architecture docs need update

### 11. `manage_ui`

**Purpose:** Create or modify UI components and scenes.

Steps:
1. Identify component type:
   - **Scene**: Extend `BaseScene`, register in `SceneFactory`
   - **HUD element**: Add to `GameHUD.js`, use correct Z-order layer
   - **Popup/Dialog**: Use `Dialog.js` or extend `BaseGUI` (legacy)
   - **Game board element**: Add to `board/` subdirectory
2. Read existing similar components for pattern matching
3. Follow UI conventions:
   - Use `gv.bus.on()` for event listening in new code
   - Use `hasEventBus` mixin for auto-cleanup
   - Respect `gv.LAYERS` Z-order constants
   - Use `ResourcePool` for frequently created/destroyed nodes
   - Load sprite sheets per-scene, unload on exit
4. Handle asset tier transparency (`low/`, `high/`, `ultra/`)
5. Test with cc-mock in Jest

### 12. `validate_result`

**Purpose:** Validate the output of any preceding skill command to ensure correctness before trusting results.

**Trigger:** Runs automatically after every other command. Can also be invoked manually.

Steps:
1. Identify which command just completed and its output type:
   - **Scan/Analysis** → verify counts, file paths, categories
   - **Documentation** → verify sections, code examples, GDD alignment
   - **Code Generation** → verify lint, JSB, tests, registration, patterns
   - **Refactoring** → verify tests before/after, lint, migration progress
2. Run **automated checks** (see `references/validation.md` for command-specific checks):
   ```bash
   # Core automated suite (always run)
   npm run lint 2>&1 | tail -5                    # Lint
   npm test 2>&1 | tail -10                       # Tests
   grep -rE '`[^`]*\$\{' <generated_files>       # JSB: no template literals
   grep -rE 'for\s*\(\s*const\s' <generated_files> # JSB: no const-in-loop
   grep -rE '^\s*import\s' <generated_files>      # JSB: no ES6 imports
   ```
3. Run **spot-checks** (pick 3 random items from output):
   - Verify file paths exist
   - Verify counts match actual codebase
   - Verify code examples follow project patterns
4. Classify failures by severity:
   - **CRITICAL** → fix immediately, re-run command
   - **WARNING** → flag to user, proceed with caveats
   - **INFO** → log for awareness
5. Generate **Validation Report**:
   ```
   ## Validation Report — {command_name}
   | # | Check | Result | Severity |
   |---|-------|--------|----------|
   | 1 | Lint passes | PASS | — |
   | 2 | JSB compat  | PASS | — |
   | ...
   **Overall: PASS / FAIL**
   ```
6. Decision:
   - All PASS → proceed, save to memory
   - WARNING only → proceed with caveats noted
   - Any CRITICAL → stop, fix, re-validate
   - Multiple CRITICAL → re-run entire command from scratch

---

## Workflow Rules

These rules apply to ALL commands:

1. **Read before write.** Always read existing source files before modifying them.

2. **Document before code.** Change order:
   - GDD first (if game rules change)
   - Tech Doc second (if architecture changes)
   - Code last

3. **User approval at every gate.** Present drafts and plans before writing.

4. **New code = new architecture.** Never extend legacy patterns for new features:
   - Use `gv.bus`, not `gv.signalMgr`
   - Use `ServiceContainer`, not `gv.*` globals
   - Use `BaseScene`, not `BaseGUI`
   - Use new `BaseModule` with DI, not `BaseModule.extend({})`

5. **JSB compatibility.** Every code change must pass:
   - No template literals (string concatenation only)
   - No `const` in loop initializers (use `let`)
   - No ES6 modules (script globals only)

6. **Lint after globals.** Run `npm run lint:global` after adding new globally-scoped files.

7. **Cross-project awareness.** Client changes may require:
   - MSerializer.js regeneration (run `./gradlew run` in serverccn2/)
   - Config JSON sync with server `res/`
   - Server validation for any game rule changes

8. **Test new code.** Create Jest tests in `tests/` mirroring `src/` structure. Use `cc-mock.js` and `setup.js` for Cocos API stubs.

9. **Save to memory.** After completing a command, save key findings to memory files.

10. **Validate every output.** After every command, run `validate_result` automatically:
    - Automated checks: lint, JSB compat, tests, counts, file paths
    - Spot-checks: 3 random items verified against actual codebase
    - Severity classification: CRITICAL (fix now), WARNING (flag), INFO (log)
    - CRITICAL failures block proceeding until fixed
    - See `references/validation.md` for command-specific validation checks

---

## Response Format

- Tables for module inventories, action catalogs, event maps
- Bullet lists for action items and recommendations
- Code blocks for file paths, commands, and snippets
- Section headers for multi-part responses
- Always state which command is executing and current step
- For multi-command flows, state the pipeline upfront:
  > "Pipeline: `edit_client_idea` → `update_gdd` → `generate_client_code`"
- Flag JSB compatibility issues with `[JSB]` badge
- Flag legacy vs new arch with `[LEGACY]` / `[NEW]` badges

## Quick Decision Guide

| User Request | Command(s) |
|---|---|
| "Scan the client" | `scan_client` |
| "Generate client tech doc" | `generate_client_tech_doc` |
| "Add a new card effect" | `edit_client_idea` → `manage_actions` → `generate_client_code` |
| "Add new event" | `manage_events` |
| "Create new module" | `manage_modules` (6a) |
| "Audit events" | `manage_events` (audit) |
| "Add new config" | `manage_configs` |
| "Is client code matching GDD?" | `check_client_consistency` |
| "Migrate X to new architecture" | `refactor_client` |
| "Add new popup/UI" | `manage_ui` |
| "Add new scene" | `manage_ui` → `manage_modules` |
| "What actions exist?" | `manage_actions` (inventory) |
| "Refactor event system" | `refactor_client` |
| "Validate last output" | `validate_result` |
| "Check if scan is correct" | `validate_result` |
