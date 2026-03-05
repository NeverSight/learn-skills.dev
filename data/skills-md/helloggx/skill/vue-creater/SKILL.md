---
name: vue-creater
description: Suite of tools for scaffolding high-fidelity Vue 3 applications using Vite 8 and Tailwind 4. Supports design-driven workflows via DSL and Tokens. Ideal for rapid prototyping or production-ready frontend setups.
version: 1.0.0
license: MIT
authors: [玄子]
---

# Vue Web Artifacts Builder

## Data Flow & Context Management (CRITICAL)

You must maintain a **Session Context** to store file paths. Do not proceed to subsequent steps until you have populated the required variables.

* `$PROJECT_ROOT`: The absolute path to the project created in Step 1.
* `$DSL_PATH`: The absolute path to the `dsl.json` file generated in Step 2 (only for Default template workflow).

## Quick Start

### Step 0: Select Project Type

**FIRST STEP - MANDATORY**: You must ask the user to select a project type:

```
Please select the project type:

    1. **Default** (shadcn + tailwindcss + vite)
    2. **Nuxt Admin Dashboard** (shadcn + tailwindcss + nuxt)

    Choice [1/2]:
```

**STOP and WAIT for user input** - do NOT execute menu items automatically - accept number or cmd trigger or fuzzy command match

**Action based on user input:**

* **If Choice "1" (Default):**
    1. Proceed to Step 1 and follow the default workflow (Steps 1-4).

* **If Choice "2" (Nuxt Admin Dashboard):**
    1. Execute the script: `python3 scripts/setup_nuxt_dashboard.py [project-name]`
       * *Condition*: If a project name is specified in the context, pass it as an argument. Otherwise, omit it to use the default name.
    2. **CAPTURE OUTPUT**: Look for the directory path in the script's output (last line before success message).
    3. **ASSIGN**: Set this path to variable `$PROJECT_ROOT`.
    4. **SKIP ALL REMAINING STEPS** - The Nuxt dashboard is fully configured and ready to use.
    5. Inform the user to run: `cd $PROJECT_ROOT && bun run dev`
    6. **END WORKFLOW** - Do not proceed to Steps 1-4.

---

## Default Template Workflow (Choice 1)

To build powerful frontend claude.ai artifacts using the Vue ecosystem, follow these steps:
1. Initialize the project scaffold using script: `scripts/shadcn_vue_init.py`
2. Retrieve design data using tool: `get_dsl`
3. Apply design tokens and styles using tool: `get_token`
4. Start development server

**Stack**: 
- **Core**: Vue 3 (Script Setup) + TypeScript + Vite v8.0.0
- **Styling**: Tailwind CSS v4 + shadcn-vue (Radix-vue based)
- **State & Logic**: Pinia (Store) + Vue Router + TanStack Query (vue-query)

### Step 1: Initialize Project Scaffolding

**Instruction**:
1. Execute the script: `python3 scripts/shadcn_vue_init.py [project-name]`
   * *Condition*: If a project name is specified in the context, pass it as an argument. Otherwise, omit it to use the default name.
2. **CAPTURE OUTPUT**: Look for the directory path in the script's output (last line before success message).
3. **ASSIGN**: Set this path to variable `$PROJECT_ROOT`.
4. *Validation*: If `$PROJECT_ROOT` is empty, stop and ask the user to verify the installation.

**What this script does**:

* ✅ Sets up Vue 3 + Vite 8.0.0
* ✅ Configures Tailwind CSS 4 (CSS-first configuration, no generic config js)
* ✅ Installs shadcn-vue and configures `components.json`
* ✅ Sets up Pinia, Vue Router, and Vue Query plugins

### Step 2: Sync Design Data (DSL)
you must ask question:
Please select the design source configuration:

    1. **Custom Design DSL** (Provide a URL or file path for the design tokens)
    2. **Use TOKEN_URL_LIGHT** (Read DSL URL from .env TOKEN_URL_LIGHT variable)
    3. **Use Default** (Skip design tokens, use default theme)

    Choice [1/2/3]:


**STOP and WAIT for user input** - do NOT execute menu items automatically - accept number or cmd trigger or fuzzy command match
Fetch the design structure and layout data from the source:

**Action based on user input:**

* **If Choice "1" (Custom):**
    1. Ask for URL (if missing).
    2. Execute `get_dsl` with the URL.
    3. **CAPTURE OUTPUT**: Look for the file path of the saved JSON (e.g., `.../dsl.json`).
    4. **ASSIGN**: Set this path to variable `$DSL_PATH`.

* **If Choice "2" (TOKEN_URL_LIGHT):**
    1. Read the `TOKEN_URL_LIGHT` variable from `.env` file.
    2. **If TOKEN_URL_LIGHT is not defined**: Prompt user to define it in `.env` file, e.g., `TOKEN_URL_LIGHT=https://your-token-url.com/dsl.json`
    3. **If TOKEN_URL_LIGHT is defined**: Execute `get_dsl` with the URL from `TOKEN_URL_LIGHT`.
    4. **CAPTURE OUTPUT**: Look for the file path of the saved JSON (e.g., `.../dsl.json`).
    5. **ASSIGN**: Set this path to variable `$DSL_PATH`.

* **If Choice "3" (Use Default):**
    1. Log "Using default theme, skipping DSL fetch."
    2. **ASSIGN**: Set `$DSL_PATH` to empty or null to indicate no custom design tokens.

### Step 3: Apply Design Tokens

**Prerequisites**:
* Ensure `$PROJECT_ROOT` is defined (from Step 1).
* Ensure `$DSL_PATH` is defined (from Step 2).

**Instruction**:
You must now call the `get_token` tool using the exact paths captured previously.

**Strict Execution Logic**:
> IF `$DSL_PATH` is valid (User chose Custom):
>   Execute: `get_token(project_path=$PROJECT_ROOT, dsl_path=$DSL_PATH)`
>
> ELSE (User chose Default):
>   Log "Skipping token application for default theme."

**Goal**: Extract design tokens from the DSL file at `$DSL_PATH` and inject them into the Tailwind 4 configuration located inside `$PROJECT_ROOT`.

### Step 4: Start Development Server

**Instruction**:
1. Execute the command below immediately.
2. **CRITICAL**: You MUST use the chained command format (`&&`) to ensure the directory context is preserved.

```bash
cd "$PROJECT_ROOT" && bun run dev
```

**Note**: The project uses `bun` as the package manager for faster dependency installation and development server startup.

## Scripts Reference

### shadcn_vue_init.py

**Location**: `scripts/shadcn_vue_init.py`

**Usage**:
```bash
python3 scripts/shadcn_vue_init.py [project-name]
```

**Features**:
- Creates Vue 3 + Vite 8.0.0 project
- Configures Tailwind CSS 4 with CSS-first configuration
- Installs and configures shadcn-vue components
- Sets up Pinia, Vue Router, and TanStack Query
- Installs Zod for schema validation
- Installs VueUse for composition utilities
- Creates utility files (lib/utils.ts, composables/useApi.ts)
- Generates comprehensive README.md
- Cleans up unnecessary template files

### setup_nuxt_dashboard.py

**Location**: `scripts/setup_nuxt_dashboard.py`

**Usage**:
```bash
python3 scripts/setup_nuxt_dashboard.py [project-name]
```

**Features**:
- Extracts a pre-configured Nuxt 3 admin dashboard template from zip file
- Includes Shadcn UI components and Tailwind CSS configuration
- Installs all necessary dependencies using bun
- Provides a ready-to-use admin dashboard structure

## Reference

* **shadcn-vue**: https://www.shadcn-vue.com/
* **Tailwind CSS v4**: https://tailwindcss.com/docs/v4-beta (CSS-centric config)
* **Vite**: https://vitejs.dev/

