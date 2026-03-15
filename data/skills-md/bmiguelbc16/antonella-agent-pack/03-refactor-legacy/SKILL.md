---
name: 03-refactor-legacy
description: Refactor legacy or procedural WordPress plugins into Antonella MVC. Use when modernizing existing plugins with configurable backward-compatibility levels.
---

# Skill: 03-refactor-legacy (Modernizer)

## 📜 Source of Truth
> **Standard**: [Architecture Standards](../../normative/architecture_standards.md)
> **Standard**: [Security Standards](../../normative/security_standards.md)

## 🎯 Purpose
Modernize legacy WordPress plugins or messy procedural codebases by refactoring them into the Antonella MVC structure, while optionally ensuring 100% backward compatibility via proxy methods. **You act as a modernization architect.**

---

## 🗣️ Agent Interaction Protocol — The Audit Phase

> [!CAUTION]
> Refactoring a legacy plugin is high-risk. **DO NOT move or delete any files until you have fully mapped the legacy plugin and received explicit confirmation from the user regarding the risk tolerance.**

**First Action:** Ask the user to provide the path to the legacy plugin and determine the modernization strategy:

"I am ready to modernize a legacy plugin for you. Please provide the path to the legacy plugin (e.g., `wp-content/plugins/my-old-plugin`). Additionally, choose the level of aggressiveness for this refactor:"

**Option A: Conservative (Safety First)**
I will extract the procedural logic into proper MVC Controllers and Services, but I will keep all original global function signatures and hooks intact as "proxy" shells. This prevents breaking other plugins that might depend on them.

**Option B: Standard Migration**
I will do a full MVC migration. Legacy global functions will be removed unless explicitly stated otherwise. Database tables and major hook names will remain identical.

**Option C: Aggressive Rebuild**
Full migration. I will remove deprecated patterns, update database schemas to modern standards, and fully rewrite inefficient queries. Backward compatibility is not guaranteed.

*Wait for the user's response to proceed.*

---

## 🔄 Execution Protocol

### 🧭 Phase 1: Snapshot & Map
Before changing any logic, scan the legacy plugin and map:
- All `add_action` and `add_filter` calls.
- All global functions declared.
- All direct database interactions (`$wpdb`).

### 🧭 Phase 2: Logic Extraction
Move procedural functions from legacy files into structured `Controllers` or `Services` in the Antonella `src/` directory.

### 🧭 Phase 3: Backward Compatibility (If Option A)
Keep legacy function names in the main plugin file or a dedicated `legacy-functions.php` file. These functions should simply call the new MVC classes. 
*Example:* `function my_old_function() { return (new MyController())->newMethod(); }`

### 🧭 Phase 4: Route Translation
Move inline `$_POST`/`$_GET` handling from procedural files into standard Antonella `config/Config.php` routing definitions mapped to the new Controllers.

---

## 🏁 Quality Gates
- ✅ Agent asked for confirmation and risk tolerance before touching files.
- ✅ All extracted logic is now PSR-4 compliant.
- ✅ If Conservative, legacy entry points remain functional.
- ✅ No logic resides directly in the main plugin bootstrap file.
