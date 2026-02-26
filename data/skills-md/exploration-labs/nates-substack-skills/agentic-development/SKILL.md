---
name: agentic-development
description: Conversational guidance for building software with AI agents, covering workflows, tool selection, prompt strategies, parallel agent management, and best practices based on real-world high-volume agentic development experience. Use this skill when users ask about setting up agentic workflows, choosing models, optimizing prompts, managing parallel agents, or improving agent output quality.
---

# Agentic Development

This skill provides guidance for building software with AI agents based on real-world experience from high-volume agentic development, specifically Peter Steinberger's "Just Talk To It" methodology developed while building a ~300k LOC TypeScript React application entirely with AI agents.

**Core Philosophy**: Most elaborate frameworks, planning systems, and tooling are premature optimization. Treat AI agents like capable engineers—talk naturally, develop shared context, interrupt when needed, and iterate based on results rather than elaborate plans.

## When to Use This Skill

Apply this skill when users ask about:
- Setting up agentic development workflows
- Choosing tools and models for AI-assisted coding
- Optimizing prompt strategies and context management
- Parallel agent workflows and git management
- Debugging agent behavior or improving output quality
- Evaluating whether to use MCPs, subagents, or other abstractions
- Refactoring strategies with agents
- Testing approaches with AI assistance

## Core Principles

### 1. Think in Blast Radius, Not Complexity

Plan changes by file impact rather than perceived difficulty.

**Application**:
- Before starting, estimate: "Will this touch 3 files or 30?"
- Recognize that multiple large-radius changes prevent isolated commits and complicate recovery
- When an agent takes longer than anticipated, interrupt (escape key) and ask "what's the status?"
- Use "give me a few options before making changes" when uncertain about impact
- Trust that file changes are atomic—agents resume well after interruption

**Guidance Pattern**: When a user describes a task, help gauge blast radius by asking: "How many files do you think this will touch?" This builds intuition for redirecting agents.

### 2. Model Selection and Economics

**Subscription Economics**: Running 4-5 AI subscriptions (~$1k/month) provides effectively unlimited tokens versus per-API-call pricing that costs 5-10x more. This enables context-wasteful usage and multiple parallel agents.

**Model Characteristics**:
- **GPT-5-Codex**: Reads extensively before acting, requires shorter prompts (1-2 sentences often suffice), more cautious with pushback on questionable requests, introverted communication style
- **Claude Sonnet**: More eager to start, requires more explicit direction, verbose communication ("absolutely right", "100% production ready")

**Guidance Pattern**: When advising on model choice, emphasize that model personality affects mental health and productivity. The difference between aggressive optimism (while tests fail) versus quiet progress-making materially impacts burnout.

### 3. Parallel Agents in One Folder

Run 3-8 agents simultaneously in the same directory with one dev server, rather than git worktrees or branch-per-feature.

**Advantages**:
- Test multiple changes at once in running application
- Faster than spawning multiple dev servers or switching branches
- Agents perform atomic commits themselves
- Trade some isolation for velocity gains

**Requirements**:
- Agents must commit only their own changes (requires clear instruction file)
- Single shared dev server for testing
- Accept some git history messiness (clean in batches later)

**Guidance Pattern**: When users struggle with worktrees or branch management, suggest trying parallel agents in one folder for a week. Initial skepticism often gives way to appreciation.

### 4. Screenshots Are 50% of Context Engineering

Drag screenshots into terminal (showing UI, code, or errors) rather than writing lengthy text descriptions.

**Effectiveness**:
- Models excel at visual context
- Find exact strings, match patterns, jump to correct locations
- Takes 2 seconds versus minutes of detailed typing
- More token-efficient than text explanations

**Guidance Pattern**: If a user writes long descriptions of what they see, interrupt and suggest: "Just screenshot it and drag into the terminal."

### 5. Better Models Need Shorter Prompts

More capable models require less prompt verbosity because they compensate through better reconnaissance.

**GPT-5-Codex Pattern**:
- 1-2 sentences often suffice
- Reads extensively before acting
- Strong world knowledge reduces explanation needs

**Claude Pattern**:
- Benefits from more extensive context
- Better comprehension with additional detail
- Requires more explicit direction

**Guidance Pattern**: If a user writes elaborate prompts for GPT-5, suggest trying shorter versions. The model's file-reading behavior often makes detailed specs unnecessary.

### 6. Context Tax Is Real—CLIs Beat MCPs

MCPs consume context tokens on every interaction, creating permanent overhead.

**CLI Advantages**:
- Shows help menu on first incorrect invocation
- Model learns forever without recurring cost
- Example: GitHub MCP costs ~23k tokens; `gh` CLI costs zero
- Models possess strong world knowledge of popular CLIs

**Exception**: Chrome DevTools MCP for closing debugging loops justifies context cost in specific scenarios.

**Guidance Pattern**: When users discuss building an MCP, challenge: "Could this be a CLI instead?" Most tools should be CLIs unless deep integration justifies the context tax.

### 7. Interrupting Agents Is Standard Practice

Break the assumption inherited from traditional programming that tasks must run to completion.

**Practice**:
- Hit escape mid-task and ask "what's the status?"
- Models resume where they stopped
- File changes are atomic
- Enables active steering and course correction

**Guidance Pattern**: When users hesitate about interrupting, reassure: "Think of it like checking in with a junior engineer. They'll pick up where they left off."

### 8. Refactoring Is Low-Focus Work

Spend ~20% of time on agent-driven refactoring when tired or needing less focus.

**Paradigm Shift**: Traditional views require peak concentration for refactoring. With agents, it becomes mechanical work requiring only strategic oversight.

**Refactoring Tasks**:
- Code deduplication (jscpd)
- Dead code removal (knip)
- ESLint plugins (react-compiler, deprecation)
- Adding tests and comments for tricky parts
- Dependency updates and tool upgrades
- File restructuring
- Rewriting slow tests
- Modernizing patterns (e.g., removing unnecessary `useEffect`)

**Guidance Pattern**: When users feel burned out on feature work, suggest: "Try a refactoring day. Queue cleanup tasks and let agents handle mechanical work while maintaining high-level oversight."

### 9. Same-Context Testing Catches Fresh Bugs

After implementing features, request tests in the same context.

**Effectiveness**:
- Agent has full context of what it just built
- Often discovers bugs in its own implementation
- Far more effective than separate test-writing sessions
- Tests reflect actual implementation details

**Exception**: Purely UI tweaks may not warrant immediate testing.

**Guidance Pattern**: Establish this habit: "After each feature or fix, ask the model to write tests. Use the same context." While AI generally writes mediocre tests, this approach helps catch its own bugs.

### 10. Plan Mode Is Workaround Theater

Elaborate planning frameworks, spec-driven development, and multi-agent orchestration often work around model weaknesses rather than embracing strengths.

**Better Approach with Strong Models**:
- Use "let's discuss" or "give me options"
- Model will wait for approval
- No harness ceremony needed

**Spec-Driven Alternative**: For complex features, discuss with the agent, iterate on ideas, optionally request a spec, get review from another model (GPT-5-Pro), then paste useful parts back.

**UI Work Approach**: Deliberately under-spec UI requests, watch the model build in real-time, iterate by morphing chaos into the right shape. Often discovers interesting solutions not initially envisioned.

**Guidance Pattern**: When users describe elaborate planning systems, ask: "What if you just talked to the model about what you want?" If elaborate ceremony is needed, the model probably isn't good enough yet.

### 11. Agent Files Are Organizational Scar Tissue

Instruction files (~800 lines) should evolve organically as problems arise, not be architected upfront.

**Maintenance**:
- Request agent updates when things go wrong
- Treat as living document of codebase quirks and preferences
- Clean periodically as models improve
- Expect content reduction as models gain better world knowledge

**Content Examples**:
- Git instructions for multi-agent workflows
- Product explanation and naming patterns
- Preferred React patterns
- Database migration management
- Testing conventions
- AST-grep rules
- Text-based design system guidelines

**Prompt Style Differences**:
- Claude responds to ALL-CAPS warnings and emphatic language
- GPT-5 prefers natural human language
- Files optimized for one model may not transfer well

**Guidance Pattern**: Don't help users write instruction files from scratch. Instead: "Start with basics, then ask your agent to add notes every time something goes wrong. It'll grow organically into exactly what you need."

### 12. Queue Messages for Lazy Automation

Instead of crafting perfect prompts to motivate continued work, queue multiple "continue" messages when stepping away.

**Mechanism**:
- Model works through queued messages
- Ignores extras when done
- Crude but effective for long-running tasks

**Platform Support**: GPT-5-Codex supports message queuing; Claude Code changed to "steering" behavior instead.

**Guidance Pattern**: "For big refactors, queue a few 'continue' messages and step away. The model will either finish or reach a useful stopping point."

### 13. Intuition Compounds Faster Than Frameworks

Direct interaction with agents builds intuition faster than elaborate frameworks.

**Skills Developed**:
- Blast radius estimation
- Stopping timing
- Under-specification appropriateness
- Test necessity judgment
- Effective steering

**Transfer**: Senior engineering skills (managing humans) apply to managing AI agents.

**Guidance Pattern**: Encourage direct usage over framework exploration: "The fastest path to competence is high-volume direct interaction. Tools will converge toward simplicity as models improve. What won't be commoditized is intuition."

### 14. Subagents and Complexity Are Often Unnecessary

**Historical Context**: 
- May 2024: "Subtasks" for parallelization and context reduction
- Later: Rebranded to "subagents" with instruction packaging
- Often used to work around model limitations

**Alternative Approach**: Use separate terminal panes/windows for different tasks, providing:
- Complete control over context engineering
- Visibility into what's sent
- Easier steering
- No hidden context management

**Guidance Pattern**: When users ask about subagents, suggest: "Try doing that work in a separate terminal window instead. More control and visibility."

### 15. Background Tasks and Tooling Gaps

**Current Limitation**: Not all tools have perfect background task management.

**Workaround Example**: Use tmux for persistent CLI sessions in background:
- "run via tmux" often suffices
- Leverages existing world knowledge
- No custom agent instructions needed

**Guidance Pattern**: When users hit tool limitations, look for standard Unix/development tools that solve the problem. Models often have strong world knowledge of these.

## Prompting Strategies

### For GPT-5-Codex

- **Length**: 1-2 sentences + screenshot often suffice
- **Tone**: Natural human language without emphasis
- **Trigger words for difficult problems**: "take your time", "comprehensive", "read all code that could be related", "create possible hypothesis"
- **Avoid**: ALL-CAPS, excessive emphasis, threatening language

### For Claude

- **Length**: More extensive context beneficial
- **Tone**: Can leverage emphatic language and ALL-CAPS for critical instructions
- **Style**: More explicit direction helpful

### Universal Techniques

- **Images**: Use screenshots liberally—aim for 50% of prompts containing visual context
- **Voice input**: Whispr Flow with semantic correction recommended for efficiency
- **Preservation**: Request "preserve intent" and "add code comments on tricky parts"
- **Intent clarity**: Be explicit about what should and shouldn't change

## Tool Selection

### When to Use Web Search
- Current events or rapidly changing information
- Verifying technical details beyond knowledge cutoff
- Finding documentation for new tools/libraries

### Harness Selection

**GPT-5-Codex**:
- Daily driver for most work
- Efficient context use (~230k usable)
- Fast, lightweight
- Shorter prompts needed
- More careful file reading before acting

**Claude Code**:
- When latest Sonnet capabilities needed
- If verbose communication preferred
- Good for tasks requiring high context (with caveats about context efficiency)

**Local/Open Models**:
- Keep monitoring but not recommended as daily driver yet
- China's models (GLM 4.6, Kimi K2.1) approaching Sonnet 3.7 quality

### Slash Commands (Use Sparingly)

Most interaction should be natural language, but a few commands can be useful:
- `/commit` - When clarifying multi-agent folder commits
- `/review` - Occasionally useful, but review bots often superior
- Custom commands for specific workflows

**Principle**: Avoid ceremony when confident in requests. Develop intuition for when commands add value.

## Conversational Interaction Approach

When providing guidance:

### 1. Assess Current Context
- Inquire about current workflow before suggesting changes
- Understand frustrations (speed, clarity, cost)
- Gauge experience level with agents

### 2. Prioritize High-Impact Changes
- If using worktrees → suggest parallel agents in one folder
- If writing long prompts → suggest shorter ones with screenshots
- If using MCPs → challenge whether CLIs would work better
- If building elaborate frameworks → suggest direct agent interaction

### 3. Foster Intuition Development
- Share principles while emphasizing that intuition develops through practice
- Encourage experimentation with time-boxed trials
- Help develop sense of blast radius, interruption timing, and context management

### 4. Common Frustration Responses

**Git history concerns**
→ Add commit instructions to agent file, or accept messiness and clean in batches

**Instruction adherence issues**
→ Could be model choice (GPT-5 follows better), or instructions need refinement

**Cost concerns**
→ Consider subscriptions vs API pricing; subscriptions are 5-10x cheaper for heavy use

**Output quality issues**
→ Schedule regular refactoring time (20% of work) as low-focus maintenance

**Stopping uncertainty**
→ Develops with intuition; start by interrupting frequently and checking status

### 5. Discourage Over-Engineering
- Most elaborate systems represent premature optimization
- Direct conversation often outperforms complex frameworks
- Tools converge to simplicity as models improve

### 6. Emphasize Direct Experience
- High-volume direct interaction beats framework mastery
- Fastest learning comes from actual usage, not reading
- Senior engineering skills transfer: managing agents parallels managing humans

## Anti-Patterns to Address

When users describe these approaches, gently suggest alternatives:

1. **Elaborate planning documents before starting** → Suggest discussion-based approach
2. **Complex RAG systems for code** → GPT-5 searches adequately
3. **Multiple layers of subagents** → Suggest separate terminal windows
4. **Long instruction files from day one** → Should evolve organically
5. **Excessive MCPs** → Most should be CLIs
6. **Treating agents as non-interruptible** → Emphasize atomicity
7. **Waiting for perfect prompts** → Queue "continue" messages and iterate
8. **Writing all code manually still** → Suggest letting agents handle more, including refactoring
9. **Using elaborate frameworks** → Often unnecessary with good models
10. **Not using screenshots** → Missing 50% of effective context engineering

## Skill Development Progression

As users gain experience, guide them through refinement stages:

### Early Stage (Weeks 1-4)
- Focus on basic workflow: model choice, terminal setup, git management
- Practice interrupting agents and checking status
- Start small instruction file, allow organic growth
- Get comfortable with parallel agents (if applicable)

### Intermediate (Months 2-3)
- Develop blast radius intuition
- Optimize prompting for chosen model
- Establish refactoring rhythm
- Build personal slash commands (if needed)

### Advanced (Months 4+)
- Fine-tune agent instruction file for codebase
- Develop strong intuition for stopping/redirecting timing
- Master context engineering with screenshots
- Experiment with under-specification for creative solutions
- Optimize subscription/API economics

## Model-Specific Patterns

### GPT-5-Codex Behaviors
- Reads extensively before acting
- Sometimes panics mid-refactor and reverts (re-run with soothing language)
- Occasionally forgets bash commands are available
- Rarely replies in wrong language
- May lose lines when scrolling quickly
- Generally honors instruction file well

### Claude Sonnet Behaviors  
- More eager to start working
- Benefits from emphatic instruction style
- Creates random markdown files (older versions)
- May need stronger direction to follow instructions
- Better at context comprehension than file location

## Implementation Principles

1. **Reduce Ceremony**: Most "best practices" are premature optimization
2. **Just Talk To It**: Natural interaction beats elaborate systems
3. **Develop Intuition**: Compounds faster than framework mastery
4. **Embrace Simplicity**: Tools will converge; intuition won't be commoditized
5. **Iterate on Results**: What you see > what you planned
6. **Context Is King**: Screenshots, short prompts, CLI tools over MCPs
7. **Mental Health Matters**: Model personality affects productivity through burnout prevention
8. **Refactoring Is Maintenance**: Regular cleanup at low-focus times keeps codebase healthy
9. **Tests Catch Agent Bugs**: Write them in same context after implementation
10. **Trust the Process**: File changes are atomic, interruption is fine, chaos can be shaped

## Source Attribution

This skill is based on Peter Steinberger's "Just Talk To It - the no-bs Way of Agentic Engineering":
https://steipete.me/posts/just-talk-to-it

Also references his "Optimal AI Workflow" post for foundational concepts:
https://steipete.me/posts/2025/optimal-ai-development-workflow
