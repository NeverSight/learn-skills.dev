---
name: typesafe-ask
description: Answer named questions (noul, choice, score) about a text with `typesafe ask` and System One models - write the questions file in JSON or YAML, use question flags, run batch mode over many states, and set request options. Use when the user says "evaluate this text with these questions", "classify this message with typesafe", "typesafe ask", "score this text", "run typesafe over a file of states" or "questions file".
license: MIT
compatibility: Needs the typesafe-unofficial-cli package (Python 3.14+) and a key from `typesafe auth login` or TYPESAFE_API_KEY / OPENROUTER_API_KEY. Each request is billed by the provider.
---

# typesafe ask

`typesafe ask` evaluates a text (the *state*) against named questions. Setup,
login and profiles are in the `typesafe-cli` skill; the key must already
exist. Each request is billed, so do not loop over many states without being
asked to.

## Rules

- Global options go before `ask`: `typesafe -o json ask --state ...`.
- Start from the template instead of writing a file by hand:
  `typesafe ask --questions-template yaml` (or `json`) prints a valid file.
- `instructions` is required on every question (OpenRouter answers 400 without
  it).
- `choice` criteria is an **object** of label to description; `score` criteria
  is an ordered **list** of level descriptions from zero; `noul` criteria is
  optional, an object with the keys `true` and `false`.
- Use `-o json` when the answer will be processed.

## Question types

- `noul`: yes/no.
- `choice`: pick one label.
- `score`: pick a level (index into the list).

## Ways to define questions

File (JSON, or YAML by `.yaml`/`.yml` extension; `-` reads standard input):

```bash
typesafe -o json ask --state "I was charged twice." --questions-file questions.yaml
```

Flags, alone or beside a file (a flag replaces a file question of the same name):

```bash
typesafe -o json ask --state "I was charged twice." \
  --noul 'billing=Is this billing?' \
  --choice 'tone=What is the tone?' \
  --criterion tone=calm --criterion 'tone=angry:Hostile or upset' \
  --score 'urgency=How urgent is it?' \
  --criterion urgency=low --criterion urgency=high
```

## The state

- `--state TEXT`, or `--state-file PATH` (`-` is standard input).
- `--state-format text|json` (default `text`) parses it as plain text or as a
  JSON object/array.
- Batch: `--states-file states.jsonl` (one JSON value per line) with
  `--concurrency N` (default 4). Do not combine with `--state`/`--state-file`.

## Request options

`--timeout SECONDS`, `--max-retries N`, repeatable `--header 'Name: value'`,
`--extra-body FILE` (JSON or YAML object of extra top-level fields),
`--model NAME` (default: the profile's, else `jev-latest`). The request id
goes to stderr and is a `request_id` field in the records.

## References

- [Questions file format and YAML rules](references/questions-file.md)
- [Batch mode](references/batch.md)
- Exit codes: `typesafe-cli` skill, `references/exit-codes.md`. A usage error
  (2) means nothing was sent.
