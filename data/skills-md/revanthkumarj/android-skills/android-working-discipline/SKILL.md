---
name: android-working-discipline
description: |
  Standing working discipline for every coding task in an Android codebase - intent-reading, layer-by-layer decomposition, effort placement, grep-backed verification, marking known vs guessed, self-attack before delivering, completeness checks, and a final gate. Use this skill at the START of any non-trivial coding task, and before delivering any code change. Trigger on any request to implement, fix, migrate, refactor, investigate, or review Android code, and on phrases like "why is this broken", "add this field", "same in the other screen", "check my change", or whenever a task spans more than one file.
---

# Standing Instructions — Working Discipline

You are working in a multi-module Android codebase: a legacy XML `:app` host plus Compose feature
modules, constructor DI, Retrofit + a reflective JSON serializer, and feature-flag-gated old/new
flows running side by side. Run these procedures on every task. They are orders, not advice.

---

## 1. Reading intent

- When a message is terse, has typos, or names a symptom ("logs not comimg", "infinite loading"), do NOT answer the literal words. Locate the concrete file/flow first: grep the named symbol, open the named file, and restate the task to yourself as "change X in file Y so behavior Z".
- When the message says "see old flow" or names a legacy file, treat the old implementation as the spec: read it, extract its exact conditions/formulas, then diff against the new flow. The task is the delta.
- When the user reports a bug in something you just changed, first suspect your own change: re-read your diff before exploring elsewhere.
- Ask exactly ONE clarifying question (with concrete options) only when BOTH: (a) two interpretations lead to editing different files or building different UI, and (b) ten minutes of code reading cannot resolve it. Otherwise pick the interpretation with codebase evidence, state it in the answer, and proceed.
- **Example:** "the starting balance field was missing in the new flow — add it" is ambiguous (a dedicated section vs. a field inside an existing "More" section; is the visibility gating from the old screen replicated or not). Two different UIs → one question with options. Guessing here builds the wrong screen.
- **Prevents:** solving the stated question instead of the real one.

## 2. Breaking problems down

- When a change spans layers, cut it along the module chain and execute in this order, each step compiling on its own:
  1. `core:network` model (request/response, serialized-name annotations)
  2. `core:models` domain model (new fields get defaults)
  3. feature `:data` mapper (`toDomain` / `toRequest`)
  4. repo interface + impl (`safeCall`)
  5. ViewModel: state field → action → handler → payload builder → edit-load
  6. Screen/component wiring (params, callbacks)
  7. Host fragment / navigation
- When a task says "X and also Y" (e.g. "in get-details and in update also"), write the parts down as separate checks before starting; verify each independently at the end.
- When touching a UI element, first grep for its every render condition in the old flow (`isVisible`, `visibility =`) — visibility rules are part of the feature.
- **Example:** adding one `starting_balance` field = 7 discrete edits (network request model, domain model, request mapper, network response model, response mapper, ViewModel payload + edit-load + state + action, and the UI section). Doing it as "one big edit" is how the mapper line gets skipped and the field silently never sends.
- **Prevents:** half-plumbed features that compile but drop data mid-chain.

## 3. Effort placement

- When you finish scoping, name the single edit whose failure is silent (no crash, no compile error) — that is where you spend the care. In a codebase like this the silent-failure points are, in order:
  1. **Shared code paths** — one function serving two flows (a `createItemPayload()` that serves create AND update; a dialog's Save bypassing a button's `enabled` guard). Before editing or relying on a guard, grep every entry point into the function.
  2. **Mappers and `?: 0.0` coercions** — they decide what actually reaches the backend.
  3. **DI resolution** — an unqualified duplicate binding of the same type swaps instances with no error.
  4. **Exhaustive `when` over enums** you extend.
- When an edit is in boilerplate (imports, preview params, spacer), do it fast; do not re-verify cosmetics.
- **Example:** an empty-name validation belonged inside `createItem()` (covers the dialog's Save *and* the button), not in the button's `enabled` — the button already had a guard; the dialog path was the silent hole.
- **Prevents:** careful work on the easy 90% while the dangerous 10% ships broken.

## 4. Verification

- When you claim "X calls Y" or "field F is sent", prove it with a grep/read in the same turn — never from memory of similar codebases. A repo like this duplicates logic (two repositories with the same method name, two DI modules with the same file name, old + new flows), so memory of one copy is not evidence about another.
- When comparing a failing request to a working one, diff **field by field in a table**; the bug is the one differing value (e.g. `user_id: 0` vs a real id), not the field you expected.
- When you need a formula or condition from old code, copy it from the source line (`unit != "NA" && unit != "OTHER"`, `stockValue = qty * purchasePrice`) — never paraphrase from recall.
- When a file read comes back truncated, never answer from that page if the answer could be further down; read the next range or grep the specific symbol.
- When you add a serialized field, verify the exact JSON key from an existing model that already sends it (old-flow request/response models are the source of truth for key names).
- **Example:** "the mapper drops the user id" was a plausible guess; the grep showed the mapper DID map it (`userId ?: 0`) — the real cause was the list endpoint returning 0. The grep prevented patching the wrong layer.
- **Prevents:** fixes aimed at the wrong layer; invented field names.

## 5. Known vs guessed

Mark every load-bearing claim in the answer with one of exactly these three forms:
- Certain: "**Confirmed** — `path/File.kt:123` shows …" (you read the line this session).
- Likely: "**Likely** — based on \<pattern/evidence\>, but I did not verify \<the missing piece\>."
- Assumption: "**Assumption** — I assumed \<X\>; verify by \<one concrete step the user can run\>."

- When a claim concerns the backend (does it reject a zero id? does it return this field?), it can never be "Confirmed" from the repo — mark it Likely/Assumption and give the verification step (usually: check the HTTP client's logged response body, or ask the backend team).
- **Example:** "the backend no-ops on a zero user id" was delivered as strong-evidence-but-unconfirmed with a revert command prepared — correct, because only a device test could confirm it.
- **Prevents:** the user acting on a guess dressed as a fact.

## 6. Self-attack

Before sending any code change, run these attacks; each is a grep, not a feeling:
- When you edited a function: grep its name; list every caller; confirm each still behaves (especially old-flow callers you didn't intend to touch).
- When you added an enum value: grep `when (` over that enum type; confirm every exhaustive `when` handles it (statement-position `when` inside a `buildList` is fine; expression-position is a compile break).
- When you added a composable param: check every call site including `@Preview`s and the sibling screen — codebases like this pair screens (a list screen and its variant screen, a settings screen duplicated per section).
- When you changed DI: check for another binding of the same type without a qualifier.
- When the attack finds something: fix it in the same turn, then re-run the same attack. If it reveals the approach is wrong (not just incomplete), say so explicitly and change approach — do not patch a broken design.
- **Example:** adding one enum entry → the attack found 4 `when` blocks and a sibling screen's call site; two needed edits, the `@Preview` needed params. Skipping the attack ships a compile error you cannot see if you cannot build.
- **Prevents:** breaking sibling flows you never opened.

## 7. Completeness

- When the request has multiple parts (commas, "also", "and", numbered items, or a follow-up "same in X"), extract them into an explicit list before working. After finishing, re-read the ORIGINAL message and tick each part against a change you actually made.
- When you consciously decide to skip a part (out of scope, better done differently), say so in the answer with the reason — never drop it silently.
- When a feature has a create path, always check whether edit/update and load paths need the same change (create/update often share a payload builder; edit-load is separate and always needs its own edit).
- **Example:** "send null AND accept null from the details endpoint" = 3 sites (payload, mapper, edit-load). Fixing only the payload passes a quick test and fails on edit.
- **Prevents:** silently dropped sub-requests.

## 8. Refusing to guess

Say "I can't verify this" and stop — instead of producing an answer — when ANY of these hold:
- The answer depends on backend behaviour, feature-flag values, or runtime state you cannot read from the repo.
- The user references an attachment/screenshot whose content you cannot see: state that you can't see it, deliver the best code-evidence-based version, and ask for the exact text/asset.
- Two implementations exist and the user's words don't disambiguate which one they run (old vs new flow) — ask, don't pick by vibes.
- A symbol you "remember" doesn't appear in grep. It does not exist. Do not use it.
- Never fill these gaps with a fluent paragraph. A wrong confident answer costs a build-test-revert cycle; "I don't know, here's how to find out" costs one message.
- **Example:** an empty-state screenshot wasn't visible → shipped a pattern-matched version AND flagged the copy/icon as unverified; the user then supplied the real asset name. Guessing the icon silently would have shipped the wrong asset unflagged.
- **Prevents:** confident fabrication.

## 9. Delivery

Structure every answer in this order, no exceptions:
1. **What changed / the answer** — one or two sentences, then a file→change table for multi-file work.
2. **Why / how it works** — the flow in plain language, referencing `file:line` for claims.
3. **Risks, caveats, and the verify steps** — what the user must check on device. Always end code-change answers with the build/run instruction and the exact user flow to exercise (if you cannot build, the user is your CI).
- When a change is speculative (a root-cause hypothesis), include the revert command in the answer.
- Keep it short: no restating the whole task, no narrating tool calls, no options you didn't take.
- **Prevents:** the user hunting through prose for the actual answer, or missing the on-device test they must run.

## 10. Fake competence — 10 failure modes, tell, counter

1. **Editing the wrong flow's copy.** Tell: grep shows two files with the same responsibility (old XML + new Compose). Counter: list both, confirm which one the user runs (the feature flag) before editing.
2. **Model field added, mapper skipped.** Tell: the new field name appears in 1–2 files, not along the whole chain. Counter: grep the field name; it must appear at every layer of the §2 chain.
3. **Remembered API that doesn't exist.** Tell: you wrote an import you never saw in a grep result. Counter: grep every helper before first use.
4. **Coercion hiding semantics.** Tell: `?: 0.0` / `?: ""` on a field whose absence means something. Counter: for every default you add or keep, state what the backend receives when the user enters nothing.
5. **"Fixed" without exercising the path.** Tell: your explanation says "should now" instead of naming the observable. Counter: give the exact log tag / screen action that proves it.
6. **DI type collision.** Tell: two providers return the same type, no qualifier. Counter: qualify both sides; grep the type name across all DI modules.
7. **Exhaustive `when` break.** Tell: you added an enum entry. Counter: grep `when` over the type (see §6).
8. **String-key drift across modules.** Tell: a fragment-result / bundle key typed twice as a literal. Counter: copy-paste the literal from the consumer's source line; note both locations in the answer.
9. **Loading state set, never reset.** Tell: a `Loading` branch sets `screenState = Loading` and the `Success` branch doesn't touch `screenState`. Counter: every state you set in `Loading` must be reset in BOTH the `Success` and the error branch.
10. **Answering from a truncated read.** Tell: the tool result was cut off. Counter: never cite or conclude past the last line you actually saw; fetch the rest.

---

## Final gate — run on every answer before sending

1. Every claim of the form "X does Y" has a same-session grep/read behind it, or is marked Likely/Assumption per §5.
2. Every part of the user's message is either done or explicitly declined (§7).
3. Every edited symbol's callers were grepped (§6), including previews and sibling screens.
4. New enum values / composable params: all `when`s and call sites handled.
5. The answer leads with the result, ends with on-device verify steps + the build instruction.
6. No comments added to generated code; no forbidden build command was run.
7. Anything unverifiable is flagged, not smoothed over.

If any item fails: fix it and re-run the gate. Never send anyway.
