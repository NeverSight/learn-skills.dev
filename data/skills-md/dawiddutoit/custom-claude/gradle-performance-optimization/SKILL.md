---
name: gradle-performance-optimization
description: |
  Optimizes Gradle build performance through caching strategies, configuration cache, parallel
  execution, and memory tuning to achieve 50-80% faster builds for large projects. Use when
  builds are slow (>2 minutes), optimizing CI/CD pipelines, or configuring new Gradle projects.
  Triggers on "speed up Gradle", "slow builds", "optimize CI/CD", "reduce build time", or
  "configure Gradle performance". Works with gradle.properties, build.gradle.kts, GitHub Actions,
  and GitLab CI configurations using build cache, configuration cache, and parallel execution.
---
# Gradle Performance Optimization

## Table of Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Quick Start](#quick-start)
- [Instructions](#instructions)
- [Examples](#examples)
- [Commands Reference](#commands-reference)
- [Troubleshooting](#troubleshooting)
- [Performance Optimization Checklist](#performance-optimization-checklist)
- [See Also](#see-also)

## Purpose

Dramatically improve Gradle build speed through intelligent caching, parallel execution, and configuration optimization. Properly configured projects can see 50-80% reduction in build times.

## When to Use

Use this skill when you need to:
- Speed up slow Gradle builds (>2 minutes for medium projects)
- Optimize CI/CD pipeline build times
- Configure caching for multi-module projects
- Enable configuration cache for faster configuration phase
- Set up parallel execution for independent subprojects
- Tune JVM memory settings for large projects
- Generate build scans to identify performance bottlenecks
- Implement dependency locking for reproducible builds

## Quick Start

Add these lines to `gradle.properties`:

```properties
# Enable caching (87% faster with cache hits)
org.gradle.caching=true
org.gradle.configuration-cache=true

# Enable parallel execution
org.gradle.parallel=true

# Configure memory (4GB for most projects)
org.gradle.jvmargs=-Xmx4g -XX:MaxMetaspaceSize=1g -XX:+HeapDumpOnOutOfMemoryError -Dfile.encoding=UTF-8

# Keep daemon running (enabled by default)
org.gradle.daemon=true
```

Then run:

```bash
./gradlew build --build-cache --parallel
```

## Instructions

### Step 1: Enable Build Cache

The build cache stores task outputs and reuses them when inputs haven't changed.

**Enable local cache in `gradle.properties`**:

```properties
org.gradle.caching=true
```

**Results**: 87% faster builds on cache hits (35s down to 4.5s example)

**Configure remote cache for CI** (optional but recommended for teams):

```kotlin
// settings.gradle.kts
buildCache {
    local {
        isEnabled = true
    }
    remote<HttpBuildCache> {
        url = uri("https://build-cache.company.com/cache/")
        isEnabled = true
        isPush = System.getenv("CI") == "true"  // Only CI pushes
        credentials {
            username = System.getenv("CACHE_USERNAME")
            password = System.getenv("CACHE_PASSWORD")
        }
    }
}
```

### Step 2: Enable Configuration Cache

Configuration cache skips the entire configuration phase when inputs haven't changed. Gradle 8.11+ gives 65% median time reduction.

**Enable in `gradle.properties`**:

```properties
org.gradle.configuration-cache=true
org.gradle.configuration-cache.problems=warn  # Start with warnings
```

**Verify compatibility**:

```bash
./gradlew help --configuration-cache
```

**Check configuration cache report**:

```
build/reports/configuration-cache/<hash>/configuration-cache-report.html
```

### Step 3: Enable Parallel Execution

Execute tasks from different projects simultaneously.

**Enable in `gradle.properties`**:

```properties
org.gradle.parallel=true
org.gradle.workers.max=4  # Adjust based on CPU cores (default: num cores)
```

**Effectiveness**: 30-50% faster for multi-module projects

**Note**: Requires independent subprojects; tasks within same project run sequentially unless using configuration cache.

### Step 4: Configure Memory Settings

Proper JVM heap allocation is critical for large projects.

**For most projects (up to 30 modules) in `gradle.properties`**:

```properties
org.gradle.jvmargs=-Xmx4g -XX:MaxMetaspaceSize=1g -XX:+HeapDumpOnOutOfMemoryError -Dfile.encoding=UTF-8
```

**For large projects (30+ modules)**:

```properties
org.gradle.jvmargs=-Xmx8g -XX:MaxMetaspaceSize=2g -XX:+HeapDumpOnOutOfMemoryError -Dfile.encoding=UTF-8
```

**Memory allocation guidelines**:
- Small projects (1-10 modules): 2-4 GB (`-Xmx2g` to `-Xmx4g`)
- Medium projects (10-30 modules): 4-6 GB (`-Xmx4g` to `-Xmx6g`)
- Large projects (30+ modules): 6-8 GB (`-Xmx6g` to `-Xmx8g`)

### Step 5: Configure Daemon Settings

Gradle daemon is enabled by default but can be optimized.

**In `gradle.properties`**:

```properties
org.gradle.daemon=true
org.gradle.daemon.idletimeout=3600000  # 1 hour (default: 3 hours)
```

**Manage daemon**:

```bash
./gradlew --status              # Show running daemons
./gradlew --stop                # Stop all daemons
./gradlew build --no-daemon     # Run without daemon (for debugging)
```

### Step 6: Dependency Resolution Optimization

Lock dependency versions for reproducible, faster builds.

**Generate lock files**:

```bash
./gradlew dependencies --write-locks
```

**Result**: `gradle.lockfile` and configuration-specific lock files created

**Verify against locks**:

```bash
./gradlew dependencies --verify-locks
```

### Step 7: Enable Build Scans

Visualize build performance and identify bottlenecks.

**One-time scan**:

```bash
./gradlew build --scan
```

**Automatic scanning in builds**:

```kotlin
// build.gradle.kts
plugins {
    id("com.gradle.build-scan") version "3.17"
}

buildScan {
    termsOfServiceUrl = "https://gradle.com/terms-of-service"
    termsOfServiceAgree = "yes"
    publishAlways()
}
```

### Step 8: Optimize CI/CD Configuration

Detect CI environment and adjust behavior:

```kotlin
// build.gradle.kts
val isCi = System.getenv("CI") != null

if (isCi) {
    // CI-specific build scan
    buildScan {
        termsOfServiceUrl = "https://gradle.com/terms-of-service"
        termsOfServiceAgree = "yes"
        publishAlways()
        tag("CI")
        tag(System.getenv("CI_COMMIT_REF_NAME") ?: "unknown")
    }
}
```

## Examples

### Example 1: Complete Optimized gradle.properties

```properties
# Gradle Optimization Configuration

# === CACHING ===
# Build cache - stores task outputs for reuse (87% faster on hits)
org.gradle.caching=true

# Configuration cache - skip configuration phase (65% faster median time)
org.gradle.configuration-cache=true
org.gradle.configuration-cache.problems=warn

# === EXECUTION ===
# Parallel execution - run tasks from different projects simultaneously
org.gradle.parallel=true
org.gradle.workers.max=4

# Daemon - long-running JVM process (enabled by default)
org.gradle.daemon=true
org.gradle.daemon.idletimeout=3600000

# === MEMORY ===
# JVM heap for Gradle daemon (adjust for project size)
org.gradle.jvmargs=-Xmx4g -XX:MaxMetaspaceSize=1g -XX:+HeapDumpOnOutOfMemoryError -Dfile.encoding=UTF-8

# === DEBUGGING ===
# Uncomment if needed
# org.gradle.logging.level=info
# org.gradle.debug=true
```

### Example 2: Enabling Configuration Cache with Warnings

Start with warnings to identify incompatible plugins:

```properties
# gradle.properties
org.gradle.configuration-cache=true
org.gradle.configuration-cache.problems=warn  # Shows warnings instead of failing
```

Monitor output:

```bash
./gradlew build 2>&1 | grep -i "configuration-cache"
```

Fix issues, then switch to strict mode:

```properties
# Once all issues are fixed
org.gradle.configuration-cache=true
org.gradle.configuration-cache.problems=fail  # Now strict
```

### Example 3: CI/CD GitHub Actions with Optimization

```yaml
# .github/workflows/build.yml
name: Optimized Build

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up JDK 21
      uses: actions/setup-java@v4
      with:
        java-version: '21'
        distribution: 'temurin'

    - name: Setup Gradle (official action with caching)
      uses: gradle/actions/setup-gradle@v4
      with:
        cache-encryption-key: ${{ secrets.GRADLE_ENCRYPTION_KEY }}

    - name: Build with Gradle (optimized)
      run: ./gradlew build --parallel --build-cache --configuration-cache --scan
      env:
        CI: true

    - name: Upload build scans
      if: always()
      uses: actions/upload-artifact@v4
      with:
        name: build-scans
        path: build/reports/
```

### Example 4: GitLab CI/CD with Performance Tuning

```yaml
# .gitlab-ci.yml
image: gradle:8.11-jdk21-alpine

variables:
  GRADLE_OPTS: "-Dorg.gradle.daemon=false -Dorg.gradle.caching=true -Dorg.gradle.parallel=true"
  GRADLE_USER_HOME: "$CI_PROJECT_DIR/.gradle"

cache:
  key: "$CI_COMMIT_REF_SLUG"
  paths:
    - .gradle/wrapper
    - .gradle/caches

build:
  stage: build
  script:
    - chmod +x ./gradlew
    - ./gradlew assemble --parallel --build-cache --configuration-cache
  artifacts:
    paths:
      - build/libs/*.jar
    expire_in: 1 day

test:
  stage: test
  script:
    - ./gradlew test --parallel --build-cache --configuration-cache
  artifacts:
    when: always
    reports:
      junit: build/test-results/test/TEST-*.xml
```

### Example 5: Measuring Build Performance Improvement

```bash
# Before optimization
time ./gradlew clean build
# Real    2m 30s

# After optimization
time ./gradlew build --parallel --build-cache --configuration-cache
# Real    0m 45s (82% improvement!)

# Generate build scan for detailed analysis
./gradlew build --scan
# Opens scan at https://scans.gradle.com
```

### Example 6: Dependency Locking for Consistency

```bash
# Generate lock files
./gradlew dependencies --write-locks

# Verify locks in CI
./gradlew dependencies --verify-locks

# Update lock files (controlled)
./gradlew dependencies --write-locks --refresh-dependencies
```

## Commands Reference

See [references/commands-and-troubleshooting.md](references/commands-and-troubleshooting.md) for complete command reference, troubleshooting guide, and optimization checklist.

## See Also

- [gradle-dependency-management](../gradle-dependency-management/SKILL.md) - Optimize dependency resolution
- [gradle-troubleshooting](../gradle-troubleshooting/SKILL.md) - Diagnose slow builds
- [Gradle Build Scans](https://scans.gradle.com/) - Analyze build performance
- [Gradle Performance Guide](https://docs.gradle.org/current/userguide/performance.html)
