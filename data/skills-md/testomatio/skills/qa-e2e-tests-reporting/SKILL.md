---
name: qa-e2e-tests-reporting
description: Install and configure Testomat.io reporting in a test automation project when a user needs to integrate their tests with Testomat.io. Detect the testing framework (e.g., Playwright, CodeceptJS, Jest, Mocha, WebdriverIO, JUnit, Pytest, XML, etc) and automatically set up the appropriate reporter so test results are sent to the Testomat.io TMS.
license: MIT
metadata:
  author: Testomat.io
  version: 1.0.0
---

# Testomat.io Reporter Setup

Install and configure the Testomat.io reporter in an automation project, then push test results to the Testomat.io TMS.

## Step 1: Detect Language & Framework

- Detect the language from the project manifest (`package.json`, `pyproject.toml`/`requirements.txt`, `pom.xml`/`build.gradle`, `*.csproj`, `composer.json`, `Gemfile`).
- Detect the framework from its config file: `playwright.config.*`, `codecept.conf.js`, `wdio.conf.*`, `jest.config.*`, `.mocharc.*`, `pytest.ini`/`conftest.py`, `*.robot`/`robot.toml`, `testng.xml`/JUnit deps in `pom.xml`.
- No native reporter for the stack (C#, PHP, Ruby, Go, etc.): use JUnit XML import (Step 4).

## Step 2: Configure Credentials

- Check `.env` for a `TESTOMATIO` API key. If present, use it.
- If missing, add a placeholder line to `.env`:

```env
TESTOMATIO=tstmt_xxxxx
```

- **Ask the user to replace the placeholder with their "Project Reporting API key" themselves — never ask them to paste the key into chat.**

Message to the user:

```
✅ Added `TESTOMATIO=tstmt_xxxxx` placeholder to .env

To activate reporting:
1. Go to Testomat.io → your project → Settings → Project
   (https://app.testomat.io/projects/<project-id>/settings/project)
2. Copy "Project Reporting API key"
3. Replace `tstmt_xxxxx` in .env with your actual key
4. Run tests: TESTOMATIO=tstmt_xxxxx npx <test-command>
```

## Step 3: Install & Configure Reporter

Pick the section for the detected language and framework.

### JavaScript / TypeScript

Use `@testomatio/reporter`:

```bash
npm install @testomatio/reporter --save-dev
```

Playwright — `playwright.config.ts` or `playwright.config.js`:

```js
reporter: [
  ['@testomatio/reporter/playwright'],
  // other reporters...
],
```

CodeceptJS — `codecept.conf.js` or `codecept.config.js`:

```js
plugins: {
  testomatio: {
    enabled: true,
    require: '@testomatio/reporter/codecept',
  }
}
```

WebdriverIO — `wdio.conf.js`:

```js
import testomatio from '@testomatio/reporter/webdriver';

exports.config = {
  // ...
  reporters: [
    [testomatio, { apiKey: process.env.TESTOMATIO }],
  ],
};
```

Jest — `jest.config.js` or `jest.config.ts`:

```js
module.exports = {
  reporters: ['default', ['@testomatio/reporter/jest', { apiKey: process.env.TESTOMATIO }]],
};
```

Mocha — run with CLI flags:

```bash
mocha --reporter @testomatio/reporter/mocha --reporter-options apiKey=tstmt_xxx
```

- Run commands and more config options: [./references/TESTOMATIO_REPORTERS_CONFIG.md](./references/TESTOMATIO_REPORTERS_CONFIG.md)
- Docs: [Testomat.io NodeJS Frameworks](https://docs.testomat.io/test-reporting/frameworks/)

### Python

Use `pytestomatio` for pytest, `robot-framework-reporter` for Robot Framework.

- Use `pip3` if Python 2.x and 3.x coexist.

pytest:

```bash
pip install pytestomatio

# Run and report tests
pytest --testomatio report
```

Robot Framework:

```bash
pip install robot-framework-reporter

# Run and report tests
robot --listener Testomatio.Report path/to/tests
```

Docs: [Testomat.io Python Reporting](https://docs.testomat.io/test-reporting/python/)

### Java (JUnit, TestNG, Cucumber, Karate)

Use the `io.testomat` Java reporters.

- Ask the user to set the API key before running tests, then verify it is set and starts with `tstmt_`:

```bash
export TESTOMATIO=<tstmt_api_key>
```

- Add the dependency for the framework in use:

```xml
<dependency>
  <groupId>io.testomat</groupId>
  <artifactId>java-reporter-junit</artifactId>
  <version>{LATEST_STABLE_VERSION}</version>
</dependency>
```

Artifact IDs: `java-reporter-junit`, `java-reporter-testng`, `java-reporter-cucumber`, `java-reporter-karate`.

- Run tests:

```bash
mvn clean test
```

- Scan the output for a run ID. If found, show the link:

```
View results: https://app.testomat.io/projects/{project-id}/runs/{run-id}
```

Docs: [Testomat.io Java/JUnit Reporting](https://docs.testomat.io/test-reporting/junit/)

## Step 4: Import Automated Tests to Testomat.io TMS

Import test source code into Testomat.io to see test structure and enable codebase-TMS synchronization.

Docs: [Testomat.io Import Overview](https://docs.testomat.io/project/import-export/)

### JavaScript / TypeScript

Use the `check-tests` CLI:

```bash
npx check-tests@latest <framework> "<glob-pattern>" [options]
```

| Framework   | Example |
|-------------|---------|
| Playwright  | `npx check-tests@latest Playwright "tests/**/*.spec.js"` |
| CodeceptJS  | `npx check-tests@latest CodeceptJS "tests/**_test.js"` |
| Cypress     | `npx check-tests@latest cypress "cypress/e2e/**/*.js"` |
| Jest        | `npx check-tests@latest Jest "tests/**/*.test.js"` |
| Mocha       | `npx check-tests@latest mocha "test/**/*_test.js"` |
| WebdriverIO | `npx check-tests@latest webdriverio "test/**/*.js"` |

Options:

- `--typescript` — for TypeScript projects: `npx check-tests@latest Playwright "tests/**/*.spec.ts" --typescript`
- `--update-ids` — sync and auto-assign test IDs in source code: `npx check-tests@latest CodeceptJS "tests/**_test.js" --update-ids`

### Python

pytest — sync tests with Testomat.io:

```bash
pytest --testomatio sync
```

Robot Framework — import tests:

```bash
robot --listener Testomatio.Import path/to/tests
```

### Java (JUnit, TestNG)

Use the `testomatio.jar` CLI. Re-run after every test execution.

- **Run only from the project root:**

```bash
cd <project-root>

export TESTOMATIO=tstmt_xxxxx && \
curl -L -O https://github.com/testomatio/java-check-tests/releases/latest/download/testomatio.jar && \
java -jar testomatio.jar sync
```

Commands:

- `import` — import test code to Testomat.io (dry-run without API key).
- `clean-ids` — import tests without system ids.
- `sync` — import tests and pull IDs into source code (alias: `update-ids`).

### JUnit XML (C#, PHP, Ruby, Go, etc.)

For stacks without a native reporter, generate a JUnit XML report, then import it.

- NUnit (C#): `dotnet test --logger:"trx;LogFileName=results.xml"` — convert to JUnit XML if needed.
- PHPUnit (PHP): `./vendor/bin/phpunit --log-junit=results.xml`
- RSpec (Ruby): `rspec --format json --out results.json` — then convert to JUnit XML.

Import to Testomat.io:

```bash
npx check-tests@latest junit "path/to/results.xml"

# Multiple XML files
npx check-tests@latest junit "results/*.xml"
```

## Step 5: Verify Setup

Run the tests with the reporter enabled:

```bash
TESTOMATIO=tstmt_xxxxx npx <your-test-command>
```

### Via Testomat.io MCP (preferred, if enabled)

- After the run, fetch the latest run via MCP to confirm data was received.
- Success indicators: a new run ID appears in the logs; run status shows passed/failed as expected; the run is retrievable by its ID.
- Setup is complete when the new run is fetchable via MCP.
- MCP tools: [Testomat.io MCP Run Management](https://github.com/testomatio/mcp/blob/main/docs/tools.md#run-management)

### Debug Mode (alternative)

- Capture reporter output locally **for only 1-2 tests** to verify data is generated correctly before sending:

```bash
DEBUG=@testomatio/reporter:pipe:testomatio npx <your-test-command>
```

- Read the execution logs to confirm the reporter is enabled and configured.
- Docs: [Testomat.io Debugging Logs](https://docs.testomat.io/not-in-use/debugging/)

## Step 6: Configure Artifacts (only on explicit request)

Store screenshots, videos, traces, and logs in S3-compatible storage alongside test results.

- **Only perform this step if the user explicitly asks for artifacts configuration** (or mentions saving screenshots, videos, traces, logs).
- Prerequisite: first test report executed successfully.
- Check `.env` for existing S3 credentials (`S3_ACCESS_KEY_ID`, `S3_BUCKET`, `S3_REGION`). If present, skip to verification.

### Create S3 Bucket (if needed)

- Recommended: one bucket per project.
- Guide the user through their provider, based on official documentation:

| Provider | Link |
|----------|------|
| AWS S3 | https://s3.console.aws.amazon.com/s3 |
| DigitalOcean | https://cloud.digitalocean.com/spaces |
| Google Cloud Storage | https://console.cloud.google.com/storage |
| Cloudflare R2 | https://dash.cloudflare.com/ |
| Minio | Self-hosted or cloud instance |

- The user obtains the Access Key ID and Secret Access Key from the provider.

### Option A: Testomat.io UI (recommended)

- **The agent cannot access Testomat.io project settings — the user configures this manually:**
  1. Open `https://app.testomat.io/projects/<project-id>/settings/artifacts`
  2. Enable the "Share credentials" toggle.
  3. Enter Access Key ID, Secret Access Key, bucket name, region, and endpoint (endpoint only for non-AWS providers).

### Option B: Environment Variables

Add S3 credentials to `.env` or the CI pipeline:

```env
# Required for all providers
S3_ACCESS_KEY_ID=your_access_key
S3_SECRET_ACCESS_KEY=your_secret_key
S3_BUCKET=your_bucket_name
S3_REGION=us-west-1

# Optional: for non-AWS providers (DigitalOcean, Minio, Cloudflare R2, GCS)
S3_ENDPOINT=https://your-endpoint-url

# Optional: private access mode (recommended)
TESTOMATIO_PRIVATE_ARTIFACTS=1
```

Cloudflare R2 example:

```env
S3_ACCESS_KEY_ID=xxx
S3_SECRET_ACCESS_KEY=xxx
S3_BUCKET=testomatio-artifacts
S3_REGION=auto
S3_ENDPOINT=https://<account-id>.r2.cloudflarestorage.com
S3_FORCE_PATH_STYLE=true
```

- Disable uploads: `TESTOMATIO_DISABLE_ARTIFACTS=1`
- Provider examples (AWS, DigitalOcean, Minio, GCS): [./references/TESTOMATIO_ARTIFACTS.md](./references/TESTOMATIO_ARTIFACTS.md)
- More options: [Testomat.io Artifacts](https://docs.testomat.io/test-reporting/artifacts/)

### Verify Artifacts

- Run tests that produce screenshots, videos, or traces: `TESTOMATIO=tstmt_xxxxx npx <your-test-command>`
- Ask the user to open `https://app.testomat.io/projects/<project-id>/runs` and click a test with artifacts (failed tests typically have screenshots).
- Success: artifacts appear in the test results ("Artifacts" section or attachment icon) and are clickable; Playwright traces open in the trace viewer.

## References

| Description | Link |
|-------------|------|
| Getting started | https://docs.testomat.io/getting-started/ |
| Reporter configuration | https://docs.testomat.io/test-reporting/frameworks/ |
| Framework config snippets | [./references/TESTOMATIO_REPORTERS_CONFIG.md](./references/TESTOMATIO_REPORTERS_CONFIG.md) |
| Python test reporting | https://docs.testomat.io/test-reporting/python/ |
| Python Robot Framework | https://github.com/testomatio/robot-framework-reporter/blob/master/README.md |
| Java/JUnit reporting | https://docs.testomat.io/test-reporting/junit/ |
| HTML pipe | [./references/TESTOMATIO_HTML_REPORT.md](./references/TESTOMATIO_HTML_REPORT.md) |
| Debug pipe | `TESTOMATIO_DEBUG=1 <test-command>` |
| Artifacts (S3) | [./references/TESTOMATIO_ARTIFACTS.md](./references/TESTOMATIO_ARTIFACTS.md) |
