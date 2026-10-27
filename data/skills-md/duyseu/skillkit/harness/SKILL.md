---
name: harness
description: "Design a harness tailored to the project, and create specialized agents and the skills each agent will use. Use when the user asks 'set up a harness', 'build a harness', 'design a harness', 'harness engineering', or 'create an agent team'. Also use when building an automation system for a new domain or project, or when reconfiguring or extending an existing harness. Also use for requests to operate or maintain an existing harness, such as 'check the harness', 'audit the harness', 'harness status', or 'sync agents/skills'. To retrospect on execution results and apply feedback, use the harness:evolve skill."
---

# Harness v2 - Designing agent teams and skills

Design a harness tailored to the project. Define the role of each agent, and create the skills the agents follow when they work.

## Core principles

1. Create agent definitions in `project/.claude/agents/` and skills in `project/.claude/skills/`. An agent records who does the work; a skill records how that work is done.
2. Choose the execution mode according to the task flow. If the order and repeat conditions can be fixed in code, use workflow orchestration. If you need to exchange feedback with the same specialist, use a persistent agent. If you only need to receive a result once, delegate the task to a subagent. Step 2 covers the selection criteria in detail.
3. Choose the model according to the task's complexity, duration, autonomy, and response speed. Use fable for the hardest tasks that must plan and run autonomously over a long period, opus for design, code generation, complex analysis, and cross-verification, and sonnet for everyday tasks such as log analysis, format conversion, and simple collection. Step 3 covers the detailed criteria.
4. So that a new session can also load the orchestrator skill, record only the trigger conditions and the change history in `CLAUDE.md`.
5. Keep reflecting what you learn from execution results into the agents, skills, and `CLAUDE.md`. The `harness:evolve` skill handles retrospectives and finding the changes to make.
6. Write the agent definitions, skills, orchestrator, and `CLAUDE.md` records you generate in the language the user uses in the conversation. Do not write deliverables in English just because this skill document and the templates in `references/` are written in English. Translate the template headings and example phrases into that language as well. If the user specifies a language, follow it; if they do not and you are extending an existing harness, follow the language of the existing files.

## Procedure

### Step 0: Check the current state

When the harness skill is loaded, first check the existing setup.

1. Read `project/.claude/agents/`, `project/.claude/skills/`, and `project/CLAUDE.md`.
2. Choose the procedure to follow according to the current state.
   - **New build**: If the agent or skill directories do not exist or are empty, run everything from Step 1.
   - **Extend an existing setup**: If you need to add agents or skills to an existing harness, run only the steps you need from the table below.
   - **Operation and maintenance**: If you need to check, modify, or sync an existing harness, go to the operation procedure in Step 7.

   | Change | Step 1 | Step 2 | Step 3 | Step 4 | Step 5 | Step 6 |
   | --- | --- | --- | --- | --- | --- | --- |
   | Add an agent | Skip and use the Step 0 result | Decide only which team and step it goes in, under which execution mode | Required | When a dedicated skill is needed | Modify the orchestrator | Required |
   | Add or modify a skill | Skip | Skip | Skip | Required | When the connections change | Required |
   | Change the structure or execution mode | Skip | Required | Only the affected agents | Only the affected skills | Required | Required |

3. If an existing orchestrator contains `TeamCreate`, `TeamDelete`, or `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`, it is a v1 deliverable. It does not work in the current execution environment, so propose moving it to v2. For the detailed method, follow "Switching from v1 to v2" in `references/execution-modes.md`.
4. Compare the actual agent and skill lists with the `CLAUDE.md` records to find mismatches.
5. Tell the user the check results and the execution plan, and get their confirmation.

### Step 1: Analyze the domain and tasks

1. Identify the project's domain and goal from the user's request.
2. Divide the required work into types such as generation, verification, editing, and analysis.
3. Check the task flow so you can choose an execution mode.
   - Can the list of items to process be enumerated in advance? Example: moving N files or reviewing M perspectives
   - Is a repeated procedure needed to verify a deliverable and fix it again?
   - Do the agents need to exchange opinions for the result to improve?
   - Do you need to keep talking with the same specialist within one session?
4. Find the parts that overlap or conflict with the existing agents and skills identified in Step 0.
5. Examine the codebase to understand the tech stack, data model, and main modules.
6. Match the difficulty of your explanations to the terms the user uses and the level of their questions. Do not use terms such as assertion and JSON Schema without explanation for users with little coding experience.

### Step 2: Design the execution mode and team structure

#### 2-1. Choose the execution mode

Harness v2 uses three multi-agent features of Claude Code. Choose one of the following modes to match the task flow.

| Execution mode | Features used | Suitable tasks |
| --- | --- | --- |
| **Workflow orchestration** | `agent()`, `pipeline()`, `parallel()`, `phase()` of a `Workflow` script | Tasks where the processing list, verification procedure, and repeat count can be fixed in code. Tasks that need results conforming to a schema or that must call `Agent` dozens of times or more |
| **Persistent agent collaboration** | `Agent(name:)`, `SendMessage`, `TaskCreate`, `TaskUpdate` | Tasks where named specialists must repeat feedback, negotiation, and joint editing while keeping the conversation context |
| **Subagent delegation** | A single `Agent` call. Runs in the background by default and can be called in parallel | Tasks where the agents do not need to talk to each other and you only need to receive the result once |

Decide in this order.

1. If the processing list, verification criteria, and repeat conditions can be expressed in code in advance, use a workflow. A fixed flow must not be left to the model's judgment of the moment, so that it can be run again the same way.
2. If it is hard to fix in code and the agents must talk to each other or remember earlier context, use persistent agents.
3. If neither condition applies and you only need the result, delegate to a subagent.
4. If the nature of the task differs from step to step, compose a mixed mode. Write the execution mode of each step in the orchestrator.

To use the `Workflow` tool, the user must explicitly consent. Treat it as consent when the user directly asks to run a workflow, or when the user has loaded an orchestrator skill that instructs a `Workflow` call. Limit the default run to a few agents, and scale up only when the user asks for broad investigation with words such as "thoroughly" or "exhaustively".

> For the comparison of execution modes, the concurrency cap, schemas, token budget, and resume conditions, see `references/execution-modes.md`.

#### 2-2. Choose the team composition

1. Divide the work by area of expertise.
2. Choose the composition that fits the task from the six approaches below. Detailed criteria are in `references/team-patterns.md`.
   - **Pipeline**: Receive the result of the previous step and process in order. Suits `pipeline()`.
   - **Fan-out/fan-in**: Process independent tasks in parallel, then merge the results. Use `pipeline()`, and `parallel()` only when needed.
   - **Expert pool**: Call only the specialists that match the input. Suits subagents or persistent agents.
   - **Generate and verify**: One agent produces and another reviews. Use the adversarial verification of a workflow or a pair of persistent agents.
   - **Supervisor**: A central agent watches progress and reassigns work. Use persistent agents and a shared task list.
   - **Hierarchical delegation**: A higher-level agent delegates again to lower-level agents. Use only within two levels, and limit workflow nesting to one level.
3. If the accuracy of the deliverable matters, combine the following verification methods.
   - **Adversarial verification**: Attach N adversarial verification agents to each item found, and pass only the items that a majority judge `confirmed` as sufficiently supported. A `refuted` or `uncertain` verdict does not count as a pass.
   - **Jury panel**: Create N drafts separately, judge them in parallel, and build the final version based on the best draft.
   - **Repeat until no new items (Loop-until-dry)**: Keep exploring until the number of newly found items is 0 for K consecutive rounds.
   - **Explore by multiple criteria**: Investigate in parallel by different criteria such as container, content, entity, and time.
   - **Omission reviewer**: Have the last agent look only for what is missing.

#### 2-3. Criteria for splitting agents

Split agents by the expertise required, whether parallel processing is possible, the conversation context that must be kept, and the likelihood of reuse. For the detailed table, see "Criteria for splitting agents" in `references/team-patterns.md`.

### Step 3: Write the agent definitions

Define specialist agents to be reused across multiple sessions as `project/.claude/agents/{name}.md` files. Do not put a role you will use repeatedly directly into the `prompt` of the `Agent` tool only.

- Define it as a file so that it can be reused in the next session as well. Call it with `subagent_type: "{name}"` in the `Agent` tool and `agentType: "{name}"` in `Workflow`.
- Fix in advance what the agents will exchange, so that the collaboration results are stable.
- Record who does the work in the agent and how that work is done in the skill, so the two do not get mixed up.

Create a reusable specialist role as a custom type in a file, and when calling it, specify that file's name in `subagent_type` or `agentType`. Do not create a separate definition file for a one-off task that uses a built-in type such as `general-purpose`, `Explore`, or `Plan` as is.

#### Check for overlap with existing agents

Before creating a new agent file, check whether its role overlaps with the existing agents in `project/.claude/agents/`. Do not skip this check even when you skip Step 1 and only add an agent. This is because building or extending a harness several times can pile up agents with the same role under different names. If they overlap, do not create a new name; use or extend the existing agent as is. For the criteria and the exception (when a domain is deliberately specialized), see "Agent reuse design" in `references/team-patterns.md`.

#### Model selection criteria

Choose a model for each agent based on the task's complexity, duration, autonomy, and response speed. Specify it in the `model:` of the YAML frontmatter (header) or in the call argument `model` or `opts.model`, and leave the reason for the choice as a comment in the agent definition or the orchestrator.

| Model | Selection criteria | Typical tasks |
| --- | --- | --- |
| **fable** | The hardest tasks that must plan on their own, connect multiple steps, and run autonomously over a long period | Agent coordination, planning and long-running execution, integrating vast material, concretizing vague ideas |
| **opus** | Specialist tasks with a clear scope that need deep reasoning and analysis | Design and architecture, code generation, complex analysis, cross-verification, critique of research methods, creative work |
| **sonnet** | Everyday tasks with a clear procedure where fast processing matters | Log analysis, format conversion, static file inspection, running deployment scripts, simple collection, general writing and summarization |

- If the task must adjust its next plan to the result of the previous step and run autonomously over a long period, use fable. If it analyzes one problem of a fixed scope in depth, use opus. For example, opus suits a task that critiques a single paper in depth, while fable suits a task that reviews dozens of papers and goes on to produce a strategy and a report.
- For general tasks where the judgment is unclear, use sonnet as the default.
- Do not assign fable or opus to every agent just because the agent is important. Choose the model by the actual nature of the task, not by the agent's standing.
- Even if you used fable for a higher-level agent in charge of planning and coordination, choose models for the lower-level workers separately to match each task.

> For the detailed criteria by model, see `references/model-selection-guide.md`.

#### What to put in the definition file

Always include `name` and `description` in the YAML frontmatter. If needed, add `tools` to restrict the tools used and `model` to change the model. In the `tools` of a read-only review or analysis agent, leave out Edit and Write so that it cannot change files.

Conversely, give an agent that fixes deliverables Edit along with Write. Without Edit, even a one-line fix requires rewriting the whole file, so when the deliverable is large the agent gives up on fixing and works around it. Also, there have been cases where a tool listed in `tools` was not provided at run time, so have persistent agents report the list of tools they can actually use in their first report.

Always write the core role, working principles, input and output rules, error handling, and collaboration method in the body. For persistent agents, add `## Communication rules` to set who they exchange `SendMessage` with and how to use the shared task list.

> For the definition template, full examples, and what to watch for when restricting `tools`, see "Agent definition structure" in `references/team-patterns.md`.

#### When adding a QA agent

- For a QA agent, specify a type that can use every verification tool. `Explore` is read-only, so it cannot run verification scripts.
- Do not only check whether files exist. Compare the response structure of the API with that of the frontend hooks.
- Do not inspect only once after the whole task is finished. Inspect right away each time a module is completed.
- For the detailed method, follow `references/qa-agent-guide.md`.

### Step 4: Write the skills

Create the skill each agent will follow in `project/.claude/skills/{name}/SKILL.md`. For the detailed writing method, follow `references/skill-writing-guide.md`.

#### 4-0. Check for overlap with existing skills

Before creating a new skill, check whether its function overlaps with the existing skills in `project/.claude/skills/`. If they overlap, do not create a new name; connect the existing skill to the agent or extend it. For the criteria, the exception (when a domain is deliberately specialized), and how far to generalize, see "Skill reuse design" in `references/skill-writing-guide.md`.

#### 4-1. Directory structure

```
skill-name/
├── SKILL.md              # required
│   ├── YAML frontmatter  # name and description required
│   └── Markdown body
├── scripts/              # optional: executable code for tasks that repeat or must always give the same result
├── references/           # optional: reference documents read only when needed
└── assets/               # optional: files used in deliverables, such as templates and images
```

#### 4-2. Write the trigger conditions in the description

Claude looks at a skill's `name` and `description` to decide which skill to load. In the `description`, state concretely what the skill does and the situations in which it must be used, and also distinguish cases that look similar but must not use it.

**Bad example:** `"A skill that handles PDF documents"`

**Good example:** `"Performs PDF tasks such as reading PDF files, extracting text and tables, merging, splitting, rotating, watermarking, encrypting, and OCR. Always use it when the user mentions a .pdf file or asks for a PDF deliverable."`

#### 4-3. Principles for writing the body

| Principle | How to apply it |
| --- | --- |
| **Explain the reason first** | Do not just list `ALWAYS` and `NEVER`; state why the rule is needed. Knowing the reason lets you judge correctly even in exceptional situations. |
| **Write concisely** | Keep `SKILL.md` under 500 lines. Delete content that does not help judgment, or move it to `references/`. |
| **Generalize into principles** | Do not create rules that fit only a specific example. Write decision criteria that apply to many inputs. |
| **Put repeated code in ahead of time** | If several agents rewrite the same script during testing, put it in `scripts/`. |
| **Write as instructions** | Choose one sentence-ending style that suits the document, either the plain declarative (-handa) or the imperative (-hara), and use it throughout. The action to take must be clear. |

#### 4-4. Load only the information you need, step by step

A skill loads the information and executable code it needs at the following times.

| Information | When it is loaded | Recommended size |
| --- | --- | --- |
| **Metadata** (`name`, `description`) | Always | About 100 words |
| **`SKILL.md` body** | When the skill is loaded | Under 500 lines |
| **`references/`** | When that material is needed | No limit |
| **`scripts/`** | When running a repeated task or a task that must always give the same result | No limit. Can be run directly without reading the contents |

- When `SKILL.md` approaches 500 lines, move the details to `references/` and write in the body when to read which file.
- If a reference document exceeds 300 lines, put a table of contents at the top of the document.
- If the guidance differs by domain or framework, split the reference documents so that only the needed file is read.

#### 4-5. Connect agents and skills

- One agent can use one or more skills.
- Several agents can share the same skill.
- Record the way of working in the skill and the role that takes on that work in the agent.

### Step 5: Integrate and set the execution order

The orchestrator is also a skill. It ties the individual agents and skills into a single task flow and decides who collaborates, when, and in what order. The full template for each mode is in `references/orchestrator-template.md`, and workflow script examples are in `references/workflow-recipes.md`.

When extending an existing harness, edit the existing file instead of creating a new orchestrator. When you add an agent, reflect it in the composition, the task assignment, and the data-passing order, and put the new trigger conditions in the `description` as well.

#### 5-0. Orchestrator by execution mode

**A. Workflow orchestration**

Define a `Workflow` script in the orchestrator skill. The script consists of `meta`, `phase()`, `pipeline()`, `parallel()`, and `agent()`. Specify a custom type with `agentType`, and receive schema-conforming results with `schema`.

```
[Orchestrator skill] → Workflow(script)
    ├── phase('Collect'): pipeline(items, ...)   ← process a predefined list in a distributed way
    ├── phase('Verify'): adversarial verification or jury panel
    └── return structured results → main writes the synthesis report
```

**B. Persistent agent collaboration**

After launching named agents, coordinate with the shared task list and `SendMessage`. `TeamCreate` and `TeamDelete` no longer exist. No explicit team object is created, and agents launched by name in a session belong to one automatically composed collaboration group. You can send a message again to such an agent while it keeps the earlier conversation context.

```
[Main agent (leader)]
    ├── Agent(name: "researcher", ...) / Agent(name: "critic", ...)  ← run in parallel
    ├── TaskCreate(tasks + dependencies)
    ├── SendMessage({to: "critic"}, "Review the researcher's draft")
    └── Collect and synthesize results
```

**C. Subagent delegation**

Call the `Agent` tool N times in parallel in a single message and gather the results from the completion notifications. The agents you call run in the background by default.

If the nature of the task differs from step to step, you can compose a mixed mode. For example, gather material with a workflow and then have persistent agents reach agreement and integrate it, or adversarially verify with a workflow the result produced by persistent agents. Write `**Execution mode:**` above each step.

#### 5-1. How to pass data

| Method | Implementation | Suitable execution mode | When to use |
| --- | --- | --- | --- |
| **Structured return value** | `agent(prompt, {schema})` of `Workflow` returns validated JSON | Workflow orchestration | When the next step must process the result in code |
| **Plain return value** | The return message of the `Agent` tool | Subagent | When the main agent gathers the summary results directly |
| **Message** | Pass directly between agents with `SendMessage` | Persistent agent | When real-time coordination and feedback are needed |
| **Shared task list** | Share state with `TaskCreate`, `TaskUpdate` | Persistent agent | When managing progress, dependencies, and dynamic assignment |
| **File** | Write to and read from a predetermined path | All modes | When the data is large or you need to check the work process later |

When passing through files, follow these rules.

- Save intermediate deliverables in `_workspace/` under the working directory.
- Use the `{phase}_{agent}_{artifact}.{ext}` format for file names. Example: `01_analyst_requirements.md`
- Save only the final deliverable at the path the user specified. Keep `_workspace/` for after-the-fact verification.

#### 5-2. Error handling

Put an error handling policy in the orchestrator.

- Retry once, and if it fails again, proceed without that result, but state the omission in the final report. Do not delete conflicting data; keep it together with its source.
- However, do not retry failures whose result would be the same on retry, such as exhausted usage limits, expired authentication, or denied permissions. Retrying only uses up the remaining limit. Open the partial deliverables yourself to confirm how far the work actually got, record the missing content in a file, and report to the user. For a usage limit, also tell them when the limit resets.
- When the orchestrator fills in the gaps left by a stalled agent, reflect on its behalf only the facts it has checked directly. Do not guess and fill in the agent's judgments (for example, why a certain source was excluded). Filling them in by guesswork amounts to forging the record used for after-the-fact verification.
- In a workflow, an `agent()` that fails or is skipped returns `null`, and `parallel()` does not throw failures as exceptions. Apply `.filter(Boolean)` to the result array and report the number of missing items with `log()`.
- If a persistent agent does not respond, check its status with `SendMessage` and instruct it again. If that still fails, launch the same custom type under a new name and pass the necessary task context in the prompt.

> For how to respond by error type, see "Error handling" in the template for the relevant execution mode in `references/orchestrator-template.md`.

#### 5-3. Task scale

| Task scale | Number of persistent agents | `Agent` call scale in a workflow |
| --- | --- | --- |
| Small: fewer than 10 tasks | 2-3 agents | 2-5 calls |
| Medium: 10-20 tasks | 3-5 agents | About 10 calls. Automatically queued beyond the concurrency cap |
| Large: more than 20 tasks | Supervisor + 3-5 workers | Dozens to hundreds of calls. Overall cap of 1,000 calls |

- The more agents there are, the more the management cost grows. Keep the default scale small.
- If the user specifies a token budget such as `+500k`, check `budget.remaining()` in the workflow script and adjust the scale of the run.

#### 5-4. Record the harness connection info in `CLAUDE.md`

When the setup is finished, record in the project's `CLAUDE.md` that the harness exists and its trigger conditions. `CLAUDE.md` is read in every new session, so do not repeat detailed execution rules in it.

````markdown
## Harness: {domain name}

**Goal:** {one line with the harness's core goal}

**Trigger conditions:** When asked for work related to {domain}, use the `{orchestrator-skill-name}` skill. Simple questions may be answered directly.

**Change history:**
| Date | Change | Target | Reason |
| --- | --- | --- | --- |
| {YYYY-MM-DD} | Initial setup with Harness v2 | All | - |
````

Do not put in the agent and skill lists, the directory structure, or detailed execution rules. This information is managed in the orchestrator skill, `.claude/agents/`, and `.claude/skills/`. Keep only the trigger conditions and the change history in `CLAUDE.md`.

#### 5-5. Handle follow-up requests

The orchestrator must work not only on the first run but also when the results are revised.

1. Put expressions such as `run again`, `re-run`, `update`, `modify`, `supplement`, `re-run only {part} of {domain}`, `based on previous results`, and `improve results` in the `description`.
2. In the orchestrator's Step 0, check the existing work context.
   - If `_workspace/` exists and the request is to fix only part of it, re-run only that step or agent.
   - If `_workspace/` exists and new input has arrived, move the existing directory to a timestamped directory and run fresh.
   - If `_workspace/` does not exist, run from the beginning.
   - If the workflow has a previous `runId`, you can resume with `resumeFromRunId`. Unchanged `agent()` calls use the cached results.
3. Write how to re-invoke in the agent definition. If there is a previous result file, read it, and if there is user feedback, fix only the relevant part.

### Step 6: Verification and testing

Verify the harness you created. For the detailed method, follow `references/skill-testing-guide.md`.

#### 6-1. Verify files and references

- Check that every agent file is in the right place.
- Check that the skill's YAML frontmatter has `name` and `description`.
- Check that the names the agents use to refer to each other match.
- Check that no command files were created in `.claude/commands/`.
- Check that no v1-style `TeamCreate`, `TeamDelete`, `team_name`, or experimental feature flags remain in the deliverables.

#### 6-2. Verify by execution mode

- **Workflow orchestration**: Check that `meta` is a literal containing only values, that `Date.now()` and `Math.random()` are not used, that `parallel()` is used only when you must wait for all results, that `.filter(Boolean)` is not missing, and that the `phase()` titles match `meta.phases`.
- **Persistent agent collaboration**: Check the sender and receiver paths of `SendMessage`, the task dependencies, and the number of agents.
- **Subagent delegation**: Check that each agent's input and output connect, that parallel calls are bundled into a single message, and that results are gathered without omission.
- **Mixed mode**: Check that the execution mode is written for each step and that data does not break when the step changes.

#### 6-3. Skill execution tests

1. For each skill, create 2-3 concrete test requests that a real user would likely enter.
2. Run With-skill runs and Baseline runs in parallel to compare how much the skill improves the results. If it must be repeated, the A/B comparison itself can be made into a workflow.
3. Use qualitative evaluation, where the user reviews directly, together with quantitative evaluation using assertions. If you cannot create objective conditions, follow the user's judgment.
4. When a problem appears, do not add a rule that blocks only that specific example; fix it with a principle that applies to many situations. Test again, and repeat until further fixes give almost no benefit.
5. If several agents repeatedly produce the same code, put it in `scripts/`.

#### 6-4. Verify the trigger conditions

1. Create 10 requests that must load the skill, varying the tone and how explicit they are.
2. Also create 10 boundary cases whose wording is similar but that should use a different skill or tool.

Clearly unrelated requests do not test the boundary. For example, when testing an image generation skill, `extract the charts in this Excel file as PNG` is a better boundary case than `write a Fibonacci function`. The result is an image, but a spreadsheet tool actually suits it better. Also check whether the trigger conditions overlap with those of existing skills.

#### 6-5. Dry run

- Check that the order of the orchestrator's steps is logical.
- Check that the data-passing path does not break in the middle.
- Check that every agent's input matches the output of the previous step.
- Check that the fallback procedure can actually be run when an error occurs.

#### 6-6. Record test scenarios

Create `## Test scenarios` in the orchestrator skill and write at least one normal flow and one error flow.

### Step 7: Operation, maintenance, and improvement

A harness is not a deliverable that is finished once it is made.

The `harness:evolve` skill handles retrospectives on execution results and applying feedback. When the user asks `harness retrospective`, `harness evolution`, or `apply the feedback`, use `harness:evolve`. This skill analyzes the difference between the initial setup and the current state, organizes the feedback so that it applies to many situations, and reflects it in the agents, skills, and orchestrator. It also updates the `CLAUDE.md` change history.

This `harness` skill directly handles the following procedure for operating and maintaining an existing harness.

1. **Check the current state**: Compare the `.claude/agents/`, `.claude/skills/`, and orchestrator composition to make a list of mismatches, and tell the user.
2. **Add and modify little by little**: Change only one item at a time and run the next verification right away.
3. **Record the change history**: Write the date, change, target, and reason in `CLAUDE.md`.
4. **Verify the change**: Check the file structure. If it affects the trigger conditions, also run a trigger test. If the change is large, do the execution test and dry run as well, then finally check that `CLAUDE.md` matches the actual files.

In the following situations, propose improving with `harness:evolve`.

- The same kind of feedback has come up two or more times.
- An agent keeps failing for the same cause.
- The user keeps handling the same task manually without going through the orchestrator.

## Deliverables checklist

- [ ] You created files in `project/.claude/agents/` for every custom type to be reused. One-off tasks that use a built-in type as is are excluded.
- [ ] You created the needed `SKILL.md` files and reference documents in `project/.claude/skills/`.
- [ ] One orchestrator skill contains the data-passing method, error handling, and test scenarios.
- [ ] You wrote down the execution mode to be used among workflow orchestration, persistent agents, and subagents. For a mixed mode, you marked it for each step.
- [ ] You chose each agent's `model:` according to complexity, duration, autonomy, and response speed, and left the reason as a comment. You did not assign the same high-performance model to every agent across the board.
- [ ] No v1-style items such as `TeamCreate`, `TeamDelete`, or experimental feature flags remain in the deliverables.
- [ ] You put `.filter(Boolean)` in the workflow script and used only literals in `meta`. Wait for all results with `parallel()` only when truly needed.
- [ ] You did not create files in `.claude/commands/`.
- [ ] Before creating new agents and skills, you checked whether their roles overlap with existing ones. Unless a domain was deliberately specialized, you used or extended the existing one where they overlapped, and no names or roles conflict.
- [ ] You wrote the agent definitions, skills, orchestrator, and `CLAUDE.md` records in the language the user uses in the conversation. If the user specified a language or the existing harness files have one, you followed that language.
- [ ] The skill `description` states concretely what to do and the trigger conditions, and also includes follow-up request expressions.
- [ ] The `SKILL.md` body is under 500 lines. If it is 500 lines or more, you moved the details to `references/`.
- [ ] You ran it with 2-3 test sentences similar to real requests.
- [ ] You verified the trigger conditions with requests that must load the skill and boundary cases that must not.
- [ ] You recorded only the trigger conditions and the change history in `CLAUDE.md`.
- [ ] The orchestrator's Step 0 distinguishes a first run, a follow-up run, and a partial re-run. For workflows it also covers the resume option.

## Reference documents

- **Execution mode details**: `references/execution-modes.md`
- **Model selection guide**: `references/model-selection-guide.md`
- **Team composition approaches and agent definitions**: `references/team-patterns.md`
- **Real-world team composition examples**: `references/team-examples.md`
- **Workflow script examples and cautions**: `references/workflow-recipes.md`
- **Orchestrator template**: `references/orchestrator-template.md`
- **Skill writing guide**: `references/skill-writing-guide.md`
- **Skill testing guide**: `references/skill-testing-guide.md`
- **QA agent guide**: `references/qa-agent-guide.md`
