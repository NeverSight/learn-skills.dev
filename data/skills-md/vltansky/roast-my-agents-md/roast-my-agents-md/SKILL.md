---
name: roast-my-agents-md
description: >-
  Brutally honest AGENTS.md/CLAUDE.md review backed by real A/B test evidence. Not just opinions — actual proof that your rules are dead weight. Roasts instruction files for bloat, slop, and redundancy, then proves it by running evals. Use when user says "roast my agents.md", "roast my CLAUDE.md", "prove my rules are useless", "eval roast", or wants entertaining evidence-based feedback on their AI config files. Also triggers on "audit my instructions" or "are my rules helping".
---

# Roast My AGENTS.md (Evidence Edition)

Most AGENTS.md roasts are vibes. This one brings receipts.

Phase 1 does a quick static roast — the jokes, the sins, the token tax. Phase 2 is where it gets real: we actually run your rules through A/B tests and prove which ones the model already knows without being told. Phase 3 delivers the verdict with hard numbers.

**Tone:** Senior dev advocate + tech Twitter snark + Gordon Ramsay energy. Not mean-spirited, not discouraging. Punch up at patterns, not people.

## Phase 1: The Static Roast (fast, no evals)

### Step 0: Gather Data

Scan all instruction files in the project — root and nested. Run the audit script for data-backed roasts:

```bash
node {this-skill-path}/scripts/roast-audit.js {project-root}
```

Key data: `detectedSins`, `summary.totalInstructions` vs ~100 budget, `summary.estimatedMonthlyCost`, `files[].initDump`, `files[].anchoringTraps`, `files[].redundancy`, `files[].llmFingerprints`.

Also find all instruction files recursively:
```bash
find {project-root} -name "CLAUDE.md" -o -name "AGENTS.md" | grep -v node_modules | grep -v .git
```

### Step 1: Opening Roast

Brief intro, 2-4 specific zingers from audit data, quote the numbers. Fresh every time — never reuse jokes or openers. Pick a random roast style:

| Style | Vibe |
|-------|------|
| **Gordon Ramsay** | "This AGENTS.md is so raw it's still a README!" |
| **Disappointed Dad** | "I'm not mad about the 400-line root file. I'm just... disappointed." |
| **Stack Overflow** | "Duplicate of every auto-generated AGENTS.md ever. Closed." |
| **Therapist** | "Let's unpack why you thought agents need to be told to 'write clean code'." |
| **Sabra** | Tachles/Dugri/Balagan/Yalla — Hebrew hooks with English gloss |
| **The Prosecutor** | Data-first, builds a case, delivers the verdict |

### Step 2: Sin Inventory

Group by severity (invent fresh severity labels each time — not just "Critical/Serious/Minor"). Each sin: cite `file:line`, quote the actual text, one-liner roast.

**The Sins** (from worst to "at least you tried"):

| Sin | Why it hurts |
|-----|-------------|
| **Codebase overview / repo map** | Agents navigate FASTER without these. You're paying to slow them down. |
| **LLM-generated / `/init` dump** | ETH Zurich: -2-3% success, +20% cost. A cover letter for a job the agent already has. |
| **Discoverable info restated** | Agent reads package.json. You copied it. Now it reads it twice and trusts neither. |
| **Identity prompts** | "You are an expert" — a horoscope, not an instruction. |
| **Rules instead of feedback loops** | Tests, types, linters, CI can enforce this — prose can't. |
| **Contradictory instructions** | Two conflicting rules = agent paralysis. |
| **Bloated root in monorepo** (>100 lines) | In monorepos, root loads every request across all packages. Keep it as a compact map — pointers to `docs/` and nested AGENTS.md. Single-repo projects can go up to ~500 lines. |
| **Monolith — no nested AGENTS.md** | One flat root file for a monorepo? Each package deserves scoped rules that only load when the agent works there. |
| **No progressive disclosure in any AGENTS.md** | Even in a single-repo project, a 400-line AGENTS.md should extract detailed guides to `docs/` and reference them. Progressive disclosure isn't just for monorepos. |
| **Instruction budget overrun** (>150) | Every line past budget makes ALL lines weaker. |
| **Vague advice** | "Follow best practices" costs tokens and changes nothing. |
| **Style rules (not linter rules)** | Never send an LLM to do a linter's job. |

**NOT a sin — don't flag these:**
- **CLAUDE.md symlinked to AGENTS.md** — this is the recommended pattern for Claude Code compatibility
- **Same rules in AGENTS.md and `.windsurfrules`** — cross-tool duplication is intentional, each tool reads its own config
- **Nested AGENTS.md in subdirectories** — scoped rules for different packages is good progressive disclosure, not duplication

**Migration opportunity (mention, don't roast):**
- **`.cursor/rules/` alongside AGENTS.md** — Cursor now supports AGENTS.md natively. If both exist with similar content, suggest migrating `.cursor/rules/` into AGENTS.md and deleting the old format. This is a cleanup opportunity, not a sin.

### Step 3: Token Tax Receipt

```
TOKEN TAX RECEIPT
Total lines:               [N]     Noise: [N] ([X]%)    Signal: [N] ([Y]%)
Root AGENTS.md:            [N] lines (budget: <100 monorepo / <500 single repo)
Instruction count:         [N] / ~100 budget
Nested AGENTS.md files:    [N] (should match package/directory count)
Content in docs/:          [yes/no]
Tokens wasted/request:     ~[N]
Monthly cost (50 req/day): ~$[N]
Structure grade:           [monolith / partial / progressive disclosure]
Recommendation:            Delete [N] lines. Keep [N]. Move [N] to docs/ or nested AGENTS.md.
```

### Step 4: Scoreboard (Static)

Rate 1-10: Signal-to-Noise, Token Efficiency, Progressive Disclosure, Specificity. Overall X/10.

**Progressive Disclosure scoring** (applies to any AGENTS.md, not just monorepo roots):
- 1-3: Monolith — everything in one file, no docs/ references, no depth
- 4-6: Partial — some structure but detailed content still inline instead of in docs/
- 7-8: Good — core rules inline, detailed guides in docs/, referenced on demand
- 9-10: Exemplary — compact rules + pointers, all detailed content in docs/, scoped nested AGENTS.md in monorepos

**Size budgets:**
- Monorepo root: <100 lines (compact map — loads for every package)
- Single repo root: <500 lines
- Nested AGENTS.md (any): <500 lines (only loads when agent works in that directory)

Then deliver the punchline: "But this is just my opinion. Want me to actually *prove* it? I can run your rules through A/B tests and show you which ones the model already knows without your help."

**STOP. Wait for the user.** If they say yes to evidence, proceed to Phase 2. If they say "just fix it", skip to Phase 3 fixes.

---

## Phase 2: The Evidence Round (A/B eval-backed roasts)

This is where you go from "I think this rule is useless" to "I proved this rule is useless."

### The Codebase-Teaches-Patterns Effect

Real talk before we start: in controlled A/B testing, **25 of 26 assertions passed identically** with and without a 755-line instruction file. The model discovered React patterns, library conventions, helper functions, locale — all from reading existing code. The only thing that discriminated was pure coupling knowledge the codebase couldn't teach.

Most instruction files are 80-95% redundant. The evidence round proves exactly how redundant yours is.

### Step 5: Pick the Suspects

From the static roast, identify 3-5 rules that are most likely to be non-discriminating. Prioritize:
- Rules that restate discoverable info (tech stack, library choices, coding patterns)
- Rules about patterns visible in existing code
- Rules the model probably follows by default (modern coding style, etc.)

Also pick 1-2 rules you suspect ARE discriminating (coupling knowledge, non-obvious workflow) — these serve as positive controls.

Present the suspect lineup to the user: "Here are the rules I'm putting on trial. Any you want to add or skip?"

### Step 6: Generate Eval Prompts

For each suspect rule, create a targeted eval prompt from the project's commit history:

```bash
git -C {project-root} log --oneline -50
```

For each suspect, write a prompt that would test whether the model follows the rule WITHOUT being told. The prompt should be a realistic task, not a test question.

Each eval gets 2-4 assertions — mix of automated (grep-able) and manual.

### Step 7: Run the A/B Tests

Follow the clean baseline protocol. This is critical — contaminated baselines produce false acquittals.

**7a. Move all instruction files to /tmp/**
```bash
BACKUP_DIR="/tmp/roast-md-backup-$(date +%s)"
mkdir -p "$BACKUP_DIR"
for f in $(find {project-root} -name "CLAUDE.md" -o -name "AGENTS.md" | grep -v node_modules | grep -v .git); do
  REL_PATH="${f#{project-root}/}"
  mkdir -p "$BACKUP_DIR/$(dirname $REL_PATH)"
  mv "$f" "$BACKUP_DIR/$REL_PATH"
done

# User-level files: ASK the user first — these are outside the project.
# "Found global configs that will contaminate baselines. OK to temporarily rename?"
for f in ~/.claude/CLAUDE.md ~/.codex/AGENTS.md ~/.cursor/AGENTS.md; do
  [ -f "$f" ] && mv "$f" "${f}.bak"
done
find ~/.claude/projects -type d -name "memory" -exec sh -c 'mv "$1" "${1}_bak"' _ {} \; 2>/dev/null
```

**7b. Verify zero remain**
```bash
find {project-root} -name "CLAUDE.md" -o -name "AGENTS.md" | grep -v node_modules | grep -v .git | wc -l
# Must be 0
```

**7c. Spawn all baseline agents** — launch them all in one turn

**7d. WAIT for ALL to complete** — do NOT restore early

**7e. Restore all files (ALWAYS — even if baselines errored)**
```bash
for f in $(find "$BACKUP_DIR" -type f); do
  REL_PATH="${f#$BACKUP_DIR/}"
  mv "$f" "{project-root}/$REL_PATH"
done
# Restore user-level files (if renamed with user consent):
for f in ~/.claude/CLAUDE.md.bak ~/.codex/AGENTS.md.bak ~/.cursor/AGENTS.md.bak; do
  [ -f "$f" ] && mv "$f" "${f%.bak}"
done
find ~/.claude/projects -type d -name "memory_bak" -exec sh -c 'mv "$1" "${1%_bak}"' _ {} \; 2>/dev/null
```

**7f. Git checkout, then spawn all with-instruction agents**

### Step 8: The Trial Results

For each suspect rule, present the evidence:

```
EXHIBIT A: "[Rule text from AGENTS.md]"

CHARGE: Non-discriminating noise
EVIDENCE: Baseline agent [passed/failed] this assertion WITHOUT the rule.
          With-instruction agent [passed/failed].
VERDICT: [GUILTY — dead weight | ACQUITTED — actually useful | MISTRIAL — inconclusive]

[Comedy beat based on the verdict]
```

Guilty verdicts get roast escalation: "Not only is this rule useless — I proved it. The model knew [X] before reading your file. You're paying tokens to tell it what it already learned from your package.json."

Acquitted verdicts get grudging respect: "Fine. This one actually matters. The model had no idea about [X] without your instruction. I'll allow it."

---

## Phase 3: The Verdict

### Step 9: Evidence-Backed Scoreboard

```
FINAL VERDICT
Rules tested:     [N]
Guilty:           [N] (non-discriminating — proven dead weight)
Acquitted:        [N] (actually change behavior)
Mistrial:         [N] (inconclusive)

Static sins:      [N] from Phase 1
Total noise:      [X]% of your instruction file
Delta:            +[N]% improvement with instructions vs without
Token savings:    ~[N] tokens/request if you delete the guilty rules

SENTENCE: [Colorful summary based on the ratio]
```

Sentence examples:
- 90%+ guilty: "Your AGENTS.md is a participation trophy. The model was already doing everything you asked."
- 50-89% guilty: "Half your rules are dead weight. The other half are doing real work. Let's keep the workers and fire the rest."
- <50% guilty: "Respect. Most of your rules are actually earning their keep. You've been burned before."

### Step 10: Redemption Arc

Present fix options:
a) Delete guilty rules only (conservative)
b) Delete guilty + restructure for progressive disclosure **[recommended]**
c) Full rewrite based on evidence
d) Custom

**Option (b) always includes this restructuring:**

The ideal structure is a 3-level hierarchy:

```
project/
├── AGENTS.md              # <100 lines — compact map, pointers, gotchas only
├── CLAUDE.md -> AGENTS.md # symlink for Claude Code
├── docs/
│   ├── architecture.md    # how the system works
│   ├── testing.md         # test patterns, fixtures, helpers
│   └── conventions.md     # naming, patterns, style decisions
├── packages/api/
│   └── AGENTS.md          # API-specific rules (only loaded when working here)
├── packages/app/
│   └── AGENTS.md          # App-specific rules
└── packages/functions/
    └── AGENTS.md          # Functions-specific rules
```

**Root AGENTS.md** should be a compact map (<100 lines):
- Project identity (one line: what this is)
- Build/test/lint commands
- Critical gotchas that apply everywhere
- Pointers to `docs/` for details
- That's it. Everything else goes deeper.

**Nested AGENTS.md** files contain scoped rules that only load when the agent works in that directory. Package-specific conventions, framework quirks, local patterns.

**docs/** contains detailed guides the agent reads on demand — architecture decisions, testing patterns, deployment workflows. Referenced from root, never auto-loaded.

**STOP. Wait for user choice.** Then execute.

### Step 11: Execute and Prove

Apply the chosen fixes, then show before/after:
- Line count delta
- Token savings
- Which rules survived and why
- Re-run the audit script to show improved signal-to-noise

---

## Comedy Techniques

| Technique | Example |
|-----------|---------|
| **The receipt** | "I didn't just think your rule was useless — I proved it. Here's the receipt." |
| **The ls test** | "Your 'Project Structure' is what `ls -la` returns. You documented the filesystem." |
| **The package.json mirror** | "Lines 5-12 are lines 8-15 of package.json. The agent reads both. Trusts neither." |
| **The 1-minute test** | "Spawned a fresh agent, no instructions. Found your 'test runner is vitest' in 8 seconds." |
| **The /init fingerprint** | "Overview + Getting Started + Project Structure. ETH Zurich: 20% more cost, 2-3% worse." |
| **The trial escalation** | "Rule 7: Guilty. Rule 12: Guilty. Rule 15: Guilty. Your AGENTS.md is a crime scene." |
| **The acquittal surprise** | "I came to roast this rule but... the baseline agent had NO IDEA. Fine. You can keep it." |
| **The delta dunk** | "+3.8% improvement. 14 instruction files. 755 lines. That's 0.005% improvement per line." |
| **The feedback loop test** | "12 lines about indent style. ESLint does this in 1 config line. And enforces it." |
| **The budget counter** | "172 instructions. Budget is ~100. Every one past the limit makes ALL of them weaker." |
| **The monolith roast** | "400 lines in one root file. That's not progressive disclosure, that's a ransom note." |
| **The nesting nudge** | "Your packages/api has its own tsconfig, its own package.json, its own tests... but shares one AGENTS.md with the React app? Give it its own rules." |
| **The docs/ test** | "This 80-line architecture section loads every single request. Move it to docs/architecture.md — the agent will read it when it needs it." |

## Edge Case: Actually Good

"I came here to roast, but... 85%+ signal, most rules discriminating in A/B tests. You've either been burned before or you read the research. Only nitpicks remain." Rate high, list 1-2 small improvements.

## Edge Case: No Instruction Files

"Nothing to roast. Either you haven't started your AI config journey (brave) or you're in the wrong directory. Your agent is flying blind — but honestly, it's probably doing fine without your help."
