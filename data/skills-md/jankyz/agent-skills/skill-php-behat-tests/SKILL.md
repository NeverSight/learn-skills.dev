---
name: skill-php-behat-tests
description: Write, extend, debug, and run Behat (Gherkin) behavioral tests in PHP/Symfony projects. Use when adding or changing `.feature` scenarios, implementing/adjusting step definitions (contexts), fixing failing Behat runs, or wiring Behat to run locally or in Docker while matching project PHP/Symfony versions. Prioritize business language in scenarios (user intent and business outcomes over technical transport details).
---

# PHP Behat Tests Skill

Keywords (GitHub): behat, gherkin, bdd, php, symfony, feature files, step definitions, contexts, docker

## Quick Start

1. Find where Behat lives:
   - `behat.yml` / `behat.yml.dist`
   - `features/` directory
   - step definitions: commonly `tests/Behat/Context/*Context.php`
2. Pick the correct PHP runtime (critical):
   - Prefer the project-defined PHP version (`composer.json`) over your local PHP.
3. Run Behat tests before changes to get a regression baseline.
4. Draft/rename scenarios in business language first (actor + business action + business outcome).
5. Add/modify scenarios in `.feature` files.
6. Add/modify step definitions only after scenario language is stable.
7. Run only what you changed (single file or single scenario line).

## Environment Discovery (PHP + Symfony + Behat)

### Detect PHP version (in order)

Run these checks and use the first match:

- `composer.json`:
  - `config.platform.php` (strongest signal)
  - `require.php`
- `Dockerfile`:
  - `ARG PHP_VERSION=...`
  - base image tag (e.g. `php:8.2-fpm`)
- `compose.yml` / `docker-compose.yml`:
  - `image:` tag for PHP service

Fast command:
```bash
rg -n "\"php\"\s*:\s*|platform\"\s*:\s*\{|PHP_VERSION|FROM php:|image:\s*.*php" composer.json Dockerfile compose*.yml docker-compose*.yml -S
```

### Detect Symfony version

Use `composer.lock` to avoid guesswork:
```bash
rg -n "\"name\":\s*\"symfony/framework-bundle\"|\"symfony\":\s*\{" composer.lock composer.json -S
```

### Detect Behat/Gherkin version (parser capabilities)

Different versions support different Gherkin keywords/structures. Confirm what you have:
```bash
rg -n "\"name\":\s*\"behat/behat\"|\"behat/gherkin\"" composer.lock -S
```

## Writing Scenarios (.feature)

### Business Language First (mandatory)

Scenarios must be written as business behavior, not technical implementation.

- Write `Feature`, `Rule`, and `Scenario` names as user/business outcomes.
- Use domain actors and intent: customer, guest user, signed-in customer, repayment customer.
- Keep low-level details out of scenario text: HTTP method, route path, headers, service names, manager interfaces.
- Move technical mapping to step definitions/contexts.
- Use technical wording in `.feature` only when the transport contract itself is the business requirement.

Examples:

- Bad: `GET /hello/my-account/profile returns 302 for anonymous user`
- Good: `Guest user is redirected to login before opening profile page`

- Bad: `POST /hello/my-account/income-update/form returns 200 on invalid payload`
- Good: `Customer stays on income update form when provided data is invalid`

### Step Text Alignment (mandatory style)

In `.feature` files, align the business text so it starts in the same column for all step keywords.

- Keep one space between keyword and step text.
- Adjust left padding before keyword based on keyword length.
- Use this formula for steps: `left_pad = base_pad + (5 - keyword_length)` where `base_pad` is the `Given` indentation.
- Practical result:
  - `Given` uses base indentation.
  - `When` and `Then` have one extra leading space.
  - `And` and `But` have two extra leading spaces.

Formatting example:

```gherkin
        Scenario: Customer stays on MyAccount page when no redirect applies
            Given customer is not eligible for next application and has no active current loan
             When I open MyAccount main page
             Then I should stay on MyAccount main page
              And I should see "MyAccount main page"
```

Apply formatter after edits:

```bash
~/.codex/skills/skill-php-behat-tests/scripts/format_feature_step_alignment.py features
```

Check mode (CI/pre-commit):

```bash
~/.codex/skills/skill-php-behat-tests/scripts/format_feature_step_alignment.py --check features
```

### Keep steps readable and domain-oriented

- `Given`: business preconditions/state.
- `When`: business action.
- `Then`: observable business outcome.
- Prefer verbs such as: `opens`, `submits`, `is redirected`, `can access`, `cannot access`, `sees`.
- Avoid exposing implementation details in step text (e.g. `X-Original-URI`, `AccountDetailsManagerInterface`).

### Keep state consistent

- Use `Background` for stable setup (e.g. signed-in customer).
- Avoid overriding auth state inside a scenario if file-level `Background` already defines it.
- If both authenticated and anonymous coverage is needed, prefer separate feature files (or suites).

### Encode business priority explicitly

If logic has priority rules (e.g. redirect A before redirect B), add a scenario where both conditions are true to lock the intended business priority.

### Keep assertions stable

- For redirects: assert status code and `Location` header.
- For response contracts: assert stable headers and minimal JSON/PDF shape.
- Avoid brittle UI assertions unless markup stability is guaranteed.

## Step Definitions (Contexts)

### Reuse before adding

Before creating a new step, search existing definitions:
```bash
rg -n "@Given|@When|@Then" tests features -S
rg -n "function\s+.*\(" tests/Behat/Context features/bootstrap -S
```

### Where to put new steps

- Prefer existing context class that matches the domain (e.g. `MyAccountContext`, `AuthContext`, `HttpContext`).
- Keep shared helpers in base/shared contexts.
- Keep transport details in context methods, not in `.feature` prose.

### Avoid flaky steps

- Reset mutable state in `@BeforeScenario`.
- Make service retrieval explicit and type-safe.
- Keep steps small and single-purpose.

## Running Behat

### Prefer composer scripts if available

If `composer.json` defines scripts like `test-behat-local`/`test-behat-ci`, use them.

Discover scripts:
```bash
rg -n "test-behat" composer.json -S
```

### Local run (no Docker)

Typical:
```bash
bin/behat -c behat.yml.dist features/path/to.feature
```

### Docker run (recommended when repo is Docker-based)

Use the detected PHP version and the repo standard image.

Typical:
```bash
docker run --rm -v "$PWD":/app -w /app <php-image> bin/behat -c behat.yml.dist features/path/to.feature
```

Default convention (if repo does not define image in compose files):
```bash
docker run --rm -v "$PWD":/app -w /app wodby/php:<major.minor> bin/behat -c behat.yml.dist features/path/to.feature
```

### Target a single scenario quickly

Use file + line number:
```bash
bin/behat -c behat.yml.dist features/foo.feature:42
```

## Debugging Checklist

- If you expected `401` but got `302`, you likely hit firewall entry-point behavior.
- If Behat rejects multiple path arguments, run per file, a suite (`-s <suite>`), or the `features/` directory.

## Resources

### scripts/
- `scripts/suggest_behat_docker_cmd.sh`: best-effort command suggestion for Docker-based runs.
- `scripts/format_feature_step_alignment.py`: align `Given/When/Then/And/But` text column in `.feature` files; supports `--check`.
