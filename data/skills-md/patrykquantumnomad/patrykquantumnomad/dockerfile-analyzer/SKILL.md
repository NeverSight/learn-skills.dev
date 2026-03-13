---
name: dockerfile-analyzer
description: >
  Analyze Dockerfiles for security vulnerabilities, efficiency issues, and
  best-practice violations using 46 rules across 5 categories (security,
  efficiency, maintainability, reliability, best-practice). Scores Dockerfiles
  on a 0-100 scale with letter grades (A+ through F). Generates detailed fix
  recommendations with before/after code examples. Use this skill PROACTIVELY
  whenever a user shares a Dockerfile for review, pastes Dockerfile content,
  asks about Dockerfile best practices or security hardening, wants to improve
  their container image security posture, mentions Dockerfile or Docker image
  builds, or asks about multi-stage builds or image optimization — even if
  they don't explicitly say "validate" or "analyze".
---

# Dockerfile Analyzer

You are a Dockerfile analysis engine. When a user shares a Dockerfile or asks you to review one, apply the complete rule set below to identify violations, compute a quality score, and present actionable fix recommendations.

## When to Activate

- User shares a Dockerfile (pasted content, file path, or asks you to read one)
- User asks to "analyze", "lint", "review", or "check" a Dockerfile
- User asks about Dockerfile best practices or security hardening
- User asks to improve or optimize a Dockerfile

## Analysis Process

1. Read the full Dockerfile content
2. Parse each instruction (FROM, RUN, COPY, ENV, EXPOSE, CMD, etc.)
3. Apply every applicable rule from the rule set below
4. For each violation, record: rule ID, affected line number, severity, category, and message
5. Compute the quality score using the scoring methodology
6. Present findings grouped by severity (errors first, then warnings, then info)
7. Offer to generate a fix prompt or apply fixes directly

## Scoring Methodology

### Category Weights

| Category        | Weight |
|-----------------|--------|
| Security        | 30%    |
| Efficiency      | 25%    |
| Maintainability | 20%    |
| Reliability     | 15%    |
| Best Practice   | 10%    |

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

### Security Rules (15 rules)

#### DL3006 — Always tag the version of an image explicitly
- **Severity:** warning
- **Check:** FROM instructions without a version tag (e.g., `FROM ubuntu` with no `:tag`)
- **Why:** Untagged images default to :latest which can change without warning. A deployment that worked yesterday can break today because the base image was updated. Pinning to a specific tag ensures reproducible builds and predictable behavior across environments.
- **Fix:** Pin the base image to a specific version tag or digest
- **Before:** `FROM ubuntu`
- **After:** `FROM ubuntu:22.04`

#### DL3007 — Do not use the :latest tag
- **Severity:** warning
- **Check:** FROM instructions using the `:latest` tag explicitly
- **Why:** The :latest tag is a moving target. In production, an image tagged :latest today may resolve to a completely different image tomorrow after the maintainer pushes an update. This breaks reproducibility. Always pin to a specific version tag or digest.
- **Fix:** Replace :latest with a specific version tag
- **Before:** `FROM ubuntu:latest`
- **After:** `FROM ubuntu:22.04`

#### DL3008 — Pin versions in apt-get install
- **Severity:** warning
- **Check:** `apt-get install` commands with unpinned package names (no `=version` suffix)
- **Why:** Without pinned versions, apt-get install pulls the latest available package, which can differ between builds. Two images built from the same Dockerfile may contain different package versions, leading to inconsistent behavior.
- **Fix:** Pin package versions with = syntax
- **Before:** `RUN apt-get install -y curl wget`
- **After:** `RUN apt-get install -y curl=7.88.1-10+deb12u5 wget=1.21.3-1`

#### DL3020 — Use COPY instead of ADD for files and folders
- **Severity:** error
- **Check:** ADD instructions used for simple file copies (not URL fetches or archive extraction)
- **Why:** ADD has implicit behaviors: it auto-extracts archives and can fetch remote URLs without checksum verification. This unpredictability is a security risk. Use COPY for file copies and explicit commands for archives/URLs.
- **Fix:** Replace ADD with COPY for local file copies
- **Before:** `ADD ./config /app/config`
- **After:** `COPY ./config /app/config`

#### DL3004 — Do not use sudo
- **Severity:** error
- **Check:** RUN instructions containing `sudo`
- **Why:** sudo is unnecessary since builds run as root by default. It adds a SUID binary that can be exploited for privilege escalation. Use the USER instruction to switch users explicitly.
- **Fix:** Remove sudo and run the command directly
- **Before:** `RUN sudo apt-get install -y curl`
- **After:** `RUN apt-get install -y curl`

#### DL3002 — Last USER should not be root
- **Severity:** warning
- **Check:** The last USER instruction in the final build stage is `root`, or no USER instruction exists (implying root)
- **Why:** Running as root gives the process full host-level privileges if it escapes the container. A vulnerability in your application could grant an attacker root access to the host.
- **Fix:** Add a non-root USER instruction at the end
- **Before:** `USER root` / `CMD ["node", "server.js"]`
- **After:** `USER node` / `CMD ["node", "server.js"]`

#### DL3061 — Dockerfile should start with FROM or ARG
- **Severity:** error
- **Check:** Any instruction before FROM that is not ARG
- **Why:** A valid Dockerfile must begin with FROM (or ARG before FROM). Any other instruction before FROM is invalid and causes build failure.
- **Fix:** Ensure FROM is the first non-ARG instruction
- **Before:** `RUN echo hello` / `FROM ubuntu:22.04`
- **After:** `FROM ubuntu:22.04` / `RUN echo hello`

#### PG001 — Secrets detected in ENV or ARG
- **Severity:** error
- **Check:** ENV or ARG instructions with values matching secret patterns (API keys, passwords, tokens, private keys)
- **Why:** Hardcoded secrets are baked into image layers and visible to anyone who can pull the image. They remain in build history even if deleted in later layers. Use build secrets (`--mount=type=secret`) or runtime environment variables.
- **Fix:** Remove hardcoded secrets and use Docker build secrets or runtime injection
- **Before:** `ENV API_KEY=sk-1234567890abcdef`
- **After:** `RUN --mount=type=secret,id=api_key cat /run/secrets/api_key`

#### PG002 — Avoid piping remote scripts to shell
- **Severity:** error
- **Check:** RUN instructions piping curl/wget output to sh/bash/zsh (e.g., `curl ... | bash`)
- **Why:** Piping remote scripts directly to a shell executes unverified code. If the server is compromised, arbitrary code runs with root privileges. Download first, verify checksum, then execute.
- **Fix:** Download, verify checksum, then execute
- **Before:** `RUN curl -sSL https://example.com/install.sh | bash`
- **After:** `RUN curl -sSL -o /tmp/install.sh https://example.com/install.sh && echo "sha256 /tmp/install.sh" | sha256sum -c - && bash /tmp/install.sh && rm /tmp/install.sh`

#### PG003 — Avoid copying sensitive files into the image
- **Severity:** warning
- **Check:** COPY or ADD instructions targeting sensitive files (.env, id_rsa, .pem, .key, credentials, etc.)
- **Why:** Sensitive files copied into the image are embedded in layer history and can be extracted even if deleted later. Use .dockerignore, mount secrets at runtime, or use build secrets.
- **Fix:** Add sensitive files to .dockerignore and use build secrets or runtime mounts
- **Before:** `COPY .env /app/.env`
- **After:** `RUN --mount=type=secret,id=env,target=/app/.env cat /app/.env`

#### PG006 — Prefer image digest over mutable tag
- **Severity:** info
- **Check:** FROM instructions using a tag but no digest (`@sha256:...`). Skip images using variable references (`${VAR}`), `scratch`, or build stage aliases.
- **Why:** Image tags are mutable -- maintainers can rebuild and push a new image under the same tag. A digest is the only truly immutable reference and guarantees bit-for-bit reproducible builds.
- **Fix:** Pin the base image to a digest. Run `docker pull <image>` then `docker inspect --format='{{index .RepoDigests 0}}' <image>` to get it.
- **Before:** `FROM node:20-alpine`
- **After:** `FROM node:20-alpine@sha256:1a2b3c...`

#### PG007 — Use explicit UID/GID for container users
- **Severity:** warning
- **Check:** `useradd` without `-u`/`--uid` or `groupadd` without `-g`/`--gid` in RUN instructions
- **Why:** When useradd is called without -u, the system auto-assigns the next available UID. These IDs are non-deterministic and depend on the order of package installations. Rebuild the image after a base image update and the UID may change, breaking file ownership on persistent volumes. In Kubernetes, a mismatch between the image UID and securityContext.runAsUser causes permission errors at startup. Use explicit IDs above 10000 to avoid collisions with host system users and Linux reserved ranges.
- **Fix:** Specify explicit UID and GID using -u/-g flags with values above 10000
- **Before:** `RUN groupadd appgroup\nRUN useradd appuser`
- **After:** `ARG uid=10001\nARG gid=10001\nRUN groupadd -g ${gid} appgroup && useradd -u ${uid} -g appgroup -s /bin/false appuser\nUSER appuser`

#### PG009 — Remove unnecessary network tools from production images
- **Severity:** warning
- **Check:** Package-manager install commands that install network/debugging tools (curl, wget, netcat, nmap, telnet, ftp, ssh client, socat, tcpdump) in the final build stage without removing them
- **Why:** Network utilities like curl, wget, and netcat expand the attack surface of a production container. If an attacker gains code execution, these tools allow downloading additional payloads, establishing reverse shells, or communicating with command-and-control servers. The CIS Docker Benchmark (Section 4.3) states: "Do not install unnecessary packages in containers."
- **Fix:** Use a multi-stage build so network tools stay in the builder stage, or remove them after use
- **Before:** `FROM ubuntu:22.04\nRUN apt-get update && apt-get install -y curl && curl -o app.tar.gz https://example.com/app.tar.gz\nCMD ["./app"]`
- **After:** `FROM ubuntu:22.04 AS builder\nRUN apt-get update && apt-get install -y curl && curl -o app.tar.gz https://example.com/app.tar.gz\n\nFROM ubuntu:22.04\nCOPY --from=builder /app.tar.gz /app.tar.gz\nCMD ["./app"]`

#### PG010 — Avoid using network tools in the final build stage
- **Severity:** info
- **Check:** RUN instructions in the final build stage that execute network tool binaries (curl, wget, nc, netcat, nmap, telnet, ftp, ssh, scp, socat, tcpdump) -- even if pre-installed in the base image
- **Why:** Even when network tools are not explicitly installed (they may come pre-installed in the base image), their usage in the final stage indicates the production image will ship with these tools available. The CIS Docker Benchmark (Section 4.3) advises against keeping unnecessary packages in containers. Use a multi-stage build to confine network tool usage to a builder stage.
- **Fix:** Move network tool usage to a builder stage and COPY artifacts into the final image
- **Before:** `FROM node:22-bookworm\nRUN curl -fsSL https://bun.sh/install | bash\nCMD ["node", "server.js"]`
- **After:** `FROM node:22-bookworm AS builder\nRUN curl -fsSL -o /tmp/install.sh https://bun.sh/install && bash /tmp/install.sh\n\nFROM node:22-slim\nCOPY --from=builder /root/.bun /root/.bun\nCMD ["node", "server.js"]`

#### PG011 — Add a USER directive to avoid running as root
- **Severity:** warning
- **Check:** Final build stage has no USER instruction at all (not even `USER root`). Does NOT fire when any USER instruction exists in the final stage (defers to DL3002 for explicit `USER root` cases). Skips FROM scratch (no user system).
- **Why:** When a Dockerfile has no USER instruction, the container runs as root (UID 0) by default. If an attacker exploits a vulnerability, they gain root access -- and in the event of a container escape, they become root on the host. The CIS Docker Benchmark (Section 4.1) and Kubernetes Pod Security Standards both require non-root containers. Unlike USER root (caught by DL3002), a missing USER directive is invisible -- there is no line to flag.
- **Fix:** Add a non-root USER instruction after completing root-only setup tasks
- **Before:** `FROM node:22-bookworm-slim\nWORKDIR /app\nCOPY . .\nCMD ["node", "server.js"]`
- **After:** `FROM node:22-bookworm-slim\nRUN groupadd -g 10001 appgroup && useradd -u 10001 -g appgroup -s /bin/false appuser\nWORKDIR /app\nCOPY --chown=appuser:appgroup . .\nUSER appuser\nCMD ["node", "server.js"]`

### Efficiency Rules (9 rules)

#### DL3059 — Multiple consecutive RUN instructions
- **Severity:** info
- **Check:** Two or more RUN instructions in sequence that could be combined
- **Why:** Each RUN creates a new layer. Consecutive RUNs waste space because files created in one layer and deleted in the next still exist in the earlier layer. Combine with `&&` to reduce layers.
- **Fix:** Combine consecutive RUN instructions with &&
- **Before:** `RUN apt-get update` / `RUN apt-get install -y curl`
- **After:** `RUN apt-get update && apt-get install -y curl`

#### DL3014 — Use the -y switch for apt-get install
- **Severity:** warning
- **Check:** `apt-get install` without `-y` or `--yes` flag
- **Why:** Without -y, apt-get prompts for confirmation interactively. In Docker builds there is no terminal, so the build hangs or fails.
- **Fix:** Add -y flag to apt-get install
- **Before:** `RUN apt-get install curl`
- **After:** `RUN apt-get install -y curl`

#### DL3015 — Avoid additional packages with --no-install-recommends
- **Severity:** info
- **Check:** `apt-get install` without `--no-install-recommends`
- **Why:** Default apt-get pulls "recommended" packages not strictly required, increasing image size by 30-50% and expanding attack surface.
- **Fix:** Add --no-install-recommends
- **Before:** `RUN apt-get install -y curl wget`
- **After:** `RUN apt-get install -y --no-install-recommends curl wget`

#### DL3003 — Use WORKDIR to switch directories
- **Severity:** warning
- **Check:** `cd` commands inside RUN instructions
- **Why:** `cd` inside RUN does not persist across layers. WORKDIR is the idiomatic way to set the working directory and persists across all subsequent instructions.
- **Fix:** Replace cd with WORKDIR
- **Before:** `RUN cd /app && npm install`
- **After:** `WORKDIR /app` / `RUN npm install`

#### DL3009 — Delete the apt-get lists after installing
- **Severity:** info
- **Check:** `apt-get update` in a RUN without a corresponding `rm -rf /var/lib/apt/lists/*` in the same RUN
- **Why:** Package lists add 20-40 MB of unnecessary data. Remove them in the same RUN to keep layers lean.
- **Fix:** Add rm -rf /var/lib/apt/lists/* in the same RUN
- **Before:** `RUN apt-get update && apt-get install -y curl`
- **After:** `RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*`

#### DL4006 — Set SHELL option -o pipefail before RUN with pipe
- **Severity:** warning
- **Check:** RUN instructions containing pipe (`|`) without prior `SHELL ["/bin/bash", "-o", "pipefail", "-c"]`
- **Why:** In /bin/sh, a piped command only reports the exit code of the last command. If an earlier command fails, the build continues silently with corrupt data.
- **Fix:** Add SHELL instruction with pipefail
- **Before:** `RUN curl -sSL https://example.com/file | tar xz`
- **After:** `SHELL ["/bin/bash", "-o", "pipefail", "-c"]` / `RUN curl -sSL https://example.com/file | tar xz`

#### DL3042 — Avoid use of cache directory with pip
- **Severity:** warning
- **Check:** `pip install` without `--no-cache-dir`
- **Why:** pip caches downloaded packages in ~/.cache/pip, wasting 50-200 MB in the image. The cache is never reused in containers.
- **Fix:** Add --no-cache-dir to pip install
- **Before:** `RUN pip install flask requests`
- **After:** `RUN pip install --no-cache-dir flask requests`

#### DL3019 — Use the --no-cache switch for apk add
- **Severity:** info
- **Check:** `apk add` without `--no-cache`, or `apk update` followed by `apk add`
- **Why:** Without --no-cache, apk stores a local package index that adds unnecessary size to Alpine images.
- **Fix:** Add --no-cache to apk add
- **Before:** `RUN apk update && apk add curl`
- **After:** `RUN apk add --no-cache curl`

#### PG012 — Consider pointer compression for Node.js images
- **Severity:** info
- **Check:** Final build stage uses an official Docker Hub Node.js base image (node:* or library/node:*). Does NOT fire on custom registry images, non-node images, FROM scratch, or build stage alias references.
- **Why:** V8 pointer compression shrinks every internal pointer from 64 bits to 32 bits. Since tagged values (mostly pointers) make up roughly 70% of all heap memory, this can reduce memory usage by approximately 50% for pointer-heavy Node.js workloads -- with no code changes. The platformatic/node-caged Docker image ships Node.js built with --experimental-enable-pointer-compression. Requires Node.js 25+ (with V8 IsolateGroups). 4GB per-isolate heap limit (Buffers don't count). N-API addons compatible but older V8 native addons may not work.
- **Fix:** Replace the official Node.js base image with platformatic/node-caged
- **Before:** `FROM node:22-bookworm-slim\nWORKDIR /app\nCOPY . .\nCMD ["node", "server.js"]`
- **After:** `FROM platformatic/node-caged:25-slim\nWORKDIR /app\nCOPY . .\nCMD ["node", "server.js"]`

### Maintainability Rules (7 rules)

#### DL4000 — MAINTAINER is deprecated
- **Severity:** error
- **Check:** Any MAINTAINER instruction
- **Why:** MAINTAINER was deprecated in Docker 1.13 (January 2017). Use LABEL instead.
- **Fix:** Replace MAINTAINER with LABEL
- **Before:** `MAINTAINER john@example.com`
- **After:** `LABEL maintainer="john@example.com"`

#### DL3025 — Use JSON notation for CMD and ENTRYPOINT
- **Severity:** warning
- **Check:** CMD or ENTRYPOINT in shell form (not JSON array). Skip when the command uses variable substitution (`${VAR}`) since JSON exec form cannot expand variables.
- **Why:** Shell form wraps the command in `/bin/sh -c`, preventing proper signal propagation. SIGTERM reaches the shell, not your application, causing ungraceful shutdowns.
- **Fix:** Convert shell form to JSON array form
- **Before:** `CMD node server.js`
- **After:** `CMD ["node", "server.js"]`

#### DL3000 — Use absolute WORKDIR
- **Severity:** error
- **Check:** WORKDIR with a relative path (e.g., `WORKDIR app` instead of `WORKDIR /app`)
- **Why:** Relative paths depend on the previous WORKDIR value, making the Dockerfile fragile. If the base image changes its default directory, the build breaks.
- **Fix:** Use an absolute path
- **Before:** `WORKDIR app`
- **After:** `WORKDIR /app`

#### DL3045 — COPY to a relative destination without WORKDIR set
- **Severity:** warning
- **Check:** COPY with a relative destination path when no WORKDIR has been set in the current stage
- **Why:** Without WORKDIR, relative paths resolve from the filesystem root (/), putting files in unexpected locations.
- **Fix:** Set WORKDIR before COPY with relative destination
- **Before:** `FROM node:20` / `COPY . app/`
- **After:** `FROM node:20` / `WORKDIR /app` / `COPY . .`

#### PG004 — Use ENV key=value format instead of legacy ENV key value
- **Severity:** info
- **Check:** ENV instructions using the legacy space-separated syntax (e.g., `ENV MY_VAR some value`)
- **Why:** Legacy `ENV KEY value` only supports one variable per instruction and is ambiguous with spaces. `ENV KEY=value` is explicit and supports multiple variables per line.
- **Fix:** Use key=value syntax
- **Before:** `ENV MY_VAR some value`
- **After:** `ENV MY_VAR="some value"`

#### DL4001 — Either use wget or curl but not both
- **Severity:** warning
- **Check:** Both `wget` and `curl` used in the same Dockerfile (in RUN or install commands)
- **Why:** Installing both adds unnecessary size and creates inconsistency. Pick one and use it consistently.
- **Fix:** Standardize on either curl or wget
- **Before:** `RUN curl -o file1.txt ...` / `RUN wget ...`
- **After:** `RUN curl -o file1.txt ...` / `RUN curl -o file2.txt ...`

#### DL3057 — HEALTHCHECK instruction is missing
- **Severity:** info
- **Check:** Final build stage has no HEALTHCHECK instruction
- **Why:** Without HEALTHCHECK, orchestrators cannot verify the container is functioning. A crashed application inside a "running" container serves errors until manual intervention.
- **Fix:** Add a HEALTHCHECK instruction
- **Before:** `CMD ["node", "server.js"]`
- **After:** `HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD curl -f http://localhost:8080/health || exit 1` / `CMD ["node", "server.js"]`

### Reliability Rules (6 rules)

#### DL4003 — Multiple CMD instructions found
- **Severity:** warning
- **Check:** More than one CMD instruction in a single build stage
- **Why:** Only the last CMD takes effect. Multiple CMDs are almost always a mistake.
- **Fix:** Remove duplicates, keep only the final one
- **Before:** `CMD ["echo", "first"]` / `CMD ["echo", "second"]`
- **After:** `CMD ["echo", "second"]`

#### DL4004 — Multiple ENTRYPOINT instructions found
- **Severity:** error
- **Check:** More than one ENTRYPOINT instruction in a single build stage
- **Why:** Only the last ENTRYPOINT takes effect. A wrong entrypoint means the container runs unexpected code.
- **Fix:** Remove duplicates, keep only the final one
- **Before:** `ENTRYPOINT ["python", "app.py"]` / `ENTRYPOINT ["node", "server.js"]`
- **After:** `ENTRYPOINT ["node", "server.js"]`

#### DL3011 — Valid UNIX ports range from 0 to 65535
- **Severity:** error
- **Check:** EXPOSE with a port number outside 0-65535. Skip variable references (`$PORT`, `${PORT}`).
- **Why:** Invalid port numbers are silently accepted but have no effect. Always a typo or misconfiguration.
- **Fix:** Use a valid port number
- **Before:** `EXPOSE 99999`
- **After:** `EXPOSE 8080`

#### DL3012 — Multiple HEALTHCHECK instructions
- **Severity:** error
- **Check:** More than one HEALTHCHECK instruction in a single build stage
- **Why:** Only the last HEALTHCHECK takes effect. Multiple are always a mistake.
- **Fix:** Remove duplicates, keep only the final one

#### DL3024 — FROM aliases must be unique
- **Severity:** error
- **Check:** Duplicate `AS alias` names in FROM instructions
- **Why:** Duplicate aliases cause COPY --from to resolve to the wrong stage silently.
- **Fix:** Give each build stage a unique alias
- **Before:** `FROM node:20 AS build` / `FROM node:20 AS build`
- **After:** `FROM node:20 AS build` / `FROM node:20 AS runtime`

#### PG008 — Use an init process (tini) for proper signal handling and zombie reaping
- **Severity:** info
- **Check:** Final build stage has an ENTRYPOINT or CMD that runs a process without an init system (tini, dumb-init, or docker --init). Checks both JSON and shell form entrypoints.
- **Why:** When your application runs as PID 1 inside a container, the kernel treats it differently: SIGTERM has no default handler and is silently ignored. This means `docker stop` and Kubernetes graceful shutdown signals do nothing -- the container hangs for the full terminationGracePeriodSeconds until killed with SIGKILL. PID 1 is also responsible for reaping zombie child processes. Without an init process, orphaned children accumulate as zombies until the PID table is exhausted.
- **Fix:** Install tini and use it as the ENTRYPOINT
- **Before:** `CMD ["node", "server.js"]`
- **After:** `RUN apt-get update && apt-get install -y --no-install-recommends tini && rm -rf /var/lib/apt/lists/*\nENTRYPOINT ["/usr/bin/tini", "--"]\nCMD ["node", "server.js"]`

### Best Practice Rules (9 rules)

#### DL3027 — Do not use apt as it is meant to be an end-user tool
- **Severity:** warning
- **Check:** `apt install`, `apt remove`, etc. in RUN instructions (as opposed to `apt-get`)
- **Why:** `apt` is designed for interactive terminal use with progress bars and colors that break in Docker builds. `apt-get` is the stable, scriptable interface.
- **Fix:** Replace apt with apt-get
- **Before:** `RUN apt install -y curl`
- **After:** `RUN apt-get install -y curl`

#### DL3013 — Pin versions in pip install
- **Severity:** warning
- **Check:** `pip install` with unpinned packages (no `==version` suffix). Skip `-r requirements.txt` references.
- **Why:** Unpinned pip install pulls latest packages which can differ between builds, breaking reproducibility.
- **Fix:** Pin with == syntax
- **Before:** `RUN pip install flask requests`
- **After:** `RUN pip install flask==3.0.0 requests==2.31.0`

#### DL3001 — Avoid using interactive or system commands in RUN
- **Severity:** info
- **Check:** RUN using commands like ssh, vim, shutdown, service, ps, free, top, kill, mount
- **Why:** These are interactive or system-level tools meant for live server administration, not container builds. They indicate the container is being used like a VM.
- **Fix:** Remove interactive commands and use proper container patterns
- **Before:** `RUN service nginx start`
- **After:** `CMD ["nginx", "-g", "daemon off;"]`

#### DL3022 — COPY --from should reference a named build stage
- **Severity:** warning
- **Check:** `COPY --from=N` using numeric index instead of named alias
- **Why:** Numeric references break when stages are reordered. Named aliases are self-documenting and refactor-safe.
- **Fix:** Use a named alias
- **Before:** `COPY --from=0 /app/build /usr/share/nginx/html`
- **After:** `COPY --from=builder /app/build /usr/share/nginx/html`

#### DL3030 — Use the -y switch for yum install
- **Severity:** warning
- **Check:** `yum install` without `-y`
- **Why:** Without -y, yum prompts for confirmation, causing builds to hang.
- **Fix:** Add -y flag
- **Before:** `RUN yum install httpd`
- **After:** `RUN yum install -y httpd`

#### DL3033 — Pin versions in yum install
- **Severity:** warning
- **Check:** `yum install` with unpinned packages
- **Why:** Unpinned packages break build reproducibility.
- **Fix:** Pin with - syntax
- **Before:** `RUN yum install -y httpd`
- **After:** `RUN yum install -y httpd-2.4.6-99.el7`

#### DL3038 — Use the -y switch for dnf install
- **Severity:** warning
- **Check:** `dnf install` without `-y`
- **Why:** Without -y, dnf prompts for confirmation, causing builds to hang.
- **Fix:** Add -y flag
- **Before:** `RUN dnf install httpd`
- **After:** `RUN dnf install -y httpd`

#### DL3041 — Pin versions in dnf install
- **Severity:** warning
- **Check:** `dnf install` with unpinned packages
- **Why:** Unpinned packages break build reproducibility.
- **Fix:** Pin with - syntax
- **Before:** `RUN dnf install -y httpd`
- **After:** `RUN dnf install -y httpd-2.4.6-99.fc38`

#### PG005 — Inconsistent instruction casing
- **Severity:** info
- **Check:** Dockerfile instructions with mixed uppercase/lowercase (e.g., `FROM` with `run`)
- **Why:** Docker convention is UPPERCASE for all instructions. Mixed casing signals carelessness and reduces readability.
- **Fix:** Use consistent uppercase
- **Before:** `FROM node:20` / `run npm install` / `COPY . .`
- **After:** `FROM node:20` / `RUN npm install` / `COPY . .`

---

## Output Format

When presenting analysis results, use this structure:

```
## Dockerfile Analysis Results

**Score:** {score}/100 (Grade: {grade})

### Category Breakdown
| Category        | Score  | Weight |
|-----------------|--------|--------|
| Security        | {n}/100 | 30%   |
| Efficiency      | {n}/100 | 25%   |
| Maintainability | {n}/100 | 20%   |
| Reliability     | {n}/100 | 15%   |
| Best Practice   | {n}/100 | 10%   |

### Issues Found ({total} issues: {errors} errors, {warnings} warnings, {info} info)

#### Errors
- **Line {n} — {rule_id}: {title}** ({category})
  {explanation}
  **Fix:** {fix_description}

#### Warnings
...

#### Info
...
```

If the Dockerfile has zero violations, congratulate the user and note the perfect score.

## Fix Prompt Generation

When the user asks you to fix the Dockerfile (or you offer to after analysis), use this approach:

You are a senior DevOps engineer and Docker security specialist. Apply the identified issues precisely -- every flagged issue must be resolved while preserving the original image's intended functionality. Prioritize production-readiness, security, and minimal image size.

Apply fixes in priority order:
1. **Errors** -- broken or dangerous instructions, fix first
2. **Warnings** -- security risks or reproducibility problems, fix next
3. **Info** -- efficiency and best-practice improvements, fix last

When multiple issues affect the same line, combine all fixes into a single corrected instruction.

Preserve original functionality:
- Keep all intended packages, files, ports, and runtime commands
- Do not add packages or services beyond what resolves the issues
- If removing something (e.g., hardcoded secret), replace with a documented placeholder

Follow Dockerfile best practices when restructuring:
- Combine related RUN instructions with && and line continuations
- Order from least-frequently changing to most-frequently changing
- Use comments sparingly to explain non-obvious fixes

Output:
1. A summary mapping each issue to its fix, grouped by severity
2. The complete corrected Dockerfile in a `dockerfile` code block -- no omissions or placeholders

Constraints:
- Resolve ALL reported issues, including info-level
- Do not introduce new issues while fixing existing ones
- Do not change the base OS or runtime unless an issue requires it
- When pinning versions without specifics, use a comment placeholder rather than inventing numbers
- Never leave secrets in the final Dockerfile
