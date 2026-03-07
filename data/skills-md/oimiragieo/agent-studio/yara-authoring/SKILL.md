---
name: yara-authoring
description: YARA-X detection rule authoring with expert judgment, linting, atom analysis, and best practices. Teaches how to think like an expert YARA author for malware detection, threat hunting, and indicator-of-compromise identification using YARA-X (the Rust-based successor to legacy YARA).
version: 1.1.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Bash, Glob, Grep]
args: '<sample-path|hash|description> [--format yara-x|legacy] [--lint] [--atoms]'
agents: [reverse-engineer, security-architect, penetration-tester]
category: security
best_practices:
  - Write rules targeting YARA-X syntax and features by default
  - Always include metadata fields (author, date, description, reference, hash)
  - Use atom analysis to verify rules have efficient matching atoms
  - Lint rules before deployment to catch common errors
  - Prefer specific byte patterns over broad wildcards to reduce false positives
error_handling: graceful
streaming: supported
verified: true
lastVerifiedAt: 2026-03-01T00:00:00.000Z
---

# YARA Authoring Skill

<!-- Agent: evolution-orchestrator | Task: #2 | Session: 2026-02-21 -->
<!-- License: CC-BY-SA-4.0 | Source: Trail of Bits (github.com/trailofbits/skills) -->
<!-- Attribution: Adapted from Trail of Bits yara-authoring skill -->

<identity>
Expert YARA-X detection rule authoring skill adapted from Trail of Bits security research methodology. Guides authoring of high-quality YARA-X rules for malware detection, threat hunting, and IOC identification. Emphasizes expert judgment, atom efficiency analysis, linting, and the YARA-X Rust-based toolchain.
</identity>

<capabilities>
- YARA-X rule authoring with expert-level patterns
- YARA-X syntax and feature usage (Rust-based successor to legacy YARA)
- Rule metadata standards (author, date, description, reference, hash)
- Atom analysis for matching efficiency verification
- Rule linting and validation
- String pattern design (hex, text, regex)
- Condition logic optimization
- False positive rate minimization
- Module usage (PE, ELF, Mach-O, dotnet, math, hash)
- Rule set organization and naming conventions
- Legacy YARA to YARA-X migration guidance
</capabilities>

## Overview

This skill implements Trail of Bits' YARA authoring methodology for the agent-studio framework. YARA-X is the Rust-based successor to legacy YARA, offering improved performance, safety, and new features. This skill teaches you to think and act like an expert YARA author, producing detection rules that are precise, efficient, and maintainable.

**Source repository**: `https://github.com/trailofbits/skills`
**License**: CC-BY-SA-4.0
**Target**: YARA-X (with legacy YARA compatibility guidance)

## When to Use

- When creating detection rules for malware samples
- When building threat hunting rules for IOC identification
- When converting legacy YARA rules to YARA-X format
- When optimizing existing rules for performance and accuracy
- When reviewing YARA rules for quality and false positive rates
- When building rule sets for automated scanning pipelines

## Iron Laws

1. **EVERY RULE MUST HAVE EFFICIENT ATOMS AND PASS LINTING** — a rule without efficient atoms degrades scanner performance across the entire rule set; always run `yr check` and `yr debug atoms` before deployment.
2. **NEVER write rules without testing against both positive and negative samples** — false positives on clean files are as harmful as missed detections; validate FP rate before deploying.
3. **ALWAYS include complete metadata** (author, date, description, reference, hash) — rules without metadata are unauditable and unmaintainable in enterprise rule sets.
4. **NEVER use single-byte atoms or patterns starting with common bytes** (0x00, 0xFF, 0x90) — these generate massive false positive rates and degrade the entire YARA scanning pipeline.
5. **ALWAYS use YARA-X toolchain (`yr`) by default** — legacy `yara`/`yarac` tooling lacks memory safety, performance optimizations, and modern module support; use YARA-X unless backward compatibility is explicitly required.

## YARA-X vs Legacy YARA

### Key Differences

| Feature     | Legacy YARA              | YARA-X                  |
| ----------- | ------------------------ | ----------------------- |
| Language    | C                        | Rust                    |
| Safety      | Manual memory management | Memory-safe             |
| Performance | Good                     | Better (parallelism)    |
| Modules     | PE, ELF, math, etc.      | Same + new modules      |
| Syntax      | YARA syntax              | Compatible + extensions |
| Toolchain   | `yara`, `yarac`          | `yr` CLI                |

### YARA-X CLI Commands

```bash
# Scan a file
yr scan rule.yar target_file

# Check rule syntax
yr check rule.yar

# View rule atoms (for efficiency analysis)
yr debug atoms rule.yar

# Format a rule
yr fmt rule.yar
```

## Rule Structure

### Standard Template

```yara
import "pe"
import "math"

rule MalwareFamily_Variant : tag1 tag2 {
    meta:
        author      = "analyst-name"
        date        = "2026-02-21"
        description = "Detects MalwareFamily variant based on [specific indicators]"
        reference   = "https://example.com/analysis-report"
        hash        = "sha256-of-sample"
        tlp         = "WHITE"
        score       = 75

    strings:
        // Unique byte sequences from the malware
        $hex_pattern1 = { 48 8B 05 ?? ?? ?? ?? 48 89 45 F0 }
        $hex_pattern2 = { E8 ?? ?? ?? ?? 85 C0 74 ?? }

        // String indicators
        $str_mutex   = "Global\\MalwareMutex_v2" ascii wide
        $str_c2      = "https://evil.example.com/gate.php" ascii
        $str_useragent = "Mozilla/5.0 (compatible; MalBot/1.0)" ascii

        // Encoded/obfuscated patterns
        $b64_config  = "aHR0cHM6Ly9ldmlsLmV4YW1wbGUuY29t" ascii  // base64

    condition:
        uint16(0) == 0x5A4D and  // MZ header (PE file)
        filesize < 5MB and
        (
            2 of ($hex_*) or
            ($str_mutex and 1 of ($str_c2, $str_useragent)) or
            $b64_config
        )
}
```

### Metadata Fields (Required)

| Field         | Purpose                    | Example                                  |
| ------------- | -------------------------- | ---------------------------------------- |
| `author`      | Who wrote the rule         | `"Trail of Bits"`                        |
| `date`        | When rule was created      | `"2026-02-21"`                           |
| `description` | What the rule detects      | `"Detects XYZ malware loader"`           |
| `reference`   | Source analysis/report     | `"https://..."`                          |
| `hash`        | Sample hash for validation | `"sha256:abc123..."`                     |
| `tlp`         | Traffic Light Protocol     | `"WHITE"`, `"GREEN"`, `"AMBER"`, `"RED"` |
| `score`       | Confidence (0-100)         | `75`                                     |

## String Pattern Best Practices

### Hex Patterns

```yara
// GOOD: Specific bytes with targeted wildcards
$good = { 48 8B 05 ?? ?? ?? ?? 48 89 45 F0 }

// BAD: Too many wildcards (poor atoms)
$bad = { ?? ?? ?? ?? 48 ?? ?? ?? ?? ?? }

// GOOD: Use jumps for variable-length gaps
$jump = { 48 8B 05 [4-8] 48 89 45 }

// GOOD: Use alternations for variant bytes
$alt = { 48 (8B | 89) 05 ?? ?? ?? ?? }
```

### Text Strings

```yara
// Case-insensitive matching
$str1 = "CreateRemoteThread" ascii nocase

// Wide strings (UTF-16)
$str2 = "cmd.exe" ascii wide

// Full-word matching (avoid substring false positives)
$str3 = "evil" ascii fullword
```

### Regular Expressions

```yara
// Use sparingly - regex is slower than literal strings
$re1 = /https?:\/\/[a-z0-9\-\.]+\.(xyz|top|club)\//

// Prefer hex patterns over regex for binary content
// WRONG: $re2 = /\x48\x8B\x05/
// RIGHT: $hex2 = { 48 8B 05 }
```

## Atom Analysis

**Atoms** are the fixed byte sequences YARA uses to pre-filter which rules to evaluate. Efficient atoms = fast scanning.

### How to Check Atoms

```bash
# View atoms for a rule
yr debug atoms rule.yar

# Good output: unique 4+ byte atoms
# Atom: 48 8B 05 (from $hex_pattern1)
# Atom: CreateRemoteThread (from $str1)

# Bad output: short or common atoms
# Atom: 00 00 (too common, will match everything)
```

### Atom Quality Guidelines

| Atom Length               | Quality    | Action                                    |
| ------------------------- | ---------- | ----------------------------------------- |
| 1-2 bytes                 | Poor       | Rewrite pattern with more specific bytes  |
| 3 bytes                   | Acceptable | Consider extending if possible            |
| 4+ bytes                  | Good       | Ideal for efficient scanning              |
| Common bytes (00, FF, 90) | Poor       | Avoid patterns starting with common bytes |

## Condition Logic

### Performance-Ordered Conditions

Place cheap checks first to enable short-circuit evaluation:

```yara
condition:
    // 1. File type check (instant)
    uint16(0) == 0x5A4D and

    // 2. File size check (instant)
    filesize < 10MB and

    // 3. Simple string matches (fast)
    $str_mutex and

    // 4. Complex conditions (slower)
    2 of ($hex_*) and

    // 5. Module calls (slowest)
    pe.imports("kernel32.dll", "VirtualAllocEx")
```

### Common Condition Patterns

```yara
// At least N of a set
2 of ($indicator_*)

// All of a set
all of ($required_*)

// Any of a set
any of ($optional_*)

// String at specific offset
$mz at 0

// String in specific range
$header in (0..1024)

// Count-based
#suspicious_call > 5
```

## Rule Categories

### Category 1: Malware Family Detection

Targets specific malware families with high-confidence indicators.

```yara
rule APT_Backdoor_SilentMoon {
    meta:
        description = "Detects SilentMoon backdoor used by APT group"
        score = 90
    strings:
        $config_marker = { 53 4D 43 46 47 } // "SMCFG"
        $decrypt_routine = { 31 C0 8A 04 08 34 ?? 88 04 08 41 }
    condition:
        uint16(0) == 0x5A4D and
        $config_marker and
        $decrypt_routine
}
```

### Category 2: Technique Detection

Targets specific attack techniques regardless of malware family.

```yara
rule TECHNIQUE_ProcessHollowing {
    meta:
        description = "Detects process hollowing technique indicators"
        score = 60
    strings:
        $api1 = "NtUnmapViewOfSection" ascii
        $api2 = "WriteProcessMemory" ascii
        $api3 = "SetThreadContext" ascii
        $api4 = "ResumeThread" ascii
    condition:
        uint16(0) == 0x5A4D and
        3 of ($api*)
}
```

### Category 3: Packer/Obfuscator Detection

Identifies packed or obfuscated executables.

```yara
rule PACKER_UPX {
    meta:
        description = "Detects UPX packed executables"
        score = 30
    strings:
        $upx0 = "UPX0" ascii
        $upx1 = "UPX1" ascii
        $upx2 = "UPX!" ascii
    condition:
        uint16(0) == 0x5A4D and
        2 of ($upx*)
}
```

## Common Pitfalls

1. **Over-broad rules**: Too many wildcards = too many false positives. Be specific.
2. **Under-tested rules**: Always test against known-clean files to measure FP rate.
3. **Missing metadata**: Rules without metadata are unmaintainable. Always include all required fields.
4. **Ignoring atoms**: A rule with poor atoms slows down the entire scanning pipeline.
5. **Hardcoded offsets**: Use `in (range)` instead of exact offsets when possible -- variants shift bytes.
6. **Legacy syntax**: Use YARA-X features and `yr` toolchain, not legacy `yara`/`yarac`.

## Linting Checklist

Before deploying any rule:

- [ ] Rule compiles without errors: `yr check rule.yar`
- [ ] Rule has efficient atoms: `yr debug atoms rule.yar`
- [ ] All required metadata fields present
- [ ] Tested against target sample (true positive confirmed)
- [ ] Tested against clean file corpus (false positive rate acceptable)
- [ ] Condition logic is performance-ordered (cheap checks first)
- [ ] No overly broad wildcard patterns
- [ ] Rule follows naming convention: `CATEGORY_FamilyName_Variant`

## Integration with Agent-Studio

### Recommended Workflow

1. Analyze malware sample with `binary-analysis-patterns` or `memory-forensics`
2. Extract indicators and patterns
3. Use `yara-authoring` to create detection rules
4. Lint and atom-analyze rules
5. Test rules against known samples and clean corpus
6. Use `variant-analysis` to find similar samples for rule tuning

### Complementary Skills

| Skill                          | Relationship                                       |
| ------------------------------ | -------------------------------------------------- |
| `binary-analysis-patterns`     | Extract indicators from malware for rule authoring |
| `memory-forensics`             | Extract memory artifacts for memory-scanning rules |
| `variant-analysis`             | Find malware variants to tune rule coverage        |
| `static-analysis`              | Automated analysis to complement YARA detection    |
| `protocol-reverse-engineering` | Extract network signatures for YARA rules          |

## Anti-Patterns

| Anti-Pattern                         | Why It Fails                                                                          | Correct Approach                                                              |
| ------------------------------------ | ------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Over-broad wildcards (`?? ?? ?? ??`) | Poor atoms cause rule to run against every file byte; massive performance degradation | Use at least 4 consecutive fixed bytes; scope wildcards to specific positions |
| Skipping atom analysis               | Invisible performance sink; rule may have 1-byte atoms causing false positives        | Always run `yr debug atoms rule.yar` before deployment                        |
| Missing metadata fields              | Rules become unauditable; cannot trace origin, sample, or analyst                     | Always include: author, date, description, reference, hash, tlp, score        |
| Conditions before file type checks   | Expensive string matching runs on non-matching file types                             | Place `uint16(0) == 0x5A4D` (or equivalent) first in every condition          |
| Using `nocase` on short strings      | Short case-insensitive patterns match everywhere in arbitrary data                    | Reserve `nocase` for strings >= 8 bytes; use exact case for shorter patterns  |

## Memory Protocol

**Before starting**: Check for existing YARA rules in the project for naming conventions and pattern reuse.

**During authoring**: Write rules incrementally, testing each against the target sample. Document atom analysis results.

**After completion**: Record effective patterns, atom quality metrics, and false positive rates to `.claude/context/memory/learnings.md` for improving future rule authoring.
