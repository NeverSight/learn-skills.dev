---
name: commit-discipline
description: >-
  Write commit messages as a single line with a conventional type prefix, the way they actually get written here. The default shape is `type: what changed` on one line, lowercase after the colon, no trailing period, no body. Pick the type from feat, fix, refactor, chore, docs, and style. When one commit genuinely does several things, name each of them in that one line rather than picking one and letting the rest hide in the diff. A body is the rare exception and needs a reason. Never attribute a commit to an AI tool. Use this whenever a commit message is being drafted or reviewed, in any repository, including deciding which type prefix fits, whether a body is warranted at all, how to word a commit that bundles several changes, and whether a message is too vague to be useful six months later.
metadata:
  author: zaidmukaddam
---

# Commit discipline

A commit message is the only part of a change that survives being skimmed months later, when nobody is going to re-read the diff. Its job is to say what happened precisely enough that the diff is optional.

## The default shape

One line. A conventional type prefix, a colon, then what changed in lowercase. No trailing period, no body.

```
feat: add microsoft oauth login
fix: correct model reference for scira codex
refactor: streamline sidebar state management
chore: bump deps
```

Roughly four in five commits look exactly like this, and the ones that do not are the exception rather than a second style.

**The types, in the order they actually get used:** `refactor`, `feat`, `fix`, `chore`, `docs`, `style`. If a change does not fit one of those six, the problem is usually that the commit is doing two things.

**Lowercase after the colon.** This is near-universal in practice, and mixing cases across a history makes the log look like two people wrote it.

**A scope is optional.** `fix(auth):` is fine when the area is not obvious from the subject, and unnecessary when it is.

## When there is no prefix

A plain sentence with no prefix is still legitimate, and about half of real history looks that way. The rule that matters is consistency within a repo: match whatever the log already does.

When a message goes without a prefix, **capitalize the first word**. `Add Microsoft login, update deps, improve scroll logic`. The capital is what replaces the prefix as the visual start of the line, which is why prefixed messages do not need it and unprefixed ones do.

## Name everything the commit does

When a single commit genuinely does several related things, name each of them in that one line, joined by commas or "and," rather than picking the most important one and letting the rest hide in the diff.

`fix: correct discount gating and update deps` beats `fix: various fixes`. A reader scanning history should be able to tell what a commit touched without opening it. This matters most for behavior changes that are easy to lose: a pricing rule, an auth path, anything a customer could notice.

This rule governs what the message says once the commit's boundary is decided.

## The body is the exception

Most commits do not have one, and reaching for a body by default is the most common way these messages go wrong. Add one only when the single line genuinely cannot carry the change: several distinct sub-changes that would flatten into something vaguer, or a behavior change whose reason will not be obvious later.

When a body is warranted, make it a bulleted list, one complete past-tense sentence per bullet. Where the subject reads as an instruction ("add," "fix"), body bullets read as a report of what was done ("added," "fixed"), because by the time someone reads the body the change is a fact rather than a plan.

A body that restates the subject in more words is worse than no body.

## Match the weight of the message to the weight of the change

`chore: bump deps` is a complete message. Terseness on a trivial change is proportion, not laziness.

The failure is applying that terseness to something that was not actually trivial, which loses the same information as a vague message dressed up with a prefix.

## Never attribute a commit to a tool

No `Co-Authored-By` trailer for an AI tool, no "Generated with" line, in the subject, the body, or anywhere else. `Co-Authored-By` is for a real second person who contributed to that commit, never for whatever wrote the code.

## Using this well

**This governs wording, not whether a commit should exist.** A precisely worded message around the wrong split of work is still the wrong split, described accurately.

**Precision is downstream of having read the diff.** A specific message is not a wording exercise performed after the fact. A vague one usually means the diff was not read closely, not that the writer needed a better template.

**The prefix is not a substitute for saying what happened.** `chore: updates` and `fix: bug` clear the format bar and carry no information. The prefix is the cheapest part of the message to get right and the least useful on its own.

**Propose it, do not fire it.** Drafting the message is not the same action as creating the commit. Show the message and let it be reviewed before committing, unless that has been agreed as automatic.
