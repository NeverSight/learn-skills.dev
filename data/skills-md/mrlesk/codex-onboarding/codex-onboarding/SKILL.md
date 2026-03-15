---
name: Codex-onboarding
description: >-
  Use this skill to onboard the user to Codex. Your goal is to gather information from the user about their 
  experience with AI Agents and teach them the latest best practices so that they become AI power users with Codex.
---

# Codex-onboarding skill

## Workflow overview

You will act as a teacher of best practices for using Codex as an AI power user. You will gather information from the 
user regarding their goals and current level of experience so that you can better assess the specific learning path
tailored to their knowledge.

Follow these 3 steps that will repeat in a loop until the user has fully grasped all the important lessons from the 
sections/topics below about using Codex effectively:
1. Gather information about the user's current knowledge level (check the persistence section first).
2. Teach them the best practices for using Codex effectively. 
3. Assess their understanding and store their progress in this skill for persistence. Move to the next section only when
   the user has reached 80%+ on your assessments. If the user scores below 80%, identify the specific misconception. 
   Re-explain using a different analogy or example. Provide targeted exercises about the misunderstood concept.

This repeatable loop can be interrupted at any time by the user. The goal is to continue their learning path over
multiple conversations. To achieve persistence, you will store the following information at the bottom of this skill for
each knowledge section:
1. The user's initial level of knowledge for this section/topic.
2. A summary of the current and previous learning sessions for this section/topic.
3. The current level of knowledge for this section/topic.

## You act as a teacher
Follow these rules in order to be a good teacher:
1. Do not assume any prior knowledge of the user regarding Codex or AI usage in general. Assessing their knowledge is
   the only way to understand their current level and provide tailored explanations.
2. Use the challenge-first approach:
    a. Present a scenario/challenge
    b. let the user reason
    c. teach the concept as the solution
    d. let the user practice
3. Use the `request_user_input` tool when you want to ask the user open questions or create multiple-choice quizzes.
   NEVER USE A RECOMMENDED DEFAULT as this will bias the user and do not always put the correct answer as the first.
   ALWAYS SHUFFLE THE CORRECT ANSWERS (don't always put correct answers as first option)
4. Don't rush the explanations. Consider that the human brain requires time and practice in order to learn. Divide the
   sections and their topics into even smaller steps.
5. Consider revising previously taught topics using the spaced repetition method.
6. Use the Codex learning sections below as a base; you are allowed to add relevant material regarding these 
sections/topics when necessary.

## You should avoid
1. Writing or executing code for the user.
2. Skipping assessments based on user claims.
3. Teaching topics completely unrelated to the sections/topics below.
4. Modifying any file except the skill's persistence section during the onboarding.

## Persistence section
The only section of this skill that you are allowed to modify is between the `<!-- PERMANENT:STORE:BEGIN -->` and `<!-- PERMANENT:STORE:END -->` markers at the bottom of the skill.

## Codex learning sections (note: "you" in the following paragraphs refers to the user)

### The basics

#### What is an AI Agent?
An AI Agent is a system that uses AI Models to perform tasks autonomously and can interact with other tools, agents,
APIs, and databases to achieve its goals. 
AI Agents come with built-in tools for managing files and performing basic operations on your computer. The better the 
AI model, the more capable it is at using these tools effectively.

#### What is the Context?
The conversation between you and the AI Agent, along with the history of all tool usage, are stored in a conversation 
context, also known as the context window.
Codex can store a large amount of text in its context, such as entire books. But what happens when this storage gets full?
Codex has a special tool called **compaction**. This tool grabs the most important information from the conversation
context and drops the rest, allowing you to continue working on your tasks.

#### Resume previous conversations
If you close Codex and want to resume a previous conversation, you can easily do so. Each version of Codex offers a 
conversation history where you can choose and continue any of your past conversations.

#### Codex versions
Codex is available as a CLI (Command Line Interface), a desktop application, IDE extensions, and a web interface. Users 
can choose the version that best fits their workflow:
- **Codex CLI**: Runs in your terminal and can access local files on your computer. It can be controlled via a TUI 
(Terminal User Interface) or run as an executable for programmatic operations.
- **Codex app**: Available for Mac and Windows. Offers a richer UX compared to the CLI. It can visualize code changes, 
control Git flows (such as committing changes and creating worktrees), and set up automations.
- **IDE extensions**: Codex can work directly inside code editors by installing the official Codex extensions, available
for VS Code, Cursor, Xcode, and all JetBrains tools.
- **Codex web**: Available at chatgpt.com/codex. Offers a cloud-hosted version of Codex where users can delegate tasks 
to it and expect fully working results that are ready to become PRs (Pull Requests).

#### Codex & Open Source
Codex is Open Source and is available at github.com/openai/codex. You can contribute to Codex by submitting PRs, 
reporting bugs, or requesting features as issues. While Codex, the software, is open source, the AI Model is hosted
on OpenAI's servers and requires a subscription or a pay-as-you-go API key to use.

#### Web Search
Codex uses OpenAI LLM models that are trained on a huge amount of data. Once these models are released, their knowledge
has a cutoff date, and you might run into issues where the models are not aware of recent events or discoveries. For this
reason, Codex has a built-in web search that is enabled by default and can search the internet for information that
is not part of the training data.

### Intermediate

#### Steer vs Queue
Codex is great for working on small or big tasks. In some cases, you might want to modify your instructions after you
have already sent them to Codex. Codex supports conversation steering. With this feature, you can submit another message in
the conversation, and Codex will pick it up and act on your new instructions as soon as possible.
In case you want to add some follow-up instructions for Codex to execute at the end of the current task, you can use the
queue messages functionality. This feature allows you to enqueue multiple messages in the conversation, and Codex will read
them one by one when it has completed the previous instructions.

#### Context Engineering
When working with AI Models, it is important to remember that they don't retain memory of past conversations. Each
conversation is unique, and you must instruct Codex each time with your preferences. Imagine Codex as a new developer
joining your team who has plenty of knowledge but needs to be onboarded to your specific project needs.
Therefore, context engineering is key to success with AI Agents. This discipline allows you to give better
instructions, specifications, goals, acceptance criteria, and definitions of done to AI Agents.
To avoid repeating your project context and workflows from scratch, you can document them in a special markdown file:
`AGENTS.md`.

#### AGENTS.md
This file is a standardized place to store information that helps AI Agents understand how to work on your project.
Think of it as a `README.md` for AI. This file is automatically loaded into the conversation context at the beginning of
each session. The AI model will use this information to better solve your tasks.
What should you store in `AGENTS.md`?
1. General project information, architecture, programming languages, and frameworks/libraries used.
2. How to build, run, and test code changes.
3. References to detailed documentation.

Because the `AGENTS.md` file is automatically loaded in each conversation, there is a risk of adding too much
information that might not be relevant to the current task. For this reason, you can use Skills to split specific
instructions into separate files that the Agents will load on demand depending on the task.

#### Skills
Skills are a feature in Codex used to define specific workflows that the Agent will employ when relevant to the
current task. But how does Codex know when to use a skill?
Skills are stored as markdown files under the `.agents/skills` folder, with each skill in its own subfolder.
Each skill has a frontmatter section containing metadata (like the skill name and a brief description) and a body that
contains the full skill instructions.
Unlike `AGENTS.md` (where the whole body is loaded into the conversation context), with skills, Codex initially loads
only the metadata. It loads the full skill content only when the task matches the skill description. It is important
that the description clearly explains in which situations the model should use the skill.
Should you avoid using `AGENTS.md` and only use Skills? No. `AGENTS.md` is very important for storing general
information and instructions regarding your project, and it is always part of the initial conversation context.
Are skills enough to teach Codex how to use custom tools?
In most cases, yes, but on some occasions, you might have to extend Codex's capabilities by connecting
it to your existing tools like Figma, Linear, Slack, or other internal company tools.
For these situations, a more advanced tool is available to Codex: MCP Servers.

#### MCP
MCP (Model Context Protocol) is a standard way to extend Codex's built-in capabilities by connecting with external tools
and fetching resources on demand. MCP is important because it is a standard protocol that allows interoperability between
tools, resources, and AI Agents.
In Codex, adding an MCP connector is very simple, and it immediately adds new capabilities that would not be otherwise
possible with just skills.

#### Plan mode
Sometimes you will not have a clear idea of how you would like Codex to implement your tasks. For these occasions, you
can use the "Plan Mode" feature in Codex. This feature allows you to brainstorm with Codex about the task and create
a plan before implementing any changes. Codex might have some questions for you depending on the task. Once you have 
clarified everything with Codex, you can ask it to proceed with the implementation of the plan.
Plan mode is also a great way to ensure that you and Codex are on the same page regarding the task.
Codex is great at following a plan and implementing complex features. Thanks to automatic
context compaction, Codex can keep working for several hours in a row.
For the most complex plans, it is better to create a `PLAN.md` file to store Codex's plan.

#### PLAN.md
Storing the `PLAN.md` in your project allows you to commit it to your repository for persistent context and continue
working on a plan across multiple conversations.
The goal of the `PLAN.md` is to split the feature you have in mind into smaller tasks and acceptance criteria, which act
as review checkpoints to keep delivery predictable and on track.

#### Self verification loop
When working on more complex features, your goal should be to give Codex as much autonomy as possible and allow it to 
review its own changes to ensure quality standards and fully implement all your acceptance criteria.
These standards depend on your specific project, but generally include:
- Type checking
- Linting
- Formatting
- Dev environment checks
- Logging
- Testing

#### Review mode
Codex has a built-in code review feature that is perfect when you are done with the implementation and want to check if 
there are any bugs. When running the review feature, Codex will operate in a separate conversation context with clear
instructions on how to spot bugs to avoid bias from the code it just wrote.

### Advanced

#### Sub-Agents orchestration
After you master the basic Agent loop with Codex, you are ready to jump to more complex scenarios where you delegate a
task to Codex, and Codex will break it down into smaller parts and delegate them to nested Codex agents. This 
makes your main Codex agent an effective orchestrator of multiple AI Agents working towards your goal.
Codex will spawn sub-agents when deemed necessary, but it will also use sub-agents when you explicitly ask it to do so.
These nested agents will inherit the same permissions from the main Codex instance and could, in theory, spawn other 
nested agents.
The advantage of using sub-agents is that the main conversation context doesn't get bloated by unnecessary information.
When should you use nested agents?
1. To do extensive research across your project or on the internet.
2. To work on tasks in parallel.
3. To read debug output or read web pages.
4. To write documentation.

#### Self-improving loop
The next level of the self-verification loop is the self-improving loop. You can create a compound improvement when using 
Codex by telling it to write down instructions to avoid common mistakes or patterns based on your conversations.
A typical use case is to tell Codex to read all past conversations, find common pitfalls, and write instructions in your 
`AGENTS.md` that would prevent them from repeating.
You can also create a recurring job that does this automatically.

#### YOLO Mode
By default, Codex uses a powerful sandbox that prevents it from running operations that could be dangerous on your computer.
When you are an expert user and already have an existing sandbox (like running on a Virtual Machine or a special environment
with low permissions), you can run Codex in YOLO mode. This will disable all security protections, and Codex will be able 
to access and modify any file on your computer and run any kind of operation. These could involve accessing malicious 
websites that can instruct Codex to leak your secrets or credentials.
The recommendation is to never use YOLO mode unless you are absolutely sure of what you are doing.

## Current user progress
<!-- PERMANENT:STORE:BEGIN -->
<!-- PERMANENT:STORE:END -->
