---
name: java-code-upgrade
description: Upgrade Java code from older idioms to modern equivalents. Scans for legacy patterns (pre-Java 10 through Java 25) across language features, collections, strings, streams, concurrency, input/output, error handling, date/time, security, tooling, and enterprise APIs, then suggests modern replacements with before/after examples. Use when modernizing Java codebases, reviewing pull requests for outdated patterns, or migrating from Java EE to Jakarta EE. Do not use for non-Java languages, build tool configuration, or framework-specific application logic.
---

# Java Evolved — Code Upgrade Skill

Modernize Java code by identifying legacy patterns and suggesting modern replacements with
before/after examples sourced from 113 patterns across 11 categories (Java 7 through Java 25).

## Procedures

**Step 1: Determine Upgrade Scope**

1. Identify the target JDK version for the project. Check `pom.xml`, `build.gradle`, or `.java-version` for the configured source/target level. If unspecified, ask the user.
2. Identify which categories are relevant to the task:
   - `language` — var, records, sealed classes, pattern matching, switch expressions, text blocks
   - `collections` — immutable factories, sequenced collections, unmodifiable collectors
   - `strings` — isBlank, strip, repeat, lines, formatted, text blocks
   - `streams` — toList, mapMulti, gatherers, takeWhile/dropWhile, optional improvements
   - `concurrency` — virtual threads, structured concurrency, scoped values, stable values
   - `io` — HTTP client, Files API, Path.of, transferTo, memory-mapped files
   - `errors` — helpful NPE, multi-catch, optional chaining, null-in-switch
   - `datetime` — java.time API, Duration/Period, HexFormat, Math.clamp
   - `security` — PEM encoding, KDF, strong random, TLS defaults
   - `tooling` — JShell, single-file execution, JFR, AOT preloading
   - `enterprise` — EJB to CDI, Servlet to JAX-RS, JDBC to JPA/jOOQ, SOAP to REST, Spring modernization
3. If performing a full codebase scan, proceed to Step 2. If upgrading specific code, skip to Step 3.

**Step 2: Scan for Legacy Patterns**

1. Read `references/detection-patterns.md` to load the detection signature database.
2. For each relevant category, search the codebase for the detection signatures listed:
   - Use grep/search for the specific code patterns documented (e.g., `Collections.unmodifiableList`, `new Thread(`, `.trim().isEmpty()`)
   - Track each match with file path, line number, and matched pattern slug.
3. Execute `python3 scripts/find-pattern.py --data-dir references/ --category {cat} --max-jdk {target} --format full` to retrieve the complete before/after transformation for each detected pattern.
4. Group findings by priority:
   - **Quick wins**: beginner difficulty, drop-in replacements (e.g., `var`, `List.of()`, `String.isBlank()`)
   - **Moderate**: intermediate difficulty, may require testing (e.g., records, sealed classes, virtual threads)
   - **Significant**: advanced difficulty, architectural changes (e.g., structured concurrency, enterprise migrations)
5. Format results using `assets/upgrade-report-template.md`.

**Step 3: Upgrade Specific Code**

1. Identify which legacy pattern the code uses. If unsure, read `references/detection-patterns.md` and match against the code.
2. Look up the specific pattern by executing:
   `python3 scripts/find-pattern.py --data-dir references/ --keyword "{pattern_name}" --format full`
3. Read the relevant category reference file from `references/{category}.md` for the complete transformation including:
   - Before/after code examples
   - Explanation of why the modern approach is better
   - JDK version requirements
   - Related patterns to consider alongside
4. Apply the transformation following the modern code example. Adapt to the specific codebase context — do not blindly copy-paste.
5. Check for related patterns that often co-occur. The reference files list `related` patterns for each entry.

**Step 4: Enterprise Migration Path**

If the codebase involves Java EE or early Jakarta EE, read `references/enterprise.md` for the complete migration mappings:
- EJB to CDI beans
- Servlet to JAX-RS endpoints
- JSF managed beans to CDI named beans
- JNDI lookups to CDI injection
- JPA EntityManager to Jakarta Data repositories
- SOAP web services to Jakarta REST
- Message-driven beans to reactive messaging
- Manual transactions to declarative @Transactional
- Spring XML configuration to annotation-driven
- Spring null safety to JSpecify

**Step 5: Validate Upgrades**

1. Verify the target JDK version supports all applied patterns. Each pattern specifies its minimum JDK version.
2. Ensure no pattern requires a JDK version higher than the project target.
3. Run the project's existing test suite to confirm no regressions.
4. For patterns marked as preview features, verify the project enables preview: `--enable-preview`.

## Quick Reference by JDK Version

| JDK | Key Patterns |
|-----|-------------|
| 7   | multi-catch, diamond operator |
| 8   | default/static interface methods, streams, CompletableFuture, java.time |
| 9   | List/Set/Map.of(), Optional.or/ifPresentOrElse, private interface methods, Stream.ofNullable/takeWhile/dropWhile, process API |
| 10  | var, unmodifiable copy, Optional.orElseThrow |
| 11  | String.isBlank/strip/repeat/lines, HTTP client, Path.of, single-file execution, Predicate.not |
| 12  | String.indent/transform, Files.mismatch, Collectors.teeing |
| 14  | switch expressions, helpful NPE |
| 15  | text blocks, String.formatted |
| 16  | records, Stream.toList, mapMulti, unmodifiable collectors, record-based errors, static members in inner classes |
| 17  | sealed classes, RandomGenerator, HexFormat |
| 18  | built-in HTTP server |
| 19  | executor try-with-resources, Thread.sleep(Duration) |
| 21  | virtual threads, pattern matching (instanceof + switch), sequenced collections, unnamed variables, guarded patterns, null-in-switch, Math.clamp |
| 22  | unnamed variables, multi-file source, FFM API (call C from Java), file memory mapping |
| 23  | markdown Javadoc |
| 24  | stream gatherers |
| 25  | structured concurrency, scoped values, stable values, flexible constructors, compact source files, module imports, primitive patterns, AOT preloading, PEM encoding, KDF, IO class |

## Error Handling

- If `scripts/find-pattern.py` fails with a file-not-found error, verify the `--data-dir` points to the `references/` directory containing the category markdown files.
- If a pattern requires a JDK version higher than the project target, flag it as "future upgrade" rather than applying it.
- If the YAML data files are missing, the reference markdown files in `references/` contain all pattern data and can be used directly without the script.
- If a detection signature matches but the code context differs from the pattern (e.g., intentional use of old API), skip the suggestion and note why.
