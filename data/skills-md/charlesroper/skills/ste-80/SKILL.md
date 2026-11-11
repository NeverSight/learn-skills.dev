---
name: ste-80
description: Write and edit operational software documentation using an 80% implementation of ASD-STE100 (Simplified Technical English) across operational runbooks, incident playbooks, deployment procedures, CLI flag and environment variable specs, error tables and code-review summaries.
---

# Simplified Technical English (STE-80)

Write and edit operational software documentation, runbooks, CLI specs, API guides and troubleshooting steps.

## Scope and routing

Use `ste-80` for operational and machine-adjacent technical writing:
- Runbooks and incident playbooks
- Deployment, rollback and maintenance steps
- CLI flag, command and environment variable specifications
- Error tables and troubleshooting steps
- Pull request descriptions and code-review summaries

Defer non-operational writing to `on-writing-well`:
- Conceptual overviews and architecture narratives
- README introductions and motivation sections
- Step-by-step beginner tutorials
- Web pages, landing pages and content design
- UI labels, button copy and microcopy

## Procedure

1. **Confirm operational scope.** Verify that the document belongs to operational writing. If the text requires conceptual exposition, narrative flow or personal voice, route to `on-writing-well`. *Completion: Operational scope is confirmed or routed to `on-writing-well`.*
2. **Draft or rewrite under STE-80 mechanics.** Apply the sentence limits, active imperatives, 80% vocabulary rules and safety warning placements defined below. *Completion: Draft satisfies all structural limits, step rules and vocabulary constraints.*
3. **Verify against checklist and deliver.** Check the draft against the 5-point verification checklist. Deliver the final text directly without meta-commentary, progress narration or conversational preamble. *Completion: Draft passes all five checklist points and is delivered directly.*

## Core mechanics

### Sentence and paragraph ceilings
- **Procedural steps:** Maximum 20 words per sentence.
- **Descriptive sentences:** Maximum 25 words per sentence.
- **Descriptive paragraphs:** Maximum 6 sentences per paragraph.

### Action steps and imperative verbs
- **Numbers for sequences, bullets for alternatives:** Use numbered lists (`1.`, `2.`, `3.`) only when two or more actions must run in chronological order. Use bulleted lists (`-`) or condition-first sentences for mutually exclusive choices, optional flag variants and unordered commands. Never number alternatives or single-action procedures.
- **One action per step:** Limit each step to one discrete action starting with an imperative transitive verb in the present tense (*Run*, *Stop*, *Set*, *Verify*). Never combine separate actions into one step with coordinating conjunctions.
- **Conditions and preconditions before actions:** State conditional clauses before the action (*"If the health check fails, run rollback.sh"*, not *"Run rollback.sh if the health check fails"*). Keep location or state preconditions as lead-in clauses (*"From the repository root:"*) before the steps; never pad preconditions into ambient operator actions (*"Open a terminal"*, *"Press enter"*) unless a privileged or non-standard environment is required (*"Open an elevated terminal"*).

### The 80% vocabulary rule
- **Retain exact technical terms:** Keep technical nouns, API names, CLI flags, configuration parameters and error codes verbatim (`SIGTERM`, `kubectl`, `--max-retries`, `HTTP 503`).
- **One term per concept:** Do not swap synonyms. Choose one technical word and use that exact word throughout.
- **Limit noun clusters:** Restrict noun modifiers to a maximum of 3 words. Break longer noun chains with prepositions (*"production database connection pool timeout"* becomes *"connection pool timeout for the production database"*).
- **Ban progressive `-ing` forms:** Replace present participles and `-ing` verbs with active verbs or conditional clauses (*"Before you compile"* instead of *"Prior to compiling"*).
- **Use simple connectors:** Replace wordy prepositions with direct words (*to* instead of *in order to*, *because* instead of *due to the fact that*, *if* instead of *in the event that*).

### Immediate safety warnings
Place warnings and cautions directly before the affected step. Never hide safety notices inside or after the action step.
- Use `WARNING:` when an action can cause data loss, downtime or security breaches.
- Use `CAUTION:` when an action can cause performance degradation, transient errors or rework.
- Format: `WARNING: [Preventive action]. [Consequence].`
  - Example: `WARNING: Stop the worker daemon before you drop the cache. Active workers crash if the cache is missing.`

## Before / after rewrites

### Procedural instruction

**Before:**
> When you are preparing to initiate the database migration process, it is essential that you first ensure all background worker services have been properly terminated by administrators so as to avoid encountering severe data corruption issues during schema updates. Once you have successfully verified that no jobs are currently running, proceed with executing the migration script via the command line interface while monitoring stdout for any potential failure indicators.

**After:**
> WARNING: Stop all worker services before you run database migrations. Active workers write corrupted data during schema updates.
>
> 1. Stop the worker service:
>    ```bash
>    systemctl stop worker.service
>    ```
> 2. Verify that no worker processes remain:
>    ```bash
>    pgrep -c worker
>    ```
> 3. Run the migration script:
>    ```bash
>    ./bin/migrate --env=production
>    ```
> 4. Verify that the command exit code is `0`.

### Technical parameter description

**Before:**
> The `--timeout-seconds` configuration flag allows system administrators the flexibility of determining the maximum permissible duration in seconds that the HTTP gateway client will patiently await an upstream microservice response prior to automatically terminating the connection and surfacing a gateway timeout error condition to downstream consumers.

**After:**
> The `--timeout-seconds` flag sets the maximum wait time for upstream HTTP responses. If the upstream service does not respond within this duration, the gateway closes the connection and returns an HTTP 504 status code. The default value is `30`.

## 5-point verification checklist

Before delivering output, verify that the text satisfies these five criteria:

1. **Sentence ceilings:** Every procedural step is 20 words or fewer; every descriptive sentence is 25 words or fewer; every paragraph is 6 sentences or fewer.
2. **Imperative verbs and list types:** Every procedural step begins with an active imperative transitive verb and contains one discrete action; numbered lists are used only for two or more sequential steps; alternatives use bullets or condition-first sentences; ambient actions (*"Open a terminal"*) are omitted.
3. **Safety warnings:** Every critical risk has a `WARNING:` or `CAUTION:` block placed directly before the affected step using the `[Preventive action]. [Consequence].` format.
4. **Vocabulary consistency:** Technical terms and flags are exact and consistent across the text, noun clusters do not exceed 3 words, and progressive `-ing` forms are absent.
5. **Direct delivery:** The text contains zero conversational filler, zero meta-commentary and no introductory or concluding pleasantries.
