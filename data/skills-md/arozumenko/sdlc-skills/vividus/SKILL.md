---
name: vividus
description: Use when the user mentions Vividus, .story files, vividus-bom/-starter, backtick-parameter BDD, or ./gradlew runStories. Bootstrap, configure, and author tests for the Vividus BDD framework — JBehave-based, config-first .story files spanning web/REST/mobile/DB via 47+ plugins.
license: Apache-2.0
metadata:
  authors:
    - Alexander Bychinskiy <alexander_bychinskiy@epam.com>
    - Artem Rozumenko <artem_rozumenko@epam.com>
  version: "1.0.0"
  framework: vividus
  framework-version: "0.6.x"
  framework-repo: https://github.com/vividus-framework/vividus
  framework-docs: https://docs.vividus.dev/vividus/latest/
---

# Vividus Test Automation

Vividus is a JBehave-based BDD framework. Tests are plain-text `.story` files using a strict, pre-built step library — authors compose tests by **wording**, not Java. Plugins extend the step library per domain (web, REST, mobile, DB, cloud).

This skill knows the framework's conventions, file layout, properties model, and step phrasings so you can scaffold projects, add plugins, author/edit stories without invented steps, and run/debug suites.

## Decision tree — pick a path

| User intent | Path |
|---|---|
| New project from scratch | [Bootstrap a project](#bootstrap-a-project) |
| Add web/REST/mobile/DB/etc. capability | [Add a plugin](#add-a-plugin) |
| Write or edit a `.story` file | [Author a story](#author-a-story); read `references/steps-cheatsheet.md` |
| Configure suites/profiles/environments | Read `references/configuration.md` |
| Set up data-driven tests / external tables | Read `references/variables-and-tables.md` |
| Run, filter, debug | [Run tests](#run-tests) |
| Test won't match / step not found / locator fails | Read `references/troubleshooting.md` |
| Pick a plugin / understand 47-plugin catalog | Read `references/plugins.md` |

When in doubt, **ground every step phrasing against the docs** (https://docs.vividus.dev/vividus/latest/) or against `./gradlew printSteps` output. Do **not** invent step phrases — Vividus matches steps by exact wording (with parameters). If a step doesn't match, it silently becomes a "pending" step at runtime.

## Core concepts you must internalize

1. **Tests are `.story` files** under `src/main/resources/story/...`. Sections: `Description:`, `Meta:`, `GivenStories:`, `Lifecycle:`, `Scenario:`, `Examples:`. Steps start with `Given`/`When`/`Then`.
2. **Step parameters use backticks `` ` ``, not quotes.** Example: `` Then `${name}` is equal to `Bob` ``. This is the #1 syntax error.
3. **Variables**: `${var}` for read, `<col>` for ExamplesTable placeholders, `#{expression(...)}` for compile-time expressions (data generation, formatting).
4. **Three orthogonal config axes**: `configuration.suites`, `configuration.profiles`, `configuration.environments`. Each loads `.properties` files; first declared wins.
5. **BOM-pinned versions**: `org.vividus:vividus-bom:<version>` controls every plugin's version. Never override individual plugin versions.
6. **JDK 21** (Temurin recommended). Older JDKs fail with cryptic errors.
7. **Build system is a git submodule** (`vividus-build-system`). Always `git clone --recursive`, or run `git submodule update --init --recursive` after a regular clone.

## Bootstrap a project

The starter is a **GitHub template repo**: https://github.com/vividus-framework/vividus-starter. Two paths:

**A. Generate from template (preferred for real projects):**
1. Open https://github.com/vividus-framework/vividus-starter/generate (user does this in browser).
2. `git clone --recursive <new-repo-url>` and `cd` into it.

**B. Local clone of the starter (for prototyping/learning):**
```bash
git clone --recursive https://github.com/vividus-framework/vividus-starter.git my-vividus-tests
cd my-vividus-tests
./gradlew build
```

If the user already cloned without `--recursive`, fix it with:
```bash
git submodule update --init --recursive
```

Then create the conventional directory tree (the starter ships nearly empty):

```bash
mkdir -p src/main/resources/story/web_app
mkdir -p src/main/resources/story/rest_api
mkdir -p src/main/resources/steps
mkdir -p src/main/resources/properties/suite/web_app
mkdir -p src/main/resources/properties/suite/rest_api
mkdir -p src/main/resources/properties/profile/web/desktop/chrome
mkdir -p src/main/resources/properties/environment/dev
```

Templates to copy as starting points (see `assets/`):
- `assets/build.gradle.template` — common plugin selection, BOM-pinned
- `assets/configuration.properties.template` — master config
- `assets/suite.properties.template` — batch + parallelism + composite-paths
- `assets/example-web.story`, `assets/example-rest.story` — runnable smoke stories
- `assets/example-visual.story` — visual regression template (ESTABLISH / COMPARE_AGAINST)
- `assets/example.steps` — composite step example

Always check the **latest BOM version** before pinning: https://github.com/vividus-framework/vividus/releases. As of skill authoring, recent versions are around `0.6.16`–`0.6.18`.

## Add a plugin

Plugins are added in `build.gradle` under `dependencies { ... }`. The BOM picks the version automatically:

```gradle
dependencies {
    implementation platform('org.vividus:vividus-bom:0.6.18')
    implementation('org.vividus:vividus')
    implementation('org.vividus:vividus-plugin-web-app')      // Selenium-based web
    implementation('org.vividus:vividus-plugin-rest-api')     // HTTP/REST
    implementation('org.vividus:vividus-plugin-json')         // JSONPath assertions
    implementation('org.vividus:vividus-plugin-db')           // JDBC databases
    implementation('org.vividus:vividus-plugin-mobile-app')   // Appium iOS/Android
}
```

Use `references/plugins.md` to choose the right plugin for a capability. Quick map:

| Need | Plugin |
|---|---|
| Selenium web testing | `vividus-plugin-web-app` |
| Playwright web testing | `vividus-plugin-web-app-playwright` |
| REST/HTTP API | `vividus-plugin-rest-api` (+ `vividus-plugin-json` for JSONPath) |
| Mobile (Appium) | `vividus-plugin-mobile-app` |
| Relational DB | `vividus-plugin-db` |
| Visual diff | `vividus-plugin-visual` (or `vividus-plugin-applitools`) |
| Accessibility | `vividus-plugin-accessibility` |
| Kafka / RabbitMQ | `vividus-plugin-kafka`, `vividus-plugin-rabbitmq` |
| AWS S3 / DynamoDB / Lambda | `vividus-plugin-aws-s3`, `-aws-dynamodb`, `-aws-lambda` |
| Azure Service Bus / Cosmos | `vividus-plugin-azure-service-bus`, `-azure-cosmos-db` |
| BrowserStack / SauceLabs / LambdaTest | `vividus-plugin-browserstack`, `-saucelabs`, `-lambdatest` |
| CSV / Excel / XML / YAML | `vividus-plugin-csv`, `-excel`, `-xml`, `-yaml` |

After adding a plugin, run `./gradlew build` and the new steps are available in `.story` files. To list every available step in the project: `./gradlew printSteps`.

## Author a story

Story files end in `.story` and live under any path matching `batch-N.resource-location` (typically `src/main/resources/story/...`). Naming is human-readable, often `Title Case With Spaces.story`.

Minimal web example:
```gherkin
Description: Login smoke test

Meta:
    @feature login
    @priority 1

Scenario: Sign in with valid credentials
Given I am on main application page
When I go to relative URL `/login`
When I enter `tomsmith` in field located by `id(username)`
When I enter `SuperSecretPassword!` in field located by `id(password)`
When I click on element located by `cssSelector(button[type='submit'])`
Then text `You logged into a secure area!` exists
```

> **`${web-application.main-page-url}` is NOT a story variable.** It is a Spring property consumed internally by the web plugin. `Given I am on main application page` is the correct step — it navigates to that configured URL without needing a variable. To expose a URL as a story variable (e.g., for building paths), declare it explicitly in `environment.properties`:
> ```properties
> web-application.main-page-url=https://staging.example.com
> variables.appUrl=https://staging.example.com   # same value — now usable as ${appUrl} in stories
> ```

Minimal REST example:
```gherkin
Description: Star Wars API smoke

Scenario: Verify Luke's eyes are blue
When I execute HTTP GET request for resource with URL `https://swapi.info/api/people/1/`
Then `${responseCode}` is equal to `200`
Then JSON element value from `${response}` by JSON path `$.eye_color` is equal to `blue`
```

Authoring rules (Vividus is finicky about syntax):
- **Backticks around every parameter.** No quotes, no plain values.
- **Locators** use a typed format: `xpath(...)`, `cssSelector(...)`, `id(...)`, `linkText(...)`, `name(...)`, `tagName(...)`, `className(...)`, `accessibilityId(...)` (mobile), `shadowCssSelector(...)`. Optional visibility flag (`:v` visible, `:i` invisible, `:a` all) and filter chain (`->filter.<type>(<value>)`).
- **Variable scopes** (narrowest wins): `step` < `scenario` < `story` < `next_batches` < `batch` < `global`. Use `scenario` by default; promote to `story` only when a value must persist across scenarios.
- **Lifecycle** blocks (`Lifecycle: Before:` / `After:`) declare scoped setup/teardown. Use `Scope: STORY` for one-time setup, `Scope: SCENARIO` for per-scenario.
- **Comments** in stories are lines starting with `!--` (not `#`).
- **Composite steps** (re-usable phrases) live in `src/main/resources/steps/**/*.steps`. See `assets/example.steps`.
- **Don't invent step phrasings.** Read `references/steps-cheatsheet.md` for verified phrasings, or run `./gradlew printSteps` in the project.

For the full step library with exact phrasings (web/REST/JSON/DB/mobile/lifecycle/composites), read `references/steps-cheatsheet.md`. For ExamplesTable, transformers (FROM_CSV, FROM_EXCEL, FROM_DB, FILTERING, MERGING, JOINING, ...), and expression syntax, read `references/variables-and-tables.md`.

## Configure suites, profiles, environments

Master file: `src/main/resources/properties/configuration.properties`:
```properties
configuration.suites=web_app
configuration.profiles=web/desktop/chrome
configuration.environments=dev
```

- **Suite** → "what stories to run" — one or more directories of `.story` files plus per-batch settings (parallelism, meta filters). Files at `properties/suite/<name>/suite.properties`.
- **Profile** → "on what platform" — browser/device specifics. Cascading paths (`web/desktop/chrome` loads `web` then `web/desktop` then `web/desktop/chrome`).
- **Environment** → "against what host" — base URLs, endpoints, env-specific creds. File at `properties/environment/<name>/environment.properties`.
- **Configuration sets** bundle a triple of suite/profile/environment under one preset key (`configuration-set.<key>.suites=...`); activate via `configuration-set.active=<key>`.

**Property precedence** (high → low): `-Pvividus.<key>=v` (Gradle CLI) > `overriding.properties` > `configuration.properties` > suite > profile > environment > plugin defaults. Inside a single tier with multiple entries declared, **first declared wins**.

For full property tables, batch settings, and reporting properties, read `references/configuration.md`.

## Run tests

```bash
# Run with active config from configuration.properties
./gradlew runStories

# Override the triple at the CLI (note the `-Pvividus.` prefix)
./gradlew runStories \
  -Pvividus.configuration.suites=web_app \
  -Pvividus.configuration.profiles=web/desktop/chrome \
  -Pvividus.configuration.environments=staging

# Single-story or pattern run
./gradlew runStories -Pvividus.batch-1.resource-include-patterns=Login*.story

# Filter by Meta tags (Groovy)
./gradlew runStories -Pvividus.bdd.all-meta-filters="groovy: smoke && !skip"

# Inject a variable
./gradlew runStories -Pvividus.variables.user=alice

# Faster local iteration (skips full build validation)
./gradlew debugStories
```

Useful inspection tasks:
- `./gradlew printSteps --args="-f available-steps.txt"` — dump every step the project knows
- `./gradlew countSteps -t 5` — top 5 most-used steps
- `./gradlew countScenarios -d story/web_app` — count under a directory
- `./gradlew validateKnownIssues` — sanity-check `known-issues.json`
- `./gradlew replaceDeprecatedSteps` / `replaceDeprecatedProperties` — auto-migrate to current names
- `./gradlew spotlessApply` — autofix formatting

## Read the report

Allure HTML output goes to `output/reports/allure/index.html`. Browsers refuse to load Allure JSON over `file://`, so serve it:

```bash
# pick one
( cd output/reports/allure && python3 -m http.server 8000 )
# or use VS Code Live Server, or VIVIDUS Studio's "Open Allure Report"
```

Then open http://localhost:8000.

## When something is wrong

Read `references/troubleshooting.md` for the common failures (missing submodule, JDK mismatch, backtick vs quote, locator visibility, suite-property precedence, parallel-story flakiness, MCP-AI hallucinated steps, Allure file:// blank page). It's the fastest path through Vividus's sharp edges.

## Working inside an existing project

When the user already has a Vividus project, before changing anything:
1. **Read `build.gradle`** to confirm the BOM version and which plugins are wired in. Don't add steps from a plugin not on the classpath.
2. **Read `properties/configuration.properties`** to learn the active suites/profiles/environments — your changes must respect the active set.
3. **Skim a few existing `.story` files** to match the project's conventions (locator style, variable scope choice, composite step naming).
4. **For new step phrasings**, run `./gradlew printSteps --args="-f /tmp/steps.txt"` and grep — this is the ground truth for that project.
5. **Run a focused test first** (`-Pvividus.batch-1.resource-include-patterns=YourStory.story`) to validate before broader runs.

This avoids drifting from project norms and catches plugin/version mismatches that would otherwise surface as "step did not match".

## Visual testing

Add `implementation('org.vividus:vividus-plugin-visual')` to `build.gradle`. See `assets/example-visual.story` for a runnable template.

### Step pattern
```gherkin
When I $actionType baseline with name `$name`
When I $actionType baseline with name `$name` ignoring:$checkSettings
```

`$actionType` values:
| Value | What it does |
|---|---|
| `ESTABLISH` | Takes a full-page screenshot and **saves it as the baseline**. Run once to seed, then commit the PNG. |
| `COMPARE_AGAINST` | Takes a fresh screenshot and diffs it against the stored baseline. Fails if diff > threshold. |
| `CHECK_INEQUALITY_AGAINST` | Inverse — fails if the page looks **too similar** (useful for verifying UI changes landed). |

### Ignoring dynamic areas
Pass an ExamplesTable with **exactly one data row**. Combine multiple selectors with a CSS multi-selector when you need to ignore more than one area:

```gherkin
When I COMPARE_AGAINST baseline with name `home` ignoring:
|ELEMENT                                        |
|cssSelector(.cookie-banner, .hero-carousel)    |
```

Columns: `ELEMENT` (locator), `AREA` (pixel region), `ACCEPTABLE_DIFF_PERCENTAGE` (per-check override), `REQUIRED_DIFF_PERCENTAGE`.

> **Gotcha:** `ignoring:` only supports **one data row**. Putting two rows throws `IllegalArgumentException: Only one row of locators to ignore supported`. Use a multi-selector CSS string to cover multiple elements.

### Key properties
```properties
# in profile.properties or environment.properties
ui.visual.acceptable-diff-percentage=2   # allow up to 2% pixel diff (default: 0)
ui.visual.required-diff-percentage=70    # for CHECK_INEQUALITY_AGAINST (default: 70)
ui.visual.baseline-storage.filesystem.folder=./baselines   # relative to src/main/resources
```

> **Gotcha:** The `./baselines` folder must exist as a classpath resource **before** `ESTABLISH` writes. Create `src/main/resources/baselines/.gitkeep` so Gradle packages the (initially empty) directory.

### Workflow
```bash
# 1. Seed baselines (first time or after intentional UI change)
./gradlew runStories -Pvividus.batch-1.resource-include-patterns="Visual.story"

# 2. Copy generated PNGs from output/ back into src/main/resources/baselines/ and commit them

# 3. Regression run (CI)
./gradlew runStories \
  -Pvividus.batch-1.resource-include-patterns="Visual.story" \
  -Pvividus."batch-1.variables.visualAction"=COMPARE_AGAINST
```

Pattern: store `batch-1.variables.visualAction=ESTABLISH` in `suite.properties`; override to `COMPARE_AGAINST` at the CLI for diff runs.

## AI-assisted authoring and the MCP server

The biggest risk when generating Vividus stories with an LLM is **hallucinated step phrasings** — invented steps that look plausible but don't exist, silently becoming "pending" at runtime.

The best defence is the **Vividus MCP server**: it exposes your project's *actual* available steps to the LLM via the Model Context Protocol, so the model can verify phrasings against the real classpath rather than guessing from training data.

### Setup
```gradle
// build.gradle
implementation('org.vividus:vividus-mcp-server')   // available from 0.6.16+
```

```bash
# Start the server (keep running while you author stories)
./gradlew startMcpServer -q -p /path/to/project
```

Then point your AI tool at it:
- **VS Code GitHub Copilot** — add to `.github/copilot-instructions.md` or `mcp.json`
- **Claude Desktop** — add to `claude_desktop_config.json`

Docs: https://docs.vividus.dev/vividus/latest/user-guides/ai.html

### Without the MCP server
If you can't run it, **ground every new step phrasing** before writing it:
1. Check `references/steps-cheatsheet.md`
2. Run `./gradlew printSteps --args="-f /tmp/steps.txt"` and grep
3. Never invent — if a step doesn't appear in `printSteps` output, it doesn't exist

## Reference index

- `references/steps-cheatsheet.md` — exact step phrasings for web, REST, JSON, DB, mobile, lifecycle, composites; locator & comparator syntax
- `references/configuration.md` — suites, profiles, environments, batches, common properties, configuration sets, reporting properties
- `references/plugins.md` — full 47-plugin catalog grouped by domain with use-cases and links
- `references/variables-and-tables.md` — variable scopes, dynamic variables, expressions (`#{...}`), ExamplesTable transformers (FROM_CSV/EXCEL/JSON/DB, FILTERING, MERGING, JOINING, ...)
- `references/troubleshooting.md` — submodule, JDK, backticks, locators, precedence, parallelism, AI-hallucinated steps, Allure viewing

External sources of truth (cite these when uncertain):
- Docs: https://docs.vividus.dev/vividus/latest/
- Core repo: https://github.com/vividus-framework/vividus
- Starter: https://github.com/vividus-framework/vividus-starter
- Sample tests: https://github.com/vividus-framework/vividus-sample-tests
- Releases (current BOM version): https://github.com/vividus-framework/vividus/releases
