---
name: 01-scaffold-and-plan
description: Scaffold and plan a new WordPress plugin with Antonella Framework. Use when starting a new plugin, defining architecture, and generating implementation plan artifacts.
---

# Skill: 01-scaffold-and-plan (Project Initialization & Architecture)

## 📜 Source of Truth
> **Standard**: [Architecture Standards](../../normative/architecture_standards.md)
> **Standard**: [Security Standards](../../normative/security_standards.md)
> **Standard**: [OOP Standards](../../normative/oop_standards.md)
> **Standard**: [Database Standards](../../normative/database_standards.md)

## 🎯 Purpose
Bootstrap a brand-new WordPress plugin from zero using the Antonella Framework CLI, and establish the technical architecture. **You act as a senior architectural agent.**

---

## 🗣️ Agent Interaction Protocol — The Discovery Phase

> [!CAUTION]
> As a modern agent, **DO NOT run any `composer` or `php antonella` commands until you understand the user's objective.**

**First Action:** Ask the user what they want to achieve and present them with clear options:

"Hello! I am ready to scaffold your new Antonella Framework plugin. To get started, please tell me a bit about the plugin or choose from the options below:"

**Option A: Standard MVC Plugin**
Create a standard plugin with Admin UI and REST API support.

**Option B: Headless API Plugin**
Create a plugin focused entirely on REST/GraphQL endpoints with no Admin UI.

**Option C: Custom Setup**
I will ask you for specific details (Name, Slug, Tables, etc.).

*Wait for the user's response to proceed.*

### Once the goal is understood, gather the required configuration:

Confirm the following details with the user (suggest logical defaults if they chose Option A or B):
1. **Plugin Name:** (e.g., "My Awesome Plugin")
2. **Plugin Slug:** (e.g., `my-awesome-plugin`)
3. **Namespace:** (e.g., `MyAwesomePlugin`)
4. **Data Strategy:** How will data be stored? (Options: `Custom Post Types`, `wp_options`, `Custom Tables`)
5. **Optional Modules:** Any Antonella modules? (Options: `blade`, `model`, `dd`)

Present a summary and ask for **final confirmation** before running the setup commands.

---

## 🔄 Execution Protocol

Only proceed here **AFTER** the user has confirmed the configuration.

### 🧭 Phase 1: Clone the Antonella Base Template

```bash
# Replace [plugin-slug] with the confirmed slug
composer create-project antonella-framework/antonella-framework [plugin-slug]
cd [plugin-slug]
```

*(If Composer fails, clone manually `git clone https://github.com/antonella-framework/antonella-framework [plugin-slug]` and run `composer install`)*

### 🧭 Phase 2: Configure Plugin Identity

Inside the `[plugin-slug]` directory:

1. Rename the main plugin file:
```bash
php antonella updateproject
```

2. Apply the Namespace:
```bash
# Replace [PluginNamespace] with the confirmed PascalCase namespace
php antonella namespace [PluginNamespace]
```

### 🧭 Phase 3: Generate Scaffolded Components

Generate the required components based on the user's selected scope and options:

*   For Admin UI/Controllers: `php antonella make [ControllerName]`
*   For API: `php antonella make ApiController`
*   For Custom Post Types: `php antonella cpt [PostTypeName]`

Install optional modules if requested:
*   `php antonella add blade`
*   `php antonella add model`
*   `php antonella add dd`

### 🧭 Phase 4: Create the Implementation Plan

Review the established configuration and generate an `implementation_plan.md` in the project root outlining the architecture mappings (Controllers to be built, Services needed, Data models). Save this file.

---

## 🏁 Quality Gates

- ✅ Agent asked for confirmation via options before executing commands.
- ✅ Plugin directory slug matches `[PluginSlug]`.
- ✅ `php antonella updateproject` and `php antonella namespace` executed successfully.
- ✅ `implementation_plan.md` generated.
