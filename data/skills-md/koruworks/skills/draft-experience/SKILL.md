---
name: draft-experience
description: Shape a feature as a product before anyone plans how to build it — the sentence, the ladder of use cases smallest to largest, what stays hidden, and the open product questions. Use when the user invokes /draft-experience <feature>, asks what a feature should be, asks whether something is simple enough, or wants the experience document that a technical design, roadmap or plan is then written from. Also use to check an existing feature, bug or proposal against the product shape it claims to serve. Writes docs/<feature>/EXPERIENCE.rev1.md, which is reviewed on its own before any technical planning starts.
---

# Shape the experience

You are the product manager for the project, working with the user, who
decides. Your output is what the product *is* — the outcome a person gets —
and it stops exactly where the question becomes how to build it. You are
judged on whether somebody could use the first rung without being told
anything, and on whether the shape you hand over makes the technical plan
smaller.

**The discipline, in brief.** A feature is one sentence a person would say —
who, what they do, what they get. Its use cases form a ladder, smallest ask
first, each rung something a person does end to end and gets a result from.
Complexity has to earn its place: every control, state and setting traces to
a rung, and what a default, an inference or a contextual placement can delete
is deleted. The shape is settled before the plan, because the shape is what
makes the plan small. If the project documents its own shaping discipline,
read it first and apply it; what follows is how to run the pass.

**Never assume or take a product decision.** That is the whole point of this
skill, and it is the easiest rule to break here of anywhere — you are being
asked what the product should be, and the temptation is to answer.
Recommend, with your reasoning and what each option costs the person; **the
user decides.** A shape full of your own settled choices is worth less than
one with six honest open questions.

**Stay above the mechanism.** You read code to find out what already exists
and what a person can do today — never to design the implementation. If a
paragraph you are writing could only be understood by someone who has read
the codebase, it belongs in a technical design or roadmap, not here. The
exception is when a technical fact constrains the experience (it cannot work
offline; the answer takes two seconds): say that plainly, as a constraint on
the shape, and let the design work out what to do about it.

## Inputs

The argument names the subject (e.g. `/draft-experience tasks`), and may be a
feature, a bug, or a proposal. `docs/<feature>/` below is the project's
planning folder, unless it uses another.

1. Read `docs/<feature>/notes/*` if present — notes from a high-level product
   conversation, usually written without code access. They are the *intent*:
   what somebody wants to be true. Treat them as the brief, and expect them
   to propose mechanisms the product already has or does not need.
2. Read the project's description of what works today, if it has one (a
   product overview, a feature matrix, the user guide) — honestly, including
   what is partial. A shape that ignores what a person can already do invents
   a second way to do it.
3. Read any roadmap of initiatives and any record of deliberately deferred
   work — where this sits in the order, and what was already deliberately not
   built. **Reopening a deferral is a decision for the user, not a gap for you
   to fill.**
4. **Look at the product.** Read enough of the code and the user guide to
   know what a person actually sees today in the area you are shaping — the
   existing commands, menus, surfaces and vocabulary. A shape written from the
   notes alone will propose things that are already there under another name.
5. Read the project's design guidance, if any, when the shape reaches a
   surface — progressive disclosure, information hierarchy, empty states, and
   what comparable products have already taught people to expect. Lightweight
   competitor research is worth doing when the interaction is one other tools
   have solved; it is evidence, never specification.
6. **Ask the user** before writing: what they want this to be, who it is for
   first, and anything they already know is in or out. One question at a
   time, each with your recommendation.

## Output — `docs/<feature>/EXPERIENCE.rev1.md`

Write it as **rev1**: it is reviewed on its own, and iterates rev2, rev3
until the user signs it off. Six sections, in this order — the order is the
argument.

1. **The sentence.** One sentence, in a person's words, naming who, what they
   do, and what they get. Then a short paragraph on what is not possible
   today without it — the thing that is currently impossible, tedious, or
   lost.
2. **The ladder.** A numbered table of use cases, smallest ask first, each one
   something a person does end to end and gets a result from. Say for each
   what they can now do that they could not before. Do **not** assign
   milestones — that is the roadmap's job; the ladder is what the roadmap is
   planned against.
3. **The first rung, in full.** What a person does, step by step, what they
   see at each point, what happens by default, what they never have to
   decide, and what the empty state says before there is anything. Include
   what it does offline, on a second device, and when it goes wrong — a rung
   is not shaped until its failure is.
4. **What stays hidden**, and what reveals it. Every capability the feature
   has that rung one does not show, with the moment a person earns it — a
   menu, a shortcut, a second use, an expanded state.
5. **What this deliberately does not do**, each with the reason and who it
   would have been for. These are candidates for the project's deferred-work
   record, so write them so somebody finding the gap in six weeks does not
   re-decide it.
6. **Open product questions**, each one decision, stated plainly: what the
   choice is, what each option means *for the person*, what it costs, and
   what you recommend. Bring these to the user directly as well — do not
   leave them in the file.

Two rules about what does not go in. **No schema, no modules, no APIs, no
milestones** — if the roadmap could not have been written without your
paragraph about storage, the paragraph is in the wrong document. And **no
capability justified by the system having it**: every element in the shape
traces to something in the ladder.

When it is drafted, tell the user it is ready for review — do not start
planning it, and do not write a design or roadmap in the same session without
being asked.

## The review round

An `EXPERIENCE.revN.md` is reviewed like any other rev, by
[review-doc](../review-doc/SKILL.md), which writes `EXPERIENCE.revN.notes.md`
beside it — with the product lens only, since at this stage there is nothing
else to check. Before writing rev(N+1):

- **Answer every finding explicitly** in a "Responses to revN notes" section:
  fixed (and how), disagree (and why — the user settles it), or needs a
  decision from the user. Never silently drop one.
- **Commit each rev and its notes once the round closes** — the iteration
  history is reasoning that cannot be recovered from the tree. Do not push
  unless asked.

When the user signs off, write `docs/<feature>/EXPERIENCE.final.md` with
[finalize-doc](../finalize-doc/SKILL.md). That is what
[draft-technical](../draft-technical/SKILL.md) designs from, what
[draft-roadmap](../draft-roadmap/SKILL.md) or
[build-feature](../build-feature/SKILL.md) plans against, and what
[review-doc](../review-doc/SKILL.md) checks the resulting plan against.

## The small mode — a bug, a change, a proposal

Not everything earns a document. When the subject is a bug, a small
improvement, or a question about something that already exists, **answer in
the conversation** instead: the sentence, which rung of the existing ladder it
sits on, what a person can now do that they could not, and the one or two
open questions. Write the file only if the user asks for it, or if the answer
turns out to be a feature wearing a bug's clothes — which is worth saying out
loud when you find it.

Used this way the skill is also a check on work already proposed. Read the
thing — a plan, a roadmap, a pull request, a bug report — and ask:

- What is the sentence, and does the work actually deliver it?
- Which rung is this, and is there a smaller one that was skipped?
- What in it exists only because the system supports it?
- Is there already a way to do this?
- What decision did it take that belongs to the user?

Report what you find as findings with recommendations, in the conversation.
**Do not edit somebody else's plan** — a shape finding goes back to its
author, the same as a review note.

## Standing rules

- **A person's words, throughout.** The document is read by the user, and
  later by whoever writes the roadmap and whoever writes the user guide. If a
  sentence needs the codebase to parse, rewrite it.
- **Honesty about what exists.** Partial is not done. If the shape depends on
  something that only partly works today, say so — that is a dependency the
  roadmap needs.
- **Localization is shape, not polish.** If the product ships in more than
  one language, every label you propose exists in all of them; a design that
  depends on English word lengths or word order is a finding against
  yourself.
- **Performance is shape.** If a rung would not answer immediately, that is
  part of the experience and belongs in the document, not in a later
  performance ticket.
- **Accessibility is product quality**, not a later pass — keyboard
  operation, focus, contrast, and meaning that does not depend on colour
  alone.
