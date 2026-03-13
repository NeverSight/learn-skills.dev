---
name: gatling-best-practices
description: "Guides developers and testers in writing, fixing, and structuring Gatling load test scenarios. Use this skill whenever the user mentions load testing, performance testing, stress testing, Gatling, virtual users, VUs, ramp-up, injection profiles, simulations, JMeter migration, k6 migration, throughput, response time SLAs, or wants to benchmark an API or service — even if they don't explicitly say 'Gatling' or 'performance test'."
compatibility: "Claude Code, Cursor, Windsurf. Supports all 5 Gatling languages: Java, Kotlin, Scala (JVM — requires Java 11+, Maven or Gradle) and JavaScript, TypeScript (requires Node.js 18+)."
metadata:
  author: rcampos
  version: "1.0"
---

# Gatling Scenario Builder

Enforces a consistent, production-ready pattern for Gatling simulations across
all five officially supported languages: **Java**, **Kotlin**, **Scala**,
**JavaScript**, and **TypeScript**.

## Output Format

When producing or fixing a simulation, always deliver three things:

1. **A complete, runnable simulation file** for the chosen language — never a
   partial snippet. The user should be able to copy it and run it immediately.
2. **The exact run command** with the environment parameters needed
   (`baseUrl`, `users`, etc.).
3. **A one-line explanation** of the injection profile chosen and why it fits
   the stated load goal.

## Step 1 — Gather context

Ask only what is unknown. Typical questions:

- **Language:** Java (most common) · Kotlin · Scala · JavaScript · TypeScript
- **Build tool:** Maven · Gradle · npm (JS/TS only)
- **Protocol:** HTTP/REST · WebSocket · MQTT · JMS
- **Goal:** New project from scratch · Fix existing simulation · Specific DSL question

**Only load [references/PROTOCOLS.md](references/PROTOCOLS.md) when the user
mentions WebSocket, MQTT, or JMS.** Contains dependency declarations and DSL
for those protocols — non-obvious setup steps the user will likely miss.

**Only load [references/DESIGN-PATTERNS.md](references/DESIGN-PATTERNS.md) when
the user asks about folder structure, project architecture, separation of
concerns, or how to scale beyond a single simulation file.** Contains the
modular layered pattern (Config → Requests → Scenarios → Simulations) with
examples in Java, Scala, and TypeScript.

## Step 2 — New project? Use the scaffold script

The scaffold script is **interactive** — it requires keyboard input and cannot
be run non-interactively. **Tell the user to run it themselves** in their
terminal; do NOT attempt to execute it with the Bash tool:

```bash
# macOS / Linux
bash scripts/scaffold.sh

# Windows
.\scripts\scaffold.ps1
```

If the user asks you to generate the project directly (without running the
script), skip to Step 3 and create the files manually following the 5-block
pattern.

**Kotlin + Gradle — minimum required files:**

`build.gradle.kts` — three omissions cause build failures every time:

```kotlin
plugins {
    kotlin("jvm") version "2.0.21"              // ① must come BEFORE the Gatling plugin
    id("io.gatling.gradle") version "3.14.5"
}

group = "perf"
version = "1.0.0-SNAPSHOT"

repositories {
    mavenCentral()                               // ② required — often forgotten
}

gatling {
    jvmArgs = listOf(
        "-Xms512m", "-Xmx2g",
        "--add-opens=java.base/java.lang=ALL-UNNAMED"  // ③ Java 21+ module restriction
    )
}

dependencies {
    gatling("io.gatling.highcharts:gatling-charts-highcharts:3.14.5")
}
```

Source directories (Gatling Gradle plugin — **not** `src/test/`):
- Kotlin simulations → `src/gatling/kotlin/<package>/`
- Resources (gatling.conf, feeders) → `src/gatling/resources/`

**For JS/TS projects**, the minimum required files are:
- `package.json` with `"type": "module"` and deps `@gatling.io/cli`, `@gatling.io/core`, `@gatling.io/http`
- `src/<SimulationName>.gatling.js` (or `.gatling.ts`) — file must be in `src/`
  directly with the `.gatling.js` / `.gatling.ts` suffix (required by the CLI)
- `tsconfig.json` — **TypeScript only**, required by `esbuild-plugin-tsc`; omitting
  it causes `failed to open 'undefined'` at bundle time

After scaffolding — or whenever the user shares an existing Gatling project —
execute the validator with the Bash tool (do not read it, only the output
consumes tokens):

```bash
bash scripts/validate.sh [project-dir]
```

Report the results. The script catches the five most common configuration
problems before the user wastes time on a broken run.

## Step 3 — Apply the 5-block pattern

Every simulation must have these five blocks in this order. Generate the
complete skeleton for the chosen language first, then fill in the details —
starting from a partial file leads to structural errors.

```
Block 1 → Protocol    baseUrl, headers, connection settings
Block 2 → Feeders     test data injected per virtual user
Block 3 → Scenario    ordered chain of requests with pauses and checks
Block 4 → Injection   how many users, at what rate, for how long
Block 5 → Assertions  pass/fail thresholds (success rate, response time p95)
```

---

## Common Mistakes — Check Every Simulation for These

These five errors appear in almost every first-draft Gatling simulation. Scan
for them before delivering any code.

### 1. Missing `pause()` between requests

Without think time, all requests fire at the maximum possible rate, generating
10–100× more load than real users would. This makes results meaningless and
can crash the system under test.

```java
// Wrong
scenario("Flow").exec(http("A").get("/a")).exec(http("B").get("/b"))

// Correct — add realistic think time between actions
scenario("Flow").exec(http("A").get("/a")).pause(1, 3).exec(http("B").get("/b"))
```

### 2. Hardcoded dynamic tokens

Hardcoded tokens mean every virtual user sends the same session — the server
sees one user repeated, not many distinct users. CSRF tokens and JWTs are
server-side validated; they must come from the actual login response.

```java
// Wrong — static token shared across all users
.header("Authorization", "Bearer eyJhbGciOiJIUzI1NiJ9.abc123")

// Correct — extract per user from the login response
.exec(http("Login").post("/auth/login")
    .check(jsonPath("$.token").saveAs("token")))
.exec(http("API Call").get("/data")
    .header("Authorization", "Bearer #{token}"))
```

### 3. `atOnceUsers` for load tests

`atOnceUsers` fires all users simultaneously. It is only appropriate for smoke
tests (2–5 users). Using it for real load tests generates an unrealistic spike
that tells you nothing about capacity.

```java
// Wrong — not a load test, just a spike
setUp(scn.injectOpen(atOnceUsers(100)))

// Correct — ramp up, then hold to measure steady-state capacity
setUp(scn.injectOpen(
    rampUsers(100).during(60),
    constantUsersPerSec(10).during(120)
))
```

### 4. No assertions

Without assertions, Gatling exits with code `0` (success) even if every
request returns 500. This means CI/CD pipelines never catch performance
regressions. Define what "passing" looks like before the test runs.

```java
// Wrong — always exits 0 regardless of results
setUp(scn.inject(...).protocols(httpProtocol))

// Correct — fail the build if thresholds are breached
setUp(scn.inject(...).protocols(httpProtocol))
    .assertions(
        global().successfulRequests().percent().gt(99.0),
        global().responseTime().percentile(95).lt(1000)
    )
```

### 5. `.queue()` feeder strategy for long tests

`.queue()` consumes each CSV record once, in order. When the file runs out,
the test fails mid-run. Use `.circular()` for any test that may run longer
than the number of records allows.

```java
// Wrong — crashes when file is exhausted
FeederBuilder<String> f = csv("data/users.csv").queue()

// Correct for sustained tests — loops back to the start
FeederBuilder<String> f = csv("data/users.csv").circular()

// Use .queue() only when each record must be unique (e.g., user registration)
```

### 6. Check failure marks the request as FAILED

A `.check()` that doesn't find its target fails the entire request — even if
the server responded 200. This silently inflates error rates and hides the real
problem: the field was absent or the path was wrong.

```java
// Wrong — if $.token is absent (e.g., login failed), request is marked FAILED
.check(jsonPath("$.token").saveAs("token"))

// Correct — validate existence first so the error message is meaningful
.check(status().is(200))
.check(jsonPath("$.token").exists())
.check(jsonPath("$.token").saveAs("token"))

// When the field is genuinely optional — use .optional() to avoid false failures
.check(jsonPath("$.refreshToken").optional().saveAs("refreshToken"))
```

### 7. Missing `Content-Type` when sending a request body

Forgetting `Content-Type` on POST/PUT requests causes the server to reject with
`415 Unsupported Media Type`. Use `.asJson()` — it sets both `Content-Type` and
`Accept` headers in one call.

```java
// Wrong — server returns 415
.post("/api/users").body(StringBody("""{"name":"#{name}"}"""))

// Correct — use .asJson() shorthand (Java / Kotlin only)
.post("/api/users").body(StringBody("""{"name":"#{name}"}""")).asJson()

// Equivalent explicit form
.post("/api/users")
    .header("Content-Type", "application/json")
    .body(StringBody("""{"name":"#{name}"}"""))
```

**Scala note:** `.asJson()` does **not** chain after `.body()` in Scala — it causes a compile error. Set `Content-Type` on the protocol instead:

```scala
// Scala — set contentTypeHeader on the protocol, not per-request
val httpProtocol = http
  .baseUrl(sys.props.getOrElse("baseUrl", "https://api.example.com"))
  .acceptHeader("application/json")
  .contentTypeHeader("application/json")  // applies to all requests

// Then just use .body() without .asJson():
http("POST Login").post("/api/auth/login")
  .body(StringBody("""{"email":"#{email}","password":"#{password}"}"""))
  .check(status.is(200))
```

---

## The 5-Block Pattern — Reference

### Block 1: Protocol

```java
// Java / Kotlin
HttpProtocolBuilder httpProtocol = http
    .baseUrl(System.getProperty("baseUrl", "https://api.example.com"))
    .acceptHeader("application/json")
    .contentTypeHeader("application/json");
```

```scala
// Scala
val httpProtocol = http
  .baseUrl(sys.props.getOrElse("baseUrl", "https://api.example.com"))
  .acceptHeader("application/json")
```

```typescript
// TypeScript / JavaScript
// File must be named *.gatling.ts / *.gatling.js and placed directly in src/
import {
  simulation, scenario, rampUsers, csv, global,
  StringBody, jsonPath, getEnvironmentVariable,  // ← jsonPath and StringBody live here, NOT in @gatling.io/http
} from "@gatling.io/core";
import { http, status } from "@gatling.io/http";  // ← do NOT import jsonPath from here — it is not exported

// process.env is NOT available at GraalVM runtime — use getEnvironmentVariable instead
const httpProtocol = http
  .baseUrl(getEnvironmentVariable("BASE_URL", "https://api.example.com"))
  .acceptHeader("application/json");
```

### Block 2: Feeders

```java
csv("data/users.csv").circular()  // sustained tests: loops forever (recommended)
csv("data/users.csv").random()    // picks records randomly, allows repeats
csv("data/users.csv").queue()     // each record used once — only for unique data
csv("data/users.csv").shuffle()   // random order, each used once

// Programmatic feeder — when each user needs a unique generated value
Iterator<Map<String, Object>> feeder =
    Stream.generate(() -> Map.<String, Object>of("id", UUID.randomUUID().toString()))
          .iterator();
```

### Block 3: Scenario

```java
// Java
ScenarioBuilder scn = scenario("My Flow")
    .feed(userFeeder)
    .exec(http("POST Login")
        .post("/auth/login")
        .body(StringBody("""{"username":"#{username}","password":"#{password}"}"""))
        .check(status().is(200))
        .check(jsonPath("$.token").saveAs("token")))   // extract token for reuse
    .pause(1, 3)                                        // think time
    .exec(http("GET Data")
        .get("/data")
        .header("Authorization", "Bearer #{token}")    // inject extracted token
        .check(status().is(200))
        .check(jsonPath("$.id").saveAs("resourceId")))
    .pause(1)
    .exec(http("POST Action")
        .post("/actions")
        .header("Authorization", "Bearer #{token}")
        .body(StringBody("""{"resourceId":"#{resourceId}"}"""))
        .check(status().is(201)));
```

```typescript
// TypeScript
const scn = scenario("My Flow")
  .feed(userFeeder)
  .exec(http("POST Login").post("/auth/login")
    .body(StringBody('{"username":"#{username}","password":"#{password}"}'))  // ← StringBody required; raw string causes NullPointerException
    .asJson()                                                                   // ← sets Content-Type: application/json
    .check(status().is(200))
    .check(jsonPath("$.token").exists())
    .check(jsonPath("$.token").saveAs("token")))
  .pause(1, 3)
  .exec(http("GET Data").get("/data")
    .header("Authorization", "Bearer #{token}")
    .check(status().is(200)));
```

Loops and conditionals:

```java
repeat(3).on(exec(http("Poll").get("/status")))                    // fixed iterations
during(Duration.ofSeconds(30)).on(                                  // time-based loop
    exec(http("Ping").get("/ping")).pause(5))
doIf("#{isPremium}").then(exec(http("VIP").get("/vip")))           // conditional branch
randomSwitch().on(                                                   // weighted paths
    percent(60.0).exec(http("Browse").get("/products")),
    percent(40.0).exec(http("Search").get("/search")))
group("Checkout Flow").on(                                          // group for cleaner reports
    exec(http("Cart").get("/cart"))
        .exec(http("Pay").post("/pay")))
```

### Block 4: Injection Profiles

Choose the profile that matches the test goal — using the wrong one produces
misleading results.

**`injectOpen`** — controls *arrival rate* (new users/second). Default for web APIs and stateless services.

| Profile | Command | When to use |
|---|---|---|
| Spike (smoke only) | `atOnceUsers(5)` | Verify the test runs — not a load test |
| Ramp | `rampUsers(100).during(60)` | Standard load test |
| Steady rate | `constantUsersPerSec(20).during(120)` | Capacity / soak test |
| Accelerating | `rampUsersPerSec(5).to(50).during(60)` | Finding the breaking point |
| Stress peak | `stressPeakUsers(500).during(30)` | Stress test |
| Stairs | `incrementUsersPerSec(5).times(5).eachLevelLasting(30)` | Progressive capacity |

**`injectClosed`** — controls *concurrent count* (users active simultaneously). Use for systems with connection pools, queues, or session limits.

| Profile | Command | When to use |
|---|---|---|
| Constant concurrent | `constantConcurrentUsers(50).during(120)` | Fixed connection pool size |
| Ramp concurrent | `rampConcurrentUsers(10).to(50).during(60)` | Gradual concurrency increase |
| Stairs concurrent | `incrementConcurrentUsers(5).times(5).eachLevelLasting(30)` | Progressive capacity (closed) |

**Scala note:** use `.inject(...)` — Scala has no `injectOpen`/`injectClosed` distinction at the call site; the step type determines the model.

**Throttling — cap RPS regardless of user count:**

Use `.throttle()` when the goal is to test at a fixed request rate rather than
a fixed user count. It overrides injection and is useful for SLA compliance tests.

```java
setUp(scn.injectOpen(constantUsersPerSec(50).during(Duration.ofMinutes(10))))
    .throttle(
        reachRps(100).in(Duration.ofSeconds(10)),  // ramp to 100 RPS over 10s
        holdFor(Duration.ofMinutes(5))              // hold at 100 RPS for 5 min
    )
    .protocols(httpProtocol);
```

**Pause distributions — choose based on realism needed:**

```java
.pause(1, 3)                                    // uniform: between 1-3s (default)
.pause(Duration.ofSeconds(2),
       PauseType.EXPONENTIAL)                   // exponential: closer to real user behavior
.pace(Duration.ofSeconds(5))                    // cadence: fixed cycle regardless of response time
```

### Block 5: Assertions

Assertions turn the test into a pass/fail gate. Without them, the test is just
an observation. Include at minimum the first line; add per-endpoint assertions
for critical paths.

```java
.assertions(
    global().failedRequests().count().lt(1L),           // minimum: zero errors
    global().successfulRequests().percent().gt(99.0),   // success rate
    global().responseTime().percentile(95).lt(1000),    // p95 < 1s
    global().responseTime().percentile(99).lt(2000),    // p99 < 2s
    global().requestsPerSec().gt(50.0),                 // throughput floor
    details("POST Login").responseTime().percentile(99).lt(500)  // per-endpoint
)
```

Use `percentile(95)` and `percentile(99)`, not `mean()`. Mean hides the tail:
a p99 of 10 seconds is invisible when mean is 200ms.

**Kotlin note:** `percentile()` requires a `Double` argument — write
`.percentile(95.0).lt(1000)`, not `.percentile(95).lt(1000)` (Int causes a
compile error in Kotlin even though Java accepts it via widening).

**Scala note:** assertion methods (`global`, `responseTime`, `successfulRequests`,
`percent`) are zero-arg methods with an implicit `GatlingConfiguration` parameter.
Call them **without parentheses** — `global()` is a compile error in Scala:

```scala
// Wrong — compile error: "not enough arguments for method global"
global().successfulRequests().percent().gt(99.0)

// Correct — no () on zero-arg methods with implicit params
global.successfulRequests.percent.gt(99.0)
global.responseTime.percentile(95).lt(800)
details("POST Login").responseTime.percentile(99).lt(300)
```

---

## Run Commands

```bash
# Maven
mvn gatling:test -Dgatling.simulationClass=perf.MySimulation \
                 -DbaseUrl=https://staging.example.com -Dusers=50

# Gradle — plugin 3.14+ supports Gradle 9; use ./gradlew (or gradle) directly
./gradlew gatlingRun                              # runs all simulations
./gradlew gatlingRun-perf.MySimulation            # specific class (plugin ≥ 3.14 only)

# TypeScript / JavaScript  (use simulation name, not file path)
BASE_URL=https://staging.example.com USERS=50 \
  npx gatling run --simulation MySimulation
```

Reports open at: `target/gatling/<simulation>-<timestamp>/index.html`

---

## References

- [Scenario DSL](https://docs.gatling.io/concepts/scenario/)
- [Injection Profiles](https://docs.gatling.io/concepts/injection/)
- [Checks](https://docs.gatling.io/concepts/checks/)
- [Feeders](https://docs.gatling.io/concepts/session/feeders/)
- [Assertions](https://docs.gatling.io/concepts/assertions/)
- [WebSocket / MQTT / JMS](references/PROTOCOLS.md)
- [Modular Design Patterns](references/DESIGN-PATTERNS.md)
