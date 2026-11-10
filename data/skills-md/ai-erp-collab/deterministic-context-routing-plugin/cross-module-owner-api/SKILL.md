---
name: cross-module-owner-api
description: Use when a task in the active module needs a rule owned by another module (for example access rules, a hierarchy walk, status transitions), or the user asks whether such a rule exists or says to reuse or extend another module. Finds the owner, keeps the rule behind an owner API, and links consumer and owner.
---

# Cross-Module Owner API

The **consumer module** is the active module where the task started.
The **owner module** is the module whose domain the rule belongs to.
The **owner API** is a small public method set in the owner module that
the consumer calls instead of copying the rule.

## 1. Mode: question or command

- **Question** ("do we already have access rules for documents
  somewhere?"): look, report, and propose. Do not change code in the
  owner module.
- **Command** ("look at module X and add a helper there", "reuse what X
  has"): you may change the owner module within the scope of the
  command.
- Never enter another module on your own initiative. If the task seems
  to need one and the user said neither, ask.

## 2. Lookup order (stop at the first hit)

1. Consumer links: the consumer's knowledge-base pages and module
   `AGENTS.md` may already link to an owner contract page.
2. Named module: if the user named the module, go to its
   `knowledge-base/modules/<owner>/INDEX.md`.
3. Registry: otherwise resolve the candidate owner in `modules.md`, then
   read its `INDEX.md`.
4. Owner contract, usage, and table pages linked from that `INDEX.md`.
5. Owner source code, only if the knowledge base lacks the fact.

Report which step produced the answer.

## 3. Record the link in the consumer

Do this only when the owner rule is taken into work: a command, or the
user decides to reuse the rule. A plain question leaves no trace in the
consumer; the user may have asked for reasons that have nothing to do
with this module.

Add a link to the owner contract page in the consumer's usage or concept
page. If every future task in the consumer should know it, also add one
line under `## Cross-Module Links` in the consumer module `AGENTS.md`.

## 4. Change, mark, and check the owner (command mode only)

Before writing anything into the owner module (code or knowledge), read
`references/owner-changes.md` and follow its three steps in order:

1. Change the owner: add an owner API, keep only an adapter in the
   consumer.
2. Mark the owner: contract page, owner, consumer, and root session logs.
3. Check: nothing owner-specific is left in the consumer.
