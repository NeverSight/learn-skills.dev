---
name: skill-comply
description: Measure whether agents actually follow a skill, rule, command, or agent definition by deriving expected behaviors, running representative scenarios, and comparing observed action timelines against the spec. Use after adding or changing instructions, before publishing skills, or when rules appear to be ignored.
metadata:
  version: "1.0.1"
  tags: "skills, evaluation, compliance, agents, quality"
---

# Skill Comply

Test whether an instruction artifact changes agent behavior in realistic
conditions. The goal is not to prove that the file is well-written; it is to
measure whether an agent follows it when the user prompt is supportive, neutral,
or competing.

## Contract

Inputs:

- Path to a `SKILL.md`, rule file, command, agent definition, or instruction doc
- Optional scenario list, trace logs, target harness, and pass threshold

Outputs:

- Expected behavior spec
- Scenario prompts by strictness level
- Compliance scores and failure categories
- Action timeline with matched, missing, reordered, or extra steps

Creates/Modifies:

- May create a local report file when requested
- Does not change the target skill or rule unless asked to fix findings

External Side Effects:

- May run local agent commands or tests when explicitly available
- No network calls or production writes by default

Confirmation Required:

- Before running costly model trials, modifying the target artifact, or writing reports outside the repo

Delegates To:

- `skill-creator` for frontmatter and instruction-quality guidance
- Optional repository-maintenance tools may validate a local catalog when
  available. Do not require unpublished meta-skills in an installed skill.
- `evaluation` for broader agent eval design

## When to Use

- A new skill, rule, command, or agent definition was added.
- An instruction was rewritten and behavior needs regression testing.
- The agent keeps ignoring a known rule.
- A maintainer wants a pass/fail signal before publishing an instruction pack.
- A rule works only when the user explicitly repeats it, but not in normal tasks.

## Core Idea

Compliance has three layers:

1. **Spec extraction**: convert the instruction artifact into observable steps.
2. **Scenario pressure**: test supportive, neutral, and competing prompts.
3. **Timeline matching**: compare observed actions to the expected sequence.

Measure behavior, not prose quality.

## Process

### 1. Derive the Expected Behavior

Read the target artifact and extract:

- trigger conditions
- required actions
- forbidden actions
- ordering constraints
- confirmation gates
- expected output shape
- side effects that must or must not happen

Represent the spec as a short table:

| Step | Required Behavior | Evidence Type | Required Order |
| --- | --- | --- | --- |
| 1 | Inspect existing examples before editing | search/read action | before write |
| 2 | Preserve unrelated user changes | diff/status check | before final |

### 2. Build Scenarios

Create three prompts:

- **Supportive**: explicitly asks for the workflow.
- **Neutral**: asks for the task but does not mention the instruction.
- **Competing**: adds pressure that often causes skipping, such as urgency,
  ambiguity, or a tempting shortcut.

For destructive or side-effecting skills, use dry-run scenarios against fixture
files or synthetic repos. Do not create real external side effects for a
compliance test.

### 3. Execute or Simulate

Use the strongest safe evidence available:

- actual tool/action trace from a sandbox run
- local command logs
- saved transcript
- reviewer reconstruction from a completed session
- dry-run plan when execution is not safe

Do not count a step as compliant because the final answer claims it happened.
Require an action trace, command output, file diff, or visible artifact.

### 4. Grade the Timeline

Classify each expected behavior:

| Result | Meaning |
| --- | --- |
| Matched | Required behavior happened with adequate evidence |
| Missing | Required behavior did not happen |
| Reordered | Behavior happened, but too late to matter |
| Weak | Behavior happened superficially or without enough evidence |
| Violated | A forbidden action happened |

Compute a simple score:

```text
score = matched / required
critical violation = automatic fail
```

Use judgment for ordering and gates. A late safety check after writing code
does not satisfy a pre-edit investigation requirement.

## Failure Categories

- **Trigger failure**: the skill or rule did not activate in neutral wording.
- **Ordering failure**: the right action happened after the risky action.
- **Evidence failure**: the agent claimed compliance without observable proof.
- **Scope failure**: the agent followed the rule for one file but not the full surface.
- **Conflict failure**: another instruction overrode the rule.
- **Overhead failure**: the rule caused excessive work for low-risk tasks.

## Output Format

```markdown
Compliance result: 2/3 scenarios passed. Neutral prompt failed because the agent edited before checking existing patterns.

| Scenario | Score | Verdict | Main Failure |
| --- | --- | --- | --- |
| Supportive | 5/5 | Pass | - |
| Neutral | 3/5 | Fail | Missing pre-edit example search |
| Competing | 4/5 | Pass | Weak final evidence |

## Timeline Findings

- Missing: [step] [evidence]
- Reordered: [step] [why order matters]

## Recommended Fix

1. Tighten the trigger phrase in `description`.
2. Move the precondition into the Contract.
3. Add a short output checklist.
```

## Promotion Guidance

When a step repeatedly fails:

- Make the trigger clearer if the skill is not selected.
- Move mandatory behavior into the Contract if it is buried in prose.
- Split the skill if it has multiple unrelated workflows.
- Convert fragile mandatory behavior into a hook, script, or command only when
  the current platform can actually enforce it.
- Add examples only when the failure is ambiguity, not lack of enforcement.

## Anti-Patterns

- Testing only prompts that name the skill.
- Treating final-answer claims as proof.
- Running live destructive actions to test a safety rule.
- Using a single scenario to certify a broad workflow.
- Fixing compliance by adding long repetitive wording instead of clarifying the
  trigger, contract, or gate.
