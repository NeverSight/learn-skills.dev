---
name: unity-card-games
description: "Build card games in Unity: battlers, TCG/CCG boards, deckbuilders, solitaires and turn-based duels. Use for rules specs, retaliation, summoning sickness, win termination, engine-free rules cores, attack event logs, legal-move AI, mana curves, hands/decks, board lanes, card frames/backs/art, crop-to-cover composition, hand fans, DragLayer drag/drop, click/drag rule parity, orphaned drag ghosts, play/attack impact feedback, or runtime-built UI registry checks. Defers generation and promotion to unity-asset-designer, unity-image-generator, unity-asset-pipeline, unity-gameplay-systems, unity-ui-designer and unity-animation."
---

# Unity Card Games (genre layer)

Field-verified on a shipped portrait 1v1 lane battler (Lane Duel, 2026-07-02): 34 EditMode +
6 PlayMode tests green, registry-gated art, zero red build iterations. Everything here defers
to the core skills for HOW; this layer owns the card-genre WHAT.

## 1. Rules-spec gate (before ANY code — director Step 2.5 applied to cards)

Card combat has forks that silently change every test. Lock them in the spec first:

- **Retaliation:** does the defender strike back (Hearthstone mutual trade) or not (PTCG)?
- **Summoning sickness:** can a creature attack the turn it's played?
- **Targeting:** same-lane forced / free-target / taunt rules.
- **TERMINATION property (the make-or-break, measure it):** every game must provably end —
  escalating fatigue (draw from empty deck = 1,2,3… damage) bounds every game regardless of
  wall stalemates or mana lock. Prove it: seeded AI-vs-AI, 50 seeds, all terminate with a
  winner within N turns, as an EditMode test on the pure core. Run it before visuals exist.
- Attack flow: a separate ATTACK phase (resolve all lanes in fixed order) makes "already
  attacked" a WrongPhase error instead of per-creature bookkeeping — and gives the AI a
  strict act→attack→end script.

## 2. Core architecture (engine-free rules + event log)

- Rules in a `noEngineReferences` Core asmdef: CardDef table as plain C# (no ScriptableObjects
  — tests need no engine), GameState, TurnEngine state machine, seeded Fisher-Yates decks.
- **Attack resolution needs an EVENT LOG.** Pure-logic combat is instantaneous; the view
  cannot infer trades/deaths/counter-damage from before/after state. Emit an ordered
  `AttackEvent` list (attacker, target, damage, died) per resolution — the view plays it back
  as animation script. Player path: play events on pre-attack tokens, then re-render; AI path:
  render first, play feedback on survivors (dead-defender rects fall back to slot rects).
- **AI through the public engine API only**, returning a result log — "AI never makes an
  illegal move across 50 seeds" becomes one assert.
- Hand indexes go stale: engine actions take hand indexes; re-render the whole hand after
  every action (or re-index explicitly).

## 3. Card art pipeline (per unity-image-generator + unity-asset-designer + unity-asset-pipeline)

- Card illustrations/frames/backs/boards are **full-bleed opaque**: QA with
  `validate_sprite.py --illustration` (cut-out geometry checks don't apply) and contract
  **`runtime.type: ui`** (RectTransform-sized; world-space scale checks don't apply).
- Character cards: **canon-conditioned** — multi-reference Gemini input (canon sheet +
  style board), `--character` for identity injection. Cross-medium canon works: a pixel-game
  anchor + frozen identity_string produces an on-model painterly card. Family cards (chief,
  shaman of the same tribe) condition on the same canon and prompt "of the same tribe/order".
- One style board anchors the whole set; batch-generate the set in one pass and review as a
  CONTACT SHEET (per-card review misses set-level drift).
- **Frame contract must declare its window**: generated frames often bake an opaque fill into
  the "empty" art window (`alpha_is_transparency: true` + `alpha_valid: true` and still a=255
  everywhere). Decide the stack from the asset, not the plan: transparent window → art under
  frame; baked window → **frame at bottom, illustration composited OVER the measured window**.
- **Measure the frame window with a script, never by eye**: PIL flood-scan from the window
  center for the uniform fill → exact px rect → uGUI anchor fractions (flip y: uGUI is
  bottom-up). Hard-code the fractions as commented consts.
- Cost gem legibility: a cost slot below ~12% of card width is unreadable at hand scale —
  let the digit overflow the gem, or design cost into a corner plate.
- If contracts declare `runtime.prefab`, the import step MUST build them (prefab factory) or
  the registry is self-inconsistent and the gate fails on integrity.

## 4. Card UI composition (per unity-ui-designer + unity-game-layout)

- **Hand fan = anchor fractions, not pixels**: `rect.width` is 0 during Awake (no layout yet);
  per-card anchorMin/Max at `cx ± w/2`, step `min(0.19, 0.96/n)` gives an overlap-when-crowded
  fan with zero layout-timing dependence. This is what makes 4:3 ↔ 19.5:9 hold unchanged.
- **Crop-to-cover**: `RectMask2D` parent + child `AspectRatioFitter(EnvelopeParent, w/h)` for
  window art and board backgrounds; `FitInParent` for whole card faces in arbitrary slots.
- **Drag-drop rules (REVISED after a shipped ghost-card bug):** (a) `raycastTarget=false` on
  the dragged card's bg in OnBeginDrag so the drop RaycastAll doesn't hit itself; (b) reparent
  the dragged view to a dedicated **DragLayer** — a no-Graphic container kept as the canvas's
  last sibling — NEVER to the canvas root or any container outside the re-render's sweep; (c)
  resolve EVERY drag end through re-render: successful drop re-renders (which sweeps the
  DragLayer); failed drop calls the same refresh — **never snap the view back into the hand
  container** (a mid-drag re-render from the AI turn/attack playback makes snap-back a
  stale-index duplicate). Resolve targets via `GetComponentInParent<SlotView>` on raycast hits.
- **Invariant, not ordering:** every re-render clears the DragLayer unconditionally as its
  FIRST act — a dragged view is transient *by construction*. "Deferred Destroy will get it"
  reasoning is banned: the shipped ghost bug wasn't fragile ordering, the assumed destroy
  NEVER TARGETED the reparented view at all (it had left the container the rebuild sweeps —
  each drag-play orphaned exactly one card).
- **Orphan-count PlayMode assertion (REQUIRED):** after drag-play, failed drop, and END TURN
  mid-hand, live card views == the hand MODEL count (state the exact identity for your
  architecture) and DragLayer.childCount == 0. Catches the whole transient-view-leak class
  regardless of which path produced it.
- **Test every input path's VIEW lifecycle separately.** One-rules-path (drag and click funnel
  into the same handlers) covers the RULES — but drag and click have different view lifecycles
  (reparenting, raycast toggles, end-events), and a click-only test suite shipped a drag-only
  ghost bug. Simulate the real drag events (ExecuteEvents + synthesized PointerEventData).
- **One rules path**: drag AND click-fallback funnel into the same DropOnLane/DropOnHero —
  RULES tests drive the shared handlers directly; VIEW-lifecycle tests still exercise the real
  drag events (bullet above). No-target spells need an explicit gesture (drop-on-own-hero or
  second click).
- The board background is the ONE legitimate full-screen Image: exempt it from the
  no-full-screen-overlay assertion BY NAME and assert it sits at sibling index 0.
- Naming: `ART_*` (registry sprites) / `UI_*` (intentional procedural chrome) / `FX_*`
  (transient) / `PLACEHOLDER_*` strictly for awaiting-real-art.

## 5. Card feel (per unity-gameplay-systems combat stack + unity-animation composite rule)

- Card play: 0.15s scale-pop + EaseOutBack settle.
- Creature attack playback (from the Core event log): forward nudge toward target → 0.08s
  **own-clock** hitstop (`WaitForSecondsRealtime`, never timeScale — composes with AI turns
  and never stalls tests) → defender **overlay-Image flash** (uGUI `Image.color` is
  multiplicative like SpriteRenderer.color — white does NOTHING; animate a white overlay's
  alpha 0.85→0) → floating damage number (TMP, rises+fades 0.5s) → hero-panel quantized shake.
- Transient-FX screenshot evidence: pre-switch the canvas to Screen-Space-Camera BEFORE
  triggering the effect and submit the render THE SAME FRAME the FX appears — batch frames
  are slow and a 0.5s FX dies before a canvas-switch + yields capture path.

## 6. Registry teeth for runtime-built UI (per unity-asset-pipeline)

A runtime-constructed card UI is invisible to the scene-walk gate (`art_references: 0` — no
serialized m_Sprite in the scene). The teeth move to: a serialized **CardArtCatalog**
(id→sprite list, populated at EDIT time by the scene builder from Approved paths — never
Resources.Load), plus a post-save reload verification that every catalog entry resolves.
Registry-only art = catalog-only art + the catalog verified against the registry.

## Where this sits

Pairs with `unity-game-director` (routing), `unity-image-generator`/`unity-asset-designer`
(card art + canon), `unity-asset-pipeline` (contracts/registry/import), `unity-ui-designer`
(safe area, panels, thumb zones), `unity-gameplay-systems` (core architecture, feel),
`unity-animation` (impact composite doctrine), `unity-qa-release` (test/build).
