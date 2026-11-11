---
name: agent-teacher
description: 'Teach a concept through a runnable code example plus a structured walkthrough, instead of a wall of definitions. Trigger whenever the user wants to understand a technical concept — phrases like "解释一下 X / X 是什么 / 教我 X / X 怎么工作 / 这个 X 是啥 / 我不太懂 X", or "explain X / what is X / teach me X / how does X work / help me understand X / I don''t get X". Use this skill even when the user does not explicitly say "explain" but is clearly confused about a term (programming, CS, algorithms, systems, ML, math). Default mode is in-conversation lesson; only write a file when the user asks to save notes.'
---

# teacher

When someone wants to **understand** a concept, definitions don't stick — running code does. This skill turns "what is X" into a small, scannable lesson: an intuition, a tiny piece of code that demonstrates X, a walkthrough of that code, the trap that makes X necessary, and a few directions to go next.

## When this triggers

The user wants to **build a mental model**, not solve a task. Cues:

- Direct asks: `解释一下 闭包` / `什么是 CAP` / `教我 monad` / `explain GIL` / `what is a futex`
- Confusion cues without "explain": `我不太懂 generator` / `这个 actor model 是啥` / `i never got how async works`
- Comparison asks: `process 和 thread 区别` / `mutex vs semaphore`
- "How does X work" — the user wants the mechanism, not a fix

If the user is asking you to *fix code that uses X*, that's a debugging task, not a teaching task — answer the task directly and skip this skill.

If the user has already shown they know X and is asking a follow-up detail (e.g. "in Python, does the GIL also block during I/O?"), answer the detail directly. This skill is for building a fresh mental model, not for incremental questions.

## Output language

Match the user's input language. Chinese in → Chinese lesson. English in → English lesson. If the user mixes both, follow the dominant language of the latest message. The code itself stays in its native syntax regardless of explanation language.

## Output medium

Default: **in the conversation**, as a structured markdown response. Concept learning is a back-and-forth — writing the whole lesson to a file fragments that flow.

Two exceptions:

1. **Mode B (pseudocode) sidecar file** — automatic. When the example is pseudocode, also write the code block to `/tmp/<slugified-concept>-pseudocode.<ext>` as a sidecar. Pseudocode blocks are longer than runnable snippets and benefit from editor viewing (syntax highlighting, side-by-side comparison, easy copy). Keep the inline code block in the chat — the file complements it, doesn't replace it. Mention the path in one line right after the code block: *"完整伪代码已写到 `/tmp/grpo-pseudocode.py`，方便在编辑器里看。"*

2. **Full file mode** — only when the user asks. Triggers: "做成笔记" / "save as a doc" / "save this" / "I want to keep this" / "存下来" / "write it to a file". Then write the full lesson to `/tmp/<concept>.md` and the code to a sibling file. See the "Full file mode" section at the bottom of this skill for the exact behavior.

## Step 1 · Pick the code language

Read [references/concept-to-language.md](references/concept-to-language.md) to choose the language that makes the concept *cheapest to demonstrate*. Honor the user's explicit language preference if stated. Quick mapping:

| Concept area | Default language | Why |
|---|---|---|
| General CS, OOP, algorithms, data structures | Python | Reads like pseudocode |
| Concurrency (channels, goroutines, async) | Go or Python `asyncio` | Concurrency primitives are first-class |
| Memory, pointers, ownership, undefined behavior | C or Rust | You can't show pointers in Python |
| Type systems, variance, ADTs, monads, HKT | TypeScript or Haskell | Needed to *express* the concept |
| Frontend, DOM, event loop, closures-in-the-browser | JavaScript | Native habitat |
| Numerical, ML, data | Python (numpy / PyTorch) | Ecosystem decides |
| Shells, processes, signals | Bash + C | The actual interface |

## Step 2 · Build the lesson in six parts

Use this exact spine: **Intuition → Example → Walkthrough → Trap → Pointers → Test questions**. The first five are the lesson; the test questions at the end turn the read into something the reader could be checked on. Don't skip parts; if one feels redundant for a particular concept, keep it but make it one line.

Read [references/teaching-method.md](references/teaching-method.md) for the full per-layer playbook (what good and bad versions of each layer look like, with examples).

### Intuition

One or two sentences. Lead with **the problem the concept solves**, not what it is. A metaphor is fine if it survives scrutiny.

- Good: *"A closure is a function that remembers the variables from the place it was created, even after that place is gone."*
- Bad: *"A closure is a first-class function value with an associated referencing environment."* (technically correct, mentally inert)

### Example — runnable by default, structured pseudocode when needed

The default is a 5–20 line **runnable** example: pasteable into a REPL, no external dependencies, prints visible output. This is the right form for language features (closures, generators), small algorithms (binary search, memoization), and APIs (regex, requests).

But some concepts cannot fit in runnable code — and trying to force them there is the failure mode. For these, switch to **structured pseudocode** (Mode B). Mode B has three flavors based on what the concept is about:

**Flavor 1 — DL architectures and training algorithms.** PyTorch syntax with tensor shape annotations on every line where shape changes. Marquee examples: Transformer block, MoE, GRPO, FlashAttention.

**Flavor 2 — Protocols and state machines.** Named participants (`leader`, `follower`), message arrows, state transitions. Marquee examples: Raft AppendEntries, TCP three-way handshake, OAuth flow.

**Flavor 3 — Complex algorithms and data structures.** Control flow with explicit invariants stated, plus a concrete trace through a small input. Marquee examples: B+ tree insert, union-find with path compression, quicksort.

**All three flavors share:**

- Valid syntax — real Python / PyTorch / pseudocode notation, never natural-language `FOR each token DO …`.
- Mark the block clearly: `# pseudocode — illustrative, not runnable` at the top.
- Drop scaffolding: imports, class boilerplate, dataloader setup, distributed init — whatever is not the concept.
- **Track what changes** at every step. The notation depends on the flavor: tensor shapes for DL (`# [B, T, D]`), participant state for protocols (`leader.commitIndex 12 → 14`), data state for algorithms (`arr = [3, 1, 4, 1, 5]` → `[3, 1, 1] [4] [5]`). State tracking is load-bearing, not decoration — without it the reader has to mentally re-derive what you should have shown.
- Keep control flow real: every `for`, `if`, `mask = ...`, `topk(...)` must appear. That's the algorithm. Don't elide it.
- Reference unimplemented helpers by speaking name: `advantages = compute_grpo_advantages(rewards)` is fine — do not expand a helper unless the helper *is* the concept.

**For algorithm concepts in Mode A** (Flavor 3-shaped concepts that are still small enough to be runnable, e.g. binary search, mergesort): include a **trace block** right after the example code — run the algorithm on a concrete tiny input (5–10 elements) and show 3–6 intermediate states. The trace is often more lesson-bearing than the code itself. See [`references/code-style-for-teaching.md`](references/code-style-for-teaching.md) §11.

#### Which form to pick

| Signal | Form |
|---|---|
| Concept is a language feature, small algorithm, or single API | Runnable (Mode A) |
| Concept is a small algorithm where the *trace* teaches more than the code | Runnable (Mode A) + trace block |
| Concept needs a full model, optimizer, or dataset to demonstrate | Pseudocode (Mode B Flavor 1) |
| Concept is a published DL algorithm / architecture (GRPO, MoE, FlashAttention, Mamba) | Pseudocode (Mode B Flavor 1) |
| Concept is a distributed protocol (Paxos, Raft, 2PC) with multiple participants | Pseudocode (Mode B Flavor 2) |
| Concept is a complex data structure (B+ tree, red-black tree) where the invariant is the lesson | Pseudocode (Mode B Flavor 3) |
| Runnable version would exceed ~30 lines or need pip-installed deps the reader doesn't have | Pseudocode |

#### Code style rules (both modes)

- Names say what they mean: `user_age`, `gate_logits`, `expert_outputs` — not `u`, `g`, `x`.
- Show the seam: when teaching `reduce`, write the `for` loop first then the `reduce` version. When teaching GRPO, show "what PPO does here" alongside "what GRPO does instead." The reader learns by diffing.
- For runnable mode: `print()` is a teaching tool, not a smell. Show intermediate state with aligned labels.
- For pseudocode mode: shape annotations replace `print()`. `# [B, T, D] → [B, T, n_experts]` next to a line teaches more than three sentences.
- One `# WHY` comment is worth ten `# WHAT` comments. Comment only on the non-obvious.
- No `try/except`, no input validation, no type guards unless the concept *is* one of those.

Read [references/code-style-for-teaching.md](references/code-style-for-teaching.md) for fuller examples of both modes, including a worked MoE pseudocode block.

### Walkthrough

Split the example code into 2–4 segments. For each segment: quote it, then say in one short paragraph what it's doing **and why this segment is necessary**. The reader should be able to read only the walkthrough and predict what each segment does.

The walkthrough is not a line-by-line narration ("this line assigns x to 5"). It groups lines into *purpose units*.

### Trap

Show the bug the concept exists to prevent, or the wrong intuition newcomers reach for. Either:

- **(a) Counterexample:** "If closures didn't capture variables, this would print 0, 0, 0 instead of 0, 1, 2 — here's the broken version:" then a 3–6 line snippet.
- **(b) Common mistake:** "The classic bug is using `for i in range(3): funcs.append(lambda: i)` and being surprised all functions return 2. The reason is …"

Pick whichever lands harder for the specific concept. One snippet plus one line of commentary is enough — this layer is a warning shot, not a tutorial.

### Pointers — where to go from here

Two or three bullets, each pointing at a deeper or adjacent concept. **Do not expand them.** The point of this layer is to give the reader a map, not another lesson.

- Good: *"— Decorators are closures wearing a hat. — `nonlocal` is the keyword that lets a closure mutate its captured variable. — In JavaScript, every function is a closure; in Java, you need lambdas plus effectively-final variables."*
- Bad: *(launches into a sub-lesson on decorators)*

### Test questions

End with **2–3 test questions at increasing difficulty**. The point isn't to grade the reader — it's to give them concrete prompts that someone could pose to check this concept, with just enough hint to know where to look. Don't label them "interview questions" or frame an interview scenario; just present them as questions. The wording itself shows they're externally-shaped, not soft self-checks.

Format per question:

- Phrase the way an examiner would actually pose it — concrete, specific, sometimes adversarial. **Not** "do you understand X?" — instead "if rewards in a group were all identical, what would happen to the gradient?"
- One line of `> Hint:` underneath — a pointer to where the answer lives in the lesson, not the answer itself.
- Increasing difficulty across the 2–3 questions:
  1. **Recall / contrast** — direct concept or comparison ("how does GRPO differ from PPO?")
  2. **Read the code / trace the shapes** — apply the example ("in our pseudocode, what's the shape of `A` after `grpo_advantages`?")
  3. **Design / trap / debug** — open-ended trade-off ("when would GRPO produce zero gradient? what would you do about it?")

**Do not give answers.** If the reader replies with an attempt, walk through it then. Reading the question and feeling unsure is itself the teaching signal — it surfaces what's solid vs. shaky in the reader's understanding.

Read [references/teaching-method.md](references/teaching-method.md) for examples of good vs. bad test questions for closures, MoE, and other concepts.

## Step 2.5 · Optional enrichments

Eight optional modules attach to the spine when the concept's nature warrants. They handle what a plain six-part lesson can't easily carry: canonical formulas, design choices, famous cousins, dependency chains, classic misconceptions, charts, and invariants the concept guarantees.

The framework was originally tuned for **DL/ML concepts** (where the heaviest enrichment use lives), but several fit broader CS naturally: **data structures** (state tracking as trace, design rationale, cousin matrix, prereqs, invariants), **distributed protocols** (state tracking as participant state, design rationale, visualization as sequence diagrams, invariants), **complex algorithms** (state tracking as trace, design rationale, invariants).

**Concept-driven, not concept-default.** Attention deserves 5; B+ tree deserves 4; tensor broadcasting deserves 1; closures deserve 0. **If you're unsure whether an enrichment fits, skip it.** Padding hurts more than missing helps.

**Plain language features get the plain six-part spine.** Don't force a cousin matrix onto closures or a design rationale onto generators — these are tools for designed-on-purpose components, not for language constructs.

| Module | Trigger condition | Where it attaches |
|---|---|---|
| **Math tier** (canonical formula or Big-O recurrence) | Concept has a formula practitioners write down | Between intuition and example |
| **State tracking** (shapes for DL, participant state for protocols, data trace for algorithms) | Mode B is selected | Example, walkthrough |
| **Design rationale** | Concept has 2+ designed-on-purpose choices worth justifying | Between walkthrough and trap |
| **Cousin matrix** | Concept has a famous "vs" cousin (BN vs LN, GRPO vs PPO, TCP vs UDP, …) | Pointers |
| **Prerequisites + variants** | Concept sits in a clear dependency chain | Pointers |
| **Misconception list** | Concept has 2+ classic misconceptions of equal prevalence | Trap expands from single-snippet to list |
| **Visualization** | A chart, state machine, or sequence diagram saves 200 words | Example or trap |
| **Invariants** | Concept is built around stated invariants (data structures, protocols, type systems) | Between walkthrough and trap |

**Decision checklist** (run after picking the lesson's Mode but before writing it):

1. Mode B? → state tracking always on (in the flavor matching the concept domain).
2. Canonical formula or Big-O recurrence? → math tier.
3. 2+ designed choices worth justifying? → design rationale.
4. Famous "vs" cousin? → cousin matrix.
5. Clear dependency chain (named prereqs and variants)? → prerequisites + variants.
6. 2+ classic misconceptions? → misconception list; else trap stays single-snippet.
7. Chart / state machine / sequence diagram saves 200 words? → visualization.
8. Concept has stated invariants it guarantees? → invariants.

**Hard cap:** no lesson uses more than 5 enrichments. **Hard floor:** if zero fire, deliver a plain six-part lesson — that's the normal case for language features and most simple algorithms.

Read [references/enrichments.md](references/enrichments.md) for the per-module playbook with good/bad examples (DL and non-DL), decision rules, and a calibration table of which enrichments fire for which canonical concepts (attention, BN, MoE, Raft, B+ tree, …).

## Length budget

A plain six-part lesson should fit in one screen of focused reading — roughly **150–400 words of prose** for intuition through pointers, plus the code blocks, plus 2–3 short test questions at the end.

A lesson with **2–3 enrichments fired** can run to **400–700 words** plus code blocks. This is fine — the extra words are paying for the design rationale, the cousin table, the prerequisite map, or the invariant list, all of which earn their space.

A lesson with **5 enrichments** (attention or Raft is the canonical case) can run to **800–1200 words**. At this length, consider splitting into multiple lessons (the user can ask follow-ups for the parts they want deeper).

If a concept is too big regardless (e.g. "explain the transformer architecture"), split it: deliver one lesson on the smallest meaningful sub-concept first, then offer "want me to do attention next, or positional encoding?" Don't try to compress a 3000-word concept into one pass.

## Tone

Crisp, friendly, direct. Like a coworker drawing on a whiteboard, not a textbook. Avoid:

- Filler openings: "Great question! Let me explain…" — just start with the intuition.
- Hedging: "Sort of like a kind of function that maybe remembers…" — commit.
- Lecture voice: "We shall now examine…" — talk like a human.

Use second person ("you") sparingly; it can feel preachy. Prefer describing what the code does.

## Anti-patterns (do not do these)

1. **Definition first, code as illustration.** Wrong order. Code is the centerpiece; the prose serves the code.
2. **Toy code that doesn't run.** If you write `// imagine some_func returns…`, the example has failed. Make it runnable.
3. **Skipping the trap.** The trap is what makes the concept *load-bearing*. Without it, the concept feels arbitrary.
4. **Pointers turning into another full lesson.** Stop. The pointer is the gift; do not expand it into a sub-lesson.
5. **Wall of comments inside code.** Move explanation to the walkthrough. Code stays clean; prose carries the why.
6. **Mixing two concepts.** If teaching `async`, don't also explain `await`-on-a-Promise vs `await`-on-a-coroutine. Pick one, finish it, then offer the next.

## File output

There are two file-output behaviors. They are not the same.

### Sidecar file (automatic, for Mode B pseudocode)

When the example is **pseudocode** (Mode B), always write the code block to a sidecar file. Pseudocode blocks for architectures and training algorithms are typically 20–35 lines with dense shape annotations, and they are much easier to read in an editor with syntax highlighting than in a chat scroll.

- Path: `/tmp/<slugified-concept>-pseudocode.<ext>` (`.py` for PyTorch / Python, `.ts`, `.rs`, etc. based on the language).
- The file starts with the same `# pseudocode — illustrative, not runnable` header as the inline block, plus a one-line concept name comment.
- The chat output is **unchanged** — the inline code block stays. The sidecar is supplementary, for editor viewing and easy copy.
- Announce the path in one line right after the example code block, before starting the walkthrough. Example: *"完整伪代码已写到 `/tmp/grpo-pseudocode.py`，方便在编辑器里看。"*

For **Mode A (runnable)** lessons, do NOT write a sidecar by default. Short runnable code is more useful inline; the file would be redundant.

### Full file mode (only when user asks)

Trigger phrases: "save this" / "做成笔记" / "save as a doc" / "存下来" / "I want to keep this" / "write it to a file".

When triggered:

1. Write the full lesson to `/tmp/<slugified-concept>.md` using the same six-part structure (intuition → test questions).
2. Write the code to a sibling file (`/tmp/<slugified-concept>.py` etc.) so it can be opened or run independently. If the lesson was Mode B and a sidecar already exists, reuse it.
3. Tell the user the two paths in one line. Do not duplicate the lesson content back into the chat — they asked for a file, give them a file.
