---
name: ue-project-context
description: "When the user wants to create or update their Unreal Engine project context document. Use when the user says 'project context,' 'set up context,' 'UE context,' 'configure project,' or wants to avoid repeating their project setup across UE development tasks. Creates `.agents/ue-project-context.md` that all other UE skills reference. See related skills footer for skills that depend on this context."
metadata:
  version: 1.0.0
---

# UE Project Context

You help UE developers create and maintain a project context document that other UE skills reference. This captures the engine version, module structure, plugin dependencies, coding conventions, and team practices specific to the user's project, so advice is always tailored rather than generic.

The document is stored at `.agents/ue-project-context.md`.

---

## Workflow

### Step 1: Check for Existing Context

First, check if `.agents/ue-project-context.md` already exists.

**If it exists:**
- Read it and summarize what's captured
- Ask which sections the user wants to update
- Only gather information for those sections

**If it doesn't exist, offer two options:**

1. **Auto-draft from codebase** (recommended): Scan the project files — `.uproject`, `Source/*/Build.cs`, `Source/*/*.Target.cs`, `Config/*.ini`, `Plugins/` — and draft a V1 of the context document. The user reviews, corrects, and fills gaps. Faster than starting from scratch.

2. **Interactive questionnaire**: Walk through each section conversationally, one at a time.

Most users prefer option 1. After presenting the auto-draft, ask: "What needs correcting? What's missing?"

---

### Step 2: Gather Information

#### If Auto-Drafting

Scan these files and populate each section:

**`.uproject`**
- `EngineAssociation` → engine version
- `Plugins[]` → enabled plugins (name + enabled state)
- `Modules[]` → module list and types

**`Source/*/Build.cs`** (one per module)
- Module name (class name)
- `PublicDependencyModuleNames` and `PrivateDependencyModuleNames`
- `Type` field → Runtime, Editor, Developer, etc.
- Any `ThirdParty` include/library paths

**`Source/*/*.Target.cs`**
- Target types: Game, Editor, Server, Client
- `DefaultBuildSettings`, `ExtraModuleNames`
- Platform-specific conditions

**`Config/DefaultEngine.ini`**
- `ActiveGameNameRedirect`, `GameDefaultMap`, `GlobalDefaultGameMode`
- Any custom subsystem or plugin settings

**`Config/DefaultGame.ini`**
- Project display name, version

**`Plugins/*/`**
- Custom plugin directories → names and types

After scanning, draft all sections and present the document. Ask what needs correcting or is missing. Iterate until the user confirms it's accurate.

#### If Using Interactive Questionnaire

Walk through each section below one at a time. Do not dump all questions at once.

For each section:
1. Briefly explain what you're capturing and why it matters
2. Ask the relevant questions
3. Confirm accuracy
4. Move to the next section

---

## Sections to Capture

### 1. Engine & Project Overview

Discovery questions:
- What is the project name and a one-sentence description of what it is?
- Which Unreal Engine version are you using (e.g., 5.3, 5.4)? Is this a launcher build or a source build?
- What type of project is this: game, simulation, visualization, tool, plugin, or something else?
- What genre or domain (e.g., first-person shooter, strategy, architectural viz, training sim)?
- What are your target platforms (Windows, Mac, Linux, PS5, Xbox, iOS, Android, VR)?

### 2. Module Structure

Discovery questions:
- How many modules does the project have? What are their names?
- Which is the primary game module?
- What type is each module: Runtime, Editor, Developer, or ThirdParty?
- Are any modules shared libraries or standalone plugins?
- Are there any modules under active development vs. stable/locked modules?

### 3. Plugin Dependencies

Discovery questions:
- Which engine plugins are enabled (e.g., GameplayAbilities, EnhancedInput, CommonUI, Niagara, PCG, MetaSounds, Chaos, OnlineSubsystem)?
- Do you use any Fab/Marketplace plugins? Which ones are critical to gameplay?
- Do you have any custom or in-house plugins in the `Plugins/` directory?
- Are any plugins licensed with restrictions the AI should know about?

### 4. Coding Conventions

Discovery questions:
- Do you follow Epic's standard UE naming prefixes (F, U, A, E, I)? Any exceptions or additions?
- Do you use `#pragma once` or traditional header guards?
- What `DEFINE_LOG_CATEGORY` names does the project use most?
- What is your preferred assertion style: `check()`, `ensure()`, `checkf()`, or `verify()`?
- How do you organize headers — separate Public/Private folders per module, or flat?
- Any other code style rules the team enforces (e.g., no raw pointers for UObjects, always use TObjectPtr)?

### 5. Subsystems in Use

Discovery questions:
- Do you have a custom GameMode or GameState? What are the class names?
- What custom PlayerController and Pawn/Character classes exist?
- Which UE subsystem types do you use: `UGameInstanceSubsystem`, `UWorldSubsystem`, `ULocalPlayerSubsystem`, `UEngineSubsystem`?
- Do you have custom systems for inventory, dialogue, quest, save, UI management, or similar?
- Are you using the Gameplay Ability System (GAS)? If so, what are your key Ability, Effect, and AttributeSet class names?

### 6. Build Configuration

Discovery questions:
- Which build targets do you ship: Game, Editor, Server, Client, or a subset?
- Do you define any custom preprocessor macros or build flags?
- Do you integrate any third-party C++ libraries? Which ones and how (binary, source)?
- Are there platform-specific code paths or compilation guards to be aware of?
- Do you use a custom engine fork or any engine modifications?

### 7. Team Context (Optional)

Discovery questions:
- How large is the team, and what are the main roles (engineers, designers, artists)?
- What source control system do you use (Perforce, Git, Plastic SCM)?
- Do you have a branching strategy or lock policy for assets?
- Do you have a code review process? What's the bar for approval?
- Are there documentation standards — in-code comments, Confluence, Notion, etc.?

---

## Step 3: Create the Document

After gathering information, create `.agents/ue-project-context.md` with this structure:

```markdown
# UE Project Context

*Last updated: [date]*

## Engine & Project Overview
**Engine version:** [e.g., UE 5.4 — Launcher build]
**Project name:** [name]
**Description:** [one sentence]
**Project type:** [game / simulation / visualization / tool]
**Genre / domain:** [e.g., third-person action RPG]
**Target platforms:**
- [Platform 1]
- [Platform 2]

## Module Structure
**Primary game module:** [ModuleName]

| Module | Type | Notes |
|--------|------|-------|
| [Name] | Runtime | Core gameplay |
| [Name] | Editor | Custom editor tools |
| [Name] | Developer | Shared utilities |

**Key dependencies per module:**
- **[ModuleName]**: PublicDeps: [list]; PrivateDeps: [list]

## Plugin Dependencies
**Engine plugins enabled:**
- [PluginName] — [brief purpose]

**Marketplace / Fab plugins:**
- [PluginName] — [brief purpose]

**Custom plugins:**
- [PluginName] — [brief purpose]

## Coding Conventions
**Naming prefixes:** Standard UE (F/U/A/E/I) [+ any exceptions]
**Header style:** `#pragma once`
**Log categories in use:**
- `LOG_[CategoryName]` — [scope]
**Assertion style:** [check / ensure / verify — preferred and rationale]
**Header organization:** [Public/Private folders per module / flat]
**Additional rules:**
- [Rule 1]
- [Rule 2]

## Subsystems in Use
**Gameplay framework:**
- GameMode: `[ClassName]`
- GameState: `[ClassName]`
- PlayerController: `[ClassName]`
- Pawn / Character: `[ClassName]`

**Subsystems:**
| Class | Type | Responsibility |
|-------|------|----------------|
| [ClassName] | UGameInstanceSubsystem | [purpose] |
| [ClassName] | UWorldSubsystem | [purpose] |

**Custom systems:**
- [System name]: [brief description and key classes]

**GAS usage:**
- Abilities: [base class name]
- Attribute Sets: [class names]
- Key gameplay tags: [list or "see Config/DefaultGameplayTags.ini"]

## Build Configuration
**Build targets:** [Game, Editor, Server, Client — which apply]
**Custom macros / build flags:**
- `[MACRO_NAME]` — [purpose]
**Third-party libraries:**
- [LibraryName] — [integration method: binary / source]
**Platform-specific notes:**
- [Platform]: [relevant constraint or code path]
**Engine modifications:** [None / Custom fork at [repo] — [what was changed]]

## Team Context
**Team size:** [N engineers, N designers, N artists]
**Source control:** [Perforce / Git / Plastic SCM]
**Branching strategy:** [description]
**Code review:** [process and bar]
**Documentation standards:** [in-code / Confluence / Notion / etc.]
```

---

## Step 4: Confirm and Save

- Show the completed document
- Ask if anything needs adjustment before saving
- Save to `.agents/ue-project-context.md`
- Tell the user: "All other UE skills will now reference this context automatically. Run `/ue-project-context` anytime to update it as your project evolves."

---

## Tips

- **Prioritize auto-draft**: Even a partial scan saves significant back-and-forth.
- **Engine version matters**: UE 5.0 vs 5.4 have meaningful API differences — always confirm it.
- **Module boundaries are important**: Many UE compilation errors trace to incorrect dependency declarations; capture them accurately.
- **Ask for class names, not descriptions**: "What's your GameMode called?" beats "Do you have a custom GameMode?"
- **GAS projects need extra detail**: If GAS is in use, capture AttributeSet names and tag conventions — other skills rely on them heavily.
- **Skip inapplicable sections**: Solo developers without team context don't need Section 7.
- **Note what's unknown**: It's valid to write "Not yet established" for conventions the team hasn't decided. Don't invent answers.

---

## Related Skills

Other UE skills that depend on this context:
- `ue-cpp-foundations` — uses module names and coding conventions
- `ue-module-build-system` — uses module structure and dependencies
- `ue-gameplay-abilities` — uses GAS setup and attribute sets
- `ue-gameplay-framework` — uses GameMode, GameState, and PlayerController classes
- `ue-actor-component-architecture` — uses module structure and subsystem list
- `ue-input-system` — uses Enhanced Input plugin status and PlayerController class
- `ue-ui-umg-slate` — uses CommonUI plugin status and module structure
- `ue-networking-replication` — uses build targets (Server/Client) and GameState class
- `ue-testing-debugging` — uses log categories and module structure
- `ue-editor-tools` — uses Editor module names and plugin list
