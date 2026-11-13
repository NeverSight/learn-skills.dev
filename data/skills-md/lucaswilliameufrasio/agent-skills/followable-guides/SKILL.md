---
name: followable-guides
description: >-
  Write a tutorial or passo a passo that a person can follow in order and
  finish without inventing a missing step. Use when asked to document a
  procedure, runbook, how-to, setup guide, or the exact steps that just worked,
  including "documente o passo a passo" and "como fazer do jeito que deu certo".
---

# Followable guides

Write the procedure the person will execute next time. Keep the voice of the
messages that already got them through it: short, in their language, one action
then the line they must see before continuing.

Store the finished guide in the repository that owns the system, next to the
command it runs. This skill does not keep one site's addresses, names, or
topology. Use the values verified in the target repository.

## Shape

1. Open with what the procedure produces and the condition that has to be true
   before the first command. Two or three sentences.
2. Number the steps in execution order. One step is one action, the exact
   command, and the answer to each prompt.
3. Put the command in a fence, complete enough to paste. Say where the secret
   comes from and that it is typed at the prompt. Leave the value out.
4. Before a confirmation that changes the system, quote the summary line that
   must appear and the reply that stops when it does not. The stop reply is
   part of the step.
5. Say what this step writes and what it leaves for a later step.
6. Close with the successful output and how to read it, including a state that
   looks idle and is still correct.

Write in the reader's language. Prefer the words already used in the session
and in the project's docs. Keep sentences short. State the safe condition
inside the step that needs it.

## When a run stops

The next message is still a step, not a lab report.

- Say whether anything was written. Tie that to a line that did or did not
  appear.
- Name the cause in one sentence, in the words of the tool's error.
- Give the same command again. Repeat only the answers that stay. Quote the
  summary line that must appear this time.

After it succeeds, fold the working path into the guide. Leave the failed
attempts out of the numbered steps. Keep the check that avoids the failure at
the point where the person decides.

## Example

The command records the limit and shows a summary before it writes. Run it from
the machine that already reaches the service.

```sh
tool apply --host 192.0.2.1
```

At the target prompt, press Enter. The summary must show `target 192.0.2.1`
and `network 203.0.113.0/24`. Enter applies. If the target is anything else,
answer `n` and stop. The command writes the limit. It does not move traffic.
That happens in the next step, after the summary names the standby path.

## Before handing it over

Read the guide once as someone who has only that page. Every prompt has an
answer. Every confirmation has the line that must appear. The last section
shows the output that means it finished. No secret value is in the page.
