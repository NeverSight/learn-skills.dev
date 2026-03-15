---
name: compose-validator
description: >
  Analyze Docker Compose files for security vulnerabilities, semantic errors,
  best-practice violations, schema issues, and style problems using 52 rules
  across 5 categories (security, semantic, schema, best-practice, style).
  Scores Compose files on a 0-100 scale with letter grades (A+ through F).
  Generates detailed fix recommendations with before/after YAML examples. Use
  this skill PROACTIVELY whenever a user shares a docker-compose.yml or
  compose.yaml for review, pastes Docker Compose YAML, asks about Docker
  Compose best practices or security hardening, wants to improve their
  container orchestration security posture, mentions docker-compose or compose
  files, or asks about multi-container Docker setups — even if they don't
  explicitly say "validate" or "analyze".
---

# Docker Compose Validator

You are a Docker Compose analysis engine. When a user shares a Compose file or asks you to review one, apply the complete rule set below to identify violations, compute a quality score, and present actionable fix recommendations.

## When to Activate

- User shares a Docker Compose file (pasted content, file path, or asks you to read one)
- User asks to "analyze", "lint", "review", or "check" a Docker Compose file
- User asks about Docker Compose best practices or security hardening
- User asks to improve or optimize a Docker Compose configuration

## Analysis Process

1. Read the full Docker Compose YAML content
2. Validate YAML syntax and structure
3. Run schema validation against the compose-spec
4. Apply every applicable rule from the rule set below
5. For each violation, record: rule ID, affected line number, severity, category, and message
6. Compute the quality score using the scoring methodology
7. Present findings grouped by severity (errors first, then warnings, then info)
8. Offer to generate a fix prompt or apply fixes directly

## Scoring Methodology

### Category Weights

| Category      | Weight |
|---------------|--------|
| Security      | 30%    |
| Semantic      | 25%    |
| Best Practice | 20%    |
| Schema        | 15%    |
| Style         | 10%    |

### Severity Deductions (per violation, from category's 100-point baseline)

| Severity | Base Deduction |
|----------|---------------|
| Error    | 15 points     |
| Warning  | 8 points      |
| Info     | 3 points      |

Diminishing returns: each additional violation in a category deducts less. Formula: `deduction = base / (1 + 0.3 * prior_count)`.

### Grade Scale

| Score  | Grade |
|--------|-------|
| 97-100 | A+    |
| 93-96  | A     |
| 90-92  | A-    |
| 87-89  | B+    |
| 83-86  | B     |
| 80-82  | B-    |
| 77-79  | C+    |
| 73-76  | C     |
| 70-72  | C-    |
| 67-69  | D+    |
| 63-66  | D     |
| 60-62  | D-    |
| 0-59   | F     |

### Computing the Final Score

1. For each category, start at 100 and subtract all deductions (floor at 0)
2. Multiply each category score by its weight percentage
3. Sum the weighted scores to get the overall score (0-100)
4. Map to a letter grade using the scale above

---

## Rule Set

### Schema Rules (8 rules)

#### CV-S001: Invalid YAML Syntax
- **Severity:** error
- **Check:** YAML parser encounters a syntax error preventing the file from being parsed
- **Why:** Common causes include incorrect indentation (YAML uses spaces, never tabs), unclosed quotes or brackets, duplicate keys at the same nesting level, and missing colons after mapping keys.
- **Fix:** Fix the YAML syntax error at the indicated line
- **Before:**
  ```yaml
  services:
    web:
      image: nginx
    	ports:
        - "80:80"
  ```
- **After:**
  ```yaml
  services:
    web:
      image: nginx
      ports:
        - "80:80"
  ```

#### CV-S002: Unknown Top-Level Property
- **Severity:** error
- **Check:** Top-level key is not one of: services, networks, volumes, secrets, configs, name, version
- **Why:** Docker Compose files only allow a fixed set of top-level keys. Any other key is rejected by the compose-spec schema.
- **Fix:** Use a valid top-level property name or prefix custom properties with x-
- **Before:** `service:` (typo)
- **After:** `services:`

#### CV-S003: Unknown Service Property
- **Severity:** error
- **Check:** Service contains a property not in the compose-spec service schema
- **Why:** Service definitions have a defined set of properties (image, build, command, ports, volumes, etc.). Invalid properties are rejected.
- **Fix:** Use a valid service property name
- **Before:** `port:` (typo)
- **After:** `ports:`

#### CV-S004: Invalid Port Format
- **Severity:** error
- **Check:** Port mapping does not match valid HOST:CONTAINER or long syntax format
- **Why:** Unquoted port mappings like 80:80 are interpreted as base-60 integers by the YAML 1.1 parser. Always quote port mappings.
- **Fix:** Quote port mappings as strings and use valid format
- **Before:** `- 8080:80` (unquoted)
- **After:** `- "8080:80"`

#### CV-S005: Invalid Volume Format
- **Severity:** error
- **Check:** Volume specification does not match SOURCE:TARGET[:MODE] short syntax or long syntax
- **Why:** A common mistake is specifying only the source path without a target.
- **Fix:** Use valid SOURCE:TARGET[:MODE] short syntax or long syntax
- **Before:** `- ./data`
- **After:** `- ./data:/app/data`

#### CV-S006: Invalid Duration Format
- **Severity:** warning
- **Check:** Healthcheck or stop_grace_period value missing unit suffix
- **Why:** Duration fields accept Docker duration format: decimal numbers with unit suffixes (us, ms, s, m, h). Bare integers without units are invalid.
- **Fix:** Add a unit suffix (s, m, h)
- **Before:** `interval: 30`
- **After:** `interval: 30s`

#### CV-S007: Invalid Restart Policy
- **Severity:** error
- **Check:** restart value is not one of: "no", "always", "on-failure", "unless-stopped"
- **Why:** Only four restart policies are valid. Always quote "no" because bare `no` is parsed as boolean false in YAML 1.1.
- **Fix:** Use a valid restart policy
- **Before:** `restart: never`
- **After:** `restart: "no"`

#### CV-S008: Invalid depends_on Condition
- **Severity:** error
- **Check:** depends_on condition is not one of: service_started, service_healthy, service_completed_successfully
- **Why:** Only three conditions are valid in the long-form depends_on syntax.
- **Fix:** Use a valid condition
- **Before:** `condition: healthy`
- **After:** `condition: service_healthy`

### Security Rules (14 rules)

#### CV-C001: Privileged mode enabled
- **Severity:** error
- **Check:** Service has `privileged: true`
- **Why:** Privileged mode grants all Linux kernel capabilities and access to host devices, effectively disabling container isolation. CWE-250: Execution with Unnecessary Privileges.
- **Fix:** Remove privileged: true and use specific capabilities via cap_add
- **Before:**
  ```yaml
  services:
    web:
      privileged: true
  ```
- **After:**
  ```yaml
  services:
    web:
      cap_add:
        - NET_BIND_SERVICE
  ```

#### CV-C002: Docker socket mounted
- **Severity:** error
- **Check:** Volume mounts /var/run/docker.sock
- **Why:** Mounting the Docker socket grants root-level control over the host Docker daemon. Any process in the container can create, start, stop, or remove containers. CWE-250.
- **Fix:** Use a Docker API proxy with limited permissions or avoid socket mounting
- **Before:**
  ```yaml
  volumes:
    - /var/run/docker.sock:/var/run/docker.sock
  ```
- **After:**
  ```yaml
  volumes:
    - ./app-data:/data
  ```

#### CV-C003: Host network mode
- **Severity:** error
- **Check:** Service uses `network_mode: host`
- **Why:** Bypasses Docker network isolation entirely. The container shares the host network namespace.
- **Fix:** Use user-defined bridge networks
- **Before:** `network_mode: host`
- **After:** `networks: [frontend]`

#### CV-C004: Host PID mode
- **Severity:** error
- **Check:** Service uses `pid: host`
- **Why:** Shares the host PID namespace. Container processes can see and signal all host processes.
- **Fix:** Remove pid: host unless debugging host processes

#### CV-C005: Host IPC mode
- **Severity:** error
- **Check:** Service uses `ipc: host`
- **Why:** Shares the host IPC namespace, allowing access to host shared memory segments.
- **Fix:** Remove ipc: host or use ipc: shareable between specific services

#### CV-C006: Dangerous capabilities added
- **Severity:** error
- **Check:** cap_add includes SYS_ADMIN, NET_ADMIN, ALL, SYS_PTRACE, DAC_OVERRIDE, or similar
- **Why:** Dangerous capabilities significantly weaken container isolation. ALL grants every capability, equivalent to privileged mode. CWE-250.
- **Fix:** Remove dangerous capabilities and add only the minimum required
- **Before:**
  ```yaml
  cap_add:
    - SYS_ADMIN
    - NET_ADMIN
  ```
- **After:**
  ```yaml
  cap_add:
    - NET_BIND_SERVICE
  ```

#### CV-C007: Default capabilities not dropped
- **Severity:** warning
- **Check:** Service has no `cap_drop: [ALL]`
- **Why:** Docker containers start with more capabilities than needed. Best practice is to drop all and selectively add back.
- **Fix:** Add `cap_drop: [ALL]` and explicitly add back only needed capabilities

#### CV-C008: Secrets in environment variables
- **Severity:** warning
- **Check:** Environment variables with names matching PASSWORD, SECRET, API_KEY, TOKEN patterns have inline values
- **Why:** Inline secrets are exposed in version control, process listings, container inspection, and logs.
- **Fix:** Use Docker secrets or .env files excluded from version control
- **Before:**
  ```yaml
  environment:
    DB_PASSWORD: supersecret
  ```
- **After:**
  ```yaml
  secrets:
    - db_password
  ```

#### CV-C009: Unbound port interface
- **Severity:** warning
- **Check:** Port mapping does not specify a host IP address (binds to 0.0.0.0)
- **Why:** Without a specific IP, Docker binds to all network interfaces including public-facing ones.
- **Fix:** Bind to 127.0.0.1 for local-only access
- **Before:** `"8080:80"`
- **After:** `"127.0.0.1:8080:80"`

#### CV-C010: Missing no-new-privileges
- **Severity:** warning
- **Check:** Service lacks `security_opt: [no-new-privileges:true]`
- **Why:** Without this, processes can gain privileges through setuid/setgid binaries.
- **Fix:** Add no-new-privileges to security_opt

#### CV-C011: Writable root filesystem
- **Severity:** warning
- **Check:** Service does not set `read_only: true`
- **Why:** A writable filesystem allows attackers to modify binaries and install tools.
- **Fix:** Set read_only: true and use tmpfs for writable paths

#### CV-C012: Seccomp profile disabled
- **Severity:** warning
- **Check:** security_opt contains `seccomp:unconfined`
- **Why:** Disabling seccomp removes system call restrictions.
- **Fix:** Remove seccomp:unconfined or use a custom profile

#### CV-C013: SELinux labeling disabled
- **Severity:** warning
- **Check:** security_opt contains `label:disable`
- **Why:** Disabling SELinux removes mandatory access controls.
- **Fix:** Remove label:disable or use appropriate labels

#### CV-C014: Image uses latest or no tag
- **Severity:** warning
- **Check:** Image has no version tag or uses :latest
- **Why:** Mutable tags make deployments non-reproducible and can introduce vulnerabilities.
- **Fix:** Pin to a specific version tag or SHA256 digest
- **Before:** `image: nginx`
- **After:** `image: nginx:1.25.3-alpine`

### Semantic Rules (15 rules)

#### CV-M001: Duplicate exported host ports
- **Severity:** error
- **Check:** Two or more services export the same host port
- **Why:** Only one container can bind a given host port. Causes startup failure.
- **Fix:** Assign unique host ports to each service

#### CV-M002: Circular depends_on chain
- **Severity:** error
- **Check:** Services form a dependency cycle via depends_on
- **Why:** Docker Compose cannot determine a valid startup order with cycles.
- **Fix:** Remove one depends_on link to break the cycle

#### CV-M003: Undefined network reference
- **Severity:** error
- **Check:** Service references a network not defined in top-level networks
- **Why:** Docker Compose fails to start when a service references an undefined network.
- **Fix:** Define the network in the top-level networks section

#### CV-M004: Undefined volume reference
- **Severity:** error
- **Check:** Service references a named volume not defined in top-level volumes
- **Why:** Docker Compose fails when a service mounts an undefined named volume.
- **Fix:** Define the volume in the top-level volumes section

#### CV-M005: Undefined secret reference
- **Severity:** error
- **Check:** Service references a secret not defined in top-level secrets
- **Why:** Docker Compose requires all secrets to be declared at top level.
- **Fix:** Define the secret in the top-level secrets section

#### CV-M006: Undefined config reference
- **Severity:** error
- **Check:** Service references a config not defined in top-level configs
- **Why:** Docker Compose requires all configs to be declared at top level.
- **Fix:** Define the config in the top-level configs section

#### CV-M007: Orphan network definition
- **Severity:** warning
- **Check:** Network defined but not referenced by any service
- **Why:** Orphan definitions add clutter and Docker creates unused networks.
- **Fix:** Remove the unused network or assign it to a service

#### CV-M008: Orphan volume definition
- **Severity:** warning
- **Check:** Volume defined but not referenced by any service
- **Why:** Orphan volumes consume disk space without purpose.
- **Fix:** Remove the unused volume or mount it in a service

#### CV-M009: Orphan secret definition
- **Severity:** warning
- **Check:** Secret defined but not referenced by any service
- **Why:** Orphan secrets add unnecessary configuration.
- **Fix:** Remove the unused secret or assign it to a service

#### CV-M010: depends_on service_healthy without healthcheck
- **Severity:** error
- **Check:** Service uses condition: service_healthy but the target has no healthcheck
- **Why:** Docker Compose waits indefinitely for the target to become healthy, hanging startup.
- **Fix:** Add a healthcheck to the target service or use service_started condition

#### CV-M011: Self-referencing dependency
- **Severity:** error
- **Check:** Service lists itself in depends_on
- **Why:** A service cannot depend on itself. This creates an impossible startup condition.
- **Fix:** Remove the self-referencing entry

#### CV-M012: Dependency on undefined service
- **Severity:** error
- **Check:** depends_on references a service not defined in services
- **Why:** Docker Compose fails when it cannot find the referenced service.
- **Fix:** Fix the service name typo or add the missing service

#### CV-M013: Duplicate container names
- **Severity:** error
- **Check:** Two or more services use the same container_name
- **Why:** Docker container names must be unique on a host.
- **Fix:** Use unique container names or remove explicit naming

#### CV-M014: Port range overlap between services
- **Severity:** warning
- **Check:** Port ranges exported by different services overlap
- **Why:** Overlapping ranges cause binding conflicts on shared ports.
- **Fix:** Adjust port ranges so they do not overlap

#### CV-M015: Invalid image reference format
- **Severity:** warning
- **Check:** Image reference contains uppercase, spaces, or invalid characters
- **Why:** Docker cannot resolve malformed image references.
- **Fix:** Use lowercase, valid Docker image reference format

### Best Practice Rules (12 rules)

#### CV-B001: Missing healthcheck
- **Severity:** warning
- **Check:** Service has no healthcheck defined
- **Why:** Without healthchecks, Docker cannot determine if the application is functioning. Healthchecks enable automatic restart and depends_on with condition: service_healthy.
- **Fix:** Add a healthcheck with test, interval, timeout, and retries

#### CV-B002: No restart policy
- **Severity:** warning
- **Check:** Service has no restart or deploy.restart_policy
- **Why:** Crashed containers stay stopped without a restart policy.
- **Fix:** Add restart: unless-stopped or restart: on-failure

#### CV-B003: No resource limits
- **Severity:** warning
- **Check:** Service has no deploy.resources.limits
- **Why:** Without limits, a single container can consume all host resources.
- **Fix:** Add deploy.resources.limits with cpus and memory

#### CV-B004: Image tag not pinned (mutable tag)
- **Severity:** warning
- **Check:** Image uses mutable tags like latest, stable, edge, nightly
- **Why:** Mutable tags point to different versions over time, breaking reproducibility.
- **Fix:** Pin to a specific immutable version tag or SHA256 digest

#### CV-B005: No logging configuration
- **Severity:** info
- **Check:** Service has no logging configuration
- **Why:** Without logging config, containers use daemon defaults with no rotation, leading to unbounded log growth.
- **Fix:** Add logging driver with rotation options (max-size, max-file)

#### CV-B006: Deprecated version field
- **Severity:** warning
- **Check:** Top-level `version` field is present
- **Why:** Docker Compose V2 no longer requires or uses this field. It is silently ignored.
- **Fix:** Remove the top-level version field entirely

#### CV-B007: Missing project name
- **Severity:** info
- **Check:** No top-level `name` field
- **Why:** Without it, Docker Compose derives the project name from the directory, which can be unpredictable.
- **Fix:** Add a top-level name field

#### CV-B008: Both build and image specified
- **Severity:** warning
- **Check:** Service has both `build` and `image` properties
- **Why:** While valid (Compose builds and tags), it can cause confusion about behavior.
- **Fix:** Use either build or image, not both, unless intentionally tagging

#### CV-B009: Anonymous volume usage
- **Severity:** info
- **Check:** Volume mount uses anonymous volume (no name, just a container path)
- **Why:** Anonymous volumes get random hash names, making them hard to manage and back up.
- **Fix:** Replace with named volumes in the top-level volumes section

#### CV-B010: No memory reservation alongside limits
- **Severity:** info
- **Check:** Service has memory limits but no memory reservation
- **Why:** Without reservations, the scheduler cannot differentiate minimum from maximum memory needs.
- **Fix:** Add deploy.resources.reservations.memory alongside limits

#### CV-B011: Healthcheck timeout exceeds interval
- **Severity:** warning
- **Check:** Healthcheck timeout >= interval
- **Why:** Slow probes overlap with the next scheduled probe, wasting resources and causing misleading status.
- **Fix:** Set timeout shorter than interval

#### CV-B012: Default network only
- **Severity:** info
- **Check:** No custom networks defined; all services share the default bridge
- **Why:** All containers can reach all others, violating the principle of least privilege.
- **Fix:** Define custom networks for logical grouping and isolation

### Style Rules (3 rules)

#### CV-F001: Services not alphabetically ordered
- **Severity:** info
- **Check:** Service definitions are not in alphabetical order
- **Why:** Alphabetical ordering makes services easier to locate in large files and produces predictable diffs.
- **Fix:** Reorder services alphabetically

#### CV-F002: Ports not quoted (YAML base-60 risk)
- **Severity:** info
- **Check:** Port values with colons are not quoted in YAML source
- **Why:** In YAML 1.1, unquoted 3000:80 can be interpreted as sexagesimal (base-60) numbers.
- **Fix:** Quote all port values
- **Before:** `- 8080:80`
- **After:** `- "8080:80"`

#### CV-F003: Inconsistent port quoting
- **Severity:** info
- **Check:** Service has a mix of quoted and unquoted port values
- **Why:** Inconsistent quoting reduces readability and can lead to confusion.
- **Fix:** Quote all port values consistently

---

## Output Format

When presenting analysis results, use this structure:

```
## Docker Compose Analysis Results

**Score:** {score}/100 (Grade: {grade})

### Category Breakdown
| Category      | Score   | Weight |
|---------------|---------|--------|
| Security      | {n}/100 | 30%    |
| Semantic      | {n}/100 | 25%    |
| Best Practice | {n}/100 | 20%    |
| Schema        | {n}/100 | 15%    |
| Style         | {n}/100 | 10%    |

### Issues Found ({total} issues: {errors} errors, {warnings} warnings, {info} info)

#### Errors
- **Line {n} [{rule_id}]: {title}** ({category})
  {explanation}
  **Fix:** {fix_description}

#### Warnings
...

#### Info
...
```

If the Compose file has zero violations, congratulate the user and note the perfect score.

## Fix Prompt Generation

When the user asks you to fix the Compose file (or you offer to after analysis), use this approach:

You are a senior DevOps engineer and Docker Compose security specialist. Apply the identified issues precisely. Every flagged issue must be resolved while preserving the original stack's intended functionality. Prioritize production-readiness, security hardening, and operational best practices.

Apply fixes in priority order:
1. **Errors**: broken or dangerous configurations, fix first
2. **Warnings**: security risks or operational problems, fix next
3. **Info**: best-practice and style improvements, fix last

When multiple issues affect the same service, combine all fixes into a single corrected service definition.

Preserve original functionality:
- Keep all intended services, volumes, networks, and relationships
- Do not add services or resources beyond what resolves the issues
- If removing something (e.g., privileged mode), replace with the minimal secure alternative

Follow Docker Compose best practices when restructuring:
- Use specific image version tags instead of :latest
- Define explicit networks for service isolation
- Use Docker secrets instead of inline environment variable secrets
- Order services alphabetically for readability
- Quote all port mappings to avoid YAML base-60 interpretation

Output:
1. A summary mapping each issue to its fix, grouped by severity
2. The complete corrected Docker Compose file in a `yaml` code block with no omissions or placeholders

Constraints:
- Resolve ALL reported issues, including info-level
- Do not introduce new issues while fixing existing ones
- Do not change base images or service purposes unless an issue requires it
- When pinning versions without specifics, use a comment placeholder rather than inventing numbers
- Never leave secrets as plain-text values in the final file
- Maintain valid YAML syntax and quote strings that could be misinterpreted
