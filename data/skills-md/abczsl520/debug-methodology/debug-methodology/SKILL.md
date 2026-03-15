---
name: debug-methodology
description: Systematic debugging and problem-solving methodology. Activate when encountering unexpected errors, service failures, regression bugs, deployment issues, or when a fix attempt has failed twice. Also activate when proposing ANY fix to verify it addresses root cause (not a workaround). Prevents patch-chaining, wrong-environment restarts, workaround addiction, and "drunk man" random fixes.
---

# Debug Methodology

Systematic approach to debugging and problem-solving. Distilled from real production incidents and industry best practices.

## ⚠️ The Root Cause Imperative

**Every fix MUST target the root cause. Workarounds are forbidden unless explicitly approved.**

Before proposing ANY solution, pass the Root Cause Gate:

```
┌─────────────────────────────────────────────┐
│            ROOT CAUSE GATE                  │
│                                             │
│  1. What is the ACTUAL problem?             │
│  2. WHY does it happen? (not just WHAT)     │
│  3. Does my fix eliminate the WHY?           │
│     YES → proceed                           │
│     NO  → this is a workaround → STOP       │
│                                             │
│  Workaround test:                           │
│  "If I remove my fix, does the bug return?" │
│     YES → workaround (fix the cause instead)│
│     NO  → genuine fix ✅                    │
└─────────────────────────────────────────────┘
```

### The 5 Whys — Mandatory for Non-Obvious Problems

```
Problem: API returns 524 timeout
  Why? → Cloudflare cuts connections >100s
  Why? → The API call takes >100s
  Why? → Using non-streaming request, server holds connection silent
  Why? → Code uses regular fetch, not streaming
  Fix: → Use streaming (server sends data continuously, Cloudflare won't cut)

  ❌ WRONG: Switch to faster model (workaround — avoids the timeout instead of fixing it)
  ✅ RIGHT: Use streaming API (root cause — Cloudflare needs ongoing data)
```

### Common Workaround Traps

| Problem | Workaround (❌) | Root Cause Fix (✅) |
|---------|----------------|-------------------|
| API timeout | Switch to faster model | Use streaming / fix the slow query |
| Data precision loss | Search by name instead of ID | Fix BigInt parsing |
| Search returns nothing | Try different search strategy | Fix the search implementation |
| Dependency conflict | Downgrade / pin version | Use correct environment (venv) |
| Feature doesn't work | Remove the feature | Debug why it fails |

**Self-check question**: "Am I solving the problem, or avoiding it?"

## Phase 1: STOP — Assess Before Acting

Before ANY fix attempt:

```
□ What is the EXACT symptom? (error message, behavior, screenshot)
□ When did it last work? What changed since then?
□ How is the service running? (process, env, startup command)
```

For running services:
```bash
ps -p <PID> -o command=        # How was it started?
ls .venv/ venv/ env/           # Virtual environment?
which python3 && python3 --version
which node && node --version
```

**NEVER restart a service without first recording its original startup command.**

## Phase 2: Hypothesize — Form ONE Theory

Priority order:
1. **Did I change something?** → diff/revert first
2. **Did the environment change?** → versions, deps, configs
3. **Did external inputs change?** → API responses, data formats
4. **Genuine new bug?** → only after ruling out 1-3

## Phase 3: Test — One Change at a Time

```
Change X → Test → Works? → Done
                → Fails? → REVERT X → new hypothesis
```

**Do NOT stack changes.**

## Phase 4: Patch-Chain Detection

**2 fix attempts failed → STOP. Revert ALL. Back to Phase 1.**

You are likely:
- Fixing symptoms of a wrong fix
- In the wrong environment entirely
- Misunderstanding the architecture

## Phase 5: Post-Fix Verification

After any fix, verify:
```
□ Does it solve the ORIGINAL problem? (not just silence the error)
□ Did I introduce new issues? (regression check)
□ Would removing my fix bring the bug back? (confirms causality)
□ Is the fix in the right layer? (not patching symptoms upstream)
```

## Anti-Patterns

### 🚨 Workaround Addiction (NEW — Most Common!)
Bypassing the problem instead of fixing it. "It's slower but works" / "Use a different approach".
→ **Ask: "Am I solving or avoiding?"** If avoiding → find the real fix.
→ Workarounds are ONLY acceptable when: (1) explicitly approved by user, (2) clearly labeled as temporary, (3) a TODO is created for the real fix.

### 🚨 Drunk Man Anti-Pattern
Randomly changing things until the problem disappears.
→ Each change needs a hypothesis.

### 🚨 Streetlight Anti-Pattern
Looking where comfortable, not where the problem is.
→ "Is this where the bug IS, or where I KNOW HOW TO LOOK?"

### 🚨 Cargo Cult Fix
Copying a fix without understanding why it works.
→ Understand the mechanism first.

### 🚨 Ignoring the User
User says "it broke after you changed X" → immediately diff X.
→ User observations are the most valuable data.

## Environment Checklist

```
□ Runtime: system or venv/nvm?
□ Dependencies: match expected versions?
□ Config: .env, config.json — recent changes?
□ Process manager: PM2/systemd — restart method?
□ Logs: tail -f before reproducing
□ Backup: snapshot before any change
```

## Deployment Safety (Hardened SCP Flow)

**Iron Rule: NEVER edit files directly on the server. NEVER overwrite server files without backup.**

```
Standard deployment (every time, no exceptions):

1. PULL    scp server:/opt/apps/项目/ ./local-项目/
           (pull the files you need + related files)

2. EDIT    Make changes locally
           (complex multi-line → write full file, never sed)

3. VERIFY  node -c *.js                    # syntax check
           node -e "require('./file')"     # module load check
           (STOP if verification fails — do not proceed)

4. BACKUP  ssh server "cp file file.bak.$(date +%s)"

5. PUSH    scp ./local-file server:/opt/apps/项目/file

6. RESTART pm2 restart <app>
           (use SAME method as original — check ps/pm2 show first)

7. HEALTH  curl -s http://localhost:<port>/health
           pm2 logs <app> --lines 5 --nostream
           (if unhealthy → revert backup immediately)
```

### Pull Scope Rules
```
Changing 1 file    → pull that file + its imports/importers
Changing routes    → also pull server.js (check mount points)
Changing frontend  → also pull index.html (check script tags)
Changing config    → also pull code that reads the config
Unsure what to pull → pull the whole project directory
```

### What NOT to Do
```
❌ sed -i for multi-line code on server
❌ Skip node -c after editing .js
❌ pm2 restart before syntax verification
❌ Tell user to refresh before health check passes
❌ Push without backup
```

## 🚨 Server Code Modification Rules

**Every code change on a server MUST be syntax-verified before restart/reload.**

```
After editing .js files:
  □ node -c <file>                          # Syntax check
  □ node -e "require('./<file>')"           # Module load check (for route files)
  □ FAIL → DO NOT restart. DO NOT tell user to refresh. Fix first.

After editing .html files:
  □ Check critical tag closure (div/script/style)
  □ grep -c '<div' file && grep -c '</div' file   # Count match

Complex multi-line changes:
  □ Write complete file locally → scp upload
  □ NEVER use sed for multi-line code insertion (newlines get swallowed)
  □ If sed is unavoidable → verify with node -c immediately after

Restart sequence:
  □ node -c *.js passes → pm2 restart <app>
  □ Check pm2 logs --lines 5 for startup errors
  □ curl health endpoint to confirm service is up
```

**Why**: `sed -i` multi-line insertion silently corrupts JS (newlines become single line), causing syntax errors that break the entire page with no visible error to the user.

## Decision Tree

```
Problem appears
  ├─ I just edited something? → DIFF → REVERT if suspect
  ├─ Service won't start? → CHECK startup command + env
  ├─ New error after fix? → STOP (patch chain!) → Revert → Phase 1
  ├─ User reports regression? → DIFF before/after
  ├─ Tempted to work around? → ROOT CAUSE GATE → fix the real issue
  └─ Intermittent? → CHECK logs + external deps + timing
```
