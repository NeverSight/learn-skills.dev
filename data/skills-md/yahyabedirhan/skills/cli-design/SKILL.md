---
name: cli-design
description: Design, explain, audit or redesign a command-line interface through the CLI design delivery framework, for people, scripts and agents that call it. Use when designing a new CLI or new commands, reviewing an existing CLI's commands, flags, output, errors or help, restructuring or renaming a command tree, or deciding one question such as a command's name or a flag's shape.
---

# CLI design

A command-line interface is a **contract** with everyone who calls it: people at a terminal, scripts, CI jobs and agents. Every command name, flag, output shape, exit code and environment variable is part of that contract, and a script somewhere will depend on it the day it ships. A good CLI is predictable: someone who has learned one command can guess the next one, and the help alone is enough to use it.

Produce and present the design through the **delivery framework** in every session, whether you are designing, explaining, auditing or redesigning, so the user always finds the same things in the same places. The user chooses what the session is for; the framework sets how you lay out the answer. Stop once the user agrees to the design, since building it is done later.

The recurring failure is **drift**: each command added on its own terms, until the same verb means three things, the same idea has three names, and the help, the docs and the code each list something different. Prevent it by deciding the rules once, for the nouns, the verbs, the flag names and the output and error conventions, and deriving every command and every list a reader sees from them.

To design the code behind the commands, at the level of its modules, classes and folders, use `/low-level-design`. For a networked API, use `/system-design`.

## Flow

1. **Restate the session's purpose in one line**, read from the request and its context, so a misreading costs one reply: designing a new CLI or new commands, explaining or auditing an existing one, redesigning it, or deciding one question.
   - **Invoked inside a project with a CLI and no instructions:** explain and audit that CLI.
   - **When the purpose is unclear:** ask whether the user wants a new design, an audit of the existing CLI, or a change to it. Check yourself whether the CLI exists.
2. **Work through the delivery framework** below, stage by stage. Read [conventions.md](references/conventions.md) when a stage reaches flags, exit codes, environment variables, configuration or the layout of the help.
3. **Present every stage and revise it with the user** until they agree.
4. **Keep the design where the user wants it.**

The purpose decides how the stages are walked. The cases below are common, not a complete list; a session can mix them or move from one to another.

- **Designing something new:** write a complete first draft through every stage, from the user's requirements.
- **Explaining or auditing an existing CLI:** walk it through the stages as it is.
  - Build each stage from the evidence: run the top help and every group's help, read the command definitions and the dispatch code, and read the docs, scripts and skills that call the CLI. Cite the file or the command behind each claim.
  - Mark requirements read from behaviour **inferred**. Mark what the evidence can't show, such as who the main callers are or why a name was chosen, **unknown**, and ask about it rather than filling it in.
  - Count what the audit finds: commands per group, verbs and the meanings each one has, places that list the same thing by hand. Numbers show drift better than adjectives.
  - Record weaknesses as observations against the review checklist at the end, without proposing changes, since this session leaves the CLI as it is.
- **Redesigning an existing CLI:** explain it first and get the user's agreement that the explanation is right. Then redesign through the same stages, changing only what the problems need. Show every renamed command as a before/after row with the rule it breaks, and carry each rename through the evolution stage, since existing callers depend on the old name.
- **Deciding one question,** such as "should this be a flag or a subcommand?": answer it with the part of the design it touches, the requirement behind it, the options with their trade-offs, and a recommendation.

When the CLI being designed resembles a well-known tool, study that tool's help and the guides cited at the end before relying on memory: copy the patterns that serve the callers, and name the ones you leave out and why.

## The delivery framework

```text
Requirements → Command model → Inputs → Output and errors → Help → Implementation → Evolution
```

Each stage rests on the one before it: the command model comes from the requirements, the inputs and outputs spell each command of the model, the help is generated from all of them, the implementation keeps them in one place, and evolution tests the whole design against the next change. Move to the next stage once the current one has everything its product lists. Go back to an earlier stage when a later one exposes a gap.

### Requirements

Work down five themes:

- **Callers:** who runs the CLI: a person at a terminal, a script, CI, an agent. Name the main caller of each job, because a command for people and a command for scripts make different trade-offs.
- **Jobs:** what each caller comes to do, as "a caller should be able to..." statements. Keep the in-scope list short; each job becomes one or a few commands.
- **Roles:** the kinds of command by their effect: read only, change data, act on a running service or app, wait for an event, administer. Each role has its own rules, such as needing confirmation, a lock or credentials.
- **Runtime:** what each command needs to run: nothing, local files, a running daemon or app, the network. Say which commands work offline, since a status check that needs the service it checks can't report that the service is down.
- **Out of scope:** what the CLI will not do, such as an interactive interface, a plugin system or Windows support. The exclusions keep the command tree from growing commands nobody asked for.

Show them as short numbered lists.

### Command model

Turn the jobs into a command tree.

- **Nouns** are the objects the jobs act on, in the words the project already uses in its glossary, its UI and its docs. A noun with commands of its own becomes a group; information about a noun is an option or an output field, not a group.
- **Hierarchy:** draw the nouns as a containment tree (account › project › environment), and let the groups follow it. Use `noun verb` order, since it is the more common order and it groups related commands in the help.
- **Verbs** come from one closed vocabulary, one meaning each, used the same way on every noun that supports it. Pick one word from each synonym pair, such as `create` or `new` and `get` or `show`, and use it everywhere. Keep printing and displaying apart: a verb that prints data always prints, and a window or a picker gets its own verb. The default vocabulary is in [conventions.md](references/conventions.md).
- **Depth:** at most two levels, `tool <noun> <verb>`. A compound action gets a hyphenated verb (`send-text`) instead of a third level.
- **Top level:** only the few commands callers run every session, plus `help`. Everything else lives in a group, because a long flat list hides the commands that matter.
- **Targets:** one rule for how a command names the object it acts on: a required word (`tool project get <id>`), a named option (`--project <id>`), or a current default (a configured context, a working directory) that an option overrides. Apply the same rule to every command.

Show the model as the command tree with one line per group, the verb table, and the targeting rule.

### Inputs

Spell every command's arguments, flags and other inputs.

- **Words and flags:** a word is required input with a natural order, such as the file to copy. Everything else is a named flag, because flags can be added later without breaking callers and read clearly in scripts. When a command needs two inputs of different kinds, take the second as a flag, so a caller can't swap them by mistake.
- **Flag names:** long names in kebab case for every flag, a short letter only for the most common few, and the standard names for standard meanings (`--help`, `--version`, `--json`, `--quiet`, `--force`, `--dry-run`). The same flag means the same thing on every command.
- **Global flags** that every command takes (output format, verbosity, the target context) are parsed in one place.
- **Other sources:** standard input when the argument is `-`, environment variables, configuration files. Apply one precedence order, from flags down to built-in defaults.
- **Interaction:** prompt only when standard input is a terminal, and give every prompt a flag that answers it, so scripts and agents never hang. Confirm destructive actions, with `--force` or `--yes` to skip the confirmation, and offer `--dry-run` where an action is hard to undo.
- **Secrets** come from a file, standard input or the environment, never from a flag, since flags land in shell history and process listings.
- **End of options:** `--` ends the options, so text that starts with a dash is still a word.

Show one usage line per command, with its words, its flags and their value placeholders.

### Output and errors

Decide what each command prints and how it fails.

- **Streams:** data goes to standard output, so it can be piped. Progress, warnings and errors go to standard error.
- **For people and for programs:** the default output is for people, short and readable. `--json` prints a stable, documented shape on every command that prints data. Treat the JSON shape as part of the contract and the plain output as free to improve.
- **Terminals:** use colour, spinners and progress bars only when the stream is a terminal, and turn colour off for `NO_COLOR`, `TERM=dumb` and `--no-color`. Print something within about 100 ms, and show progress for anything that takes longer than a moment, so the command never looks hung.
- **Errors:** one line that says what went wrong and what to do next, naming the command or flag that fixes it. Put the most important information last, where the eye lands. Print a debugging trace only on request.
- **Exit codes:** 0 for success, a non-zero code for failure, and a distinct code for wrong usage. Document every code the CLI uses, and add a code only for a case a caller handles differently from failure, such as a timeout or "nothing found".
- **Robustness:** validate input before doing anything, give every network call and every wait a timeout, make reruns safe where possible, and exit promptly on Ctrl-C.

Show a table per command or per group: what it prints, its `--json` shape, its refusals and their exit codes.

### Help

Design the help as the main interface for learning the CLI, for people and for agents alike.

- **Three levels:** the top help (`tool --help`) fits one screen, a group's help (`tool <group> --help`, or the group alone) lists each of its commands with its full usage line, and a command's help (`tool <group> <verb> --help`) gives the usage, a description, every flag and examples. The layouts are in [conventions.md](references/conventions.md).
- **Summaries:** one line per command, starting with a verb and saying what the command achieves, not how the code does it. Use the same summary everywhere it appears.
- **Examples** lead the command help, because most readers copy one and adjust it.
- **When the caller is wrong:** wrong usage prints that command's usage line and a pointer to its help, not the whole manual. A mistyped command suggests the closest match and leaves the caller to run it.
- **Discovery:** the top help names where the full documentation lives. When agents are callers, give them a machine-readable listing of the commands (a `help --json` or a schema command), and point them to it from the top help once.
- **Completions** for the common shells, generated from the same command definitions.

Show the top help, one group's help and one command's help as mock-ups.

### Implementation

Design how the CLI keeps the contract in code. Use the argument-parsing library the language's ecosystem already standardises on, and build only what it lacks.

- **One command table as data:** each command's name, group, usage, summary, description, examples, flags, target and role, in one place. The parser, the help, the completions, the docs and the machine-readable listing all read from it.
- **One path** from arguments to exit code: parse the global flags, find the command, parse its inputs, run it, print, exit. Every command passes through it, so the conventions apply without each command restating them.
- **No list written twice:** every list a reader sees, such as which commands take a flag, comes from the table. A list written by hand in the help or the docs will drift from the code.
- **One file per group**, named for the group, so a change to a group opens one file.
- **Contract tests** that keep the design true: every example in the help parses; every command named in an error message, a doc or a script exists; the help matches a stored snapshot; each command's `--json` output matches its documented shape.

Show the folder tree with what each file owns, the command table's fields, and one command traced from arguments to exit code, plus one refusal.

### Evolution

Test the design against the changes likely to come next, and decide how the contract changes.

- **Additive first:** add a command, a flag or a JSON field rather than changing one. A new flag can change a behaviour without breaking anyone who doesn't pass it.
- **Renames** keep the old name as a hidden alias, with a warning on standard error that names the new one, for a stated period. List every alias by name, and match only full names: a catch-all command blocks any future command with the word it catches, and prefix matching blocks any future command that shares a prefix.
- **Breaking changes** are announced in the CLI before they ship, with the way to change usage today, and released with a version bump that callers can see.
- **Versioning:** `--version` prints the version, and the docs, completions and any agent instructions that call the CLI ship with the same release.

Show the likely changes as a "change → what you touch" table. A change that lands in one new command in the table is absorbed; one that repeats the same edit across several files needs a seam.

## Defaults first

Start each choice from its default, because callers bring these expectations from other CLIs and every departure costs each of them a lookup: `noun verb` at two levels, the standard flag names, `--json` on every command that prints data, standard output for data and standard error for messages, exit 0 for success, 1 for failure and 2 for wrong usage, no prompts when not in a terminal, and help generated from one command table. Move off a default only for a named requirement, and say which.

## Review checklist

Check a finished design, or audit an existing CLI, against every item:

1. Each job can be done from the help alone.
2. Each verb means one thing across the whole tree, and each idea has one name.
3. Every noun is a word the project already uses.
4. The tree is at most two levels deep, with only everyday commands at the top level.
5. The same flag means the same thing on every command, and standard meanings use the standard names.
6. Every command that prints data takes `--json`, and data and messages go to different streams.
7. Every error says what to do next, and every exit code is documented.
8. Nothing prompts or hangs when there is no terminal, and every wait has a timeout.
9. Every list in the help and the docs is generated from the command table.
10. Every example is tested, and every command named in an error, a doc or a script exists.
11. Every rename leaves an alias, and every breaking change is announced before it ships.

## Working with the user

Load `/show-me` and present every stage visually: the command tree as a tree, the verbs and the renames as tables, the help as a mock-up, a traced command as a call tree. Use prose only for the reasons behind choices.

- Keep one current version of the design and revise it rather than starting over.
- Open each revision with what changed and why, as a before/after `diff` of the tree, table or help that changed, and carry a change through every stage it affects.
- Leave a point the user settled as it is unless they reopen it.
- When there is more than one reasonable option, number the options side by side, each with its cost, and lead with your recommendation.
- Ask only what the code, the docs and the user's earlier answers can't settle, one question at a time. Decide the rest and say what you decided.

While the design is being refined, keep it in a draft in the project's scratch or temporary folder, following the repository's conventions; when it has none, ask where. An explanation can stay in the conversation. Once the user agrees and wants the design kept, write it into the project's documentation, updating an existing design document rather than adding a second one.

## References

| Reference | Covers |
|---|---|
| [conventions.md](references/conventions.md) | The default verb vocabulary, standard flag names, exit codes, environment variables, configuration precedence, and the layouts of the three help levels |

---

Sources: [Command Line Interface Guidelines](https://clig.dev/) and [POSIX Utility Conventions](https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap12.html).
