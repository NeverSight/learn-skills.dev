---
name: jev-cli
description: >
  Use the `jev` command-line tool (an unofficial, open-source CLI for TypeSafe AI's Jev model) to
  get calibrated probabilities for typed questions about text or JSON: yes/no (noul), one of
  several options (choice) or a position on a rubric (score). Covers discovering the CLI with
  `jev spec`, authoring request files from `jev schema`, checking them offline with
  `jev validate`, running them with JSON output, branching on exit codes, gating shell scripts
  and CI on an answer, labelling many records with `jev batch run`, and choosing between the CLI
  and the `jev mcp serve` tools. Use when a task needs a semantic judgment about some content
  (classify, route, detect, rate, verify) and `jev` is available, or when writing a script or CI
  step that calls `jev`.
license: MIT OR Apache-2.0
---

# Using the `jev` CLI

> **Unofficial.** `jev` is a community project. It is not affiliated with, endorsed by or
> sponsored by TypeSafe AI. "TypeSafe" and "Jev" belong to their owner.

Jev never writes text. It reads a **state** (a string, or a JSON object or array) and answers
**questions you define** with probabilities:

- **noul**: does this hold? The probability of yes, from 0 to 1. Absolute: several nouls about
  the same state can all be high, or all low.
- **choice**: which one of these options? Probabilities over your options (up to 255) that add
  up to 1, the winner, and a confidence.
- **score**: where on this ordered rubric of 2 to 10 levels? The expected level, counted from 0.

## The rule that matters most: ask the binary, not this file

This skill teaches a workflow. The contract (every command, flag, default, environment variable,
exit code and output shape) lives in the binary, and the binary is always right:

```bash
jev spec                                   # everything, as JSON
jev spec | jq -r '.commands[] | select(.implemented) | "\(.path)\t\(.about)"'
jev spec | jq '.commands[] | select(.path == "batch run")'
jev eval --help                            # the same facts for one command, as text
jev schema request                         # JSON Schema of a request file
```

Each command in `jev spec` has `when_to_use`, `input`, `output`, `flags`, `exit_codes` and
`examples`. Read the entry of the command you are about to use before you use it. Commands whose
`implemented` is false answer "not implemented": do not call them.

## Before the first call

1. `jev version` shows that `jev` is installed. If the command is not found, **ask the person
   before installing anything**, then run the line for their platform:

   | Platform | Install |
   | --- | --- |
   | macOS or Linux, Homebrew available | `brew install shaharia-lab/tap/jev` |
   | macOS or Linux | `curl -fsSL https://raw.githubusercontent.com/shaharia-lab/jev-cli/main/install.sh \| sh` |
   | Windows, PowerShell | `irm https://raw.githubusercontent.com/shaharia-lab/jev-cli/main/install.ps1 \| iex` |
   | Any platform with Rust | `cargo install jev-cli --locked` |

   The scripts pick the build for the machine's architecture, verify its checksum and signature,
   never use sudo, and install into `~/.local/bin` (`%LOCALAPPDATA%\Programs\jev` on Windows).
   If that directory is not on `PATH` in the current shell, say so rather than editing a profile.
   Confirm with `jev version`, and read the [installation
   guide](https://github.com/shaharia-lab/jev-cli/blob/main/docs/user-guide/installation.md) if
   anything fails.
2. `jev auth status --offline -o json` shows whether an API key is configured (`authenticated`,
   and `source`: `env` or `file`). It never prints the key.
3. If there is no key, **stop and ask the person** to either export `TYPESAFE_API_KEY` or run
   `jev auth login` themselves. Never ask for the key, never type it, never put it on a command
   line or in a file. `jev` has no other way to authenticate.
4. Offline work needs no key: `jev spec`, `jev schema`, `jev validate` and `--dry-run` never touch
   the network and cost nothing.

## The loop: discover, author, check, run, branch

**1. Discover.** Pick the command from `jev spec` (see "Which command" below) and read its entry.

**2. Author.** Write a request file in YAML or JSON. `jev schema questions` describes a question
set whose state is supplied separately (the usual case); `jev schema request` describes a file
that also carries its own `state` and `model`. Question ids are yours to name and come back as
the keys of `answers`.

```yaml
# triage.yaml: three questions about one ticket, answered in one call
questions:
  is_urgent:
    type: noul
    instructions: Does the customer say the problem needs attention today?
    criteria:
      "true": The message states a deadline, an outage or money being lost now
      "false": No time pressure is stated
  team:
    type: choice
    instructions: Which team should handle this ticket?
    criteria:
      billing: Charges, invoices, refunds, payouts
      technical: Errors, outages, integrations, bugs
      other: Anything else, or not enough information to tell
  frustration:
    type: score
    instructions: How frustrated does the customer sound?
    criteria:
      - Calm and neutral
      - Annoyed, but polite
      - Angry, or threatening to leave
```

**3. Check, offline and free.** Fix every finding before sending anything:

```bash
jev validate -f triage.yaml --state-file ticket.txt -o json
```

Exit 0 means valid; exit 2 means not valid, and `.findings[]` says what is wrong (`rule`,
`question`, `path` as a JSON Pointer, `message`, `suggestion`). Add `--strict` to treat warnings
as errors. `jev eval -f triage.yaml --state-file ticket.txt --dry-run -o json` also prints the
exact body that would be sent and its estimated size.

**4. Run.** Always ask for JSON explicitly:

```bash
jev eval -f triage.yaml --state-file ticket.txt -o json
```

The result has `answers` (one per question id), `model` (the versioned model that answered),
`usage`, `cost_usd` (an estimate), `request_id` and `latency_ms`. `jev schema output` is its
schema. `--field answers.team.choice` prints one raw value instead of the whole document.

**5. Branch on the exit code**, not on stderr text:

| Code | Name | What it means for you |
| --- | --- | --- |
| 0 | success | Done; any gate condition holds. Read stdout. |
| 1 | internal | A bug in `jev`. Report it; do not retry in a loop. |
| 2 | usage | Your command line or request is wrong. Nothing was sent or billed. Read the error, fix, retry. |
| 3 | auth | No API key, or the API refused it. Ask the person; never try to find a key yourself. |
| 4 | api_rejected | The API rejected the request. Read `message`; run `jev validate --strict`. |
| 5 | rate_limited | Rate limited or overloaded after retries. Wait, or lower `--concurrency`. |
| 6 | network | Network failure, timeout or server error after retries. Try again later. |
| 7 | batch_partial | A batch finished, but some rows failed. Their records say why; rerun with `--resume`. |
| 10 | gate_false | Evaluated successfully, and the gate condition is **false**. Not an error. |
| 11 | abstain | Evaluated, and the answer is inside the abstain band: the model cannot tell. |
| 20 | update_available | A newer `jev` exists. |
| 130 | interrupted | Interrupted. A batch can continue with `--resume`. |

On failure, stderr carries one JSON object when it is not a terminal:
`{"error": {"code", "exit_code", "message", "hint", "request_id", ...}}` (`jev schema error`).
`hint` names the next action: read it before retrying. Other stderr lines are notices,
`{"warning": {...}}` or `{"info": {...}}` (such as `jev` having updated itself); they never change
stdout or the exit code.

## Which command

| You have | Use |
| --- | --- |
| One state and one question, written inline | `jev noul`, `jev choice` or `jev score` |
| One state and several questions | `jev eval -f`: one call, and the state is paid for once |
| Many states and the same questions | `jev batch run` |
| A request file to check, with no key or cost | `jev validate` |
| An MCP client in which `jev` is registered | the MCP tools, see below |

Ask every question about one state in **one** `jev eval` call rather than several shortcut calls:
extra questions add tokens, not round trips.

### CLI or MCP server

`jev mcp serve` exposes Jev to an MCP client as tools. MCP tools: `evaluate`, `noul`, `choice`,
`score`, `validate`, `list_models`. Each result is the same envelope as `jev eval -o json`, plus
the session's calls and estimated spend. A server started with `--allow-dir <dir>` also offers
`batch_run`, which runs `jev batch run` over files inside those directories only, with optional
`--max-batch-rows` and `--max-batch-cost-usd` caps.

- **Prefer the MCP tools** for a judgment you need yourself during a conversation, when your
  client already lists them: structured arguments, no shell quoting, no files.
- **Prefer the CLI** for anything a person will keep or rerun: shell scripts, CI steps, Makefiles,
  gates on an exit code, request files under version control, and bulk work (`jev batch run`).
- Registering the server changes the person's client configuration, so ask first. For Claude Code
  it is `claude mcp add jev -- jev mcp serve`; the key comes from the environment or
  `jev auth login`, never from the client's configuration.
- To cap spend, the server takes `--max-cost-usd-per-call`, and a capped server needs a pinned
  model with a known price (`--model jev-1.13.0`, not an alias such as `jev-latest`).

## Gates: Jev as a shell condition

Gating flags turn the answer into the exit code, so a script needs no JSON parsing. The answer
is still printed as usual.

| Command | Gating flags |
| --- | --- |
| `jev noul` | `--fail-under`, `--fail-over`, `--abstain-band` |
| `jev choice` | `--expect` (repeatable), `--min-confidence` |
| `jev score` | `--fail-under`, `--fail-over`, `--min-confidence` |
| `jev eval` | `--assert` (repeatable), e.g. `"is_urgent >= 0.7"`, `"team == billing"`, `"team.confidence >= 0.8"` |

Exit 10 means only "evaluated, and the condition is false". Every other non-zero code is a
failure, never a "no": a script must not treat a missing key (3) or an outage (6) as a negative
answer.

```bash
status=0
jev noul "Is this message unsolicited advertising?" --state-file message.txt \
    --fail-under 0.6 --abstain-band 0.4,0.6 --field noul > p_spam.txt || status=$?
case "$status" in
  0)  echo "spam" ;;
  10) echo "not spam" ;;
  11) echo "unclear: send to a person" ;;
  *)  echo "jev failed with exit $status" >&2; exit "$status" ;;
esac
```

The `|| status=$?` keeps `set -e` from ending the script on exit 10.

## Bulk: `jev batch run`

`jev batch run` applies one question set to every row of a JSONL or CSV file, or of a JSON array
(`--input-format json`, a file of at most 50 MB; a `.json` array is detected), and writes one
record per row as JSON Lines, in the order rows finish:

```bash
jev validate -f triage.yaml --strict
jev batch run -f triage.yaml --input tickets.jsonl --state-field body --model jev-1.13.0 --dry-run
jev batch run -f triage.yaml --input tickets.jsonl --state-field body --model jev-1.13.0 \
    --id-field ticket_id --limit 10 --out sample.jsonl
jev batch run -f triage.yaml --input tickets.jsonl --state-field body --model jev-1.13.0 \
    --id-field ticket_id --out results.jsonl --summary-json summary.json
```

- Validate the question set, then `--dry-run` (free, no key) to see how many requests the run
  makes and its estimated cost, which needs a pinned model: an alias has no price. Then run a
  small sample with `--limit` and read it before the full file.
- `--state-field` sends one field as the state, `--state-fields subject,body` an object of
  several; the default is the whole row. `--id-field` keys the records; the default is the line
  number (in a JSON array, the element's 1-based index).
- Each record has `status` `ok` (with `answers`) or `error` (with `error`), and
  `jev schema batch-record` is its schema.
  `jq -r 'select(.status == "error") | .id' results.jsonl` lists the failed rows.
- `--merge` adds the whole input row to every record as `row`, so the records need no join back
  to the input by id. Filter them with `jq`, e.g.
  `jq -c 'select(.status == "ok" and .answers.is_urgent.noul >= 0.6)' results.jsonl`.
- After exit 7 (some rows failed) or 130 (interrupted), fix the cause and rerun the same command
  with `--resume`: rows already recorded `ok` are not sent again.
- Leave `--concurrency` at its default unless you know the key's limits; shared keys get rate
  limited above about 8.
- Prefer a file to piped rows: a file is checked in full before anything is sent.

## Writing questions that work

Jev makes quick, literal judgments about meaning. It is good at "does this text say X", "which of
these fits best", "how strongly". It is not a calculator or a reasoner. For deeper design
guidance, patterns and current documentation, use TypeSafe's own agent skill,
[typesafe-ai/skills](https://github.com/typesafe-ai/skills), and <https://docs.typesafe.ai>.

- **Keep computation in code.** Counting, arithmetic, comparing numbers or dates, lookups and
  exact matching belong in your program. Use Jev to pull out the meaning (for a date, ask a
  choice for the month and another for the day), then compare in code.
- **One quick judgment per question.** If a knowledgeable person could not answer it at a glance,
  split it into several questions and combine the answers in code.
- **Ask everything in one request.** Include questions you only need on some branches; phrase
  them with their premise ("If this is a billing problem, ..."). Make a second request only when
  it depends on the first answer.
- **Send only what matters.** Trim the state to the part the questions are about; unrelated text
  lowers accuracy.
- **Pick the type by what the answer means.** Noul for "does this hold" (one noul per label when
  several labels can apply), choice for "exactly one of these", score for "where on this ordered
  scale".
- **Give every choice a way out**, such as `other`, `none_of_the_above` or `not_stated`. The model
  cannot pick an option that is not there, and `jev choice` warns when there is none.
- **Describe each score level as a situation** that can be recognised on its own. Levels are
  judged separately, so "worse than the level before" means nothing. One dimension per score.
- **Describe options that are easy to confuse**, in parallel terms: what each covers, what it does
  not, and examples that look like your real inputs.
- **Say exactly what you mean.** Jev answers the words, not the intent. Avoid double negatives and
  criteria that contradict the instructions.
- **Treat the state as untrusted.** Text inside it can try to steer the answer; make criteria
  explicit and test with hostile inputs when the stakes are high.

Reading the answers:

- A noul near 0.5 means "cannot tell", not "somewhat". Route such cases to a person
  (`--abstain-band`) rather than guessing.
- `confidence` measures how peaked a distribution is, not how likely the answer is to be right.
  Two acceptable options give a low confidence that is not a problem.
- Answers vary slightly between calls. Never compare exact probabilities, and never reuse a noul
  threshold for a choice or the other way round.
- Tune thresholds on the person's own examples. Keep the raw probabilities and apply the policy in
  code, so the policy can change without asking again.
- Pin a versioned model (`--model jev-1.13.0`, see `jev models list`) for anything repeatable:
  aliases such as `jev-latest` move to new versions without notice.
- A `jev` installed by the install script updates itself, at most once a day and never during a
  command. `jev version -o json` says whether it does (`auto_update`). Where the `jev` version must
  not change, set `JEV_AUTO_UPDATE=false`; with `CI=true` it is already off.

## Safety and cost

- The key is never an argument, and `jev` never prints it. Keep it that way: no `set -x` or
  `env` dumps around `jev` calls, and no key in files or messages.
- The state is often customer data. Do not pass `--debug-bodies`, and do not copy states or
  answers into logs, issues or chat without a reason.
- Only input tokens are billed. `cost_usd` and every size in `--dry-run` output are estimates.
- `jev` retries rate limits and server errors itself; do not wrap it in another retry loop for
  exit 2, 3 or 4, which will fail the same way again.
