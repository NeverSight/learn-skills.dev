---
name: cocos-vscene
description: |
  Use when working with Cocos Creator scenes and needing to query, browse, analyze, map, or optimize scene node structures. Triggers on "vscene" commands or Chinese equivalents: 拉取场景索引, 读取场景, 分析场景, 审查场景, 场景地图, 优化场景. Also triggers on scene node lookup, scene quality scoring, scene hierarchy review, or scene structure mapping needs.

  Keywords: vscene, scene index, scene cache, node lookup, Cocos Creator, scene analysis, quality score, scene map, node annotation, hierarchy optimization, progressive loading
---

# Cocos VScene - Scene Index & Analysis System

## Design Philosophy

**VScene = Index (索引) + Map (地图) + Analysis (分析)**

```
┌──────────────────────────────────────────────────────────────────────────┐
│                           VScene System                                  │
├──────────────────────┬──────────────────────┬────────────────────────────┤
│  Index Layer (索引层) │  Map Layer (地图层)   │   Analysis Layer (分析层)   │
├──────────────────────┼──────────────────────┼────────────────────────────┤
│ • Fast lookup        │ • Key node extract   │ • Structure quality score  │
│ • Node/Component     │ • Bilingual annotate │ • Code-scene relations     │
│ • Offline capable    │ • Smart collapse     │ • Module identification    │
│ • Minimal context    │ • Human+AI readable  │ • Self-check & iteration   │
└──────────────────────┴──────────────────────┴────────────────────────────┘
```

| Principle | Description |
|-----------|-------------|
| Index only | Store name, path, component types - NOT property values |
| Query on demand | Fetch details via MCP when needed |
| Progressive load | Load large scenes in layers |
| AI friendly | Minimal structure for fast lookup |
| Quality scoring | Rate structure and code-scene relations |
| Self-iterating | Support review and improvement suggestions |

---

## Commands

| Command | MCP | Description |
|---------|-----|-------------|
| `vscene pull` | ✅ | Build/update index from editor |
| `vscene read [--depth N]` | ❌ | Read from cache (default depth: 3) |
| `vscene find <pattern>` | ❌ | Search nodes by name/type |
| `vscene detail <uuid>` | ✅ | Get full node properties |
| `vscene diff` | ✅ | Compare index vs real scene |
| `vscene status` | ❌ | View index status |
| `vscene analyze` | ✅ | **Generate quality analysis with scoring** |
| `vscene review` | ❌ | **Self-check analysis, suggest improvements** |
| `vscene map` | ❌* | **Generate annotated scene map with bilingual comments** |
| `vscene pretty` | ✅ | **Analyze hierarchy, propose & execute optimizations** |

_* Offline if index exists; auto-pulls (requires MCP) if no index available._

---

## Directory Structure

```
.vscene/
├── manifest.json                    # Scene manifest (场景清单)
├── scenes/
│   └── {sceneName}.json             # Scene index (场景索引)
├── maps/
│   └── {sceneName}.map.md           # Scene map (场景地图)
└── analysis/
    └── {sceneName}.analysis.md      # Quality analysis (质量分析)
```

---

## Index Layer (索引层)

### VNode Format (Enhanced)

```json
{
  "u": "uuid",
  "n": "NodeName",
  "c": ["GameManager", "AudioSource"],
  "k": true,
  "d": 0,
  "role": "logic",
  "desc": "游戏逻辑根节点",
  "_": []
}
```

| Field | Full name | Description |
|-------|-----------|-------------|
| `u` | uuid | Node UUID |
| `n` | name | Node name |
| `c` | components | Component type names (excludes cc.* engine) |
| `k` | key | Is key node (has important components) |
| `d` | depth | Hierarchy depth |
| `role` | role | _(planned)_ Node role: `logic`/`ui`/`render`/`data`/`container` |
| `desc` | description | _(planned)_ One-line description (中文) |
| `_` | children | Child nodes array |

### Node Role Classification

| Role | Description | Examples |
|------|-------------|----------|
| `logic` | Business logic, controllers | GameManager, PlayerController |
| `ui` | User interface elements | Canvas, Button, Label |
| `render` | Visual elements only | MeshRenderer, Sprite (no script) |
| `data` | Data containers | ConfigNode, AssetsNode |
| `container` | Organizational grouping | Managers, World, UI |

---

## Map Layer (地图层)

### map Command (Scene Map Generator)

**Purpose**: Generate a navigable, annotated scene map that both humans and AI can quickly understand. Unlike `read` (full tree dump), `map` extracts only the structural skeleton and key nodes, with bilingual (EN/ZH) annotations.

**Output**: `.vscene/maps/{sceneName}.map.md`

**MCP**: ❌ offline if index exists, auto-pulls if not (then needs MCP)

```
vscene map
  │
  ├─ Step 1: Load Index
  │   └─ If no index → auto pull (requires MCP)
  │
  ├─ Step 2: Filter Nodes (节点筛选)
  │   ├─ Keep all nodes at depth 0-1 (top-level skeleton)
  │   ├─ Keep all key nodes (k=true) at any depth
  │   ├─ Keep ancestor containers of key nodes (path completeness)
  │   ├─ Collapse repeated siblings (Enemy1~10 → [×10 Enemy*])
  │   └─ Aggregate decoration leaves (→ [... N nodes])
  │
  ├─ Step 3: Generate Annotations (注释生成)
  │   ├─ Component-based inference (GameManager → Core game controller / 核心游戏控制器)
  │   ├─ Name-based translation (Player → Player character / 玩家角色)
  │   ├─ Container inference from children (3 Buttons → Button group / 按钮组)
  │   └─ Mark ambiguous names with [?] (weilan → ? / 围栏? [?])
  │
  ├─ Step 4: Render Map Document (渲染地图文档)
  │   ├─ Header: scene info, stats, generation time
  │   ├─ Node Map: annotated tree with smart collapse
  │   ├─ Legend: symbol explanations
  │   ├─ Quick Reference: flat table of key nodes (path/components/purpose)
  │   └─ Stats: total nodes, key nodes shown, collapsed groups
  │
  └─ Output: .vscene/maps/{sceneName}.map.md
```

#### Command Variants

```bash
vscene map                # Generate map (auto-pull if no index)
vscene map --refresh      # Force regenerate (overwrites existing map)
```

#### Node Filtering Rules (节点筛选规则)

| Priority | Rule | Description |
|----------|------|-------------|
| 1 | Depth 0-1 | All top-level nodes kept (scene skeleton) |
| 2 | Key nodes | Nodes with `k=true` kept at any depth |
| 3 | Custom components | Nodes with non-engine components kept |
| 4 | Ancestor containers | Parent nodes of kept nodes preserved (path integrity) |
| 5 | Repeated siblings | Same-prefix siblings collapsed: `[×N Pattern*]` |
| 6 | Decoration leaves | Remaining leaf nodes aggregated: `[... N nodes]` |

**Collapse detection for repeated siblings:**

```
Detect pattern: ≥3 siblings sharing a common prefix (case-insensitive)
  Enemy1, Enemy2, Enemy3 → [×3 Enemy*]
  Zone_Oven, Zone_Helper, Zone_Fish → [×3 Zone_*]
  tree, tree (1), tree (2) → [×3 tree*]
```

#### Annotation Inference Rules (注释推断规则)

AI generates bilingual `# EN / 中文` annotations using 4 strategies (priority order):

1. **Component match** → `GameManager` → `Game manager / Game管理器`
2. **Ambiguous detection** → `node1` → `unnamed / 未命名 [?]` (checked early to prevent bad translations)
3. **Name translation** → `Player` → `Player / 玩家`
4. **Container inference** → children are all Buttons → `Button group / 按钮组`

Full mapping tables: see [references/annotation-rules.md](references/annotation-rules.md)

#### Map Output Template

See [references/map-template.md](references/map-template.md) for the full output template.

**Key sections:**
1. **Header** — Scene name, generation time, node count summary
2. **Node Map** — Annotated tree with inline `# EN / 中文` comments
3. **Legend** — Symbol meanings (★, [×N], [...], [?])
4. **Quick Reference** — Flat table of key nodes with path, components, purpose
5. **Stats** — Total/shown/collapsed node counts

---

## Analysis Layer (分析层)

### analyze Command Flow

```
vscene analyze
  │
  ├─ Step 1: Check/Load Index
  │   └─ If no index → auto pull
  │
  ├─ Step 2: Structure Analysis (结构分析)
  │   ├─ Hierarchy depth analysis
  │   ├─ Node naming conventions
  │   ├─ Module organization
  │   └─ Component distribution
  │
  ├─ Step 3: Code-Scene Relation Analysis (代码-场景关系分析)
  │   ├─ Grep: getChildByName / find patterns
  │   ├─ Grep: getComponent patterns
  │   ├─ Match code references to scene nodes
  │   └─ Identify missing/orphan references
  │
  ├─ Step 4: Quality Scoring (质量评分)
  │   ├─ Structure Score (结构分)
  │   ├─ Naming Score (命名分)
  │   ├─ Code-Scene Coupling Score (耦合分)
  │   └─ Overall Score (总分)
  │
  ├─ Step 5: Generate Issues & Suggestions (问题与建议)
  │   ├─ Critical issues (严重��题)
  │   ├─ Warnings (警告)
  │   └─ Improvement suggestions (改进建议)
  │
  └─ Output: .vscene/analysis/{sceneName}.analysis.md
```

### Quality Scoring System (评分体系)

**Total Score: 100 points**

| Dimension | Weight | Criteria |
|-----------|--------|----------|
| **Structure (结构)** | 30 | Hierarchy depth, module organization, node grouping |
| **Naming (命名)** | 20 | Consistent naming, semantic clarity, no magic names |
| **Code-Scene (代码-场景)** | 30 | Clean references, no hardcoded paths, proper coupling |
| **Maintainability (可维护性)** | 20 | Component reuse, prefab usage, separation of concerns |

#### Scoring Rules

**Structure Score (30 points)**

| Rule | Points | Deduction |
|------|--------|-----------|
| Max depth ≤ 6 | +10 | -2 per level over 6 |
| Logic nodes grouped under one root | +10 | -5 if scattered |
| UI nodes under Canvas | +5 | -5 if mixed |
| Clear module separation | +5 | -2 per violation |

**Naming Score (20 points)**

| Rule | Points | Deduction |
|------|--------|-----------|
| PascalCase for nodes | +5 | -1 per violation |
| Semantic names (not node1, node2) | +5 | -2 per violation |
| Consistent prefixes (e.g., UI_, Btn_) | +5 | -1 per inconsistency |
| Chinese comments for key nodes | +5 | -1 per missing |

**Code-Scene Score (30 points)**

| Rule | Points | Deduction |
|------|--------|-----------|
| No hardcoded getChildByName paths >2 levels | +10 | -2 per violation |
| Scene references match actual nodes | +10 | -5 per orphan ref |
| Components attached to appropriate nodes | +5 | -2 per misplacement |
| Events properly scoped | +5 | -2 per global leak |

**Maintainability Score (20 points)**

| Rule | Points | Deduction |
|------|--------|-----------|
| Prefab usage for repeated structures | +5 | -2 per copy-paste |
| Single responsibility per component | +5 | -2 per god component |
| No circular references | +5 | -5 per cycle |
| Clear data flow direction | +5 | -2 per unclear flow |

#### Score Levels

| Score | Level | Emoji | Description |
|-------|-------|-------|-------------|
| 90-100 | Excellent | 🌟 | Production ready, well architected |
| 75-89 | Good | ✅ | Minor issues, acceptable |
| 60-74 | Fair | ⚠️ | Needs improvement before release |
| 40-59 | Poor | ❌ | Significant refactoring needed |
| 0-39 | Critical | 🚨 | Architectural problems, redesign required |

---

### review Command (Self-Check & Iterate)

```
vscene review
  │
  ├─ Step 1: Load existing analysis
  │
  ├─ Step 2: Verify issues still exist
  │   └─ Re-check each reported issue
  │
  ├─ Step 3: Check if suggestions implemented
  │   └─ Compare with previous analysis
  │
  ├─ Step 4: Update scores
  │   └─ Recalculate based on current state
  │
  └─ Output: Updated analysis with delta
```

**Review Output Example:**

```markdown
## Review: gameScene

### Score Change
| Dimension | Previous | Current | Delta |
|-----------|----------|---------|-------|
| Structure | 22/30 | 25/30 | +3 ✅ |
| Naming | 12/20 | 15/20 | +3 ✅ |
| Code-Scene | 20/30 | 20/30 | 0 |
| Total | 64/100 | 70/100 | +6 ✅ |

### Resolved Issues
- ✅ [S-001] node1 renamed to Environment
- ✅ [N-002] Added Chinese comments

### Remaining Issues
- ⚠️ [C-001] Still has hardcoded path in PlayerController.ts:45
```

---

### pretty Command (Hierarchy Optimization)

**Core Workflow: Analyze → Propose → Confirm → Execute**

```
vscene pretty
  │
  ├─ Phase 1: Analysis (分析阶段)
  │   ├─ Check/Load index (auto pull if needed)
  │   ├─ Detect naming issues (node1, New Node, etc.)
  │   ├─ Detect hierarchy issues (depth > 6, scattered nodes)
  │   ├─ Detect structure issues (ungrouped, mixed concerns)
  │   └─ Generate issue list with severity
  │
  ├─ Phase 2: Proposal (方案生成)
  │   ├─ Generate optimization operations
  │   │   ├─ Rename operations (重命名)
  │   │   ├─ Reparent operations (调整父节点)
  │   │   ├─ Reorder operations (调整顺序)
  │   │   └─ Group operations (分组整理)
  │   ├─ Preview before/after structure
  │   └─ Estimate impact (affected nodes count)
  │
  ├─ Phase 3: Confirmation (用户确认) ⏸️
  │   ├─ Display proposal to user
  │   ├─ Wait for user decision:
  │   │   ├─ "同意" / "执行" → Proceed to Phase 4
  │   │   ├─ "修改" + feedback → Revise proposal
  │   │   └─ "取消" → Abort
  │   └─ User can select specific operations
  │
  └─ Phase 4: Execution (执行阶段)
      ├─ Execute via MCP node_modify
      ├─ Batch operations for efficiency
      ├─ Update local index
      └─ Output: Execution summary
```

#### Optimization Rules (优化规则)

**1. Naming Optimization (命名优化)**

| Pattern | Issue | Suggested Fix |
|---------|-------|---------------|
| `node`, `node1`, `node2` | 无意义命名 | 根据子节点/组件推断语义名 |
| `New Node`, `Node` | 默认名称 | 根据上下文推断 |
| `节点1`, `测试` | 临时命名 | 提示用户提供语义名 |
| Mixed case (`playerNode`) | 大小写不规范 | `PlayerNode` (PascalCase) |

**2. Hierarchy Optimization (层级优化)**

| Issue | Criteria | Action |
|-------|----------|--------|
| 过深层级 | depth > 6 | 提升到合适父节点 |
| 单子节点链 | A→B→C (each has 1 child) | 扁平化，合并中间节点 |
| 散落逻辑节点 | Logic nodes under render | 移动到 LogicRoot |
| 散落 UI 节点 | UI nodes outside Canvas | 移动到 Canvas 下 |

**3. Structure Optimization (结构优化)**

| Issue | Criteria | Action |
|-------|----------|--------|
| 未分组 | >10 siblings at root | 按类型分组到容器 |
| 混合关注点 | UI + Logic + Render mixed | 分离到不同容器 |
| 重复结构 | Similar node patterns | 建议转为 Prefab |

#### Proposal Output Format (方案输出格式)

```markdown
## VScene Pretty: gameScene

### 检测到的问题 (Issues Found)

| # | 类型 | 节点 | 问题 | 严重度 |
|---|------|------|------|--------|
| 1 | 命名 | `node1` | 无意义命名 | ⚠️ |
| 2 | 命名 | `New Node` | 默认名称 | ⚠️ |
| 3 | 层级 | `A/B/C/D/E/F/G` | 层级过深 (7层) | ❌ |
| 4 | 结构 | `Canvas/PlayerCtrl` | 逻辑组件在UI容器下 | ⚠️ |

### 优化方案 (Optimization Plan)

#### 重命名操作 (Rename)
| # | 原名称 | 新名称 | UUID |
|---|--------|--------|------|
| R1 | `node1` | `Environment` | abc123 |
| R2 | `New Node` | `GameManager` | def456 |

#### 层级调整 (Reparent)
| # | 节点 | 原父节点 | 新父节点 | 原因 |
|---|------|----------|----------|------|
| P1 | `PlayerCtrl` | `Canvas` | `LogicRoot` | 逻辑组件应在逻辑容器 |
| P2 | `DeepNode` | `A/B/C/D/E/F` | `A/B` | 层级扁平化 |

#### 分组操作 (Group)
| # | 新容器 | 包含节点 | 原因 |
|---|--------|----------|------|
| G1 | `Managers` | `GameMgr, AudioMgr, UIMgr` | 管理器分组 |

### 预览 (Preview)

**Before:**
```
gameScene
├─ node1
├─ New Node [GameManager]
├─ Canvas
│  └─ PlayerCtrl [PlayerController]  ⚠️
└─ A/B/C/D/E/F/G  ❌
```

**After:**
```
gameScene
├─ Environment (原 node1)
├─ LogicRoot
│  ├─ GameManager (原 New Node)
│  └─ PlayerCtrl ✅
├─ Canvas
└─ A/B/DeepNode ✅
```

### 影响范围
- 重命名: 2 个节���
- 移动: 2 个节点
- 新建容器: 1 个

---
**请确认是否执行以上优化？**
- 输入 `同意` 或 `执行` 执行全部操作
- 输入 `执行 R1 P1` 执行指定操作
- 输入 `修改` + 反馈 调整方案
- 输入 `取消` 放弃优化
```

#### Execution Output (执行结果)

```markdown
## 执行完成 ✅

### 执行结果
| # | 操作 | 状态 |
|---|------|------|
| R1 | `node1` → `Environment` | ✅ 成功 |
| R2 | `New Node` → `GameManager` | ✅ 成功 |
| P1 | `PlayerCtrl` → `LogicRoot` | ✅ 成功 |

### 索引已更新
场景已保存，建议运行 `vscene analyze` 查看优化后评分。
```

---

## Analysis Document Template

See [references/analysis-template.md](references/analysis-template.md) for full template.

### Key Sections

1. **Header** - Scene name, stats, score summary
2. **Score Card** - Detailed scoring breakdown
3. **Structure Overview** - Annotated hierarchy tree
4. **Module Analysis** - Business module identification
5. **Code-Scene Relations** - Reference mapping table
6. **Issues & Suggestions** - Prioritized improvement list
7. **Iteration Log** - Review history

---

## Quick Start

### First Analysis

```bash
vscene pull              # Build index
vscene analyze           # Generate analysis
# Review .vscene/analysis/{scene}.analysis.md
```

### Iterate on Quality

```bash
# Make improvements to scene...
vscene review            # Check progress
vscene analyze           # Full re-analysis
```

### Generate Scene Map

```bash
vscene map               # Generate annotated scene map
# View .vscene/maps/{scene}.map.md
vscene map --refresh     # Force regenerate
```

### Auto Optimization

```bash
vscene pretty            # Analyze and propose optimizations
# Review proposal, then:
# - "同意" to execute all
# - "执行 R1 P1" to execute specific operations
# - "修改" + feedback to revise
# - "取消" to abort
```

### Check Specific Issues

```bash
vscene find node*        # Find poorly named nodes
vscene detail <uuid>     # Inspect specific node
```

---

## Index Output Format

### vscene read (depth: 3)

```
## VScene: gameScene (226 nodes, depth 8)
Cached: 2026-01-26 | Score: 72/100 ⚠️

gameScene                           # 场景根节点
├─ Main Light [DirectionalLight]    # 主光源
├─ Main Camera [CameraComponent]    # 主相机
├─ Canvas [Canvas] ★                # UI 画布
│  ├─ JoystickUI                   # 摇杆控制
│  └─ DragtoMove                   # 拖拽提示
├─ node1                           # ⚠️ 命名不规范
│  └─ [+36 nodes]
└─ LogicRoot ★                     # 逻辑根节点
   ├─ Player ★                     # 玩家角色
   ├─ Unlock ★                     # 解锁系统
   └─ UnlockBuildings ★            # 可解锁建筑

★ = Key node | ⚠️ = Has issues | [+N] = Collapsed
```

---

## Key Node Detection

Nodes with these components are marked as key (`k: true`):

**Priority 1 (Always):**
- `*Manager`, `*Controller`, `*System`, `Root`
- `*Assets`, `*Factory`, `*Spawner`

**Priority 2 (Business):**
- `*Trigger`, `*Handler`, `*Generator`
- Any custom component (not `cc.*` prefixed)

---

## Detailed References

- [references/data-structure.md](references/data-structure.md) - Full JSON schema
- [references/auto-sync.md](references/auto-sync.md) - Auto-sync flow details
- [references/mcp-integration.md](references/mcp-integration.md) - MCP API usage
- [references/analysis-template.md](references/analysis-template.md) - Analysis document template
- [references/map-template.md](references/map-template.md) - Scene map output template
- [references/annotation-rules.md](references/annotation-rules.md) - Map annotation inference rules

---

## Error Handling

| Scenario | Handling |
|----------|----------|
| MCP disconnected + has cache | read/find/status/review/map work offline |
| MCP disconnected + no cache | Error, prompt to start editor |
| MCP disconnected + analyze | Error, MCP required for full analysis |
| MCP disconnected + map (no index) | Error, index required (auto-pull needs MCP) |
| Index corrupted | Auto rebuild |
| Analysis outdated | Warn on read, suggest re-analyze |
