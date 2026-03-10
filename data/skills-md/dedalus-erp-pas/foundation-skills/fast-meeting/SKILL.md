---
name: fast-meeting
description: Run a fast autonomous meeting with auto-selected personas, implement the decision, create a MR/PR, commit, push, and post a French summary — all without user intervention.
allowed-tools: gitlab-mcp(get_issue), gitlab-mcp(create_issue_note), gitlab-mcp(update_issue), gitlab-mcp(list_issues), gitlab-mcp(create_merge_request), gitlab-mcp(update_merge_request)
license: MIT
metadata:
  author: Foundation Skills
  version: 1.0.0
---

# Fast Meeting

Run a fully autonomous meeting with expert personas, then immediately implement the recommended solution, create a merge request or pull request, and post a French description — all without asking the user for confirmation.

## When to Use This Skill

Activate when the user:
- Demande un « fast meeting » ou « réunion rapide » sur un sujet
- Veut une décision ET une implémentation automatique sans interruption
- Dit « fast-meeting » ou « lance un fast meeting sur... »
- Veut qu'un sujet soit analysé, décidé et implémenté en une seule commande

## Core Principles

### 1. Full Autonomy
- The entire pipeline runs without asking any user questions
- Persona selection is automatic based on context analysis
- The best course of action is implemented immediately after the meeting
- A MR/PR is created automatically on the detected remote (GitLab or GitHub)

### 2. Speed Over Thoroughness
- The meeting is compressed: 2 rounds instead of 3 (opening + convergence)
- Personas are limited to 3-4 maximum
- The analysis is concise and action-oriented
- Implementation starts as soon as the meeting concludes

### 3. Diverse but Focused Perspectives
- Personas are auto-selected based on the subject matter
- Each persona brings a genuinely different viewpoint
- The meeting converges quickly toward an actionable recommendation

### 4. Complete Delivery
- Code changes are committed on a dedicated branch
- A MR/PR is created automatically
- The MR/PR description in French summarizes the meeting analysis and implementation

## Workflow

### Step 1: Understand the Subject and Gather Context

1. **Read the user's prompt** — extract the topic, constraints, and goals
2. **If an issue is referenced** (GitLab `#123` or GitHub `#123`):
   - Fetch the issue details (description, labels, comments)
3. **If code is involved**, read relevant files to understand the current state
4. **Detect the remote repository type:**
   - Run `git remote -v` to determine if the remote is GitLab or GitHub
   - Store this for Step 6 (MR/PR creation)
5. **Identify the decision to make** — frame it as a clear one-line question

Output the decision question before proceeding. Example:
> "Question: Should we migrate the authentication system from session-based to JWT tokens?"

### Step 2: Auto-Select Personas

Automatically select 3-4 personas based on the subject matter. Use these heuristics:

| Subject involves... | Auto-select personas |
|---------------------|---------------------|
| Backend / API / database | SOLID Alex (Backend), Whiteboard Damien (Architect), EXPLAIN PLAN Isabelle (Oracle DBA) |
| Frontend / UI / UX | Pixel-Perfect Hugo (Frontend), Figma Fiona (UX/UI), Sprint Zero Sarah (PO), Whiteboard Damien (Architect) |
| Security / auth / access control | Paranoid Shug (Security), RGPD Raphaël (DPO), SOLID Alex (Backend), Whiteboard Damien (Architect) |
| Infrastructure / deploy / CI-CD | Pipeline Mo (DevOps), SOLID Alex (Backend), Whiteboard Damien (Architect) |
| Data / migration / ETL | Schema JB (Data), EXPLAIN PLAN Isabelle (Oracle DBA), Whiteboard Damien (Architect) |
| Interoperability / HL7 / FHIR / HPK | RFC Santiago (Interop PO), HL7 Victor (Interop Dev), SOLID Alex (Backend) |
| Legacy / Uniface / modernization | Legacy Larry (Uniface), Whiteboard Damien (Architect), SOLID Alex (Backend) |
| Testing / quality / regression | Edge-Case Nico (QA), SOLID Alex (Backend), Pipeline Mo (DevOps) |
| Product / feature / UX decision | Sprint Zero Sarah (PO), Pixel-Perfect Hugo (Frontend), Figma Fiona (UX/UI), Whiteboard Damien (Architect) |
| Healthcare / clinical workflows | Dr. Workflow Wendy (Healthcare), Sprint Zero Sarah (PO), RGPD Raphaël (DPO) |
| GDPR / data privacy / compliance | RGPD Raphaël (DPO), Paranoid Shug (Security), Whiteboard Damien (Architect) |
| Full-stack / mixed concern | Whiteboard Damien (Architect), SOLID Alex (Backend), Sprint Zero Sarah (PO), Edge-Case Nico (QA) |

If the subject spans multiple areas, pick the most relevant 3-4 personas. Always include **Whiteboard Damien (Architect)** for technical decisions. Always include **Sprint Zero Sarah (PO)** for product decisions.

**Custom personas:** If the subject is domain-specific (healthcare, finance, legal...), create a relevant domain expert persona automatically.

#### Persona Pool

| Persona | Role | Perspective | Bias |
|---------|------|-------------|------|
| **SOLID Alex** | Senior Backend Engineer, clean code evangelist & design patterns enforcer | Code quality, maintainability, technical debt | Prefers proven patterns, cautious about new tech |
| **Sprint Zero Sarah** | Product Owner, backlog tyrant & velocity obsessed | User value, delivery speed, business impact | Prefers shipping fast, pragmatic trade-offs |
| **Paranoid Shug** | Security Engineer (OWASP certified) | Attack surface analysis, web security (OWASP Top 10), authentication standards (OAuth2, OpenID Connect, JWT), penetration testing, vulnerability scanning, secure coding practices | Prefers the most secure option, systematically challenges exposed surfaces, assumes every input is hostile |
| **Pipeline Mo** | DevOps/SRE Engineer, CI/CD perfectionist & zero-downtime deployer | Operability, monitoring, deployment, scalability, Docker, Kubernetes, IaC (Terraform/Ansible), observability (Grafana, Prometheus, ELK), incident response | Prefers simple infrastructure, observable systems, won't approve anything without a rollback plan |
| **Pixel-Perfect Hugo** | Frontend Engineer, CSS wizard & component library champion | User experience, frontend performance, Vue.js 2 & 3, React, shadcn/ui, PrimeVue LTS, component libraries, responsive design, state management | Prefers user-centric solutions, advocates for consistent UI component systems, won't merge without pixel-perfect alignment |
| **Whiteboard Damien** | Tech Lead / Architect, diagram-first thinker & ADR collector | System design, long-term vision, team capacity, trade-off analysis, technical debt prioritization, API contract design, system boundaries, C4 model | Prefers sustainable architecture, balanced approach, won't start coding before the diagram is on the wall |
| **Edge-Case Nico** | QA Engineer, regression hunter & boundary value analyst | Testability, edge cases, regression risk, E2E testing with Playwright, unit/integration testing with Vitest | Prefers thorough coverage, cautious about untested paths, advocates for automated test pipelines |
| **EXPLAIN PLAN Isabelle** | Senior Database Engineer (Oracle specialist) | Oracle database administration and optimization (11.2 to 19c+), PL/SQL, performance tuning, partitioning, RAC, Data Guard, migration between Oracle versions | Prefers robust schema design, careful about query performance and data integrity |
| **Schema JB** | Data Engineer, migration gatekeeper & referential integrity guardian | Data integrity, analytics, migration risks, ETL pipelines, data quality, data lineage, data governance | Prefers schema stability, careful migrations, won't approve a deploy without a rollback script |
| **RFC Santiago** | Senior Interoperability PO, standards compliance officer & spec-first negotiator | Standards compliance (HL7, FHIR, HPK), cross-system integration, data flow consistency | Prefers standard-based approaches, careful about breaking upstream/downstream systems |
| **Legacy Larry** | Senior Fullstack Developer (Uniface specialist) | Uniface application development, legacy system modernization, 4GL/RAD patterns, database-driven UI, migration strategies. Documentation: https://erp-pas.gitlab-pages-erp-pas.dedalus.lan/hexagone/uniface/ | Prefers pragmatic evolution over rewrite, deep knowledge of Uniface runtime and deployment |
| **HL7 Victor** | Senior Interoperability Fullstack Developer, message parser & protocol translator | End-to-end integration (API, middleware, frontend), message parsing (HL7, FHIR, HPK), system connectors, data mapping and transformation | Prefers pragmatic solutions that work across the full stack, bridges the gap between standards and implementation |
| **RGPD Raphaël** | DPO / Compliance Officer, health data regulation specialist & consent watchdog | GDPR/RGPD compliance, HDS certification, patient data protection, consent management, data retention policies, audit trails | Prefers the most compliant option, blocks anything that touches personal data without proper justification, risk-averse on legal exposure |
| **Dr. Workflow Wendy** | Healthcare Domain Expert, clinical process analyst & patient journey guardian | Hospital workflows, patient administration, medical terminology, clinical use cases, end-user adoption, functional specifications | Prefers solutions that match real clinical reality, pushes back on tech-first approaches that ignore how hospitals actually work |
| **Figma Fiona** | UX/UI Designer, user research advocate & design system curator | User research, wireframes, design consistency, design tokens, accessibility (WCAG), user testing, information architecture | Prefers design-first approaches, challenges any UI decision made without user validation, advocates for consistent design systems |

**Announce the selected personas and their roles before starting the meeting.**

### Step 3: Run the Fast Meeting

The meeting uses sub-agents to run each persona independently and in parallel. The fast meeting compresses the process into 2 rounds.

**IMPORTANT: Use the Agent tool to launch each persona as a separate sub-agent.**

#### Round 1: Position and Recommendation (Parallel Sub-Agents)

Launch one sub-agent per persona **in parallel** using the Agent tool. Each sub-agent receives:

1. The **decision question** from Step 1
2. All **context** gathered (issue details, code snippets, constraints)
3. The persona's **identity prompt**

**Sub-agent prompt template:**

```
You are {name}, a {role}.

Your perspective: {perspective}
Your natural bias: {bias}

You are participating in a fast meeting about: {decision_question}

Context:
{context}

As {name}, provide your position:
1. What is your recommended approach? Be specific and concrete.
2. What are the top 2 risks? Be specific about failure scenarios.
3. What is your preferred implementation strategy in concrete steps?
4. What would you push back on from other typical perspectives?

Stay fully in character. Be concise and actionable — this is a fast meeting.

This is a research task — do NOT write or edit any files.
```

**Launch ALL persona sub-agents in a single message** so they run in parallel. Use `subagent_type: "general-purpose"` and a short description like `"Fast persona: {name}"`.

**Collect all positions** and present them as quotes:

> **SOLID Alex (Senior Backend Engineer):** "I recommend..."

#### Anti-Groupthink Check

After collecting Round 1 responses, evaluate the consensus level:

1. **Check if all personas converged on the same approach** (same recommendation, no meaningful disagreement)
2. **If consensus is too high** (all personas agree on the approach with no pushback):
   - Launch **one additional sub-agent** as a devil's advocate, prompted to find the strongest argument against the consensus position
   - Use this prompt:
     ```
     You are a devil's advocate in a fast meeting.

     All participants agreed on this approach: {consensus_summary}

     Your job: find the strongest possible argument AGAINST this consensus.
     - What could go wrong that nobody mentioned?
     - What assumption are they all making that might be false?
     - What alternative did they dismiss too quickly?

     Be specific and concrete. Reference real failure scenarios.
     This is a research task — do NOT write or edit any files.
     ```
   - Include the dissenting view in the analysis even if the recommendation doesn't change
3. **If there is already meaningful disagreement:** proceed directly to Round 2

#### Round 2: Convergence (Single Synthesis)

After collecting all Round 1 responses, **you** (the facilitator, not a sub-agent) synthesize:

- Points of agreement across personas
- Key trade-offs that emerged
- The **winning recommendation** with rationale
- Concrete implementation plan (files to change, approach, order of operations)

**Do NOT launch a second round of sub-agents.** Synthesize directly for speed.

### Step 4: Produce the Compact Decision

Write a compact analysis displayed to the user:

```markdown
## Fast Meeting : [Sujet]

**Question :** [La question de décision]

**Participants :** [Name (Role)] | [Name (Role)] | [Name (Role)]

### Recommandation retenue
[The recommended approach in 2-3 sentences]

### Justification
- [Reason 1]
- [Reason 2]
- [Reason 3]

### Risques et mitigations
- [Risk 1 → Mitigation]
- [Risk 2 → Mitigation]

### Plan d'implémentation
1. [Step 1]
2. [Step 2]
3. [Step 3]
```

### Step 4b: Implementation Scope Guard

Before implementing, estimate the scope of the recommended changes:

1. **Assess the scope:** count the estimated number of files to change, lines of code to add/modify, and whether new dependencies or infrastructure are needed
2. **Apply thresholds:**
   - **Small scope** (≤10 files, ≤500 lines, no new infrastructure): proceed to Step 5 normally
   - **Medium scope** (>10 files OR >500 lines): proceed but **scope down** to the most critical first step only. Add the remaining steps as a checklist in the MR/PR description under a `### Étapes restantes` section
   - **Large scope** (multi-service changes, architectural migration, new infrastructure required): **abort implementation**. Output the meeting analysis from Step 4, and suggest the user run the full `/meeting` skill for proper planning with validation before implementation
3. **If scoping down:** clearly state in the analysis what is being implemented now vs. deferred

### Step 5: Implement the Recommendation

**Immediately proceed to implementation without asking the user.** This is the key difference from meeting.

#### 5a: Protect the Working Tree

Before creating a branch, safeguard any existing work:

1. Run `git status` to check for uncommitted changes (staged, unstaged, or untracked)
2. **If the working tree is dirty:**
   - Run `git stash push -m "fast-meeting: auto-stash before <topic>"` to save the user's in-progress work
   - Remember the original branch name for later restoration
3. **If the working tree is clean:** proceed normally

#### 5b: Create Branch and Implement

1. **Create a new branch** from the current branch:
   - Branch name: `fast-meeting/<short-kebab-case-topic>` (e.g., `fast-meeting/jwt-auth-migration`)
   - Run: `git checkout -b fast-meeting/<topic>`
2. **Implement the changes** as described in the implementation plan from Step 4
   - Write code, modify files, add tests as needed
   - Follow the project's existing conventions and patterns
3. **Stage and commit** all changes:
   - Use a conventional commit message: `feat(<scope>): <description>`
   - Include `Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>` in the commit message

#### 5c: Run Tests

After committing, validate the implementation against the project's test suite:

1. **Auto-detect the test runner:**
   - Check `package.json` for `test`, `test:unit`, `test:e2e` scripts
   - Check for `Makefile`, `pytest.ini`, `phpunit.xml`, or other test config files
   - If no test runner is found, skip this step and note "No test suite detected" in the MR/PR description
2. **Run the tests** (scoped to affected files/modules if the test runner supports it, otherwise run the full suite)
3. **If tests pass:** proceed to push
4. **If tests fail:**
   - Analyze the failures and attempt **one fix cycle** (fix the code, re-run tests)
   - If tests pass after the fix: amend the commit with the fix and proceed
   - If tests still fail after one fix attempt:
     - Mark the MR/PR as **Draft** (prefix title with `Draft:`)
     - Add a `### Tests en échec` section in the MR/PR description listing the failing tests and error messages
     - Push anyway so the team can review
5. **Include test results summary** in the MR/PR description: number of tests run, passed, failed

#### 5d: Push and Restore

4. **Push the branch** to the remote:
   - Run: `git push -u origin fast-meeting/<topic>`
5. **Restore the user's working state:**
   - Run `git checkout <original-branch>` to return to the branch the user was on
   - If a stash was created in Step 5a, run `git stash pop` to restore the user's uncommitted work

### Step 6: Create the MR/PR

Based on the remote type detected in Step 1:

#### If GitLab:

Use `gitlab-mcp(create_merge_request)` to create a merge request with:
- **Title:** Short description (under 70 chars, in English)
- **Description:** The French meeting analysis and implementation summary (see template below)

#### If GitHub:

Use `gh pr create` to create a pull request with:
- **Title:** Short description (under 70 chars, in English)
- **Body:** The French meeting analysis and implementation summary (see template below)

#### MR/PR Description Template (French)

```markdown
## Analyse de réunion rapide

### Question posée
[La question de décision]

### Participants
| Persona | Rôle | Position |
|---------|------|----------|
| ... | ... | ... |

### Recommandation retenue
[L'approche recommandée]

**Justification :**
- [Raison 1]
- [Raison 2]
- [Raison 3]

### Risques identifiés
- [Risque 1 → Mitigation]
- [Risque 2 → Mitigation]

### Changements implémentés
- [Description des modifications fichier par fichier]

### Prochaines étapes
- [ ] Revue de code par l'équipe
- [ ] Validation des tests
- [ ] Merge après approbation

---
_Analyse et implémentation générées automatiquement par IA 🤖_
_Version : fast-meeting v1.0.0_
```

### Step 7: Post to Issue (If Applicable)

If the subject is linked to a GitLab or GitHub issue:

1. Post a comment on the issue linking to the MR/PR
2. Format: `Réunion rapide terminée. MR/PR créée : [link]. Voir la description de la MR/PR pour l'analyse complète.`
3. Use the appropriate tool:
   - **GitLab:** `gitlab-mcp(create_issue_note)`
   - **GitHub:** `gh issue comment`

## Meeting Quality Rules

### Persona Authenticity
- Each persona speaks consistently with their role and bias
- Personas use concrete examples, not abstract platitudes
- A security engineer talks about attack vectors, not vague "security concerns"
- A product owner talks about user impact and delivery timelines, not code patterns

### Speed Rules
- Maximum 3-4 personas per meeting
- Single round of parallel sub-agents + facilitator synthesis (no Round 2 debate)
- Optional devil's advocate sub-agent only when consensus is too high (adds ~10 seconds)
- No user confirmation before implementation
- Commit message and MR/PR are created automatically

### Implementation Quality
- Follow existing project conventions and patterns
- Write clean, tested code
- Run the project's test suite after implementation; attempt one fix cycle on failures
- Keep changes focused on the recommendation — do not over-engineer
- Scope guard: if changes exceed 10 files / 500 lines, scope down to the critical first step; if the scope is architectural, abort implementation and suggest `/meeting`
- Protect the user's working tree: stash uncommitted changes before branching, restore after push

## Examples

### Example 1: Technical Decision

```
User: fast-meeting : est-ce qu'on doit utiliser GraphQL ou REST pour la nouvelle API

→ Auto-selects: SOLID Alex (Backend), Pixel-Perfect Hugo (Frontend), Whiteboard Damien (Architect)
→ Runs fast meeting (1 round + synthesis)
→ Implements the recommended approach
→ Creates branch fast-meeting/graphql-vs-rest-api
→ Commits, pushes, creates MR/PR with French description
```

### Example 2: Bug Fix with Issue

```
User: fast-meeting sur l'issue #42 - les notifications ne s'affichent pas

→ Fetches issue #42 details
→ Auto-selects: Pixel-Perfect Hugo (Frontend), SOLID Alex (Backend), Edge-Case Nico (QA)
→ Runs fast meeting
→ Implements the fix
→ Creates MR/PR, posts link on issue #42
```

### Example 3: Refactoring

```
User: fast-meeting : refactorer le module d'authentification pour supporter OAuth2

→ Auto-selects: Paranoid Shug (Security), SOLID Alex (Backend), Whiteboard Damien (Architect), Pipeline Mo (DevOps)
→ Runs fast meeting
→ Implements the refactoring
→ Creates MR/PR with French analysis
```

## Important Notes

- **Never create new labels** on GitLab or GitHub. When adding labels to issues or merge requests, only use labels that already exist in the project. If unsure which labels exist, list them first (`gh label list` for GitHub, or check existing issue labels for GitLab) and pick from the available ones. If no suitable label exists, skip labeling rather than creating a new one.
- **This skill does NOT ask for user confirmation** — it runs the full pipeline autonomously
- If tests fail after one fix attempt, mark the MR/PR as **Draft** and document the failures
- If the implementation scope is too large (architectural, multi-service), abort and suggest `/meeting` instead
- The user's working tree is always protected: uncommitted changes are stashed before branching and restored after push
- The MR/PR description is always in French
- Branch names use the pattern `fast-meeting/<topic>`
- If the remote type cannot be determined, default to `gh pr create` (GitHub)
- Never force-push or modify existing branches — always create a new branch
