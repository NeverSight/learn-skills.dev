---
name: gradle-spring-boot-integration
description: |
  Configures Gradle with Spring Boot projects including plugin setup, bootable JAR creation,
  layered JARs for Docker optimization, and multi-module Spring Boot configurations.
  Use when asked to "set up Spring Boot with Gradle", "create executable JARs",
  "configure Docker layering", or "set up Spring Boot microservices".
---

Works with build.gradle.kts, application.yml, and Dockerfile configurations.
# Gradle Spring Boot Integration

## Table of Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Quick Start](#quick-start)
- [Instructions](#instructions)
- [Examples](#examples)
- [Commands Reference](#commands-reference)
- [Troubleshooting](#troubleshooting)
- [See Also](#see-also)

## Purpose

Set up and configure Spring Boot projects in Gradle with proper JAR creation, Docker optimization, and multi-module support. This skill covers bootable JAR setup, layered JARs for optimal Docker caching, and Spring Boot-specific task configuration.

## When to Use

Use this skill when you need to:
- Set up new Spring Boot projects with Gradle
- Create executable JAR files for Spring Boot applications
- Configure layered JARs for optimized Docker builds
- Set up multi-module projects with shared libraries
- Configure Spring Boot DevTools for hot reload
- Inject build information into application.yml
- Set up Spring Boot Actuator for monitoring
- Configure testing with Spring Boot test starters

## Quick Start

Minimal Spring Boot setup in `build.gradle.kts`:

```kotlin
plugins {
    id("java")
    id("org.springframework.boot") version "3.5.5"
    id("io.spring.dependency-management") version "1.1.7"
}

group = "com.example"
version = "0.0.1-SNAPSHOT"

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}

repositories {
    mavenCentral()
}

dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web")
    testImplementation("org.springframework.boot:spring-boot-starter-test")
}

tasks.test {
    useJUnitPlatform()
}
```

Run and build:

```bash
./gradlew bootRun                                    # Run locally
./gradlew bootJar                                    # Create executable JAR
./gradlew bootRun --args='--spring.profiles.active=dev'  # Run with profile
```

## Instructions

### Step 1: Apply Spring Boot Plugin

Configure the Spring Boot Gradle plugin for your project type:

```kotlin
// build.gradle.kts - Web Service (creates bootable JAR)
plugins {
    id("java")
    id("org.springframework.boot") version "3.5.5"
    id("io.spring.dependency-management") version "1.1.7"
}
```

**Key plugins**:
- `org.springframework.boot`: Creates executable JARs, provides bootRun task
- `io.spring.dependency-management`: Automatically imports Spring Boot BOM

### Step 2: Configure Java Toolchain

Specify Java version for consistency:

```kotlin
java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}
```

### Step 3: Add Spring Boot Dependencies

Use the BOM automatically imported by the plugin:

```kotlin
dependencies {
    // Spring Boot starter (no version needed - from BOM)
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.springframework.boot:spring-boot-starter-actuator")
    implementation("org.springframework.boot:spring-boot-starter-data-jpa")

    // Development only (DevTools for hot reload)
    developmentOnly("org.springframework.boot:spring-boot-devtools")

    // Test dependencies
    testImplementation("org.springframework.boot:spring-boot-starter-test")
}

// Enable JUnit 5
tasks.test {
    useJUnitPlatform()
}
```

### Step 4: Configure Bootable JAR Creation

**For services (executable JARs)**:

```kotlin
tasks.bootJar {
    enabled = true
    archiveClassifier = ""  // No classifier for main artifact
}

tasks.jar {
    enabled = false  // Disable plain JAR
}
```

**For libraries (plain JARs)**:

```kotlin
tasks.bootJar {
    enabled = false  // Not executable
}

tasks.jar {
    enabled = true  // Create library JAR
}
```

### Step 5: Enable Layered JARs for Docker Optimization

Layered JARs separate dependencies by change frequency for better Docker caching:

```kotlin
tasks.bootJar {
    enabled = true

    layered {
        enabled = true
        application {
            enabled = true
        }
        dependencies {
            enabled = true
        }
        springBootLoader {
            enabled = true
        }
        snapshot {
            enabled = true
        }
    }
}
```

**Layers** (in order):
1. **dependencies**: Rarely-changing external dependencies
2. **spring-boot-loader**: Spring Boot loader classes
3. **snapshot-dependencies**: Snapshot/SNAPSHOT versions (changing)
4. **application**: Application classes (most frequently changing)

**Extract layers in Dockerfile**:

```dockerfile
FROM eclipse-temurin:21-jre-alpine AS builder
WORKDIR /builder
COPY build/libs/app.jar .
RUN java -Djarmode=layertools -jar app.jar extract

FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
COPY --from=builder /builder/dependencies ./
COPY --from=builder /builder/spring-boot-loader ./
COPY --from=builder /builder/snapshot-dependencies ./
COPY --from=builder /builder/application ./
ENTRYPOINT ["java", "org.springframework.boot.loader.launch.JarLauncher"]
```

### Step 6: Configure Application Properties

Inject build information into `application.yml`:

```kotlin
tasks.processResources {
    filesMatching("application.yml") {
        expand(
            "version" to project.version,
            "name" to project.name,
            "timestamp" to System.currentTimeMillis()
        )
    }
}
```

In `application.yml`:

```yaml
spring:
  application:
    name: ${name}

info:
  app:
    name: ${name}
    version: ${version}
    build-timestamp: ${timestamp}
```

### Step 7: Set Up Spring Boot DevTools for Local Development

Enable hot reload during development:

```kotlin
dependencies {
    developmentOnly("org.springframework.boot:spring-boot-devtools")
}
```

**Trigger reload**:
- **IntelliJ**: Build Project (Cmd/Ctrl + F9)
- **Eclipse**: Save file
- **CLI**: Run `./gradlew compileJava` in separate terminal

### Step 8: Configure Actuator for Monitoring

Add actuator endpoints and metrics:

```kotlin
dependencies {
    implementation("org.springframework.boot:spring-boot-starter-actuator")
    implementation("io.micrometer:micrometer-registry-prometheus")
}
```

In `application.yml`:

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info,prometheus,metrics,env
  metrics:
    export:
      prometheus:
        enabled: true
  endpoint:
    health:
      show-details: always
```

## Examples

### Example 1: Simple Web Service

```kotlin
// build.gradle.kts
plugins {
    id("java")
    id("org.springframework.boot") version "3.5.5"
    id("io.spring.dependency-management") version "1.1.7"
}

group = "com.waitrose"
version = "1.0.0"

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}

repositories {
    mavenCentral()
}

dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.springframework.boot:spring-boot-starter-actuator")

    testImplementation("org.springframework.boot:spring-boot-starter-test")
}

tasks.test {
    useJUnitPlatform()
}

tasks.bootJar {
    enabled = true
}

tasks.jar {
    enabled = false
}
```

Build and run:

```bash
./gradlew bootJar              # Create JAR: build/libs/app-1.0.0.jar
java -jar build/libs/app-1.0.0.jar  # Run JAR
```

For advanced examples including multi-module setups, layered JARs with Docker, build info injection, and testing configurations, see [examples/advanced-examples.md](examples/advanced-examples.md).

## Commands Reference

See [references/commands-and-troubleshooting.md](references/commands-and-troubleshooting.md) for complete command reference and troubleshooting guide.

## See Also

- [gradle-dependency-management](../gradle-dependency-management/SKILL.md) - Manage Spring Boot BOMs and versions
- [gradle-docker-jib](../gradle-docker-jib/SKILL.md) - Build Docker images with Jib
- [gradle-testing-setup](../gradle-testing-setup/SKILL.md) - Configure Spring Boot testing
- [Spring Boot Gradle Plugin Documentation](https://docs.spring.io/spring-boot/docs/current/gradle-plugin/reference/)
- [Spring Boot Reference Guide](https://docs.spring.io/spring-boot/docs/)
